# Session 3 — Practice: Functions & Recursion

This 2-hour session has two halves. Do **Part A** after the first topic, **Part B** after the second. Predict every output before you run it.

## Part A — Functions, Scope & Reusability

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

## Part B — Recursion & Recursive Thinking

### Task 1 — Recursive total
Write `total(scores)` that sums a list of scores **with recursion** (no loop):
`scores[0] + total(rest)`, with the empty list as the base case. Name the base
case out loud first. Test `total([91, 58, 73])` and `total([])`.

### Task 2 — Recursion vs iteration
Write `reverse(s)` that reverses a string recursively. Then write the loop version.
Which reads more clearly to you? Test `reverse("data")`.

### Task 3 — Flatten nested data
Write `flatten(xs)` that turns a list-of-lists (nested to any depth) into one flat list:
`flatten([1, [2, [3, 4]], 5])` → `[1, 2, 3, 4, 5]`. This is the move for nested JSON/exports.

### Task 4 — How deep does it go?
Write `depth(xs)` returning how deeply a list is nested:
`depth([1, [2, [3, [4]]]])` → `4`, `depth([1, 2, 3])` → `1`, `depth(5)` → `0`.

### Task 5 — Trap check
1. Why does this raise `RecursionError`, and what's the fix?
   ```python
   def f(n):
       return n + f(n - 1)
   ```
2. This returns `None` instead of a number — why?
   ```python
   def orderings(n):
       if n <= 1:
           return 1
       n * orderings(n - 1)
   ```
3. Name one case where a plain loop is the better choice over recursion.

### Bonus — Pythonic idiom drill
One decorator makes exponential recursion instant by remembering past calls.

```python
import functools

@functools.cache                     # memoize: each n is computed once
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
print(fib(35))                       # -> 9227465   (try this WITHOUT @cache... then wait)
```

---

## Solutions

### Part A — Functions, Scope & Reusability

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

### Part B — Recursion & Recursive Thinking

```python
# 1
def total(scores):
    if not scores:                  # base case: empty list sums to 0
        return 0
    return scores[0] + total(scores[1:])   # first score + total of the rest
print(total([91, 58, 73]), total([]))      # 222 0

# 2
def reverse(s):
    if s == "":                     # base case: empty string
        return ""
    return reverse(s[1:]) + s[0]    # all-but-first, reversed, then first
print(reverse("data"))             # "atad"
# loop version: "".join(reversed(s))  — usually clearer for flat strings

# 3
def flatten(xs):
    out = []
    for x in xs:
        if isinstance(x, list):
            out.extend(flatten(x))  # recurse into the sub-list
        else:
            out.append(x)
    return out
print(flatten([1, [2, [3, 4]], 5]))   # [1, 2, 3, 4, 5]

# 4
def depth(xs):
    if not isinstance(xs, list):
        return 0                              # a non-list has no nesting
    return 1 + max((depth(x) for x in xs), default=0)
print(depth([1, [2, [3, [4]]]]), depth([1, 2, 3]), depth(5))   # 4 1 0

# 5
# 1) No reachable base case -> the calls never stop -> stack overflows.
#    Fix: add `if n == 0: return 0` (or n <= 0) at the top.
# 2) The recursive case computes n*fact(n-1) but never RETURNs it,
#    so the function falls off the end and returns None. Add `return`.
# 3) A loop is better when the work is a simple flat sequence, or when the
#    depth could exceed ~1000 (Python has no tail-call optimization, so deep
#    recursion hits RecursionError where a loop would be fine).
```
