"""Dhruv's A1 course ("The German Lab by Sneha – A1 Grammar"), lesson by lesson, as sections
of the website. The source is the teacher's Google Drive (A1 / PDF / LektionNN_*.pdf).

Each lesson becomes one section with: its goals, its parts (lessons built from blocks),
its 20 new words (a word list in Words) and its homework. install() adds the lessons that
are not there yet and never changes a section that already exists, so it is safe to run
again (`python manage.py add_a1_course`).

Mistakes in the slides corrected here (see the project note "content-source"):
- L1: "schön" was an example of the soft ch-sound; it has none (sch). Milch is used instead.
- L1: final -e is a soft, short "uh", not "eh".
- L2: Exercise 1 no. 2, "3:15 = Es ist ___ nach drei": the answer is Viertel (fünf = 3:05).
- L3: Exercise 1 no. 5, "Sie ___ (sprechen) Deutsch": Sie can be she (spricht) or they/you (sprechen); both count.
"""

# ---------------------------------------------------------------- helpers
def text(body, heading=""):
    return {"type": "text", "heading": heading, "body": body}


def tip(body, heading="Watch out"):
    return {"type": "tip", "heading": heading, "body": body}


def table(headers, rows, heading=""):
    return {"type": "table", "heading": heading, "headers": headers, "rows": rows}


def words(items, heading=""):
    return {"type": "words", "heading": heading, "items": [{"german": g, "english": e} for g, e in items]}


def rules(rows, heading, intro=""):
    return {"type": "sounds", "heading": heading, "intro": intro,
            "rows": [{"label": label, "rule": rule, "words": ws} for label, rule, ws in rows]}


def mistakes(pairs, heading="Common mistakes"):
    return {"type": "mistakes", "heading": heading, "items": [{"wrong": w, "right": r} for w, r in pairs]}


def blanks(items, heading, intro=""):
    return {"type": "blanks", "heading": heading, "intro": intro,
            "items": [{"before": b, "after": a, "answer": ans} for b, a, ans in items]}


def choice(items, heading):
    return {"type": "choice", "heading": heading, "items": [
        {"prompt": i.get("prompt", ""), "say": i.get("say", ""), "clock": i.get("clock", ""),
         "options": i["options"], "answer": i["answer"], "explain": i.get("explain", "")} for i in items]}


# ---------------------------------------------------------------- Lektion 1
L1_LETTERS = [
    ("A", "Ah", "Apfel", "apple"), ("B", "Beh", "Banane", "banana"), ("C", "Tseh", "Café", "cafe"),
    ("D", "Deh", "Dach", "roof"), ("E", "Eh", "Elefant", "elephant"), ("F", "Ef", "Fenster", "window"),
    ("G", "Geh", "Garten", "garden"), ("H", "Ha", "Haus", "house"), ("I", "Ih", "Insel", "island"),
    ("J", "Yot", "Januar", "January"), ("K", "Kah", "Katze", "cat"), ("L", "El", "Lampe", "lamp"),
    ("M", "Em", "Mutter", "mother"), ("N", "En", "Nase", "nose"), ("O", "Oh", "Ozean", "ocean"),
    ("P", "Peh", "Party", "party"), ("Q", "Ku", "Quiz", "quiz"), ("R", "Er", "Rose", "rose"),
    ("S", "Es", "Sonne", "sun"), ("T", "Teh", "Tee", "tea"), ("U", "Uh", "Uhr", "watch/clock"),
    ("V", "Fau", "Vater", "father"), ("W", "Veh", "Wagen", "car"), ("X", "Iks", "Xylophon", "xylophone"),
    ("Y", "Ypsilon", "Yoga", "yoga"), ("Z", "Tset", "Zombie", "zombie"),
]

