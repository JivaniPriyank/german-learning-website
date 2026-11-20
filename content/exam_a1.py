"""Exam practice for A1, laid out like the Goethe / telc exam but with our own texts.

The topics follow Dhruv's course (Lektion 1-3: spelling, numbers, time, days), so students
practise the exam format with words they already know.

Shapes of `items`:
  kind "listen": {"q": question, "audio": what the voice reads, "options": [a, b, c],
                  "answer": index of the right option, "explain": why}
  kind "tf":     {"q": statement, "answer": true/false, "explain": why}
"""

PARTS = [
    {
        "exam": "goethe", "module": "hoeren", "teil": 1, "slug": "hoeren-1-kurze-gespraeche-1",
        "title": "Kurze Gespräche", "kind": "listen", "minutes": 4,
        "example": {"q": "Wie heißt der Mann?", "audio": "Guten Tag, wie heißen Sie? — Ich heiße Peter Braun.",
                    "options": ["Peter Braun", "Paul Braun", "Peter Brandt"], "answer": 0, "explain": "Er sagt: Ich heiße Peter Braun."},
        "instructions": "Sie hören kurze Gespräche. Wählen Sie a, b oder c. Sie hören jeden Text zweimal.",
        "items": [
            {"q": "Wann beginnt der Deutschkurs?",
             "audio": "Entschuldigung, wann beginnt der Deutschkurs? — Am Montag, um Viertel nach neun. — Um Viertel nach neun. Danke schön!",
             "options": ["9:15 Uhr", "9:45 Uhr", "8:45 Uhr"], "answer": 0,
             "explain": "Viertel nach neun = 9:15. Viertel vor zehn wäre 9:45."},
            {"q": "Wie heißt die Frau mit Nachnamen?",
             "audio": "Wie ist Ihr Name, bitte? — Kowalski. — Wie schreibt man das? — Ka, Oh, Weh, Ah, El, Es, Ka, Ih.",
             "options": ["Kovalski", "Kowalski", "Kowalsky"], "answer": 1,
             "explain": "„Weh“ ist W, und am Ende hört man „Ih“, also I."},
            {"q": "Welche Telefonnummer hat Herr Braun?",
             "audio": "Herr Braun, wie ist Ihre Telefonnummer? — Null, eins, sieben, sechs, dreiundvierzig, achtundsechzig.",
             "options": ["0176 34 86", "0176 43 68", "0167 43 68"], "answer": 1,
             "explain": "dreiundvierzig = 43: Im Deutschen sagt man zuerst die Einer, dann die Zehner."},
            {"q": "Wann hat die Frau einen Termin beim Arzt?",
             "audio": "Praxis Doktor Weber, guten Tag. — Guten Tag, ich brauche einen Termin. Geht es am Mittwoch? — Am Mittwoch leider nicht. Aber am Donnerstag um halb elf. — Gut, Donnerstag um halb elf.",
             "options": ["Mittwoch, 10:30 Uhr", "Donnerstag, 10:30 Uhr", "Donnerstag, 11:30 Uhr"], "answer": 1,
             "explain": "Halb elf = 10:30, eine halbe Stunde vor elf. Mittwoch geht nicht."},
        ],
    },
    {
        "exam": "goethe", "module": "lesen", "teil": 1, "slug": "lesen-1-e-mail-1",
        "title": "Eine E-Mail", "kind": "tf", "minutes": 5,
        "example": {"q": "Lena macht einen Deutschkurs.", "answer": True, "explain": "„ab Montag mache ich einen Deutschkurs“"},
        "instructions": "Lesen Sie die E-Mail. Sind die Sätze richtig oder falsch?",
        "text": ("Hallo Tom,\n"
                 "ab Montag mache ich einen Deutschkurs! Der Kurs ist von Montag bis Donnerstag, immer von 18 Uhr "
                 "bis halb neun. Freitags habe ich frei. Mein Lehrer heißt Herr Wagner, er kommt aus Hamburg.\n"
                 "Am Samstag, den 14. März, machen wir eine Party in der Schule. Kommst du mit?\n"
                 "Meine neue Handynummer ist 0176 52 31 90.\n"
                 "Viele Grüße\nLena"),
        "items": [
            {"q": "Lena hat fünf Tage in der Woche Kurs.", "answer": False, "explain": "Montag bis Donnerstag sind vier Tage."},
            {"q": "Der Kurs ist um 20:30 Uhr zu Ende.", "answer": True, "explain": "Halb neun am Abend = 20:30 Uhr."},
            {"q": "Herr Wagner kommt aus München.", "answer": False, "explain": "Er kommt aus Hamburg."},
            {"q": "Die Party ist an einem Samstag.", "answer": True, "explain": "„Am Samstag, den 14. März“."},
            {"q": "Lena hat eine neue Telefonnummer.", "answer": True, "explain": "„Meine neue Handynummer ist …“"},
        ],
    },
]


def clean_items(kind, items, text=""):
    """Return a list of problems with a part's questions (empty when everything is fine)."""
    errors = []
    if not isinstance(items, list) or not items:
        return ["Add at least one question."]
    if kind == "tf" and not str(text).strip():
        errors.append("A richtig/falsch task needs a reading text.")
    for n, it in enumerate(items, 1):
        if not isinstance(it, dict) or not str(it.get("q") or "").strip():
            errors.append(f"Question {n} has no text.")
            continue
        if kind == "listen":
            opts = it.get("options")
            if not str(it.get("audio") or "").strip():
                errors.append(f"Question {n} has nothing to listen to.")
            if not isinstance(opts, list) or len(opts) < 2 or any(not str(o).strip() for o in opts):
                errors.append(f"Question {n} needs at least two answers, none of them empty.")
            elif not isinstance(it.get("answer"), int) or isinstance(it.get("answer"), bool) or not 0 <= it["answer"] < len(opts):
                errors.append(f"Question {n} has no right answer marked.")
        elif kind == "tf":
            if not isinstance(it.get("answer"), bool):
                errors.append(f"Question {n} must be richtig or falsch.")
        else:
            errors.append(f"Unknown task type “{kind}”.")
            break
    return errors


def install(Level, ExamPart):
    """Add the A1 exam practice sets that aren't there yet (matched by exam and slug).
    Never changes or deletes sets that already exist, so the teacher's edits stay."""
    level = Level.objects.filter(code="A1").first()
    if level is None:
        return []
    added = []
    for order, p in enumerate(PARTS, 1):
        problems = clean_items(p["kind"], p["items"], p.get("text", ""))
        if problems:
            raise ValueError(f"{p['slug']}: {problems}")
        _, created = ExamPart.objects.get_or_create(
            level=level, exam=p["exam"], slug=p["slug"],
            defaults={"module": p["module"], "teil": p["teil"], "title": p["title"], "kind": p["kind"],
                      "instructions": p["instructions"], "text": p.get("text", ""), "items": p["items"],
                      "minutes": p["minutes"], "example": p.get("example", {}), "order": order})
        if created:
            added.append(f"{p['module']} Teil {p['teil']}: {p['title']}")
    return added


def add_examples(ExamPart):
    """Give existing exam parts their worked example where they have none yet."""
    n = 0
    for p in PARTS:
        n += ExamPart.objects.filter(exam=p["exam"], slug=p["slug"], example={}).update(example=p["example"])
    return n
