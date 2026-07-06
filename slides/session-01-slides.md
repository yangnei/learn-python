---
marp: true
title: "Session 1 — Running Python, Variables & Types"
paginate: true
---

# Session 1
## Running Python, Variables & Types

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

# Going deeper
## Numbers, strings & the tools around them

---

## Arithmetic, fully

| Op | Meaning | Example |
|---|---|---|
| `+ - *` | the usual | `3 * 7` → `21` |
| `/` | true division | `7 / 2` → `3.5` |
| `//` | floor division | `7 // 2` → `3` |
| `%` | remainder | `7 % 2` → `1` |
| `**` | power | `2 ** 10` → `1024` |

Precedence follows math (`**` first, then `* / // %`, then `+ -`) — when in doubt, **parenthesize**.
Update in place: `score += 5`, `count -= 1`, `total *= 2`.

---

## `%` earns its keep

```python
n % 2 == 0            # even?
student_id % 3        # 0, 1, or 2 -> rotate into 3 discussion groups
minutes = 130
print(minutes // 60, "h", minutes % 60, "min")   # 2 h 10 min
```

🧠 `//` and `%` together split a quantity into "whole units + remainder" — hours/minutes,
pages/sheets, groups/leftovers.

---

## Strings have methods

```python
name = "  aDA lovelace "
name.strip()          # "aDA lovelace"   (trim ends)
name.strip().title()  # "Ada Lovelace"   (chain them!)
"CS50".lower()        # "cs50"
"a,b,c".count(",")    # 2
"ana@uni.edu".startswith("ana")   # True
"@" in "ana@uni.edu"  # True  (membership)
len("data")           # 4
```

Methods **return a new string** — the original never changes (strings are immutable).

---

## f-strings, round 2 — aligned reports

```python
name, score, rate = "Ana", 91.456, 0.873
print(f"{name:<10}{score:>8.1f}{rate:>8.1%}")
# Ana           91.5   87.3%
```

- `:<10` pad left-aligned to 10 · `:>8` right-align to 8
- `:.1f` one decimal · `:,` thousands · `:.1%` percent
- `{score=}` prints `score=91.456` — debugging gold.

---

## Borrowing a toolbox: `import`

```python
import math
math.sqrt(144)     # 12.0
math.floor(3.9)    # 3
math.ceil(3.1)     # 4
math.pi            # 3.141592653589793
```

One line borrows a whole library. (The full import story — and `pip` — lands in Session 8.)

---

## Ask Python itself

```python
help(round)      # the manual for one function
dir(str)         # every method a string has
```

In the REPL, `_` holds the last result. These three habits replace half your web searches.

---

## Names that don't bite

- `snake_case` for variables and functions: `class_average`, not `ClassAvg`.
- Names say **what it is**: `n_students`, not `x`.
- Constants by convention: `MAX_SCORE = 100` (Python won't enforce it — the capitals warn humans).
- Comments explain **why**, not what: the code already says what.

---

## Your turn — round 2

`examples/session-01/practice.md` → **In class — going deeper**:
formatting drill, a name normalizer, and the `%`-groups exercise.
---

## Traps recap

- `input()` → **always a string**; convert with `int()`/`float()`.
- `print(a, b)` (comma → spaces) vs `print(a + b)` (must be same type).
- `int(3.9)` truncates to `3`; use `round()` to round.

## Summary
You can run code, name values, convert types, format output, and read an error.
**Next:** Session 2 — the dynamic-typing traps.

---

## Homework (before Session 2)

*Outside class — it doesn't count toward class time. Full specs + solutions: `examples/session-01/practice.md` → **Homework**.*

1. **Unit converter** — a script that asks for a value and reports it converted, nicely f-string formatted.
2. **Traceback drill** — break three lines on purpose; for each, read the last line and name the error.
3. **Type-prediction table** — predict `type(...)` for ten expressions, then check in the REPL.
