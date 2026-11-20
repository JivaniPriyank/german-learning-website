"""Adds Lektion 3 of Dhruv's A1 course (and any earlier lesson still missing). Never changes
sections that already exist."""
from django.db import migrations


def add(apps, schema_editor):
    from content.course_a1 import install

    m = lambda name: apps.get_model("content", name)
    install(m("Level"), m("Section"), m("Lesson"), m("Topic"), m("VocabularyItem"), m("SpeakingTask"))


class Migration(migrations.Migration):
    dependencies = [("content", "0005_a1_course_lektion_1_2")]

    operations = [migrations.RunPython(add, migrations.RunPython.noop)]
