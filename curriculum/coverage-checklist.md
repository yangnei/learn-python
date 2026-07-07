# Session-by-Session Coverage Checklist

> The teacher's tick-list: every point each session must land, split by half.
> Print it, keep it next to the clock, and check items off as you go. A session is
> "covered" when every unticked box has been *deliberately* cut (see each session's
> cut line in the playbook), not forgotten. Codes: **C** = core hour, **D** = going
> deeper, **T** = trap to demo predict-then-run.

---

## Session 1 — Running Python, Variables & Types

**C — Core hour**
- [ ] REPL (`python3`, `>>>`) vs script (`python3 file.py`); when to use each
- [ ] Variables are **labels on objects**, not boxes; `=` is an action, so `n = n + 1` is legal
- [ ] The five core types: `int`, `float`, `str`, `bool`, `None`; `type(x)` to inspect
- [ ] `input()` **always returns `str`** → `"5" + "3" == "53"`; convert immediately
- [ ] `print()` with commas (space-joined) vs `+` (same types only)
- [ ] f-strings: `{x}`, `:.1f`, `:,`, `:.1%`
- [ ] Casting: `int()`, `float()`, `str()`; `int(3.9)` **truncates**; `round()` rounds
- [ ] Reading a traceback: **last line first** — exception name + offending value

**D — Going deeper**
- [ ] Full operator set: `+ - * / // % **`; precedence follows math; parenthesize when unsure
- [ ] Augmented assignment: `+= -= *=`
- [ ] `%` in practice: even/odd, rotating into k groups, `//`+`%` = whole units + remainder (130 min → 2 h 10 min)
- [ ] String methods: `.strip() .title() .lower() .count() .startswith()`, `in`, `len()`; **chaining**
- [ ] Strings are immutable — methods **return new strings**; repetition `"ab" * 3`, `"=" * 40` dividers
- [ ] f-strings round 2: alignment `:<10` `:>8`, `{x=}` debugging form
- [ ] `print()` fine-tuned: `sep=`, `end=`; escape sequences `\n`, `\"`; quote alternation
- [ ] `import math`: `sqrt`, `floor`, `ceil`, `pi` — "borrowing a toolbox" (full story S8)
- [ ] Self-help: `help(round)`, `dir(str)`, REPL `_`
- [ ] Naming: snake_case, meaningful names, `UPPER` constants, comments say *why*, pseudocode-first habit

**T — Traps (4):** `"5" + "3"` · `"Age: " + 21` → TypeError · `int(3.9)` → 3 · `.upper()` doesn't mutate

**Practice:** C → GPA reporter, age bucket, string-concat trap; D → aligned gradebook lines, name normalizer, `%`-groups
**Homework:** unit converter · traceback drill · type-prediction table

---

## Session 2 — The Dynamic-Typing Traps

**C — Core hour**
- [ ] `==` (value) vs `is` (identity); `is` reserved for `None`/`True`/`False`
- [ ] `b = a` does not copy — mutation shows through both names; copy via `list(a)` / `a[:]`
- [ ] `bool ⊂ int`: `True == 1`, `5 + True == 6`, `sum(flags)` counts Trues
- [ ] `isinstance(True, int)` True but `type(True) is int` False — subclass awareness
- [ ] `/` always float; `//` floors toward −∞ (`-7 // 2 == -4`)
- [ ] Floats are binary: `0.1 + 0.2 != 0.3`; **never `==` floats** → `math.isclose`
- [ ] Cross-type: `5 == "5"` → False (no error); `5 > "5"` → TypeError
- [ ] List ≠ tuple even with equal contents; sequences compare element-by-element
- [ ] Truthiness: falsy = `0 0.0 "" [] {} set() None`; `"0"`/`"False"`/`[0]` are truthy; `if scores:` idiom
- [ ] The ~18-trap gauntlet, every prediction **out loud**

