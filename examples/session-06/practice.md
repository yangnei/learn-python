# Session 6 — Practice: Recursion & Recursive Thinking

Type each solution yourself. **Predict every output before you run it.** Solutions at the bottom.

## In class

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

## Extra practice (in class, if you're ahead)

### E1 — Recursive countdown
`countdown(3)` prints `3 2 1 Go!`. Say the base case out loud before you type.

### E2 — Trace on paper
Write the full expansion of `total([5, 10, 20])` (Task 1) the way the slides traced
`orderings(3)` — every pending call, then the unwind.

## Homework (before Session 7)

*~30–45 minutes, outside class — it doesn't count toward the hour. Try everything before peeking at the solutions.*

### H1 — `sum_digits(n)`
`sum_digits(4823)` → `17`, recursively. (Hint: `n % 10` is the last digit, `n // 10` is
the rest. What's the smallest number whose digit-sum is obvious?)

### H2 — `deep_count(obj)`
Count how many **numbers** (int/float — but not bool!) appear anywhere in a nested
structure. Handle dicts, lists/tuples, and scalars.
`deep_count({"quiz": [90, 85], "final": {"written": 88, "oral": 92}, "note": "great"})` → `4`.

### H3 — In your own words
One paragraph: for which shapes of problem is a plain loop the better tool, and what
*specifically* goes wrong with deep recursion around depth ~1000? (Name the error.)

---

## Solutions

### In class

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

### Extra practice

```python
# E1
def countdown(n):
    if n == 0:            # base case
        print("Go!")
        return
    print(n)
    countdown(n - 1)      # recursive case, moving toward 0

# E2 — the trace
# total([5, 10, 20])
# = 5 + total([10, 20])
# =     10 + total([20])
# =          20 + total([])
# =               0            <- base case
# unwind: 20 + 0 = 20 ; 10 + 20 = 30 ; 5 + 30 = 35
```

### Homework

```python
# H1
def sum_digits(n):
    if n < 10:                       # single digit: the sum is itself
        return n
    return n % 10 + sum_digits(n // 10)

print(sum_digits(4823))              # 17

# H2
def deep_count(obj):
    if isinstance(obj, bool):        # bool ⊂ int — a flag isn't a number (Session 2!)
        return 0
    if isinstance(obj, (int, float)):
        return 1
    if isinstance(obj, dict):
        return sum(deep_count(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return sum(deep_count(x) for x in obj)
    return 0

print(deep_count({"quiz": [90, 85], "final": {"written": 88, "oral": 92},
                  "note": "great"}))   # 4
```

H3 — model answer: flat sequences (summing a list, walking rows) read best as loops.
Every pending recursive call keeps a stack frame, and Python has no tail-call
optimization, so around ~1000 frames it raises `RecursionError` — where a loop would
simply keep going. Recursion earns its keep when the *data itself* is nested/self-similar.
