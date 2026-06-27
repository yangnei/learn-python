# Session 8 — Practice (25 min)

Files provided: `students.csv`, `survey.csv`.

## Task 1 — Read & summarize students
Read `students.csv` with `csv.DictReader`. Remember the values are **strings** — convert
`score` to `int`. Print the class mean and median with the `statistics` module.

## Task 2 — Mean by major
Build `{major: mean_score}`. (Hint: `dict.setdefault(key, []).append(...)`.)

## Task 3 — Clean & summarize the survey
`survey.csv` has `"N/A"` and blanks in numeric columns. For each `q*` item, compute the
mean of the **valid** values only, and how many were valid. Write `survey_summary.csv`
with columns `item,mean,n_valid`.

## Task 4 — pandas teaser (optional)
If `pandas` is installed: `pd.read_csv("students.csv")["score"].describe()`. Compare the
mean to your hand-computed one.

## Trap check
What happens if you accidentally open `students.csv` with mode `"w"` before reading it?

---
## Solutions
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
