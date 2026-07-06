---
marp: true
title: "Session 8 — Files, Libraries & Research Data"
paginate: true
---

# Session 8
## Files, Libraries & Research Data

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

```python
with open("log.txt", "a") as f:       # append: adds to the end, never clobbers
    f.write("cleaned survey.csv\n")   # \n is YOUR job when writing
```

(`"rb"`/`"wb"` read/write **binary** — images, PDFs. Text mode is the default.)

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

You *could* split each line yourself with `.split(",")` — until a field contains a
comma. That, plus quoting and headers, is why `csv` exists.

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

```python
# pip install cowsay          # PyPI hosts ~half a million packages
import cowsay
cowsay.cow("pip install anything")
```

`pip install <name>`, then `import` — that's the whole third-party story. (Yes,
even silly ones: the point is that installing is trivial.)

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

# Going deeper
## Real data work

---

## `pathlib`, the full tour

```python
from pathlib import Path
data = Path("data")
f = data / "students.csv"          # / joins paths, any OS
f.exists(), f.stat().st_size       # is it there? how big?
list(data.glob("*.csv"))           # every CSV here
list(data.rglob("*.csv"))          # ...and in every subfolder
data.mkdir(exist_ok=True)
notes = f.with_suffix(".txt").read_text()   # small files: one-liners
```

---

## Encodings — the Excel gotcha

```python
open("survey.csv", newline="", encoding="utf-8")        # say it explicitly
open("from_excel.csv", newline="", encoding="utf-8-sig") # eats Excel's BOM
```

- Mojibake (`Ã©` for `é`) = the bytes were read with the wrong encoding.
- Excel often saves `cp1252` or UTF-8 *with a BOM* — `utf-8-sig` handles the latter.

---

## `csv`, round 2

```python
csv.reader(f)        # rows as LISTS (no/duplicate headers)
csv.DictReader(f)    # rows as DICTS (the default choice)
w.writerows(report)  # write many dicts at once
csv.DictReader(f, delimiter=";")   # European Excel exports
```

---

## JSON for nested data

```python
import json
snapshot = {"course": "ED101",
            "items": {"q1": {"mean": 4.2, "n": 28}, "q2": {"mean": 3.8, "n": 27}}}
Path("snapshot.json").write_text(json.dumps(snapshot, indent=2))
back = json.loads(Path("snapshot.json").read_text())
```

CSV is a rectangle; JSON nests. `True/None` become `true/null` — JSON is its own language,
`json.load` translates back.

---

## APIs: the same JSON, from the web *(a taste)*

```python
# pip install requests
import requests

r = requests.get("https://itunes.apple.com/search",
                 params={"term": "python", "media": "ebook", "limit": 3})
data = r.json()                     # the response body, parsed into dicts/lists
for item in data["results"]:
    print(item["trackName"])
```

An "API call" is just: fetch a URL, parse the JSON — the same `json` skills, new
source. (Needs internet; this course stays with offline files.)

---

## `datetime` — dates are data too

```python
from datetime import date, datetime
d = datetime.strptime("2026-07-06", "%Y-%m-%d")   # parse text -> datetime
d.strftime("%b %d")                                # format -> "Jul 06"
(date(2026, 7, 6) - date(2026, 1, 5)).days         # 182 — date math works
date.fromisoformat("2026-07-06")                   # the ISO shortcut
```

`strptime` = *parse* (string → date), `strftime` = *format* (date → string).

---

## `random`, reproducibly

```python
import random
random.seed(42)                 # same "random" every run — methods sections rejoice
random.choice(roster)           # one
random.sample(roster, 3)        # three, no repeats
random.shuffle(order)           # in place — random assignment
```

Seeding makes stochastic analysis **reproducible** — rerunning your script re-draws the
same sample.

---

## Scripts that take arguments: `sys.argv`

```python
# report.py — run as:  python3 report.py survey.csv
import sys

if len(sys.argv) != 2:                    # argv[0] is the script's own name
    sys.exit("Usage: python3 report.py <file.csv>")
filename = sys.argv[1]
```

- `sys.argv` is a plain **list of strings** from the command line — `len()` it, slice it
  (`sys.argv[1:]` = just the real arguments).
- Guard first, then trust: a missing argument is an `IndexError` waiting to happen;
  `sys.exit("message")` stops the program and prints the usage line.
- When flags multiply (`--top 5 --verbose`), graduate to the stdlib's `argparse`.

---

## Binary files in practice: images with Pillow

```python
# pip install pillow
from PIL import Image

before = Image.open("chart_2025.png")     # a binary file, decoded into pixels
after = Image.open("chart_2026.png")
before.save("growth.gif", save_all=True,
            append_images=[after],        # more frames -> an animated GIF
            duration=500, loop=0)         # ms per frame; 0 = loop forever
```

- Text mode decodes bytes into characters; **binary** formats (images, PDFs) need a
  library that speaks them — for images, that's Pillow.
- Three calls = an animated before/after of your results chart for a slide deck.

---

## The pandas teaser, extended

```python
import pandas as pd
df = pd.read_csv("students.csv")
df["score"].describe()                    # count/mean/std/quartiles
df.groupby("major")["score"].agg(["mean", "count"])
df[df["score"] < 60]                      # filter rows
df.to_csv("report.csv", index=False)
```

Five lines = today's whole session. That's the next course — and now you know what each
line does underneath.

---

## Your turn — round 2

`examples/session-08/practice.md` → **In class — going deeper**:
a `pathlib` inventory, date math on enrollment dates, a seeded sample, and CSV → JSON.
---

## Traps recap

- `"w"` silently overwrites — be sure of the filename.
- `csv` module → open with `newline=""`.
- Files exhaust after one read; re-open to re-read.
- Specify `encoding="utf-8"` for non-ASCII text.

## Summary
You can load, summarize, and write real research data.
**Next:** Session 9 — regular expressions & text cleaning.

---

## Homework (before Session 9)

*Outside class — it doesn't count toward class time. Full specs + solutions: `examples/session-08/practice.md` → **Homework**.*

1. **Attendance report** — read a CSV, clean it, summarize it, write a report CSV — the whole pipeline.
2. **JSON round-trip** — save your summary with `json.dump`, load it back, verify equality.
3. **Your own data** — point the pipeline at any CSV from your research.