LEKTION_1 = {
    "title": "Lektion 1: Alphabet & Aussprache",
    "description": "The German alphabet, umlauts & pronunciation rules",
    "icon": "chat",
    "goals": [
        {"title": "The alphabet", "text": "Confidently name all 26 letters and their German pronunciation"},
        {"title": "Umlauts & ß", "text": "Correctly pronounce and recognize ä, ö, ü and ß"},
        {"title": "Pronunciation rules", "text": "Apply core rules for ei/ie, ch, s, e/en and g/ig"},
        {"title": "Reading words", "text": "Read common German words independently and correctly"},
    ],
    "words_topic": "Lektion 1 – Neue Wörter",
    "words": [
        ("der", "Apfel", "apple"), ("die", "Banane", "banana"), ("das", "Haus", "house"), ("das", "Buch", "book"),
        ("das", "Wasser", "water"), ("das", "Brot", "bread"), ("die", "Schule", "school"), ("der", "Freund", "friend"),
        ("die", "Familie", "family"), ("das", "Auto", "car"), ("die", "Straße", "street"), ("die", "Stadt", "city"),
        ("das", "Land", "country"), ("der", "Tag", "day"), ("die", "Nacht", "night"), ("die", "Woche", "week"),
        ("das", "Jahr", "year"), ("das", "Kind", "child"), ("die", "Frau", "woman"), ("der", "Mann", "man"),
    ],
    "homework": "1. Practice the alphabet: write out all 26 letters with their German pronunciation from memory.\n\n"
                "2. Apply the vocabulary: form 5 simple sentences using at least 5 of the new words "
                "(e.g. Apfel, Haus, Buch, Freund, Familie).",
    "lessons": [
        ("Das Alphabet", [
            text("Tap a letter to hear it. Under each letter: how it is said, and a word that starts with it."),
            {"type": "tiles", "heading": "A–Z", "intro": "",
             "items": [{"big": l, "small": said, "say": l, "note": f"{ex} – {en}"} for l, said, ex, en in L1_LETTERS]},
            rules([
                ("ä", "like 'e' in 'bed' (English)", ["Mädchen"]),
                ("ö", "say 'e', round your lips", ["schön"]),
                ("ü", "say 'i', round your lips", ["über"]),
                ("ß", "Eszett: a sharp, long 's' sound", ["groß", "Spaß"]),
            ], "Umlauts & ß", "Special characters in the German alphabet."),
            {"type": "spell_demo", "heading": "Spelling a word",
             "intro": "This is how you spell in German: say the name of each letter.", "word": "Haus"},
            {"type": "spell_name", "heading": "Spell your name in German"},
        ]),
        ("Aussprache-Regeln", [
            rules([
                ("ei · ai", "sounds like 'eye': a glide sound, like English 'eye'", ["vielleicht", "Ei"]),
                ("ie", "long 'ee' sound, like English 'see'", ["Liebe", "Sie"]),
                ("äu · eu", "sounds like 'oy', like English 'boy'", ["Häuser", "neu"]),
                ("au", "sounds like 'ow', like English 'how'", ["Bauch", "Haus"]),
            ], "Rule: diphthongs", "Double vowel sounds: how to pronounce letter combinations."),
            rules([
                ("ch", "soft 'ch' (Ich-sound) after i, e, ä, ö, ü or a consonant", ["ich", "echt", "Milch"]),
                ("ch", "hard 'ch' (Ach-sound) after a, o, u, au: deep in the throat", ["Buch", "machen", "Bauch"]),
            ], "Rule: 'ch'", "Two different pronunciations depending on context."),
            rules([
                ("s", "before a vowel (a, e, i, o, u, ä, ö, ü) it sounds like 'z'", ["sehen", "sagen", "Sonne"]),
                ("s", "otherwise a normal, sharp 's': at the end of a word or before a consonant", ["Haus", "ist"]),
            ], "Rule: 's'", "Pronunciation depends on position."),
            rules([
                ("-e", "a soft, short 'uh' sound at the end", ["Lage", "Name"]),
                ("-en", "unstressed 'en': about 80% of infinitive verbs end this way", ["spielen", "machen"]),
            ], "Rule: word endings '-e' / '-en'", "Very common in infinitive verbs."),
            rules([
                ("-g", "at the end: a soft 'k'", ["genug"]),
                ("-ig", "at the end: sounds like '-ich', don't say '-igg'", ["zwanzig", "langweilig", "traurig"]),
            ], "Rule: word endings '-g' / '-ig'", "They sound different at the end of a word than at the start."),
            words([
                ("Apfel", "apple · vowel start"), ("schön", "beautiful · umlaut ö"), ("vielleicht", "perhaps, maybe · ei sound"),
                ("Buch", "book · hard ch"), ("sehen", "to see · s like z"), ("zwanzig", "twenty · -ig like -ich"),
                ("spielen", "to play · -en ending"), ("Häuser", "houses · äu like oy"), ("groß", "big, tall · ß sharp s"),
                ("Haus", "house · au like ow"),
            ], "Examples: listen and say them out loud"),
        ]),
        ("Häufige Fehler", [
            mistakes([
                ("ich → a hard 'ick'", "ich → a soft 'ch', like the start of English 'hue'"),
                ("'-ig' pronounced like '-igg'", "'-ig' sounds like '-ich' (zwanzig)"),
                ("ü/ö pronounced like a plain u/o", "consciously round your lips for ü and ö"),
                ("'ei' as two separate sounds 'e-i'", "'ei' is a glide sound, like English 'eye'"),
            ], "Typical beginner mistakes in pronunciation"),
        ]),
    ],
}

# ---------------------------------------------------------------- Lektion 2
NUMBERS = ["null", "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn", "elf",
           "zwölf", "dreizehn", "vierzehn", "fünfzehn", "sechzehn", "siebzehn", "achtzehn", "neunzehn", "zwanzig"]

