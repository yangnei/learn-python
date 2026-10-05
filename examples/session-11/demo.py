"""Session 11 demo — NumPy & pandas for Research Data.

Run me:  python3 demo.py        (needs:  pip install numpy pandas)
Predict each printed line BEFORE you run.

The data is the same students + survey you cleaned by hand in Session 8 — written
inline here so the demo runs anywhere (a real script would call pd.read_csv("file.csv")).
"""

from io import StringIO

import numpy as np
import pandas as pd

pd.set_option("display.width", 120)

STUDENTS_CSV = """name,major,score
Ana,Education,91
Ben,Psychology,58
Cara,Education,73
Dev,Sociology,64
Eve,Psychology,88
Finn,Education,79
"""

SURVEY_CSV = """respondent,q1_engagement,q2_clarity,q3_workload,q4_support
R01,5,4,2,5
R02,4,4,3,4
R03,3,5,N/A,4
R04,5,5,1,5
R05,2,3,4,2
R06,4,,3,4
R07,5,4,2,5
R08,1,2,5,1
"""

# --- 1. NumPy arrays: one type, one block of memory -----------------------
scores = np.array([91, 58, 73, 64, 88, 79])
print("array:", scores, "| dtype:", scores.dtype, "| shape:", scores.shape)
print("zeros:", np.zeros(3), "| arange:", np.arange(0, 10, 2), "| linspace:", np.linspace(0, 1, 5))

# --- 2. Vectorized math: no loop needed ----------------------------------
print("curved +5:   ", scores + 5)                 # every element at once
print("as fraction: ", scores / 100)
print("list * 2:    ", [91, 58] * 2)               # a LIST repeats...
print("array * 2:   ", np.array([91, 58]) * 2)     # ...an ARRAY multiplies
print("mean / std:  ", scores.mean(), round(scores.std(), 2))

# --- 3. Boolean masks: filter with a condition ---------------------------
passed = scores >= 60
print("mask:        ", passed)
print("passing:     ", scores[passed])
print("how many:    ", passed.sum())               # True counts as 1 (Session 2!)
print("60s and 70s: ", scores[(scores >= 60) & (scores < 80)])   # & not `and`, parentheses required
print("labels:      ", np.where(scores >= 60, "pass", "fail"))  # vectorized if/else

# --- 4. 2D arrays and the axis argument ---------------------------------
# rows = 3 students, columns = 4 quizzes
quizzes = np.array([[8, 9, 7, 10],
                    [5, 6, 4, 7],
                    [9, 9, 10, 8]])
print("\nshape:", quizzes.shape)
print("one cell [1, 2]:", quizzes[1, 2])
print("student 0's row:", quizzes[0])
print("quiz 3 column:  ", quizzes[:, 3])
print("per quiz (axis=0):   ", quizzes.mean(axis=0))   # collapse rows -> one value per column
print("per student (axis=1):", quizzes.mean(axis=1))   # collapse columns -> one value per row

# --- 5. pandas: load and inspect a DataFrame -----------------------------
students = pd.read_csv(StringIO(STUDENTS_CSV))
print()
print(students.head(3))
print("shape:", students.shape, "| columns:", list(students.columns))
print(students["score"].describe().round(1))       # count, mean, std, min, quartiles, max

# --- 6. Selecting: columns, loc (labels), iloc (positions) ----------------
print(students["name"].tolist())                   # one column -> Series
print(students[["name", "score"]].head(2))         # list of columns -> DataFrame
print("loc[0, 'name']:", students.loc[0, "name"])
print(students.iloc[-1])                           # last row, by position

# --- 7. Filtering rows -----------------------------------------------------
print(students[students["score"] >= 75])
print(students[(students["major"] == "Education") & (students["score"] < 80)])
print(students[students["major"].isin(["Sociology", "Psychology"])]["name"].tolist())
print(students.query("score > 70 and major != 'Education'"))

# --- 8. New columns, sorting, counting ------------------------------------
students["passed"] = students["score"] >= 60
students["grade"] = pd.cut(students["score"], bins=[0, 59, 69, 79, 89, 100],
                           labels=["F", "D", "C", "B", "A"])
students["z"] = ((students["score"] - students["score"].mean()) / students["score"].std()).round(2)
print(students.sort_values("score", ascending=False))
print(students["major"].value_counts())

# --- 9. groupby: Session 8's by-hand loop, in one line ---------------------
print(students.groupby("major")["score"].mean().round(1))
summary = students.groupby("major").agg(
    n=("name", "count"),
    mean_score=("score", "mean"),
    best=("score", "max"),
)
print(summary.round(1).sort_values("mean_score", ascending=False))

