"""Exam practice: sets laid out like the Goethe / telc exam parts, with instant results."""
from django.db.models import Max
from django.http import Http404
from django.shortcuts import get_object_or_404

from content.models import ExamPart
from learning import services
from learning.models import ExamResult

from .utils import approved_required, body, fail, methods, ok

EXAM_INFO = {
    "goethe": {"name": "Goethe-Zertifikat", "sub": "Start Deutsch"},
    "telc": {"name": "telc Deutsch", "sub": "Start Deutsch telc"},
}
MODULE_TIME = {"hoeren": 20, "lesen": 25, "schreiben": 20, "sprechen": 15}


def _parts(request, level):
    qs = ExamPart.objects.filter(level=level)
    return qs if request.user.is_teacher else qs.filter(is_published=True)


def _part_row(p, best):
    return {"id": p.pk, "teil": p.teil, "title": p.title, "kind": p.kind, "questions": len(p.items),
            "minutes": p.minutes, "is_published": p.is_published, "best": best.get(p.pk)}


@approved_required
@methods("GET")
def exams(request):
    """The exams of the level being studied, each with its modules and practice sets."""
    level = services.current_level(request.user)
    if level is None:
        return ok({"level": None, "exams": []})
    parts = list(_parts(request, level))
    best = {}
    for r in (ExamResult.objects.filter(user=request.user, part__in=parts)
              .values("part").annotate(best=Max("score"))):
        best[r["part"]] = r["best"]
    totals = {p.pk: len(p.items) for p in parts}
    best = {pk: round(score * 100 / totals[pk]) if totals[pk] else 0 for pk, score in best.items()}
    out = []
    for code, label in ExamPart.Exam.choices:
        mine = [p for p in parts if p.exam == code]
        if not mine:
            continue
        modules = []
        for key, name in ExamPart.Module.choices:
            sets = [p for p in mine if p.module == key]
            if sets:
                modules.append({"key": key, "name": name, "minutes": MODULE_TIME[key],
                                "teile": sorted({p.teil for p in sets}),
                                "parts": [_part_row(p, best) for p in sets]})
        out.append({"id": code, "name": f"{EXAM_INFO[code]['name']} {level.code}",
                    "sub": f"{EXAM_INFO[code]['sub']} {level.code[-1]}" if level.code.startswith("A") else "",
                    "modules": modules})
    return ok({"level": {"code": level.code, "name": level.name}, "exams": out})


def _student_part(request, pk):
    part = get_object_or_404(ExamPart.objects.select_related("level"), pk=pk)
    if not request.user.can_see_level(part.level) or (not part.is_published and not request.user.is_teacher):
        raise Http404
    return part


@approved_required
@methods("GET")
def exam_part(request, pk):
    p = _student_part(request, pk)
    scores = ExamResult.objects.filter(user=request.user, part=p).aggregate(best=Max("score"))
    return ok({"part": {
        "id": p.pk, "exam": p.exam, "exam_name": f"{EXAM_INFO[p.exam]['name']} {p.level.code}",
        "module": p.module, "module_name": p.get_module_display(), "teil": p.teil, "title": p.title,
        "instructions": p.instructions, "kind": p.kind, "text": p.text, "items": p.items, "example": p.example or None,
        "minutes": p.minutes, "is_published": p.is_published, "best": scores["best"]}})


@approved_required
@methods("POST")
def exam_result(request, pk):
    """POST {score, timed}: save a finished go at a practice set."""
    p = _student_part(request, pk)
    data = body(request)
    total = len(p.items)
    try:
        score = max(0, min(int(data.get("score") or 0), total))
    except (TypeError, ValueError):
        return fail("The score must be a number.")
    ExamResult.objects.create(user=request.user, part=p, score=score, total=total, timed=bool(data.get("timed")))
    best = ExamResult.objects.filter(user=request.user, part=p).aggregate(best=Max("score"))["best"]
    return ok({"score": score, "total": total, "best": best})
