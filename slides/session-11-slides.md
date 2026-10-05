---
marp: true
title: "Session 11 — NumPy & pandas for Research Data"
paginate: true
---

# Session 11
## NumPy & pandas for Research Data

---

## Why now? 🧠

In Session 8 you computed a class mean, a mean per major, and per-item survey means
**by hand**: loops, `setdefault`, a `to_int` cleaner. That was the point — you now know
what has to happen underneath.

Today, two libraries do it in a line each:

- **NumPy** — fast arrays of numbers (the engine).
- **pandas** — labeled tables built on NumPy (your spreadsheet, scripted).

```bash
pip install numpy pandas        # preinstalled in Colab and the browser notebook
```

```python
import numpy as np              # the community-standard nicknames
import pandas as pd
```

---

## A list vs an array

```python
scores = [91, 58, 73]
scores * 2                 # [91, 58, 73, 91, 58, 73]   <- a list REPEATS

import numpy as np
arr = np.array([91, 58, 73])
arr * 2                    # array([182, 116, 146])     <- an array MULTIPLIES
arr.dtype, arr.shape       # (dtype('int64'), (3,))
```

A NumPy array holds **one type** in **one block of memory**, and its math runs in
compiled C. It's faster *and* shorter.

```python
np.zeros(3)                # array([0., 0., 0.])
np.arange(0, 10, 2)        # like range(): array([0, 2, 4, 6, 8])
np.linspace(0, 1, 5)       # 5 evenly spaced points, both ends included
```

---

## Vectorization: say what, not how

```python
arr + 5                    # curve every score by 5 points
arr / 100                  # as fractions
arr.mean(), arr.std()      # whole-array statistics
np.sqrt(arr)
```

Session 3 you wrote: `for s in scores: new.append(s + 5)`.
NumPy: `scores + 5`. The loop still happens, just in C, not Python.

⚠️ An integer array stays integer: `np.array([1, 2]) / 2` gives floats, but assigning a
float *into* an int array truncates it.

---

## Boolean masks — the most useful trick

A comparison on an array gives an array of `True`/`False` — use it to **filter**:

```python
scores = np.array([91, 58, 73, 64, 88])
passed = scores >= 60            # array([ True, False,  True,  True,  True])
scores[passed]                   # array([91, 73, 64, 88])
passed.sum()                     # 4 — True counts as 1 (Session 2!)
scores[(scores >= 60) & (scores < 80)]    # & | ~ — and wrap each condition in ()
np.where(scores >= 60, "pass", "fail")    # vectorized if/else
```

⚠️ `and` / `or` on arrays raise **ValueError: truth value … is ambiguous**. Python can't
turn five booleans into one. Use `&`, `|`, `~`.

---

## 2D arrays and `axis`

```python
# rows = students, columns = quizzes
quizzes = np.array([[8, 9, 7, 10],
                    [5, 6, 4, 7],
                    [9, 9, 10, 8]])
quizzes.shape            # (3, 4)
quizzes[1, 2]            # 4 — row 1, column 2
quizzes[0]               # first student's row
quizzes[:, 3]            # every student's quiz 3
quizzes.mean(axis=0)     # one mean PER QUIZ    (collapse the rows)
quizzes.mean(axis=1)     # one mean PER STUDENT (collapse the columns)
```

Memory hook: **`axis` is the dimension that disappears.**

---

## pandas: Series and DataFrame

- **Series** — one labeled column.
- **DataFrame** — a table of Series sharing one row index.

```python
import pandas as pd
students = pd.read_csv("students.csv")   # one line replaces your DictReader loop
students.head()           # first 5 rows
students.shape            # (6, 3)
students.info()           # columns, types, non-null counts — look at this FIRST
students.describe()       # count/mean/std/min/quartiles/max of numeric columns
```

Unlike `csv`, `read_csv` **infers types**: `score` arrives as numbers, not strings.

---

## Selecting

