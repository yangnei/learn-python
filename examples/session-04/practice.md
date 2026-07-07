# Session 4 — Practice: Data Structures

Type each solution yourself. **Predict every output before you run it.** Solutions at the bottom.

## In class

Start from:
```python
roster = [
    {"name": "Ana", "score": 91}, {"name": "Ben", "score": 58},
    {"name": "Cara", "score": 73}, {"name": "Dev", "score": 64},
]
```

### Task 1 — Rank
Print names sorted by score, highest first.

### Task 2 — Map (dict comprehension)
Build `{name: score}` in one line.

### Task 3 — Group
Build `{"pass": [...names...], "fail": [...names...]}` using a loop.

### Task 4 — Dedup
From `["A","B","A","C","B"]`, get the distinct values and how many there are.

### Task 5 — Aliasing
Show that `b = roster` then `roster.append({...})` also changes `b`. Then make `b` an
independent copy so it doesn't. (Hint: nested dicts → `copy.deepcopy`.)

### Bonus — Pythonic idiom drill
Cover the `# ->` answers, predict each line, then run.

```python
head, *tail = [10, 20, 30, 40]
print(head, tail)                    # -> 10 [20, 30, 40]   (star-unpacking)
print({"a": 1} | {"b": 2})           # -> {'a': 1, 'b': 2}  (dict union, 3.9+)
print({1, 2, 3} & {2, 3, 4})         # -> {2, 3}            (set intersection)
print(list(zip(*[(1, 2), (3, 4)])))  # -> [(1, 3), (2, 4)]  (transpose)
```

## In class — going deeper (second hour)

### Task 1 — Slicing drill
With `xs = list(range(10))`, predict:
`xs[2:5]` · `xs[-3:]` · `xs[:-3]` · `xs[::2]` · `xs[::-1]` · `xs[5:2:-1]`.

### Task 2 — Two cohorts
`fall = {"Ana", "Ben", "Cara"}`, `spring = {"Ben", "Dev"}` — who attended both terms?
either term? only fall? (`&`, `|`, `-`)

### Task 3 — `Counter` in one line
Redo the answer tally (`["yes", "no", "yes", "maybe", "yes", "no"]`) with
`collections.Counter`, and print the top answer with `.most_common(1)`.

### Task 4 — Group with `defaultdict`
Group `roster` (list of dicts with `major`) into `{major: [names]}` using
`collections.defaultdict(list)`.

### Task 5 — Multi-key sort
Sort `[("Ana", 91), ("Ben", 73), ("Cara", 91)]` by score **descending**, ties by name
**ascending** — one `sorted()` call with a tuple key.

### Task 6 — Dedupe, order kept
From `["B", "A", "B", "C", "A"]` produce `["B", "A", "C"]` (first-seen order). Why does
plain `set()` not guarantee this?

## Homework (before Session 5)

*~30–45 minutes, outside class — it doesn't count toward class time. Try everything before peeking at the solutions.*

### Task 1 — Gradebook dict drill
Start from `gradebook = {"Ana": 91, "Ben": 58}`. Then: add Cara (73); Ben resubmits
(58 → 68); look up Dev **without** a `KeyError` (default `"no record"`); delete Ben;
print `name: score` lines sorted by score, highest first.

### Task 2 — Frequency counter
Turn `answers = ["yes", "no", "yes", "maybe", "yes", "no"]` into
`{"yes": 3, "no": 2, "maybe": 1}` with a plain dict and `.get(k, 0)` — no imports. Then
print the most common answer with `max(counts, key=counts.get)`.

### Task 3 — Fix the grid
Build a 3×3 grid of zeros with `[[0]*3]*3`, set `grid[0][0] = 9`, print it — see the bug
with your own eyes. Rebuild it with a comprehension and prove the fix.

---

## Solutions

### In class

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

### In class — going deeper

```python
xs = list(range(10))
xs[2:5]     # [2, 3, 4]          (stop excluded)
xs[-3:]     # [7, 8, 9]          (last three)
xs[:-3]     # [0, 1, 2, 3, 4, 5, 6]
xs[::2]     # [0, 2, 4, 6, 8]    (every other)
xs[::-1]    # reversed COPY
xs[5:2:-1]  # [5, 4, 3]          (backward, stop excluded)

# Task 2
fall & spring   # {'Ben'}            — both terms
fall | spring   # all four names     — either term
fall - spring   # {'Ana', 'Cara'}    — only fall
```

```python
# Task 3
from collections import Counter
counts = Counter(["yes", "no", "yes", "maybe", "yes", "no"])
print(counts, counts.most_common(1))   # Counter({'yes': 3, ...}) [('yes', 3)]

# Task 4
from collections import defaultdict
by_major = defaultdict(list)
for s in roster:
    by_major[s["major"]].append(s["name"])

# Task 5
pairs = [("Ana", 91), ("Ben", 73), ("Cara", 91)]
print(sorted(pairs, key=lambda p: (-p[1], p[0])))
# [('Ana', 91), ('Cara', 91), ('Ben', 73)] — negative flips score, name breaks the tie

# Task 6
xs = ["B", "A", "B", "C", "A"]
print(list(dict.fromkeys(xs)))   # ['B', 'A', 'C'] — dicts remember insertion order;
                                 # a set has no order to keep
```

### Homework

```python
# Task 1
gradebook = {"Ana": 91, "Ben": 58}
gradebook["Cara"] = 73                       # add
gradebook["Ben"] = 68                        # update
print(gradebook.get("Dev", "no record"))     # safe lookup
del gradebook["Ben"]                         # delete
for name, score in sorted(gradebook.items(), key=lambda kv: kv[1], reverse=True):
    print(f"{name}: {score}")                # Ana: 91 / Cara: 73

# Task 2
answers = ["yes", "no", "yes", "maybe", "yes", "no"]
counts = {}
for a in answers:
    counts[a] = counts.get(a, 0) + 1
print(counts)                       # {'yes': 3, 'no': 2, 'maybe': 1}
print(max(counts, key=counts.get))  # yes

# Task 3
grid = [[0] * 3] * 3
grid[0][0] = 9
print(grid)   # [[9,0,0],[9,0,0],[9,0,0]] — three labels on ONE row (aliasing!)

grid = [[0] * 3 for _ in range(3)]
grid[0][0] = 9
print(grid)   # [[9,0,0],[0,0,0],[0,0,0]] — independent rows
```
