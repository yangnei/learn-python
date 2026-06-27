# Session 2 — Practice (60 min)

## Part A — Explain the gauntlet (25 min)
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

## Part B — `clean_score()` (35 min)
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

## Bonus — Pythonic idiom drill
Cover the `# ->` answers, predict each line, then run.

```python
x = int("257"); y = int("257")
print(x == y, x is y)                # -> True False   (equal value, different objects)
print(float("nan") == float("nan"))  # -> False        (NaN equals nothing, not even itself)
```

---
## Solution

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