| You want | Write |
|---|---|
| one column (a Series) | `df["score"]` |
| several columns | `df[["name", "score"]]` |
| by **label** | `df.loc[0, "name"]`, `df.loc[0:2, ["name"]]` |
| by **position** | `df.iloc[0, 0]`, `df.iloc[-1]` |

⚠️ `loc` slices **include** the end label; `iloc` slices **exclude** the end position
(like normal Python). `df.loc[0:2]` is 3 rows; `df.iloc[0:2]` is 2.

---

## Filtering rows

Same mask idea as NumPy:

```python
students[students["score"] >= 75]
students[(students["major"] == "Education") & (students["score"] < 80)]
students[students["major"].isin(["Sociology", "Psychology"])]
students.query("score > 70 and major != 'Education'")   # readable alternative
```

---

## New columns, sorting, counting

```python
students["passed"] = students["score"] >= 60
students["grade"] = pd.cut(students["score"], bins=[0, 59, 69, 79, 89, 100],
                           labels=["F", "D", "C", "B", "A"])
students["z"] = (students["score"] - students["score"].mean()) / students["score"].std()

students.sort_values("score", ascending=False)
students["major"].value_counts()          # a Counter for a column
```

Prefer these vectorized forms to `.apply(some_function)`, which runs Python once
per row and gives up the speed.

---

## groupby: split → apply → combine 🧠

Your whole Session 8 by-major loop:

```python
students.groupby("major")["score"].mean()
```

Several statistics with clean column names (**named aggregation**):

```python
students.groupby("major").agg(
    n=("name", "count"),
    mean_score=("score", "mean"),
    best=("score", "max"),
)
```

Research bridge: this is "descriptives by condition", the first table of most
results sections.

---

## Your turn

`examples/session-11/practice.md`:
1. Vectorize Session 8: class mean, curve, pass count with NumPy.
2. Load the students into pandas, filter, add a grade column.
3. `groupby` major: n, mean, max.

---

# Going deeper
## Arrays that bend, tables that reshape

---

## Views vs copies

```python
original = np.array([91, 58, 73, 64])
view = original[:2]       # a slice is a VIEW of the same memory
view[0] = 0
original                  # array([ 0, 58, 73, 64])   <- changed!

safe = original[:2].copy()   # independent
```

Session 2's aliasing, back again: slicing a **list** copies, slicing an **array**
doesn't. (Boolean and list indexing, `arr[mask]`, do return copies.)

---

## Broadcasting

Arrays of different shapes combine when, compared **from the right**, each dimension
is equal or 1. The size-1 dimension stretches.

```python
weights = np.array([0.1, 0.2, 0.3, 0.4])        # (4,)   one weight per quiz
(quizzes * weights).sum(axis=1)                 # (3, 4) * (4,) -> weighted total per student

z = (quizzes - quizzes.mean(axis=0)) / quizzes.std(axis=0)   # z-score every column
```

No loops over rows or columns: the mean row stretches over all the students.

---

## Reproducible randomness

```python
rng = np.random.default_rng(seed=42)    # the modern Generator API
rng.integers(1, 7, size=8)              # dice
rng.normal(loc=70, scale=10, size=5)    # simulated scores
rng.choice(["A", "B"], size=10)         # random assignment to conditions

sums = rng.integers(1, 7, size=(100_000, 2)).sum(axis=1)
(sums == 7).mean()                      # ~0.167, a simulation in two lines
```