LEKTION_2 = {
    "title": "Lektion 2: Zahlen, Zeit, Tage, Monate",
    "description": "Cardinal & ordinal numbers, clock time, weekdays & months",
    "icon": "book",
    "goals": [
        {"title": "Numbers 0–100", "text": "Count and combine German numbers using the correct pattern"},
        {"title": "Ordinal numbers", "text": "Form ordinals like 'first', 'third', 'twentieth' correctly"},
        {"title": "Days & months", "text": "Name all weekdays and months confidently"},
        {"title": "Telling time", "text": "Tell time in both formal (Uhr) and informal (nach/vor/halb) styles"},
    ],
    "words_topic": "Lektion 2 – Neue Wörter",
    "words": [
        ("der", "Montag", "Monday"), ("der", "Dienstag", "Tuesday"), ("der", "Mittwoch", "Wednesday"),
        ("der", "Donnerstag", "Thursday"), ("der", "Freitag", "Friday"), ("der", "Samstag", "Saturday"),
        ("der", "Sonntag", "Sunday"), ("der", "Januar", "January"), ("der", "Juni", "June"), ("der", "Dezember", "December"),
        ("die", "Uhr", "clock / o'clock"), ("die", "Minute", "minute"), ("die", "Stunde", "hour"), ("", "heute", "today"),
        ("", "morgen", "tomorrow"), ("", "gestern", "yesterday"), ("das", "Datum", "date"), ("der", "Kalender", "calendar"),
        ("der", "Mittag", "noon"), ("die", "Mitternacht", "midnight"),
    ],
    "homework": "1. Practice numbers & time: write the numbers 10, 20, 30 … 100 in German, then practice saying "
                "5 random clock times out loud.\n\n"
                "2. Apply the vocabulary: write your weekly schedule (Monday–Sunday) with one activity per day, "
                "using at least 5 new words.",
    "lessons": [
        ("Zahlen 0–100", [
            text("The basic counting numbers: learn 0–20 first. Tap a number to hear it."),
            {"type": "tiles", "heading": "0–20", "intro": "",
             "items": [{"big": str(n), "small": w, "say": w, "note": ""} for n, w in enumerate(NUMBERS)]},
            text("**Rule:** ones + und + tens. 21 = ein + und + zwanzig = **einundzwanzig**. "
                 "Note that 'eins' drops the 's'.", "21–100: tens + ones, joined by 'und'"),
            table(["Tens", "", "Examples", ""], [
                ["20", "zwanzig", "21", "einundzwanzig"], ["30", "dreißig", "25", "fünfundzwanzig"],
                ["40", "vierzig", "34", "vierunddreißig"], ["50", "fünfzig", "47", "siebenundvierzig"],
                ["60", "sechzig", "58", "achtundfünfzig"], ["70", "siebzig", "69", "neunundsechzig"],
                ["80", "achtzig", "72", "zweiundsiebzig"], ["90", "neunzig", "83", "dreiundachtzig"],
                ["100", "hundert", "96", "sechsundneunzig"],
            ]),
            {"type": "number_builder", "heading": "Build a number"},
        ]),
        ("Ordinalzahlen", [
            text("1st, 2nd, 3rd … expressed in German.\n\n**Rule:** add **-te** for 1–19 (irregular: erste, "
                 "dritte, siebte, achte), add **-ste** for 20 and above."),
            table(["", "German", "", "German"], [
                ["1st", "erste", "9th", "neunte"], ["2nd", "zweite", "10th", "zehnte"],
                ["3rd", "dritte", "11th", "elfte"], ["4th", "vierte", "12th", "zwölfte"],
                ["5th", "fünfte", "20th", "zwanzigste"], ["6th", "sechste", "21st", "einundzwanzigste"],
                ["7th", "siebte", "30th", "dreißigste"], ["8th", "achte", "", ""],
            ], "Ordinal numbers"),
            words([("der dritte Mai", "the third of May"), ("der erste Januar", "the first of January")], "Dates"),
        ]),
        ("Wochentage und Monate", [
            words([("Montag", "Monday"), ("Dienstag", "Tuesday"), ("Mittwoch", "Wednesday"), ("Donnerstag", "Thursday"),
                   ("Freitag", "Friday"), ("Samstag", "Saturday"), ("Sonntag", "Sunday")], "Wochentage (days)"),
            words([("Januar", "January"), ("Februar", "February"), ("März", "March"), ("April", "April"),
                   ("Mai", "May"), ("Juni", "June"), ("Juli", "July"), ("August", "August"),
                   ("September", "September"), ("Oktober", "October"), ("November", "November"),
                   ("Dezember", "December")], "Monate (months)"),
        ]),
        ("Die Uhrzeit", [
            text("There are two ways to say the time: **formal** (Uhr, 24-hour clock) and **informal** "
                 "(nach, vor, Viertel, halb). Move the clock and listen to both."),
            {"type": "clock", "heading": "Try it"},
            words([("Es ist drei Uhr.", "It is 3:00."), ("Es ist zwölf Uhr (Mittag).", "It is 12:00 (noon)."),
                   ("Es ist vierzehn Uhr dreißig.", "It is 14:30."), ("Es ist Mitternacht.", "It is midnight.")],
                  "Formal: Es ist … Uhr"),
            table(["", "Meaning", "Example", ""], [
                ["nach", "after: minutes after the hour", "Es ist fünf nach drei.", "3:05"],
                ["vor", "before: minutes before the next hour", "Es ist zehn vor fünf.", "4:50"],
                ["Viertel", "quarter past / quarter to", "Es ist Viertel nach zwei.", "2:15"],
                ["", "", "Es ist Viertel vor sieben.", "6:45"],
                ["halb", "half (to the NEXT hour)", "Es ist halb sechs.", "5:30"],
            ], "Informal: the everyday way"),
            tip("**halb sechs** means half-way TO six: 5:30, not 6:30!"),
        ]),
        ("Häufige Fehler", [
            mistakes([
                ("Saying 'zwanzigeins' for 21", "einundzwanzig: the ones come first, joined by 'und'"),
                ("Keeping the 's' in 'einsundzwanzig'", "'ein' drops the 's' when combined: einundzwanzig"),
                ("Thinking 'halb sechs' means 6:30", "'halb sechs' means 5:30: half TO six"),
                ("Mixing up the '-te' and '-ste' endings", "1–19 use '-te', 20 and above use '-ste'"),
            ], "Typical beginner mistakes with numbers and time"),
            words([("einunddreißig", "thirty-one · tens + ones"), ("der dritte Mai", "the third of May · ordinal date"),
                   ("Es ist halb acht.", "It's 7:30 · informal time"), ("zweiundsiebzig", "seventy-two · tens + ones"),
                   ("Es ist Viertel vor neun.", "It's 8:45 · informal time"), ("vierzehn Uhr", "2:00 PM (14:00) · formal time")],
                  "Examples: listen and say them out loud"),
        ]),
    ],
}

