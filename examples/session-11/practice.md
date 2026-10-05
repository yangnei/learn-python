# Session 11 — Practice: NumPy & pandas for Research Data

Type each solution yourself. **Predict every output before you run it.** Solutions at the bottom.

## In class

Files provided: `students.csv`, `survey.csv` (the same data as Session 8).
Start every script with `import numpy as np` and `import pandas as pd`.

### Task 1 — Session 8, vectorized
Put the scores `[91, 58, 73, 64, 88, 79]` in a NumPy array. Without a loop, print: the
mean, every score curved by 5 points (capped at 100 with `np.minimum`), and how many
students passed (score >= 60).

### Task 2 — Quiz grid
Build a 3×4 array (3 students, 4 quizzes) of your own numbers. Print each student's mean
and each quiz's mean. Which `axis` gave which? Then print the single highest score and
**which student** got it (`np.argmax` on the right axis).

### Task 3 — Load and look
`pd.read_csv("students.csv")`. Print `.shape`, `.head()`, `.info()`, and
`["score"].describe()`. Compare the mean to your Session 8 hand-computed one.

### Task 4 — Filter and label
Show only Education students scoring under 80. Then add a `grade` column with `pd.cut`
(A ≥ 90, B ≥ 80, C ≥ 70, D ≥ 60, else F) and print the students sorted by score.

### Task 5 — Descriptives by major
With one `groupby(...).agg(...)`, build a table with `n`, `mean_score`, `min_score`,
`max_score` per major, sorted by `mean_score`.

### Trap check
Predict, then run: `np.array([60, 75]) > 70 and np.array([60, 75]) < 90`. What
happens, and what should you write instead?

### Bonus — Pythonic idiom drill
Cover the `# ->` answers, predict each line, then run.

```python
import numpy as np
a = np.array([3, 1, 2])
print(a * 2)                  # -> [6 2 4]        (a list would repeat: [3, 1, 2, 3, 1, 2])
print(a[a > 1])               # -> [3 2]          (mask: keep where True)
print(np.sort(a)[::-1])       # -> [3 2 1]        (sort, then reverse)
print((a > 1).mean())         # -> 0.666...       (share of True values)
```

## In class — going deeper (second hour)

### Task 1 — z-scores by broadcasting
For your quiz grid from Task 2, compute every cell's z-score **within its quiz column**
in one expression. Check that each column's mean is now ~0.

### Task 2 — A view surprise
Make `a = np.arange(5)`, take `b = a[1:3]`, set `b[:] = 0`. Predict `a`. Redo it with
`.copy()` and confirm `a` survives.

### Task 3 — Clean the survey
Read `survey.csv` so that `"N/A"` becomes missing. Print missing values per column, the
mean of each `q*` item, and the number of complete rows. Why did `q2_clarity` become
`float64`?

### Task 4 — Melt it long
Melt the survey to one row per (respondent, item, rating). Produce a table of `mean` and
`count` per item, and a `crosstab` of item × rating.

### Task 5 — Who's above their major?
Add `major_mean` with `groupby(...).transform("mean")`, then list the students who beat
their own major's average.

### Task 6 — Join in advisors
Create `advisors` (Education → Dr. Lee, Psychology → Dr. Okafor). Left-merge it onto the
students with `validate="many_to_one"`. Which students got `NaN`? Re-run with
`indicator=True` to confirm.

### Task 7 — Weekly logins
With `rng = np.random.default_rng(1)`, build 21 days of logins (`pd.date_range` +
`rng.integers(10, 50, size=21)`). Print weekly totals with `resample("W")` and a 3-day
rolling mean.

## Homework (before the capstone)

*~30–45 minutes, outside class — it doesn't count toward class time. Try everything before peeking at the solutions.*

### Task 1 — Rewrite Session 8 in pandas
Take your Session 8 survey summary (per-item mean and `n_valid`, written to
`survey_summary.csv`). Redo it with pandas in **at most six lines**. Diff the two output
files: do the numbers match?

### Task 2 — A simulation
With a seeded generator, simulate 10,000 classes of 30 students whose scores are
`rng.normal(72, 12)` (clip to 0–100). What fraction of classes have a mean **above 75**?
Run it twice with the same seed, then with a different one.

### Task 3 — Your own data
Load a CSV from your own work with `pd.read_csv`. Run `.info()` and `.isna().sum()`,
then produce one `groupby` table you'd put in a paper. Write down every cleaning decision
you made (dropped? imputed? renamed?), because that list *is* part of your methods section.

