"""
Session 8 — Regular Expressions & Text Cleaning
Run me:  python3 demo.py
Always write patterns as RAW strings: r"..."
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

# --- 3. The "." trap -----------------------------------------------------
print('\n"." matches ANY char:', re.search(r".", "a.b").group())   # 'a', not '.'
print('literal dot with \\.:   ', re.search(r"\.", "a.b").group())  # '.'

# --- 4. Substitute / clean text -----------------------------------------
messy = "  too    much\t  space  "
print("\ncleaned:", repr(re.sub(r"\s+", " ", messy).strip()))

# --- 5. Mine free-text survey responses ---------------------------------
responses = ["loved #python and #stats", "more #python please", "no tags here"]
tags = []
for r in responses:
    tags += re.findall(r"#(\w+)", r)      # findall returns all matches
print("\nall tags:", tags)
from collections import Counter
print("tag counts:", Counter(tags))

# --- 6. Reformat "Last, First" -> "First Last" ---------------------------
def flip_name(s: str) -> str:
    m = re.search(r"^(.+),\s*(.+)$", s.strip())
    return f"{m.group(2)} {m.group(1)}" if m else s

print("\n", flip_name("Curie, Marie"))      # Marie Curie

# --- 7. When NOT to use regex -------------------------------------------
# For simple splits/trims, string methods are clearer than regex:
print("\nuse .split():", "a,b,c".split(","))
print("use .strip():", "  hi  ".strip())
