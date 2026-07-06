# Python Traps & Gotchas — The Master Cheat Sheet

> The quirks that bite beginners (and plenty of experts). Every behavior below was run and
> verified on CPython 3.11+. Read the **Surprise** column, cover the **Why/Fix**, and predict.
> Keep this open for the whole course.

---

## 1 — Equality `==` vs Identity `is`  *(Session 2)*

| Expression | Result | |
|---|---|---|
| `a = [1,2]; b = [1,2]; a == b` | `True` | same **value** |
| `a = [1,2]; b = [1,2]; a is b` | `False` | different **objects** in memory |
| `a = [1,2]; b = a; a is b` | `True` | `b` is the *same* object (an alias) |

- **`==`** asks "same value?" — this is what you almost always want.
- **`is`** asks "same object?" — use it **only** for `None`, `True`, `False`:
  ```python
  if x is None:        # ✅ correct
  if x == None:        # ⚠️ works, but not idiomatic — use `is`
  ```
- **Identity wrinkle (do NOT rely on this):** CPython caches small integers (−5 to 256) and
  interns some strings, so `a = 256; b = 256; a is b` is `True` but at `257` it may be `False`.
  This is an implementation detail. **For value, always use `==`.**

🧠 *Bridge:* two students with the same GPA are `==`; the same student is `is`.

---

## 2 — Booleans ARE integers  *(Session 2)*

```python
True == 1            # True   (bool is a subclass of int)
False == 0           # True
5 + True             # 6      yes, you can do arithmetic on bools
sum([True, False, True])   # 2   ← counts the Trues
isinstance(True, int)      # True
type(True) is int          # False  (its type is bool, a subtype)
```
- **Fix / use it well:** `sum(conditions)` is the Pythonic way to *count* how many are true.
- **Trap:** `True is 1` is `False` (different objects) even though `True == 1`. Compare with `==`.

🧠 *Bridge:* this is dummy coding (1/0) built into the language — summing flags counts cases.

---

## 3 — Float precision  *(Session 2)*

```python
0.1 + 0.2            # 0.30000000000000004
0.1 + 0.2 == 0.3     # False  😱
```
- **Why:** decimals are stored in binary; most can't be represented exactly. Not a Python bug — every language does this.
- **Fix:**
  ```python
  import math
  math.isclose(0.1 + 0.2, 0.3)     # True   ← compare floats with a tolerance
  round(0.1 + 0.2, 2) == 0.3       # True   ← or round for display/compare
  from decimal import Decimal       # exact decimal arithmetic when you truly need it (money, grades)
  Decimal("0.1") + Decimal("0.2")  # Decimal('0.3')
  ```
- **Rule:** never test computed floats with `==`. Use `math.isclose` (or `round`).

🧠 *Bridge:* you already never test two measured scores for exact equality — same instinct, new cause (binary storage, not measurement error).

---

## 4 — Comparing across types  *(Session 2)*

```python
5 == "5"     # False   (different types → not equal, but NO error)
5 == 5.0     # True    (int vs float compare by numeric value)
5 > "5"      # 💥 TypeError: '>' not supported between 'int' and 'str'
```
- **Equality (`==`/`!=`)** across unrelated types → just `False`, never crashes.
- **Ordering (`<`,`>`,`<=`,`>=`)** across incompatible types → **`TypeError`**.
- **Fix:** convert first. `int("5") == 5` → `True`. Guard with `isinstance` before ordering.

🧠 *Bridge:* the computer can equate "are these the same?" across types, but can't *rank* text against numbers — it has no shared scale.

---

## 5 — Sequences compare element-by-element  *(Session 2 / 4)*

```python
[1, 2] == [1, 2]     # True
[1, 2] == (1, 2)     # False   ← list vs tuple: different types, never equal
(1, 2) < (1, 3)      # True    ← compares position by position (lexicographic)
"apple" < "banana"   # True    ← strings compare char by char (alphabetical-ish)
[1, 2] < [1, 2, 3]   # True    ← prefix is "less than"
```
- **Trap:** a `list` and a `tuple` with identical contents are **never `==`** — type matters.
- Lists/tuples/strings compare left-to-right; the first differing element decides.

---

## 6 — Truthiness (what counts as False)  *(Session 2 / 3)*

```python
# These are all "falsy":
bool(0) bool(0.0) bool("") bool([]) bool({}) bool(set()) bool(None)   # all False
bool("0")   # True!  ← a non-empty string is truthy, even "0"
bool([0])   # True   ← a non-empty list is truthy, even if it holds a 0
```
- **Fix / idiom:** check emptiness directly — `if scores:` not `if len(scores) > 0:`; `if name:` not `if name != "":`.
- **Trap:** `"0"` (string) and `"False"` (string) are **truthy**. Convert user input before testing.

---

## 7 — `and` / `or` return an operand, not a bool  *(Session 3)*

```python
5 and 0      # 0      (and → first falsy, or last value)
0 or "hi"    # "hi"   (or → first truthy, or last value)
"" or "N/A"  # "N/A"  ← handy default-value idiom
```
- **Use it well:** `name = user_input or "Anonymous"` supplies a default.
- **Trap:** don't write `if x == True`. Just `if x:`. And `and`/`or` short-circuit — the right
  side may never run, so don't hide side effects there.

---

## 8 — Mutable default arguments  *(Session 5)* — the famous one