Same seed → same numbers → a reproducible methods section (Session 8's lesson, at scale).

---

## Missing data

```python
survey = pd.read_csv("survey.csv", na_values=["N/A"])   # "N/A" and blanks -> NaN
survey.isna().sum()                    # missing per column
survey["q2_clarity"].mean()            # pandas SKIPS NaN (NumPy's .mean() would give nan)
survey.dropna()                        # only complete rows
survey.fillna(survey.median(numeric_only=True))   # impute with column medians
```

⚠️ One missing value turns an int column into **float64**, because NaN is a float.
Your 1–5 Likert column now prints `4.0`.

Whether you drop or impute is a **methods decision**: report it.

---

## transform: group stats on every row

`agg` shrinks to one row per group; `transform` keeps the original shape:

```python
students["major_mean"] = students.groupby("major")["score"].transform("mean")
students["vs_major"] = students["score"] - students["major_mean"]
```

"How far is each student from their major's average?", with no merge needed.

---

## Reshaping: wide ↔ long

Survey exports are **wide** (one column per item). Most analysis wants **long**
(one row per answer):

```python
long = survey.melt(id_vars="respondent", var_name="item", value_name="rating")
long.groupby("item")["rating"].agg(["mean", "count"])
pd.crosstab(long["item"], long["rating"])        # frequency table: 1s, 2s, ... per item

students.pivot_table(index="major", columns="passed", values="score",
                     aggfunc="count", fill_value=0)   # long -> wide summary
```

---

## merge: joining tables

```python
advisors = pd.DataFrame({"major": ["Education", "Psychology", "History"],
                         "advisor": ["Dr. Lee", "Dr. Okafor", "Dr. Ruiz"]})
students.merge(advisors, on="major", how="left", validate="many_to_one")
```

| `how=` | keeps |
|---|---|
| `"inner"` (default) | keys in both |
| `"left"` | every left row (missing matches → NaN) |
| `"outer"` | everything |

`validate=` catches accidental duplicate keys; `indicator=True` adds a `_merge`
column showing where each row came from. Use both when a join "loses" rows.

---

## Dates and time series

```python
logins["day"] = pd.to_datetime(logins["day"])   # or read_csv(..., parse_dates=["day"])
logins["day"].dt.day_name()                     # .dt = date tools for a column
weekly = logins.set_index("day")["logins"].resample("W").sum()   # per-week totals
logins["logins"].rolling(7).mean()              # 7-day moving average
```

`.str` does the same for text columns: `df["name"].str.upper()`,
`.str.contains("ED")`, `.str.strip()`.

---

## Method chaining

Each step returns a new DataFrame, so an analysis reads top to bottom:

```python
report = (
    students
    .query("passed")
    .groupby("major", as_index=False)
    .agg(n=("name", "count"), mean_score=("score", "mean"))
    .sort_values("mean_score", ascending=False)
)
report.to_csv("report.csv", index=False)
```

---

## The one assignment rule ⚠️

```python
students[students["score"] < 60]["grade"] = "D"      # ✗ edits a temporary copy
students.loc[students["score"] < 60, "grade"] = "D"  # ✓ one .loc: rows, column
```

The first line filters into a **copy**, then sets a value on that copy, so `students`
never changes (pandas warns). Always change values with a single `.loc[rows, col]`.

---

## Your turn (deeper)

`examples/session-11/practice.md`, **In class — going deeper**: z-scores by
broadcasting, clean the survey's missing values, melt it long, merge in advisors,
and a weekly resample.

---

## Trap recap

- A list `* 2` repeats; an array `* 2` multiplies.
- `and`/`or` on arrays → ValueError; use `&`/`|`/`~` with parentheses.
- An array slice is a **view**; `.copy()` when you need independence.
- One NaN turns an int column into floats.
- `loc` slices include the end; `iloc` slices don't.
- Change values with one `.loc[rows, col]`, never `df[mask]["col"] = ...`.

## Summary
Everything you did by hand in Session 8 is now a line or two, and you know what each
line does underneath.
**Next (optional):** the capstone. Build it with pandas if you like.

---

## Homework (before the capstone)

*Outside class — doesn't count toward class time. Full tasks + solutions:
`examples/session-11/practice.md` → **Homework**.*

1. **Rewrite Session 8 in pandas.** The survey summary in six lines; diff the outputs.
2. **A simulation.** 10,000 seeded classes: how often is the mean above 75?
3. **Your own data.** One publishable `groupby` table, plus your list of cleaning decisions.
