---
marp: true
title: "Session 8 — Regular Expressions & Text Cleaning"
paginate: true
---

# Session 8
## Regular Expressions & Text Cleaning

Find, validate, extract, and clean messy text — the researcher's power tool.

---

## Why a researcher cares

- Validate IDs, emails, dates before they pollute your data.
- Extract structured bits from free text (codes, names, numbers).
- Clean and normalize open-ended survey responses.
- A first pass at **qualitative coding** (find every response matching a pattern).

🧠 Like search-and-filter over a corpus — but it matches *form*, not meaning.

---

## Always use raw strings

```python
import re
re.search(r"\d+", "id 42")     # r"..." = raw string
```

Without `r"..."`, Python eats the backslashes (`\d` → error/garbage).
**Rule:** every regex pattern is a raw string.

---

## The survival tokens

| Token | Matches |
|---|---|
| `.` | **any** char (except newline) |
| `\d \w \s` | digit / word-char / whitespace |
| `\D \W \S` | the negations |
| `+ * ?` | 1+, 0+, 0-or-1 |
| `{m}` `{m,n}` | exactly m / between m and n |
| `^ $` | start / end of string |
| `[abc]` `[^abc]` | any in set / none in set |
| `(...)` | capture group |
| `a\|b` | a or b |

---

## The `.` trap

```python
re.search(r".", "a.b").group()    # 'a'  — ANY char, not a dot!
re.search(r"\.", "a.b").group()   # '.'  — escape it for a literal dot
```

Escape the specials when you mean them literally: `\. \^ \$ \* \+ \? \( \) \[ \] \{ \} \|`

---

## The four functions you need

```python
re.search(pattern, s)     # first match ANYWHERE -> match or None
re.fullmatch(pattern, s)  # the WHOLE string must match -> validation
re.findall(pattern, s)    # list of ALL matches
re.sub(pattern, repl, s)  # replace matches -> cleaning
```

`re.IGNORECASE` flag for case-insensitive: `re.search(p, s, re.IGNORECASE)`.

---

## Validate (fullmatch anchors both ends)

```python
def valid_university_email(addr):
    return re.fullmatch(r"\w+@\w+\.edu", addr) is not None

valid_university_email("ana@university.edu")   # True
valid_university_email("ana@gmail.com")        # False
valid_university_email("ana@@x.edu")           # False
```

---

## Extract with capture groups

```python
m = re.search(r"([A-Z]{2})(\d{4})", "Course ED1234 meets Tue")
m.group(0)   # "ED1234"  whole match
m.group(1)   # "ED"      dept
m.group(2)   # "1234"    number
```

`m` is `None` if nothing matched — check before `.group()`.

---

## Clean & mine free text

```python
re.sub(r"\s+", " ", messy).strip()        # collapse whitespace
re.findall(r"#(\w+)", "love #python #stats")   # ['python', 'stats']

from collections import Counter
Counter(re.findall(r"#(\w+)", corpus))    # theme frequencies
```

Reformat with groups: `re.sub(r"^(.+),\s*(.+)$", r"\2 \1", "Curie, Marie")` → `"Marie Curie"`.

---

## When NOT to use regex

```python
"a,b,c".split(",")     # simple split — no regex needed
"  hi  ".strip()       # trim — no regex needed
text.replace("X", "Y") # fixed substring — no regex needed
```

Regex shines for *variable* patterns. For fixed strings, plain methods read better.

---

## Your turn

`examples/session-08/practice.md`:
1. Email validator. 2. Extract dept+number. 3. Collapse whitespace.
4. Count hashtags across responses. 5. Flip `"Last, First"`. 6. One case to use `.split()` instead.

---

## Traps recap

- `.` matches **any** char — use `\.` for a literal dot.
- Forgetting `r"..."` breaks your backslashes.
- `re.search` returns `None` on no match — guard before `.group()`.
- Don't use regex where a string method is clearer.

## Summary
You can validate, extract, and clean real-world text.
**Next:** organize code into modules and classes.
