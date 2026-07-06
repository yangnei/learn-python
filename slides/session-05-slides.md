---
marp: true
title: "Session 5 — Functions, Scope & Reusability"
paginate: true
---

# Session 5
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
Bigger projects standardize docstring fields (`:param:`, `:return:`, `:raises:`) so
tools like **Sphinx** can build a documentation website straight from the code.

---

## Your turn

`examples/session-05/practice.md`:
1. A small grade-functions module (with docstrings + hints).
2. Reproduce the mutable-default bug, then fix it.
3. `summary(*scores)` using `*args`.

---

# Going deeper
## Functions as values

---

## Functions are objects

```python
f = letter_grade            # no () — the function itself
f(85)                       # "B"
sorted(roster, key=grade_of)          # you've been passing functions since Session 4
stats = {"mean": class_average, "max": max}
stats["mean"]([91, 58, 73])           # dispatch by name
```

`key=lambda …` was never magic — you were handing `sorted` a function.

---

## `lambda`, honestly

```python
lambda s: s["score"]        # one expression, no statements, no docstring
```

Perfect as a throwaway `key=`. The moment it needs a second line or a name to be
understood — promote it to `def`.

---

## Closures: functions that remember

```python
def make_curver(bonus):
    def curve(score):
        return min(score + bonus, 100)
    return curve             # a function, with `bonus` baked in

gentle = make_curver(5)
harsh_year = make_curver(2)
gentle(96)                   # 100
```

A **factory** for functions. (The lambda-in-a-loop trap earlier is this — capture happens by
variable, not by value.)

---

## A first decorator

```python
def announce(f):
    def wrapper(*args, **kwargs):
        print(f"calling {f.__name__}{args}")
        return f(*args, **kwargs)
    return wrapper

@announce                    # sugar for: curve = announce(curve)
def curve(score):
    return min(score + 5, 100)
```

A decorator **wraps** a function with extra behavior. You'll *use* them constantly
(`@property`, `@cache`, `@pytest.mark...`) — now you know what the `@` does.

---

## Locking the call signature

```python
def curve(scores, *, bonus=5):     # everything after * is keyword-only
    ...
curve(xs, bonus=3)     # ✅ self-documenting
curve(xs, 3)           # 💥 TypeError — no mystery positional flags
```

Keyword-only arguments make call sites readable a month later.

---

## Docstrings that test themselves

```python
def class_average(scores):
    """Mean of scores.

    >>> class_average([90, 80, 70])
    80.0
    """
    return sum(scores) / len(scores)
```

`python -m doctest grades.py` runs every `>>>` example and complains on mismatch —
documentation that can't silently rot.

---

## Your turn — round 2

`examples/session-05/practice.md` → **In class — going deeper**:
your own `apply_to_all`, a curve factory, an `@announce` decorator, and a doctest.
---

## Traps recap

- Mutable default arg → use `None`.
- `print` ≠ `return` (forgot return → `None`).
- Assigning a global inside a function → `UnboundLocalError`.
- Type hints aren't enforced.

## Summary
You can write reusable, documented, reproducible functions.
**Next:** Session 6 — recursion.

---

## Homework (before Session 6)

*Outside class — it doesn't count toward class time. Full specs + solutions: `examples/session-05/practice.md` → **Homework**.*

1. **A tiny stats library** — `validate_score`, `curve`, `summarize`, with docstrings + type hints.
2. **`mean_ignoring_none(*values)`** — `*args` meets data cleaning.
3. **Scope-prediction drill** — say what prints *before* you run it.
