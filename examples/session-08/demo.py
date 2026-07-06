"""Session 8 demo — Files, Libraries & Research Data.

Run me:  python3 demo.py
Predict each printed line BEFORE you run.
"""

import csv
import json
import statistics
from collections import Counter
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
print("majors tally:", Counter(s["major"] for s in students))   # quick frequency count

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

# --- 4. JSON: serialize a Python object to text and back ----------------
snapshot = {"n": len(students), "mean": statistics.mean(scores), "by_major": major_means}
(HERE / "snapshot.json").write_text(json.dumps(snapshot, indent=2))   # pathlib write
restored = json.loads((HERE / "snapshot.json").read_text())           # pathlib read
print("\nJSON round-trip ok?", restored == snapshot)

# --- 5. Survey: per-item means, skipping dirty values -------------------
def to_int(x):
    try:
        return int(x)
    except (ValueError, TypeError):
        return None        # handles "N/A" and "" (Session 7's move)

with open(HERE / "survey.csv", newline="") as f:
    rows = list(csv.DictReader(f))

items = [c for c in rows[0] if c != "respondent"]
item_means = {}
for item in items:
    vals = [to_int(r[item]) for r in rows]
    vals = [v for v in vals if v is not None]      # drop missing
    item_means[item] = round(statistics.mean(vals), 2)
print("\nper-item survey means:", item_means)

# Two files open at once in a single `with` (read source, write report together):
with open(HERE / "survey.csv", newline="") as src, \
     open(HERE / "survey_summary.csv", "w", newline="") as out:
    rows = list(csv.DictReader(src))
    w = csv.DictWriter(out, fieldnames=["item", "mean", "n_valid"])
    w.writeheader()
    for item in items:
        valid = [to_int(r[item]) for r in rows if to_int(r[item]) is not None]
        w.writerow({"item": item, "mean": round(statistics.mean(valid), 2),
                    "n_valid": len(valid)})
print("wrote survey_summary.csv")

# --- 6. pathlib: discover files without hard-coding names ---------------
csvs = sorted(p.stem for p in HERE.glob("*.csv"))   # .stem = filename without extension
print("\nCSV files here:", csvs)

# ==========================================================================
# GOING DEEPER — second-hour material
# ==========================================================================
# --- deeper 1: csv.reader vs DictReader -------------------------------------------
print("\n=== GOING DEEPER ===")
with open(HERE / "students.csv", newline="", encoding="utf-8") as f:
    first_rows = list(csv.reader(f))[:2]
print("csv.reader gives LISTS:", first_rows)   # row 0 is the header itself

# --- deeper 2: datetime — dates are data too ---------------------------------------
from datetime import date, datetime
enrolled = datetime.strptime("2026-01-05", "%Y-%m-%d").date()
today = date(2026, 7, 6)
print("enrolled:", enrolled.strftime("%b %d, %Y"), "->", (today - enrolled).days, "days ago")

# --- deeper 3: random, reproducibly -------------------------------------------------
import random
random.seed(42)                          # same "random" numbers every run
names = ["Ana", "Ben", "Cara", "Dev", "Eve"]
print("reproducible sample of 2:", random.sample(names, 2))
random.seed(42)
print("run it again, same seed :", random.sample(names, 2))

# --- deeper 4: scripts that take arguments (sys.argv) ------------------------
import sys
print("this run saw sys.argv =", sys.argv[:2], "...")   # [0] is always the script itself

def pick_input(argv, default="survey.csv"):
    """The filename from the command line, a default if none, a usage exit if garbage."""
    if len(argv) > 2:
        sys.exit("Usage: python3 report.py [file.csv]")
    return argv[1] if len(argv) == 2 else default

for fake in (["report.py"], ["report.py", "grades.csv"]):
    print(fake, "->", pick_input(fake))       # a plain function -> easy to test (S7!)
try:
    pick_input(["report.py", "a", "b"])
except SystemExit as e:
    print("too many args ->", e)              # sys.exit raises SystemExit with the message

# --- deeper 5: binary files — a tiny animated GIF with Pillow -----------------
try:
    from PIL import Image
    frame_a = Image.new("RGB", (60, 60), "steelblue")   # two frames, generated in memory
    frame_b = Image.new("RGB", (60, 60), "goldenrod")
    frame_a.save(HERE / "pulse.gif", save_all=True, append_images=[frame_b],
                 duration=400, loop=0)
    print("wrote pulse.gif:", (HERE / "pulse.gif").stat().st_size, "bytes of pure binary")
except ImportError:
    print("Pillow not installed — `pip install pillow` to run the GIF demo")

# --- deeper 6: pip's half-million packages, e.g. cowsay ------------------------
try:
    import cowsay
    cowsay.cow("pip install anything")
except ImportError:
    print("cowsay not installed — `pip install cowsay` for the full moo")
