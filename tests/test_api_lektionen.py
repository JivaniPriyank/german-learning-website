"""Lektionen as practice areas: open once taught, practice sets with results, writing tasks the teacher checks."""
import io

from django.core.management import call_command

from content import course_a1
from content.models import Lesson, PracticeSet, Section, WritingTask
from content.practice import clean_example, clean_set, time_limit
from learning.models import PracticeResult, WritingAnswer

from .test_api_accounts import ApiCase


class CourseContentTests(ApiCase):
    def test_every_course_set_is_valid(self):
        for lektion in course_a1.COURSE:
            for s in lektion["sets"]:
                self.assertEqual(clean_set(s["kind"], s["items"], s["text"]), [], f"{lektion['title']} · {s['title']}")
            self.assertTrue(lektion["writing"])

    def test_every_course_set_has_a_worked_example(self):
        for lektion in course_a1.COURSE:
            for s in lektion["sets"]:
                name = f"{lektion['title']} · {s['title']}"
                self.assertTrue(s.get("example"), name)
                self.assertEqual(clean_example(s["kind"], s["example"], s["text"]), [], name)
                self.assertNotIn(s["example"], s["items"], name)  # never gives away a real question

    def test_bad_sets_are_reported(self):
        self.assertEqual(clean_set("choice", []), ["Add at least one question."])
        self.assertIn("Unknown kind", clean_set("essay", [{}])[0])
        p = clean_set("choice", [{"prompt": "?", "options": ["a", ""], "answer": 0}, {"clock": "7:30", "options": ["a", "b"], "answer": 5}])
        self.assertTrue(any("none of them empty" in x for x in p))
        self.assertTrue(any("07:30" in x for x in p))
        self.assertTrue(any("no right answer" in x for x in p))
        self.assertTrue(clean_set("blanks", [{"before": "Ich", "answer": "|"}]))
        self.assertTrue(clean_set("tf", [{"prompt": "x", "answer": True}], text=""))
        self.assertTrue(clean_set("listen_type", [{"say": "", "answer": "1"}]))


