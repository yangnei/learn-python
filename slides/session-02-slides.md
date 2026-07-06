---
marp: true
title: "Session 2 — The Dynamic-Typing Traps"
paginate: true
---

# Session 2
## The Dynamic-Typing Traps

---

## A name is just a label

Python won't lock a name to a type — it can point at an `int` now and a
`str` later. That freedom is powerful, but it creates **traps** where the
result contradicts your intuition.

> This session is hands-on. Every rule below has a one-line, runnable trap in
> **Traps — predict, then run** at the bottom of the page. Predict first,
> then reveal.

---

## `==` value, `is` identity

- `==` asks "same value?" — almost always what you want.
- `is` asks "same object?" — use it only for `None` (and `True`/`False`).
- `b = a` does **not** copy: both names point at one list, so mutating `a`
  shows through `b`. Copy with `list(a)` or `a[:]`.

🧠 Same GPA = `==`. Same student = `is`.

---

## Booleans are integers

- `bool` is a *subtype* of `int`, so `True` behaves as `1` and `False` as `0`.
- That means `5 + True` works, and `sum(flags)` counts how many are `True`.
- Identity still differs, and `isinstance(True, int)` is true while
  `type(True) is int` is not.

🧠 Dummy coding (1/0) baked right into the language.

---

## Numbers: int, float, division

- `/` **always** returns a float (`4 / 2` is `2.0`); `//` floors **toward −∞**.
- `3 == 3.0` compares by value, but decimals are stored in **binary**, so
  `0.1 + 0.2` is not exactly `0.3`.
- Never test two floats with `==` — use `math.isclose(a, b)`. (You already
  never compare two measured scores for exact equality; same instinct.)

---

## Comparing across types

- `==` / `!=` across types returns `False` and never crashes.
- `<` / `>` across incompatible types raises **TypeError** — the computer can
  ask "same?" but can't *rank* text against numbers.
- A list and a tuple with the same contents are **never equal**; sequences
  compare element by element.

---

## Truthiness

- Falsy: `0  0.0  ""  []  {}  set()  None`. Truthy: everything else —
  including `"0"`, `"False"`, and `[0]`.
- Idiom: `if scores:` rather than `if len(scores) > 0:`.
- But convert user text first — `"0"` is truthy.

---

# Going deeper
## None, conversions & exact decimals

---

## `None`, properly

- `None` means **absence** — "no value here" — not zero, not empty.
- Test with identity: `if x is None:` (never `== None`).
- A function without `return` hands back `None` (you'll meet this again in Session 5).
- Three different "nothings": `None` (missing) · `""` (empty text) · `0` (a real count of zero).
  A survey blank is `None`-shaped; a student with 0 points is not missing.

---

## The conversion matrix

| Call | Result |
|---|---|
| `int("42")` | `42` |
| `int("4.2")` | 💥 `ValueError` |
| `float("4.2")` | `4.2` |
| `int(4.9)` | `4` (truncates) |
| `int(float("4.2"))` | `4` — the two-step |
| `str(4.2)` | `"4.2"` (anything converts *to* str) |

**Rule: convert at the edge, once** — the moment data enters, make it the right type.

---

## `nan` and `inf`

```python
bad = float("nan")     # "not a number" — a failed/missing numeric
bad == bad             # False! NaN equals nothing
import math
math.isnan(bad)        # True — the only reliable test
float("inf") > 10**100 # True — infinity beats everything
```

NaN appears in real data pipelines (pandas uses it for missing cells) — recognize it now.

---

## Mutable vs immutable

| Immutable (can't change) | Mutable (can change) |
|---|---|
| `int, float, bool, str, tuple, None` | `list, dict, set` |

```python
id(x)    # the object's identity — what `is` actually compares
```

Immutables are safe to share; mutables make **aliases** (`b = a` shares!). That's Session 4's
headline trap — you now know *why* it happens.

---

## When floats aren't good enough: `Decimal`

```python
from decimal import Decimal
Decimal("0.1") + Decimal("0.2") == Decimal("0.3")   # True!
```

- Exact decimal arithmetic — build it **from strings**, not floats.
- Use for money and any bookkeeping where `isclose` isn't acceptable.
- Cost: wordier and slower — floats stay the everyday default.
- (`fractions.Fraction` exists too: exact thirds, `Fraction(1, 3)`.)

---

## Chained comparisons, revisited

```python
1 <= likert <= 5        # both ends checked — reads like math
a == b == c             # all three equal
```

But don't chain `is` or mix operators cleverly — chain only when it reads *exactly* like the math
you mean.

---

## Your turn — round 2

`examples/session-02/practice.md` → **In class — going deeper**:
the conversion-matrix prediction table, a `Decimal` re-run of `0.1 + 0.2`, and `describe(x)`
telling `None` / `""` / `0` apart.
---

## Now spring the traps

Open **Traps — predict, then run** below: ~18 one-line traps. For each one,
**say your prediction out loud, then run it** to reveal the real result and
the reason behind it.

Then in `examples/session-02/practice.md`: write `clean_score(value)` that
accepts `5`, `5.0`, or `"5"` and returns a float, rejecting nonsense — safely.

**Next:** Session 3 — control flow: conditionals & loops.

---

## Homework (before Session 3)

*Outside class — it doesn't count toward class time. Full specs + solutions: `examples/session-02/practice.md` → **Homework**.*

1. **Trap journal** — pick the 5 traps that surprised you most; explain each in one sentence of your own.
2. **`approx_equal(a, b)`** — the float comparison you'll use instead of `==`, forever.
3. **`is_missing(x)`** — tell `None` apart from `0`, `""`, and `False`, correctly.
