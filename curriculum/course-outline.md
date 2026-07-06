# Master Course Outline — Learn Python

> Single source of truth. The student and teacher syllabi both derive from this.
> **10 core two-hour sessions** + 1 optional capstone session (~20 hours core, ~22 with
> the capstone). Every session pairs a **core** hour with a **Going deeper** hour of new
> material, and assigns **homework (~30–45 min)** that does *not* count toward class time.

## How the topics are sequenced

A typical intro-Python course teaches roughly: functions/variables → conditionals →
loops → exceptions → libraries → unit tests → file I/O → regular expressions → OOP →
assorted "power-tools."

We **re-sequence** for a fast adult learner, and we front-load the dynamic-typing traps —
they're the whole reason this course exists. The 10 sessions run in five natural pairs,
each pair sharing a through-line (name it when you cross between them):

1. **Types (S1) → the type traps (S2).** You can't reason about the traps until you know
   the types — so they lead, back to back, on days one and two.
2. **Control flow (S3) → data structures (S4).** Loops are most useful over the
   containers worth looping; a list of dicts is just a dataset.
3. **Functions (S5) → recursion (S6).** Recursion is a function that calls itself, so it
   lands while function mechanics are fresh — and nested data (from S4) is the payoff.
4. **Exceptions (S7) → files & research data (S8).** Surviving one dirty value scales
   straight into cleaning a whole CSV of them.
5. **Regex (S9) → modules & OOP (S10).** The two "finishing" skills: clean any text, then
   organize code into modules and a small class.

The power-tools (comprehensions, generators, `*args`, type hints, the walrus) are folded
into the sessions where they naturally belong, not saved for the end.

## Design rules (from the e-learning pipeline)
- **Every session = two hours = one topic, twice as deep**: warm-up → core concept →
  live example → practice → **break** → going-deeper concept → live example → practice →
  recap + quiz. The second hour is **new material** (never overflow practice); the two
  practice blocks total ~30 min of protected hands-on time.
- Every session assigns **homework** (in `examples/session-NN/practice.md` →
  *Homework*): ~30–45 min outside class, solutions included, reviewed in the next
  session's warm-up. The practice file's **In class — going deeper** block belongs to
  the second hour.
- Every session has 3–5 learning objectives across its core and going-deeper halves;
  every objective is testable in that session's quiz.
- Every abstract idea ships with a runnable, education-flavored example.
- Difficulty rises monotonically; nothing is used before it's introduced (except
  clearly-flagged teasers).

---

## Session 1 — Running Python, Variables & Types

**Objectives**
1. Run Python interactively (REPL) and as a `.py` script; read a traceback without panic
   (last line first).
2. Use the core types (`int`, `float`, `str`, `bool`, `None`); check them with `type()`.
3. Do I/O with `input()`/`print()`, f-strings, and `int()`/`float()`/`str()` casting —
   and remember `input()` is *always* a `str`.

**Going deeper (second hour):** the full operator set (`// % **`), string methods,
aligned f-strings, `import math`, `help()`/`dir()`, naming conventions.
**Trap focus:** `input()` returns text (`"5" + "3"` is `"53"`); `int(3.9)` truncates;
`print(a, b)` vs `print(a + b)`.
**Homework:** unit converter; traceback drill; type-prediction table.

---

## Session 2 — The Dynamic-Typing Traps *(the core of the course)*

**Objectives**
1. Distinguish **value equality (`==`)** from **identity (`is`)**; keep `is` for `None`.
2. Predict `bool ⊂ int` (`True == 1`, summing flags), int/float mixing, and **float
   precision** (`0.1 + 0.2`); compare floats with `math.isclose`.
3. Handle cross-type comparison (`5 == "5"` is `False`, `5 > "5"` raises); check types
   with `isinstance()` vs `type()`; reason about truthiness.

