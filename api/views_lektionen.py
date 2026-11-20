"""The Lektionen: the course taught on Zoom, revised here.

Students: the list of Lektionen (open once taught), a Lektion's practice sets, rule pages,
words and writing tasks; results of practice sets; writing answers sent to the teacher.
Teacher: mark a Lektion as taught, check writing answers.
"""
from django.db.models import Count, Max, Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone

from content import blocks as B
from content.models import Lesson, PracticeSet, Section, WritingTask
from content.practice import time_limit
from learning import services
from learning.models import PracticeResult, VideoView, WritingAnswer

from .utils import approved_required, body, fail, methods, ok, teacher_required

MAX_ANSWER = 5000


def _lektionen(user, level):
    qs = Section.objects.filter(level=level).select_related("level")
    return qs if user.is_teacher else qs.filter(is_visible=True)


def _best_by_set(user, sets):
    """{set id: best score in percent} for the sets this student has finished."""
    rows = (PracticeResult.objects.filter(user=user, practice_set__in=sets)
            .values("practice_set").annotate(best=Max("score"), total=Max("total")))
    return {r["practice_set"]: round(r["best"] * 100 / r["total"]) if r["total"] else 0 for r in rows}


def _published(qs, user):
    return qs if user.is_teacher else qs.filter(is_published=True)


# ---------------- student: list and one Lektion ----------------
@approved_required
@methods("GET")
def lektionen(request):
    user = request.user
    level = services.current_level(user)
    if level is None:
        return ok({"level": None, "lektionen": [], "feedback": []})
    sections = list(_lektionen(user, level).annotate(
        n_sets=Count("practice_sets", filter=Q(practice_sets__is_published=True), distinct=True),
        n_writing=Count("writing_tasks", filter=Q(writing_tasks__is_published=True), distinct=True),
        n_words=Count("topic__items", distinct=True)))
    sets = PracticeSet.objects.filter(section__in=sections, is_published=True)
    done_sets = set(PracticeResult.objects.filter(user=user, practice_set__in=sets).values_list("practice_set", flat=True))
    set_section = dict(sets.values_list("pk", "section_id"))
    done_by_section = {}
    for set_id in done_sets:
        done_by_section[set_section[set_id]] = done_by_section.get(set_section[set_id], 0) + 1
    rows = [{"id": x.pk, "title": x.title, "description": x.description, "icon": x.icon, "is_visible": x.is_visible,
             "is_taught": x.is_taught, "taught_at": x.taught_at, "sets": x.n_sets, "sets_done": done_by_section.get(x.pk, 0),
             "writing": x.n_writing, "words": x.n_words} for x in sections]
    feedback = (WritingAnswer.objects.filter(user=user, checked_at__isnull=False, task__section__level=level)
                .select_related("task", "task__section").order_by("-checked_at")[:3])
    watched = VideoView.objects.filter(user=user, watched_at__isnull=False).values_list("video_id", flat=True)
    new_videos = services.visible_videos(user).filter(level=level).exclude(pk__in=list(watched))[:3]
    return ok({"level": {"code": level.code, "name": level.name}, "lektionen": rows, "streak": services.streak(user),
               "new_videos": [{"id": v.pk, "title": v.title} for v in new_videos],
               "feedback": [{"id": a.pk, "task": a.task.title, "section": a.task.section_id,
                             "section_title": a.task.section.title, "feedback": a.feedback, "checked_at": a.checked_at}
                            for a in feedback]})


def _open_section(request, pk):
    """A Lektion the user may open: visible, at a level they can see, and taught (teacher: always)."""
    sec = get_object_or_404(Section.objects.select_related("level", "topic"), pk=pk)
    user = request.user
    if user.is_teacher:
        return sec
    if not sec.is_visible or not user.can_see_level(sec.level):
        raise Http404
    return sec


def _not_taught(sec):
    return fail(f"{sec.title} opens after it has been taught in class.", status=403, code="not_taught")


@approved_required
@methods("GET")
def lektion(request, pk):
    user = request.user
    sec = _open_section(request, pk)
    if not sec.is_taught and not user.is_teacher:
        return _not_taught(sec)
    sets = list(_published(sec.practice_sets.all(), user))
    best = _best_by_set(user, sets)
    pages = list(_published(sec.lessons.all(), user))
    tasks = list(_published(sec.writing_tasks.all(), user))
    answers = {a.task_id: a for a in WritingAnswer.objects.filter(user=user, task__in=tasks)}
    words = list(sec.topic.items.all()) if sec.topic else []
    return ok({
        "section": {"id": sec.pk, "title": sec.title, "description": sec.description, "icon": sec.icon,
                    "level": sec.level.code, "goals": sec.goals or [], "is_taught": sec.is_taught,
                    "taught_at": sec.taught_at, "is_visible": sec.is_visible},
        "sets": [{"id": x.pk, "title": x.title, "source": x.source, "kind": x.kind, "questions": len(x.items), "seconds": time_limit(x),
                  "is_published": x.is_published, "best": best.get(x.pk)} for x in sets],
        "pages": [{"id": x.pk, "title": x.title, "is_published": x.is_published, "summary": B.summary(x.blocks)} for x in pages],
        "words": [{"article": w.article, "german": w.german, "english": w.english, "extra": w.extra} for w in words],
        "topic": {"level": sec.topic.level.code, "slug": sec.topic.slug, "name": sec.topic.name} if sec.topic else None,
        "writing": [_task(t, answers.get(t.pk)) for t in tasks],
    })


def _task(t, answer):
    return {"id": t.pk, "title": t.title, "source": t.source, "prompt": t.prompt, "is_published": t.is_published,
            "answer": None if answer is None else {"text": answer.text, "status": answer.status, "submitted_at": answer.submitted_at,
                                                   "feedback": answer.feedback, "checked_at": answer.checked_at}}


