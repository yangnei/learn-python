# Learn Python — Course Package

A complete, ready-to-teach Python course for a **PhD-in-Education student with no prior coding
experience** but strong self-learning skills. The pace is accelerated and the course is
deliberately front-loaded with the **easily-missed language fundamentals** (the dynamic-typing
"traps") that beginners skip and later get bitten by.

- **Length:** **9 one-hour sessions** + an optional 10th capstone hour.
- **Two editions:** a clean **student** track and a **teacher** track (timing, transitions, misconceptions).
- **Everything original.** All prose, slides, code, and cheat sheets here were written for this learner.

> Built with three methods: **personalized-syllabus** (bridges to education-research background),
> **e-learning-course-creator** (the brief→curriculum→lessons→assessments pipeline), and the
> **DeepTutor** tutoring approach (Socratic prompts, predict-then-run, per-session quizzes,
> a running "misconceptions log"). *Note: the DeepTutor pedagogy is baked into the teacher notes;
> the actual self-hosted DeepTutor server is not provisioned here.*

## Two ready-to-use formats
- **Student → interactive website** (`docs/`): a GitHub Pages-ready site where the student runs
  **real Python in the browser** (via Pyodide — nothing to install), with editable code on every
  session page, collapsible solutions, self-checking quizzes, and progress tracking. The site also
  offers a **downloadable student PDF** (`docs/learn-python-student.pdf`) for offline reading. See
  [Hosting on GitHub Pages](#hosting-the-student-site-on-github-pages).
- **Teacher → PDF** (`output/teacher-edition.pdf`): the full instructor playbook (minute-by-minute
  clocks, transition scripts, predicted misconceptions, Socratic prompts) + the outline, connection
  map, and quiz keys as appendices. Print it or read on screen.

## Start here
1. **Teacher:** open `output/teacher-edition.pdf` (or read `curriculum/syllabus-teacher.md`).
2. **Student:** open the website (`docs/index.html` locally, or the GitHub Pages URL once hosted).
3. Both: skim `curriculum/connection-map.md` — why each concept connects to research methods.
4. Keep the Cheat sheets page (or `cheatsheets/traps-and-gotchas.md`) open the entire course.

## Hosting the student site on GitHub Pages
1. Put this folder in a GitHub repo and push.
2. Repo **Settings → Pages → Build and deployment**: Source = *Deploy from a branch*,
   Branch = `main`, Folder = **`/docs`**. Save.
3. Your site goes live at `https://<user>.github.io/<repo>/` in a minute or two.
4. The first time a student clicks **Run**, the browser downloads the Python engine (~10 MB) once,
   then everything runs locally. Requires an internet connection (for the CDN libraries); after the
   first load it's cached. To preview locally: `cd docs && python3 -m http.server` then open
   `http://localhost:8000`.

## Regenerating the outputs
All artifacts are generated from the markdown — edit the source, then rebuild:
```bash
# Student website  ->  docs/
python3 tools/build_site.py

# Teacher PDF  ->  output/teacher-edition.pdf       (needs the `markdown` package + chromium)
# Student PDF  ->  docs/learn-python-student.pdf
python3 -m venv .venv && .venv/bin/pip install markdown
.venv/bin/python tools/build_teacher_pdf.py
.venv/bin/python tools/build_student_pdf.py
```
The site itself needs no build dependencies (it renders markdown client-side); only the two PDF
builds need `markdown` + a headless Chromium.

## What's in the box
```
learn-python/
├── README.md                       ← you are here
├── brief/
│   └── course-brief.md             ← audience, outcomes, scope (the "why")
├── curriculum/
│   ├── course-outline.md           ← master plan; the single source of truth for all sessions
│   ├── syllabus-student.md         ← STUDENT edition
│   ├── syllabus-teacher.md         ← TEACHER edition (timing, transitions, Socratic prompts)
│   └── connection-map.md           ← Python ⇄ education-research bridges (personalization)
├── slides/
│   └── session-01..09-slides.md    ← Marp-compatible slide decks (one per session)
├── examples/
│   └── session-01..09/             ← runnable demo.py + practice.md (+ sample CSVs in S7)
├── cheatsheets/
│   ├── traps-and-gotchas.md        ← the quirks, wrong-vs-right, all verified
│   ├── quick-reference.md          ← syntax you'll forget
│   └── glossary.md                 ← plain-language definitions
├── assessments/
│   ├── quizzes.md                  ← per-session quizzes + answer keys
│   └── capstone-project.md         ← the Gradebook & Survey Analyzer
├── docs/                           ← STUDENT interactive website (GitHub Pages)
│   ├── index.html, session-01..09.html, cheatsheets.html
│   ├── learn-python-student.pdf    ← downloadable student edition (offline reading)
│   └── assets/ (style.css, app.js) ← Pyodide-powered runnable code, quizzes, progress
├── output/
│   └── teacher-edition.pdf         ← TEACHER edition, print-ready
└── tools/
    ├── build_site.py               ← regenerates docs/ from the markdown
    ├── build_teacher_pdf.py        ← regenerates the teacher PDF
    └── build_student_pdf.py        ← regenerates the student PDF
```

## The 9 sessions at a glance
| # | Title |
|---|---|
| 1 | Running Python, Variables & Types |
| 2 | The Dynamic-Typing Traps |
| 3 | Control Flow: Conditionals & Loops |
| 4 | Data Structures (list/tuple/dict/set) |
| 5 | Functions, Scope & Reusability |
| 6 | Exceptions & Defensive Code |
| 7 | Files, Libraries & Research Data |
| 8 | Regular Expressions & Text Cleaning |
| 9 | Modules, OOP & the Pythonic Toolkit |
| 10 | Capstone (optional) |

## How to render the slides (optional)
The decks are plain Markdown with `---` slide breaks and Marp front-matter. To export to
HTML/PDF: `npx @marp-team/marp-cli slides/session-02-slides.md -o session-02.html`.
They also read fine as-is in any Markdown viewer.

## How to run the examples
Each `examples/session-XX/demo.py` is self-contained:
```bash
cd examples/session-02 && python3 traps_demo.py
cd examples/session-07 && python3 demo.py     # reads the bundled CSVs
```
Requires Python 3.11+. The only optional third-party packages are `pytest` (Session 6 test)
and `pandas` (Session 7 teaser); everything else is the standard library.

## Scaling to the available time
- **~8 hours:** fold the Pythonic-toolkit half of S9 into S4/S5 and drop the pandas teaser.
- **9 hours:** run S1–S9 as written (recommended).
- **10 hours:** add the S10 capstone.

## Note
All instructional content in this package — prose, slides, code, cheat sheets, and quizzes —
is original.
