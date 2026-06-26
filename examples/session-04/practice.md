# Session 4 — Practice (25 min)

Start from:
```python
roster = [
    {"name": "Ana", "score": 91}, {"name": "Ben", "score": 58},
    {"name": "Cara", "score": 73}, {"name": "Dev", "score": 64},
]
```

## Task 1 — Rank
Print names sorted by score, highest first.

## Task 2 — Map (dict comprehension)
Build `{name: score}` in one line.

## Task 3 — Group
Build `{"pass": [...names...], "fail": [...names...]}` using a loop.

## Task 4 — Dedup
From `["A","B","A","C","B"]`, get the distinct values and how many there are.

## Task 5 — Aliasing
Show that `b = roster` then `roster.append({...})` also changes `b`. Then make `b` an
independent copy so it doesn't. (Hint: nested dicts → `copy.deepcopy`.)

---
## Solutions

```python
# 1
print([s["name"] for s in sorted(roster, key=lambda s: s["score"], reverse=True)])
# ['Ana', 'Cara', 'Dev', 'Ben']

# 2
name_to_score = {s["name"]: s["score"] for s in roster}

# 3
groups = {"pass": [], "fail": []}
for s in roster:
    groups["pass" if s["score"] >= 60 else "fail"].append(s["name"])

# 4
vals = ["A","B","A","C","B"]
distinct = set(vals); print(distinct, len(distinct))   # {'A','B','C'} 3

# 5
import copy
b = roster                       # alias
roster.append({"name": "Eve", "score": 80})
# b now also has Eve. To stay independent:
b = copy.deepcopy(roster)        # changes to roster no longer touch b
```
