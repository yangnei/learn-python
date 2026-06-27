# Master Course Outline — Learn Python

> Single source of truth. The student and teacher syllabi both derive from this.
> **10 core one-hour sessions** + 1 optional capstone hour.

## How the topics are sequenced

A typical intro-Python course teaches roughly: functions/variables → conditionals → loops →
exceptions → libraries → unit tests → file I/O → regular expressions → OOP → assorted
"power-tools."

We **re-sequence** for a fast adult learner: dynamic-typing fundamentals come forward into
Session 2; conditionals and loops are taught together as one "control flow" hour (they're the
two halves of the same idea, and a fast learner clears them quickly); and the power-tools
(comprehensions, generators, `*args`, type hints) are folded into the sessions where they
naturally belong instead of left to the end. **Recursion** gets its own session right after
Functions (S6): it's a function that calls itself, so it lands best while function mechanics are
fresh — and Data Structures (S4) is already in hand for the nested-data payoff.

## Design rules (from the e-learning pipeline)
- Every session = one hour, structured **Concept → Live Example → Practice → Traps → Summary**.
- **Practice is the biggest block (~30 min) and is packed** — this learner moves fast, so each
  session's practice carries enough tasks to fill the time without padding.
- Every session has 2–4 learning objectives; every objective is testable in that session's quiz.
- Every abstract idea ships with a runnable, education-flavored example.
- Difficulty rises monotonically; nothing is used before it's introduced (except clearly-flagged teasers).

---

## Session 1 — Running Python, Variables & Types
**Objectives**
1. Run Python both interactively (REPL) and as a `.py` script; read a traceback without panic.
2. Use variables and the core built-in types: `int`, `float`, `str`, `bool`, `None`.
3. Do I/O with `input()`/`print()`, format with f-strings, and convert types with `int()`/`float()`/`str()`.

**Key idea the beginner misses:** `input()` *always* returns a `str`; numbers from users must be converted.

---

## Session 2 — The Dynamic-Typing Traps (THE CORE SESSION)
**Objectives**
1. Distinguish **value equality (`==`)** from **identity (`is`)** and know when each is correct.
2. Predict results when mixing numeric types: `bool` ⊂ `int`, `int`/`float`, and **float precision**.
3. Check types correctly with `isinstance()` vs `type()`, and reason about truthiness.

**This is the session the whole course is built around** — it front-loads every trap in the
learner's brief (`==` vs `is`, `True == 1`, `3 == 3.0`, `0.1 + 0.2`, `5 == "5"` vs `5 > "5"`,
sequence comparison, `isinstance`). Everything later assumes this fluency.

---

## Session 3 — Control Flow: Conditionals & Loops
**Objectives**
1. Write `if`/`elif`/`else` with comparison & logical operators and **chained comparisons**;
   use `and`/`or`/`not` correctly (short-circuit, operand-return) and avoid `if x == True`.
2. Write `for` and `while` loops; control them with `break`/`continue`; mind `range` off-by-one.
3. Iterate the Pythonic way with `enumerate` and `zip`, and build the `while True:` validation loop.

**Trap focus:** `if x == True`/`is None`, `=` vs `==`, `range(1,5)` excludes 5, mutating a list
while iterating it, reaching for `range(len(...))` instead of `enumerate`/`zip`.

---

## Session 4 — Data Structures: list, tuple, dict, set
**Objectives**
1. Choose between `list`, `tuple`, `dict`, and `set`; index, slice, and nest them.
2. Sort with `sorted(..., key=...)` and lambdas; build **list/dict comprehensions**.
3. Reason about **mutability & aliasing** (copy vs reference, shallow vs deep copy).

**Trap focus:** aliasing (`b = a`), `list * n` shared rows, mutable default arguments (preview),
element-by-element sequence comparison, set deduplication of survey data.

---

