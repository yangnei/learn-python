#!/usr/bin/env python3
"""
Build the interactive student website into docs/ (GitHub Pages ready).

Each session page embeds the lesson (from slides/), practice (from examples/),
and quiz (from assessments/quizzes.md) as raw markdown that the browser renders
with marked.js, plus a set of editable "playground" snippets that run real Python
in the browser via Pyodide.

Run:  python3 tools/build_site.py
"""
from __future__ import annotations
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

SESSIONS = [
    (1, "Running Python, Variables & Types", "Run code; the 5 core types; input/output & f-strings.", False),
    (2, "The Dynamic-Typing Traps", "== vs is, True==1, float precision, 5=='5'. The keystone.", True),
    (3, "Conditionals & Boolean Logic", "if/elif/else, chained comparisons, and/or, match.", False),
    (4, "Loops & Iteration", "for/while, break/continue, range, enumerate, zip.", False),
    (5, "Data Structures", "list/tuple/dict/set, comprehensions, sorting, aliasing.", False),
    (6, "Functions, Scope & Reusability", "params, *args/**kwargs, scope, the mutable-default bug.", False),
    (7, "Exceptions & Defensive Code", "try/except, raising, validating dirty research data.", False),
    (8, "Files, Libraries & Research Data", "open/with, CSV, statistics, the pandas teaser.", False),
    (9, "Regex, Modules, OOP & Pythonic", "regex, modules, a small class, comprehensions/generators.", False),
]

