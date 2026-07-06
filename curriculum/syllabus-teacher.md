# Learn Python — TEACHER Edition

Everything in the student syllabus, **plus** the instructor scaffolding: a minute-by-minute
clock for each one-hour session, transition scripts (how to move between blocks without dead
air), predicted misconceptions for *this* learner, Socratic prompts (DeepTutor-style — ask,
don't tell), and an explicit **"if you're behind, cut this"** line per session.

The 10 sessions run in five natural pairs (types→traps, control flow→data structures,
functions→recursion, exceptions→files, regex→modules/OOP). Each pair shares a through-line;
**name it out loud** when you open the second session of a pair, so consecutive hours feel
like one arc.

## How to read this document
Each session has:
- **Covers** — the one topic this hour owns.
- **Pre-flight** — what to have open/ready before the student arrives.
- **The clock** — a 60-minute breakdown. Keep a timer visible. The numbers are targets, not law.
- **Transitions** — short scripted lines to hand off cleanly between blocks.
- **Predicted misconceptions** — where THIS learner (expert in research, novice in code) will stumble.
- **Socratic prompts** — questions to ask instead of explaining; let him derive it.
- **Cut line** — the first thing to drop if you're running over.
- **Homework** — what to assign at the close (specs live in `examples/session-NN/practice.md` → *Homework*).

## Universal pacing principles (this learner is fast)
- **Talk less than you want to.** He reads fast and abstracts well. Default to "here's the rule, here's the trap, now you try."
- **Protect the practice block.** ~18 minutes of hands-on in every hour, plus the live-coding he types along with. If concept overruns, steal from your own talking, never from his typing.
- **Predict-then-run is the engine, especially the Session 2 traps.** Always have him *commit to an answer out loud* before running. The cognitive surprise is the teaching moment.
- **The warm-up is homework-powered.** Every session (except S1) opens with 5 minutes on the previous homework + the misconception log. Don't re-teach — quiz. If homework wasn't done, do H1 together as the warm-up and move on.
- **Fast finisher?** Send him to the session's **Extra practice** block, not more of your talking.
- **Don't pad.** Each clock is tight by design. If a block ends early, bank the minutes for practice.
- **Carry a running "misconceptions log"** (DeepTutor "learning memory"): note every trap he hit this session; re-surface it as the next warm-up.

---

## SESSION 1 — Running Python, Variables & Types
**Covers:** REPL vs script, variables as labels, the five core types, `input()`/`print()`, f-strings, casting, reading a traceback.
**Pre-flight:** terminal + VS Code open; `examples/session-01/` ready; a deliberately broken line staged to show a traceback.

**The clock (60 min)**
- **0:00–0:05 — Orientation.** Why Python, why this re-ordered path, how the hour runs, what homework is for. Don't oversell; he wants to start.
- **0:05–0:25 — Concept.** REPL vs script; `python3 file.py`. Variables as *labels on objects* (Connection Map #1). The five core types; `type(x)`. `input()` → always `str`. f-strings. `int()/float()/str()`; `int(3.9)` truncates.
- **0:25–0:37 — Live (he types along).** Build `greet.py`, then "years to graduation"; trigger and *read* one traceback together (last line first).
- **0:37–0:55 — Practice.** `examples/session-01/practice.md` (In class): GPA reporter, age bucket, the string-concatenation trap. Ahead? → Extra practice (f-string drill).
- **0:55–1:00 — Recap + quiz + homework.** Traps recap: `input()` → string; `int(3.9)` truncates; `print(a, b)` vs `print(a + b)`. Quiz S1. Assign homework.

**Transitions**
- Concept→live: *"Enough theory — watch me make these mistakes so you don't have to."*
- Live→practice: *"Your turn. Same moves, your fingers."*
- Close: *"You now know the five types. Next hour is the whole reason this course exists: the ways Python lets those types surprise you."*

**Predicted misconceptions (this learner)**
- Expects `input()` to give a number → `"5" + "3" == "53"`.
- Thinks `=` asserts equality (math habit). Reinforce label-on-object now; it pays off in S2 and in S4's aliasing.
- Expects `int(3.9)` to round.

**Socratic prompts**
- "What type do you think `input()` hands back? How could we check?" (→ `type(...)`)
- "Why did `'5' + '3'` not crash, and not give 8 either?"
- "The traceback is nine lines. Which one pays rent?"

**Cut line:** drop the years-to-graduation demo; never cut the traceback reading or the practice.
**Homework:** unit converter · traceback drill · type-prediction table.

---

## SESSION 2 — The Dynamic-Typing Traps *(the most important hour)*
**Covers:** `==` vs `is`, `bool ⊂ int`, float precision, cross-type comparison, truthiness, `isinstance` vs `type`.
**Pre-flight:** `examples/session-02/`; the trap gauntlet open (site page or notebook); `cheatsheets/traps-and-gotchas.md` ready to hand over at the end.

**The clock (60 min)**
- **0:00–0:05 — Warm-up.** S1 homework debrief: one traceback from his drill, one row of the type table. Log anything shaky.
- **0:05–0:22 — Concept (compressed — the demos carry it).** This is the heart of the course; tell him so. `==` value vs `is` identity (Connection Map #3), `is None`; `bool ⊂ int` (`True == 1`, `sum(flags)`, Connection Map #4); floats are binary → `0.1 + 0.2` → `math.isclose` (Connection Map #5); `5 == "5"` False but `5 > "5"` raises; `isinstance` vs `type`; truthiness.
- **0:22–0:40 — The gauntlet (predict-then-run).** ~18 one-line traps. He predicts every line *out loud* before you run it. This is live and practice fused — his hands on the keyboard, your questions in the air.
- **0:40–0:55 — Practice.** `examples/session-02/practice.md` (In class): the predict-the-output gauntlet on paper, then `clean_score()` handling int/float/str and rejecting `bool`.
- **0:55–1:00 — Recap + quiz + homework.** *"These traps are 80% of week-one bugs."* Hand over the trap cheat sheet as his permanent reference. Quiz S2. Assign homework (the trap journal seeds his bug log).

**Transitions**
- Warm-up→concept: *"You now know the five types. Here's the catch: Python lets them mix in ways that surprise everyone. Cover the right column and predict each line."*
- Concept→gauntlet: *"Rule time is over. Eighteen traps. Say your answer out loud, then we run it."*
- Close: *"Every one of these you predicted wrong goes in your journal tonight — that's the homework, and it becomes your personal cheat sheet."*

**Predicted misconceptions**
- Assumes `is` is a stylistic `==` — nail it with the mutable-list demo.
- Trusts `==` on floats out of stats habit ("I round anyway") — stress the *cause* is binary storage, not data.
- Over-generalizes the `TypeError` and thinks `5 == "5"` errors too. It returns `False` — show it.
- Thinks `"0"` is falsy.

**Socratic prompts**
- "Two students, same 3.7 GPA. `==`? `is`? Why?"
- "If `0.1 + 0.2` isn't `0.3`, is the bug in the data or in the computer? How would you test 'close enough'?"
- "`5 == '5'` is False, fine. So why does `5 > '5'` *crash*?"
- "`sum([True, False, True])` — why is that even legal? And when is it useful?" (→ counting flags)

**Cut line:** drop the small-int-cache and `nan` wrinkles; **never** cut `==`/`is`, floats, `isinstance`, or `clean_score()`.
**Homework:** trap journal · `approx_equal` · `is_missing`.

---

## SESSION 3 — Control Flow: Conditionals & Loops
**Covers:** `if/elif/else`, chained comparisons, `and`/`or`/`not`, `for`/`while`, `range`, `break`/`continue`, `enumerate`/`zip`, the validation loop.
**Pre-flight:** `examples/session-03/`; a messy nested-`if` staged for the refactor; `Ctrl+C` ready for the infinite-loop demo.

**The clock (60 min)**
- **0:00–0:05 — Warm-up.** S2 homework debrief: two entries from his trap journal; quiz `approx_equal(0.1+0.2, 0.3)`.
- **0:05–0:25 — Concept.** `if/elif/else`; **chained comparisons** (`90 <= x < 100` — reads like math); `and/or/not`, short-circuit, `and`/`or` return an *operand*; `while` (+ infinite-loop demo); `for ... in`; `range` (off-by-one!); `break`/`continue`; the `while True: … break` validation pattern; **`enumerate`/`zip`** as the antidote to `range(len(...))`.
- **0:25–0:37 — Live.** A Likert→label classifier (chained comparison + early `return`); sum/average a roster two ways (index vs `enumerate`/`zip`); a robust "ask until valid" loop.
- **0:37–0:55 — Practice.** `examples/session-03/practice.md` (In class): grade-band classifier — **test every boundary** (89.999/90/90.001) — logic drill, `zip` pass/fail, validation loop, mutate-while-iterating trap.
- **0:55–1:00 — Recap + quiz + homework.** `if x == True` → `if x`; `range(1,5)` excludes 5; don't mutate a list you're looping. Quiz S3.

**Transitions**
- Concept→live: *"Watch me turn an ugly five-level `if` into three readable lines — then loop a whole roster."*
- Live→practice: *"Boundaries are where the bugs live. Make 89.999, 90, and 90.001 all behave."*
- Close: *"You can branch and repeat. Next hour: the containers worth looping over — and a list of dicts is secretly your dataset."*

**Predicted misconceptions**
- Writes `if score >= 90 and score < 100` — show chaining `90 <= score < 100`.
- Boundary errors (`>=` vs `>`) at cutoffs — make him test 89.999 / 90 / 90.001.
- `range(len(x))` index habit (from R/SPSS vectorized thinking) — push `enumerate`/`zip`.
- Removes items from a list *while iterating it* → demo the bug, then build a new list.

**Socratic prompts**
- "`x = 5 and 0` — what's `x`? Why isn't it `True`/`False`?"
- "You need both the position and the value. What's cleaner than indexing?"
- "How many numbers does `range(1, 5)` produce? Prove it."

**Cut line:** drop `match/case` and `for/else`; keep chained comparisons, `enumerate`/`zip`, and the validation loop.
**Homework:** attendance labeler · number-guessing game · leap-year checker.

---

## SESSION 4 — Data Structures
**Covers:** `list`/`tuple`/`dict`/`set`, slicing, nesting (list of dicts = dataset), comprehensions, `sorted(key=…)`, aliasing.
**Pre-flight:** `examples/session-04/`; a "list of dicts = tidy dataset" diagram (Connection Map #6); the aliasing demo staged.

**The clock (60 min)**
- **0:00–0:05 — Warm-up.** S3 homework debrief: `label(79.9)`? `is_leap(1900)`? One boundary he got wrong, re-run.
- **0:05–0:25 — Concept.** `list`(mutable)/`tuple`(immutable)/`dict`(key→value)/`set`(unique); indexing & **slicing**; nesting → **a list of dicts is a dataset** (rows as dicts, keys as your variables); list/dict comprehensions; `sorted(key=lambda …)`.
- **0:25–0:37 — Live.** Build a roster as a list of dicts, sort by score, dedupe answers with a `set`, rewrite a loop as a comprehension — then the **aliasing** bug (`b = a`, mutate `a`, watch `b`) and its fix.
- **0:37–0:55 — Practice.** `examples/session-04/practice.md` (In class): rank, `{name: score}` comprehension, group pass/fail, dedupe, reproduce-then-fix aliasing.
- **0:55–1:00 — Recap + quiz + homework.** `=` aliases; `.sort()` returns `None`; `.get()` beats `KeyError`; `[[0]*3]*3` shares rows. Quiz S4.

**Transitions**
- Open (the pair's thread): *"You can loop over data now. This hour: the containers worth looping — and a list of dicts is just a tidy dataset."*
- Live→aliasing: *"One last thing that bites everyone — assignment doesn't copy. Watch `b` change when I never touched it."*
- Close: *"Data's handled. Next hour we stop repeating ourselves: functions."*

**Predicted misconceptions**
- **Aliasing** is the big one — expects `b = a` to copy. Show `a.append(...)` changing `b`; tie to S1 "label on object" and S2 `is`.
- Expects `xs.sort()` to return the sorted list (it returns `None`).
- Reaches for a list when uniqueness is the requirement (→ `set`).

**Socratic prompts**
- "`b = a; a.append(99)` — what's in `b`? Why? (Labels, not boxes.)"
- "Survey gave duplicate free-text answers. What structure removes duplicates for free?"
- "Each dict is a row, each key a column. What's your unit of analysis here?"

**Cut line:** drop deep-copy/`[[0]*3]*3` (homework covers the grid); keep comprehensions and aliasing basics.
**Homework:** gradebook dict drill · frequency counter · fix-the-grid.

---

## SESSION 5 — Functions, Scope & Reusability
**Covers:** `def`, parameters (positional/keyword/default, `*args`/`**kwargs`), `return` vs `print`, LEGB scope, docstrings, type hints, the mutable-default bug.
**Pre-flight:** `examples/session-05/`; the **mutable-default-arg** demo staged (the headline); S4's inline code ready to refactor.

**The clock (60 min)**
- **0:00–0:05 — Warm-up.** S4 homework debrief: the grid bug — *why* did every row change? (Aliasing, again. It should be automatic now.)
- **0:05–0:25 — Concept.** `def`; parameters (positional/keyword/default, `*args`/`**kwargs`); `return` vs `print`; scope (LEGB), `global` and why to avoid it; docstrings; **type hints** ("not enforced; `mypy` checks them").
- **0:25–0:37 — Live.** Refactor S4 inline code into `class_average`/`letter_grade`; then the **mutable-default bug** live (`def add(x, bag=[])` accumulating across calls) → fix with `bag=None`.
- **0:37–0:55 — Practice.** `examples/session-05/practice.md` (In class): grade-functions library with hints/docstrings; reproduce-then-fix the mutable default; `summary(*scores)`.
- **0:55–1:00 — Recap + quiz + homework.** Mutable default → `None`; forgot `return` → `None`; assigning a global → `UnboundLocalError`; hints aren't enforced. Quiz S5.

**Transitions**
- Concept→live: *"This next bug has burned every Python programmer once. Watch the list keep growing across calls."*
- Live→practice: *"Now you cause the bug on purpose, then cure it. Bugs you've caused are bugs you recognize."*
- Close: *"A function can call other functions. Next hour, the mind-bender: it can call itself."*

**Predicted misconceptions**
- Won't believe the default list persists until shown twice; then explain defaults evaluate *once, at definition* — and note it's the S4 aliasing story again.
- Thinks a function that `print`s has "returned" the value → show `x = show(...)` is `None`.
- Expects type hints to enforce types → show `add("a","b")` still runs.

**Socratic prompts**
- "I called `add(1)` three times and the list keeps growing. When does `bag=[]` actually run?"
- "`print` vs `return` — which lets the *next* function use the result?"
- "Where does Python look for a name first? (L-E-G-B — walk it.)"

**Cut line:** drop decorators/closures and keyword-only args (Extra practice has them); **never** cut the mutable-default demo.
**Homework:** tiny stats library · `mean_ignoring_none` · scope prediction.

---

## SESSION 6 — Recursion & Recursive Thinking
**Covers:** base case + recursive case, tracing the call stack, recursion vs iteration, nested data, `RecursionError`.
**Pre-flight:** `examples/session-06/`; a nested-JSON-shaped dict staged for `deep_sum`; the `runaway` overflow + `sys.getrecursionlimit()` queued.

**The clock (60 min)**
- **0:00–0:05 — Warm-up.** S5 homework debrief: `mean_ignoring_none(None)`? The scope drill — what error, and why?
- **0:05–0:25 — Concept.** The two parts: a **base case** and a **recursive case** that moves toward it. Trace `orderings(3)` as a stack that builds then unwinds; recursion vs iteration; the cost (each pending call is a frame; **no tail-call optimization**, limit ≈ 1000). The prereq-chain example (`prereqs_deep`).
- **0:25–0:37 — Live.** `countdown`/`factorial`, then `deep_sum` over nested data (the payoff a single loop can't reach), then a `RecursionError` read together. Mention `@functools.cache`.
- **0:37–0:55 — Practice.** `examples/session-06/practice.md` (In class): recursive `total`, `reverse`, `flatten`, `depth`, and the two trap-fixes (missing base case; forgetting to `return`).
- **0:55–1:00 — Recap + quiz + homework.** Reachable base case or overflow; `return` the recursive call; loops for flat work. Quiz S6.

**Transitions**
- Open (the pair's thread): *"A function can call other functions. The mind-bender: it can call *itself*. That's exactly the tool for data defined in terms of itself — nested data."*
- Live→practice: *"Say the base case out loud before you write the function — that's where the bugs hide."*
- Close: *"You handle clean data beautifully. Next hour: what to do when the data fights back."*

**Predicted misconceptions**
- Writes the recursive case but forgets to `return` it → silent `None`.
- From a vectorized stats background, may not see when recursion beats a loop → the nested-data demo is the "aha".
- May assume recursion is a free swap for loops → show the limit.

**Socratic prompts**
- "What's the smallest input where the answer is obvious without recursing? That's your base case."
- "Your data is a list that can contain lists. What kind of function matches a thing defined in terms of itself?"
- "Each pending call sits on a stack. What happens at call #1001?"

**Cut line:** drop `depth`/string-reverse tasks and `@cache`; **never** cut `deep_sum` on nested data.
**Homework:** `sum_digits` · `deep_count` · loop-vs-recursion paragraph.

---

## SESSION 7 — Exceptions & Defensive Code
**Covers:** `try`/`except`/`else`/`finally`, exception types, `raise`, EAFP vs LBYL, `assert`, a first `pytest` test.
**Pre-flight:** `examples/session-07/`; a dirty list ("N/A", "", "7" on a 1–5 scale) staged; `pytest` installed and verified.

**The clock (60 min)**
- **0:00–0:05 — Warm-up.** S6 homework debrief: `sum_digits(4823)` trace; why did `deep_count` need the bool check? (S2 pays rent again.)
- **0:05–0:25 — Concept.** Errors vs exceptions; `try/except/else/finally`; common types (`ValueError`, `KeyError`, `FileNotFoundError`); `raise ValueError(...)`; **EAFP** vs LBYL; `assert` (a developer check, can be disabled — not input validation).
- **0:25–0:37 — Live.** Harden `safe_int()`/`clean_likert()` against blanks/"N/A"/out-of-range; a first `pytest.raises` test, run it, watch it pass.
- **0:37–0:55 — Practice.** `examples/session-07/practice.md` (In class): validate a raw response list into clean values + a rejection log; add a `raise`; one pytest test.
- **0:55–1:00 — Recap + quiz + homework.** Never bare `except:`; don't swallow errors; `assert` ≠ validation. Quiz S7.

**Transitions**
- Open: *"Your real survey data WILL have 'N/A' in a numeric column. This hour we write code that shrugs it off."*
- Live→practice: *"Here are eight dirty values. I want a clean list AND a rejection log — you never silently discard data."*
- Close: *"You can survive one bad value. Real data is a *file full* of them — next hour we open a real CSV and clean it with exactly these moves."*

**Predicted misconceptions**
- Reaches for `if/else` (LBYL) everywhere; introduce EAFP as the Pythonic default, but be honest both are valid.
- Writes bare `except:` — show why `except ValueError:` is safer.
- Confuses `raise` with `return`, and `assert` with input validation.

**Socratic prompts**
- "User typed 'seven' instead of 7. Catch it *before* (`if`) or *after* (`try`)? Trade-offs?"
- "Why is a bare `except:` dangerous? What might you swallow?"
- "You rejected four values. Should the program say so? Where's the audit trail?"

**Cut line:** drop the custom exception subclass (Extra practice has it) and shrink pytest to one test; keep `try/except` validation.
**Homework:** `ask_int` · three pytest cases · error triage.

---

## SESSION 8 — Files, Libraries & Research Data
**Covers:** `open`/`with`, file modes, CSV via `DictReader`/`DictWriter`, `json`, the researcher's stdlib, the pandas teaser.
**Pre-flight:** `examples/session-08/` with `students.csv` + `survey.csv`; confirm `pip` works and have `pandas` importable for the teaser.

**The clock (60 min)**
- **0:00–0:05 — Warm-up.** S7 homework debrief: one error-triage item; `ask_int` — what happens on `" 42 "`, and why does EAFP win there?
- **0:05–0:25 — Concept.** `open`/`with` (auto-close); modes (`r/w/a`; **`w` overwrites!**); **CSV** via `csv.DictReader`/`DictWriter` (rows as dicts → ties to S4); `json`; researcher stdlib (`statistics`, `datetime`, `pathlib`); `pip install`.
- **0:25–0:37 — Live.** Read `students.csv` → list of dicts, class mean with `statistics.mean`, write a summary CSV; then the **`pandas` teaser** (*"same thing in three lines — that's your next course"*).
- **0:37–0:55 — Practice.** `examples/session-08/practice.md` (In class): per-item survey means skipping dirty values, write `survey_summary.csv`, mean by major — S7's exception skills do the cleaning.
- **0:55–1:00 — Recap + quiz + homework.** Bare `"w"` destroys data; `newline=""`; files exhaust after one read; CSV values are strings. Quiz S8.

**Transitions**
- Open (the pair's thread): *"You can now survive one bad value. Real data is a file full of them — let's open a real CSV."*
- Teaser framing: *"Everything you just did by hand, pandas does in three lines — your next course, not today's. Now you know what it's doing underneath."*
- Close: *"Numbers are clean. Next hour: the messiest data of all — text."*

**Predicted misconceptions**
- Opens with `"w"` to read and wonders why the file is empty; stress mode meanings.
- Expects to iterate a file object twice without re-opening; show the exhausted cursor.
- Forgets CSV values are strings (`"91" + 1` → `TypeError` — S2 again).

**Socratic prompts**
- "Why does `with` matter even if your program crashes? What does it guarantee?"
- "The score column came back as `'91'`. What must happen before math?"
- "Your summary has `True` in it. What will JSON write there?" (→ `true` — JSON is its own language)

**Cut line:** drop the `pandas`/`json` teaser; keep `csv.DictReader/Writer` and the dirty-value cleaning.
**Homework:** attendance-report pipeline · JSON round-trip · your own CSV.

---

## SESSION 9 — Regular Expressions & Text Cleaning
**Covers:** raw strings, the survival tokens, `search`/`fullmatch`/`findall`/`sub`, capture groups, when NOT to use regex.
**Pre-flight:** `examples/session-09/`; messy free-text, emails, and "Last, First" names staged; regex101.com open (flavor: Python).

**The clock (60 min)**
- **0:00–0:05 — Warm-up.** S8 homework debrief: what did JSON do to `True`? What dirty value did his own CSV throw, and how did he handle it?
- **0:05–0:25 — Concept.** Why regex for a researcher (validate/extract/clean/qualitative-coding, Connection Map #9). **Raw strings** `r"..."`. Survival tokens (`. \d \w \s + * ? {m,n} ^ $ [] () |`); `.` matches *any* char (use `\.`). The four functions: `search`/`fullmatch`/`findall`/`sub`; capture groups.
- **0:25–0:37 — Live.** Validate an email (`fullmatch`), extract dept+number with groups, collapse whitespace with `sub`, count `#hashtags` with `findall` — and one case where `.split()` beats regex.
- **0:37–0:55 — Practice.** `examples/session-09/practice.md` (In class): email validator, extract codes, hashtag count, the `"Last, First"` flip, the judgment call.
- **0:55–1:00 — Recap + quiz + homework.** `r"..."` always; `\.` for a literal dot; guard `None` before `.group()`. Quiz S9.

**Transitions**
- Concept→live: *"Four functions cover almost everything: search, fullmatch, findall, sub. Every pattern is a raw string, no exceptions."*
- Live→practice: *"Regex matches form, not meaning. You decide what the pattern should be — then make Python agree."*
- Close: *"You can now clean any string. Last hour of new material: organizing your code so it's reusable."*

**Predicted misconceptions**
- Forgets raw strings → backslash chaos. Always `r"..."`.
- Calls `.group()` on a `None` result → teach the `if m:` guard (same shape as `5 > '5'` from S2).
- Expects regex to understand meaning (qualitative-coding hopes) — it matches *form*.

**Socratic prompts**
- "You want every response mentioning a theme. Is that a *form* match (regex) or a *meaning* match (human coding)? What can regex actually catch?"
- "Why does `re.search(...).group()` crash when there's no match? (Same shape as `5 > '5'` weeks ago.)"
- "Would you regex-split `'a,b,c'`? What's the simpler tool?"

**Cut line:** drop named groups / `re.VERBOSE` (Extra practice has named groups); keep validate + extract + `sub`.
**Homework:** pattern drill · messy-name cleanup · domain harvest.

---

## SESSION 10 — Modules, OOP & the Pythonic Toolkit
**Covers:** modules & `import`, the `__main__` guard, a class with `__init__`/`self`/`__str__`, a validating `@property`, inheritance, generators, `map`/`filter`, walrus.
**Pre-flight:** `examples/session-10/`; `grades.py` ready to import; the `Student` class and the generator-exhaustion demo staged.

**The clock (60 min)**
- **0:00–0:05 — Warm-up.** S9 homework debrief: his three patterns — run each against one *invalid* example; did `fullmatch` catch it?
- **0:05–0:25 — Concept.** Modules: move grade functions to `grades.py`, `import`, the `if __name__ == "__main__":` guard. OOP: a small `Student` class — `__init__`, `self`, a method, `__str__`, a validating `@property` setter (Connection Map #10), brief inheritance with `super()`.
- **0:25–0:37 — Live.** Build the validating `Student`; `ana.gpa = 5.0` raises — the object defends its own integrity. Then the toolkit tour-by-doing: comprehension, `map`/`filter`, a generator + its one-pass exhaustion, the walrus `:=`.
- **0:37–0:55 — Practice.** `examples/session-10/practice.md` (In class): import from `grades.py`, the validating `Student`, `GradStudent(super())`, toolkit drills.
- **0:55–1:00 — Recap + quiz + homework + course wrap.** `self` is just "this instance"; generators exhaust; don't class-ify what a dict does. Quiz S10. Frame the capstone: *"Next time, you drive."*

**Transitions**
- Open (the pair's thread): *"You can now clean any string. Last step: organize your code so it's reusable — functions into modules, then data-plus-behavior into a class."*
- Modules→OOP: *"Functions in a file is reuse. A class bundles the data *and* the rules that guard it."*
- Close: *"That's the toolbox — every tool in it earned its place. The capstone is where you prove it's yours."*

**Predicted misconceptions**
- `self` looks magical — it's just "this particular instance."
- Treats a generator like a list (iterates once) → show the second pass is empty.
- Reaches for a class when a function or dict would do — name when OOP earns its keep.

**Socratic prompts**
- "Your operational definition of 'student' — what attributes and rules belong to it? That's your class."
- "A million rows won't fit in memory. What does `yield` give you that a list doesn't?"
- "Why does the demo code in `grades.py` NOT run when you import it?"

**Cut line:** drop `@dataclass` (Extra practice) and compress the toolkit tour to comprehensions + generators; keep modules and the validating class.
**Homework:** `Student` with computed GPA · `Cohort` class · Pythonic rewrite.

---

## SESSION 11 (Optional) — Capstone
**Role shift:** you stop teaching and start *coaching*. He drives; you ask questions and unblock. Plan ~2 hours.
- **0:00–0:15 — Brief & plan.** He restates the goal and sketches the steps aloud (pseudocode). You only check the plan is sound.
- **0:15–1:05 — Build.** He codes the Gradebook & Survey Analyzer (`assessments/capstone-project.md`). Intervene only when stuck >3 min; prefer a question over an answer.
- **1:05–1:13 — Break.**
- **1:13–1:45 — Build, continued.** Finish the report CSV, then one stretch goal (a `Student` class, a regex validation, or the recursive nested-data total).
- **1:45–1:55 — Review.** Walk his code for the course's traps (identity, aliasing, mutable defaults, bare `except:`). Praise readability.
- **1:55–2:00 — Debrief & next steps.** Point to pandas/visualization as the genuine next course.

**Coaching prompts:** "What's your data structure?" · "What happens if that cell is blank?" · "Is that comparing value or identity?" · "Could that be one comprehension?"

---

## Instructor's running checklist (use across all sessions)
- [ ] Timer visible; the practice block got its full ~18 minutes.
- [ ] Warm-up pulled from the homework and the misconceptions log — not improvised.
- [ ] Pair through-lines named out loud (S2, S4, S6, S8, S10 openings).
- [ ] Every trap demoed via **predict-then-run**, not narration.
- [ ] Each new concept hooked to the **Connection Map** before syntax.
- [ ] Student typed everything himself; you talked less than half the session.
- [ ] End-of-session quiz given; homework assigned by name; capstone kept in view as the destination.
