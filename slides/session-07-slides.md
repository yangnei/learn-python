---
marp: true
title: "Session 7 — Exceptions & Defensive Code"
paginate: true
---

# Session 7
## Exceptions & Defensive Code

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

# Going deeper
## Robust programs

---

## The exception family tree

```text
Exception
 ├── ValueError        ├── KeyError / IndexError (LookupError)
 ├── TypeError         └── OSError (FileNotFoundError, ...)
```

```python
try:
    n = int(raw)
except (ValueError, TypeError):   # catch a tuple of specifics
    ...
```

**Order matters**: `except` clauses are tried top-down — specific before broad, and a final
`except Exception as e:` only to log-and-stop, never to ignore.

---

## Custom exceptions that carry data

```python
class SurveyError(ValueError):
    def __init__(self, value, message):
        super().__init__(message)
        self.value = value            # keep the evidence

raise SurveyError(raw, f"{raw!r} is not a 1-5 rating")
```

Callers can catch `SurveyError` specifically — or `ValueError` broadly — and still see
*which* value broke.

---

## `raise ... from` — keep the cause

```python
try:
    n = int(cell)
except ValueError as e:
    raise SurveyError(cell, "bad rating cell") from e
```

The traceback shows **both**: your domain-level error on top, the real low-level cause
beneath. Future-you debugging at midnight says thanks.

---

## `finally` and the cleanup mindset

```python
try:
    f = open("data.csv")
    ...
finally:
    f.close()        # runs no matter what happened above
```

`with open(...)` (Session 8) is exactly this pattern, packaged. Rule: whoever acquires a
resource guarantees its release.

---

## `logging` beats `print` for diagnostics

```python
import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logging.info("processing %s rows", len(rows))
logging.warning("rejected %r: out of range", raw)
```

- `print` is for the program's *output*; `logging` is for its *diary*.
- Levels (`DEBUG/INFO/WARNING/ERROR`) let you silence chatter without deleting lines.

---

## pytest, round 2

```python
import pytest
from clean import clean_likert

@pytest.mark.parametrize("bad", ["3", True, None, 0, 9])
def test_rejects(bad):
    with pytest.raises(ValueError):
        clean_likert(bad)
```

One test, five inputs, five reported results. Pattern: **arrange, act, assert** — and test the
*edges* (boundaries, wrong types), not the happy middle.

---

## Your turn — round 2

`examples/session-07/practice.md` → **In class — going deeper**:
fix an except-order bug, build `SurveyError` with `raise ... from`, switch the rejection log
to `logging`, and parametrize your tests.
---

## Traps recap

- **Never** bare `except:` — name the exception.
- Don't catch too broadly or swallow errors silently.
- `assert` ≠ input validation (use `raise`).
- Catch the *specific* error you expect.

## Summary
You can validate messy input and fail loudly when you should.
**Next:** Session 8 — files & research data.

---

## Homework (before Session 8)

*Outside class — it doesn't count toward class time. Full specs + solutions: `examples/session-07/practice.md` → **Homework**.*

1. **`ask_int(prompt, lo, hi)`** — Session 3's validation loop rebuilt the EAFP way.
2. **Three more pytest cases** — edge cases for `clean_likert` (`True`, `"3"`, `None`).
3. **Error triage** — five real error messages: name the exception and the fix.
