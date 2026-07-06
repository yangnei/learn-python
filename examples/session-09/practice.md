# Session 9 — Practice: Regular Expressions & Text Cleaning

Type each solution yourself. **Predict every output before you run it.** Solutions at the bottom.

## In class

Always use raw strings `r"..."`. Predict each result before running.

### Task 1 — Validate
Write `valid_university_email(addr)` returning `True` only for `something@something.edu`.
Test: `"ana@university.edu"`, `"ana@gmail.com"`, `"a@b.edu.evil.com"`.

### Task 2 — Extract with groups
From `"Course ED1234 meets Tue"`, pull the department (`ED`) and number (`1234`) using one
regex with two capture groups.

### Task 3 — Clean
Collapse all runs of whitespace in `"  too    much\t space "` to single spaces and trim.

### Task 4 — Mine free text
From a list of open-ended responses, count how often each `#hashtag` appears
(use `re.findall(r"#(\w+)", text)` and `collections.Counter`).

### Task 5 — Reformat
Turn `"Curie, Marie"` into `"Marie Curie"` with a single regex + groups.

### Task 6 — Judgment
Give one task where a plain string method (`.split()`, `.strip()`, `.replace()`) is the better,
clearer choice than a regex.

### Bonus — Pythonic idiom drill
Cover the `# ->` answers, predict each line, then run.

```python
import re
m = re.search(r"(?P<year>\d{4})", "class of 2026")
print(m.group("year"), m.groupdict())   # -> 2026 {'year': '2026'}   (named groups)
print(re.split(r"\s*,\s*", "a, b ,c")) # -> ['a', 'b', 'c']        (split on commas + spaces)
```

## Extra practice (in class, if you're ahead)

### E1 — Named groups
Redo the dept+number extraction with `(?P<dept>...)` / `(?P<num>...)` and print
`m.groupdict()`.

### E2 — regex101 field trip
Paste your email pattern into regex101.com (flavor: **Python**). Read the left-panel
explanation token by token — does it say what you *meant*?

## Homework (before Session 10)

*~30–45 minutes, outside class — it doesn't count toward the hour. Try everything before peeking at the solutions.*

### H1 — Pattern drill
One `re.fullmatch` pattern each; test against two valid and two invalid strings:
1. Student ID: two uppercase letters + six digits (`AB123456`)
2. US phone: `555-867-5309` (digits and dashes only)
3. ISO date: `2026-07-06` (just the shape — don't validate month ranges)

### H2 — Messy-name cleanup
Normalize `["  smith,  ana", "LEE,BEN", "Garcia ,  Cara "]` to `"Ana Smith"`,
`"Ben Lee"`, `"Cara Garcia"`: regex-split on the comma (with optional spaces around it),
then `.strip()` + `.title()`, and flip the order.

### H3 — Domain harvest
From a paragraph containing several email addresses, extract the **unique** domains
(e.g. `{"university.edu", "gmail.com"}`) with one `findall` + a `set`.

---

## Solutions

### In class

See `demo.py` in this folder — it implements all six. Key lines:

```python
re.fullmatch(r"\w+@\w+\.edu", addr) is not None      # 1 (fullmatch anchors both ends)
m = re.search(r"([A-Z]{2})(\d{4})", s); m.group(1), m.group(2)   # 2
re.sub(r"\s+", " ", messy).strip()                   # 3
from collections import Counter; Counter(re.findall(r"#(\w+)", text))   # 4
m = re.search(r"^(.+),\s*(.+)$", s); f"{m.group(2)} {m.group(1)}"      # 5
```
Task 6: splitting `"a,b,c"` on commas is just `"a,b,c".split(",")` — no regex needed.
Reach for regex only when the pattern is genuinely variable (digits, optional parts, anchors).

Trap reminder: `.` matches **any** character — use `\.` for a literal dot, and never forget the
`r"..."` prefix or your backslashes become Python escape sequences.

### Extra practice

```python
# E1
import re
m = re.search(r"(?P<dept>[A-Z]{2})(?P<num>\d{4})", "Course ED1234 meets Tue")
print(m.group("dept"), m.group("num"))   # ED 1234
print(m.groupdict())                     # {'dept': 'ED', 'num': '1234'}
```

E2 — the point is the habit: regex101's explainer catches "`.` matches any character"
mistakes before your data does.

### Homework

```python
# H1
import re

sid   = r"[A-Z]{2}\d{6}"        # AB123456 ✓  CD000001 ✓  ab123456 ✗  AB12345 ✗
phone = r"\d{3}-\d{3}-\d{4}"    # 555-867-5309 ✓  555-8675309 ✗
date  = r"\d{4}-\d{2}-\d{2}"    # 2026-07-06 ✓  2026-7-6 ✗

for s in ["AB123456", "ab123456"]:
    print(s, re.fullmatch(sid, s) is not None)

# H2
def clean_name(raw):
    last, first = re.split(r"\s*,\s*", raw.strip(), maxsplit=1)
    return f"{first.strip().title()} {last.strip().title()}"

for raw in ["  smith,  ana", "LEE,BEN", "Garcia ,  Cara "]:
    print(clean_name(raw))      # Ana Smith · Ben Lee · Cara Garcia

# H3
text = "Write ana@university.edu or ben@gmail.com; cc cara@university.edu today."
print(set(re.findall(r"\w+@([\w.]+\.\w+)", text)))
# {'university.edu', 'gmail.com'}  — the set removes the duplicate
```
