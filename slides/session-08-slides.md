---
marp: true
title: "Session 8 — Files, Libraries & Research Data"
paginate: true
---

# Session 8
## Files, Libraries & Research Data

The hour your actual data shows up.

---

## Opening files with `with`

```python
with open("notes.txt") as f:
    text = f.read()
# file auto-closes here, even if the code crashes
```

`with` = a context manager: sets up and tears down the resource for you.
Always prefer it to a bare `open()`/`close()`.

---

## File modes (mind the trap)

| Mode | Meaning |
|---|---|
| `"r"` | read (default) |
| `"w"` | write — **truncates the file to empty first!** |
| `"a"` | append |
| `"r+"` | read + write |

⚠️ Open the wrong file with `"w"` → its contents are gone.

---

## Reading text

```python
with open("notes.txt") as f:
    whole = f.read()           # one big string
    # or
    for line in f:             # line by line (memory-friendly)
        print(line.rstrip())
```

⚠️ A file object is exhausted after one pass — re-open to read again.

---

## CSV in, as dicts 🧠

```python
import csv
with open("students.csv", newline="") as f:
    for row in csv.DictReader(f):
        print(row["name"], row["score"])   # row is a dict keyed by header
```

`csv.DictReader` turns each row into a dict — your "list of dicts" dataset from Session 4.
(`newline=""` avoids blank rows on Windows.)

---

## CSV out

```python
with open("summary.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["name", "score"])
    w.writeheader()
    w.writerow({"name": "Ana", "score": 91})
```

---

## Libraries a researcher reaches for

```python
import statistics
statistics.mean(xs); statistics.median(xs); statistics.stdev(xs)

import random
random.choice(xs); random.randint(1, 6); random.shuffle(xs)

from datetime import date
date.today()

from pathlib import Path
Path("students.csv").exists()
```

`pip install <package>` for third-party libs.

---

## The pandas teaser (your next course)

```python
import pandas as pd
df = pd.read_csv("students.csv")
df["score"].describe()      # count, mean, std, min, quartiles, max
df.groupby("major")["score"].mean()
```

Everything you did by hand today — in three lines.
We learned the fundamentals *underneath* it first.

---

## Your turn

`examples/session-08/practice.md` (uses `survey.csv`):
1. Read `students.csv`; print class mean with `statistics.mean`.
2. Compute per-item survey means; write `survey_summary.csv`.

---

## Traps recap

- `"w"` silently overwrites — be sure of the filename.
- `csv` module → open with `newline=""`.
- Files exhaust after one read; re-open to re-read.
- Specify `encoding="utf-8"` for non-ASCII text.

## Summary
You can load, summarize, and write real research data.
**Next:** clean and validate text with regular expressions.
