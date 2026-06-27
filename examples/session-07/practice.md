# Session 7 — Practice (25 min)

## Task 1 — `safe_int`
Write `safe_int(value)` returning `int(value)` or `None` on failure. Test on
`"42"`, `"N/A"`, `""`, `None`, `3.0`.

## Task 2 — Clean a survey column
Given `raw = ["5","3","N/A","7","","1","two","4"]`, produce:
- `clean` — list of valid Likert ints (1–5), and
- `rejected` — list of `(value, reason)` pairs.
Use a `clean_likert(n)` that **raises** `ValueError` for out-of-range or non-ints.

## Task 3 — Write a test
Put `clean_likert` in `clean.py` and write `test_clean.py` with pytest:
one passing case and one `pytest.raises(ValueError)` case. Run `pytest`.

## Task 4 — Discuss
Why is `except:` (bare) dangerous? Give one error it would hide that you'd rather see.

---
## Solutions

```python
def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def clean_likert(n):
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError(f"{n!r} not an int")
    if not 1 <= n <= 5:
        raise ValueError(f"{n} outside 1–5")
    return n

raw = ["5","3","N/A","7","","1","two","4"]
clean, rejected = [], []
for r in raw:
    try:
        clean.append(clean_likert(safe_int(r)))
    except ValueError as e:
        rejected.append((r, str(e)))
print(clean)      # [5, 3, 1, 4]
print(rejected)   # [('N/A', ...), ('7', ...), ('', ...), ('two', ...)]
```

```python
# test_clean.py
import pytest
from clean import clean_likert
def test_ok():   assert clean_likert(3) == 3
def test_bad():
    with pytest.raises(ValueError):
        clean_likert(9)
```

Task 4: a bare `except:` also catches `KeyboardInterrupt` (Ctrl+C) and `NameError`
from your own typos — so a misspelled variable would be silently swallowed instead of
showing you the bug. Always catch the specific exception you expect.
