# Session 10 — Practice: Modules, OOP & the Pythonic Toolkit

Type each solution yourself. **Predict every output before you run it.** Solutions at the bottom.

## In class

Files in this folder: `grades.py` (a module you import), `demo.py` (worked example).

### Task 1 — Use a module
From a new file, `from grades import letter_grade, class_average` and call both. Why does the
`if __name__ == "__main__":` block in `grades.py` NOT run when you import it?

### Task 2 — A class with a validating property
Build `Student(name, gpa)` with:
- `__str__` → `"Ana: 3.9 (Good)"`,
- `standing()` → `"Good"` if gpa ≥ 2.0 else `"Probation"`,
- a `@property` setter for `gpa` that raises `ValueError` outside 0–4.
Prove the setter rejects `5.0`.

### Task 3 — Inheritance
Add `GradStudent(Student)` that also stores an `advisor` and uses `super().__init__(...)`.
Override `__str__` to append the advisor.

### Task 4 — The Pythonic toolkit
Given a roster of `Student`s:
1. names in good standing (list comprehension),
2. uppercase names (`map`),
3. at-risk students (`filter`),
4. mean gpa via a **generator** that `yield`s each gpa — then show the generator is empty on a
   second pass.

### Bonus — Pythonic idiom drill
Cover the `# ->` answers, predict each line, then run.

```python
from dataclasses import dataclass

@dataclass                           # auto __init__, __repr__, __eq__
class Point:
    x: int
    y: int
print(Point(1, 2), Point(1, 2) == Point(1, 2))   # -> Point(x=1, y=2) True

def head(v):
    match v:                         # structural pattern matching (3.10+)
        case [first, *_]: return first
        case _: return None
print(head([9, 8]), head(5))         # -> 9 None
```

## In class — going deeper (second hour)

### E1 — The guard, observed
Add `print("running as", __name__)` to the top of `grades.py`. Run the file directly,
then `import grades` from the REPL — what prints each time, and why?

### E2 — `@dataclass` Student
Rebuild the plain (non-validating) `Student` as a `@dataclass`. What do you get for free?
Check `repr` and `==` on two equal students.

### D1 — Sortable students
Give `Student` a `__repr__`, `__eq__`, and `__lt__` (by gpa) so that `sorted(roster)`
works with **no** `key=`. Prove it.

### D2 — `dataclass` done right
Write `@dataclass class Course: name: str; roster: list = field(default_factory=list)`.
Why would `roster: list = []` be wrong — and which Session 5 bug is this the class-shaped
version of?

### D3 — `from_row`
Add `Student.from_row(cls, row)` building a `Student` from a CSV `DictReader` row
(convert types!). Why is a `@classmethod` the right home for this?

### D4 — A two-stage pipeline
Write generators `to_ints(cells)` (skip unparseable) and `in_range(vals, lo=1, hi=5)`;
chain them over `["5", "3", "N/A", "7", "1"]`. When does any work actually happen?

## Homework (before the capstone)

*~30–45 minutes, outside class — it doesn't count toward class time. Try everything before peeking at the solutions.*

### H1 — Courses and a computed GPA
Extend `Student`: a `courses` list of `(name, grade_points)` tuples, an
`add_course(name, points)` method that validates 0–4, and make `gpa` a **computed
property** (mean of the course points; `None` with no courses). No stored gpa that can go
stale.

### H2 — A `Cohort` class
`Cohort(name)` holds `Student`s: `add(student)`, `mean_gpa()` (skip students with no
gpa), `at_risk(threshold=2.0)` returning names, and `__str__` →
`"Fall-26 (3 students)"`. Careful where the student list lives — remember the
class-variable trap.

### H3 — Pythonic rewrite
Rewrite each as a single comprehension / generator / `map` line:
```python
# 1 -> list comprehension
out = []
for s in roster:
    if s.gpa is not None and s.gpa >= 3.5:
        out.append(s.name)

# 2 -> generator inside sum() (no list built)
total = 0
for s in roster:
    total += len(s.courses)

# 3 -> map (or a comprehension — say which you prefer, and why)
labels = []
for s in roster:
    labels.append(str(s))
```

---

## Solutions

### In class

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

### In class — going deeper

```python
# E1
# python3 grades.py   -> "running as __main__"  (the file IS the program)
# >>> import grades   -> "running as grades"    (so the __main__ block is skipped)

# E2
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    gpa: float

# Free: __init__, a readable __repr__, and field-by-field __eq__:
print(Student("Ana", 3.9) == Student("Ana", 3.9))   # True
```

```python
# D1
class Student:
    def __init__(self, name, gpa):
        self.name = name
        self.gpa = gpa
    def __repr__(self):
        return f"Student({self.name!r}, {self.gpa})"
    def __eq__(self, other):
        return (self.name, self.gpa) == (other.name, other.gpa)
    def __lt__(self, other):
        return self.gpa < other.gpa

roster = [Student("Ana", 3.9), Student("Ben", 1.8), Student("Cara", 3.2)]
print(sorted(roster))    # Ben, Cara, Ana — __lt__ told sorted() how

# D2
from dataclasses import dataclass, field

@dataclass
class Course:
    name: str
    roster: list = field(default_factory=list)
# `roster: list = []` would share ONE list across every Course — the mutable-default
# bug from Session 5, in class form. default_factory makes a fresh list per instance.

# D3
@dataclass
class Student2:
    name: str
    score: int

    @classmethod
    def from_row(cls, row):
        return cls(row["name"], int(row["score"]))
# It constructs an instance of the class itself, so it belongs to the CLASS (cls),
# not to any one object — the "alternate constructor" pattern.

# D4
def to_ints(cells):
    for c in cells:
        try:
            yield int(c)
        except ValueError:
            pass

def in_range(vals, lo=1, hi=5):
    yield from (v for v in vals if lo <= v <= hi)

pipeline = in_range(to_ints(["5", "3", "N/A", "7", "1"]))
print(list(pipeline))    # [5, 3, 1] — nothing ran until list() pulled values through
```

### Homework

```python
# H1
class Student:
    def __init__(self, name):
        self.name = name
        self.courses = []                    # (course, grade_points) tuples

    def add_course(self, course, points):
        if not 0 <= points <= 4:
            raise ValueError(f"{points} outside 0-4")
        self.courses.append((course, points))

    @property
    def gpa(self):                           # computed — can never go stale
        if not self.courses:
            return None
        return sum(p for _, p in self.courses) / len(self.courses)

    def __str__(self):
        return f"{self.name} (GPA {self.gpa})"

# H2
class Cohort:
    def __init__(self, name):
        self.name = name
        self.students = []                   # per-instance — NOT a class variable!

    def add(self, student):
        self.students.append(student)

    def mean_gpa(self):
        gpas = [s.gpa for s in self.students if s.gpa is not None]
        return sum(gpas) / len(gpas) if gpas else None

    def at_risk(self, threshold=2.0):
        return [s.name for s in self.students
                if s.gpa is not None and s.gpa < threshold]

    def __str__(self):
        return f"{self.name} ({len(self.students)} students)"

# H3
names  = [s.name for s in roster if s.gpa is not None and s.gpa >= 3.5]
total  = sum(len(s.courses) for s in roster)      # generator — no list in memory
labels = list(map(str, roster))   # or [str(s) for s in roster] — either is fine;
                                  # most Pythonistas find the comprehension clearer
```
