# Session 9 — Practice (60 min): Regular Expressions

Always use raw strings `r"..."`. Predict each result before running.

## Task 1 — Validate
Write `valid_university_email(addr)` returning `True` only for `something@something.edu`.
Test: `"ana@university.edu"`, `"ana@gmail.com"`, `"a@b.edu.evil.com"`.

## Task 2 — Extract with groups
From `"Course ED1234 meets Tue"`, pull the department (`ED`) and number (`1234`) using one
regex with two capture groups.

## Task 3 — Clean
Collapse all runs of whitespace in `"  too    much\t space "` to single spaces and trim.

## Task 4 — Mine free text
From a list of open-ended responses, count how often each `#hashtag` appears
(use `re.findall(r"#(\w+)", text)` and `collections.Counter`).

## Task 5 — Reformat
Turn `"Curie, Marie"` into `"Marie Curie"` with a single regex + groups.

## Task 6 — Judgment
Give one task where a plain string method (`.split()`, `.strip()`, `.replace()`) is the better,
clearer choice than a regex.

## Bonus — Pythonic idiom drill
Cover the `# ->` answers, predict each line, then run.

```python
import re
m = re.search(r"(?P<year>\d{4})", "class of 2026")
print(m.group("year"), m.groupdict())   # -> 2026 {'year': '2026'}   (named groups)
print(re.split(r"\s*,\s*", "a, b ,c")) # -> ['a', 'b', 'c']        (split on commas + spaces)
```

---
## Solutions
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
```
```
Trap reminder: `.` matches **any** character — use `\.` for a literal dot, and never forget the
`r"..."` prefix or your backslashes become Python escape sequences.
