# Session 4 — Practice (60 min)

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

## Bonus — Pythonic idiom drill
Cover the `# ->` answers, predict each line, then run.

```python
head, *tail = [10, 20, 30, 40]
print(head, tail)                    # -> 10 [20, 30, 40]   (star-unpacking)
print({"a": 1} | {"b": 2})           # -> {'a': 1, 'b': 2}  (dict union, 3.9+)
print({1, 2, 3} & {2, 3, 4})         # -> {2, 3}            (set intersection)
print(list(zip(*[(1, 2), (3, 4)])))  # -> [(1, 3), (2, 4)]  (transpose)
```

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
