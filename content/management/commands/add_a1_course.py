from django.core.management.base import BaseCommand

from content import exam_a1
from content.course_a1 import install
from content.models import (
    ExamPart, Lesson, Level, PracticeSet, Section, SpeakingTask, Topic, VocabularyItem, WritingTask,
)


class Command(BaseCommand):
    help = ("Add the lessons of Dhruv's A1 course and the A1 exam practice sets that aren't on the site yet "
            "(never changes existing ones).")

    def handle(self, *args, **options):
        if not Level.objects.filter(code="A1").exists():
            self.stdout.write(self.style.WARNING("There is no level A1 yet. Run seed_content first."))
            return
        added = install(Level, Section, Lesson, Topic, VocabularyItem, SpeakingTask, PracticeSet, WritingTask)
        if added:
            self.stdout.write(self.style.SUCCESS("Added: " + ", ".join(added)))
        else:
            self.stdout.write("All lessons are already there; nothing changed.")
        from content.course_a1 import add_examples

        add_examples(Section, PracticeSet)
        exam_a1.add_examples(ExamPart)
        exams = exam_a1.install(Level, ExamPart)
        if exams:
            self.stdout.write(self.style.SUCCESS("Exam practice added: " + ", ".join(exams)))
        else:
            self.stdout.write("Exam practice is already there; nothing changed.")
