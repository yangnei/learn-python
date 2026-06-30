"""
Session 3 — Functions, Scope & Recursion
Run me:  python3 demo.py
Two halves — (A) Functions, Scope & Reusability; (B) Recursion & Recursive Thinking.
Predict each block, then run it.
"""

# ======================================================================
# PART A — Functions, Scope & Reusability
# ======================================================================

import functools

# --- 1. return vs print --------------------------------------------------
def avg(xs: list[float]) -> float:
    """Return the mean of xs."""
    return sum(xs) / len(xs)

def show(xs):
    print("mean is", sum(xs) / len(xs))

x = avg([1, 2, 3])      # 2.0  (a value we can keep using)
y = show([1, 2, 3])     # prints, but...
print("x =", x, "| y =", y)     # y is None!

# --- 2. defaults, *args, **kwargs ---------------------------------------
def grade(score, scale=100, passing=60):
    pct = score / scale
    return "PASS" if score >= passing else "FAIL", round(pct, 3)

print(grade(85), grade(40, passing=35))
print("via **dict:", grade(**{"score": 85, "passing": 80}))  # ** unpacks a dict into kwargs

def total(*args):              # collect positionals into a tuple
    return sum(args)
print("total:", total(1, 2, 3, 4))

def tag(**kwargs):             # collect keywords into a dict
    return kwargs
print("tag:", tag(name="Ana", gpa=3.9))

scores = [91, 58, 73]
print("unpacked into total:", total(*scores))   # * unpacks the list

# --- 3. Keyword-only arguments (everything after * must be named) -------
def report(name, *, verbose=False):    # `verbose` can't be passed positionally
    return f"{name} (full report)" if verbose else name
print("\n", report("Ana", verbose=True))
# report("Ana", True)   # would raise TypeError — that's the point: clarity at the call site

# --- 4. A decorator: a function that wraps another function -------------
def announce(func):
    @functools.wraps(func)            # keep func's name/docstring on the wrapper
    def wrapper(*args, **kwargs):     # *args/**kwargs forward ANY signature
        print(f"  calling {func.__name__}{args}")
        return func(*args, **kwargs)
    return wrapper

@announce                              # sugar for:  add = announce(add)
def add(a, b):
    return a + b

print("\ndecorated:", add(2, 3))

# --- 5. Closures + nonlocal: a function that remembers state ------------
def make_counter():
    count = 0
    def step():
        nonlocal count                # rebind the enclosing variable, not a new local
        count += 1
        return count
    return step

tick = make_counter()
print("\ncounter:", tick(), tick(), tick())   # 1 2 3

# --- 6. TRAP: mutable default argument ----------------------------------
def add_bad(name, roster=[]):       # ❌ shared default
    roster.append(name)
    return roster

print("\nBUGGY:")
print(add_bad("Ana"))               # ['Ana']
print(add_bad("Ben"))               # ['Ana', 'Ben']  <- persists!

def add_ok(name, roster=None):      # ✅
    if roster is None:
        roster = []
    roster.append(name)
    return roster

print("FIXED:")
print(add_ok("Ana"))                # ['Ana']
print(add_ok("Ben"))                # ['Ben']  <- fresh each call

# --- 7. Scope: UnboundLocalError demo (commented) -----------------------
# count = 0
# def bump():
#     count = count + 1   # UnboundLocalError: assigning makes `count` local
# Prefer returning a value (or use `nonlocal`/a closure, as in block 5).


# ======================================================================
# PART B — Recursion & Recursive Thinking
# ======================================================================

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
