"""
Session 1 — Running Python, Variables & Types
Run me:  python3 demo.py
Read each block, then change ONE thing and predict the output before re-running.
"""

# --- 1. Variables are labels on objects ---------------------------------
n = 30          # int
mean = 3.7      # float
name = "Ada"    # str
passed = True   # bool
missing = None  # NoneType

print(name, "->", type(name))
print(mean, "->", type(mean))
print("passed?", passed, "| missing?", missing)

# `=` is an action, not a math claim. Re-pointing a label is fine:
n = n + 1
print("n is now", n)

# Parallel assignment: the right side is built first, then unpacked left.
x, y = 1, 2
x, y = y, x                 # the Pythonic swap — no temp variable needed
print("after swap:", x, y)             # 2 1
big = 1_000_000            # underscores are just visual separators in numbers
print("big =", big)                    # 1000000


# --- 2. input() is ALWAYS a string --------------------------------------
# (Hard-coded here so the file runs without typing; the trap is real.)
raw = "5"                 # imagine this came from input()
print('"5" + "3" =', raw + "3")          # '53'  <- string concatenation!
print("int + int =", int(raw) + 3)       # 8     <- convert first


# --- 3. f-strings: clean formatting -------------------------------------
score = 87.456
print(f"{name} scored {score:.1f}")      # one decimal -> 87.5
print(f"big number: {1234567:,}")        # 1,234,567
print(f"as percent: {0.873:.1%}")        # 87.3%
print(f"{score=}")                       # self-documenting: score=87.456 (great for debugging)


# --- 4. Strings are objects with methods --------------------------------
full = "ada  LOVELACE"
print("title:", full.title())            # 'Ada  Lovelace'
print("upper:", name.upper(), "| len:", len(name))   # ADA 3
print("words:", "one two three".split())  # ['one', 'two', 'three']
print("'da' in name?", "da" in name)      # True — `in` tests membership


# --- 5. Casting (type conversion) ---------------------------------------
print("int('42')   =", int("42"))
print("float('3.1')=", float("3.1"))
print("int(3.9)    =", int(3.9), "(truncates!)")
print("round(3.9)  =", round(3.9))


# --- 6. A tiny real program: years to graduation ------------------------
def years_to_graduation(credits_done: int, credits_needed: int, per_year: int) -> float:
    remaining = credits_needed - credits_done
    return remaining / per_year          # / always gives a float

print("Years left:", years_to_graduation(60, 120, 30))   # 2.0


# --- 7. Reading a traceback ---------------------------------------------
# Uncomment the next line to SEE an error on purpose, then read the LAST line:
# age = int("thirty")   # ValueError: invalid literal for int() with base 10: 'thirty'