class LektionTests(ApiCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        call_command("add_a1_course", stdout=io.StringIO())
        cls.l1 = Section.objects.get(title__startswith="Lektion 1")
        cls.l2 = Section.objects.get(title__startswith="Lektion 2")
        cls.set1 = cls.l1.practice_sets.get(title="Übung 1: Lückentext")
        cls.task = cls.l1.writing_tasks.first()
        cls.page = cls.l1.lessons.get(title="Das Alphabet")

    def setUp(self):
        super().setUp()
        self.client.force_login(self.student)

    def teach(self, section, taught=True):
        self.client.force_login(self.teacher)
        r = self.post(f"/teacher/lektionen/{section.pk}/taught/", {"taught": taught})
        self.assertEqual(r.status_code, 200)
        self.client.force_login(self.student)
        return r.json()

    def test_lektionen_stay_closed_until_taught(self):
        rows = {x["title"]: x for x in self.get("/lektionen/").json()["lektionen"]}
        self.assertFalse(rows[self.l1.title]["is_taught"])
        self.assertEqual(rows[self.l1.title]["sets"], 5)
        r = self.get(f"/lektionen/{self.l1.pk}/")
        self.assertEqual((r.status_code, r.json()["code"]), (403, "not_taught"))
        self.assertEqual(self.get(f"/practice-sets/{self.set1.pk}/").status_code, 404)
        self.assertEqual(self.get(f"/lessons/{self.page.pk}/").status_code, 404)
        self.assertEqual(self.post(f"/writing/{self.task.pk}/", {"text": "Ah"}).status_code, 404)
        # the student can't open it themselves
        self.assertEqual(self.post(f"/teacher/lektionen/{self.l1.pk}/taught/", {"taught": True}).status_code, 403)
        res = self.teach(self.l1)
        self.assertTrue(res["is_taught"])
        self.assertIn("can open it now", res["message"])
        d = self.get(f"/lektionen/{self.l1.pk}/").json()
        self.assertEqual(len(d["sets"]), 5)
        self.assertEqual(d["sets"][0]["source"], "lesson")
        self.assertEqual(len(d["words"]), 20)
        self.assertEqual(len(d["writing"]), 6)
        self.assertNotIn("Übungen", [p["title"] for p in d["pages"]])
        self.assertEqual(self.get(f"/lessons/{self.page.pk}/").status_code, 200)
        # closed again
        self.teach(self.l1, taught=False)
        self.assertEqual(self.get(f"/lektionen/{self.l1.pk}/").status_code, 403)

    def test_teacher_always_sees_everything(self):
        self.client.force_login(self.teacher)
        self.assertEqual(self.get(f"/lektionen/{self.l2.pk}/").status_code, 200)
        self.assertEqual(self.get(f"/practice-sets/{self.set1.pk}/").status_code, 200)

    def test_practice_results_keep_the_best(self):
        self.teach(self.l1)
        d = self.get(f"/practice-sets/{self.set1.pk}/").json()["set"]
        self.assertEqual((d["kind"], len(d["items"]), d["seconds"]), ("blanks", 5, time_limit(self.set1)))
        self.assertEqual(d["example"]["answer"], "ä")  # the worked example comes with the set
        r = self.post(f"/practice-sets/{self.set1.pk}/result/", {"score": 3, "timed": True}).json()
        self.assertEqual((r["score"], r["total"], r["best"]), (3, 5, 60))
        self.assertEqual(self.post(f"/practice-sets/{self.set1.pk}/result/", {"score": 50}).json()["score"], 5)
        self.assertEqual(self.post(f"/practice-sets/{self.set1.pk}/result/", {"score": 1}).json()["best"], 100)
        self.assertEqual(self.post(f"/practice-sets/{self.set1.pk}/result/", {"score": "x"}).status_code, 400)
        self.assertEqual(PracticeResult.objects.filter(user=self.student).count(), 3)
        row = next(x for x in self.get("/lektionen/").json()["lektionen"] if x["id"] == self.l1.pk)
        self.assertEqual((row["sets_done"], row["sets"]), (1, 5))
        sets = self.get(f"/lektionen/{self.l1.pk}/").json()["sets"]
        self.assertEqual(sets[0]["best"], 100)
        self.assertEqual(self.get("/lektionen/").json()["streak"], 1)  # practising counts as a day

    def test_draft_sets_are_hidden(self):
        self.teach(self.l1)
        PracticeSet.objects.filter(pk=self.set1.pk).update(is_published=False)
        self.assertEqual(self.get(f"/practice-sets/{self.set1.pk}/").status_code, 404)
        self.assertEqual(len(self.get(f"/lektionen/{self.l1.pk}/").json()["sets"]), 4)

    def test_writing_answer_checked_by_teacher(self):
        self.teach(self.l1)
        self.assertEqual(self.post(f"/writing/{self.task.pk}/", {"text": "  "}).status_code, 400)
        r = self.post(f"/writing/{self.task.pk}/", {"text": "Ah-En-En-Ah"})
        self.assertEqual(r.json()["task"]["answer"]["status"], "waiting")
        # the teacher sees it waiting, with a count in the menu
        self.client.force_login(self.teacher)
        self.assertEqual(self.get("/session/").json()["counts"]["writing_waiting"], 1)
        inbox = self.get("/teacher/writing/").json()
        self.assertEqual(inbox["answers"][0]["text"], "Ah-En-En-Ah")
        aid = inbox["answers"][0]["id"]
        self.assertEqual(self.post(f"/teacher/writing/{aid}/", {"feedback": ""}).status_code, 400)
        r = self.post(f"/teacher/writing/{aid}/", {"feedback": "Sehr gut!"}).json()
        self.assertEqual(r["answer"]["status"], "checked")
        self.assertIsNone(r["next"])
        self.assertEqual(self.get("/teacher/writing/?show=checked").json()["answers"][0]["feedback"], "Sehr gut!")
        # the student sees the comment, also on their home page
        self.client.force_login(self.student)
        task = next(t for t in self.get(f"/lektionen/{self.l1.pk}/").json()["writing"] if t["id"] == self.task.pk)
        self.assertEqual(task["answer"]["feedback"], "Sehr gut!")
        self.assertEqual(self.get("/lektionen/").json()["feedback"][0]["feedback"], "Sehr gut!")
        # sending again asks for a new check
        self.post(f"/writing/{self.task.pk}/", {"text": "Anna: Ah-En-En-Ah"})
        a = WritingAnswer.objects.get(user=self.student, task=self.task)
        self.assertEqual((a.status, a.feedback), ("waiting", ""))
        self.assertEqual(WritingAnswer.objects.count(), 1)

    def test_students_cant_use_the_teacher_inbox(self):
        self.assertEqual(self.get("/teacher/writing/").status_code, 403)

    def test_hidden_section_and_other_level(self):
        self.teach(self.l1)
        Section.objects.filter(pk=self.l1.pk).update(is_visible=False)
        self.assertEqual(self.get(f"/lektionen/{self.l1.pk}/").status_code, 404)
        a2 = Section.objects.create(level=self.a2, title="A2 Lektion", is_taught=True)
        self.assertEqual(self.get(f"/lektionen/{a2.pk}/").status_code, 404)

    def test_old_exercise_pages_become_hidden_drafts(self):
        # A site that still had the old "Übungen" page: install moves it aside, once.
        PracticeSet.objects.filter(section=self.l2).delete()
        WritingTask.objects.filter(section=self.l2).delete()
        Lesson.objects.create(section=self.l2, title="Übungen", is_published=True, blocks=[])
        call_command("add_a1_course", stdout=io.StringIO())
        old = self.l2.lessons.get(title__startswith="Übungen (old")
        self.assertFalse(old.is_published)
        self.assertEqual(self.l2.practice_sets.count(), 7)
        self.assertEqual(self.l2.writing_tasks.count(), 6)