**D — Going deeper**
- [ ] `None` = absence; `is None` test; no-`return` functions give `None`; None vs `""` vs `0` (three "nothings")
- [ ] The conversion matrix: `int("4.2")` fails, `int(float("4.2"))` two-step, `str()` takes anything; **convert at the edge, once**
- [ ] `nan`: `nan != nan`, `math.isnan`; `inf` comparisons; where NaN appears in real pipelines
- [ ] Mutable vs immutable table; `id()` is what `is` compares; why immutables are safe to share
- [ ] `Decimal("0.1") + Decimal("0.2") == Decimal("0.3")`; build **from strings**; when floats aren't acceptable; `Fraction` exists
- [ ] Chained equality `a == b == c`, `1 <= x <= 5`; don't chain `is`

**T — Traps (18):** `is` on equal lists · alias append · `True == 1` · `5 + True` · `sum(bools)` · `0.1+0.2` · `== 0.3` · `nan == nan` · `7/2` · `-7//2` · `"5" == 5` · `5 > "5"` · list vs tuple · `type(True) is int` · `isinstance(True, int)` · `bool("0")` · `bool([])` · small-int cache 257

**Practice:** C → paper gauntlet, `clean_score()` (rejects `bool`!); D → conversion predictions, Decimal re-run, `describe(x)`
**Homework:** trap journal (5 traps, own words) · `approx_equal` · `is_missing`

---

## Session 3 — Control Flow: Conditionals & Loops

**C — Core hour**
- [ ] `if/elif/else`; indentation defines blocks; first true branch wins
- [ ] **`if` vs `elif`**: stacked `if`s are independent questions and ALL fire (double-label bug); `elif` = one ladder
- [ ] Comparison operators; **chained comparisons** `0 <= score <= 100`
- [ ] `and/or/not`; short-circuit; `and`/`or` return an **operand** (`5 and 0` → `0`; `"" or "N/A"` idiom)
- [ ] Never `if x == True` — just `if x:`
- [ ] `while` (+ Ctrl+C for infinite loops); `for ... in`; `range` **excludes the stop**
- [ ] `for _ in range(3)` — the underscore convention for unused values
- [ ] `break` / `continue`
- [ ] `enumerate` / `zip` instead of `range(len(...))`
- [ ] The `while True: … break` validation loop

**D — Going deeper**
- [ ] The ternary `x if cond else y` — tiny choices only
- [ ] **Return the test itself**: `return score >= 60`, never `if ...: return True`; call helpers bare (`if is_passing(s):`)
- [ ] `match/case`: literals, `|` alternatives, `_` default; its niche = one value vs literals
- [ ] `for/else` — search without a `found` flag (else = no break)
- [ ] Nested loops; `break` exits inner only → function + `return` escape
- [ ] The four named patterns: accumulator, counter, best-so-far, sentinel

**T — Traps (3):** `"" or 'Anonymous'` · `range(1,5)` · `all(gen)` with one failure

**Practice:** C → grade-band classifier (test 89.999/90/90.001!), logic drill, zip pass/fail, validation loop, mutate-while-iterating, double-label bug; D → match/case rewrite, for/else search, best+worst one pass, return-the-test rewrite
**Homework:** attendance labeler · number-guessing game · leap-year checker

---

## Session 4 — Data Structures

**C — Core hour**
- [ ] The four containers: list (mutable/ordered), tuple (immutable record), dict (key→value), set (unique)
- [ ] Indexing, negative indices, **slicing** (`[1:3]`, `[:2]`, `[::-1]`); stop excluded
- [ ] `.append()`, `.sort()` mutates in place and **returns None**; `sorted()` returns new
- [ ] Dict access, `.get(k, default)`, add/update, `.items()`
- [ ] **A list of dicts is a dataset** — rows as dicts, keys as variables
- [ ] Sets: dedupe, fast membership
- [ ] Comprehensions: list, filtered, dict, set — "expr, for each, if"
- [ ] `sorted(key=lambda …)`, `reverse=True`
- [ ] **Aliasing**: `b = a` shares; `.copy()`; `[[0]*3]*3` shares one row

**D — Going deeper**
- [ ] Unpacking: `name, score = pair`, `head, *rest`, swap; zip-loops ARE unpacking
- [ ] Dict power methods: `.setdefault`, `.pop(k, default)`, `d1 | d2` merge, `.keys/.values/.items`
- [ ] `Counter`: the tally loop in one line; `.most_common(n)`
- [ ] `defaultdict(list)` grouping
- [ ] Set algebra: `& | - ^`, subset `<=`; ordered dedupe `dict.fromkeys`
- [ ] Multi-key sorts: tuple keys `(-score, name)`; sort stability
- [ ] `copy` vs `deepcopy` — nested + mutating inners → deepcopy

