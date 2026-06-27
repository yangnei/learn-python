---
marp: true
title: "Session 4 — Data Structures"
paginate: true
---

# Session 4
## Data Structures: list · tuple · dict · set

The containers that hold your data.

---

## Four containers, four jobs

| Type | Syntax | Mutable? | Use for |
|---|---|---|---|
| `list` | `[1, 2, 3]` | yes | ordered, changing collection |
| `tuple` | `(1, 2)` | no | fixed record / coordinates |
| `dict` | `{"k": v}` | yes | key → value lookup |
| `set` | `{1, 2, 3}` | yes | unique items |

---

## Lists & slicing

```python
xs = [10, 20, 30, 40]
xs[0]      # 10     xs[-1]   # 40 (last)
xs[1:3]    # [20, 30]   (stop excluded)
xs[:2]     # [10, 20]
xs[::-1]   # reversed
xs.append(50); xs.sort()      # mutate in place
```

⚠️ `xs.sort()` returns **None** — it sorts in place. Use `sorted(xs)` for a new list.

---

## Dicts = labeled records

```python
student = {"name": "Ana", "gpa": 3.9}
student["name"]              # "Ana"
student.get("major", "N/A")  # safe access with default
student["major"] = "Ed"      # add/update
for key, val in student.items(): ...
```

---

## A list of dicts = a dataset 🧠

```python
roster = [
    {"name": "Ana", "score": 91},
    {"name": "Ben", "score": 58},
]
```

Each dict = a **row/respondent**; each key = a **variable/column**.
This is your tidy dataset until pandas shows up (Session 8).

---

## Sets: unique, fast membership

```python
answers = ["yes", "no", "yes", "maybe", "no"]
set(answers)            # {'yes', 'no', 'maybe'}  — dedup
"yes" in set(answers)   # True, very fast
```

Great for "distinct responses" and "have I seen this ID?"

---

## Comprehensions

```python
[s["score"] for s in roster]                 # list
[s for s in roster if s["score"] >= 60]      # with filter
{s["name"]: s["score"] for s in roster}      # dict
{s["score"] // 10 for s in roster}           # set of score-decades
```

Read as: *expr, for each item, (optionally) if condition.*

---

## Sorting with a key

```python
sorted(roster, key=lambda s: s["score"])               # ascending
sorted(roster, key=lambda s: s["score"], reverse=True) # descending
```

`lambda s: s["score"]` = "sort by the score field."

---

## TRAP: aliasing (labels, not boxes)

```python
a = [1, 2, 3]
b = a                # SAME list
a.append(4)
b                    # [1, 2, 3, 4]  😱

b = a.copy()         # ✅ independent copy
```

`[[0]*3]*3` makes 3 references to ONE row — use `[[0]*3 for _ in range(3)]`.

---

## Your turn

`examples/session-04/practice.md`:
1. Build the roster (list of dicts); sort by score.
2. `{name: score}` dict comprehension.
3. Group students into pass/fail buckets.
4. Demonstrate the aliasing trap and fix it.

---

## Traps recap

- `=` aliases; use `.copy()` / `copy.deepcopy()`.
- `.sort()` returns None (in place); `sorted()` returns new.
- list ≠ tuple even with same contents (Session 2).
- `dict.get(key, default)` avoids `KeyError`.

## Summary
You can store, look up, dedup, sort, and reshape data.
**Next:** package logic into reusable functions.
