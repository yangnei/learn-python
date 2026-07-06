---
marp: true
title: "Session 6 — Recursion & Recursive Thinking"
paginate: true
---

# Session 6
## Recursion & Recursive Thinking

---

## The shape of every recursion

Real example: how many prerequisites deep is a course?

```python
prereq_of = {"ED700": "ED600", "ED600": "ED500",
             "ED500": "ED400", "ED400": None}   # ED400 has none

def prereqs_deep(course):
    earlier = prereq_of[course]
    if earlier is None:               # BASE CASE — stop here
        return 0
    return 1 + prereqs_deep(earlier)  # RECURSIVE CASE — step back one
```

Two parts, always:
- a **base case** that stops, and
- a **recursive case** that moves *toward* the base case.

---

## Trace the call stack

`orderings(n)` = ways to rank *n* students = n!

```python
orderings(3)
= 3 * orderings(2)
=     3 * (2 * orderings(1))
=         3 * (2 * 1)          # base case returns 1
= 6
```

Each call waits on the one inside it. The calls stack up, then unwind.

🧠 Each pending call is a **stack frame** — that matters in a moment.

---

## Recursion vs iteration

```python
def orderings(n):                 # ways to rank n students (n!)
    if n <= 1:
        return 1
    return n * orderings(n - 1)   # ← must RETURN the call

def orderings_loop(n):
    total = 1
    for k in range(2, n + 1):
        total *= k
    return total
```

Same answer. For flat counting, the **loop** is usually clearer.

---

## Where recursion shines: nested data

```python
def deep_sum(obj):
    if isinstance(obj, (int, float)):
        return obj
    if isinstance(obj, dict):
        return sum(deep_sum(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return sum(deep_sum(x) for x in obj)
    return 0

deep_sum([1, [2, [3, 4]], {"a": 6}])   # 16
```

Nested JSON, folder trees, threaded replies — a single loop can't reach all the way down. Recursion can.

---

## The trap: no base case

```python
def runaway(n):
    return runaway(n + 1)     # never stops
```

```
RecursionError: maximum recursion depth exceeded
```

Python has **no tail-call optimization** — every call keeps its frame
(default limit ≈ 1000). Deep recursion *will* hit the ceiling.

---

## Your turn

`examples/session-06/practice.md`:
1. Recursive `total(scores)` — sum a list of scores; name the base case first.
2. `flatten([1, [2, [3, 4]], 5])` → one flat list.
3. `depth(...)` — how deeply is a list nested?

---

# Going deeper
## Recursion in the wild

---

## Memoization: remember past calls

```python
def fib(n):                       # naive: fib(35) recomputes fib(5) thousands of times
    return n if n < 2 else fib(n - 1) + fib(n - 2)

import functools
@functools.cache                  # remembers every (input -> output) it has seen
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

Naive `fib(35)`: seconds. Cached: instant. Same code — a decorator (Session 5!) did the work.
When a recursion re-solves the **same subproblem**, cache it.

---

## Divide & conquer: binary search

```python
def find(sorted_names, target, lo=0, hi=None):
    if hi is None:
        hi = len(sorted_names)
    if lo >= hi:
        return False                   # base case: empty range
    mid = (lo + hi) // 2
    if sorted_names[mid] == target:
        return True
    if sorted_names[mid] < target:
        return find(sorted_names, target, mid + 1, hi)
    return find(sorted_names, target, lo, mid)
```

Each call **halves** the problem: 1 000 names ≈ 10 steps, a million ≈ 20.
(Requires sorted data — Session 4's `sorted` earns its keep.)

---

## Tree-shaped data

```python
org = {"name": "Dean",
       "reports": [{"name": "Chair A", "reports": []},
                   {"name": "Chair B",
                    "reports": [{"name": "Prof C", "reports": []}]}]}

def count_people(node):
    return 1 + sum(count_people(r) for r in node["reports"])

count_people(org)      # 4
```

Org charts, folder trees, threaded replies, nested codes — the function's shape **mirrors the
data's shape**. That's the whole trick.

---

## Escaping the limit: an explicit stack

```python
def flatten_iter(xs):
    out, to_visit = [], list(xs)
    while to_visit:
        x = to_visit.pop(0)
        if isinstance(x, list):
            to_visit = x + to_visit    # open the box in place
        else:
            out.append(x)
    return out
```

Same logic, **no call-stack frames** — depth 10 000 is fine. When data may nest deeper than
~1000, carry your own to-visit list.

---

## Choosing: loop, recursion, or cache?

| Situation | Reach for |
|---|---|
| flat sequence | a plain **loop** |
| self-similar / nested data | **recursion** |
| repeated subproblems | recursion + **`@cache`** |
| possibly very deep | loop + **explicit stack** |

Recursion is a tool, not a virtue — pick by the *shape of the data*.

---

## Your turn — round 2

`examples/session-06/practice.md` → **In class — going deeper**:
binary search with a step counter, an org-tree count, and `flatten` without recursion.
---

## Traps recap

- Every recursion needs a **reachable base case**, or it overflows the stack.
- **Return** the recursive call — forgetting to gives you a silent `None`.
- Recursion isn't free: each call costs a stack frame (no tail-call optimization).
- A plain **loop** is better for flat sequences and for very deep work.

## Summary
You can solve problems that are defined in terms of themselves — especially nested data.
**Next:** Session 7 — exceptions & defensive code.

---

## Homework (before Session 7)

*Outside class — it doesn't count toward class time. Full specs + solutions: `examples/session-06/practice.md` → **Homework**.*

1. **`sum_digits(n)`** — recursion on a number instead of a list.
2. **`deep_count(obj)`** — count every score in a nested gradebook dict.
3. **In your own words** — one paragraph: when is a loop the better tool?
