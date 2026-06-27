"""
Session 8 — Files, Libraries & Research Data
Run me from this folder:  python3 demo.py
Reads students.csv and survey.csv; writes summary CSVs.
"""
import csv
import statistics
from pathlib import Path

HERE = Path(__file__).parent     # so it works no matter where you run it

# --- 1. Read a CSV into a list of dicts ---------------------------------
with open(HERE / "students.csv", newline="") as f:
    students = list(csv.DictReader(f))   # each row is a dict keyed by header

print("rows read:", len(students))
print("first row:", students[0])

# CSV values are STRINGS — convert numbers (recall Session 1!)
scores = [int(s["score"]) for s in students]
print("class mean:", statistics.mean(scores))
print("class stdev:", round(statistics.stdev(scores), 2))

# --- 2. Group by major, mean score -------------------------------------
by_major = {}
for s in students:
    by_major.setdefault(s["major"], []).append(int(s["score"]))
major_means = {m: round(statistics.mean(v), 1) for m, v in by_major.items()}
print("means by major:", major_means)

# --- 3. Write a summary CSV --------------------------------------------
with open(HERE / "students_summary.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["major", "mean_score", "n"])
    w.writeheader()
    for major, vals in by_major.items():
        w.writerow({"major": major, "mean_score": round(statistics.mean(vals), 1),
                    "n": len(vals)})
print("wrote students_summary.csv")

# --- 4. Survey: per-item means, skipping dirty values -------------------
def to_int(x):
    try:
        return int(x)
    except (ValueError, TypeError):
        return None        # handles "N/A" and "" (Session 7)

with open(HERE / "survey.csv", newline="") as f:
    rows = list(csv.DictReader(f))

items = [c for c in rows[0] if c != "respondent"]
item_means = {}
for item in items:
    vals = [to_int(r[item]) for r in rows]
    vals = [v for v in vals if v is not None]      # drop missing
    item_means[item] = round(statistics.mean(vals), 2)
print("\nper-item survey means:", item_means)

with open(HERE / "survey_summary.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["item", "mean", "n_valid"])
    w.writeheader()
    for item in items:
        valid = [to_int(r[item]) for r in rows if to_int(r[item]) is not None]
        w.writerow({"item": item, "mean": round(statistics.mean(valid), 2),
                    "n_valid": len(valid)})
print("wrote survey_summary.csv")
