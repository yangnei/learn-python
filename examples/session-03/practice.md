# Session 3 — Practice: Control Flow: Conditionals & Loops

Type each solution yourself. **Predict every output before you run it.** Solutions at the bottom.

## In class

### Task 1 — Grade-band classifier
Write `letter_grade(score)` returning A/B/C/D/F (90/80/70/60 cutoffs), `"Invalid"` outside 0–100.
**Test the boundaries:** 90, 89.999, 0, 100, -5, 101.

### Task 2 — Boolean logic
1. What is `5 and 0`? `"" or "N/A"`? Why aren't they `True`/`False`?
2. Rewrite `if attended == True:` the Pythonic way.

### Task 3 — Average + pass/fail (loops)
Given `names = ["Ana","Ben","Cara","Dev"]` and `scores = [91, 58, 73, 64]`:
1. Compute the mean with a loop and a running total.
2. Use `zip` to print `"<name>: PASS"` (≥60) or `"<name>: FAIL"`.
3. Count the passes with `sum(s >= 60 for s in scores)`.

### Task 4 — Validation loop
Write a real `while True:` prompt that keeps asking until the user types an integer 0–100.

### Task 5 — Trap check
Why does this skip elements, and what's the fix?
```python
xs = [1, 2, 3, 4]
for x in xs:
    if x % 2 == 0:
        xs.remove(x)
```

### Bonus — Pythonic idiom drill
Cover the `# ->` answers, predict each line, then run.

```python
nums = [80, 92, 45]
print(all(n >= 60 for n in nums))    # -> False   (45 fails)
print(any(n >= 90 for n in nums))    # -> True    (92 passes)
print(92 in nums, 60 in nums)        # -> True False
```

## Extra practice (in class, if you're ahead)

### E1 — Refactor to chained comparisons
Rewrite each with one chained comparison:
1. `if x >= 0 and x <= 100:`
2. `if lo < value and value < hi:`
3. `if a == b and b == c:`

### E2 — Countdown
Print 10 → 1 then `Go!` — once with `range`, once with `while`. Mind the off-by-one at
**both** ends.

## Homework (before Session 4)

*~30–45 minutes, outside class — it doesn't count toward the hour. Try everything before peeking at the solutions.*

### H1 — Attendance labeler
Write `label(pct)` → `"perfect"` (exactly 100), `"good"` (≥ 80), `"at risk"` (≥ 50), else
`"critical"`; `"invalid"` outside 0–100. Loop over
`[100, 92.5, 80, 79.9, 50, 12, -3, 104]` printing `pct -> label`. **Test every boundary.**

### H2 — Number-guessing game
Set `secret = 37`. Loop: ask for a guess (validate it's an integer 1–100 — reuse today's
validation-loop pattern), print `higher` / `lower` / `got it in N tries`. Count attempts.

### H3 — Leap-year checker
`is_leap(year)`: divisible by 4, except centuries unless divisible by 400 — as **one**
boolean expression. Verify: 2024 → True, 1900 → False, 2000 → True, 2026 → False.

---

## Solutions

### In class

```python
# 1
def letter_grade(score):
    if not 0 <= score <= 100: return "Invalid"
    for cutoff, g in [(90,"A"),(80,"B"),(70,"C"),(60,"D")]:
        if score >= cutoff: return g
    return "F"
# 90->A, 89.999->B, 0->F, 100->A, -5->Invalid, 101->Invalid

# 2
# 5 and 0 -> 0 ; "" or "N/A" -> "N/A"  (and/or return an operand, not a bool)
result = "pass" if attended else "absent"     # and just `if attended:`

# 3
total = 0
for s in scores: total += s
print(total / len(scores))                    # 71.5
for name, score in zip(names, scores):
    print(f"{name}: {'PASS' if score >= 60 else 'FAIL'}")
print("passes:", sum(s >= 60 for s in scores))   # 3

# 4
while True:
    raw = input("Score 0–100: ")
    if raw.isdigit() and 0 <= int(raw) <= 100:
        print("Got", int(raw)); break
    print("Try again.")

# 5  Removing while iterating shifts indices, so elements get skipped.
xs = [x for x in xs if x % 2 != 0]            # build a new list instead -> [1, 3]
```

### Extra practice

```python
# E1
0 <= x <= 100
lo < value < hi
a == b == c

# E2
for n in range(10, 0, -1):    # start 10, stop BEFORE 0, step -1
    print(n)
print("Go!")

n = 10
while n >= 1:
    print(n)
    n -= 1
print("Go!")
```

### Homework

```python
# H1
def label(pct):
    if not 0 <= pct <= 100:
        return "invalid"
    if pct == 100:
        return "perfect"
    if pct >= 80:
        return "good"
    if pct >= 50:
        return "at risk"
    return "critical"

for pct in [100, 92.5, 80, 79.9, 50, 12, -3, 104]:
    print(pct, "->", label(pct))
# 100 perfect · 92.5 good · 80 good · 79.9 at risk · 50 at risk · 12 critical ·
# -3 invalid · 104 invalid

# H2
secret, tries = 37, 0
while True:
    raw = input("Guess 1-100: ")
    if not (raw.isdigit() and 1 <= int(raw) <= 100):
        print("Whole number 1-100, try again.")
        continue
    tries += 1
    guess = int(raw)
    if guess < secret:
        print("higher")
    elif guess > secret:
        print("lower")
    else:
        print(f"got it in {tries} tries")
        break

# H3
def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

print(is_leap(2024), is_leap(1900), is_leap(2000), is_leap(2026))
# True False True False
```
