---
marp: true
title: "Session 3 — Functions, Scope & Recursion"
paginate: true
---

# Session 3
## Functions, Scope & Recursion

*Learn Python — a two-hour session, in two halves.*

**Part A:** Functions, Scope & Reusability  ·  **Part B:** Recursion & Recursive Thinking

---

# Part A
## Functions, Scope & Reusability

---

## Defining & calling

```python
def class_average(scores):
    """Return the mean of a list of scores."""
    return sum(scores) / len(scores)

class_average([91, 58, 73])     # 74.0
```

🧠 A function is a formula/coding-scheme: same input → same output.

---

## return vs print

```python
def avg(xs): return sum(xs) / len(xs)   # hands value back
def show(xs): print(sum(xs) / len(xs))  # just displays

x = avg([1,2,3])     # x = 2.0
y = show([1,2,3])    # prints 2.0, but y is None!
```

`print` shows; `return` gives the value to the next step.

---

## Parameters: positional, keyword, default

```python
def grade(score, scale=100, passing=60):
    ...
grade(85)                 # uses defaults
grade(85, passing=50)     # keyword arg
```

⚠️ Defaults must be **immutable** (numbers, strings, `None`) — never `[]` or `{}`.

---

## *args / **kwargs

```python
def total(*args):        # any number of positionals -> tuple
    return sum(args)
total(1, 2, 3)           # 6

def tag(**kwargs):       # any number of keywords -> dict
    return kwargs
tag(name="Ana", gpa=3.9) # {'name':'Ana','gpa':3.9}

func(*my_list)           # unpack list into args
func(**my_dict)          # unpack dict into kwargs
```

---

## TRAP: mutable default argument 😱

```python
def add_student(name, roster=[]):    # ❌
    roster.append(name)
    return roster

add_student("Ana")    # ?
add_student("Ben")    # ?  ← does the list persist? (Traps below)
```

The default `[]` is created **once**, at definition. Fix on next slide.

---

## The fix: default to None

```python
def add_student(name, roster=None):   # ✅
    if roster is None:
        roster = []
    roster.append(name)
    return roster
```

**Rule:** mutable default? Use `None` and create inside.

---

## Scope (LEGB) & globals

Python looks up names: **L**ocal → **E**nclosing → **G**lobal → **B**uilt-in.

```python
count = 0
def bump():
    count = count + 1   # 💥 UnboundLocalError
```
Assigning `count` makes it local. Avoid `global`; **return** a value and reassign instead.

---

## Docstrings & type hints

```python
def class_average(scores: list[float]) -> float:
    """Return the arithmetic mean of `scores`."""
    return sum(scores) / len(scores)
```

Type hints document intent. **They are NOT enforced at runtime** (`mypy` checks them).

---

## Your turn

`examples/session-03/practice.md`:
1. A small grade-functions module (with docstrings + hints).
2. Reproduce the mutable-default bug, then fix it.
3. `summary(*scores)` using `*args`.

---

## Traps recap

- Mutable default arg → use `None`.
- `print` ≠ `return` (forgot return → `None`).
- Assigning a global inside a function → `UnboundLocalError`.
- Type hints aren't enforced.

## Summary
You can write reusable, documented, reproducible functions.
**Next:** *Part B of this session* — recursion.

---

# Part B
## Recursion & Recursive Thinking

---

## The shape of every recursion

Real example: how many prerequisites deep is a course?

```python
prereq_of = {"ED700": "ED600", "ED600": "ED500",
             "ED500": "ED400", "ED400": None}   # ED400 has none

def prereqs_deep(course):
    earlier = prereq_of[course]
    if earlier is None:               # BASE CASE — stop here
        return 0
    return 1 + prereqs_deep(earlier)  # RECURSIVE CASE — step back one
```

Two parts, always:
- a **base case** that stops, and
- a **recursive case** that moves *toward* the base case.

---

## Trace the call stack

`orderings(n)` = ways to rank *n* students = n!

```python
orderings(3)
= 3 * orderings(2)
=     3 * (2 * orderings(1))
=         3 * (2 * 1)          # base case returns 1
= 6
```

Each call waits on the one inside it. The calls stack up, then unwind.

🧠 Each pending call is a **stack frame** — that matters in a moment.

---

## Recursion vs iteration

```python
def orderings(n):                 # ways to rank n students (n!)
    if n <= 1:
        return 1
    return n * orderings(n - 1)   # ← must RETURN the call

def orderings_loop(n):
    total = 1
    for k in range(2, n + 1):
        total *= k
    return total
```

Same answer. For flat counting, the **loop** is usually clearer.

---

## Where recursion shines: nested data

```python
def deep_sum(obj):
    if isinstance(obj, (int, float)):
        return obj
    if isinstance(obj, dict):
        return sum(deep_sum(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return sum(deep_sum(x) for x in obj)
    return 0

deep_sum([1, [2, [3, 4]], {"a": 6}])   # 16
```

Nested JSON, folder trees, threaded replies — a single loop can't reach all the way down. Recursion can.

---

## The trap: no base case

```python
def runaway(n):
    return runaway(n + 1)     # never stops
```

```
RecursionError: maximum recursion depth exceeded
```

Python has **no tail-call optimization** — every call keeps its frame
(default limit ≈ 1000). Deep recursion *will* hit the ceiling.

---

## Your turn

`examples/session-03/practice.md`:
1. Recursive `total(scores)` — sum a list of scores; name the base case first.
2. `flatten([1, [2, [3, 4]], 5])` → one flat list.
3. `depth(...)` — how deeply is a list nested?

---

## Traps recap

- Every recursion needs a **reachable base case**, or it overflows the stack.
- **Return** the recursive call — forgetting to gives you a silent `None`.
- Recursion isn't free: each call costs a stack frame (no tail-call optimization).
- A plain **loop** is better for flat sequences and for very deep work.

## Summary
You can solve problems that are defined in terms of themselves — especially nested data.
**Next:** Exceptions, files & research data.
