"""Session 6 demo — Recursion & Recursive Thinking.

Run me:  python3 demo.py
Predict each printed line BEFORE you run.
"""

import functools
import sys

# 1) The shape of EVERY recursion: a BASE CASE that stops + a RECURSIVE CASE
#    that moves toward it. Real example: how many prerequisites deep is a course?
prereq_of = {
    "ED700": "ED600",    # to take ED700 you must first pass ED600,
    "ED600": "ED500",    #   which needs ED500,
    "ED500": "ED400",    #   which needs ED400,
    "ED400": None,       #   which has no prerequisite — the base case
}

def prereqs_deep(course):
    earlier = prereq_of[course]
    if earlier is None:                 # BASE CASE — nothing comes before it
        return 0
    return 1 + prereqs_deep(earlier)    # RECURSIVE CASE — step back one course

print("ED700 prerequisite depth:", prereqs_deep("ED700"))   # 3


# 2) Recursion vs iteration: how many distinct ways can n students finish a
#    race? That is n! (n factorial). Same answer two ways; the loop is clearer.
def orderings(n):
    if n <= 1:                          # base case: 0 or 1 student -> one order
        return 1
    return n * orderings(n - 1)         # <- you MUST return the recursive call

def orderings_loop(n):
    total = 1
    for k in range(2, n + 1):
        total *= k
    return total

print("\nways to rank 5 students:", orderings(5), "==", orderings_loop(5))   # 120


# 3) Memoization: @lru_cache remembers past results so each input is computed
#    once. A value built from smaller copies of itself — here a growth model,
#    the Fibonacci sequence — otherwise recomputes the same subtotals exponentially.
calls = 0
def growth_naive(week):
    global calls
    calls += 1
    return week if week < 2 else growth_naive(week - 1) + growth_naive(week - 2)

@functools.lru_cache(maxsize=None)      # one line turns the slow version fast
def growth_fast(week):
    return week if week < 2 else growth_fast(week - 1) + growth_fast(week - 2)

print("\ngrowth_naive(30):", growth_naive(30), "in", calls, "calls")
print("growth_fast(30): ", growth_fast(30), "->", growth_fast.cache_info())
# The same @lru_cache speeds up ANY expensive repeated call — a slow file
# parse, a web lookup, a database query.


# 4) Where recursion SHINES: naturally NESTED data, where one loop can't reach
#    all the way down. This is shaped like a real nested-JSON survey export.
export = {
    "cohort": "2026",
    "students": [
        {"name": "Ana", "scores": [91, 88]},
        {"name": "Ben", "scores": [58, [60, 64]]},   # arbitrarily nested
    ],
}

def deep_sum(obj):
    """Add up every number found anywhere inside nested lists/dicts."""
    if isinstance(obj, bool):                 # bool is an int subclass (Session 1!)
        return 0
    if isinstance(obj, (int, float)):
        return obj
    if isinstance(obj, dict):
        return sum(deep_sum(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return sum(deep_sum(x) for x in obj)
    return 0                                  # strings, None, etc. contribute nothing

print("\ndeep_sum of nested export:", deep_sum(export))   # 91+88+58+60+64 = 361


# 5) The trap: with no reachable base case, recursion never stops. Python has no
#    tail-call optimization, so it just piles up stack frames until it gives up.
print("\nPython's recursion limit:", sys.getrecursionlimit())

def runaway(n):
    return runaway(n + 1)        # BUG: never reaches a base case

try:
    runaway(0)
except RecursionError:
    print("RecursionError: maximum recursion depth exceeded (as expected)")

# ==========================================================================
# GOING DEEPER — second-hour material
# ==========================================================================
# --- deeper 1: divide & conquer — binary search -------------------------------
print("\n=== GOING DEEPER ===")
def find(sorted_names, target, lo=0, hi=None, depth=0):
    if hi is None:
        hi = len(sorted_names)
    if lo >= hi:
        return False
    mid = (lo + hi) // 2
    print("  " * depth + f"looking at {sorted_names[mid]!r}")
    if sorted_names[mid] == target:
        return True
    if sorted_names[mid] < target:
        return find(sorted_names, target, mid + 1, hi, depth + 1)
    return find(sorted_names, target, lo, mid, depth + 1)

roster = sorted(["Ana", "Ben", "Cara", "Dev", "Eve", "Fay", "Gus"])
print("found Fay?", find(roster, "Fay"), "— each step HALVES the problem")

# --- deeper 2: tree-shaped data ------------------------------------------------
org = {"name": "Dean", "reports": [
    {"name": "Chair A", "reports": []},
    {"name": "Chair B", "reports": [{"name": "Prof C", "reports": []}]},
]}

def count_people(node):
    return 1 + sum(count_people(r) for r in node["reports"])

print("people in the org tree:", count_people(org))

# --- deeper 3: same logic, no recursion — an explicit stack ---------------------
def flatten_iter(xs):
    out, to_visit = [], list(xs)
    while to_visit:
        x = to_visit.pop(0)
        if isinstance(x, list):
            to_visit = x + to_visit     # unpack in place, keep order
        else:
            out.append(x)
    return out

print("flatten_iter:", flatten_iter([1, [2, [3, 4]], 5]), "— depth 10,000? no problem")