---

## Solutions

### In class

```python
import numpy as np
import pandas as pd

# Task 1
scores = np.array([91, 58, 73, 64, 88, 79])
print(scores.mean())                      # 75.5
print(np.minimum(scores + 5, 100))        # [96 63 78 69 93 84]
print((scores >= 60).sum())               # 5

# Task 2
q = np.array([[8, 9, 7, 10], [5, 6, 4, 7], [9, 9, 10, 8]])
print(q.mean(axis=1))                     # per student (columns collapse)
print(q.mean(axis=0))                     # per quiz    (rows collapse)
print(q.max(), "by student", q.max(axis=1).argmax())   # 10 by student 0 (first max wins)

# Task 3
students = pd.read_csv("students.csv")
print(students.shape)                     # (6, 3)
students.info()
print(students["score"].describe())       # mean 75.5 — same as Session 8

# Task 4
print(students[(students["major"] == "Education") & (students["score"] < 80)])
students["grade"] = pd.cut(students["score"], bins=[0, 59, 69, 79, 89, 100],
                           labels=["F", "D", "C", "B", "A"])
print(students.sort_values("score", ascending=False))

# Task 5
table = students.groupby("major").agg(
    n=("name", "count"), mean_score=("score", "mean"),
    min_score=("score", "min"), max_score=("score", "max"),
).sort_values("mean_score", ascending=False)
print(table)
```

Trap: `ValueError: The truth value of an array with more than one element is ambiguous`.
`and` needs ONE True/False, but each side is a whole array. Write
`(a > 70) & (a < 90)`, with the parentheses, because `&` binds tighter than `>`.

### In class — going deeper

```python
# Task 1
z = (q - q.mean(axis=0)) / q.std(axis=0)  # (3,4) - (4,) broadcasts down the rows
print(z.mean(axis=0).round(10))           # all zero (a "-0." is still zero)

# Task 2
a = np.arange(5); b = a[1:3]; b[:] = 0
print(a)                                  # [0 0 0 3 4] — b was a view
a = np.arange(5); b = a[1:3].copy(); b[:] = 0
print(a)                                  # [0 1 2 3 4]

# Task 3
survey = pd.read_csv("survey.csv", na_values=["N/A"])
items = [c for c in survey.columns if c.startswith("q")]
print(survey.isna().sum())
print(survey[items].mean().round(2))
print(len(survey.dropna()))               # 6
# q2 has a blank -> NaN, and NaN is a float, so the whole column becomes float64.

# Task 4
long = survey.melt(id_vars="respondent", value_vars=items, var_name="item", value_name="rating")
print(long.groupby("item")["rating"].agg(["mean", "count"]).round(2))
print(pd.crosstab(long["item"], long["rating"]))

# Task 5
students["major_mean"] = students.groupby("major")["score"].transform("mean")
print(students[students["score"] > students["major_mean"]]["name"].tolist())   # ['Ana', 'Eve']

# Task 6
advisors = pd.DataFrame({"major": ["Education", "Psychology"], "advisor": ["Dr. Lee", "Dr. Okafor"]})
joined = students.merge(advisors, on="major", how="left", validate="many_to_one", indicator=True)
print(joined[["name", "major", "advisor", "_merge"]])   # Dev (Sociology) -> NaN, left_only

# Task 7
rng = np.random.default_rng(1)
logins = pd.Series(rng.integers(10, 50, size=21),
                   index=pd.date_range("2026-09-01", periods=21, freq="D"))
print(logins.resample("W").sum())
print(logins.rolling(3).mean().round(1).tail())
```

### Homework

```python
# Task 1 — six lines
survey = pd.read_csv("survey.csv", na_values=["N/A"])
items = [c for c in survey.columns if c.startswith("q")]
out = pd.DataFrame({"item": items,
                    "mean": survey[items].mean().round(2).values,
                    "n_valid": survey[items].count().values})
out.to_csv("survey_summary_pandas.csv", index=False)
print(out)

# Task 2
rng = np.random.default_rng(7)
classes = np.clip(rng.normal(72, 12, size=(10_000, 30)), 0, 100)   # rows = classes
print((classes.mean(axis=1) > 75).mean())   # ~0.08: a class mean above 75 is rare
```

Task 3 is yours: the pattern is `read_csv` → `info()` / `isna().sum()` → clean →
`groupby(...).agg(...)`, plus the written list of decisions.
