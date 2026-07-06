---
marp: true
title: "Session 2 — The Dynamic-Typing Traps"
paginate: true
---

# Session 2
## The Dynamic-Typing Traps

*Learn Python — Session 2 of 10 · one hour.*

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

## Now spring the traps

Open **Traps — predict, then run** below: ~18 one-line traps. For each one,
**say your prediction out loud, then run it** to reveal the real result and
the reason behind it.

Then in `examples/session-02/practice.md`: write `clean_score(value)` that
accepts `5`, `5.0`, or `"5"` and returns a float, rejecting nonsense — safely.

**Next:** Session 3 — control flow: conditionals & loops.

---

## Homework (before Session 3)

*Outside class — it doesn't count toward the hour. Full specs + solutions: `examples/session-02/practice.md` → **Homework**.*

1. **Trap journal** — pick the 5 traps that surprised you most; explain each in one sentence of your own.
2. **`approx_equal(a, b)`** — the float comparison you'll use instead of `==`, forever.
3. **`is_missing(x)`** — tell `None` apart from `0`, `""`, and `False`, correctly.
