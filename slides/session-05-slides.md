---
marp: true
title: "Session 5 — Functions, Scope & Reusability"
paginate: true
---

# Session 5
## Functions, Scope & Reusability

Define a rule once; apply it everywhere. (Reproducibility!)

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

add_student("Ana")    # ['Ana']
add_student("Ben")    # ['Ana', 'Ben']  — the list PERSISTS!
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

`examples/session-05/practice.md`:
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
**Next:** make them survive messy real-world input — exceptions.
