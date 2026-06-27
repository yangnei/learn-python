"""
Session 2 — The Dynamic-Typing Traps
Run me:  python3 traps_demo.py
Every line below was verified on CPython 3.11+. Cover the right side and PREDICT first.
"""
import math

print("=== 1. == vs is ===")
a = [1, 2]; b = [1, 2]
print("a == b :", a == b)          # True  (same value)
print("a is b :", a is b)          # False (different objects)
print("id(a) == id(b)?", id(a) == id(b))   # False — `is` is really an id() check
c = a
print("a is c :", a is c)          # True  (c is an alias for a)

x = None
print("x is None :", x is None)    # True  (correct way to test None)

print("\n=== 2. Booleans are integers ===")
print("True == 1 :", True == 1)            # True
print("5 + True  :", 5 + True)             # 6
print("sum([T,F,T]):", sum([True, False, True]))  # 2  (counts Trues)
# Note: Python prints a SyntaxWarning here ("is with int literal") — that warning
# IS the lesson: don't use `is` to compare values. We do it once to show the result.
print("True is 1 :", True is 1)            # False (value equal, not same object)
print("isinstance(True, int):", isinstance(True, int))  # True

print("\n=== 3. int vs float / division ===")
print("3 == 3.0 :", 3 == 3.0)      # True
print("7 / 2    :", 7 / 2)         # 3.5  (always float)
print("7 // 2   :", 7 // 2)        # 3
print("-7 // 2  :", -7 // 2)       # -4   (floors toward -inf)

print("\n=== 4. Float precision (and the NaN oddity) ===")
print("0.1 + 0.2          :", 0.1 + 0.2)            # 0.30000000000000004
print("0.1 + 0.2 == 0.3   :", 0.1 + 0.2 == 0.3)     # False
print("math.isclose(...)  :", math.isclose(0.1 + 0.2, 0.3))  # True  <- the fix
nan = float("nan")
print("nan == nan         :", nan == nan)           # False! NaN equals nothing, not even itself
print("math.isnan(nan)    :", math.isnan(nan))      # True   <- the right test

print("\n=== 5. Comparing across types ===")
print('5 == "5" :', 5 == "5")      # False (no error)
try:
    print(5 > "5")
except TypeError as e:
    print('5 > "5"  : TypeError ->', e)

print("\n=== 6. Sequences compare element-by-element ===")
print("[1,2] == [1,2] :", [1, 2] == [1, 2])   # True
print("[1,2] == (1,2) :", [1, 2] == (1, 2))   # False (list vs tuple)
print("(1,2) < (1,3)  :", (1, 2) < (1, 3))    # True
print("'apple'<'banana':", "apple" < "banana")  # True

print("\n=== 7. type vs isinstance ===")
print("isinstance(5,(int,float)):", isinstance(5, (int, float)))  # True
print("type(True) is int        :", type(True) is int)            # False
print("isinstance(True, int)    :", isinstance(True, int))        # True

print("\n=== 8. Truthiness ===")
for v in (0, 0.0, "", [], {}, None, "0", [0], "False"):
    print(f"bool({v!r:>7}) = {bool(v)}")

print("\n=== 9. The small-int cache (an implementation detail — never rely on it) ===")
m = 256; p = 256
print("256 cached    :", m is p)        # True  — CPython pre-caches small ints (-5..256)
m = int("257"); p = int("257")          # built at runtime, so NOT folded to one object
print("257 runtime   :", m is p)        # False — outside the cache, separate objects
print("but 257 == 257:", m == p)        # True  — value is equal; identity is not
# Lesson: this is why you compare values with ==, never identities with `is`.
