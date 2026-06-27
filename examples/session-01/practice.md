# Session 1 — Practice (60 min)

Type each solution yourself. Predict output before running. Solutions at the bottom.

## Task 1 — Warm-up REPL
In the REPL (`python3`), check the type of: `42`, `42.0`, `"42"`, `True`, `None`, `7/2`, `7//2`.
*What surprises you?* (Hint: `7/2`.)

## Task 2 — GPA reporter (`gpa.py`)
Ask for a name and a GPA (a decimal). Print:
`"<name>'s GPA is <gpa to 2 decimals>, which is <87.5%> of a 4.0 scale."`

## Task 3 — Survey age bucket (`age.py`)
Ask for an age (integer). Print the age, and the age in "months lived" (age × 12).
Then deliberately type `twenty` instead of a number and **read the traceback's last line.**

## Task 4 — Stretch: the string trap
Without converting, what does `input("a: ") + input("b: ")` print if you type `2` then `3`?
Now fix it so it prints `5`.

## Bonus — Pythonic idiom drill
Cover the `# ->` answers, predict each line, then run.

```python
a, b = 1, 2
a, b = b, a;          print(a, b)        # -> 2 1   (swap, no temp variable)
print(f"{a + b = }")                     # -> a + b = 3   (self-documenting f-string)
print("CS50".lower(), "  hi ".strip())   # -> cs50 hi
print("@" in "ana@uni.edu", len("data")) # -> True 4   (membership + length)
```

---
## Solutions

```python
# Task 2 — gpa.py
name = input("Name: ")
gpa = float(input("GPA: "))
print(f"{name}'s GPA is {gpa:.2f}, which is {gpa/4:.1%} of a 4.0 scale.")

# Task 3 — age.py
age = int(input("Age: "))
print(f"You are {age} years old, about {age*12} months.")
# Typing "twenty" -> ValueError: invalid literal for int() with base 10: 'twenty'

# Task 4
# "2" + "3" -> "23"  (string concatenation)
a = int(input("a: ")); b = int(input("b: "))
print(a + b)          # 5
```
