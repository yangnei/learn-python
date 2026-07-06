"""Session 9 demo — Regular Expressions & Text Cleaning.

Run me:  python3 demo.py
Predict each printed line BEFORE you run.
"""

import re

# --- 1. Validate: does the whole string match the pattern? ---------------
def valid_university_email(addr: str) -> bool:
    # \w+ chars, @, domain, literal dot (\.), then "edu"
    return re.fullmatch(r"\w+@\w+\.edu", addr) is not None

for addr in ["ana@university.edu", "ana@gmail.com", "ana@@x.edu"]:
    print(f"{addr:22} -> {valid_university_email(addr)}")

# --- 2. Search anywhere; extract pieces with capture groups -------------
m = re.search(r"([A-Z]{2})(\d{4})", "Course ED1234 meets on Tue")
print("\ndept:", m.group(1), "| number:", m.group(2), "| whole:", m.group(0))

# --- 3. NAMED groups read better than group(1)/group(2) -----------------
m = re.search(r"(?P<dept>[A-Z]{2})(?P<num>\d{4})", "ED1234")
print("named:", m.group("dept"), m.group("num"), "| dict:", m.groupdict())

# --- 4. re.compile + re.VERBOSE: a reusable, self-documenting pattern ----
COURSE = re.compile(r"""
    (?P<dept>[A-Z]{2})    # two-letter department
    (?P<num>\d{4})        # four-digit course number
""", re.VERBOSE)
print("compiled findall:", COURSE.findall("Take ED1234 and PS5500 this term"))

# --- 5. The walrus := keeps the match object without a second lookup -----
if (hit := re.search(r"\d+", "cohort 2026 has 30 students")):
    print("first number found:", hit.group())     # 2026

# --- 6. The "." trap -----------------------------------------------------
print('\n"." matches ANY char:', re.search(r".", "a.b").group())   # 'a', not '.'
print('literal dot with \\.:   ', re.search(r"\.", "a.b").group())  # '.'

# --- 7. Substitute / split / clean text ---------------------------------
messy = "  too    much\t  space  "
print("\ncleaned:", repr(re.sub(r"\s+", " ", messy).strip()))
print("re.split:", re.split(r"\s*,\s*", "a , b,c ,  d"))   # split on commas + stray spaces

# --- 8. Mine free-text survey responses ---------------------------------
responses = ["loved #python and #stats", "more #python please", "no tags here"]
tags = []
for r in responses:
    tags += re.findall(r"#(\w+)", r)      # findall returns all matches
print("\nall tags:", tags)
from collections import Counter
print("tag counts:", Counter(tags))

# --- 9. Reformat "Last, First" -> "First Last" ---------------------------
def flip_name(s: str) -> str:
    m = re.search(r"^(.+),\s*(.+)$", s.strip())
    return f"{m.group(2)} {m.group(1)}" if m else s

print("\n", flip_name("Curie, Marie"))      # Marie Curie

# --- 10. When NOT to use regex ------------------------------------------
# For simple splits/trims, string methods are clearer than regex:
print("\nuse .split():", "a,b,c".split(","))
print("use .strip():", "  hi  ".strip())

# ==========================================================================
# GOING DEEPER — second-hour material
# ==========================================================================
# --- deeper 1: flags -----------------------------------------------------------------
print("\n=== GOING DEEPER ===")
corpus = "Stress was high. Some stress is normal. STRESS!"
print("ignorecase count:", len(re.findall(r"stress", corpus, re.IGNORECASE)))
lines = "42 Ana\n7 Ben\nnope Cara"
print("per-line numbers:", re.findall(r"^\d+", lines, re.MULTILINE))

# --- deeper 2: greedy vs lazy ---------------------------------------------------------
tags = "[ED101][ED102]"
print("greedy .+ :", re.search(r"\[(.+)\]", tags).group(1))
print("lazy  .+? :", re.search(r"\[(.+?)\]", tags).group(1))

# --- deeper 3: re.sub with a FUNCTION — the anonymizer ---------------------------------
transcript = "Ana said the course helped. Ben disagreed. Ana insisted."
ids = {}
def anonymize(m):
    name = m.group(0)
    ids.setdefault(name, f"P{len(ids) + 1:03d}")
    return ids[name]

print(re.sub(r"\b(?:Ana|Ben|Cara)\b", anonymize, transcript))
print("mapping:", ids)
