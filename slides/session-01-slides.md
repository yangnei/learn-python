---
marp: true
title: "Session 1 — Running Python, Variables & Types"
paginate: true
---

# Session 1
## Running Python, Variables & Types

*Learn Python*

Goal: run code, use the 5 core types, do input/output.

---

## Why Python (for you)

- Free, readable, the lingua franca of research computing.
- Glue between your data, your stats, and your writing.
- Today: from zero to "I ran a program."

> Mantra for the whole course: **readability wins**.

---

## Two ways to run Python

1. **REPL** — type `python3`, get `>>>`, run one line at a time. Great for experiments.
2. **Script** — save `hello.py`, run `python3 hello.py`. Great for real work.

```python
# hello.py
print("Hello, researcher")
```

---

## Variables = labels on objects

```python
n = 30          # an int
mean = 3.7      # a float
name = "Ada"    # a str
passed = True   # a bool
missing = None  # "no value"
```

`=` is an **action** ("stick this label on that object"), **not** a math equation.
So `n = n + 1` is fine.

🧠 In stats you name quantities (`n`, `α`). Same idea — but the name can be re-pointed.

---

## The 5 core types

| Type | Example | Think |
|---|---|---|
| `int` | `30` | counts |
| `float` | `3.7` | measurements |
| `str` | `"Ada"` | text |
| `bool` | `True`/`False` | flags |
| `NoneType` | `None` | missing |

`type(x)` tells you which.

---

## Input & output

```python
name = input("Your name: ")        # ⚠️ ALWAYS a str
age  = int(input("Your age: "))    # convert right away
print("Hi", name, "— age", age)
```

**The #1 week-one trap:** `input()` gives you text.
`"5" + "3"` is `"53"`, not `8`.

---

## f-strings (use these)

```python
score = 87.456
print(f"{name} scored {score:.1f}")   # one decimal
print(f"{1234567:,}")                  # 1,234,567
print(f"{0.873:.1%}")                  # 87.3%
```

Cleaner than `+` concatenation and no type errors.

---

## Type conversion (casting)

```python
int("42")     # 42
float("3.14") # 3.14
str(42)       # "42"
int(3.9)      # 3   (truncates, doesn't round!)
round(3.9)    # 4
```

`int(input(...))` = read text, convert to number, in one step.

---

## Reading a traceback (don't panic)

```text
Traceback (most recent call last):
  File "x.py", line 3, in <module>
    age = int(input("Age: "))
ValueError: invalid literal for int() with base 10: 'thirty'
```

**Read the LAST line first.** It names the problem: `ValueError`, and the bad value `'thirty'`.

---

## Live demo & your turn

- Live: `greet.py`, then a "years to graduation" calculator. We'll break it once on purpose.
- You: `examples/session-01/practice.md` — build a GPA-or-BMI style script.

---

## Traps recap

- `input()` → **always a string**; convert with `int()`/`float()`.
- `print(a, b)` (comma → spaces) vs `print(a + b)` (must be same type).
- `int(3.9)` truncates to `3`; use `round()` to round.

## Summary
You can run code, name values, convert types, format output, and read an error.
**Next:** the dynamic-typing traps.