# Editable, in-browser-runnable snippets per session (Pyodide-safe: no file I/O, no input()).
PLAYGROUNDS: dict[int, list[dict]] = {
    1: [{"title": "types_and_fstrings.py", "code": '''\
# Edit me, then press Run. Predict the output first!
name = "Ada"
score = 87.456
n_students = 1234

print(type(name), type(score))
print(f"{name} scored {score:.1f}")          # one decimal
print(f"{n_students:,} students")            # thousands separator
print("int('42') + 8 =", int("42") + 8)      # convert text to number
print("int(3.9) =", int(3.9), "| round(3.9) =", round(3.9))
'''}],
    2: [
        {"title": "the_traps.py", "code": '''\
import math
print("True == 1            :", True == 1)
print("5 + True             :", 5 + True)
print("sum([True,False,True]):", sum([True, False, True]))
print("3 == 3.0             :", 3 == 3.0)
print("0.1 + 0.2            :", 0.1 + 0.2)
print("0.1 + 0.2 == 0.3     :", 0.1 + 0.2 == 0.3)
print("math.isclose(...)    :", math.isclose(0.1 + 0.2, 0.3))
print('5 == "5"             :', 5 == "5")
print("[1,2] == (1,2)       :", [1, 2] == (1, 2))
a = [1, 2]; b = a; a.append(3)
print("alias b              :", b)    # b changed too!
'''},
        {"title": "comparisons_that_crash.py", "code": '''\
# Some comparisons return False; some CRASH. Run it and read the error.
print('5 == "5" :', 5 == "5")     # False, no error
print('5 > "5"  :', 5 > "5")      # TypeError! Python can't rank text vs number
# Fix: compare numbers. Comment the line above and try:
# print(5 > int("5"))
'''},
    ],
    3: [{"title": "grades_and_logic.py", "code": '''\
def letter_grade(score):
    if not 0 <= score <= 100:        # chained comparison
        return "Invalid"
    for cutoff, letter in [(90, "A"), (80, "B"), (70, "C"), (60, "D")]:
        if score >= cutoff:
            return letter
    return "F"

for s in [95, 90, 89.999, 60, 59, 120]:
    print(s, "->", letter_grade(s))

print("5 and 0     =", 5 and 0)        # and/or return an operand
print("'' or 'N/A' =", "" or "N/A")    # default-value idiom
'''}],
    4: [{"title": "enumerate_zip.py", "code": '''\
names  = ["Ana", "Ben", "Cara", "Dev"]
scores = [91, 58, 73, 64]

for i, name in enumerate(names, start=1):     # index + value
    print(i, name)

print("---")
for name, score in zip(names, scores):        # two lists together
    print(f"{name}: {'PASS' if score >= 60 else 'FAIL'}")

print("passes:", sum(s >= 60 for s in scores))  # bools sum!
'''}],
    5: [{"title": "structures_and_aliasing.py", "code": '''\
roster = [{"name": "Ana", "score": 91},
          {"name": "Ben", "score": 58},
          {"name": "Cara", "score": 73}]

ranked = sorted(roster, key=lambda s: s["score"], reverse=True)
print("ranked:", [s["name"] for s in ranked])
print("map:   ", {s["name"]: s["score"] for s in roster})   # dict comprehension

# Aliasing: assignment does NOT copy.
a = [1, 2, 3]; b = a; a.append(4)
print("alias b:", b)        # [1, 2, 3, 4]
c = a.copy(); a.append(5)
print("copy  c:", c)        # unaffected
'''}],
    6: [{"title": "mutable_default_bug.py", "code": '''\
def add_bad(name, roster=[]):     # BUG: default list is shared across calls
    roster.append(name)
    return roster

print("BUGGY:", add_bad("Ana"))   # ['Ana']
print("BUGGY:", add_bad("Ben"))   # ['Ana', 'Ben']  <- persists!

def add_ok(name, roster=None):    # FIX: default None, create inside
    if roster is None:
        roster = []
    roster.append(name)
    return roster

print("FIXED:", add_ok("Ana"))    # ['Ana']
print("FIXED:", add_ok("Ben"))    # ['Ben']
'''}],
    7: [{"title": "clean_dirty_survey.py", "code": '''\
def safe_int(v):
    try:
        return int(v)
    except (ValueError, TypeError):
        return None

def clean_likert(n):
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError(f"{n!r} not an int")
    if not 1 <= n <= 5:
        raise ValueError(f"{n} outside 1-5")
    return n

raw = ["5", "3", "N/A", "7", "", "1", "two", "4"]
clean, rejected = [], []
for r in raw:
    try:
        clean.append(clean_likert(safe_int(r)))
    except ValueError as e:
        rejected.append((r, str(e)))
print("clean:   ", clean)
print("rejected:", rejected)
'''}],
    8: [{"title": "read_csv_in_memory.py", "code": '''\
import csv, statistics, io

# A real CSV would be a file; here we read it from a string so it runs in-browser.
DATA = """name,major,score
Ana,Education,91
Ben,Psychology,58
Cara,Education,73
Dev,Sociology,64
Eve,Psychology,88"""

rows = list(csv.DictReader(io.StringIO(DATA)))
scores = [int(r["score"]) for r in rows]      # CSV values are STRINGS — convert!
print("class mean:", statistics.mean(scores))

by_major = {}
for r in rows:
    by_major.setdefault(r["major"], []).append(int(r["score"]))
print("by major:  ", {m: round(statistics.mean(v), 1) for m, v in by_major.items()})
'''}],
    9: [{"title": "regex_class_generator.py", "code": '''\
import re
print(re.fullmatch(r"\\w+@\\w+\\.edu", "ana@harvard.edu") is not None)   # True
m = re.search(r"([A-Z]{2})(\\d{4})", "Course ED1234 meets Tue")
print("dept:", m.group(1), "| number:", m.group(2))

class Student:
    def __init__(self, name, gpa):
        self.name = name
        self.gpa = gpa
    def __str__(self):
        return f"{self.name} ({self.gpa})"

roster = [Student("Ana", 3.9), Student("Ben", 1.8)]
print([str(s) for s in roster])

def gpas(students):           # a generator: yields one at a time
    for s in students:
        yield s.gpa

g = gpas(roster)
print("first pass: ", list(g))
print("second pass:", list(g))   # [] — a generator is exhausted after one pass
'''}],
}

CDN = {
    "marked": "https://cdn.jsdelivr.net/npm/marked@12.0.0/marked.min.js",
    "hljs_js": "https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js",
    "hljs_css": "https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github-dark.min.css",
}


