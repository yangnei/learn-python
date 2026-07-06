---
marp: true
title: "Session 3 — Control Flow: Conditionals & Loops"
paginate: true
---

# Session 3
## Control Flow: Conditionals & Loops

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

## `if` vs `elif` — not interchangeable

```python
# BUG: three separate ifs — a 95 prints ALL THREE labels
if score >= 60: print("passing")
if score >= 80: print("strong")
if score >= 90: print("excellent")
```

- Stacked `if`s are **independent questions** — overlapping conditions all fire.
- `elif` makes them **one question with branches**: first hit wins, the rest are skipped.
- Stack `if`s only when several can *legitimately* be true at once.

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
5 and 0        # ?  ← predict, then reveal in Traps below
"" or "N/A"    # the default-value idiom
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
4. The double-label bug — three stacked `if`s that should be one ladder.

---

# Going deeper
## More control flow

---

## The ternary — a tiny `if` in one line

```python
label = "pass" if score >= 60 else "fail"
print(f"{name}: {'✔' if attended else '✘'}")
```

For **tiny** choices only. If it needs two reads, use a real `if`.

---

## Return the test itself

```python
def is_passing(score):        # clunky
    if score >= 60:
        return True
    return False

def is_passing(score):        # Pythonic — the comparison already IS a bool
    return score >= 60
```

Then use it bare: `if is_passing(s):` — never `if is_passing(s) == True:`.
🧠 Same for any yes/no helper: `is_valid`, `is_missing`, `is_full` — one `return` line each.

---

## `match/case` — the readable ladder (3.10+)

```python
match answer:
    case 5 | 4:
        label = "agree"
    case 3:
        label = "neutral"
    case 1 | 2:
        label = "disagree"
    case _:                 # the default
        label = "invalid"
```

When every branch compares the **same value** against literals, `match` beats an `elif` ladder.

---

## `for/else` — search without a flag

```python
for s in scores:
    if s < 60:
        print("first failing score:", s)
        break
else:                      # runs only if the loop did NOT break
    print("everyone passed")
```

The `else` belongs to the `for`. No `found = False` bookkeeping needed.

---

## Nested loops

```python
for section in ["A", "B"]:
    for student in roster:
        print(section, student)
```

- Every inner pass runs per outer pass (2 × 4 = 8 lines).
- `break` exits the **inner** loop only — to escape both, put the loops in a function and `return`.

---

## Name the pattern you're writing

| Pattern | Skeleton |
|---|---|
| **accumulator** | `total = 0` … `total += x` |
| **counter** | `n = 0` … `n += 1` |
| **best-so-far** | `best = xs[0]` … `if x > best: best = x` |
| **sentinel** | `while True:` … `if raw == "done": break` |

Recognizing these turns "staring at a blank editor" into "picking a skeleton".

---

## Your turn — round 2

`examples/session-03/practice.md` → **In class — going deeper**:
a `match/case` rewrite, a `for/else` search, best-so-far without `max()`, and the
return-the-test rewrite.
---

## Traps recap

- `if x == True` → just `if x:`; use `x is None` (not `== None`).
- Stacked `if`s are independent questions — they ALL fire; `elif` makes one ladder.
- `=` (assign) vs `==` (compare) — classic typo.
- `range(1, 5)` excludes 5; test your boundaries.
- Don't modify a list while looping it; prefer `enumerate`/`zip` over `range(len(...))`.

*(More in the cheat sheet: `match`/`case`, the ternary, `for/else`.)*

## Summary
You can branch and repeat cleanly.
**Next:** Session 4 — data structures.

---

## Homework (before Session 4)

*Outside class — it doesn't count toward class time. Full specs + solutions: `examples/session-03/practice.md` → **Homework**.*

1. **Attendance labeler** — chained comparisons + `elif` ladder on a list of percentages.
2. **Number-guessing game** — a `while` loop with input validation and attempt counting.
3. **Leap-year checker** — one boolean expression, tested on the tricky years.
