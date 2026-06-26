---
marp: true
title: "Session 3 — Control Flow: Conditionals & Loops"
paginate: true
---

# Session 3
## Control Flow: Conditionals & Loops

Make decisions, and repeat work — the two halves of control flow.

---

## Part 1 — Conditionals

```python
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "F"
```

Indentation defines the block. Only the **first** true branch runs.

---

## Comparison + chained comparisons

`==`  `!=`  `<`  `<=`  `>`  `>=`

```python
0 <= score <= 100      # chained — reads like math
```

🧠 No need for `score >= 0 and score <= 100` — chain it.

---

## Logical operators (and the gotcha)

```python
passed and submitted     # both
late or excused          # either
not flagged              # negate
```

**Short-circuit:** `a and b` skips `b` if `a` is falsy.
And `and`/`or` return an **operand, not a bool**:

```python
5 and 0        # 0
"" or "N/A"    # "N/A"   ← default-value idiom
```

So write `if x:` — never `if x == True`.

---

## Part 2 — Loops

```python
for s in scores:          # each element directly
    print(s)

for i in range(5):        # 0,1,2,3,4
    print(i)

while not done:           # repeat until a condition flips
    ...
```

⚠️ `range(1, 5)` → `1,2,3,4` — **stop is excluded** (off-by-one!).

---

## break / continue

```python
for x in data:
    if x is None:
        continue          # skip this one
    if x == "STOP":
        break             # leave the loop entirely
    process(x)
```

---

## Stop juggling indices: enumerate & zip

```python
for i, name in enumerate(names):       # index + value
    print(i, name)

for name, score in zip(names, scores): # two lists together
    print(name, score)
```

🧠 If you write `range(len(x))`, stop — use `enumerate`/`zip`.

---

## The validation loop (you'll reuse this everywhere)

```python
while True:
    raw = input("Score 0–100: ")
    if raw.isdigit() and 0 <= int(raw) <= 100:
        score = int(raw)
        break
    print("Try again.")
```

---

## Your turn

`examples/session-03/practice.md`:
1. Grade-band classifier — test the boundaries (89.999 / 90 / 90.001).
2. Average a roster and label each student PASS/FAIL with `zip`.
3. A robust "ask until valid" loop.

---

## Traps recap

- `if x == True` → just `if x:`; use `x is None` (not `== None`).
- `=` (assign) vs `==` (compare) — classic typo.
- `range(1, 5)` excludes 5; test your boundaries.
- Don't modify a list while looping it; prefer `enumerate`/`zip` over `range(len(...))`.

*(More in the cheat sheet: `match`/`case`, the ternary, `for/else`.)*

## Summary
You can branch and repeat cleanly.
**Next:** the containers you loop over — lists, dicts, sets.