**Why it leads:** front-loading the traps — right after the types they concern — means
every later session can assume the fluency.
**Going deeper (second hour):** `None` semantics, the conversion matrix, `nan`/`inf`,
mutable vs immutable + `id()`, exact arithmetic with `Decimal`.
**Trap focus:** the ~18-trap predict-then-run gauntlet *is* the session.
**Homework:** trap journal (5 traps in your own words); `approx_equal`; `is_missing`.

---

## Session 3 — Control Flow: Conditionals & Loops

**Objectives**
1. Write `if`/`elif`/`else` with comparison & logical operators and **chained
   comparisons**; use `and`/`or`/`not` correctly (short-circuit, operand-return); avoid
   `if x == True`.
2. Write `for`/`while` loops; control them with `break`/`continue`; mind the `range`
   off-by-one; run the `while True:` validation loop.
3. Iterate Pythonically with `enumerate`/`zip` instead of `range(len(...))`.

**Going deeper (second hour):** the ternary, `match/case`, `for/else`, nested loops,
the named loop patterns (accumulator, counter, best-so-far, sentinel).
**Trap focus:** `if x == True`; `range(1,5)` excludes 5; mutating a list while iterating
it; `range(len(...))`.
**Homework:** attendance labeler (boundary testing); number-guessing game; leap-year
checker.

---

## Session 4 — Data Structures

**Objectives**
1. Choose between `list`/`tuple`/`dict`/`set`; index, slice, and nest them — a **list of
   dicts is a dataset**.
2. Build list/dict **comprehensions**; sort with `sorted(key=…)`.
3. Reason about **mutability & aliasing** (copy vs reference, `[[0]*3]*3` shared rows).

**Going deeper (second hour):** unpacking, dict power methods, `Counter`/`defaultdict`,
full set algebra, multi-key sorting, `copy` vs `deepcopy`.
**Trap focus:** aliasing (`b = a` shares the list); `.sort()` returns `None`;
`dict.get()` vs `KeyError`; the shared-row grid.
**Homework:** gradebook dict drill; frequency counter; fix-the-grid.

---

## Session 5 — Functions, Scope & Reusability

**Objectives**
1. Define functions with positional, keyword, default, `*args`, and `**kwargs`
   parameters; know `return` vs `print`.
2. Explain scope (LEGB) and dodge the `UnboundLocalError`/`global` trap.
3. Document with docstrings and **type hints** (and know hints aren't enforced).

**Going deeper (second hour):** functions as values, closures, a first decorator,
keyword-only arguments, doctests.
**Trap focus:** the **mutable default argument** bug; forgetting to `return`; assigning
to a global inside a function.
**Homework:** a tiny stats library; `mean_ignoring_none(*values)`; scope-prediction
drill.

---

## Session 6 — Recursion & Recursive Thinking

**Objectives**
1. Write a recursive function with a correct **base case** and **recursive case**; trace
   the **call stack**.
2. Convert between recursion and iteration; know recursion's cost (`RecursionError`, no
   tail-call optimization, limit ≈ 1000).
3. Apply recursion to **naturally nested data** (nested lists/dicts/JSON) where one loop
   is awkward.

**Going deeper (second hour):** memoization (`@functools.cache`), binary search,
tree-shaped data, the explicit-stack escape from the recursion limit.
**Trap focus:** an unreachable base case → stack overflow; forgetting to `return` the
recursive call.
**Homework:** `sum_digits`; `deep_count` on a nested gradebook; loop-vs-recursion
paragraph.

---

## Session 7 — Exceptions & Defensive Code

**Objectives**
1. Handle errors with `try`/`except`/`else`/`finally`; `raise` deliberately; validate
   messy human/research input the EAFP way.
2. Know the common exception types on sight (`ValueError`, `TypeError`, `KeyError`,
   `FileNotFoundError`, …).
3. Use `assert` for developer checks (never input validation) and write a first `pytest`
   test.

**Going deeper (second hour):** the exception hierarchy & handler order, custom
exceptions that carry data, `raise ... from`, `logging`, parametrized tests.
**Trap focus:** bare `except:`; swallowing errors; `assert` ≠ validation.
**Homework:** `ask_int` (EAFP validation loop); three more pytest cases; error triage.

