"""Practice sets of a Lektion: checking their questions.

Shapes of `items` for each kind of set:
  choice       {"prompt": "Ich ___ ein Buch.", "say": optional audio, "clock": optional "HH:MM",
                "options": ["bin", "habe"], "answer": 1, "explain": optional}
  blanks       {"before": "Ich", "after": "(sein) Student.", "answer": "bin" (alternatives: "a|b"),
                "hint": optional, "explain": optional}
  tf           {"prompt": "Lena hat fünf Tage Kurs.", "answer": false, "explain": optional}
               (the set needs a reading `text`)
  listen_type  {"say": "einundzwanzig", "answer": "21", "explain": optional}
"""
import re

KINDS = ("choice", "blanks", "tf", "listen_type")


def _s(value):
    return str(value or "").strip()


def clean_example(kind, example, text=""):
    """Problems with a set's worked example (none when it's empty: an example is optional)."""
    if not example:
        return []
    return [p.replace("Question 1", "The example") for p in clean_set(kind, [example], text)]


def clean_set(kind, items, text=""):
    """Return a list of problems with a set's questions (empty when everything is fine)."""
    if kind not in KINDS:
        return [f"Unknown kind of set “{kind}”."]
    if not isinstance(items, list) or not items:
        return ["Add at least one question."]
    errors = []
    if kind == "tf" and not _s(text):
        errors.append("A richtig/falsch set needs a reading text.")
    for n, it in enumerate(items, 1):
        if not isinstance(it, dict):
            errors.append(f"Question {n} isn't a question.")
            continue
        if kind == "choice":
            opts = it.get("options")
            if not (_s(it.get("prompt")) or _s(it.get("say")) or _s(it.get("clock"))):
                errors.append(f"Question {n} needs a question, something to listen to, or a clock.")
            if _s(it.get("clock")) and not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", _s(it.get("clock"))):
                errors.append(f"Question {n}: the clock time must look like 07:30.")
            if not isinstance(opts, list) or len(opts) < 2 or any(not _s(o) for o in opts):
                errors.append(f"Question {n} needs at least two answers, none of them empty.")
            elif not isinstance(it.get("answer"), int) or isinstance(it.get("answer"), bool) or not 0 <= it["answer"] < len(opts):
                errors.append(f"Question {n} has no right answer marked.")
        elif kind == "blanks":
            if not (_s(it.get("before")) or _s(it.get("after"))):
                errors.append(f"Question {n} has no sentence around the gap.")
            if not _s(it.get("answer")).strip("|"):
                errors.append(f"Question {n} has no answer.")
        elif kind == "tf":
            if not _s(it.get("prompt")):
                errors.append(f"Question {n} has no sentence.")
            if not isinstance(it.get("answer"), bool):
                errors.append(f"Question {n} must be richtig or falsch.")
        elif kind == "listen_type":
            if not _s(it.get("say")):
                errors.append(f"Question {n} has nothing to listen to.")
            if not _s(it.get("answer")).strip("|"):
                errors.append(f"Question {n} has no answer.")
    return errors


def time_limit(practice_set):
    """Seconds allowed in exam mode: the set's minutes, or half a minute per question."""
    if practice_set.minutes:
        return practice_set.minutes * 60
    return max(60, 30 * len(practice_set.items))