# ---------------------------------------------------------------- Lektion 3
LEKTION_3 = {
    "title": "Lektion 3: Pronomen, Präsens, sein & haben",
    "description": "Personal pronouns, regular & strong verbs, sein and haben",
    "icon": "pencil",
    "goals": [
        {"title": "Personal pronouns", "text": "Use ich, du, er/sie/es, wir, ihr, sie/Sie correctly"},
        {"title": "sein & haben", "text": "Conjugate 'to be' and 'to have' in the present tense"},
        {"title": "Regular verbs", "text": "Build present-tense forms using the standard verb endings"},
        {"title": "Strong verbs", "text": "Apply vowel changes (a→ä, e→i/ie) in du and er/sie/es forms"},
    ],
    "words_topic": "Lektion 3 – Neue Verben",
    "words": [
        ("", "sein", "to be"), ("", "haben", "to have"), ("", "spielen", "to play"), ("", "fahren", "to drive"),
        ("", "sprechen", "to speak"), ("", "sehen", "to see"), ("", "lesen", "to read"), ("", "essen", "to eat"),
        ("", "geben", "to give"), ("", "nehmen", "to take"), ("", "helfen", "to help"), ("", "wohnen", "to live"),
        ("", "machen", "to make / do"), ("", "kommen", "to come"), ("", "gehen", "to go"), ("", "trinken", "to drink"),
        ("", "kaufen", "to buy"), ("", "schreiben", "to write"), ("", "hören", "to listen"), ("", "arbeiten", "to work"),
    ],
    "homework": "1. Conjugate 5 verbs: fully conjugate sein, haben, spielen, fahren and sprechen for all six pronouns.\n\n"
                "2. Describe your routine: write 5 sentences describing your daily routine, using at least 5 of the new verbs.",
    "lessons": [
        ("Personalpronomen", [
            text("The six pronouns every verb conjugation is built around."),
            table(["Pronoun", "English"], [
                ["ich", "I"], ["du", "you (informal, singular)"], ["er / sie / es", "he / she / it"],
                ["wir", "we"], ["ihr", "you (informal, plural)"], ["sie / Sie", "they / you (formal)"],
            ], "Personal pronouns"),
        ]),
        ("sein & haben", [
            text("The two most important irregular verbs: learn these by heart."),
            table(["", "sein (to be)", "haben (to have)"], [
                ["ich", "bin", "habe"], ["du", "bist", "hast"], ["er / sie / es", "ist", "hat"],
                ["wir", "sind", "haben"], ["ihr", "seid", "habt"], ["sie / Sie", "sind", "haben"],
            ]),
            words([("Du bist mein Freund.", "You are my friend."), ("Wir haben Zeit.", "We have time."),
                   ("Ich bin müde.", "I am tired."), ("Du hast einen Hund.", "You have a dog."),
                   ("Ihr seid nett.", "You (pl.) are nice.")], "Examples"),
        ]),
        ("Regelmäßige Verben", [
            text("Take the stem (remove **-en**) and add the ending for each pronoun.\n\n"
                 "**Endings:** ich **-e** · du **-st** · er/sie/es **-t** · wir **-en** · ihr **-t** · sie/Sie **-en**"),
            table(["", "spielen (to play), stem: spiel-"], [
                ["ich", "spiele"], ["du", "spielst"], ["er / sie / es", "spielt"],
                ["wir", "spielen"], ["ihr", "spielt"], ["sie / Sie", "spielen"],
            ], "Regular verbs: present tense"),
            table(["Verb", "du-form", "Example", ""], [
                ["heißen (to be called)", "du heißt (not heißst)", "Du heißt Anna.", "Your name is Anna."],
                ["tanzen (to dance)", "du tanzt", "Du tanzt gut.", "You dance well."],
                ["reisen (to travel)", "du reist", "Du reist viel.", "You travel a lot."],
                ["sitzen (to sit)", "du sitzt", "Du sitzt hier.", "You sit here."],
            ], "Special case: stems ending in -s, -ß, -z, -x"),
            tip("With these stems the du-form adds only **-t**, not -st, to avoid a double-s sound.", "Remember"),
        ]),
        ("Starke Verben", [
            text("Some verbs change their stem vowel, but **only in the du and er/sie/es forms**."),
            table(["Verb", "du", "er / sie / es", "Example"], [
                ["fahren (to drive)", "fährst", "fährt", "Er fährt nach Berlin."],
                ["waschen (to wash)", "wäschst", "wäscht", "Sie wäscht das Auto."],
                ["tragen (to wear / carry)", "trägst", "trägt", "Er trägt eine Tasche."],
                ["halten (to hold / stop)", "hältst", "hält", "Der Bus hält hier."],
            ], "a → ä"),
            table(["Verb", "du", "er / sie / es", "Example"], [
                ["sprechen (to speak)", "sprichst", "spricht", "Sie spricht Deutsch."],
                ["essen (to eat)", "isst", "isst", "Er isst einen Apfel."],
                ["geben (to give)", "gibst", "gibt", "Er gibt mir das Buch."],
                ["nehmen (to take)", "nimmst", "nimmt", "Sie nimmt das Buch."],
                ["sehen (to see)", "siehst", "sieht", "Er sieht den Bus."],
                ["lesen (to read)", "liest", "liest", "Er liest ein Buch."],
            ], "e → i / ie"),
        ]),
        ("Häufige Fehler", [
            mistakes([
                ("Writing 'du spielest'", "du spielst: no extra 'e' before '-st'"),
                ("Forgetting the vowel change: 'du fahrst'", "du fährst: a→ä in the du and er/sie/es forms"),
                ("Writing 'du heißst' with a double s", "du heißt: stems ending in -ß add only '-t'"),
                ("Confusing sein and haben: 'ich bin ein Buch'", "ich habe ein Buch: haben = to have, sein = to be"),
            ], "Typical beginner mistakes with verb conjugation"),
            words([("Ich spiele Fußball.", "I play soccer · regular"), ("Du bist mein Freund.", "You are my friend · sein"),
                   ("Er fährt ein Auto.", "He drives a car · a→ä"), ("Wir haben Zeit.", "We have time · haben"),
                   ("Sie spricht Deutsch.", "She speaks German · e→i"), ("Ich bin müde.", "I am tired · sein"),
                   ("Du hast einen Hund.", "You have a dog · haben"), ("Er liest ein Buch.", "He reads a book · e→ie"),
                   ("Wir wohnen in Berlin.", "We live in Berlin · regular"), ("Ihr seid nett.", "You (pl.) are nice · sein")],
                  "Examples: listen and say them out loud"),
        ]),
    ],
}

# ---------------------------------------------------------------- practice sets & writing tasks
# Sets marked "lesson" are the PDF's own exercises; "extra" sets are written strictly from the
# same lesson (its rules, examples and words); "both" mixes the two.
LETTER_NAME = {l: said for l, said, _, _ in L1_LETTERS}


def spelled(word):
    return ", ".join(LETTER_NAME[c.upper()] for c in word)


def pset(title, source, kind, intro, items, text_=""):
    return {"title": title, "source": source, "kind": kind, "intro": intro, "items": items, "text": text_}


def bl(before, after, answer, hint="", explain=""):
    return {"before": before, "after": after, "answer": answer, "hint": hint, "explain": explain}


def ch(prompt, options, answer, explain="", say="", clock=""):
    return {"prompt": prompt, "options": options, "answer": answer, "explain": explain, "say": say, "clock": clock}


def task(title, source, prompt):
    return {"title": title, "source": source, "prompt": prompt}