def _open_set(request, pk):
    ps = get_object_or_404(PracticeSet.objects.select_related("section", "section__level"), pk=pk)
    sec = _open_section(request, ps.section_id)
    if not request.user.is_teacher and (not ps.is_published or not sec.is_taught):
        raise Http404
    return ps


@approved_required
@methods("GET")
def practice_set(request, pk):
    ps = _open_set(request, pk)
    best = _best_by_set(request.user, [ps]).get(ps.pk)
    return ok({"set": {"id": ps.pk, "title": ps.title, "source": ps.source, "kind": ps.kind, "intro": ps.intro,
                       "text": ps.text, "items": ps.items, "example": ps.example or None, "seconds": time_limit(ps), "best": best,
                       "is_published": ps.is_published},
               "section": {"id": ps.section_id, "title": ps.section.title}})


@approved_required
@methods("POST")
def practice_result(request, pk):
    """POST {score, timed}: save a finished go at a practice set."""
    ps = _open_set(request, pk)
    data = body(request)
    total = len(ps.items)
    try:
        score = max(0, min(int(data.get("score") or 0), total))
    except (TypeError, ValueError):
        return fail("The score must be a number.")
    PracticeResult.objects.create(user=request.user, practice_set=ps, score=score, total=total, timed=bool(data.get("timed")))
    return ok({"score": score, "total": total, "best": _best_by_set(request.user, [ps]).get(ps.pk)})


@approved_required
@methods("POST")
def writing_answer(request, pk):
    """POST {text}: send (or send again) an answer to a writing task for the teacher to check."""
    task = get_object_or_404(WritingTask.objects.select_related("section"), pk=pk)
    sec = _open_section(request, task.section_id)
    if not request.user.is_teacher and (not task.is_published or not sec.is_taught):
        raise Http404
    text = str(body(request).get("text") or "").strip()
    if not text:
        return fail("Write your answer first.", errors={"text": ["Write your answer first."]})
    if len(text) > MAX_ANSWER:
        return fail(f"Your answer can be at most {MAX_ANSWER} characters.", errors={"text": ["Too long."]})
    answer, _ = WritingAnswer.objects.update_or_create(
        user=request.user, task=task,
        defaults={"text": text, "submitted_at": timezone.now(), "feedback": "", "checked_at": None, "checked_by": None})
    return ok({"task": _task(task, answer), "message": "Sent. Your teacher will check it."})


# ---------------- teacher ----------------
@teacher_required
@methods("POST")
def mark_taught(request, pk):
    """POST {taught: true|false}: open a Lektion for students after the class (or close it again)."""
    sec = get_object_or_404(Section, pk=pk)
    taught = bool(body(request).get("taught"))
    sec.is_taught = taught
    sec.taught_at = timezone.now() if taught else None
    sec.save(update_fields=["is_taught", "taught_at"])
    return ok({"id": sec.pk, "is_taught": sec.is_taught, "taught_at": sec.taught_at,
               "message": f"{sec.title}: students can open it now." if taught else f"{sec.title} is closed for students again."})


def _answer_row(a):
    return {"id": a.pk, "student": {"id": a.user_id, "name": a.user.full_name or a.user.email},
            "task": {"id": a.task_id, "title": a.task.title, "prompt": a.task.prompt, "source": a.task.source},
            "section": {"id": a.task.section_id, "title": a.task.section.title},
            "text": a.text, "submitted_at": a.submitted_at, "feedback": a.feedback, "checked_at": a.checked_at,
            "status": a.status}


@teacher_required
@methods("GET")
def writing_inbox(request):
    show = request.GET.get("show", "waiting")
    qs = WritingAnswer.objects.select_related("user", "task", "task__section")
    qs = qs.filter(checked_at__isnull=True).order_by("submitted_at") if show == "waiting" else qs.filter(checked_at__isnull=False).order_by("-checked_at")
    return ok({"show": show, "answers": [_answer_row(a) for a in qs[:200]],
               "waiting": WritingAnswer.objects.filter(checked_at__isnull=True).count()})


@teacher_required
@methods("GET", "POST")
def writing_check(request, pk):
    """GET: one answer. POST {feedback}: save the comment and mark the answer as checked."""
    a = get_object_or_404(WritingAnswer.objects.select_related("user", "task", "task__section"), pk=pk)
    if request.method == "POST":
        feedback = str(body(request).get("feedback") or "").strip()
        if not feedback:
            return fail("Write a short comment for the student.", errors={"feedback": ["Write a short comment for the student."]})
        if len(feedback) > MAX_ANSWER:
            return fail(f"The comment can be at most {MAX_ANSWER} characters.", errors={"feedback": ["Too long."]})
        a.feedback, a.checked_at, a.checked_by = feedback, timezone.now(), request.user
        a.save(update_fields=["feedback", "checked_at", "checked_by"])
        nxt = WritingAnswer.objects.filter(checked_at__isnull=True).order_by("submitted_at").first()
        return ok({"answer": _answer_row(a), "next": nxt.pk if nxt else None, "message": "Checked. The student can see your comment."})
    return ok({"answer": _answer_row(a)})


def writing_waiting_count():
    return WritingAnswer.objects.filter(checked_at__isnull=True).count()


def lektion_page_allowed(request, lesson):
    """Rule pages of a Lektion follow the same 'taught' rule as the Lektion."""
    return request.user.is_teacher or lesson.section.is_taught


__all__ = ["lektionen", "lektion", "practice_set", "practice_result", "writing_answer", "mark_taught",
           "writing_inbox", "writing_check", "writing_waiting_count", "lektion_page_allowed", "Lesson"]
