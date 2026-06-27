---
marp: true
title: "Session 6 — Recursion & Recursive Thinking"
paginate: true
---

# Session 6
## Recursion & Recursive Thinking

A function that solves a problem by calling **itself** on a smaller piece.

---

## The shape of every recursion

```python
def countdown(n):
    if n <= 0:          # BASE CASE — when to stop
        print("liftoff!")
        return
    print(n)
    countdown(n - 1)    # RECURSIVE CASE — same problem, smaller input
```

Two parts, always:
- a **base case** that stops, and
- a **recursive case** that moves *toward* the base case.

---

## Trace the call stack

```python
factorial(3)
= 3 * factorial(2)
=     3 * (2 * factorial(1))
=         3 * (2 * 1)        # base case returns 1
= 6
```

Each call waits on the one inside it. The calls stack up, then unwind.

🧠 Each pending call is a **stack frame** — that matters in a moment.

---

## Recursion vs iteration

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)   # ← must RETURN the call

def factorial_loop(n):
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
1. Recursive `rsum(n)` — name the base case first.
2. `flatten([1, [2, [3, 4]], 5])` → one flat list.
3. `depth(...)` — how deeply is a list nested?

---

## Traps recap

- Every recursion needs a **reachable base case**, or it overflows the stack.
- **Return** the recursive call — forgetting to gives you a silent `None`.
- Recursion isn't free: each call costs a stack frame (no tail-call optimization).
- A plain **loop** is better for flat sequences and for very deep work.

## Summary
You can solve problems that are defined in terms of themselves — especially nested data.
**Next:** make your code survive messy real-world input — exceptions.