RULES_L1 = ["au like 'ow'", "äu/eu like 'oy'", "soft ch", "hard ch", "s like z", "-en ending", "-ig like -ich", "-g at the end: soft k"]

LEKTION_1["sets"] = [
    pset("Übung 1: Lückentext", "lesson", "blanks", "Fill in the blanks with the correct pronunciation term.", [
        bl("Schön has the umlaut", ".", "ö"),
        bl("Infinitive verbs mostly end in", ".", "-en|en"),
        bl("'Ei' sounds like the English word", ".", "eye"),
        bl("When 's' is before a vowel, it sounds like", ".", "z"),
        bl("'-ig' at the end of a word sounds like", ".", "-ich|ich"),
    ]),
    pset("Übung 2: Welche Regel passt?", "lesson", "choice", "Listen to the word. Which pronunciation rule does it show?", [
        ch("Häuser", ["äu/eu like 'oy'", "au like 'ow'", "s like z"], 0, "äu sounds like 'oy' in English 'boy'.", say="Häuser"),
        ch("genug", ["-ig like -ich", "-g at the end: soft k", "hard ch"], 1, "A g at the end of a word sounds like a soft k.", say="genug"),
        ch("ich", ["hard ch", "soft ch", "-en ending"], 1, "After i the ch is soft (Ich-sound).", say="ich"),
        ch("Buch", ["soft ch", "hard ch", "au like 'ow'"], 1, "After u the ch is hard (Ach-sound).", say="Buch"),
        ch("zwanzig", ["-g at the end: soft k", "s like z", "-ig like -ich"], 2, "-ig at the end sounds like -ich.", say="zwanzig"),
        ch("Haus", ["au like 'ow'", "soft ch", "s like z"], 0, "au sounds like 'ow' in English 'how'.", say="Haus"),
        ch("sehen", ["s like z", "-ig like -ich", "hard ch"], 0, "s before a vowel sounds like z.", say="sehen"),
        ch("spielen", ["-en ending", "hard ch", "äu/eu like 'oy'"], 0, "The unstressed -en ending of a verb.", say="spielen"),
    ]),
    pset("Welchen Buchstaben hörst du?", "extra", "choice", "Listen and choose the letter.", [
        ch("", ["E", "I", "A"], 0, "E is said 'Eh', I is said 'Ih'.", say="E"),
        ch("", ["V", "W", "F"], 1, "W is said 'Veh', V is said 'Fau'.", say="W"),
        ch("", ["Y", "G", "J"], 2, "J is said 'Yot', G is said 'Geh'.", say="J"),
        ch("", ["C", "S", "Z"], 2, "Z is said 'Tset', C is said 'Tseh'.", say="Z"),
        ch("", ["W", "V", "F"], 1, "V is said 'Fau'.", say="V"),
        ch("", ["A", "H", "K"], 1, "H is said 'Ha'.", say="H"),
        ch("", ["K", "Q", "U"], 1, "Q is said 'Ku'.", say="Q"),
        ch("", ["I", "E", "Y"], 0, "I is said 'Ih'.", say="I"),
    ]),
    pset("Hören und schreiben: buchstabierte Wörter", "extra", "listen_type", "Listen to the spelling and write the word.", [
        {"say": spelled(w), "answer": w, "explain": f"{w} = {spelled(w)}"} for w in ["Haus", "Buch", "Vater", "Katze", "Apfel", "Brot"]
    ]),
    pset("Umlaute und Laute", "extra", "choice", "Which letters are missing?", [
        ch("sch__n (beautiful)", ["o", "ö", "ü"], 1, "schön has the umlaut ö."),
        ch("M__dchen (girl)", ["a", "ä", "e"], 1, "Mädchen has the umlaut ä."),
        ch("__ber (over, about)", ["u", "ü", "i"], 1, "über has the umlaut ü."),
        ch("gro__ (big)", ["s", "ß", "z"], 1, "groß ends with ß, a sharp long s."),
        ch("H__ser (houses)", ["au", "äu", "eu"], 1, "Häuser: äu, sounds like 'oy'."),
        ch("n__ (new)", ["eu", "ei", "au"], 0, "neu: eu, sounds like 'oy'."),
        ch("L__be (love)", ["ei", "ie", "i"], 1, "Liebe: ie, a long 'ee'."),
        ch("B__ch (stomach)", ["au", "äu", "eu"], 0, "Bauch: au, sounds like 'ow'."),
    ]),
]
LEKTION_1["writing"] = [
    task("Buchstabiere deinen Namen", "Übung 2, Aufgabe 1", "Spell your name in German with the letter names (e.g. Anna = Ah-En-En-Ah)."),
    task("Wörter mit Umlaut", "Übung 3, Aufgabe 1", "Write 5 German words with umlauts (ä, ö, ü) and their meaning."),
    task("Ein Satz mit -ig", "Übung 3, Aufgabe 2", "Write a short sentence with a word that ends in '-ig'."),
    task("Drei Wörter buchstabieren", "Übung 3, Aufgabe 3", "Spell three German words in writing using letter names (e.g. Haus = Ha-Ah-Uh-Es)."),
    task("Hausaufgabe: das Alphabet", "Hausaufgabe 1", "Write out all 26 letters with their German pronunciation from memory."),
    task("Hausaufgabe: neue Wörter", "Hausaufgabe 2", "Form 5 simple sentences using at least 5 of the new words (e.g. Apfel, Haus, Buch, Freund, Familie)."),
]

