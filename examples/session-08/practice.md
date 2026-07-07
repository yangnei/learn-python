# Session 8 — Practice: Files, Libraries & Research Data

Type each solution yourself. **Predict every output before you run it.** Solutions at the bottom.

## In class

Files provided: `students.csv`, `survey.csv`.

### Task 1 — Read & summarize students
Read `students.csv` with `csv.DictReader`. Remember the values are **strings** — convert
`score` to `int`. Print the class mean and median with the `statistics` module.

### Task 2 — Mean by major
Build `{major: mean_score}`. (Hint: `dict.setdefault(key, []).append(...)`.)

### Task 3 — Clean & summarize the survey
`survey.csv` has `"N/A"` and blanks in numeric columns. For each `q*` item, compute the
mean of the **valid** values only, and how many were valid. Write `survey_summary.csv`
with columns `item,mean,n_valid`.

### Task 4 — pandas teaser (optional)
If `pandas` is installed: `pd.read_csv("students.csv")["score"].describe()`. Compare the
mean to your hand-computed one.

### Trap check
What happens if you accidentally open `students.csv` with mode `"w"` before reading it?

### Bonus — Pythonic idiom drill
Cover the `# ->` answers, predict each line, then run.

```python
import json
s = json.dumps({"n": 3, "ok": True})
print(s)                             # -> {"n": 3, "ok": true}   (Python True -> JSON true)
print(json.loads(s)["ok"])           # -> True                   (and back to a Python bool)
```

## In class — going deeper (second hour)

### Task 1 — One more column
Extend the survey summary: add a `pct_valid` column (share of rows with a usable value),
formatted to one decimal.

### Task 2 — pathlib mini-tour
With `from pathlib import Path`: does `students.csv` exist? How many bytes is it
(`.stat().st_size`)? List every `.csv` in this folder (`.glob`).

### Task 3 — pathlib inventory
List every `.csv` in this folder with its size in bytes, one aligned line each, using
`Path(".").glob` and `.stat().st_size`.

### Task 4 — Date math
Parse `"2026-01-05"` and `"2026-07-06"` with `strptime`, print the number of days between
them, and print the first date as `Jan 05, 2026` with `strftime`.

### Task 5 — A reproducible sample
Seed with `random.seed(42)`, then `random.sample` 3 names from the students in
`students.csv`. Run it twice — same three? Why does a methods section care?

### Task 6 — CSV → JSON
Read `students.csv` into a list of dicts with **int** scores, and write it to
`students.json` with `indent=2`. Open the file: what happened to the quotes and numbers?

### Task 7 — Take the filename from the command line
Turn Task 1 into `report.py`: read the CSV named on the command line
(`python3 report.py students.csv`), print the class mean, and exit with a usage
message when the argument is missing or extra. (`sys.argv`, `sys.exit`.)

### Task 8 — An animated before/after
With Pillow (`pip install pillow`), generate two solid-color frames using
`Image.new("RGB", (60, 60), color)` and save them as one looping GIF
(`save_all=True`, `append_images=[...]`, `duration=400`, `loop=0`). Open the file —
it pulses. How big is this binary file (`pathlib`)?

## Homework (before Session 9)

*~30–45 minutes, outside class — it doesn't count toward class time. Try everything before peeking at the solutions.*

### Task 1 — Attendance report (the whole pipeline)
Create `attendance.csv` yourself: a `name` column plus five `s1..s5` columns of 0/1, about
six rows — and sneak in one dirty cell (`"?"`). Then: read it with `DictReader`, compute
each student's attendance rate (skip dirty cells; remember that summing 0/1 ints just
works), and write `attendance_report.csv` with `name,rate,n_valid` via `DictWriter`.
Everything inside `with open(...)`.

### Task 2 — JSON round-trip
`json.dump` your per-item survey means to `summary.json` (use `indent=2`), read it back
with `json.load`, and verify `loaded == original`. Open the file in your editor — what
happened to `True`?

### Task 3 — Your own data
Point the pipeline at ANY CSV from your own work (export one from Excel/Sheets if
needed): read it, count the rows, compute one mean, print a two-line report. Note the
first dirty value you hit and how you handled it — into the bug log it goes.

---

## Solutions

### In class

