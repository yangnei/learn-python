# Session 2 — Practice: The Dynamic-Typing Traps

Type each solution yourself. **Predict every output before you run it.** Solutions at the bottom.

## In class

### Predict-the-output gauntlet
For each line, write *why* (one sentence). Predict, then run to check.

```python
True + True            # 2     — bools are ints; True is 1
3 == 3.0               # True  — numbers compare by value
0.1 + 0.2 == 0.3       # False — binary float rounding
5 == "5"               # False — different types, no error
5 > "5"                # 💥    — can't ORDER int vs str
[1,2] == (1,2)         # False — list vs tuple are different types
bool("0")              # True  — non-empty string is truthy
x=[1]; y=x; x.append(2); y   # [1,2] — y is an alias of x
```

### Build `clean_score()`
Write a function that safely turns a value into a float on a 0–100 scale:

```python
def clean_score(value):
    """
    Accept 87, 87.0, or "87" and return 87.0 (a float).
    - Reject anything outside 0..100 with a clear message (return None).
    - Compare floats safely (no exact ==).
    """
```
Test it on: `87`, `87.0`, `"87"`, `"eighty"`, `120`, `True`.
*What does `True` do, and why? (Hint: bool is an int...)*

### Bonus — Pythonic idiom drill
Cover the `# ->` answers, predict each line, then run.

```python
x = int("257"); y = int("257")
print(x == y, x is y)                # -> True False   (equal value, different objects)
print(float("nan") == float("nan"))  # -> False        (NaN equals nothing, not even itself)
```

## In class — going deeper (second hour)

### E1 — isinstance drill
Predict each, then run:
```python
isinstance(True, int)
type(True) is int
isinstance(3.0, int)
isinstance("3", (int, float))
isinstance(3, (int, float))
```

### E2 — Same value, same object?
Without running: after `a = [1, 2]; b = [1, 2]; c = a`, what are `a == b`, `a is b`,
`a is c`? Now `c.append(3)` — what is `a`? Run and check all four.

### D1 — Conversion-matrix predictions
Predict each, then run: `int("42")` · `int("4.2")` · `float("4.2")` · `int(4.9)` ·
`int(float("4.2"))` · `str(4.2) + "!"` · `bool("False")`.

### D2 — `Decimal` re-run
Show that `Decimal("0.1") + Decimal("0.2") == Decimal("0.3")` where floats said False —
and check the grade weights: does `0.1 + 0.2 + 0.3 == 0.6` fix itself with `Decimal`?
Why must you build Decimals from **strings**?

### D3 — `describe(x)`
Return `"missing"` for `None`, `"empty"` for `""`, `"zero"` for `0`/`0.0` (but **not**
`False`), else `"value"`. Prove it on `[None, "", 0, 0.0, False, "0", 5]`.
(Careful: `False == 0` — Session 2's own trap. What tool tells them apart?)

## Homework (before Session 3)

*~30–45 minutes, outside class — it doesn't count toward class time. Try everything before peeking at the solutions.*

### H1 — Trap journal
From today's ~18 traps, pick the **five** that surprised you most. For each, write down:
the one-line code, your wrong expectation, and *why* Python answers differently — one
sentence, your own words. (This journal is the seed of your personal cheat sheet.)

### H2 — `approx_equal(a, b, tol=1e-9)`
Write the float comparison you'll use instead of `==` from now on; it must make
`approx_equal(0.1 + 0.2, 0.3)` come out `True`. Do it once by hand (`abs`), once with
`math.isclose`.

### H3 — `is_missing(x)`
Return `True` **only** for `None` — not for `0`, `0.0`, `""`, or `False`. Prove it on all
five. (Hint: this is exactly what `is` is for.)

---

## Solutions

### In class

```python
import math

def clean_score(value):
    # Reject bools explicitly — they'd sneak through as ints (True == 1).
    if isinstance(value, bool):
        print(f"Rejected {value!r}: looks like a flag, not a score.")
        return None
    try:
        score = float(value)              # handles int, float, and numeric strings
    except (ValueError, TypeError):
        print(f"Rejected {value!r}: not a number.")
        return None
    if not 0 <= score <= 100:
        print(f"Rejected {value!r}: out of range 0–100.")
        return None
    return score

for v in [87, 87.0, "87", "eighty", 120, True]:
    print(v, "->", clean_score(v))
# 87->87.0, 87.0->87.0, "87"->87.0, "eighty"->None, 120->None, True->None
```
Key lesson: `float(True)` is `1.0`, so without the explicit bool check a flag would
pass as a valid score. This is the `bool ⊂ int` trap in a real function.

### In class — going deeper

```python
# E1
isinstance(True, int)          # True  — bool is a subclass of int
type(True) is int              # False — the exact type is bool
isinstance(3.0, int)           # False — float is not an int subclass
isinstance("3", (int, float))  # False — a numeric-LOOKING string is still a str
isinstance(3, (int, float))    # True  — the tuple means "any of these"

# E2
a == b   # True  — same values
a is b   # False — two separate list objects
a is c   # True  — c is another label on a's object
# after c.append(3): a == [1, 2, 3] — mutating through c shows through a
```

```python
# D1
int("42")          # 42
# int("4.2")       -> ValueError — int() parses integer text only
float("4.2")       # 4.2
int(4.9)           # 4  (truncates)
int(float("4.2"))  # 4  (the two-step)
str(4.2) + "!"     # '4.2!'
bool("False")      # True — any non-empty string is truthy!

# D2
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))                    # True
print(Decimal("0.1") + Decimal("0.2") + Decimal("0.3") == Decimal("0.6"))   # True
# From strings, because Decimal(0.1) would copy the float's binary error in.

# D3
def describe(x):
    if x is None:
        return "missing"
    if x == "":
        return "empty"
    if isinstance(x, bool):        # bool ⊂ int — check the flag FIRST
        return "value"
    if isinstance(x, (int, float)) and x == 0:
        return "zero"
    return "value"

for v in [None, "", 0, 0.0, False, "0", 5]:
    print(repr(v), "->", describe(v))
# None missing · "" empty · 0 zero · 0.0 zero · False value · "0" value · 5 value
```

### Homework

H1 — any five, e.g.: `0.1 + 0.2 == 0.3` (binary floats), `True == 1` (bool ⊂ int),
`5 == "5"` (no cross-type conversion), `[1, 2] == (1, 2)` (list ≠ tuple), `is` on equal
lists (identity ≠ equality). The *why* in your own words matters more than the pick.

```python
# H2
import math

def approx_equal(a, b, tol=1e-9):
    return abs(a - b) <= tol
    # or: return math.isclose(a, b, abs_tol=tol)

print(approx_equal(0.1 + 0.2, 0.3))   # True

# H3
def is_missing(x):
    return x is None          # identity — only None itself passes

for v in [None, 0, 0.0, "", False]:
    print(repr(v), "->", is_missing(v))   # only None -> True
```
