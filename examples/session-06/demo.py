"""Session 6 — Recursion & Recursive Thinking  (run me: python3 demo.py)."""

import sys
import functools


# 1) The shape of EVERY recursive function: a base case + a recursive case.
def countdown(n):
    if n <= 0:                 # BASE CASE — the stop condition
        print("liftoff!")
        return
    print(n)
    countdown(n - 1)           # RECURSIVE CASE — same problem, smaller input

print("countdown:")
countdown(3)


# 2) Recursion vs iteration: same answer, two styles. Each call adds a stack frame.
def factorial(n):
    if n <= 1:
        return 1               # base case
    return n * factorial(n - 1)   # remember to RETURN the recursive call

def factorial_loop(n):
    total = 1
    for k in range(2, n + 1):
        total *= k
    return total

print("\nfactorial(5):", factorial(5), "==", factorial_loop(5))


# 3) Memoization: @lru_cache remembers past calls so each input is computed once.
#    Naive fibonacci recomputes the same values exponentially; the cache makes it linear.
calls = 0
def fib_naive(n):
    global calls
    calls += 1
    return n if n < 2 else fib_naive(n - 1) + fib_naive(n - 2)

@functools.lru_cache(maxsize=None)     # one decorator turns the slow version fast
def fib_fast(n):
    return n if n < 2 else fib_fast(n - 1) + fib_fast(n - 2)

print("\nfib_naive(30):", fib_naive(30), "in", calls, "calls")
print("fib_fast(30): ", fib_fast(30), "->", fib_fast.cache_info())   # far fewer hits


# 4) Mutual recursion: two functions that call each other toward a shared base case.
def is_even(n):
    return True if n == 0 else is_odd(n - 1)
def is_odd(n):
    return False if n == 0 else is_even(n - 1)
print("\nis_even(10):", is_even(10), "| is_odd(7):", is_odd(7))


# 5) Where recursion SHINES: naturally NESTED data, where one loop can't reach
#    all the way down. This is shaped like a real nested-JSON export.
export = {
    "cohort": "2026",
    "students": [
        {"name": "Ana", "scores": [91, 88]},
        {"name": "Ben", "scores": [58, [60, 64]]},   # arbitrarily nested
    ],
}

def deep_sum(obj):
    """Add up every number found anywhere inside nested lists/dicts."""
    if isinstance(obj, bool):                 # bool is an int subclass (Session 2!)
        return 0
    if isinstance(obj, (int, float)):
        return obj
    if isinstance(obj, dict):
        return sum(deep_sum(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return sum(deep_sum(x) for x in obj)
    return 0                                  # strings, None, etc. contribute nothing

print("\ndeep_sum of nested export:", deep_sum(export))   # 91+88+58+60+64 = 361


# 6) The trap: with no reachable base case, recursion never stops. Python has no
#    tail-call optimization, so it just piles up stack frames until it gives up.
print("\nPython's recursion limit:", sys.getrecursionlimit())

def runaway(n):
    return runaway(n + 1)        # BUG: never reaches a base case

try:
    runaway(0)
except RecursionError:
    print("RecursionError: maximum recursion depth exceeded (as expected)")
