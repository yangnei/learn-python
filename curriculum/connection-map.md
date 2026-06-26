# Connection Map — Python ⇄ Education-Research Background

> From the *personalized-syllabus* method: each new programming concept is bridged to something
> the student already knows from education research, and — crucially — **where the bridge breaks**
> is named, so the new concept isn't quietly collapsed into the familiar one. Use these as the
> "hooks" when introducing each topic; they cut learning time dramatically for an expert adult.

---

### 1. Variables & assignment  *(S1)*
- **Maps onto:** named quantities in a stats model — `n`, `mean`, `alpha`.
- **Where it breaks:** in math, `x = x + 1` is a contradiction; in Python `=` is an *action*
  (rebind the name), not an assertion of equality. A variable is a **label stuck on an object**,
  not a box that holds a value. This single reframing prevents most aliasing confusion later.

### 2. Types & dynamic typing  *(S1, S2)*
- **Maps onto:** measurement levels — nominal/ordinal/interval/ratio. Python's `str`/`bool`/`int`/
  `float` are loosely analogous (categorical vs counted vs continuous).
- **Where it breaks:** SPSS/R columns have *one declared type per column*; a Python variable can
  hold a string now and an int later. The discipline a column gives you for free, you must supply
  yourself. This is exactly why the comparison traps in S2 exist.

### 3. `==` vs `is`  *(S2)*
- **Maps onto:** the difference between **two questionnaires with identical answers** (equal in
  value) and **the same physical respondent** (identical individual). Two students can have the
  same GPA (`==`) without being the same person (`is`).
- **Where it breaks:** the analogy is exact for objects, but Python adds an implementation wrinkle
  (small-integer caching) that has no analogue in research — flagged as a "do not rely on this."

### 4. Boolean as a subclass of int (`True == 1`)  *(S2)*
- **Maps onto:** **dummy coding** — you already encode "treatment = 1, control = 0" and then
  *sum* the dummies to count cases. Python literally does this: `sum([True, False, True]) == 2`.
- **Where it breaks:** in your data the 1/0 is a convention you imposed; in Python it's baked into
  the language, so `True + True == 2` works even when you didn't intend arithmetic on a flag.

### 5. Float precision (`0.1 + 0.2 != 0.3`)  *(S2)*
- **Maps onto:** **rounding/measurement error**. You already never test two measured scores for
  exact equality; you use tolerances and report to 2 decimals.
- **Where it breaks:** here the error isn't in the data — it's in how the *computer* stores
  decimals in binary. Same instinct (`math.isclose`, round for display), new cause.

### 6. Lists / dicts / DataFrames  *(S5, S8)*
- **Maps onto:** a `list` of `dict`s is a **tidy dataset**: each dict is a *row/respondent*, each
  key is a *variable/column*. A `dict` alone is one record's variable→value map.
- **Where it breaks:** a spreadsheet enforces rectangularity; a list of dicts does not — rows can
  have missing or extra keys, which is the source of many bugs (and why we validate in S7).

### 7. Functions  *(S6)*
- **Maps onto:** a **statistical formula or a coding scheme**: defined once, applied to many cases,
  same rule every time → reproducibility, the thing you care about most as a researcher.
- **Where it breaks:** functions can carry *hidden state* (mutable defaults, globals) so the "same
  input → same output" promise can silently fail. That trap (S6) is the whole reason to learn scope.

### 8. Exceptions & validation  *(S7)*
- **Maps onto:** **data cleaning** — out-of-range Likert values, blank cells, "N/A" typed into a
  numeric field. You already have a mental model of dirty data; exceptions are how code reacts to it.
- **Where it breaks:** cleaning in SPSS is a one-time batch pass; in a program you decide *at runtime*,
  per value, whether to skip, fix, or stop — a more granular control than a recode syntax file.

### 9. Regular expressions  *(S9)*
- **Maps onto:** **search-and-filter in a corpus / qualitative coding** — finding every response
  matching a pattern, extracting IDs, normalizing free-text.
- **Where it breaks:** regex matches *surface form*, not meaning. It's powerful for structure
  (emails, dates, IDs) and treacherous for semantics — the opposite trade-off from human coding.

### 10. Classes / OOP  *(S9)*
- **Maps onto:** an **operational definition / construct** — a `Student` class bundles the
  attributes and behaviors you've decided "count" as a student, like an operationalized variable.
- **Where it breaks:** a construct is a measurement choice; a class is also *behavior* (methods) and
  *enforced rules* (validation in setters), so it's a construct that can defend its own integrity.

---

## Questions to hold while learning (Socratic spine)
These recur across sessions; the teacher should keep returning to them.
1. *Is this a question about value, or about identity?* (drives `==` vs `is`, copy vs alias)
2. *What type is this right now, and who decided that?* (dynamic typing discipline)
3. *Could this input be dirty? What happens if it is?* (defensive mindset)
4. *Is the same rule guaranteed to run the same way every time?* (reproducibility / pure functions)
5. *Is there a more Pythonic, more readable way to say this?* (the Zen of Python's "readability counts")
