# Session 6 — Practice (60 min): Recursion & Recursive Thinking

## Task 1 — Recursive sum
Write `rsum(n)` that adds `1 + 2 + ... + n` **with recursion** (no loop).
Name the base case out loud before you write it. Test `rsum(5)` and `rsum(0)`.

## Task 2 — Recursion vs iteration
Write `reverse(s)` that reverses a string recursively. Then write the loop version.
Which reads more clearly to you? Test `reverse("data")`.

## Task 3 — Flatten nested data
Write `flatten(xs)` that turns a list-of-lists (nested to any depth) into one flat list:
`flatten([1, [2, [3, 4]], 5])` → `[1, 2, 3, 4, 5]`. This is the move for nested JSON/exports.

## Task 4 — How deep does it go?
Write `depth(xs)` returning how deeply a list is nested:
`depth([1, [2, [3, [4]]]])` → `4`, `depth([1, 2, 3])` → `1`, `depth(5)` → `0`.

## Task 5 — Trap check
1. Why does this raise `RecursionError`, and what's the fix?
   ```python
   def f(n):
       return n + f(n - 1)
   ```
2. This returns `None` instead of a number — why?
   ```python
   def fact(n):
       if n <= 1:
           return 1
       n * fact(n - 1)
   ```
3. Name one case where a plain loop is the better choice over recursion.

## Bonus — Pythonic idiom drill
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

```python
# 1
def rsum(n):
    if n == 0:                      # base case
        return 0
    return n + rsum(n - 1)
print(rsum(5), rsum(0))             # 15 0

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
