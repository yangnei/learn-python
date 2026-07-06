# Learn Python — Student Syllabus

Welcome. This is a fast, ~10-hour path (**ten one-hour sessions**, plus an optional
capstone) from "never coded" to "I can write a real Python program to wrangle my research
data." It's re-ordered for you and front-loaded with the language quirks that trip people
up.

**How each 1-hour session runs:** a 5-minute warm-up on last time's traps and homework,
then Concept (≈20 min) → I code, you watch (≈12 min) → **you code (≈18 min)** → recap +
quiz (5 min). The practice is the biggest block on purpose — you learn by typing. You
will *type every example yourself*.

**Homework:** every session assigns ~30–45 minutes of homework (the **Homework** section
of that session's `practice.md`). It does **not** count toward class time, solutions are
included, and the next session's warm-up starts from it. If you finish in-class practice
early, each practice file also has an **Extra practice** block.

**What you need:** Python 3.11+, VS Code (or any editor), and this folder. Open the
matching `slides/`, `examples/`, and `cheatsheets/` file for each session. (A full
**PDF** of the course is downloadable from the website, and every session is also a
**Jupyter notebook** you can run in the browser — no install.)

---

## The 10 sessions (1 hour each, + homework)

| # | Title | You'll be able to… |
|---|---|---|
| 1 | **Running Python, Variables & Types** | Run code (REPL + scripts), use `int/float/str/bool/None`, f-strings, casting, read a traceback |
| 2 | **The Dynamic-Typing Traps** | Tell `==` from `is`, predict `True==1` / `0.1+0.2` / `5=="5"`, check types with `isinstance`, truthiness |
| 3 | **Control Flow: Conditionals & Loops** | `if/elif/else`, chained comparisons, `for`/`while`, `break`/`continue`, `enumerate`/`zip`, the validation loop |
| 4 | **Data Structures** | `list/tuple/dict/set`, slicing, a list of dicts as a dataset, comprehensions, sorting, aliasing |
| 5 | **Functions, Scope & Reusability** | Write reusable functions, `*args/**kwargs`, type hints, LEGB, dodge the mutable-default bug |
| 6 | **Recursion & Recursive Thinking** | Base + recursive case, trace the call stack, recurse over nested data, know the limits |
| 7 | **Exceptions & Defensive Code** | Validate messy input with `try/except`, `raise`, EAFP, a first `pytest` test |
| 8 | **Files, Libraries & Research Data** | Read/write CSV survey data, `statistics`/`datetime`/`pathlib`, `pip install`, pandas teaser |
| 9 | **Regular Expressions & Text Cleaning** | Validate, extract, and clean real text with `re` + capture groups |
| 10 | **Modules, OOP & the Pythonic Toolkit** | Import modules, build a small class with `@property`, generators/`map`/`filter`/walrus |
| 11 | **Capstone (optional)** | Build a Gradebook & Survey Analyzer end-to-end |

Files for session N: `slides/session-NN-slides.md` · `examples/session-NN/`.
Session 2's **type traps** are the most load-bearing material in the course — if you
deeply master one session, make it that one.

---

## Your standing toolkit (open these any time)
- **`cheatsheets/traps-and-gotchas.md`** — every quirk, with the wrong vs right way. *Keep this open.*
- **`cheatsheets/quick-reference.md`** — syntax you'll forget (slicing, f-strings, comprehensions).
- **`cheatsheets/glossary.md`** — plain-language definitions of every term.

## How to study (specific to this material)
1. **Type, don't read.** Re-type every example in `examples/`; change one thing and predict the result *before* you run it.
2. **Predict-then-run on traps.** For Session 2 especially, guess the output, then run. The surprise *is* the lesson.
3. **Do the homework the same day.** ~30–45 min while it's fresh; check the solutions only after a real attempt.
4. **Keep a "bugs I hit" log.** When you get a traceback, write the last line + your fix. You'll build your own personalized cheat sheet (Session 2's homework starts it).
5. **Connect to what you know.** Every topic maps to research methods/stats (see `connection-map.md`). Lean on those bridges.

## What "done" looks like
You finish the capstone (S11) or, at minimum, complete every session's practice +
homework and score the per-session quizzes in `assessments/`. The real test: you can open
a messy CSV of your own data and write a short script that summarizes it without copying
from anyone.

## Scope (so you're not surprised)
This makes you a confident *programmer who handles research data*. It is **not** a full
data-science course — pandas, plotting, and statistical modeling get a taste, not a deep
dive. Those are the natural next step once these fundamentals are solid.
