# Capstone Project — Gradebook & Survey Analyzer

**Time:** ~2 hours (Session 11). **Role:** the student drives; the teacher coaches with questions.
**Goal:** independently build one end-to-end program on realistic education data, exercising
every fundamental from the course.

## The brief
Write a program `analyzer.py` that:
1. **Reads** `students.csv` and `survey.csv` (reuse the files from `examples/session-08/`).
2. **Cleans & validates** the data:
   - Convert score/Likert strings to numbers; skip/flag `"N/A"`, blanks, out-of-range values.
   - Reject impossible scores (outside 0–100) and Likert values outside 1–5.
3. **Computes** summary statistics:
   - Class mean, median, and standard deviation of scores.
   - Mean score by major.
   - Per-item survey means (valid responses only) and the count of valid responses.
4. **Flags at-risk students** (score < 60) and lists them.
5. **Writes** a report `report.csv` (e.g., `major, mean_score, n, n_at_risk`).
6. **Is organized**: at least one helper module or class, functions with docstrings/type hints,
   and an `if __name__ == "__main__": main()` entry point.

## Required techniques (checklist — hits the whole course)
- [ ] f-strings & type conversion (S1)
- [ ] correct comparisons; `math.isclose` or rounding where floats are compared (S2)
- [ ] conditionals / chained comparisons + loops with `enumerate`/`zip` (S3)
- [ ] list of dicts + a comprehension + a dict (S4)
- [ ] functions with docstrings + type hints; **no mutable default args** (S5)
- [ ] `try/except` to survive dirty values; no bare `except:` (S7)
- [ ] `csv.DictReader`/`DictWriter`, `statistics`, `with open(...)` (S8)
- [ ] a module or a small class (S10); optionally a regex validation (S9)

## Stretch goals (pick any)
- Validate student emails/IDs with a regex.
- Add a `Student` class with a validating `@property` and use it to hold each record.
- Use a **generator** to stream rows if the file were huge.
- Read a **nested** export (e.g., grades grouped by class → student → attempts) and total it with
  a **recursive** `deep_sum` (S6).
- Add a `--top N` command-line argument with `sys.argv` or `argparse`.
- Sort and print the top/bottom 3 students by score.

## Alternative briefs (if "gradebook" doesn't fit the student's interests)
- **Reading-log analyzer:** pages read per day per student → weekly averages, streaks.
- **Qualitative-code counter:** read open-ended responses, count keyword/theme frequencies
  (regex), output a frequency table.
- **Attendance tracker:** parse an attendance CSV → per-student attendance rate, flag < 80%.

## What "done" looks like
The program runs without crashing on the provided dirty data, prints a readable summary, and
writes `report.csv`. The student can explain, for any line, whether it compares *value or
identity*, what *type* each variable is, and what happens if the input is *dirty*.

## Teacher rubric (coach, don't grade)
| Dimension | Look for |
|---|---|
| Correctness | right stats; dirty rows handled, not crashed on |
| Robustness | specific `except`, range checks, no silent swallowing |
| Traps avoided | no mutable default; no `==` on raw floats; no aliasing surprise |
| Readability | functions, docstrings, comprehensions where they help |
| Independence | student reasoned it out; teacher only unblocked with questions |

**Coaching prompts:** "What's your data structure?" · "What if that cell is blank?" ·
"Is that comparing value or identity?" · "Could that loop be one comprehension?" ·
"Where would this crash on real data?"
