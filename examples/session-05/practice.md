# Session 5 — Practice: Functions, Scope & Reusability

Type each solution yourself. **Predict every output before you run it.** Solutions at the bottom.

## In class

### Task 1 — Grade-functions module
Write three functions with docstrings and type hints:
- `class_average(scores: list[float]) -> float`
- `letter_grade(score: float) -> str`  (reuse Session 3)
- `pass_rate(scores: list[float], passing: float = 60) -> float`  (fraction passing, 0–1)

Use bool-summing for `pass_rate` (recall `sum(s >= passing for s in scores)`).

### Task 2 — Reproduce & fix the mutable-default bug
Write `add_note(text, notes=[])` that appends and returns. Call it three times and watch
the list grow. Then fix it with the `None` pattern and prove each call starts fresh.

### Task 3 — *args summary
Write `summary(*scores)` that returns a dict `{"n":..., "mean":..., "max":..., "min":...}`.
Call it both as `summary(91, 58, 73)` and as `summary(*my_list)`.

### Bonus — Pythonic idiom drill
Cover the `# ->` answers, predict each line, then run.

```python
def f(a, *, b):          # everything after * is keyword-only
    return a, b
print(f(1, b=2))                     # -> (1, 2)
print(f(**{"a": 1, "b": 9}))         # -> (1, 9)   (** unpacks a dict into arguments)
```

## In class — going deeper (second hour)

### Task 1 — Keyword-only
Rewrite `letter_grade(score, plus_minus)` so that `plus_minus` **must** be passed by
keyword (`letter_grade(95, plus_minus=True)`); calling it positionally should raise
`TypeError`.

### Task 2 — Docstring polish
Give `pass_rate` a docstring that states what it returns, what `passing` means, and one
usage example. One short paragraph, no fluff.

### Task 3 — Your own `map`
Write `apply_to_all(func, values)` returning a new list with `func` applied to each value.
Test with `abs` and with a lambda that curves by +5.

### Task 4 — A function factory
Write `make_curver(bonus)` returning a function that adds `bonus`, capped at 100. Build a
`gentle = make_curver(5)` and a `strict = make_curver(1)` and show they differ.

### Task 5 — A first decorator
Write `@announce` that prints `calling <name> with <args>` before running the wrapped
function. Decorate your `letter_grade` and call it.

### Task 6 — A doctest
Add a docstring with two `>>>` examples to `class_average`, then run
`python -m doctest your_file.py -v` and watch them pass.

## Homework (before Session 6)

*~30–45 minutes, outside class — it doesn't count toward class time. Try everything before peeking at the solutions.*

### Task 1 — A tiny stats library
Three functions, each with a docstring and type hints:
- `validate_score(x) -> float` — accept int/float/numeric str in 0–100; `raise ValueError`
  otherwise (and reject `bool` — remember Session 2!),
- `curve(scores: list[float], bonus: float = 5) -> list[float]` — add the bonus, cap at
  100, and **don't mutate the input list**,
- `summarize(scores: list[float]) -> dict` — `n` / `mean` / `min` / `max`.

### Task 2 — `mean_ignoring_none(*values)`
`mean_ignoring_none(90, None, 80, None, 70)` → `80.0`. If nothing survives the cleaning,
return `None` rather than dividing by zero.

### Task 3 — Scope prediction
What does this print — and what breaks? Predict *before* running:
```python
count = 0

def tally(xs):
    total = 0
    for x in xs:
        total += x
    return total

def bump():
    count = count + 1   # ← think hard here

print(tally([1, 2, 3]))
bump()
```

---

## Solutions

### In class

```python
def class_average(scores: list[float]) -> float:
    """Mean of scores."""
    return sum(scores) / len(scores)

def letter_grade(score: float) -> str:
    """A/B/C/D/F by 90/80/70/60 cutoffs."""
    for cutoff, letter in [(90,"A"),(80,"B"),(70,"C"),(60,"D")]:
        if score >= cutoff:
            return letter
    return "F"

def pass_rate(scores: list[float], passing: float = 60) -> float:
    """Fraction of scores >= passing (0..1)."""
    return sum(s >= passing for s in scores) / len(scores)

# Task 2
def add_note(text, notes=None):     # fixed version
    if notes is None:
        notes = []
    notes.append(text)
    return notes

# Task 3
def summary(*scores):
    return {"n": len(scores), "mean": sum(scores)/len(scores),
            "max": max(scores), "min": min(scores)}
print(summary(91, 58, 73))
print(summary(*[91, 58, 73]))
```

### In class — going deeper

```python
# Task 1
def letter_grade(score, *, plus_minus=False):   # * makes what follows keyword-only
    ...
# letter_grade(95, True)            -> TypeError
# letter_grade(95, plus_minus=True) -> ok

# Task 2
def pass_rate(scores, passing=60):
    """Return the fraction (0..1) of scores at or above `passing`.

    `passing` is the cutoff, 60 by default: pass_rate([70, 50, 90]) -> 0.66...
    """
```

```python
# Task 3
def apply_to_all(func, values):
    return [func(v) for v in values]

print(apply_to_all(abs, [-3, 4, -5]))                 # [3, 4, 5]
print(apply_to_all(lambda s: min(s + 5, 100), [58, 97]))   # [63, 100]

# Task 4
def make_curver(bonus):
    def curve(score):
        return min(score + bonus, 100)
    return curve

gentle, strict = make_curver(5), make_curver(1)
print(gentle(96), strict(96))    # 100 97

# Task 5
def announce(f):
    def wrapper(*args, **kwargs):
        print(f"calling {f.__name__} with {args}")
        return f(*args, **kwargs)
    return wrapper

@announce
def letter_grade(score):
    for cutoff, letter in [(90, "A"), (80, "B"), (70, "C"), (60, "D")]:
        if score >= cutoff:
            return letter
    return "F"

print(letter_grade(85))          # calling letter_grade with (85,)  ->  B

# Task 6
def class_average(scores):
    """Mean of scores.

    >>> class_average([90, 80, 70])
    80.0
    >>> class_average([100])
    100.0
    """
    return sum(scores) / len(scores)
# python -m doctest your_file.py -v  ->  2 passed.
```

### Homework

```python
# Task 1
def validate_score(x) -> float:
    """Return x as a float score in 0-100, or raise ValueError."""
    if isinstance(x, bool):                  # bool would sneak through float()!
        raise ValueError("bool is a flag, not a score")
    score = float(x)                         # ValueError for bad strings
    if not 0 <= score <= 100:
        raise ValueError(f"{score} outside 0-100")
    return score

def curve(scores: list[float], bonus: float = 5) -> list[float]:
    """Return a NEW list with `bonus` added to each score, capped at 100."""
    return [min(s + bonus, 100) for s in scores]

def summarize(scores: list[float]) -> dict:
    """n, mean, min, max of `scores`."""
    return {"n": len(scores), "mean": sum(scores) / len(scores),
            "min": min(scores), "max": max(scores)}

# Task 2
def mean_ignoring_none(*values):
    clean = [v for v in values if v is not None]
    return sum(clean) / len(clean) if clean else None

print(mean_ignoring_none(90, None, 80, None, 70))   # 80.0
print(mean_ignoring_none(None, None))               # None

# Task 3
# tally([1, 2, 3]) prints 6 — `total` is local to tally, no conflict with anything.
# bump() raises UnboundLocalError: the assignment makes `count` local to bump,
# so `count + 1` reads a local variable that doesn't exist yet.
# The fix is not `global` — return the new value and reassign at the call site.
```
