"""Exam practice: sets laid out like the Goethe / telc exam parts, with results saved per student."""
import io

from django.core.management import call_command

from content import exam_a1
from content.models import ExamPart, Level
from learning.models import ExamResult

from .test_api_accounts import ApiCase


class ExamDataTests(ApiCase):
    def test_our_sets_are_valid_and_install_once(self):
        for p in exam_a1.PARTS:
            self.assertEqual(exam_a1.clean_items(p["kind"], p["items"], p.get("text", "")), [], p["slug"])
        exam_a1.install(Level, ExamPart)
        count = ExamPart.objects.count()
        self.assertGreaterEqual(count, len(exam_a1.PARTS))
        self.assertEqual(exam_a1.install(Level, ExamPart), [])  # nothing added twice
        self.assertEqual(ExamPart.objects.count(), count)

    def test_bad_questions_are_reported(self):
        self.assertEqual(exam_a1.clean_items("listen", []), ["Add at least one question."])
        problems = exam_a1.clean_items("listen", [{"q": "Wann?", "audio": "", "options": ["a", ""], "answer": 4}])
        self.assertTrue(any("nothing to listen" in p for p in problems))
        self.assertTrue(any("none of them empty" in p for p in problems))
        problems = exam_a1.clean_items("tf", [{"q": "Satz", "answer": "ja"}], text="")
        self.assertTrue(any("reading text" in p for p in problems))
        self.assertTrue(any("richtig or falsch" in p for p in problems))

    def test_command_adds_exam_practice(self):
        ExamPart.objects.all().delete()
        out = io.StringIO()
        call_command("add_a1_course", stdout=out)
        self.assertIn("Exam practice added", out.getvalue())
        self.assertEqual(ExamPart.objects.count(), len(exam_a1.PARTS))


class StudentExamTests(ApiCase):
    def setUp(self):
        super().setUp()
        exam_a1.install(Level, ExamPart)
        self.listen = ExamPart.objects.get(slug="hoeren-1-kurze-gespraeche-1")
        self.client.force_login(self.student)

    def test_overview_lists_exam_modules_and_parts(self):
        d = self.get("/exams/").json()
        self.assertEqual(d["level"]["code"], "A1")
        goethe = next(e for e in d["exams"] if e["id"] == "goethe")
        self.assertEqual(goethe["name"], "Goethe-Zertifikat A1")
        keys = [m["key"] for m in goethe["modules"]]
        self.assertEqual(keys[:2], ["hoeren", "lesen"])
        self.assertIsNone(goethe["modules"][0]["parts"][0]["best"])

    def test_open_a_part_and_save_results_keeping_the_best(self):
        d = self.get(f"/exams/parts/{self.listen.pk}/").json()["part"]
        self.assertEqual(d["kind"], "listen")
        self.assertEqual(len(d["items"]), 4)
        r = self.post(f"/exams/parts/{self.listen.pk}/result/", {"score": 3, "timed": True}).json()
        self.assertEqual((r["score"], r["total"], r["best"]), (3, 4, 3))
        r = self.post(f"/exams/parts/{self.listen.pk}/result/", {"score": 99}).json()
        self.assertEqual(r["score"], 4)  # capped at the number of questions
        r = self.post(f"/exams/parts/{self.listen.pk}/result/", {"score": 1}).json()
        self.assertEqual(r["best"], 4)
        self.assertEqual(ExamResult.objects.filter(user=self.student).count(), 3)
        part = next(e for e in self.get("/exams/").json()["exams"] if e["id"] == "goethe")["modules"][0]["parts"][0]
        self.assertEqual(part["best"], 100)
        self.assertEqual(self.post(f"/exams/parts/{self.listen.pk}/result/", {"score": "viel"}).status_code, 400)

    def test_drafts_and_other_levels_are_hidden_from_students(self):
        self.listen.is_published = False
        self.listen.save()
        self.assertEqual(self.get(f"/exams/parts/{self.listen.pk}/").status_code, 404)
        self.assertNotIn(self.listen.pk, [p["id"] for e in self.get("/exams/").json()["exams"]
                                          for m in e["modules"] for p in m["parts"]])
        b1 = ExamPart.objects.create(level=self.a2, exam="goethe", module="lesen", teil=1, slug="x", title="A2 Text",
                                     instructions="Lesen Sie.", kind="tf", text="Hallo", items=[{"q": "S", "answer": True}])
        self.assertEqual(self.get(f"/exams/parts/{b1.pk}/").status_code, 404)

    def test_teacher_sees_drafts(self):
        self.listen.is_published = False
        self.listen.save()
        self.client.force_login(self.teacher)
        self.assertEqual(self.get(f"/exams/parts/{self.listen.pk}/").status_code, 200)

    def test_guests_and_waiting_students_are_kept_out(self):
        self.client.logout()
        self.assertIn(self.get("/exams/").status_code, (401, 403))
        self.client.force_login(self.waiting)
        self.assertIn(self.get("/exams/").status_code, (401, 403))
