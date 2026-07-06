# Per-Session Quizzes (with answer keys)

Each quiz is 5–6 questions (the last one or two from the Going-deeper hour), ~8 minutes,
given at the end of the session. Every question
maps to a session objective. **Teacher:** ask the student to *predict* code output before
they run it — the surprise is the assessment. Answers are at the end of each session block.

---

## Session 1 — Running Python, Variables & Types
1. What type does `input("x: ")` return, always?
2. What does `"5" + "3"` evaluate to? How do you get `8`? And what is `int(3.9)`?
3. What does `f"{0.873:.1%}"` produce?
4. In a traceback, which line do you read first — and what two things does it tell you?
5. What are `17 // 5` and `17 % 5` — and name one practical use of `%`.

**Answers:** 1. `str`. 2. `"53"`; use `int("5") + int("3")`; `int(3.9)` is `3` (truncates,
doesn't round). 3. `"87.3%"`. 4. The **last** line: the exception's name (what kind of
problem) and the message (the offending value or detail). 5. `3` and `2`; `%` gives the remainder — even/odd tests, rotating IDs into k groups, splitting minutes into h + min.

---

## Session 2 — The Dynamic-Typing Traps
1. `a = [1,2]; b = [1,2]` — is `a == b`? Is `a is b`? Why?
2. What is `True + True`? Why?
3. Is `0.1 + 0.2 == 0.3` True or False? How *should* you compare them?
4. What does `5 == "5"` give? What about `5 > "5"`?
5. Which of these are falsy: `"0"`, `""`, `[0]`, `[]`, `None`, `0.0`?
6. Why does `Decimal("0.1") + Decimal("0.2") == Decimal("0.3")` hold when the float version doesn't — and why build Decimals from strings?

**Answers:** 1. `==` True (same value), `is` False (different objects in memory).
2. `2` — bool is a subclass of int (`True` acts as `1`). 3. False (binary float rounding);
use `math.isclose(0.1 + 0.2, 0.3)` or round. 4. `False` (no error); `5 > "5"` raises
`TypeError` — Python can't *order* int vs str. 5. `""`, `[]`, `None`, `0.0` are falsy;
`"0"` and `[0]` are truthy (non-empty). 6. `Decimal` stores base-10 digits exactly, so there's no binary rounding; built from a float (`Decimal(0.1)`) it would inherit the float's error.

---

## Session 3 — Control Flow: Conditionals & Loops
1. Rewrite `if x >= 90 and x < 100:` using a chained comparison.
2. What is `5 and 0`? What is `0 or "hi"`? Why aren't they `True`/`False`?
3. What does `list(range(1, 5))` produce?
4. What goes wrong when you `remove` items from a list while looping over it — and what's
   the fix?
5. When does the `else` clause on a `for` loop run?

**Answers:** 1. `if 90 <= x < 100:`. 2. `0` and `"hi"` — `and`/`or` return an *operand*,
not a bool. 3. `[1, 2, 3, 4]` (5 excluded — off-by-one). 4. Removal shifts the remaining
indices, so elements get skipped; build a new list instead
(`[x for x in xs if keep(x)]`) or iterate over a copy. 5. Only when the loop finishes **without** `break` — the "searched everything, found nothing" branch.

---

## Session 4 — Data Structures
1. Which are mutable: list, tuple, dict, set?
2. `a = [1,2]; b = a; a.append(3)` — what is `b`? Why?
3. (Practical) Write a one-line dict comprehension mapping each name in `names` to `0`.
4. `xs.sort()` vs `sorted(xs)` — what does each return?
5. You need "have I seen this ID before?" over thousands of IDs — which structure, and why?
6. What does `Counter(['a','b','a']).most_common(1)` return?

**Answers:** 1. list, dict, set are mutable; tuple is not. 2. `[1, 2, 3]` — `b` is an
alias for the *same* list (assignment doesn't copy). 3. `{n: 0 for n in names}`.
4. `.sort()` sorts in place and returns `None`; `sorted()` returns a *new* sorted list.
5. A `set` — membership tests are fast and duplicates are impossible by construction. 6. `[('a', 2)]` — a list of (value, count) pairs, biggest first.

---

## Session 5 — Functions, Scope & Reusability
1. What's the difference between `return` and `print`?
2. Why is `def f(x, items=[])` dangerous? What's the fix?
3. What does a function with no `return` statement return? Are type hints enforced at
   runtime?
4. `count = 0` at top level, then inside a function `count = count + 1` — what error, and
   why?
5. In one sentence: what does a decorator do, and what is `@d` above a `def f` sugar for?

**Answers:** 1. `return` hands a value to the caller; `print` only displays it.
2. The default list is created once, at `def` time, and persists across calls; use
`items=None` then create inside. 3. `None`; and no — hints are documentation (`mypy`
checks them optionally). 4. `UnboundLocalError` — the assignment makes `count` local to
the function, so the right-hand side reads a local that doesn't exist yet. 5. It wraps a function with extra behavior; `@d` is exactly `f = d(f)`.

---

## Session 6 — Recursion & Recursive Thinking
1. What two parts must every recursive function have?
2. What error comes from a base case that's never reached, and why doesn't Python just
   keep going?
3. Why is recursion a natural fit for nested data (a list of lists, or nested JSON)?
4. The recursive case computes `n * f(n - 1)` but has no `return` in front — what does a
   call produce?
5. Naive recursive `fib(35)` takes seconds but `@functools.cache` makes it instant — what does the cache change?

**Answers:** 1. A **base case** (stops) and a **recursive case** (calls itself on a
smaller input, *toward* the base case). 2. `RecursionError` — Python has no tail-call
optimization, so each pending call keeps a stack frame until the limit (~1000).
3. The data is *defined in terms of itself* (a list may contain lists), so a function
defined in terms of itself mirrors its shape and reaches every level. 4. `None` — the
value is computed and thrown away; the function falls off the end. 5. Each distinct input is computed once and remembered, so the exponential tree of repeated subcalls collapses into ~35 lookups.

---

## Session 7 — Exceptions & Defensive Code
1. Which exception does `int("N/A")` raise? Wrap `int(value)` so it returns `None` on
   failure.
2. Why is a bare `except:` dangerous?
3. When should you use `raise` vs `assert`?
4. Name the two validation styles — and give the EAFP version of converting `value` to an
   int.
5. Why must `except ValueError:` come before `except Exception:`?

**Answers:** 1. `ValueError`;
`try: return int(value)` / `except (ValueError, TypeError): return None`.
2. It catches *everything* (even Ctrl+C and your own typos) and can hide bugs.
3. `raise` to validate real/untrusted input; `assert` for developer sanity checks (it can
be disabled with `python -O`). 4. LBYL ("look before you leap": `if value.isdigit():`)
vs EAFP ("easier to ask forgiveness"): `try: n = int(value)` / `except ValueError: ...`. 5. Handlers are tried top-down and `Exception` matches a `ValueError` too — placed first it would swallow everything, leaving the specific handler unreachable.

---

## Session 8 — Files, Libraries & Research Data
1. What does opening a file in `"w"` mode do to existing contents? Why prefer
   `with open(...)`?
2. After `csv.DictReader`, what type is each row?
3. CSV values read from a file are what type — and what must you do with numbers?
4. Your second loop over an open file object sees nothing — why, and what's the fix?
5. What do `strptime` and `strftime` each do — and why seed `random` in an analysis script?

**Answers:** 1. Truncates it to empty *immediately*; `with` auto-closes the file even if
the code crashes. 2. A `dict` keyed by the header row. 3. Strings; convert with
`int()`/`float()`. 4. The file cursor is exhausted after one pass — re-open the file (or
read it into a list first). 5. `strptime` parses text → datetime; `strftime` formats datetime → text; seeding makes the "random" sample reproducible for your methods section.

---

## Session 9 — Regular Expressions & Text Cleaning
1. In regex, what does `.` match? How do you match a literal dot?
2. Why write regex patterns as raw strings `r"..."`?
3. What does `re.search` return when there's no match, and what must you do before
   `.group()`?
4. `re.search` vs `re.fullmatch` — which one is for validation, and why?
5. What does `re.IGNORECASE` change, and what is `re.VERBOSE` for?

**Answers:** 1. Any character (except newline); use `\.` for a literal dot. 2. So
backslashes aren't treated as Python string escapes. 3. It returns `None`; check `if m:`
before `m.group()` or you'll hit an `AttributeError`. 4. `fullmatch` — it anchors both
ends, so the *whole* string must fit the pattern; `search` would accept a valid-looking
fragment inside garbage. 5. `IGNORECASE` matches regardless of case; `VERBOSE` lets a pattern span lines with comments so a colleague can actually review it.

---

## Session 10 — Modules, OOP & the Pythonic Toolkit
1. In a class, what is `self`?
2. What happens if you iterate a generator twice?
3. Why doesn't a module's `if __name__ == "__main__":` block run when you `import` it?
4. `class Course: students = []` — what goes wrong when two `Course` objects enroll
   students, and what's the fix?
5. In a dataclass, why write `courses: list = field(default_factory=list)` instead of `= []`?

**Answers:** 1. The current instance ("this particular object"). 2. The second pass is
empty — a generator is exhausted after one iteration. 3. On import, `__name__` is the
module's name, not `"__main__"`, so the block is skipped. 4. `students` is a *class*
variable shared by every instance, so both courses see one combined list; give each its
own in `__init__`: `self.students = []`. 5. A bare `[]` default would be created once and shared by every instance — the Session 5 mutable-default bug in class form; `default_factory` builds a fresh list per instance.

---

## Scoring guide (formative, not graded)
- **All correct, explained why:** ready for the next session (or the capstone).
- **Right answer, fuzzy why:** re-do that session's `traps-and-gotchas` rows.
- **Wrong on Session 2 items:** revisit the type traps before continuing — they're
  load-bearing for everything after.