LEKTION_2["sets"] = [
    pset("Übung 1: Lückentext", "lesson", "blanks", "Fill in the blanks with the correct German word.", [
        bl("21 =", ".", "einundzwanzig"),
        bl("3:15 = Es ist", "nach drei.", "Viertel", explain="3:15 is a quarter past three: Viertel nach drei."),
        bl("The ordinal for '5th' is", ".", "fünfte"),
        bl("Saturday in German is", ".", "Samstag"),
        bl("5:30 = Es ist", "sechs.", "halb", explain="halb sechs = half-way to six = 5:30."),
    ]),
    pset("Übung 2: Zahlen 1–10", "lesson", "blanks", "Write the number in German.", [
        bl(f"{n} =", "", w) for n, w in enumerate(NUMBERS[1:11], 1)
    ]),
    pset("Wie spät ist es?", "both", "choice", "Look at the clock. What time is it?", [
        ch("", ["Es ist halb sieben.", "Es ist halb acht.", "Es ist sieben Uhr halb."], 1, "halb acht = half-way to eight = 7:30.", clock="07:30"),
        ch("", ["Es ist Viertel nach neun.", "Es ist Viertel vor acht.", "Es ist Viertel vor neun."], 2, "8:45 = a quarter to nine.", clock="08:45"),
        ch("", ["Es ist Viertel nach zwei.", "Es ist Viertel vor zwei.", "Es ist halb drei."], 0, "2:15 = a quarter past two.", clock="02:15"),
        ch("", ["Es ist zehn nach fünf.", "Es ist zehn vor fünf.", "Es ist zehn vor vier."], 1, "4:50 = ten to five.", clock="04:50"),
        ch("", ["Es ist halb fünf.", "Es ist halb sechs.", "Es ist halb sieben."], 1, "halb sechs = 5:30, not 6:30!", clock="05:30"),
        ch("", ["Es ist fünf nach drei.", "Es ist fünf vor drei.", "Es ist drei nach fünf."], 0, "3:05 = five past three.", clock="03:05"),
        ch("", ["Es ist fünf nach sieben.", "Es ist fünf vor sieben.", "Es ist fünf vor sechs."], 1, "6:55 = five to seven.", clock="06:55"),
        ch("", ["Es ist Viertel vor acht.", "Es ist Viertel nach acht.", "Es ist halb acht."], 0, "7:45 = a quarter to eight.", clock="07:45"),
    ]),
    pset("Formell: Es ist … Uhr", "extra", "choice", "How do you say the time the formal way (24-hour clock)?", [
        ch("14:30", ["vierzehn Uhr dreißig", "vier Uhr dreißig", "halb vierzehn Uhr"], 0, "Formal: hours + Uhr + minutes."),
        ch("19:45", ["neunzehn Uhr fünfundvierzig", "neun Uhr fünfundvierzig", "neunzehn Uhr vierundfünfzig"], 0, "19 = neunzehn, 45 = fünfundvierzig."),
        ch("07:45", ["neunzehn Uhr fünfundvierzig", "sieben Uhr fünfundvierzig", "Viertel nach sieben"], 1, "7:45 in the morning = sieben Uhr fünfundvierzig."),
        ch("12:00", ["zwölf Uhr", "zwei Uhr", "zwanzig Uhr"], 0, "12:00 = zwölf Uhr (Mittag)."),
        ch("00:00", ["Mittag", "Mitternacht", "null Uhr null"], 1, "00:00 = Mitternacht (midnight)."),
    ]),
    pset("Ordinalzahlen", "both", "blanks", "Write the ordinal number.", [
        bl("1. Januar = der", "Januar", "erste"),
        bl("3. Mai = der", "Mai", "dritte", explain="dritte is irregular."),
        bl("5. = der", "Tag", "fünfte"),
        bl("7. = der", "Tag", "siebte", explain="siebte is irregular (not siebente at A1)."),
        bl("8. = der", "Tag", "achte"),
        bl("20. = der", "Tag", "zwanzigste", explain="20 and above add -ste."),
        bl("21. = der", "Tag", "einundzwanzigste"),
    ]),
    pset("Zahlen hören", "extra", "listen_type", "Listen to the number and write it in digits.", [
        {"say": w, "answer": str(n)} for n, w in [(21, "einundzwanzig"), (34, "vierunddreißig"), (47, "siebenundvierzig"),
                                                   (72, "zweiundsiebzig"), (96, "sechsundneunzig"), (13, "dreizehn"),
                                                   (58, "achtundfünfzig"), (100, "hundert")]
    ]),
    pset("Tage und Monate", "extra", "choice", "Choose the right word.", [
        ch("Der Tag nach Montag ist …", ["Mittwoch", "Dienstag", "Sonntag"], 1),
        ch("Der Tag vor Sonntag ist …", ["Samstag", "Freitag", "Montag"], 0),
        ch("Der erste Monat ist …", ["Juni", "Januar", "Dezember"], 1),
        ch("Der Monat nach April ist …", ["März", "Mai", "Juli"], 1),
        ch("Der letzte Monat ist …", ["November", "Dezember", "Oktober"], 1),
        ch("Wednesday =", ["Mittwoch", "Donnerstag", "Montag"], 0),
    ]),
]
LEKTION_2["writing"] = [
    task("Das Datum von heute", "Übung 2, Aufgabe 2", "Write today's date in German using day + month (e.g. der erste Januar)."),
    task("Mein Wochenplan (3 Tage)", "Übung 3, Aufgabe 1", "Write your weekly schedule for 3 days using the German days of the week."),
    task("Ordinalzahlen in Sätzen", "Übung 3, Aufgabe 2", "Write 5 ordinal numbers, each in a short sentence (e.g. 'der erste Tag')."),
    task("Drei Uhrzeiten", "Übung 3, Aufgabe 3", "Write three clock times in German using nach, vor or halb."),
    task("Hausaufgabe: Zahlen und Uhrzeit", "Hausaufgabe 1", "Write the numbers 10, 20, 30 … 100 in German. Then write 5 clock times."),
    task("Hausaufgabe: meine Woche", "Hausaufgabe 2", "Write your weekly schedule (Monday–Sunday) with one activity per day, using at least 5 new words."),
]

