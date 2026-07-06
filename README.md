# Learn Python — Course Package

A complete, ready-to-teach Python course for a **PhD-in-Education student with no prior coding
experience** but strong self-learning skills. The pace is accelerated and the course is
deliberately front-loaded with the **easily-missed language fundamentals** (the dynamic-typing
"traps") that beginners skip and later get bitten by.

- **Length:** **10 two-hour sessions** (~20 hours) + an optional 11th capstone session. Each
  session = a **core** hour + a **Going deeper** hour of new material around a break, and
  assigns **homework (~30–45 min)** that doesn't count toward class time.
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
- **Student → Jupyter notebooks** (`docs/notebooks/`): every session is also a self-contained
  `.ipynb`. Each session page links three ways to run it — **Run in browser** (a hosted
  [JupyterLite](https://jupyterlite.readthedocs.io/) app in `docs/jupyter/`, no install),
  **Open in Colab**, and **Download .ipynb** for local Jupyter/VS Code.
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

# Jupyter notebooks  ->  docs/notebooks/*.ipynb   (from examples/, no extra deps)
python3 tools/build_notebooks.py

# In-browser JupyterLite app  ->  docs/jupyter/   (one-time tooling, then rebuild)
python3 -m venv .venv-jlite
.venv-jlite/bin/pip install jupyterlite-core jupyterlite-pyodide-kernel jupyter-server
bash tools/build_jupyterlite.sh

# Teacher PDF  ->  output/teacher-edition.pdf       (needs the `markdown` package + chromium)
# Student PDF  ->  docs/learn-python-student.pdf
python3 -m venv .venv && .venv/bin/pip install markdown
.venv/bin/python tools/build_teacher_pdf.py
.venv/bin/python tools/build_student_pdf.py
```
The site and notebooks need no special dependencies (the site renders markdown client-side; the
notebook generator is plain Python). The PDF builds need `markdown` + a headless Chromium, and the
JupyterLite app needs the `jupyterlite-*` tooling shown above. Regenerate notebooks **before**
rebuilding JupyterLite so the in-browser copies stay in sync.

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
│   └── session-01..10-slides.md    ← Marp slide decks (one per session)
├── examples/
│   └── session-01..10/             ← runnable demo.py + practice.md (+ CSVs in S8, grades.py in S10)
├── cheatsheets/
│   ├── traps-and-gotchas.md        ← the quirks, wrong-vs-right, all verified
│   ├── quick-reference.md          ← syntax you'll forget
│   └── glossary.md                 ← plain-language definitions
├── assessments/
│   ├── quizzes.md                  ← per-session quizzes + answer keys
│   └── capstone-project.md         ← the Gradebook & Survey Analyzer
├── docs/                           ← STUDENT interactive website (GitHub Pages)
│   ├── index.html, session-01..10.html, cheatsheets.html
│   ├── learn-python-student.pdf    ← downloadable student edition (offline reading)
│   ├── notebooks/session-01..10.ipynb  ← one Jupyter notebook per session (+ -try/-traps)
│   ├── jupyter/                    ← hosted JupyterLite app (run notebooks in-browser)
│   └── assets/ (style.css, app.js) ← Pyodide-powered runnable code, quizzes, progress
├── output/
│   └── teacher-edition.pdf         ← TEACHER edition, print-ready
└── tools/
    ├── build_site.py               ← regenerates docs/ from the markdown
    ├── build_notebooks.py          ← regenerates docs/notebooks/*.ipynb from examples/
    ├── build_jupyterlite.sh        ← rebuilds the in-browser JupyterLite app
    ├── build_teacher_pdf.py        ← regenerates the teacher PDF
    └── build_student_pdf.py        ← regenerates the student PDF
```

## The 10 sessions at a glance (two hours each, + homework)
| # | Title |
|---|---|
| 1 | Running Python, Variables & Types |
| 2 | The Dynamic-Typing Traps |
| 3 | Control Flow: Conditionals & Loops |
| 4 | Data Structures |
| 5 | Functions, Scope & Reusability |
| 6 | Recursion & Recursive Thinking |
| 7 | Exceptions & Defensive Code |
| 8 | Files, Libraries & Research Data |
| 9 | Regular Expressions & Text Cleaning |
| 10 | Modules, OOP & the Pythonic Toolkit |
| 11 | Capstone (optional) — Gradebook & Survey Analyzer, end to end |

The sessions run in five natural pairs (types→traps, control flow→data structures,
functions→recursion, exceptions→files, regex→modules/OOP); each pair shares a through-line.

## How to render the slides (optional)
The decks are plain Markdown with `---` slide breaks and Marp front-matter. To export to
HTML/PDF: `npx @marp-team/marp-cli slides/session-01-slides.md -o session-01.html`.
They also read fine as-is in any Markdown viewer.

## How to run the examples
Each `examples/session-XX/demo.py` is self-contained:
```bash
cd examples/session-01 && python3 demo.py     # variables & types
cd examples/session-08 && python3 demo.py     # reads the bundled CSVs
```
Requires Python 3.11+. The only optional third-party packages are `pytest` (Session 7 test)
and `pandas` (Session 8 teaser); everything else is the standard library.

## Scaling to the available time
- **~14–16 hours:** keep every core hour; trim the Going-deeper blocks to the essentials
  named by each session's cut line.
- **~20 hours:** run S1–S10 as written, two hours each (recommended).
- **~22 hours:** add the S11 capstone.

## Note
All instructional content in this package — prose, slides, code, cheat sheets, and quizzes —
is original.
