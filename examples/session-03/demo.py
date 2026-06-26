"""
Session 3 — Control Flow: Conditionals & Loops
Run me:  python3 demo.py
"""

# --- 1. Conditionals + chained comparison -------------------------------
def letter_grade(score):
    if not 0 <= score <= 100:        # chained comparison
        return "Invalid"
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    if score >= 60: return "D"
    return "F"

for s in [95, 90, 89.999, 72, 60, 59, 120]:
    print(f"{s:>7} -> {letter_grade(s)}")

# --- 2. and / or return an operand (short-circuit) ----------------------
print("\n5 and 0   =", 5 and 0)        # 0
print("'' or N/A =", "" or "N/A")      # N/A
name = "" or "Anonymous"               # default-value idiom
print("name      =", name)

# truthiness instead of == True
submitted = ["essay.pdf"]
if submitted:                          # not  if len(submitted) > 0
    print("Has submissions")

# --- 3. Loops: iterate elements, range, break/continue ------------------
names  = ["Ana", "Ben", "Cara", "Dev"]
scores = [91, 58, 73, 64]

print("\nrange(1,5) =", list(range(1, 5)))   # [1,2,3,4] — stop excluded!

total = 0
for s in scores:
    total += s
print("average:", total / len(scores))

# --- 4. enumerate + zip (no index juggling) -----------------------------
for i, name in enumerate(names, start=1):
    print(f"{i}. {name}")

for name, score in zip(names, scores):
    print(f"{name}: {'PASS' if score >= 60 else 'FAIL'}")

print("passes:", sum(s >= 60 for s in scores))   # bools sum! (Session 2)

# --- 5. break / continue -------------------------------------------------
print("\nfirst failing student:")
for name, score in zip(names, scores):
    if score >= 60:
        continue
    print(" ->", name)
    break

# --- 6. The validation loop (simulated input) ---------------------------
def to_valid_score(raw):
    """The logic inside a `while True:` prompt: int 0..100 or None."""
    return int(raw) if raw.isdigit() and 0 <= int(raw) <= 100 else None

print("\nvalidation:", [to_valid_score(x) for x in ["150", "abc", "84"]])  # None,None,84