**T — Traps (3):** `[[0]*3]*3` grid · `.get()` missing key · `[::-1]` reversed copy

**Practice:** C → rank, dict comprehension, group pass/fail, dedupe, aliasing reproduce+fix; D → Counter + most_common, defaultdict grouping, multi-key sort, ordered dedupe
**Homework:** gradebook dict drill · frequency counter · fix-the-grid

---

## Session 5 — Functions, Scope & Reusability

**C — Core hour**
- [ ] `def`, calling, docstrings; a function = a formula/coding scheme (reproducibility)
- [ ] `return` vs `print` — `x = show(...)` is `None`
- [ ] Parameters: positional, keyword, defaults; **defaults must be immutable**
- [ ] `*args` (→ tuple), `**kwargs` (→ dict); unpacking `f(*lst)`, `f(**dct)`
- [ ] **The mutable-default bug**, shown live twice; fix = `None` + create inside
- [ ] Scope LEGB; assigning makes a name local → `UnboundLocalError`; avoid `global`, return instead
- [ ] Type hints document, are **not enforced** (`mypy`); docstring field conventions (`:param:` …) + Sphinx pointer

**D — Going deeper**
- [ ] Functions are objects: assign, pass, dict dispatch — `key=` demystified
- [ ] `lambda`: one expression only; name anything bigger
- [ ] Closures: `make_curver(bonus)` factory; capture-by-variable (the lambda-in-loop trap)
- [ ] A first decorator: `@announce`; write `f = announce(f)` long-hand FIRST; where he'll meet them (`@property`, `@cache`, `@pytest.mark`)
- [ ] Keyword-only args (`*,`) for readable call sites
- [ ] Doctests: `>>>` examples in docstrings; `python -m doctest`

**T — Traps (3):** mutable default persists · print-not-return `is None` · closure late binding

**Practice:** C → grade-functions library, mutable-default reproduce+fix, `summary(*scores)`; D → `apply_to_all`, curve factory, `@announce`, doctest
**Homework:** tiny stats library · `mean_ignoring_none` · scope prediction

---

## Session 6 — Recursion & Recursive Thinking

**C — Core hour**
- [ ] The two parts: **base case** (stops) + **recursive case** (moves toward it); say the base case aloud first
- [ ] Trace the call stack building and unwinding (`orderings(3)`)
- [ ] Each pending call = a stack frame
- [ ] Recursion vs iteration; loops win for flat sequences
- [ ] **Nested data is the payoff**: `deep_sum` over lists/dicts/JSON
- [ ] `RecursionError`; no tail-call optimization; limit ≈ 1000
- [ ] Must **return** the recursive call — else silent `None`

**D — Going deeper**
- [ ] Memoization: naive `fib` re-solves subproblems; `@functools.cache` (decorator payoff); when caching helps (repeated subproblems only)
- [ ] Binary search: halve a **sorted** roster; log₂ intuition (1,000 → ~10 looks)
- [ ] Tree-shaped data: org chart `count_people`; function shape mirrors data shape
- [ ] Explicit-stack conversion: `flatten_iter` with a to-visit list — no frames, no limit
- [ ] The decision checklist: flat→loop · nested→recursion · repeated→cache · deep→stack

**T — Traps (3):** no base case → RecursionError · missing `return` → None · `sys.getrecursionlimit()` = 1000

**Practice:** C → recursive `total`, `reverse`, `flatten`, `depth`, two trap-fixes; D → binary search + step counter, org-tree count + deepest, `flatten` without recursion
**Homework:** `sum_digits` · `deep_count` · loop-vs-recursion paragraph

---

## Session 7 — Exceptions & Defensive Code

**C — Core hour**
- [ ] Syntax errors vs runtime exceptions
- [ ] `try/except`; **keep the try block small**; `except ValueError: pass` = visible deliberate skip (log if in doubt)
- [ ] The common types on sight: `ValueError`, `TypeError`, `KeyError`, `IndexError`, `ZeroDivisionError`, `FileNotFoundError`
- [ ] `try/except/else/finally` — else = no exception; finally = always
- [ ] `raise ValueError(...)` deliberately; caller decides
- [ ] EAFP vs LBYL — both valid; EAFP is the Pythonic default
- [ ] `assert` = developer check, disableable, **never input validation**
- [ ] A first pytest test: `test_` naming, `assert`, `pytest.raises`

