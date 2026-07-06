---
marp: true
title: "Session 10 — Modules, OOP & the Pythonic Toolkit"
paginate: true
---

# Session 10
## Modules, OOP & the Pythonic Toolkit

---

## Modules: split your code into files

```python
# grades.py
def letter_grade(score): ...
def class_average(scores): ...

# analysis.py
from grades import letter_grade, class_average
```

A `.py` file is a **module**. `import` reuses its functions elsewhere → no copy-paste.

---

## The `__main__` guard

```python
# grades.py
if __name__ == "__main__":
    print(letter_grade(85))   # runs ONLY when you execute grades.py directly
```

On `import grades`, `__name__` is `"grades"`, so the block is skipped.
One file can be both a runnable script *and* an importable library.

---

## OOP: model a domain entity

```python
class Student:
    def __init__(self, name, gpa):   # constructor
        self.name = name
        self.gpa = gpa
    def __str__(self):               # how it prints
        return f"{self.name} ({self.gpa})"

ana = Student("Ana", 3.9)
print(ana)        # Ana (3.9)
```

🧠 A class is an *operational definition*: the attributes + behaviors that "count" as a Student.
`self` = "this particular student."

---

## @property: validate on assignment

```python
class Student:
    ...
    @property
    def gpa(self):
        return self._gpa
    @gpa.setter
    def gpa(self, value):
        if not 0 <= value <= 4:
            raise ValueError("gpa must be 0–4")
        self._gpa = value
```

`ana.gpa = 5.0` now raises — the object defends its own integrity.

---

## Inheritance

```python
class GradStudent(Student):
    def __init__(self, name, gpa, advisor):
        super().__init__(name, gpa)    # reuse parent setup
        self.advisor = advisor
    def __str__(self):
        return super().__str__() + f" — {self.advisor}"
```

`GradStudent` *is a* `Student` plus extra. `super()` calls the parent.

---

## The Pythonic toolkit (recap tour)

```python
[s.name for s in roster if s.gpa >= 2.0]   # comprehension (from S4)
list(map(lambda s: s.name.upper(), roster))# map: apply to all
list(filter(lambda s: s.gpa < 2.0, roster))# filter: keep matches
for i, s in enumerate(roster): ...          # index + item
for a, b in zip(names, scores): ...         # parallel
```

---

## Generators & walrus

```python
def gpas(students):
    for s in students:
        yield s.gpa          # one value at a time — low memory on big data

g = gpas(roster)
list(g)   # ?
list(g)   # ?  ← run it twice — what changes? (Traps below)

if (n := len(roster)) > 30:   # walrus := : assign + test in one step
    print(f"{n} students")
```

---

## Your turn

`examples/session-10/practice.md`:
1. Import from `grades.py`. 2. Build the validating `Student` class.
3. Add `GradStudent` with `super()`. 4. Comprehension + `map` + `filter` + a generator.

---

# Going deeper
## Designing with objects

---

## `__repr__` and friends

```python
class Student:
    def __repr__(self):                    # for developers (REPL, lists, logs)
        return f"Student({self.name!r}, {self.gpa})"
    def __eq__(self, other):
        return (self.name, self.gpa) == (other.name, other.gpa)
    def __lt__(self, other):               # "less than" — sorted() now just works
        return self.gpa < other.gpa

sorted(roster)                              # no key= needed anymore
```

Dunders make your objects behave like built-ins: printable, comparable, sortable —
even **addable**: define `__add__(self, other)` and `total = quiz + final` just works.
That's all "operator overloading" is.

---

## `@dataclass`, round 2

```python
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    gpa: float = 0.0
    courses: list = field(default_factory=list)   # NOT courses: list = []
```

`default_factory=list` is the mutable-default rule (Session 5!) in class form — a fresh list
per instance. `@dataclass(frozen=True)` gives you an immutable record.

---

## `@classmethod`: alternate constructors

```python
@dataclass
class Student:
    name: str
    score: int

    @classmethod
    def from_row(cls, row):                # a CSV row (Session 8) -> an object
        return cls(row["name"], int(row["score"]))

roster = [Student.from_row(r) for r in csv.DictReader(f)]
```

`cls` is the class itself. Pattern: **file format at the edge, objects inside**.
(`@staticmethod` is the third flavor: a plain helper that lives in the class's
namespace — no `self`, no `cls`.)

---

## Composition over inheritance

```python
class Cohort:                    # a Cohort HAS Students  (composition ✅)
    def __init__(self, name):
        self.students = []

class GradStudent(Student):      # a GradStudent IS a Student (inheritance ✅)
    ...
```

Inherit only for a true *is-a*. When in doubt, hold objects inside other objects —
it stays flexible and testable.

---

## Class vs instance attributes — the rule

```python
class Course:
    school = "Ed School"         # class attr: SHARED by all — constants only
    def __init__(self):
        self.students = []       # instance attr: each object its own
```

Mutable data goes in `__init__`, always. (You met the shared-list trap — this is the law it
teaches.)

---

## Generator pipelines

```python
def to_ints(rows):
    for r in rows:
        try:
            yield int(r)
        except ValueError:
            pass

def in_range(vals, lo=1, hi=5):
    yield from (v for v in vals if lo <= v <= hi)

clean = list(in_range(to_ints(raw)))    # nothing runs until consumed
```

Each stage yields to the next — **lazy**, constant-memory, works on a million-row file.

---

## From script to project

```text
survey_tool/
├── clean.py        # validation functions
├── stats.py        # summaries
├── report.py       # main: python3 report.py
└── tests/test_clean.py
```

One module per concern; `report.py` imports the rest; tests alongside. Inside
`report.py`, the convention:

```python
def main():                     # the program's real work, in one place
    ...

if __name__ == "__main__":
    main()
```

You already know every ingredient — this is just arranging them.

---

## Your turn — round 2

`examples/session-10/practice.md` → **In class — going deeper**:
sortable `Student`s, a dataclass with `default_factory`, `from_row`, and a two-stage
generator pipeline.
---

## Traps recap

- `self` is just "this instance" — not magic.
- A generator iterates **once**, then it's empty.
- The `__main__` guard keeps imported modules from running their demo code.
- Don't reach for a class when a function or dict will do.

## Summary
You can structure code into modules and classes and write idiomatic Python.
**Next (optional):** Session 11 — the capstone: put it all together.

---

## Homework (before the capstone)

*Outside class — it doesn't count toward class time. Full specs + solutions: `examples/session-10/practice.md` → **Homework**.*

1. **`Student.courses`** — a courses list and a *computed* `gpa` — data plus the rules that guard it.
2. **A `Cohort` class** — holds `Student`s; `mean_gpa()`, `at_risk()`.
3. **Pythonic rewrite** — three given loops → comprehension, generator, `map`.