See `demo.py` in this folder — it implements Tasks 1–3 exactly. Key lines:

```python
scores = [int(s["score"]) for s in students]     # convert strings!
statistics.mean(scores)                           # 75.5

by_major = {}
for s in students:
    by_major.setdefault(s["major"], []).append(int(s["score"]))

def to_int(x):
    try: return int(x)
    except (ValueError, TypeError): return None   # handles N/A and ""
```

Trap: opening with `"w"` **truncates the file to empty immediately** — your data is gone
before you ever read it. Use `"r"` (the default) to read.

### In class — going deeper

```python
# Task 1 — inside the loop over survey items
vals = [to_int(r[item]) for r in rows]
good = [v for v in vals if v is not None]
writer.writerow({"item": item,
                 "mean": round(statistics.mean(good), 2),
                 "n_valid": len(good),
                 "pct_valid": f"{100 * len(good) / len(vals):.1f}"})

# Task 2
from pathlib import Path
p = Path("students.csv")
print(p.exists())                      # True (in this folder)
print(p.stat().st_size)                # size in bytes
print(sorted(Path(".").glob("*.csv"))) # every CSV here
```

```python
# Task 3
from pathlib import Path
for p in sorted(Path(".").glob("*.csv")):
    print(f"{p.name:<24}{p.stat().st_size:>8,} bytes")

# Task 4
from datetime import datetime
a = datetime.strptime("2026-01-05", "%Y-%m-%d")
b = datetime.strptime("2026-07-06", "%Y-%m-%d")
print((b - a).days)                    # 182
print(a.strftime("%b %d, %Y"))         # Jan 05, 2026

# Task 5
import csv, random
with open("students.csv", newline="", encoding="utf-8") as f:
    names = [r["name"] for r in csv.DictReader(f)]
random.seed(42)
print(random.sample(names, 3))         # same 3 every run — the seed pins the RNG,
                                       # so your "random" sample is reproducible.

# Task 6
import json
with open("students.csv", newline="", encoding="utf-8") as f:
    rows = [{**r, "score": int(r["score"])} for r in csv.DictReader(f)]
Path("students.json").write_text(json.dumps(rows, indent=2))
# In the file: keys/strings get double quotes, scores sit bare (real JSON numbers).
```

```python
# Task 7 — report.py
import csv, statistics, sys

if len(sys.argv) != 2:                     # argv[0] is report.py itself
    sys.exit("Usage: python3 report.py <file.csv>")

with open(sys.argv[1], newline="", encoding="utf-8") as f:
    scores = [int(r["score"]) for r in csv.DictReader(f)]
print(f"n={len(scores)}  mean={statistics.mean(scores):.1f}")
```

```python
# Task 8
from PIL import Image
from pathlib import Path

a = Image.new("RGB", (60, 60), "steelblue")
b = Image.new("RGB", (60, 60), "goldenrod")
a.save("pulse.gif", save_all=True, append_images=[b], duration=400, loop=0)
print(Path("pulse.gif").stat().st_size, "bytes")   # a few hundred — tiny but real binary
```

### Homework

```python
# Task 1
import csv

with open("attendance.csv", newline="") as f:
    rows = list(csv.DictReader(f))

report = []
for r in rows:
    marks = []
    for key in list(r)[1:]:            # every column after "name"
        try:
            marks.append(int(r[key]))
        except ValueError:
            pass                       # skip the dirty cell — but count it as invalid
    rate = sum(marks) / len(marks) if marks else 0.0
    report.append({"name": r["name"], "rate": round(rate, 2), "n_valid": len(marks)})

with open("attendance_report.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["name", "rate", "n_valid"])
    w.writeheader()
    w.writerows(report)

# Task 2
import json

original = {"q1": 4.2, "q2": 3.8, "all_valid": False}
with open("summary.json", "w") as f:
    json.dump(original, f, indent=2)
with open("summary.json") as f:
    loaded = json.load(f)
print(loaded == original)   # True — and in the file, Python's False is written as
                            # JSON's false (lowercase): JSON is its own language.
```

Task 3 — a pattern, not a fixed answer: `rows = list(csv.DictReader(f))` inside a `with`,
`len(rows)` for the count, one column through a `to_int`/`to_float` cleaner for the mean.
The first dirty value and its exception belong in your bug log.
