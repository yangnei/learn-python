# Session 10 — Practice (25 min): Modules, OOP & Pythonic

Files in this folder: `grades.py` (a module you import), `demo.py` (worked example).

## Task 1 — Use a module
From a new file, `from grades import letter_grade, class_average` and call both. Why does the
`if __name__ == "__main__":` block in `grades.py` NOT run when you import it?

## Task 2 — A class with a validating property
Build `Student(name, gpa)` with:
- `__str__` → `"Ana: 3.9 (Good)"`,
- `standing()` → `"Good"` if gpa ≥ 2.0 else `"Probation"`,
- a `@property` setter for `gpa` that raises `ValueError` outside 0–4.
Prove the setter rejects `5.0`.

## Task 3 — Inheritance
Add `GradStudent(Student)` that also stores an `advisor` and uses `super().__init__(...)`.
Override `__str__` to append the advisor.

## Task 4 — The Pythonic toolkit
Given a roster of `Student`s:
1. names in good standing (list comprehension),
2. uppercase names (`map`),
3. at-risk students (`filter`),
4. mean gpa via a **generator** that `yield`s each gpa — then show the generator is empty on a
   second pass.

---
## Solutions
See `demo.py` — it implements Tasks 2–4. Key points:

```python
@property
def gpa(self): return self._gpa
@gpa.setter
def gpa(self, v):
    if not 0 <= v <= 4: raise ValueError(...)
    self._gpa = v

class GradStudent(Student):
    def __init__(self, name, gpa, advisor):
        super().__init__(name, gpa)
        self.advisor = advisor

[s.name for s in roster if s.gpa >= 2.0]          # comprehension
list(map(lambda s: s.name.upper(), roster))        # map
[s.name for s in filter(lambda s: s.gpa < 2.0, roster)]   # filter
def gpas(rs):
    for s in rs: yield s.gpa                        # generator (exhausts after one pass)
```
Task 1: the `__name__` guard is only `"__main__"` when the file is **run directly**; on `import`
its `__name__` is `"grades"`, so the demo block is skipped — that's how a file can be both a
runnable script and an importable module.