# ============================== GOING DEEPER ==============================
print("\n--- GOING DEEPER ---")

# --- deeper 1: views vs copies ----------------------------------------------
original = np.array([91, 58, 73, 64])
view = original[:2]          # a slice is a VIEW of the same memory
view[0] = 0
print("after editing the slice:", original)        # original changed!
safe = original[2:].copy()   # .copy() when you need independence
safe[0] = 99
print("after editing a copy:   ", original, "<- the 73 is untouched")

# --- deeper 2: broadcasting -------------------------------------------------
# Shapes line up from the right; a size-1 (or missing) dimension stretches.
weights = np.array([0.1, 0.2, 0.3, 0.4])                # shape (4,) -> stretched over 3 rows
print("weighted totals:", (quizzes * weights).sum(axis=1).round(2))
z = (quizzes - quizzes.mean(axis=0)) / quizzes.std(axis=0)   # z-score every column at once
print("column z-scores:\n", z.round(2))

# --- deeper 3: reproducible random numbers -----------------------------------
rng = np.random.default_rng(seed=42)               # same seed -> same numbers (methods sections!)
print("dice:", rng.integers(1, 7, size=8))
sim = rng.integers(1, 7, size=(100_000, 2)).sum(axis=1)
print("P(two dice sum to 7) ~", round((sim == 7).mean(), 3), "(exact: 0.167)")

# --- deeper 4: missing data -------------------------------------------------
survey = pd.read_csv(StringIO(SURVEY_CSV), na_values=["N/A"])   # treat "N/A" as missing
print(survey.isna().sum())                         # missing per column
print("q2 dtype:", survey["q2_clarity"].dtype)     # float64: a NaN turns an int column into floats
items = [c for c in survey.columns if c.startswith("q")]
print(survey[items].mean().round(2))               # pandas skips NaN by default
print("rows complete:", len(survey.dropna()), "of", len(survey))
filled = survey.fillna(survey[items].median())     # or impute with each column's median
print(filled.loc[[2, 5]])

# --- deeper 5: transform — group stats aligned to every row -----------------
students["major_mean"] = students.groupby("major")["score"].transform("mean").round(1)
students["vs_major"] = students["score"] - students["major_mean"]
print(students[["name", "major", "score", "major_mean", "vs_major"]])

# --- deeper 6: reshape — melt (wide -> long) and pivot_table ----------------
long = survey.melt(id_vars="respondent", value_vars=items, var_name="item", value_name="rating")
print(long.head())
print(long.groupby("item")["rating"].agg(["mean", "count"]).round(2))
print(pd.crosstab(long["item"], long["rating"]))   # how many 1s, 2s, ... per item
print(students.pivot_table(index="major", columns="passed", values="score",
                           aggfunc="count", fill_value=0))

# --- deeper 7: merge — join two tables on a key ------------------------------
advisors = pd.DataFrame({"major": ["Education", "Psychology", "History"],
                         "advisor": ["Dr. Lee", "Dr. Okafor", "Dr. Ruiz"]})
joined = students.merge(advisors, on="major", how="left", validate="many_to_one")
print(joined[["name", "major", "advisor"]])        # Sociology has no advisor -> NaN
check = students[["major"]].drop_duplicates().merge(advisors, on="major", how="outer", indicator=True)
print(check)                                       # _merge shows where each key came from

# --- deeper 8: dates and time series ----------------------------------------
logins = pd.DataFrame({
    "day": pd.date_range("2026-09-01", periods=28, freq="D"),
    "logins": rng.integers(20, 60, size=28),
})
logins["weekday"] = logins["day"].dt.day_name()
weekly = logins.set_index("day")["logins"].resample("W").sum()
print(weekly)                                      # weeks end on Sunday; the last one is partial
logins["avg_7d"] = logins["logins"].rolling(7).mean().round(1)
print(logins.tail(3))

# --- deeper 9: method chaining + the one assignment rule ---------------------
report = (
    students
    .query("passed")
    .groupby("major", as_index=False)
    .agg(n=("name", "count"), mean_score=("score", "mean"))
    .sort_values("mean_score", ascending=False)
    .round(1)
)
print(report)

# Change values through ONE .loc call — never df[mask]["col"] = ... (that edits a copy)
students.loc[students["score"] < 60, "grade"] = "D"   # a regrade: the F becomes a D
print(students[["name", "score", "grade"]])
print(students.to_csv(index=False)[:80], "...")     # to_csv("file.csv", index=False) writes a file