**D — Going deeper**
- [ ] The exception family tree; handlers tried top-down → **specific before broad**; catch a tuple; `except Exception` only to log-and-stop
- [ ] Custom exceptions that carry data (`SurveyError` with `.value`)
- [ ] `raise ... from` — domain error on top, real cause beneath
- [ ] `finally` → the cleanup mindset; `with` is this packaged (S8 bridge)
- [ ] `logging` vs `print`: output vs diary; levels; `basicConfig` format
- [ ] pytest round 2: `@pytest.mark.parametrize`; arrange-act-assert; test the **edges**; print-only functions aren't testable — return values

**T — Traps (4):** `int("3.0")` · `round(2.5)` banker's · `0.1+0.2+0.3 == 0.6` · `int("1_000")`

**Practice:** C → clean the raw list + rejection log, add a `raise`, one pytest test; D → fix except-order bug, `SurveyError` + `raise from`, logging conversion, parametrize
**Homework:** `ask_int` · three pytest cases · error triage

---

## Session 8 — Files, Libraries & Research Data

**C — Core hour**
- [ ] `open`/`with` — auto-close even on crash
- [ ] Modes: `r` / **`w` truncates immediately!** / `a` append (`f.write`, `\n` is your job) / binary `rb`/`wb` exist
- [ ] Reading: `.read()`, line-by-line iteration, `.rstrip()`; file objects exhaust after one pass
- [ ] CSV in: `csv.DictReader`, rows as dicts, `newline=""`; **values are strings — convert!**
- [ ] Why `csv` exists (fields containing commas beat `.split(",")`)
- [ ] CSV out: `DictWriter`, `writeheader`, `writerow`
- [ ] Researcher's stdlib: `statistics` (mean/median/stdev), `random`, `datetime`, `pathlib`
- [ ] `pip install` + PyPI; `cowsay` (installing is trivial)

**D — Going deeper**
- [ ] `pathlib` tour: `/` joins, `.exists`, `.stat().st_size`, `.glob`/`.rglob`, `mkdir(exist_ok=True)`, `read_text`/`write_text`
- [ ] Encodings: say `encoding="utf-8"`; Excel's BOM → `utf-8-sig`; mojibake symptom
- [ ] `csv.reader` (lists) vs `DictReader` (dicts); `writerows`; `delimiter=";"`
- [ ] JSON: nested data, `dumps(indent=2)`/`loads`, `True`→`true`, `None`→`null`
- [ ] APIs taste: `requests.get(url, params=...).json()` — fetch a URL, parse the JSON
- [ ] `datetime`: `strptime` (parse) vs `strftime` (format); date arithmetic `.days`; `fromisoformat`
- [ ] `random` with `seed()` → **reproducible** sampling; `sample` vs `choice`; `shuffle`
- [ ] Scripts with arguments: `sys.argv` (list of strings, `[0]` = script), guard `len()`, `sys.exit("usage")`, slice `[1:]`; `argparse` pointer
- [ ] Binary in practice: Pillow `Image.open`, animated GIF (`save_all`, `append_images`, `duration`, `loop`)
- [ ] pandas teaser: `read_csv`, `.describe()`, `groupby().agg()`, boolean filter, `to_csv`

**T — Traps (3):** CSV strings `'91' + 1` · `json.dumps(True)` → `true` · exhausted file cursor

**Practice:** C → per-item survey means skipping dirty values, `survey_summary.csv`, mean by major; D → pathlib inventory, days-between, seeded sample, CSV→JSON, argv-guarded `report.py`, Pillow GIF
**Homework:** attendance-report pipeline · JSON round-trip · your own CSV

---

## Session 9 — Regular Expressions & Text Cleaning