def strip_frontmatter(md: str) -> str:
    """Remove a leading YAML front-matter block (--- ... ---) from slide markdown."""
    if md.startswith("---"):
        end = md.find("\n---", 3)
        if end != -1:
            nl = md.find("\n", end + 1)
            return md[nl + 1:].lstrip() if nl != -1 else ""
    return md


def wrap_solutions(md: str) -> str:
    """Wrap everything from a 'Solutions'/'Solution' heading onward in a <details>."""
    m = re.search(r"(?m)^#{2,4}\s+Solutions?\b.*$", md)
    if not m:
        return md
    before = md[:m.start()].rstrip()
    after = md[m.end():].lstrip("\n")
    return (before + "\n\n<details><summary>Show solutions</summary>\n\n"
            + after + "\n\n</details>\n")


def session_quiz_md(qfile_text: str, n: int) -> str:
    """Extract the '## Session N' block from quizzes.md and collapse its answers."""
    blocks = re.split(r"(?m)^##\s+Session\s+", qfile_text)
    for b in blocks[1:]:
        if b.lstrip().startswith(str(n)):
            block = "## Session " + b
            block = block.split("\n---")[0].rstrip()
            # collapse the answers into a <details>
            block = re.sub(r"\*\*Answers:\*\*",
                           "<details><summary>Show answers</summary>\n\n**Answers:**", block, count=1)
            if "<details>" in block:
                block += "\n\n</details>"
            # demote the H2 so it sits under our "Check yourself" H2
            block = block.replace("## Session " + str(n), "### Quiz", 1)
            return block
    return ""


def md_script(el_id: str, md: str) -> str:
    """Embed markdown safely inside a script tag (browser reads .textContent)."""
    safe = md.replace("</script", "<\\/script")  # guard (won't normally occur)
    return f'<script type="text/markdown" id="{el_id}">\n{safe}\n</script>'


def nav_html(active: str) -> str:
    links = [f'<a href="index.html"{" class=\"active\"" if active=="index" else ""}>Home</a>']
    for n, title, _desc, key in SESSIONS:
        page = f"session-{n:02d}"
        cls = []
        if active == page:
            cls.append("active")
        star = " ⭐" if key else ""
        cls_attr = f' class="{" ".join(cls)}"' if cls else ""
        links.append(f'<a href="{page}.html"{cls_attr} data-page="{page}" title="{html.escape(title)}">S{n}{star}</a>')
    links.append(f'<a href="cheatsheets.html"{" class=\"active\"" if active=="cheats" else ""}>Cheat sheets</a>')
    return ('<header class="site"><div class="nav-inner">'
            '<a class="brand" href="index.html">Python<span class="py">·</span>for Researchers</a>'
            f'<nav class="nav-links">{"".join(links)}</nav></div></header>')


def page_shell(title: str, active: str, body: str, scripts: str, page_id: str = "") -> str:
    pid = f' data-page="{page_id}"' if page_id else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="{CDN['hljs_css']}">
</head>
<body{pid}>
{nav_html(active)}
<main>
{body}
</main>
{scripts}
<script src="{CDN['marked']}"></script>
<script src="{CDN['hljs_js']}"></script>
<script src="assets/app.js"></script>
</body>
</html>
"""


def build_index() -> str:
    cards = []
    for n, title, desc, key in SESSIONS:
        page = f"session-{n:02d}"
        cls = "card key" if key else "card"
        star = " ⭐" if key else ""
        cards.append(
            f'<a class="{cls}" href="{page}.html" data-page="{page}">'
            f'<span class="done">✓</span>'
            f'<div class="n">SESSION {n}{star}</div>'
            f'<div class="t">{html.escape(title)}</div>'
            f'<div class="d">{html.escape(desc)}</div></a>')
    body = f"""
<h1 class="page-title">Python for Researchers</h1>

<h2>The sessions</h2>
<div class="cards">{''.join(cards)}</div>

<h2>Keep these open</h2>
<ul>
  <li><a href="cheatsheets.html">Traps &amp; Gotchas cheat sheet</a> — the quirks, wrong-vs-right (start here, Session&nbsp;2).</li>
  <li><a href="cheatsheets.html#quick-reference">Quick syntax reference</a> and <a href="cheatsheets.html#glossary">plain-language glossary</a>.</li>
