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

# --- 2. raise your own validation error ---------------------------------
def clean_likert(n):
    """Return n if it's a valid 1–5 Likert int, else raise ValueError."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError(f"{n!r} is not an integer")
    if not 1 <= n <= 5:
        raise ValueError(f"{n} is outside 1–5")
    return n

# --- 3. clean a dirty survey column, keeping a rejection log ------------
raw_responses = ["5", "3", "N/A", "7", "", "1", "two", "4"]
clean, rejected = [], []
for r in raw_responses:
    n = safe_int(r)
    try:
        clean.append(clean_likert(n))        # may raise
    except ValueError as e:
        rejected.append((r, str(e)))

print("\nclean:", clean)
print("rejected:")
for original, why in rejected:
    print(f"  {original!r}: {why}")

# --- 4. else / finally ---------------------------------------------------
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

# --- 5. TRAP: bare except hides real bugs (don't do this) ---------------
# try:
#     risky()
# except:            # ❌ catches EVERYTHING, even Ctrl+C and typos
#     pass           # ❌ and silently swallows the error
# Always: except SpecificError as e: ...