LEKTION_3["sets"] = [
    pset("Übung 1: Lückentext", "lesson", "blanks", "Conjugate the verb in brackets correctly.", [
        bl("Ich", "(sein) Student.", "bin"),
        bl("Du", "(haben) ein Buch.", "hast"),
        bl("Er", "(fahren) nach Berlin.", "fährt", explain="fahren changes a→ä: er fährt."),
        bl("Wir", "(spielen) Fußball.", "spielen"),
        bl("Sie", "(sprechen) Deutsch.", "spricht|sprechen", explain="sie (she) spricht, sie/Sie (they/you) sprechen: both are right."),
    ]),
    pset("Übung 2: lesen konjugieren", "lesson", "blanks", "Write the right form of lesen (e→ie) for each pronoun.", [
        bl("ich", "", "lese"), bl("du", "", "liest"), bl("er / sie / es", "", "liest"),
        bl("wir", "", "lesen"), bl("ihr", "", "lest"), bl("sie / Sie", "", "lesen"),
    ]),
    pset("Übung 2: von ich zu du", "lesson", "blanks", "Change the sentence from ich to du.", [
        bl("Ich spiele Fußball. → Du", "Fußball.", "spielst"),
        bl("Ich fahre ein Auto. → Du", "ein Auto.", "fährst"),
        bl("Ich spreche Deutsch. → Du", "Deutsch.", "sprichst"),
    ]),
    pset("sein oder haben?", "extra", "choice", "Choose sein or haben.", [
        ch("Ich ___ ein Buch.", ["bin", "habe"], 1, "haben = to have: ich habe ein Buch."),
        ch("Wir ___ müde.", ["sind", "haben"], 0, "sein = to be: wir sind müde."),
        ch("Er ___ einen Hund.", ["ist", "hat"], 1, "haben: er hat einen Hund."),
        ch("Ihr ___ nett.", ["seid", "habt"], 0, "sein: ihr seid nett."),
        ch("Du ___ mein Freund.", ["bist", "hast"], 0, "sein: du bist mein Freund."),
        ch("Wir ___ Zeit.", ["sind", "haben"], 1, "haben: wir haben Zeit."),
        ch("Ich ___ müde.", ["bin", "habe"], 0, "sein: ich bin müde."),
        ch("Anna ___ zwei Katzen.", ["ist", "hat"], 1, "haben: Anna hat zwei Katzen."),
    ]),
    pset("Starke Verben", "extra", "blanks", "Careful: a→ä and e→i/ie in the du and er/sie/es forms.", [
        bl("Du", "(fahren) nach Berlin.", "fährst"),
        bl("Sie", "(waschen) das Auto.", "wäscht|waschen", explain="sie (she) wäscht; sie/Sie (they/you) waschen."),
        bl("Er", "(tragen) eine Tasche.", "trägt"),
        bl("Du", "(essen) einen Apfel.", "isst"),
        bl("Er", "(geben) mir das Buch.", "gibt"),
        bl("Anna", "(nehmen) das Buch.", "nimmt"),
        bl("Du", "(sehen) den Bus.", "siehst"),
        bl("Er", "(lesen) ein Buch.", "liest"),
    ]),
    pset("Regelmäßige Verben", "extra", "blanks", "Stem + ending: ich -e, du -st, er/sie/es -t, wir -en, ihr -t, sie/Sie -en.", [
        bl("Ich", "(wohnen) in Berlin.", "wohne"),
        bl("Du", "(spielen) Fußball.", "spielst"),
        bl("Ihr", "(machen) Musik.", "macht"),
        bl("Wir", "(kaufen) Brot.", "kaufen"),
        bl("Du", "(heißen) Anna.", "heißt", explain="Stems ending in -ß add only -t: du heißt."),
        bl("Er", "(kommen) aus Indien.", "kommt"),
        bl("Ihr", "(trinken) Wasser.", "trinkt"),
        bl("Du", "(tanzen) gut.", "tanzt", explain="Stems ending in -z add only -t: du tanzt."),
    ]),
    pset("Welches Pronomen?", "extra", "choice", "Which pronoun replaces the words?", [
        ch("Anna und ich → ___", ["wir", "ihr", "sie"], 0),
        ch("Peter → ___", ["sie", "er", "es"], 1),
        ch("das Kind → ___", ["er", "sie", "es"], 2),
        ch("Maria und Tom → ___", ["ihr", "sie", "wir"], 1),
        ch("Herr Weber (formal) → ___", ["du", "Sie", "er"], 1),
        ch("du und Anna → ___", ["ihr", "wir", "sie"], 0),
    ]),
]
LEKTION_3["writing"] = [
    task("Über mich: sein und haben", "Übung 2, Aufgabe 2", "Write 3 sentences about yourself using 'sein' and 'haben'."),
    task("Stell dich vor", "Übung 3, Aufgabe 1", "Write a short paragraph (3–4 sentences) introducing yourself using sein, haben and one regular verb."),
    task("Starke Verben", "Übung 3, Aufgabe 2", "Write 3 sentences using verbs that change a→ä or e→i/ie."),
    task("Mein Freund / meine Freundin", "Übung 3, Aufgabe 3", "Describe a friend using er/sie with at least 3 different verbs."),
    task("Hausaufgabe: 5 Verben konjugieren", "Hausaufgabe 1", "Fully conjugate sein, haben, spielen, fahren and sprechen for all six pronouns."),
    task("Hausaufgabe: mein Tag", "Hausaufgabe 2", "Write 5 sentences describing your daily routine, using at least 5 of the new verbs."),
]

