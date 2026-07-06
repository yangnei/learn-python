---
marp: true
title: "Session 9 — Regular Expressions & Text Cleaning"
paginate: true
---

# Session 9
## Regular Expressions & Text Cleaning

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
| `[abc]` `[a-z]` `[^abc]` | any in set / in range / none in set |
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

`m.groups()` hands back every capture at once: `('ED', '1234')`.
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
url.removeprefix("https://")   # trim a known prefix — no regex needed (3.9+)
```

Regex shines for *variable* patterns. For fixed strings, plain methods read better.

---

## Your turn

`examples/session-09/practice.md`:
1. Email validator. 2. Extract dept+number. 3. Collapse whitespace.
4. Count hashtags across responses. 5. Flip `"Last, First"`. 6. One case to use `.split()` instead.

---

# Going deeper
## Power regex

---

## Flags

```python
re.findall(r"stress", corpus, re.IGNORECASE)   # Stress, STRESS, stress
re.findall(r"^\d+", text, re.MULTILINE)        # ^ and $ match per LINE
re.search(p, s, re.IGNORECASE | re.MULTILINE)  # combine with |
re.search(r"a.b", text, re.DOTALL)             # . crosses newlines too
```

---

## `re.compile` — name your patterns

```python
EMAIL = re.compile(r"\w+@\w+\.edu")
COURSE = re.compile(r"[A-Z]{2}\d{4}")

EMAIL.fullmatch(addr)        # same four functions, now methods
COURSE.findall(text)
```

Compile once, reuse everywhere — the pattern gets a *name* the reader can trust.

---

## Readable patterns: `re.VERBOSE`

```python
EMAIL = re.compile(r"""
    \w+          # the user part
    @
    \w+          # the domain
    \.edu        # a literal dot, then edu
""", re.VERBOSE)
```

Whitespace is ignored, comments allowed — a regex your future self can review.

---

## Groups, round 2

```python
m = re.search(r"(?P<dept>[A-Z]{2})(?P<num>\d{4})", "ED1234")
m.group("dept"), m.groupdict()     # names beat positions

r"(?:Prof|Dr)\.?\s+(\w+)"        # (?:...) groups WITHOUT capturing
```

Name the groups you extract; use `(?:...)` for grouping-only parentheses.

---

## Greedy vs lazy

```python
re.search(r"\[(.+)\]",  "[ED101][ED102]").group(1)   # 'ED101][ED102'  😱
re.search(r"\[(.+?)\]", "[ED101][ED102]").group(1)   # 'ED101'
```

`+` and `*` grab as much as possible; `+?` / `*?` as little as possible.
Bracketed/quoted things almost always want **lazy**.

---

## `re.sub` with a function: the anonymizer

```python
ids = {}
def anonymize(m):
    name = m.group(0)
    ids.setdefault(name, f"P{len(ids) + 1:03d}")
    return ids[name]

re.sub(r"\b(?:Ana|Ben|Cara)\b", anonymize, transcript)
# "P001 said ... P002 replied ... P001 agreed"
```

When the replacement must be *computed*, pass a function — every match goes through it.
(A closure over `ids` — Session 5 pays off.)

---

## Regex meets files

```python
text = Path("responses.txt").read_text(encoding="utf-8")
emails = sorted(set(EMAIL.findall(text)))
```

Session 8 + Session 9 in two lines: read the file, mine the pattern, dedupe with a set.

---

## Your turn — round 2

`examples/session-09/practice.md` → **In class — going deeper**:
a commented `VERBOSE` email pattern, the anonymizer, and a two-format date harvest.
---

## Traps recap

- `.` matches **any** char — use `\.` for a literal dot.
- Forgetting `r"..."` breaks your backslashes.
- `re.search` returns `None` on no match — guard before `.group()`.
- Don't use regex where a string method is clearer.

## Summary
You can validate, extract, and clean real-world text.
**Next:** Session 10 — modules, OOP & the Pythonic toolkit.

---

## Homework (before Session 10)

*Outside class — it doesn't count toward class time. Full specs + solutions: `examples/session-09/practice.md` → **Homework**.*

1. **Pattern drill** — student IDs, US phone numbers, ISO dates: one `fullmatch` pattern each.
2. **Messy-name cleanup** — normalize a scraped name column with `re.sub`.
3. **Domain harvest** — extract every email domain from a block of text.
