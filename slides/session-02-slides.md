---
marp: true
title: "Session 2 — The Dynamic-Typing Traps"
paginate: true
---

# Session 2
## The Dynamic-Typing Traps

*Predict every line before you run it.*

---

## Why this hour matters

Python won't lock a variable to a type. That freedom creates **subtle traps**:
mixing numbers, comparing across types, trusting floats.

Master these now → every later session is easier.

> Method today: **predict → run → explain the surprise.**

---

## Equality `==` vs Identity `is`

```python
a = [1, 2]; b = [1, 2]
a == b      # True   same VALUE
a is b      # False  different OBJECTS
c = a
a is c      # True   same object (alias)
```

- `==` → "same value?" (almost always what you want)
- `is` → "same object?" (use only for `None`, `True`, `False`)

🧠 Same GPA = `==`. Same student = `is`.

---

## Use `is` only for None/True/False

```python
if x is None:     # ✅
if x == None:     # ⚠️ works, not idiomatic
```

**Wrinkle (never rely on it):** CPython caches small ints (−5…256), so
`256 is 256` → True but `257 is 257` may be False. For value, always `==`.

---

## Booleans ARE integers

```python
True == 1                 # True
False == 0                # True
5 + True                  # 6
sum([True, False, True])  # 2   <- counts the Trues
```

🧠 This is dummy coding (1/0) baked into the language.
`sum(conditions)` = "how many are true?"

---

## ...but identity still differs

```python
True == 1     # True   (value)
True is 1     # False  (different objects)
```

Compare with `==`. `isinstance(True, int)` → `True` (bool is a *subtype* of int).

---

## Int vs float

```python
3 == 3.0      # True   (compared by numeric value)
7 / 2         # 3.5    / ALWAYS returns a float
7 // 2        # 3      floor division
-7 // 2       # -4     floors toward -infinity
```

`4 / 2` is `2.0` (a float!), not `2`.

---

## Float precision 😱

```python
0.1 + 0.2            # 0.30000000000000004
0.1 + 0.2 == 0.3     # False
```

Not a bug — decimals stored in **binary** can't all be exact.

```python
import math
math.isclose(0.1 + 0.2, 0.3)   # True  ✅
round(0.1 + 0.2, 2) == 0.3     # True  ✅
```

🧠 You already never `==` two measured scores. Same instinct, new cause.

---

## Comparing across types

```python
5 == "5"     # False   (different types, NO error)
5 == 5.0     # True    (numbers compare by value)
5 > "5"      # 💥 TypeError: '>' not supported
```

- `==`/`!=` across types → `False` (never crashes).
- `<`/`>` across incompatible types → **TypeError**.

🧠 Computer can ask "same?" but can't *rank* text vs numbers — no shared scale.

---

## Sequences compare element-by-element

```python
[1, 2] == [1, 2]    # True
[1, 2] == (1, 2)    # False  (list vs tuple = different types)
(1, 2) < (1, 3)     # True   (position by position)
"apple" < "banana"  # True   (char by char)
```

A list and a tuple with the same contents are **never equal**.

---

## type() vs isinstance()

```python
isinstance(x, int)            # ✅ Pythonic, respects inheritance
isinstance(x, (int, float))   # ✅ "any kind of number?"
type(x) is int                # exact type only
```

**Gotcha:** `isinstance(True, int)` is `True`.
To exclude bools: `isinstance(x, int) and not isinstance(x, bool)`.

---

## Truthiness

```python
# Falsy:  0  0.0  ""  []  {}  set()  None
# Truthy: everything else — including "0", "False", [0]
bool("0")   # True!
bool([0])   # True
```

Idiom: `if scores:` (not `if len(scores) > 0:`).
But convert user text first — `"0"` is truthy.

---

## Predict-then-run gauntlet

Cover the answers; commit out loud first.

```python
True + True            # ?
3 == 3.0               # ?
0.1 + 0.2 == 0.3       # ?
5 == "5"               # ?
[1,2] == (1,2)         # ?
bool("0")              # ?
x=[1]; y=x; x.append(2); y   # ?
```

---

## Your turn

`examples/session-02/practice.md`:
1. Explain each gauntlet line.
2. Write `clean_score(value)` that accepts `5`, `5.0`, or `"5"` and returns a float,
   rejecting nonsense — safely.

---

## Traps recap (take the cheat sheet)

- `==` value, `is` identity (only None/True/False).
- `True == 1`; `sum(bools)` counts.
- Never `==` floats → `math.isclose`.
- `5=="5"`→False; `5>"5"`→TypeError.
- list ≠ tuple even with same contents.
- `isinstance` over `type`; bools are ints.

**Next:** Control flow — conditionals & loops, now that you know what's *really* being compared.
