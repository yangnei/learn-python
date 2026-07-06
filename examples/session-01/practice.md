# Session 1 — Practice: Running Python, Variables & Types

Type each solution yourself. **Predict every output before you run it.** Solutions at the bottom.

## In class

Type each solution yourself. Predict output before running. Solutions at the bottom.

### Task 1 — Warm-up REPL
In the REPL (`python3`), check the type of: `42`, `42.0`, `"42"`, `True`, `None`, `7/2`, `7//2`.
*What surprises you?* (Hint: `7/2`.)

### Task 2 — GPA reporter (`gpa.py`)
Ask for a name and a GPA (a decimal). Print:
`"<name>'s GPA is <gpa to 2 decimals>, which is <87.5%> of a 4.0 scale."`

### Task 3 — Survey age bucket (`age.py`)
Ask for an age (integer). Print the age, and the age in "months lived" (age × 12).
Then deliberately type `twenty` instead of a number and **read the traceback's last line.**

### Task 4 — Stretch: the string trap
Without converting, what does `input("a: ") + input("b: ")` print if you type `2` then `3`?
Now fix it so it prints `5`.

### Bonus — Pythonic idiom drill
Cover the `# ->` answers, predict each line, then run.

```python
a, b = 1, 2
a, b = b, a;          print(a, b)        # -> 2 1   (swap, no temp variable)
print(f"{a + b = }")                     # -> a + b = 3   (self-documenting f-string)
print("CS50".lower(), "  hi ".strip())   # -> cs50 hi
print("@" in "ana@uni.edu", len("data")) # -> True 4   (membership + length)
```

## In class — going deeper (second hour)

### E1 — f-string formatting drill
Given `pi = 3.14159265`, `n = 9876543`, `rate = 0.4567`, print exactly:
`3.14` · `9,876,543` · `45.7%` · `pi = 3.14159265` (the self-documenting form).

### E2 — Weeks enrolled
Extend `age.py`: also report the age in **weeks** (52 per year), with a thousands separator.

### D1 — Aligned gradebook lines
Print three students (`name, score, rate`) as aligned columns: name left-padded to 10,
score right-aligned with 1 decimal, rate as a percent. All three lines must line up.

### D2 — Name normalizer
Turn `"  aDA lovelace "` into `"Ada Lovelace"` by *chaining* string methods, then report
`len()` of the result and whether it `.startswith("Ada")`.

### D3 — Whole units + remainder
1. Convert 130 minutes into `2 h 10 min` using `//` and `%`.
2. Assign student IDs `[101, 102, 103, 104, 105, 106]` to discussion groups 0/1/2 with `%`.

## Homework (before Session 2)

*~30–45 minutes, outside class — it doesn't count toward class time. Try everything before peeking at the solutions.*

### H1 — Unit converter (`convert.py`)
Ask for a distance in miles (may be a decimal). Print kilometers (`× 1.60934`) to 2
decimals and meters with a thousands separator:
`5.0 miles = 8.05 km (8,047 meters)`

### H2 — Traceback drill
Break each of these on purpose in a script, run it, and copy down the LAST line of each
traceback:
1. `int("ten")`
2. `"age: " + 21`
3. `print(nmae)` right after `name = "Ada"` (typo on purpose)
Then, one sentence each: what does the error *name* tell you?

### H3 — Type-prediction table
Predict `type(...)` (or the output) of each, then check in the REPL:
`7/2` · `7//2` · `7.0//2` · `"7"*2` · `int("7")*2` · `7 == 7.0` · `None` · `input`
(no parentheses!) · `print("hi")`

---

## Solutions

### In class

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

### In class — going deeper

```python
pi, n, rate = 3.14159265, 9876543, 0.4567
print(f"{pi:.2f}")        # 3.14
print(f"{n:,}")           # 9,876,543
print(f"{rate:.1%}")      # 45.7%
print(f"{pi = }")         # pi = 3.14159265

# E2
age = int(input("Age: "))
print(f"That's about {age * 52:,} weeks.")
```

```python
# D1
for name, score, rate in [("Ana", 91.456, 0.873), ("Ben", 58.0, 0.412), ("Cara", 73.2, 0.65)]:
    print(f"{name:<10}{score:>8.1f}{rate:>8.1%}")

# D2
clean = "  aDA lovelace ".strip().title()
print(clean, len(clean), clean.startswith("Ada"))   # Ada Lovelace 12 True

# D3
minutes = 130
print(f"{minutes // 60} h {minutes % 60} min")      # 2 h 10 min
for sid in [101, 102, 103, 104, 105, 106]:
    print(sid, "-> group", sid % 3)
```

### Homework

```python
# H1 — convert.py
miles = float(input("Miles: "))
km = miles * 1.60934
print(f"{miles} miles = {km:.2f} km ({round(km * 1000):,} meters)")
```

H2 — the last lines, and what the names mean:
1. `ValueError: invalid literal for int() with base 10: 'ten'` — right *type* of argument, unusable value.
2. `TypeError: can only concatenate str (not "int") to str` — the types themselves don't fit the operation.
3. `NameError: name 'nmae' is not defined` — you used a name that was never assigned (usually a typo).

```python
# H3 — what type() says
7 / 2         # float — / always gives a float (3.5)
7 // 2        # int   — floor division of two ints (3)
7.0 // 2      # float — floored VALUE, float TYPE (3.0)
"7" * 2       # str   — repetition: '77', not math
int("7") * 2  # int   — 14
7 == 7.0      # bool  — True (numbers compare by value)
None          # NoneType
input         # builtin_function_or_method — a function is a value too
print("hi")   # prints hi, then evaluates to None (print returns nothing)
```
