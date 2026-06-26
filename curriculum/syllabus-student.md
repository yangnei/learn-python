# Python for Researchers — Student Syllabus

Welcome. This is a fast, 10-hour path from "never coded" to "I can write a real Python program
to wrangle my research data." It is re-ordered for you and front-loaded with the language
quirks that trip people up.

**How each hour runs:** Concept (≈15 min) → I code, you watch (≈10 min) → you code (≈25 min) →
Traps recap (≈5 min) → Summary + quiz (≈5 min). You will *type every example yourself*.

**What you need:** Python 3.11+, VS Code (or any editor), and this folder. Open the matching
`slides/`, `examples/`, and `cheatsheets/` file for each session.

---

## The 10 sessions (1 hour each)

| # | Title | You'll be able to… | Files |
|---|---|---|---|
| 1 | **Running Python, Variables & Types** | Run code, use `int/float/str/bool/None`, do input/output with f-strings | `slides/session-01` · `examples/session-01` |
| 2 | **The Dynamic-Typing Traps** | Tell `==` from `is`, predict `True==1` / `0.1+0.2` / `5=="5"`, check types right | `slides/session-02` · `cheatsheets/traps-and-gotchas` |
| 3 | **Conditionals & Boolean Logic** | Write clean `if/elif/else`, chained comparisons, `match`, avoid `== True` | `slides/session-03` · `examples/session-03` |
| 4 | **Loops & Iteration** | `for`/`while`, `break`/`continue`, `range`/`enumerate`/`zip`, validation loops | `slides/session-04` · `examples/session-04` |
| 5 | **Data Structures** | Use `list/tuple/dict/set`, comprehensions, sorting, understand aliasing | `slides/session-05` · `examples/session-05` |
| 6 | **Functions, Scope & Reuse** | Write reusable functions, `*args/**kwargs`, type hints; dodge the mutable-default bug | `slides/session-06` · `examples/session-06` |
| 7 | **Exceptions & Defensive Code** | Validate messy input with `try/except`, raise errors, write a first test | `slides/session-07` · `examples/session-07` |
| 8 | **Files, Libraries & Research Data** | Read/write CSV survey data, use `statistics`/`datetime`, `pip install`, pandas teaser | `slides/session-08` · `examples/session-08` |
| 9 | **Regular Expressions & Text Cleaning** | Validate, extract, and clean real text with regex patterns & capture groups | `slides/session-09` · `examples/session-09` |
| 10 | **Modules, OOP & the Pythonic Toolkit** | Import modules; build a small class with `@property`; use generators/`map`/`filter` | `slides/session-10` · `examples/session-10` |
| 11 | **Capstone (optional)** | Build a Gradebook & Survey Analyzer end-to-end | `assessments/capstone-project` |

Session 2 is the most load-bearing hour — if you deeply master one, make it that one.

---

## Your standing toolkit (open these any time)
- **`cheatsheets/traps-and-gotchas.md`** — every quirk, with the wrong vs right way. *Keep this open.*
- **`cheatsheets/quick-reference.md`** — syntax you'll forget (slicing, f-strings, comprehensions).
- **`cheatsheets/glossary.md`** — plain-language definitions of every term.

## How to study (specific to this material)
1. **Type, don't read.** Re-type every example in `examples/`; change one thing and predict the result *before* you run it.
2. **Predict-then-run on traps.** For S2 especially, guess the output, then run. The surprise *is* the lesson.
3. **Keep a "bugs I hit" log.** When you get a traceback, write the last line + your fix. After 9 hours you'll have your own personalized cheat sheet.
4. **Connect to what you know.** Every session opens with how the concept maps to research methods/stats (see `connection-map.md`). Lean on those bridges.

## What "done" looks like
You finish the capstone (S10) or, at minimum, complete every session's practice block and score
the per-session quizzes in `assessments/`. The real test: you can open a messy CSV of your own
data and write a short script that summarizes it without copying from anyone.

## Scope (so you're not surprised)
This makes you a confident *programmer who handles research data*. It is **not** a full data-science
course — pandas, plotting, and statistical modeling get a taste, not a deep dive. Those are the
natural next step once these fundamentals are solid.