</ul>
<p style="color:#5b6675;font-size:13.5px">Course structure follows CS50P (Weeks 0–9); all lessons, examples, and cheat sheets here are original.</p>
"""
    return page_shell("Python for Researchers — Home", "index", body, "")


def build_session(n: int, title: str, slides_dir: Path, examples_dir: Path, quizzes_text: str) -> str:
    lesson = strip_frontmatter((slides_dir / f"session-{n:02d}-slides.md").read_text())
    # practice file is practice.md in each example folder
    practice_path = examples_dir / f"session-{n:02d}" / "practice.md"
    practice = wrap_solutions(practice_path.read_text()) if practice_path.exists() else ""
    quiz = session_quiz_md(quizzes_text, n)
    quiz_block = (f'<h2>Check yourself</h2>\n<div id="quiz" class="md"></div>' if quiz else "")
    practice_block = (f'<h2>Practice</h2>\n<div id="practice" class="md"></div>' if practice else "")

    pg = PLAYGROUNDS.get(n, [])
    body = f"""
<article>
  <div id="lesson" class="md"></div>
  <section id="playgrounds"></section>
  {practice_block}
  {quiz_block}
  <div class="page-foot">
    <button id="complete-btn" class="complete-btn" type="button">Mark this session complete</button>
    <div class="foot-nav">
      {'<a href="session-%02d.html">&larr; Prev</a>' % (n-1) if n > 1 else '<a href="index.html">&larr; Home</a>'}
      {'<a href="session-%02d.html">Next &rarr;</a>' % (n+1) if n < 9 else '<a href="cheatsheets.html">Cheat sheets &rarr;</a>'}
    </div>
  </div>
</article>
"""
    scripts = "\n".join([
        md_script("lesson-md", lesson),
        md_script("practice-md", practice) if practice else "",
        md_script("quiz-md", quiz) if quiz else "",
        f'<script type="application/json" id="playgrounds-data">{json.dumps(pg)}</script>',
    ])
    return page_shell(f"Session {n} — {title}", f"session-{n:02d}", body, scripts, page_id=f"session-{n:02d}")


def build_cheats(cheats_dir: Path) -> str:
    traps = (cheats_dir / "traps-and-gotchas.md").read_text()
    quick = (cheats_dir / "quick-reference.md").read_text()
    gloss = (cheats_dir / "glossary.md").read_text()
    combined = (
        "# Cheat Sheets\n\n"
        "Jump to: [Traps &amp; Gotchas](#traps) · "
        "[Quick Reference](#quick-reference) · "
        "[Glossary](#glossary)\n\n"
        '<div id="traps"></div>\n\n' + traps +
        '\n\n---\n\n<div id="quick-reference"></div>\n\n' + quick +
        '\n\n---\n\n<div id="glossary"></div>\n\n' + gloss
    )
    body = '<div id="cheats" class="md"></div>'
    scripts = md_script("cheats-md", combined)
    return page_shell("Cheat Sheets — Python for Researchers", "cheats", body, scripts)


def main() -> None:
    slides_dir = ROOT / "slides"
    examples_dir = ROOT / "examples"
    cheats_dir = ROOT / "cheatsheets"
    quizzes_text = (ROOT / "assessments" / "quizzes.md").read_text()

    (DOCS / "assets").mkdir(parents=True, exist_ok=True)
    (DOCS / "index.html").write_text(build_index())
    for n, title, _desc, _key in SESSIONS:
        (DOCS / f"session-{n:02d}.html").write_text(
            build_session(n, title, slides_dir, examples_dir, quizzes_text))
    (DOCS / "cheatsheets.html").write_text(build_cheats(cheats_dir))
    # GitHub Pages: don't run Jekyll over our files
    (DOCS / ".nojekyll").write_text("")
    print(f"Built site into {DOCS}")
    for p in sorted(DOCS.glob("*.html")):
        print("  ", p.name)


if __name__ == "__main__":
    main()