**C — Core hour**
- [ ] Why regex for a researcher: validate / extract / clean / first-pass qualitative coding; matches **form, not meaning**
- [ ] **Raw strings always**: `r"..."`
- [ ] Survival tokens: `.` `\d \w \s` (+ negations) `+ * ?` `{m,n}` `^ $` `[abc] [a-z] [^abc]` `(...)` `|`
- [ ] The `.` trap; escaping literals `\.`
- [ ] The four functions: `search` / `fullmatch` (validation — anchors both ends) / `findall` / `sub`
- [ ] Capture groups: `group(0/1/2)`, `m.groups()`; **`m` may be `None` — guard before `.group()`**
- [ ] Cleaning recipes: collapse whitespace, `findall` + `Counter`, group-reorder `r"\2 \1"`
- [ ] When NOT to use regex: `.split()`, `.strip()`, `.replace()`, `.removeprefix()`

**D — Going deeper**
- [ ] Flags: `IGNORECASE`, `MULTILINE` (^$ per line), `DOTALL`; combining with `|`
- [ ] `re.compile` — name your patterns, reuse as methods
- [ ] `re.VERBOSE` — commented, reviewable patterns
- [ ] Named groups `(?P<dept>...)` + `groupdict`; non-capturing `(?:...)`
- [ ] Greedy vs lazy: `.+` vs `.+?` (bracketed/quoted content wants lazy)
- [ ] `re.sub` with a **function** replacement — the anonymizer (closure!)
- [ ] Regex + files: `findall` over `Path.read_text()` (S8 bridge)

**T — Traps (3):** greedy `\[(.+)\]` · `re.match` anchors at start · `.` in `grades.csv` matches X

**Practice:** C → email validator, extract codes, hashtag count, "Last, First" flip, judgment call; D → VERBOSE email, anonymizer, two-format date harvest, flag count
**Homework:** pattern drill · messy-name cleanup · domain harvest

---

## Session 10 — Modules, OOP & the Pythonic Toolkit

**C — Core hour**
- [ ] Modules: a `.py` file; `import` / `from ... import`; no copy-paste reuse
- [ ] The `if __name__ == "__main__":` guard — script AND library
- [ ] A class = an operational definition; `__init__`, `self`, attributes, methods, `__str__`
- [ ] `@property` + setter validation — the object defends its integrity; `_attr` privacy convention
- [ ] Inheritance: `GradStudent(Student)`, `super().__init__`, override `__str__`
- [ ] Toolkit: comprehensions, `map`, `filter`, `enumerate`, `zip`
- [ ] Generators: `yield`, lazy, **exhaust after one pass**; walrus `:=`

**D — Going deeper**
- [ ] `__repr__` (developers) vs `__str__` (people); `__eq__`; `__lt__` → `sorted()` with no key; `__add__` = operator overloading
- [ ] Dataclasses round 2: defaults, **`field(default_factory=list)`** (the S5 rule in class form), `frozen=True`
- [ ] `@classmethod` alternate constructor `from_row` (CSV at the edge, objects inside); `@staticmethod` third flavor
- [ ] Composition over inheritance: Cohort HAS Students; inherit only for true is-a
- [ ] Class vs instance attributes — mutable data in `__init__`, always; object state beats `global`
- [ ] Generator pipelines: chained stages, lazy, constant memory; the `iter()`/`next()` protocol underneath
- [ ] From script to project: folder layout, one module per concern, `def main()` convention, `tests/` (+ `__init__.py` note)

**T — Traps (3):** generator exhausts · dataclass `__eq__` · shared class-variable list

**Practice:** C → import from `grades.py`, validating `Student`, `GradStudent`, toolkit drills; D → sortable `Student`, dataclass `Course`, `from_row`, two-stage pipeline
**Homework:** `Student` with computed GPA · `Cohort` class · Pythonic rewrite

---

## Session 11 (Optional) — Capstone

- [ ] Brief restated by the student in pseudocode before any code
- [ ] Reads both CSVs; cleans & validates (skip/flag dirty, range checks)
- [ ] Computes: class mean/median/stdev, mean by major, per-item survey means + n
- [ ] Flags at-risk students (< 60)
- [ ] Writes `report.csv`
- [ ] Organized: helper module or class, docstrings + hints, `main()` + guard
- [ ] Review pass hits the course traps: identity, aliasing, mutable defaults, bare except
- [ ] One stretch goal attempted (class / regex / recursive total / argparse)
- [ ] Debrief: pandas & visualization named as the next course
