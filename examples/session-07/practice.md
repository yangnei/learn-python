# Session 7 — Practice: Exceptions & Defensive Code

Type each solution yourself. **Predict every output before you run it.** Solutions at the bottom.

## In class

### Task 1 — `safe_int`
Write `safe_int(value)` returning `int(value)` or `None` on failure. Test on
`"42"`, `"N/A"`, `""`, `None`, `3.0`.

### Task 2 — Clean a survey column
Given `raw = ["5","3","N/A","7","","1","two","4"]`, produce:
- `clean` — list of valid Likert ints (1–5), and
- `rejected` — list of `(value, reason)` pairs.
Use a `clean_likert(n)` that **raises** `ValueError` for out-of-range or non-ints.

### Task 3 — Write a test
Put `clean_likert` in `clean.py` and write `test_clean.py` with pytest:
one passing case and one `pytest.raises(ValueError)` case. Run `pytest`.

### Task 4 — Discuss
Why is `except:` (bare) dangerous? Give one error it would hide that you'd rather see.

### Bonus — Pythonic idiom drill
Cover the `# ->` answers, predict each line, then run.

```python
class LikertError(ValueError):       # your own exception type
    pass
print(issubclass(LikertError, ValueError))   # -> True  (so `except ValueError` still catches it)

try:
    assert 1 == 2, "values differ"   # assert: cheap internal sanity check
except AssertionError as e:
    print(e)                         # -> values differ
```

## In class — going deeper (second hour)

### E1 — Which exception?
Without running, name the exception each raises:
`int("3.5")` · `{"a": 1}["b"]` · `[1, 2][5]` · `1/0` · `open("nope.csv")` · `len(42)`

### E2 — Your own exception
Define `class SurveyError(ValueError)` and raise it for out-of-range Likert values. Show
that `except ValueError:` still catches it — that's subclassing at work.

### D1 — Fix the except order
This always prints `"unexpected"` for bad cells — why, and what's the fix?
```python
try:
    n = int(cell)
except Exception:
    print("unexpected")
except ValueError:
    n = None
```

### D2 — `SurveyError` with evidence
Build `class SurveyError(ValueError)` that stores the offending value as `.value`. In your
cleaning loop, catch the low-level `ValueError` from `int()` and re-raise as
`SurveyError(cell, ...) from e`. Show the two-level traceback once.

### D3 — Log, don't print
Convert your rejection log to `logging`: `logging.warning` per rejected cell,
`logging.info` with the final counts. Configure the format to show the level name.

### D4 — Parametrize
Rewrite your three homework tests as ONE `@pytest.mark.parametrize` test over
`["3", True, None, 0, 9]`. Run `pytest -q`.

## Homework (before Session 8)

*~30–45 minutes, outside class — it doesn't count toward class time. Try everything before peeking at the solutions.*

### H1 — `ask_int(prompt, lo, hi)`
Session 3's validation loop, rebuilt the EAFP way: `try: n = int(raw)` /
`except ValueError` instead of `.isdigit()` — so `"-5"` and `" 42 "` work too. Loop until
valid; return the int.

### H2 — Three more pytest cases
For `clean_likert`, add tests that: `clean_likert(True)` raises (a bool is not a rating!),
`clean_likert("3")` raises (a str, even if numeric), `clean_likert(None)` raises.
Run `pytest -q` until green.

### H3 — Error triage
For each message, name the exception class and give the one-line fix:
1. `invalid literal for int() with base 10: 'N/A'`
2. `unsupported operand type(s) for +: 'int' and 'str'`
3. `'score'` (raised by a dict lookup)
4. `division by zero`
5. `[Errno 2] No such file or directory: 'survy.csv'`

---

## Solutions

### In class

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

### In class — going deeper

```python
# E1
int("3.5")        # ValueError          (int() parses integer text only)
{"a": 1}["b"]     # KeyError
[1, 2][5]         # IndexError
1 / 0             # ZeroDivisionError
open("nope.csv")  # FileNotFoundError
len(42)           # TypeError           (ints have no length)

# E2
class SurveyError(ValueError):
    pass

def clean_likert(n):
    if not 1 <= n <= 5:
        raise SurveyError(f"{n} outside 1-5")
    return n

try:
    clean_likert(9)
except ValueError as e:      # the parent class catches the subclass
    print("caught:", e)
```

```python
# D1 — except clauses are tried top-down; `Exception` is the parent of ValueError,
# so it matches FIRST and the specific handler is unreachable. Specific before broad:
try:
    n = int(cell)
except ValueError:
    n = None
except Exception as e:
    print("unexpected:", e)
    raise

# D2
class SurveyError(ValueError):
    def __init__(self, value, message):
        super().__init__(message)
        self.value = value

def clean_cell(cell):
    try:
        n = int(cell)
    except ValueError as e:
        raise SurveyError(cell, f"{cell!r} is not a rating") from e
    return n
# The traceback shows the ValueError as the cause, the SurveyError on top.

# D3
import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
kept, rejected = [], []
for cell in ["5", "N/A", "3", ""]:
    try:
        kept.append(clean_cell(cell))
    except SurveyError as e:
        rejected.append(e.value)
        logging.warning("rejected %r", e.value)
logging.info("kept %d, rejected %d", len(kept), len(rejected))

# D4 — test_clean.py
import pytest
from clean import clean_likert

@pytest.mark.parametrize("bad", ["3", True, None, 0, 9])
def test_rejects(bad):
    with pytest.raises(ValueError):
        clean_likert(bad)
```

### Homework

```python
# H1
def ask_int(prompt, lo, hi):
    while True:
        raw = input(prompt)
        try:
            n = int(raw)                 # EAFP: just try the conversion
        except ValueError:
            print("A whole number, please.")
            continue
        if lo <= n <= hi:
            return n
        print(f"Between {lo} and {hi}, please.")

# H2 — test_clean.py
import pytest
from clean import clean_likert

def test_bool_rejected():
    with pytest.raises(ValueError):
        clean_likert(True)

def test_str_rejected():
    with pytest.raises(ValueError):
        clean_likert("3")

def test_none_rejected():
    with pytest.raises(ValueError):
        clean_likert(None)
```

H3 — triage:
1. `ValueError` — clean/convert first, or wrap in `try/except ValueError`.
2. `TypeError` — convert one side: `str(n)` or `int(s)`.
3. `KeyError` — `row.get("score")`, or fix the header spelling.
4. `ZeroDivisionError` — guard the empty case before dividing.
5. `FileNotFoundError` — the filename is misspelled (`survey.csv`); check with `Path(...).exists()`.