```python
def add_student(name, roster=[]):     # ❌ DANGER
    roster.append(name)
    return roster

add_student("Ana")     # ['Ana']
add_student("Ben")     # ['Ana', 'Ben']  😱  the default list PERSISTS across calls
```
- **Why:** the default `[]` is created **once**, when the function is *defined*, and reused every call.
- **Fix:**
  ```python
  def add_student(name, roster=None):   # ✅
      if roster is None:
          roster = []
      roster.append(name)
      return roster
  ```
- **Rule:** never use a mutable default (`[]`, `{}`, `set()`). Use `None` and create inside.

---

## 9 — Aliasing: variables are labels, not boxes  *(Session 4)*

```python
a = [1, 2, 3]
b = a            # b is the SAME list, not a copy
a.append(4)
b                # [1, 2, 3, 4]  😱  b changed too

b = a.copy()     # ✅ now b is an independent (shallow) copy
import copy
b = copy.deepcopy(a)   # ✅ independent even for nested lists/dicts
```
- **Trap:** `grid = [[0] * 3] * 3` makes **three references to one row** — editing `grid[0][0]` changes all rows. Use `[[0]*3 for _ in range(3)]`.
- **Rule:** assignment never copies. `=` binds another name to the same object.

🧠 *Bridge:* a variable is a sticky label on an object, not a container holding a value.

---

## 10 — `type()` vs `isinstance()`  *(Session 2)*

```python
isinstance(x, int)              # ✅ Pythonic; respects inheritance
isinstance(x, (int, float))     # ✅ "is x any kind of number?"
type(x) is int                  # exact type only; rarely what you want
type(x) == int                  # works but use `is` for type identity
```
- **Trap:** `isinstance(True, int)` is `True` (bool is a subtype of int). If you must exclude bools,
  check `type(x) is int` or `isinstance(x, int) and not isinstance(x, bool)`.

---

## 11 — Integer vs float division  *(Session 1 / 2)*

```python
7 / 2      # 3.5   true division ALWAYS returns a float
7 // 2     # 3     floor division (rounds toward −∞)
-7 // 2    # -4    ← floors, doesn't truncate toward zero!
7 % 2      # 1     modulo (remainder) — use % 2 to test even/odd
7 / 0      # 💥 ZeroDivisionError
```
- **Trap:** `/` gives a float even when the result is whole (`4 / 2` is `2.0`). Use `//` for integer results.

---

## 12 — Strings are immutable; some methods *return*, don't mutate  *(Session 1 / 9)*

```python
s = "  Hello  "
s.strip()          # "Hello"   ← returns a NEW string
s                  # "  Hello  "  ← s is UNCHANGED
s = s.strip()      # ✅ reassign to keep the result
```
- **Trap:** `s.strip()` / `s.replace(...)` / `s.upper()` do nothing to `s` unless you reassign.
- Contrast: list methods like `.append()`/`.sort()` mutate **in place** and return `None`:
  ```python
  nums = [3, 1, 2]
  nums = nums.sort()    # ❌ now nums is None!  .sort() returns None
  nums.sort()           # ✅ sorts in place; use sorted(nums) to get a new list
  ```

---

## 13 — `range` excludes the stop; off-by-one  *(Session 3)*

```python
list(range(1, 5))      # [1, 2, 3, 4]   ← 5 is NOT included
list(range(5))         # [0, 1, 2, 3, 4]
list(range(0, 10, 2))  # [0, 2, 4, 6, 8]
```
- **Rule:** `range(a, b)` is the half-open interval `[a, b)`.

---

## 14 — Modifying a list while iterating it  *(Session 3)*

```python
xs = [1, 2, 3, 4]
for x in xs:
    if x % 2 == 0:
        xs.remove(x)     # ❌ skips elements / unpredictable
# ✅ iterate a copy, or build a new list:
xs = [x for x in xs if x % 2 != 0]
```

---

## 15 — Files: `"w"` overwrites; cursor exhausts  *(Session 8)*

```python
open("data.csv", "w")    # ❗ TRUNCATES the file to empty immediately
open("data.csv", "a")    # append
open("data.csv", "r")    # read (default)

with open("data.csv") as f:
    rows = f.readlines()      # read once
    again = f.readlines()     # [] — cursor is at end of file now
```
- Always prefer `with open(...) as f:` — it closes the file even if the code crashes.
- With the `csv` module on Windows, open with `newline=""` to avoid blank rows.

---

## 16 — Regex: `.` matches *anything*; use raw strings  *(Session 9)*

```python
import re
re.search(r"\d+", "id 42")     # use r"..." so \d isn't a Python escape
re.search(".", "a.b")          # the "." matches "a", not just the dot!
re.search(r"\.", "a.b")        # use \. for a literal dot
```
- **Rule:** always write patterns as raw strings `r"..."`. Escape `. ^ $ * + ? ( ) [ ] { } | \`.

---

## Quick "predict-then-run" self-test (cover the answers)
```python
print(True + True)            # 2
print(3 == 3.0)               # True
print(0.1 + 0.2 == 0.3)       # False
print(5 == "5")               # False
print([1,2] == (1,2))         # False
print(bool("0"))              # True
print(7 // 2, -7 // 2)        # 3 -4
x = [1]; y = x; x.append(2); print(y)   # [1, 2]
```
If you can explain *why* for all eight, you've got the fundamentals most beginners miss.
