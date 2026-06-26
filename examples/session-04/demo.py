"""
Session 4 — Data Structures: list, tuple, dict, set
Run me:  python3 demo.py
"""
import copy

# --- 1. A list of dicts is a tidy dataset -------------------------------
roster = [
    {"name": "Ana",  "score": 91},
    {"name": "Ben",  "score": 58},
    {"name": "Cara", "score": 73},
    {"name": "Dev",  "score": 64},
]

# --- 2. Slicing ----------------------------------------------------------
xs = [10, 20, 30, 40]
print("xs[1:3]:", xs[1:3], "| xs[-1]:", xs[-1], "| xs[::-1]:", xs[::-1])

# --- 3. Sorting by a key ------------------------------------------------
top = sorted(roster, key=lambda s: s["score"], reverse=True)
print("\nRanked:", [s["name"] for s in top])

# --- 4. Comprehensions ---------------------------------------------------
name_to_score = {s["name"]: s["score"] for s in roster}      # dict comp
passers = [s["name"] for s in roster if s["score"] >= 60]    # filtered list
print("map:", name_to_score)
print("passers:", passers)

# --- 5. Grouping into buckets -------------------------------------------
buckets = {"pass": [], "fail": []}
for s in roster:
    key = "pass" if s["score"] >= 60 else "fail"
    buckets[key].append(s["name"])
print("buckets:", buckets)

# --- 6. Sets: dedup survey answers --------------------------------------
answers = ["yes", "no", "yes", "maybe", "no"]
print("\ndistinct answers:", set(answers))

# --- 7. TRAP: aliasing ---------------------------------------------------
a = [1, 2, 3]
b = a                 # alias — SAME list
a.append(4)
print("\nalias b:", b)          # [1, 2, 3, 4]  (changed!)

c = a.copy()          # independent shallow copy
a.append(5)
print("copy c:", c)             # [1, 2, 3, 4]  (unaffected)

# Nested data needs deepcopy:
grid_bad = [[0] * 3] * 3        # 3 refs to ONE row
grid_bad[0][0] = 9
print("shared-row grid:", grid_bad)   # [[9,0,0],[9,0,0],[9,0,0]]  😱
grid_ok = [[0] * 3 for _ in range(3)]
grid_ok[0][0] = 9
print("independent grid:", grid_ok)   # [[9,0,0],[0,0,0],[0,0,0]]
