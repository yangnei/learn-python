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

## Extra practice (in class, if you're ahead)

### E1 — Keyword-only
Rewrite `letter_grade(score, plus_minus)` so that `plus_minus` **must** be passed by
keyword (`letter_grade(95, plus_minus=True)`); calling it positionally should raise
`TypeError`.

### E2 — Docstring polish
Give `pass_rate` a docstring that states what it returns, what `passing` means, and one
usage example. One short paragraph, no fluff.

## Homework (before Session 6)

*~30–45 minutes, outside class — it doesn't count toward the hour. Try everything before peeking at the solutions.*

### H1 — A tiny stats library
Three functions, each with a docstring and type hints:
- `validate_score(x) -> float` — accept int/float/numeric str in 0–100; `raise ValueError`
  otherwise (and reject `bool` — remember Session 2!),
- `curve(scores: list[float], bonus: float = 5) -> list[float]` — add the bonus, cap at
  100, and **don't mutate the input list**,
- `summarize(scores: list[float]) -> dict` — `n` / `mean` / `min` / `max`.

### H2 — `mean_ignoring_none(*values)`
`mean_ignoring_none(90, None, 80, None, 70)` → `80.0`. If nothing survives the cleaning,
return `None` rather than dividing by zero.

### H3 — Scope prediction
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

### Extra practice

```python
# E1
def letter_grade(score, *, plus_minus=False):   # * makes what follows keyword-only
    ...
# letter_grade(95, True)            -> TypeError
# letter_grade(95, plus_minus=True) -> ok

# E2
def pass_rate(scores, passing=60):
    """Return the fraction (0..1) of scores at or above `passing`.

    `passing` is the cutoff, 60 by default: pass_rate([70, 50, 90]) -> 0.66...
    """
```

### Homework

```python
# H1
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

# H2
def mean_ignoring_none(*values):
    clean = [v for v in values if v is not None]
    return sum(clean) / len(clean) if clean else None

print(mean_ignoring_none(90, None, 80, None, 70))   # 80.0
print(mean_ignoring_none(None, None))               # None

# H3
# tally([1, 2, 3]) prints 6 — `total` is local to tally, no conflict with anything.
# bump() raises UnboundLocalError: the assignment makes `count` local to bump,
# so `count + 1` reads a local variable that doesn't exist yet.
# The fix is not `global` — return the new value and reassign at the call site.
```
