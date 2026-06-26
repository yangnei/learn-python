# Session 3 — Practice (25 min): Conditionals & Loops

## Task 1 — Grade-band classifier
Write `letter_grade(score)` returning A/B/C/D/F (90/80/70/60 cutoffs), `"Invalid"` outside 0–100.
**Test the boundaries:** 90, 89.999, 0, 100, -5, 101.

## Task 2 — Boolean logic
1. What is `5 and 0`? `"" or "N/A"`? Why aren't they `True`/`False`?
2. Rewrite `if attended == True:` the Pythonic way.

## Task 3 — Average + pass/fail (loops)
Given `names = ["Ana","Ben","Cara","Dev"]` and `scores = [91, 58, 73, 64]`:
1. Compute the mean with a loop and a running total.
2. Use `zip` to print `"<name>: PASS"` (≥60) or `"<name>: FAIL"`.
3. Count the passes with `sum(s >= 60 for s in scores)`.

## Task 4 — Validation loop
Write a real `while True:` prompt that keeps asking until the user types an integer 0–100.

## Task 5 — Trap check
Why does this skip elements, and what's the fix?
```python
xs = [1, 2, 3, 4]
for x in xs:
    if x % 2 == 0:
        xs.remove(x)
```

---
## Solutions

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
