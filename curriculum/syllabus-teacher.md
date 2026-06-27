# Learn Python — TEACHER Edition

Everything in the student syllabus, **plus** the instructor scaffolding: a minute-by-minute clock
for each hour, transition scripts (how to move between blocks without dead air), predicted
misconceptions for *this* learner, Socratic prompts (DeepTutor-style — ask, don't tell), and an
explicit **"if you're behind, cut this"** line per session.

## How to read this document
Each session has:
- **Pre-flight** — what to have open/ready before the student arrives.
- **The clock** — a 60-minute breakdown. Keep a timer visible. The numbers are targets, not law.
- **Transitions** — short scripted lines to hand off cleanly between blocks.
- **Predicted misconceptions** — where THIS learner (expert in research, novice in code) will stumble.
- **Socratic prompts** — questions to ask instead of explaining; let them derive it.
- **Cut line** — the first thing to drop if you're running over.

## Universal pacing principles (this learner is fast)
- **Talk less than you want to.** He reads fast and abstracts well. Default to "here's the rule, here's the trap, now you try."
- **Protect — and fill — the practice block.** The ~30-minute hands-on block is where learning happens. It's packed on purpose: this learner finishes individual tasks quickly, so the block carries *more* tasks rather than more minutes. If concept overruns, steal from your own talking, never from his typing.
- **Predict-then-run is the engine, especially S2.** Always have him *commit to an answer out loud* before running. The cognitive surprise is the teaching moment.
- **Don't pad.** Each clock is tight by design — no long buffers to fill with lecture. If he's ahead, give him the next practice task or a stretch goal, not more talking.
- **Carry a running "misconceptions log"** (DeepTutor "learning memory"): note every trap he hit this hour; re-surface it as a 60-second warm-up next session.

---

## SESSION 1 — Running Python, Variables & Types
**Pre-flight:** terminal + VS Code open; `examples/session-01/` ready; a deliberately broken line staged to show a traceback.

**The clock (60 min)**
- **0:00–0:05 — Orientation.** Why Python, why this re-ordered path, how the hour works. Don't oversell; he wants to start.
- **0:05–0:16 — Concept.** REPL vs script; `python file.py`. Variables as *labels on objects* (use Connection Map #1). The five core types. `input()` → always `str`. f-strings. `int()/float()/str()`.
- **0:16–0:24 — Live code.** Build `greet.py` then a tiny `interest.py` ("years to graduation") together; deliberately trigger and *read* one traceback.
- **0:24–0:54 — Practice (packed).** Student works through `examples/session-01/practice.md` (BMI/GPA-converter style script + the extra short tasks). You stay quiet; answer only when asked. Hand him the next task the moment he finishes one.
- **0:54–0:58 — Traps recap.** The `input()`-returns-string trap; `print(a, b)` vs `print(a + b)`; integer vs float division preview.
- **0:58–1:00 — Summary + 3-question quiz.**

**Transitions**
- Concept→Live: *"Enough theory — watch me make these mistakes so you don't have to."*
- Live→Practice: *"Your turn. Break it on purpose at least once and read the error out loud."*
- Practice→Traps: *"Before we close — here are the two things that get everyone in week one."*

**Predicted misconceptions (this learner)**
- Expects `input()` to give a number (it's a string) → `"5" + "3" == "53"`.
- Thinks `=` asserts equality (math habit). Reinforce label-on-object framing now; it pays off in S2/S5.
- Reads tracebacks top-down and panics. Teach: **read the last line first.**

**Socratic prompts**
- "What type do you think `input()` hands back? How could we check?" (→ `type(...)`)
- "Why did `'5' + '3'` give `'53'`? What would make it `8`?"

**Cut line:** drop the compound-interest live demo; keep `greet.py` + the traceback.

---

## SESSION 2 — The Dynamic-Typing Traps
**Pre-flight:** Open `cheatsheets/traps-and-gotchas.md` and `examples/session-02/traps_demo.py`. This is the most important hour — protect it. Tell him so.

**The clock (60 min)** — this hour is *predict-then-run* almost end to end, so the hands-on practice is woven through every block, not saved for one slot.
- **0:00–0:04 — Warm-up.** Re-surface S1 traps (60-sec quiz from your misconceptions log).
- **0:04–0:20 — Block A: `==` vs `is`.** Value vs identity (Connection Map #3: same GPA vs same person). Show `is` with lists, `None` (`is None`), and the small-int cache wrinkle (label it "implementation detail — never rely on it").
- **0:20–0:36 — Block B: the number traps.** `bool` ⊂ `int` (`True == 1`, `5 + True`, `sum([True,False,True])` = dummy coding, Connection Map #4); `3 == 3.0`; **float precision** `0.1 + 0.2` (Connection Map #5) → `math.isclose`, round-for-display.
- **0:36–0:48 — Block C: cross-type comparison + type checking.** `5 == "5"` is `False` but `5 > "5"` raises `TypeError`; sequence comparison element-by-element (`[1,2]==(1,2)` is `False`); `isinstance(x,(int,float))` vs `type(x) is int`; truthiness of `0/""/[]/None`.
- **0:48–0:57 — Practice.** `examples/session-02/practice.md`: a "predict the output" gauntlet, then a `clean_score()` that handles int/float/str-number inputs safely.
- **0:57–1:00 — Summary.** Hand him the trap cheat sheet as his permanent reference; quiz.

**Transitions**
- A→B: *"Identity vs value — hold that. Now the same question for numbers, where Python is sneakier."*
- B→C: *"Mixing numbers is fine. Mixing a number with text? Watch — sometimes False, sometimes an explosion."*
- C→Practice: *"Cover the right column of the cheat sheet. Predict each line, then run."*

**Predicted misconceptions (this learner)**
- Will assume `is` is just a stylistic `==` (very common). Nail it with mutable-list demo.
- Will trust `==` on floats out of stats habit ("I round anyway") — connect to measurement error but stress the *cause* is binary storage, not data.
- May over-generalize the `TypeError` and think `5 == "5"` also errors. It returns `False` — show it.
- Will reach for `type(x) == int`; redirect to `isinstance` and explain inheritance (sets up `bool`⊂`int`).

**Socratic prompts**
- "Two students, same 3.7 GPA. `==`? `is`? Why?"
- "You already sum 0/1 dummies. So what's `sum([True, False, True])`? Why?"
- "If `0.1 + 0.2` isn't `0.3`, is the bug in the data or in the computer? How would you test 'close enough'?"
- "`5 == '5'` is False, fine. So why does `5 > '5'` *crash*? What does the computer not know how to do?"

**Cut line:** drop the small-int cache wrinkle and the walrus aside; never cut Blocks A–C core or the practice.

---

## SESSION 3 — Control Flow: Conditionals & Loops
**Pre-flight:** `examples/session-03/`; a messy nested-`if` snippet staged for the refactor demo; `Ctrl+C` ready to demo killing an infinite loop. (This hour merges what many courses split across two — a fast learner clears decisions and repetition together, since loops are just decisions that repeat.)

**The clock (60 min)**
- **0:00–0:04 — Warm-up** (S2 traps recap).
- **0:04–0:16 — Concept.** *Conditionals:* `if/elif/else`; comparison ops; **chained comparisons** (`90 <= x < 100` — they love this, it reads like math); `and/or/not`; short-circuit; `and/or` return an *operand*, not a bool. *Loops:* `while` (+ infinite-loop demo, `Ctrl+C`); `for ... in`; `range` (off-by-one!); `break`/`continue`; the `while True: ... break` validation pattern; **`enumerate`** and **`zip`** as the antidote to `range(len(...))`.
- **0:16–0:24 — Live code.** A Likert→label classifier using a chained comparison and an early `return`; then sum/average a list of scores two ways (index vs `enumerate`/`zip`); finish with a robust "ask until valid" prompt using `while True`.
- **0:24–0:54 — Practice (packed).** `examples/session-03/practice.md`: grade-band classifier (test every boundary), boolean-logic predictions, average + pass/fail with `zip`, a real validation loop, and the mutate-while-iterating trap fix. Keep handing him the next task; this block is sized to fill the half hour.
- **0:54–0:58 — Traps recap.** `if x == True` (just `if x`); `is None` not `== None`; `=` vs `==` typo; `range(1,5)` excludes 5; **mutating a list while looping it**; reaching for `range(len(...))` instead of `enumerate`/`zip`.
- **0:58–1:00 — Summary + quiz.**

**Transitions**
- Concept→Live: *"Watch me turn an ugly five-level `if` into three readable lines — then loop over a whole roster."*
- Live→Practice: *"Build the grade classifier; make it pass all the band boundaries — the edges are where bugs hide. Then loop the roster, and if you catch yourself writing `range(len(...))`, stop and use `enumerate`."*

**Predicted misconceptions**
- Will write `if score >= 90 and score < 100` and not know about chaining → show `90 <= score < 100`.
- Will write `if passed == True`. Ask "what type is `passed` already?"
- Boundary errors (`>=` vs `>`) at grade cutoffs — make him test 89.999 / 90 / 90.001.
- Off-by-one with `range`. Have him print `list(range(1,5))` to see it.
- `range(len(x))` index habit (from R/SPSS vectorized thinking) — push `enumerate`/`zip`.
- Trying to remove items from a list *while iterating it* → demo the bug, then the fix (iterate a copy / build a new list).

**Socratic prompts**
- "`x = 5 and 0` — what's `x`? Why isn't it `True`/`False`?"
- "How would a mathematician write `between 90 and 100`? Python lets you write it that way."
- "You need both the position and the value. What's cleaner than indexing?"
- "Two parallel lists, names and scores. How do you walk them together?"

**Cut line:** drop `match/case` and `for/else` (mention they exist, point to the cheat sheet); keep chained comparisons, `enumerate`/`zip`, and the validation loop.

---

## SESSION 4 — Data Structures: list, tuple, dict, set
**Pre-flight:** `examples/session-04/`; a "list of dicts = tidy dataset" diagram (Connection Map #6).

**The clock (60 min)**
- **0:00–0:04 — Warm-up.**
- **0:04–0:16 — Concept.** `list` (mutable) vs `tuple` (immutable) vs `dict` (key→value) vs `set` (unique). Indexing & **slicing**. Nesting → **list of dicts = a dataset**. Comprehensions (list + dict). `sorted(key=lambda ...)`.
- **0:16–0:24 — Live code.** Build a roster as a list of dicts; sort by score; dedupe survey answers with a `set`; rewrite a loop as a comprehension.
- **0:24–0:54 — Practice (packed).** Group students by grade band into a dict; build `{name: average}` with a dict comprehension; slice/sort tasks (`examples/session-04/practice.md`). Feed the next task as soon as one lands.
- **0:54–0:58 — Traps recap.** **Aliasing** (`b = a` shares the list) vs `a.copy()`; `[[0]*3]*3` shared rows; shallow vs deep copy; sequence comparison recap (ties back to S2); **mutable default arg** preview (full treatment S5).
- **0:58–1:00 — Summary + quiz.**

**Transitions**
- Concept→Live: *"A list of dicts is just a tidy dataset — rows are dicts, keys are your variables."*
- Live→Practice: *"Group the roster by grade band. Then make a `{name: average}` in one line."*

**Predicted misconceptions**
- **Aliasing** is the big one — he'll expect `b = a` to copy. Show `a.append(...)` changing `b`. Tie to S1 "label on object."
- Confusing tuple immutability with "you can't have a tuple of lists" — you can; the *tuple* is fixed, contents may not be.
- Comprehension syntax order (`[expr for x in xs if cond]`) — have him read it as "expr, for each x, when cond."

**Socratic prompts**
- "`b = a; a.append(99)` — what's in `b`? Why? (Remember: labels, not boxes.)"
- "Survey gave duplicate free-text answers. What structure removes duplicates for free?"

**Cut line:** drop deep-copy/`[[0]*3]*3`; keep aliasing basics + comprehensions.

---

## SESSION 5 — Functions, Scope & Reusability
**Pre-flight:** `examples/session-05/`; the **mutable-default-arg** demo staged (this is the headline).

**The clock (60 min)**
- **0:00–0:04 — Warm-up.**
- **0:04–0:16 — Concept.** `def`, parameters (positional/keyword/default), `return` vs `print`, `*args`/`**kwargs`, scope (LEGB), `global` (and why to avoid it), docstrings, **type hints** (+ "not enforced; `mypy` checks them").
- **0:16–0:24 — Live code.** Refactor S3/S4 inline code into `class_average(scores)`, `letter_grade(score)`; then the **mutable-default bug** live: `def add(x, bag=[])` accumulating across calls → fix with `bag=None`.
- **0:24–0:54 — Practice (packed).** Write a small library of grade functions with type hints + docstrings, plus a `*args` aggregator and a keyword-default formatter (`examples/session-05/practice.md`).
- **0:54–0:58 — Traps recap.** Mutable default; late-binding closures; forgetting `return` (function returns `None`); `UnboundLocalError` from assigning a global.
- **0:58–1:00 — Summary + quiz.**

**Transitions**
- Concept→Live: *"This next bug has burned every Python programmer at least once. Watch."*
- Live→Practice: *"Build your grade-functions module — these are the pieces of your capstone."*

**Predicted misconceptions**
- Will not believe the default list persists between calls until shown twice. Run it, then explain *when* defaults are evaluated (once, at definition).
- Thinks a function that `print`s has "returned" the value → show `x = show(...)` is `None`.
- Will expect type hints to enforce types at runtime. Show `add("a","b")` still runs.

**Socratic prompts**
- "I called `add(1)` three times and the list keeps growing. When do you think `bag=[]` actually runs?"
- "`print` vs `return` — which one lets the *next* function use the result?"

**Cut line:** drop late-binding closures; never cut the mutable-default demo.

---

## SESSION 6 — Recursion & Recursive Thinking
**Pre-flight:** `examples/session-06/`; a nested-JSON-shaped dict staged for the `deep_sum` demo;
have `sys.getrecursionlimit()` ready and the `runaway` overflow demo queued.

**The clock (60 min)**
- **0:00–0:04 — Warm-up.** Re-surface an S5 trap from your misconceptions log.
- **0:04–0:16 — Concept.** The two parts: a **base case** and a **recursive case** that moves
  toward it. Trace `factorial(3)` on the board as a stack that builds, then unwinds. Recursion vs
  iteration (factorial both ways). Name the cost: each pending call is a stack frame; Python has
  **no tail-call optimization** (`sys.getrecursionlimit()` ≈ 1000).
- **0:16–0:24 — Live code.** `countdown`/`factorial`; then `deep_sum` over a nested dict — the
  payoff, since a single loop can't reach the bottom of arbitrarily nested data; then trigger a
  `RecursionError` with `runaway` and read it together.
- **0:24–0:54 — Practice (packed).** `examples/session-06/practice.md`: recursive sum, string
  reverse (recursion vs loop), `flatten`, `depth`, and the two trap-fixes. Hand out the next task
  as each lands.
- **0:54–0:58 — Traps recap.** Unreachable base case → stack overflow; forgetting to `return` the
  recursive call → silent `None`; recursion isn't free; when a loop simply reads clearer.
- **0:58–1:00 — Summary + quiz; point ahead to exceptions (S7).**

**Transitions**
- Concept→Live: *"Watch the stack build up and then collapse — that's the whole trick."*
- Live→Practice: *"Your turn. Say the base case out loud before you write the function — that's where the bugs hide."*

**Predicted misconceptions (this learner)**
- Will write the recursive case but forget to `return` it → silent `None`. Show it once.
- Will fear infinite recursion everywhere; reassure — a *reachable* base case is the guarantee.
- From a vectorized stats background, may not see when recursion beats a loop → the nested-data demo is the "aha."
- May assume recursion is a free, elegant swap for a loop → show the `RecursionError` and the ~1000 limit.

**Socratic prompts**
- "What's the smallest input where the answer is obvious without recursing? That's your base case."
- "Your data is a list that can contain lists. What kind of function matches a thing defined in terms of itself?"
- "`factorial(2000)` by recursion vs by loop — which one risks crashing, and why?"

**Cut line:** drop the `depth`/string-reverse practice tasks; keep base/recursive case, `deep_sum`
on nested data, and the `RecursionError` demo.

---

## SESSION 7 — Exceptions & Defensive Code
**Pre-flight:** `examples/session-07/`; a CSV-ish list with dirty values ("N/A", "", "7" on a 1–5 scale).

**The clock (60 min)**
- **0:00–0:04 — Warm-up.**
- **0:04–0:16 — Concept.** Errors vs exceptions; `try/except/else/finally`; common types (`ValueError`, `KeyError`, `ZeroDivisionError`, `FileNotFoundError`); `raise ValueError(...)`; **EAFP** ("easier to ask forgiveness") vs LBYL; `assert`.
- **0:16–0:24 — Live code.** Harden `get_int()`/`clean_likert()` to survive blanks, "N/A", out-of-range; show a first `pytest` test (`test_clean.py`) including `pytest.raises`.
- **0:24–0:54 — Practice (packed).** Validate a list of raw survey responses, collecting good values and a report of bad ones; add a `raise` for impossible input and one `pytest.raises` test (`examples/session-07/practice.md`).
- **0:54–0:58 — Traps recap.** **Bare `except:`** (catches everything, even `Ctrl+C`); catching too broad; silently swallowing errors; using exceptions for normal control flow excessively.
- **0:58–1:00 — Summary + quiz.**

**Transitions**
- Concept→Live: *"Your real survey data WILL have 'N/A' in a numeric column. Let's make code that shrugs it off."*
- Live→Practice: *"Clean this dirty response list; keep a log of every value you rejected and why."*

**Predicted misconceptions**
- Will reach for `if/else` checks (LBYL) everywhere; introduce EAFP as the Pythonic default but be honest both are valid.
- Will write `except:` bare — show why `except ValueError:` is safer.
- Confuses `raise` (throw) with `return`; and `assert` (a developer check, can be disabled) with input validation (must always run).

**Socratic prompts**
- "User typed 'seven' instead of 7. Catch it *before* (`if`) or *after* (`try`)? Trade-offs?"
- "Why is a bare `except:` dangerous? What might you accidentally swallow?"

**Cut line:** drop the `pytest` test → just use `assert` statements; keep `try/except` validation.

---

## SESSION 8 — Files, Libraries & Research Data
**Pre-flight:** ship a sample `students.csv` and `survey.csv` in `examples/session-08/`; confirm `pip` works; have `pandas` install ready (or pre-installed) for the teaser.

**The clock (60 min)**
- **0:00–0:04 — Warm-up.**
- **0:04–0:16 — Concept.** `open`/`with` (context manager: auto-close); file modes (`r/w/a`; **`w` overwrites!**); reading lines; **CSV** via `csv.DictReader`/`DictWriter` (rows as dicts → ties to S4); `json` briefly; `import`; `pip install`; researcher stdlib: `statistics`, `random`, `datetime`, `pathlib`.
- **0:16–0:24 — Live code.** Read `students.csv` into a list of dicts, compute the class mean with `statistics.mean`, write a summary CSV. Then a short **`pandas` teaser**: same task in 3 lines (`read_csv`, `.describe()`), framed as "here's your next course."
- **0:24–0:54 — Practice (packed).** Read `survey.csv`, compute per-item means, write `survey_summary.csv`; add a `datetime`-stamped filename and a `pathlib` existence check (`examples/session-08/practice.md`).
- **0:54–0:58 — Traps recap.** `"w"` silently destroys data; forgetting `newline=""` with `csv` (blank rows on Windows); forgetting `\n`; encoding (`utf-8`); reading a file twice (cursor at end).
- **0:58–1:00 — Summary + quiz.**

**Transitions**
- Concept→Live: *"This is the hour your actual research data shows up. Let's read a real CSV."*
- Teaser framing: *"Everything you just did by hand, pandas does in three lines — that's your next course, not today's. But now you know what it's doing underneath."*

**Predicted misconceptions**
- Will open with `"w"` to read and wonder why the file is empty. Stress mode meanings.
- Expects to iterate a file object twice without re-opening; show the exhausted-cursor effect.
- May jump to pandas and skip the fundamentals — hold the line: hand-rolled first, pandas as dessert.

**Socratic prompts**
- "Why does `with` matter even if your program crashes? What does it guarantee?"
- "You read the file once and the second loop is empty. Where did the data 'go'?"

**Cut line:** drop the `pandas` teaser and `json`; keep `with`, modes, and `csv.DictReader/Writer`.

---

## SESSION 9 — Regular Expressions & Text Cleaning
**Pre-flight:** `examples/session-09/`; a list of messy free-text responses, emails, and "Last, First" names staged for live demos.

**The clock (60 min)**
- **0:00–0:04 — Warm-up.** Re-surface an S8 trap from your misconceptions log.
- **0:04–0:16 — Concept.** Why regex for a researcher (validate/extract/clean/qualitative-coding, Connection Map #9). **Raw strings** `r"..."`. The survival tokens (`. \d \w \s + * ? {m,n} ^ $ [] () |`). Stress `.` matches *any* char (use `\.`).
- **0:16–0:24 — Live code.** The four functions: `re.search`/`fullmatch`/`findall`/`sub`. Validate an email (`fullmatch`), extract dept+number with capture groups, collapse whitespace with `sub`.
- **0:24–0:54 — Practice (packed).** `examples/session-09/practice.md`: email validator, extract codes, count `#hashtags` across responses, flip `"Last, First"`, and one case where `.split()` beats regex.
- **0:54–0:58 — Traps recap.** `.` matches anything; forgot `r"..."`; `re.search` returns `None`; regex vs string methods.
- **0:58–1:00 — Summary + quiz.**

**Transitions**
- Concept→Live: *"Four functions cover almost everything: search, fullmatch, findall, sub. Watch."*
- Live→Practice: *"Your turn — and every pattern is a raw string, no exceptions."*

**Predicted misconceptions**
- Forgets raw strings → backslash chaos. Always `r"..."`.
- Assumes `.` matches only a dot → show it matches any char; `\.` for literal.
- Calls `.group()` on a `None` result → teach the `if m:` guard.
- Over-uses regex where `.split()`/`.strip()`/`.replace()` are clearer.

**Socratic prompts**
- "You want every response mentioning a theme. Is that a *form* match (regex) or a *meaning* match (human coding)? What can regex actually catch?"
- "`5 > "5"` crashed weeks ago. Why does `re.search(...).group()` crash when there's no match?"

**Cut line:** drop the `findall`/Counter hashtag-mining demo; keep validate + extract + `sub`.

---

## SESSION 10 — Modules, OOP & the Pythonic Toolkit
**Pre-flight:** `examples/session-10/` (`grades.py` staged for the import demo, `Student` class ready); the generator-exhaustion demo queued.

**The clock (60 min)**
- **0:00–0:04 — Warm-up.** Re-surface an S9 trap.
- **0:04–0:12 — Modules.** Move grade functions into `grades.py`, `import` them; the `if __name__ == "__main__":` guard (file as both script and library).
- **0:12–0:24 — OOP.** A small `Student` class: `__init__`, `self` ("this particular student"), a method, `__str__`, a validating `@property` setter (Connection Map #10), then brief inheritance with `super()`.
- **0:24–0:54 — Practice (packed).** Build the validating `Student`, add `GradStudent(super())`, then one comprehension + `map` + `filter` + a generator (`examples/session-10/practice.md`). Mix in the Pythonic-toolkit recap (comprehensions, `map`/`filter`, `enumerate`/`zip`, generators/`yield`, walrus `:=`) as you hand out tasks rather than lecturing it.
- **0:54–0:58 — Traps recap.** `self` confusion; a generator exhausts after one pass; over-using a class where a function/dict fits; forgetting the `__main__` guard.
- **0:58–1:00 — Summary + quiz; course wrap, point to the capstone.**

**Transitions**
- Modules→OOP: *"Functions in a file is reuse. Now let's bundle data *and* behavior — a class."*
- OOP→Practice: *"Build your `Student`, then we'll tour the moves that make code read like the experts'."*

**Predicted misconceptions**
- `self` looks redundant/magical — it's just "this particular instance."
- Treats a generator like a list (iterates once) → show the second pass is empty.
- Thinks the `__main__` guard is boilerplate → show the demo block firing on run but not on import.
- Reaches for a class when a function or dict would do — name when OOP earns its keep.

**Socratic prompts**
- "Your operational definition of 'student' — what attributes and rules belong to it? That's your class."
- "A million rows won't fit in memory. What does `yield` give you that a list doesn't?"

**Cut line:** compress the Pythonic tour to comprehensions + `enumerate`/`zip`; defer `map`/`filter`/walrus to the cheat sheet. Keep modules + the validating class.

---

## SESSION 11 (Optional) — Capstone
**Role shift:** you stop teaching and start *coaching*. He drives; you ask questions and unblock.
- **0:00–0:10 — Brief & plan.** He restates the goal and sketches the steps aloud (pseudocode). You only check the plan is sound.
- **0:10–0:45 — Build.** He codes the Gradebook & Survey Analyzer (`assessments/capstone-project.md`). Intervene only when stuck >3 min; prefer a question over an answer.
- **0:45–0:55 — Review.** Walk his code for the traps from S2/S4/S5 (identity, aliasing, mutable defaults). Praise readability.
- **0:55–1:00 — Debrief & next steps.** Point to pandas/visualization as the genuine next course.

**Coaching prompts:** "What's your data structure?" · "What happens if that cell is blank?" · "Is that comparing value or identity?" · "Could that be one comprehension?"

---

## Instructor's running checklist (use across all sessions)
- [ ] Timer visible; practice block protected *and* packed.
- [ ] Misconceptions log updated after each hour; warm-up next session pulls from it.
- [ ] Every trap demoed via **predict-then-run**, not narration.
- [ ] Each new concept hooked to the **Connection Map** before syntax.
- [ ] Student typed everything himself; you talked less than half the hour.
- [ ] End-of-session quiz given; capstone kept in view as the destination.
