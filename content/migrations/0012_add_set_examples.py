"""Every practice set and exam part gets a worked example shown before the questions."""
from django.db import migrations


def forwards(apps, schema_editor):
    from content import course_a1, exam_a1

    course_a1.add_examples(apps.get_model("content", "Section"), apps.get_model("content", "PracticeSet"))
    exam_a1.add_examples(apps.get_model("content", "ExamPart"))


class Migration(migrations.Migration):
    dependencies = [("content", "0011_set_examples")]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
