"""
Session 5 — Functions, Scope & Reusability
Run me:  python3 demo.py
"""

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

def total(*args):              # collect positionals into a tuple
    return sum(args)
print("total:", total(1, 2, 3, 4))

def tag(**kwargs):             # collect keywords into a dict
    return kwargs
print("tag:", tag(name="Ana", gpa=3.9))

scores = [91, 58, 73]
print("unpacked into total:", total(*scores))   # * unpacks the list

# --- 3. TRAP: mutable default argument ----------------------------------
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

# --- 4. Scope: UnboundLocalError demo (commented) -----------------------
# count = 0
# def bump():
#     count = count + 1   # UnboundLocalError: assigning makes `count` local
# Prefer returning a value and reassigning at the call site.