---

## Session 8 — Files, Libraries & Research Data

**Objectives**
1. Read/write text with `open`/`with` and understand file modes (why `"w"` is
   dangerous).
2. Load and write **CSV** survey/gradebook data with `csv.DictReader`/`DictWriter`;
   touch `json`.
3. `import` the researcher's stdlib (`statistics`, `datetime`, `pathlib`),
   `pip install` a package, and meet `pandas` in a guided teaser.

**Going deeper (second hour):** `pathlib`, encodings, `csv.reader` vs `DictReader`,
JSON for nested data, `datetime`, seeded `random`, the extended pandas teaser.
**Trap focus:** `"w"` silently overwrites; forgotten `newline=""`; reading a file twice;
CSV values are strings.
**Homework:** attendance-report pipeline; JSON round-trip; run the pipeline on your own
CSV.

---

## Session 9 — Regular Expressions & Text Cleaning

**Objectives**
1. Write patterns with raw strings and the survival tokens; know when *not* to use regex.
2. Use `re.search`/`fullmatch`/`findall`/`sub` to validate, extract (capture groups),
   and clean real research text.

**Going deeper (second hour):** flags, `re.compile`, `re.VERBOSE`, named groups,
greedy vs lazy, `re.sub` with a function replacement, regex over files.
**Trap focus:** forgetting `r"..."`; `.` matches any char; `re.search` returns `None` —
guard before `.group()`.
**Homework:** pattern drill (IDs, phones, dates); messy-name cleanup; domain harvest.

---

## Session 10 — Modules, OOP & the Pythonic Toolkit

**Objectives**
1. Split code into modules and `import` them; understand the
   `if __name__ == "__main__":` guard.
2. Model a domain entity with a small **class** (`__init__`, `self`, `__str__`, a
   validating `@property`, brief inheritance with `super()`).
3. Apply the **Pythonic toolkit**: comprehensions, `map`/`filter`, generators/`yield`,
   the walrus `:=`.

**Going deeper (second hour):** `__repr__`/`__eq__`/`__lt__`, dataclasses with
`default_factory`, `@classmethod` constructors, composition vs inheritance,
generator pipelines, project layout.
**Trap focus:** `self` confusion; a generator exhausts after one pass; the shared class
variable; over-using a class where a function/dict fits.
**Homework:** `Student` with computed GPA; a `Cohort` class; Pythonic rewrite of three
loops.

---

## Session 11 (Optional) — Capstone Project *(integrative)*

**Objective:** independently build one small, end-to-end program on a real-ish education
dataset. Default brief: **"Gradebook & Survey Analyzer"** — read a CSV of students +
Likert responses, clean and validate it, compute summary statistics, flag at-risk
students, and write a report CSV. Alternative briefs are listed in
`assessments/capstone-project.md`. Plan ~2 hours.

---

## Coverage check (every core topic lands somewhere)
| Topic | Where it lives now |
|---|---|
| Running Python, variables & types | S1 |
| The dynamic-typing traps (`==`/`is`, floats, `bool⊂int`, `isinstance`) | S2 |
| Conditionals & loops | S3 |
| Data structures (list/tuple/dict/set) | S4 |
| Functions, scope & reuse | S5 |
| Recursion | S6 (nested data ties back to S4) |
| Exceptions & unit tests | S7 |
| Files & libraries (CSV, `statistics`, `pandas` teaser) | S8 |
| Regular expressions | S9 |
| Modules & OOP | S10 |
| Power-tools (comprehensions, `*args`, type hints, generators, `map`/`filter`, walrus) | S4, S5, S10 |

## Scaling to the time budget
- **~14–16 hours:** keep every core hour; trim each Going-deeper block to its two or
  three starred essentials (each session's *cut line* names them).
- **~20 hours:** run S1–S10 as written, two hours each (recommended).
- **~22 hours:** add the S11 capstone.
