# Python Quick Reference — Syntax You'll Forget

> The "how do I write that again?" sheet. Grouped by session.

## I/O & types  *(S1)*
```python
name = input("Name: ")          # ALWAYS returns a str
age  = int(input("Age: "))      # convert immediately
print("Hi", name, age)          # space-separated
print(f"Hi {name}, age {age}")  # f-string (preferred)
print(f"{score:.2f}")           # 2 decimals
print(f"{count:,}")             # thousands separator: 1,234
print("no newline", end="")     # suppress the trailing \n
int("42"), float("3.14"), str(42), bool(0)   # casts
type(x)                          # what type is x?
```

## f-string formatting mini-table
| Spec | Example | Output |
|---|---|---|
| `:.2f` | `f"{3.14159:.2f}"` | `3.14` |
| `:,` | `f"{1234567:,}"` | `1,234,567` |
| `:>8` | `f"{'hi':>8}"` | `      hi` (right-align) |
| `:<8` | `f"{'hi':<8}"` | `hi      ` (left-align) |
| `:^8` | `f"{'hi':^8}"` | `   hi   ` (center) |
| `:.1%` | `f"{0.873:.1%}"` | `87.3%` |

## Conditionals  *(S3)*
```python
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "F"

90 <= score <= 100              # chained comparison
grade = "pass" if score >= 60 else "fail"   # ternary

match command:                   # Python 3.10+
    case "start": ...
    case "stop" | "halt": ...    # multiple values
    case _: ...                  # default
```

## Loops  *(S3)*
```python
for i in range(5): ...                  # 0..4
for x in items: ...                     # each element
for i, x in enumerate(items): ...       # index + element
for a, b in zip(names, scores): ...     # walk two lists together
while condition: ...
while True:                             # validation loop
    x = input("...")
    if valid(x):
        break
# break / continue control flow
```

## Sequences & slicing  *(S4)*
```python
xs = [1, 2, 3]; xs.append(4); xs[0]; xs[-1]   # last
xs[1:3]      # [2, 3]   (start inclusive, stop exclusive)
xs[:2]       # first two
xs[::-1]     # reversed
t = (1, 2)                       # tuple (immutable)
d = {"name": "Ana", "gpa": 3.9}  # dict
d["name"]; d.get("missing", 0)   # access; safe access w/ default
d.keys(); d.values(); d.items()
s = {1, 2, 2, 3}                 # set -> {1, 2, 3}  (unique)
```

## Comprehensions  *(S4/S10)*
```python
[x*2 for x in xs]                       # list
[x for x in xs if x > 0]                # with filter
{name: 0 for name in names}             # dict
{x % 3 for x in xs}                     # set
(x*x for x in xs)                       # generator (lazy)
```

## Sorting  *(S4)*
```python
sorted(xs)                              # new sorted list
sorted(xs, reverse=True)
sorted(students, key=lambda s: s["gpa"])          # by a field
sorted(students, key=lambda s: s["gpa"], reverse=True)
xs.sort()                               # in place (returns None!)
```

## Functions  *(S5)*
```python
def avg(nums: list[float]) -> float:
    """Return the mean of nums."""      # docstring
    return sum(nums) / len(nums)

def greet(name, greeting="Hello"): ...  # default arg (NOT mutable!)
def total(*args): ...                   # any number of positionals -> tuple
def config(**kwargs): ...               # any number of keywords -> dict
func(*my_list)                          # unpack list into args
func(**my_dict)                         # unpack dict into kwargs
```

## Exceptions  *(S7)*
```python
try:
    n = int(value)
except ValueError:
    n = None
except (KeyError, IndexError) as e:
    print(e)
else:
    print("ok")          # ran only if no exception
finally:
    print("always")      # cleanup, always runs

raise ValueError("score must be 1–5")
assert n > 0, "n must be positive"
```

## Files & CSV  *(S8)*
```python
with open("f.txt") as f:          # read, auto-closes
    text = f.read()
with open("f.txt", "w") as f:     # write (OVERWRITES)
    f.write("line\n")

import csv
with open("data.csv", newline="") as f:
    for row in csv.DictReader(f):    # row is a dict keyed by header
        print(row["name"])

with open("out.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["name", "gpa"])
    w.writeheader()
    w.writerow({"name": "Ana", "gpa": 3.9})
```

## Handy stdlib  *(S8)*
```python
import statistics; statistics.mean(xs); statistics.median(xs); statistics.stdev(xs)
import random; random.choice(xs); random.randint(1, 6); random.shuffle(xs)
from datetime import date; date.today(); date(2026, 6, 26)
from pathlib import Path; Path("data.csv").exists()
import json; json.dumps(obj, indent=2); json.loads(text)
```

## Regex  *(S9)*
```python
import re
re.search(r"pattern", text)      # first match anywhere (or None)
re.fullmatch(r"\d{5}", zip)      # whole string must match
re.sub(r"\s+", " ", text)        # collapse whitespace
m = re.search(r"(\w+)@(\w+)", s)
m.group(1)                        # first capture group
```
| Token | Means |
|---|---|
| `.` | any char (except newline) |
| `\d \w \s` | digit / word-char / whitespace |
| `+ * ?` | 1+, 0+, 0-or-1 |
| `{m,n}` | between m and n |
| `^ $` | start / end |
| `[...] [^...]` | set / not-in-set |
| `(...)` | capture group |
| `a\|b` | a or b |

## Classes  *(S10)*
```python
class Student:
    def __init__(self, name, gpa):
        self.name = name
        self._gpa = gpa
    def __str__(self):
        return f"{self.name} ({self._gpa})"
    @property
    def gpa(self):
        return self._gpa
    @gpa.setter
    def gpa(self, value):
        if not 0 <= value <= 4:
            raise ValueError("gpa out of range")
        self._gpa = value

s = Student("Ana", 3.9)
print(s)            # uses __str__
```

## The program skeleton  *(every script)*
```python
def main():
    ...

def helper():
    ...

if __name__ == "__main__":
    main()
```