## Session 5 — Functions, Scope & Reusability
**Objectives**
1. Define functions with positional, keyword, default, `*args`, and `**kwargs` parameters.
2. Explain scope (LEGB), `return` vs `print`, and avoid the `UnboundLocalError`/`global` trap.
3. Document with docstrings and annotate with **type hints** (and know hints aren't enforced).

**Trap focus:** the **mutable default argument** bug, late-binding closures, implicit `None` return.

---

## Session 6 — Recursion & Recursive Thinking
**Objectives**
1. Write a recursive function with a correct **base case** and a **recursive case**; trace the
   **call stack** and convert between recursion and iteration.
2. Reason about recursion's cost: a missing base case → `RecursionError`, and Python has no
   tail-call optimization (each pending call keeps a stack frame, default limit ~1000).
3. Apply recursion to **naturally nested data** (nested lists/dicts, JSON, trees) where a single loop is awkward.

**Trap focus:** missing/unreachable base case (infinite recursion → stack overflow), forgetting to
`return` the recursive call (silent `None`), assuming recursion is free, reaching for recursion where
a plain loop reads more clearly.

---

## Session 7 — Exceptions & Defensive Code
**Objectives**
1. Handle errors with `try`/`except`/`else`/`finally`; raise `ValueError` etc. deliberately.
2. Validate real, messy human/research input robustly (EAFP "ask forgiveness" style).
3. Use `assert` and write a first `pytest` test for a function.

**Trap focus:** bare `except:`, catching too broadly, swallowing errors silently.

---

## Session 8 — Files, Libraries & Research Data
**Objectives**
1. Read/write text with `open`/`with`; understand file modes and why `with` matters.
2. Load and write **CSV** survey/gradebook data with `csv.DictReader`/`DictWriter`; touch `json`.
3. `import` standard-library tools a researcher reaches for (`statistics`, `random`, `datetime`,
   `pathlib`) and install a third-party package with `pip` (guided `pandas` teaser).

**Trap focus:** `"w"` silently overwrites, forgotten `newline=""`/`\n`, file encoding.

---

## Session 9 — Regular Expressions & Text Cleaning
**Objectives**
1. Write patterns with raw strings and the core tokens (`. \d \w \s + * ? {m,n} ^ $ [] () |`).
2. Use `re.search`/`fullmatch`/`findall`/`sub` to validate, extract (capture groups), and clean text.
3. Apply regex to real research text: validate IDs/emails, extract codes, normalize and mine free responses.

**Trap focus:** `.` matches *any* char (use `\.`), forgetting raw strings, `re.search` returns `None`,
reaching for regex where a string method is clearer.

---

## Session 10 — Modules, OOP & the Pythonic Toolkit
**Objectives**
1. Split code into modules and `import` them; understand the `if __name__ == "__main__":` guard.
2. Model a domain entity with a small **class** (`__init__`, `self`, `__str__`, a validating `@property`, brief inheritance with `super()`).
3. Apply the "Pythonic" toolkit: comprehensions, `map`/`filter`, `enumerate`/`zip`, generators/`yield`, the walrus `:=`.

**Trap focus:** `self` confusion, a generator exhausts after one pass, over-using a class where a function/dict fits.

---

## Session 11 (Optional) — Capstone Project *(integrative)*
**Objective:** Independently build one small, end-to-end program on a real-ish education dataset.
Default brief: **"Gradebook & Survey Analyzer"** — read a CSV of students + Likert responses,
clean and validate it, compute summary statistics, flag at-risk students, and write a report CSV.
Alternative briefs are listed in `assessments/capstone-project.md`.

---

## Coverage check (every core topic lands somewhere)
| Topic | Where it lives here |
|---|---|
| Functions & variables | S1, S5 |
| Conditionals | S3 (+ traps in S2) |
| Loops | S3 (+ iterating data in S4) |
| Recursion | S6 (nested data ties to S4) |
| Exceptions | S7 |
| Libraries | S8 |
| Unit tests | S7 (+ modules in S10) |
| File I/O | S8 (+ data structures S4) |
| Regular expressions | S9 |
| Modules & OOP | S10 |
| Power-tools (sets, comprehensions, `*args`, type hints, generators, `map`/`filter`) | S4, S5, S10 |

## Scaling to the time budget
- **~8 hours:** fold the Pythonic-toolkit half of S10 into S4/S5 and trim the `pandas` teaser
  (recursion, S6, stays — it's a core skill, not an add-on).
- **10 hours:** run S1–S10 as written (recommended).
- **11 hours:** add the S11 capstone.
