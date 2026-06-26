# Per-Session Quizzes (with answer keys)

Each quiz is 3–5 questions, ~5 minutes, given at the end of the hour. Every question maps to
a session objective. **Teacher:** ask the student to *predict* code output before they run it —
the surprise is the assessment. Answers are at the end of each session block.

---

## Session 1 — Variables & Types
1. What type does `input("x: ")` return, always?
2. What does `"5" + "3"` evaluate to? How do you get `8`?
3. What is `int(3.9)`? What is `round(3.9)`?
4. (Practical) Write one line that prints a float `score` to 2 decimal places.

**Answers:** 1. `str`. 2. `"53"`; use `int("5") + int("3")`. 3. `3` (truncates) and `4`.
4. `print(f"{score:.2f}")`.

---

## Session 2 — Dynamic-Typing Traps
1. `a = [1,2]; b = [1,2]` — is `a == b`? is `a is b`? Why?
2. What is `True + True`? Why?
3. Is `0.1 + 0.2 == 0.3` True or False? How should you compare them?
4. What does `5 == "5"` give? What about `5 > "5"`?
5. Is `[1,2] == (1,2)` True or False? Why?

**Answers:** 1. `==` True (same value), `is` False (different objects). 2. `2` (bool is a
subclass of int). 3. False; use `math.isclose(0.1+0.2, 0.3)` (or round). 4. `False`; `5 > "5"`
raises `TypeError` (can't order int vs str). 5. False — a list and a tuple are different types.

---

## Session 3 — Control Flow: Conditionals & Loops
1. Rewrite `if x >= 90 and x < 100:` using a chained comparison.
2. What is `5 and 0`? What is `0 or "hi"`? Why aren't they `True`/`False`?
3. Why is `if passed == True:` not ideal? Write the better version.
4. What does `list(range(1, 5))` produce?
5. Why can removing items from a list *while looping it* go wrong, and what's a clean fix?

**Answers:** 1. `if 90 <= x < 100:`. 2. `0` and `"hi"` — `and`/`or` return an operand, not a
bool. 3. `passed` is already a bool; write `if passed:`. 4. `[1, 2, 3, 4]` (5 excluded).
5. Removing shifts indices so the loop skips elements; iterate a copy or build a new list
(`[x for x in xs if keep(x)]`).

---

## Session 4 — Data Structures
1. Which are mutable: list, tuple, dict, set?
2. What does `xs.sort()` return? How do you get a *new* sorted list?
3. `a = [1,2]; b = a; a.append(3)` — what is `b`? Why?
4. (Practical) One-line dict comprehension mapping each name in `names` to `0`.

**Answers:** 1. list, dict, set are mutable; tuple is not. 2. `None` (sorts in place);
`sorted(xs)`. 3. `[1, 2, 3]` — `b` is an alias for the same list. 4. `{n: 0 for n in names}`.

---

## Session 5 — Functions & Scope
1. What's the difference between `return` and `print`?
2. Why is `def f(x, items=[])` dangerous? What's the fix?
3. What does a function return if it has no `return` statement?
4. Are type hints enforced at runtime?

**Answers:** 1. `return` hands a value to the caller; `print` only displays. 2. The default
list is created once and persists across calls; use `items=None` then create inside. 3. `None`.
4. No — they're documentation; `mypy` checks them optionally.

---

## Session 6 — Exceptions
1. Which exception does `int("N/A")` raise?
2. Why is a bare `except:` dangerous?
3. When should you use `raise` vs `assert`?
4. (Practical) Wrap `int(value)` so it returns `None` on failure.

**Answers:** 1. `ValueError`. 2. It catches everything (even Ctrl+C and your own typos) and
can hide bugs. 3. `raise` to validate real/untrusted input; `assert` for developer sanity
checks (can be disabled). 4. `try: return int(value) except (ValueError, TypeError): return None`.

---

## Session 7 — Files & Data
1. What does opening a file in `"w"` mode do to existing contents?
2. Why prefer `with open(...)` over `open()`/`close()`?
3. After `csv.DictReader`, what type is each row?
4. CSV values read from a file are what type — and what must you do with numbers?

**Answers:** 1. Truncates it to empty immediately. 2. `with` auto-closes the file even if the
code crashes. 3. A `dict` keyed by the header row. 4. Strings; convert with `int()`/`float()`.

---

## Session 8 — Regular Expressions
1. In regex, what does `.` match? How do you match a literal dot?
2. Why write regex patterns as raw strings `r"..."`?
3. Which function do you use to (a) check the *whole* string matches, and (b) replace matches?
4. What does `re.search` return when there's no match, and what must you do before `.group()`?

**Answers:** 1. Any character (except newline); use `\.` for a literal dot. 2. So backslashes
aren't treated as Python string escapes. 3. (a) `re.fullmatch`, (b) `re.sub`. 4. It returns
`None`; check `if m:` before calling `m.group()` or you'll hit an `AttributeError`.

---

## Session 9 — Modules, OOP & Pythonic
1. In a class, what is `self`?
2. What happens if you iterate a generator twice?
3. Why doesn't a module's `if __name__ == "__main__":` block run when you `import` it?
4. What does a `@property` setter let you do that a plain attribute can't?

**Answers:** 1. The current instance ("this particular object"). 2. The second pass is empty —
a generator is exhausted after one iteration. 3. On import, `__name__` is the module's name, not
`"__main__"`, so the block is skipped. 4. Validate (or transform) the value on every assignment,
so the object can reject bad data.

---

## Scoring guide (formative, not graded)
- **All correct, explained why:** ready for the capstone.
- **Right answer, fuzzy why:** re-do that session's `traps-and-gotchas` rows.
- **Wrong on Session 2 items:** revisit Session 2 before continuing — it's load-bearing.
