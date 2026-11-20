"""Lektionen become practice areas: the Lektionen already on the site count as taught (so
students keep what they can open), and Lektion 1-3 get their practice sets and writing tasks."""
from django.db import migrations
from django.utils import timezone


def forwards(apps, schema_editor):
    from content.course_a1 import install

    Section = apps.get_model("content", "Section")
    Section.objects.filter(is_visible=True).update(is_taught=True, taught_at=timezone.now())
    m = lambda name: apps.get_model("content", name)
    install(m("Level"), Section, m("Lesson"), m("Topic"), m("VocabularyItem"), m("SpeakingTask"),
            m("PracticeSet"), m("WritingTask"))
    # "Spell your name" and the speaking task were on Lektion 1's old Übungen page: move them to "Das Alphabet".
    Lesson = m("Lesson")
    old = Lesson.objects.filter(section__title="Lektion 1: Alphabet & Aussprache", title__startswith="Übungen (old").first()
    page = Lesson.objects.filter(section__title="Lektion 1: Alphabet & Aussprache", title="Das Alphabet").first()
    if old and page and not any(b.get("type") == "spell_name" for b in page.blocks):
        page.blocks = page.blocks + [b for b in old.blocks if b.get("type") in ("spell_name", "speaking")]
        page.save()


class Migration(migrations.Migration):
    dependencies = [("content", "0009_lektion_practice_writing")]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
