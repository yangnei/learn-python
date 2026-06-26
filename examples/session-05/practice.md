# Session 5 — Practice (25 min)

## Task 1 — Grade-functions module
Write three functions with docstrings and type hints:
- `class_average(scores: list[float]) -> float`
- `letter_grade(score: float) -> str`  (reuse Session 3)
- `pass_rate(scores: list[float], passing: float = 60) -> float`  (fraction passing, 0–1)

Use bool-summing for `pass_rate` (recall `sum(s >= passing for s in scores)`).

## Task 2 — Reproduce & fix the mutable-default bug
Write `add_note(text, notes=[])` that appends and returns. Call it three times and watch
the list grow. Then fix it with the `None` pattern and prove each call starts fresh.

## Task 3 — *args summary
Write `summary(*scores)` that returns a dict `{"n":..., "mean":..., "max":..., "min":...}`.
Call it both as `summary(91, 58, 73)` and as `summary(*my_list)`.

---
## Solutions

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
