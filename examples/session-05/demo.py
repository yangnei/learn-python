"""
Session 5 — Functions, Scope & Reusability
Run me:  python3 demo.py
"""
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
