"""Adds the first A1 exam practice sets (Goethe: Hören Teil 1, Lesen Teil 1). Never changes
sets that already exist."""
from django.db import migrations


def add(apps, schema_editor):
    from content.exam_a1 import install

    install(apps.get_model("content", "Level"), apps.get_model("content", "ExamPart"))


class Migration(migrations.Migration):
    dependencies = [("content", "0007_exam_parts")]

    operations = [migrations.RunPython(add, migrations.RunPython.noop)]
