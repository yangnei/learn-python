---
marp: true
title: "Session 7 — Exceptions & Defensive Code"
paginate: true
---

# Session 7
## Exceptions & Defensive Code

Real research data is dirty. Make code that survives it.

---

## try / except

```python
try:
    n = int(value)
except ValueError:
    n = None        # handle the bad case
```

When code might fail at runtime, wrap it. The `except` catches the named error.

---

## Common exception types

| Exception | Happens when |
|---|---|
| `ValueError` | right type, bad value: `int("N/A")` |
| `TypeError` | wrong type: `5 > "5"` |
| `KeyError` | missing dict key: `d["nope"]` |
| `IndexError` | bad list index: `xs[99]` |
| `ZeroDivisionError` | `x / 0` |
| `FileNotFoundError` | `open("missing.csv")` |

---

## try / except / else / finally

```python
try:
    n = int(value)
except ValueError:
    print("not a number")
else:
    print("ok:", n)      # only if NO exception
finally:
    print("always runs")  # cleanup
```

---

## Raise your own

```python
def clean_likert(n):
    if not 1 <= n <= 5:
        raise ValueError(f"{n} not in 1–5")
    return n
```

`raise` throws an exception on purpose — caller decides how to handle it.

---

## EAFP vs LBYL

```python
# LBYL — "look before you leap"
if value.isdigit():
    n = int(value)

# EAFP — "easier to ask forgiveness" (Pythonic)
try:
    n = int(value)
except ValueError:
    n = None
```

Both valid. EAFP shines when "checking first" is hard or racy.

---

## assert (developer check, not validation)

```python
assert len(scores) > 0, "scores must not be empty"
```

For *your* sanity checks while developing. Can be disabled (`python -O`),
so **never** use `assert` to validate untrusted input — use `raise`.

---

## A first test with pytest

```python
# clean.py
def clean_likert(n):
    if not 1 <= n <= 5:
        raise ValueError("1–5 only")
    return n

# test_clean.py
import pytest
from clean import clean_likert

def test_valid():    assert clean_likert(3) == 3
def test_invalid():
    with pytest.raises(ValueError):
        clean_likert(9)
```
Run: `pytest`

---

## Your turn

`examples/session-07/practice.md`:
1. `safe_int(value)` returning int or None.
2. Clean a dirty survey list, collecting good values + a rejection log.
3. Write one `pytest` test.

---

## Traps recap

- **Never** bare `except:` — name the exception.
- Don't catch too broadly or swallow errors silently.
- `assert` ≠ input validation (use `raise`).
- Catch the *specific* error you expect.

## Summary
You can validate messy input and fail loudly when you should.
**Next:** read that messy data from real files.
