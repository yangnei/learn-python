"""
Session 7 — Exceptions & Defensive Code
Run me:  python3 demo.py
"""

# --- 1. try / except: convert what you can ------------------------------
def safe_int(value):
    """Return int(value) or None if it can't be parsed."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

for v in ["42", "N/A", "", None, "7"]:
    print(f"safe_int({v!r}) = {safe_int(v)}")

# --- 2. Your own exception type, and raising it -------------------------
class LikertError(ValueError):
    """Raised when a value isn't a valid 1–5 Likert response."""

def clean_likert(n):
    """Return n if it's a valid 1–5 Likert int, else raise LikertError."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise LikertError(f"{n!r} is not an integer")
    if not 1 <= n <= 5:
        raise LikertError(f"{n} is outside 1–5")
    return n

# --- 3. clean a dirty survey column, keeping a rejection log ------------
raw_responses = ["5", "3", "N/A", "7", "", "1", "two", "4"]
clean, rejected = [], []
for r in raw_responses:
    n = safe_int(r)
    try:
        clean.append(clean_likert(n))        # may raise LikertError
    except LikertError as e:                 # catching the base ValueError works too
        rejected.append((r, str(e)))

print("\nclean:", clean)
print("rejected:")
for original, why in rejected:
    print(f"  {original!r}: {why}")

# --- 4. Exception chaining: keep the original cause with `raise ... from` -
def parse_score(text):
    try:
        return int(text)
    except ValueError as e:
        raise LikertError(f"bad score {text!r}") from e   # preserves the __cause__

try:
    parse_score("oops")
except LikertError as e:
    print("\nraised:", e, "| caused by:", repr(e.__cause__))

# --- 5. else / finally ---------------------------------------------------
def parse(value):
    try:
        n = int(value)
    except ValueError:
        return "bad"
    else:
        return f"ok:{n}"          # only when no exception
    finally:
        pass                       # cleanup would go here (e.g., close a file)

print("\n", parse("10"), parse("x"))

# --- 6. assert: a cheap internal sanity check ---------------------------
def mean(xs):
    assert xs, "mean() needs at least one value"   # AssertionError if xs is empty
    return sum(xs) / len(xs)

print("mean:", mean([2, 4, 6]))

# --- 7. TRAP: bare except hides real bugs (don't do this) ---------------
# try:
#     risky()
# except:            # ❌ catches EVERYTHING, even Ctrl+C and typos
#     pass           # ❌ and silently swallows the error
# Always: except SpecificError as e: ...