# ---------------------------------------------------------------- worked examples
# Every set starts with one solved question (not scored), so students see what to do.
# Each example is a new question from the same lesson, never one of the set's own questions.
EXAMPLES = {
    1: {
        "Übung 1: Lückentext": bl("Mädchen has the umlaut", ".", "ä", explain="Mädchen is written with ä."),
        "Übung 2: Welche Regel passt?": ch("echt", ["soft ch", "hard ch", "s like z"], 0, "After e the ch is soft (Ich-sound).", say="echt"),
        "Welchen Buchstaben hörst du?": ch("", ["P", "B", "D"], 1, "B is said 'Beh', P is said 'Peh'.", say="B"),
        "Hören und schreiben: buchstabierte Wörter": {"say": spelled("Tag"), "answer": "Tag", "explain": f"Tag = {spelled('Tag')}"},
        "Umlaute und Laute": ch("T__r (door)", ["u", "ü", "o"], 1, "Tür has the umlaut ü."),
    },
    2: {
        "Übung 1: Lückentext": bl("11 =", ".", "elf"),
        "Übung 2: Zahlen 1–10": bl("0 =", "", "null"),
        "Wie spät ist es?": ch("", ["Es ist halb drei.", "Es ist halb vier.", "Es ist drei Uhr halb."], 1, "halb vier = half-way to four = 3:30.", clock="03:30"),
        "Formell: Es ist … Uhr": ch("09:15", ["neun Uhr fünfzehn", "Viertel nach neun", "neunzehn Uhr fünfzehn"], 0,
                                   "Formal: hours + Uhr + minutes. (Viertel nach neun is the informal way.)"),
        "Ordinalzahlen": bl("2. = der", "Tag", "zweite"),
        "Zahlen hören": {"say": "fünfzehn", "answer": "15", "explain": "fünfzehn = 15"},
        "Tage und Monate": ch("Der Tag nach Freitag ist …", ["Samstag", "Sonntag", "Donnerstag"], 0),
    },
    3: {
        "Übung 1: Lückentext": bl("Wir", "(sein) müde.", "sind", explain="sein: wir sind."),
        "Übung 2: lesen konjugieren": bl("du (sehen)", "", "siehst", explain="sehen is strong too: e→ie in the du form."),
        "Übung 2: von ich zu du": bl("Ich wohne in Berlin. → Du", "in Berlin.", "wohnst"),
        "sein oder haben?": ch("Du ___ Zeit.", ["bist", "hast"], 1, "haben = to have: du hast Zeit."),
        "Starke Verben": bl("Er", "(sprechen) Deutsch.", "spricht", explain="sprechen changes e→i: er spricht."),
        "Regelmäßige Verben": bl("Wir", "(spielen) Fußball.", "spielen", explain="wir + -en: wir spielen."),
        "Welches Pronomen?": ch("Lisa → ___", ["er", "sie", "es"], 1, "Lisa is a woman: sie."),
    },
}
for _n, _lektion in enumerate([LEKTION_1, LEKTION_2, LEKTION_3], 1):
    for _s in _lektion["sets"]:
        _s["example"] = EXAMPLES[_n][_s["title"]]


def add_examples(Section, PracticeSet):
    """Give the course's sets their worked example where they have none yet (sites built before examples)."""
    changed = 0
    for data in COURSE:
        for s in data.get("sets", []):
            n = PracticeSet.objects.filter(section__title=data["title"], title=s["title"], example={}).update(example=s["example"])
            changed += n
    return changed


COURSE = [LEKTION_1, LEKTION_2, LEKTION_3]


def _speaking_block(level, SpeakingTask):
    if SpeakingTask is None:
        return None
    task = SpeakingTask.objects.filter(level=level, slug="wie-schreibt-man-das").first()
    return {"type": "speaking", "heading": "Now say it to your teacher", "task_id": task.pk} if task else None


def install(Level, Section, Lesson, Topic, VocabularyItem, SpeakingTask=None, PracticeSet=None, WritingTask=None):
    """Add what of COURSE isn't on the site yet: missing Lektionen (sections with their pages and
    words), and practice sets and writing tasks for Lektionen that have none. Never changes
    anything that already exists. Returns what was added."""
    from django.utils.text import slugify

    level = Level.objects.filter(code="A1").first()
    if level is None:
        return []
    added = []
    for n, data in enumerate(COURSE, 1):
        section = Section.objects.filter(level=level, title=data["title"]).first()
        if section is None:
            topic = Topic.objects.filter(level=level, name=data["words_topic"]).first()
            if topic is None:
                slug, i = slugify(data["words_topic"])[:80], 2
                base = slug
                while Topic.objects.filter(level=level, slug=slug).exists():
                    slug, i = f"{base}-{i}", i + 1
                topic = Topic.objects.create(level=level, name=data["words_topic"], slug=slug, order=100 + n,
                                             description=data["title"].split(": ", 1)[-1])
                for i, (article, german, english) in enumerate(data["words"], 1):
                    VocabularyItem.objects.create(topic=topic, article=article, german=german, english=english, order=i)
            section = Section.objects.create(level=level, title=data["title"], description=data["description"],
                                             icon=data["icon"], goals=data["goals"], homework=data["homework"],
                                             topic=topic, order=n)
            for i, (title, blocks) in enumerate(data["lessons"], 1):
                blocks = [dict(b) for b in blocks]
                if n == 1 and title == "Das Alphabet":
                    extra = _speaking_block(level, SpeakingTask)
                    if extra:
                        blocks.append(extra)
                Lesson.objects.create(section=section, title=title, blocks=blocks, is_published=True, order=i)
            added.append(data["title"])
        if PracticeSet is not None and data.get("sets") and not PracticeSet.objects.filter(section=section).exists():
            for i, s in enumerate(data["sets"], 1):
                PracticeSet.objects.create(section=section, title=s["title"], source=s["source"], kind=s["kind"],
                                           intro=s["intro"], text=s["text"], items=s["items"],
                                           example=s.get("example", {}), order=i)
            # The old "Übungen" page is replaced by the practice sets: kept as a hidden draft.
            Lesson.objects.filter(section=section, title="Übungen").update(title="Übungen (old, now in practice sets)",
                                                                          is_published=False, order=99)
            added.append(f"{data['title'].split(':')[0]}: {len(data['sets'])} practice sets")
        if WritingTask is not None and data.get("writing") and not WritingTask.objects.filter(section=section).exists():
            for i, w in enumerate(data["writing"], 1):
                WritingTask.objects.create(section=section, title=w["title"], source=w["source"], prompt=w["prompt"], order=i)
            added.append(f"{data['title'].split(':')[0]}: {len(data['writing'])} writing tasks")
    # The earlier "Basics of A1" (from another book) is replaced by Lektion 1: hidden, not deleted.
    Section.objects.filter(level=level, title="Basics of A1", is_visible=True).update(is_visible=False, order=99)
    return added
