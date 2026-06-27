"""
Session 10 — Modules, OOP & the Pythonic Toolkit
Run me from this folder:  python3 demo.py
"""
import functools
import itertools
from dataclasses import dataclass

from grades import letter_grade, class_average   # import from our own module (grades.py)


# --- 1. Modules: reuse code from another file ---------------------------
print("letter for 85:", letter_grade(85))
print("average:", class_average([91, 58, 73]))


# --- 2. OOP: model a domain entity --------------------------------------
class Student:
    def __init__(self, name: str, gpa: float):
        self.name = name
        self.gpa = gpa             # runs through the setter below (validates!)

    def __str__(self) -> str:      # how the object prints
        return f"{self.name}: {self.gpa} ({self.standing()})"

    def standing(self) -> str:
        return "Good" if self.gpa >= 2.0 else "Probation"

    @property                       # makes .gpa look like an attribute...
    def gpa(self) -> float:
        return self._gpa

    @gpa.setter                     # ...but validates on every assignment
    def gpa(self, value: float):
        if not 0 <= value <= 4:
            raise ValueError(f"gpa {value} not in 0-4")
        self._gpa = value

    @classmethod                    # an alternate constructor: build from a CSV row
    def from_row(cls, row: str) -> "Student":
        name, gpa = row.split(",")
        return cls(name.strip(), float(gpa))

    @staticmethod                   # a helper that needs no instance/class
    def is_passing(gpa: float) -> bool:
        return gpa >= 2.0


ana = Student("Ana", 3.9)
print("\n", ana)                    # uses __str__
print("from_row:", Student.from_row("Ben, 3.4"))     # classmethod constructor
print("is_passing(1.5)?", Student.is_passing(1.5))   # staticmethod
try:
    ana.gpa = 5.0                   # rejected by the setter
except ValueError as e:
    print("rejected:", e)


# --- 3. Inheritance ------------------------------------------------------
class GradStudent(Student):
    def __init__(self, name, gpa, advisor):
        super().__init__(name, gpa)     # reuse the parent's setup
        self.advisor = advisor
    def __str__(self):
        return super().__str__() + f" — advised by {self.advisor}"

print("\n", GradStudent("Cara", 3.4, "Dr. Lee"))


# --- 4. @dataclass: __init__, __repr__, __eq__ written for you ----------
@dataclass
class Grade:
    course: str
    score: int

g1, g2 = Grade("ED1234", 91), Grade("ED1234", 91)
print("\ndataclass repr:", g1)          # Grade(course='ED1234', score=91) — free __repr__
print("value equality:", g1 == g2)      # True — free __eq__ compares fields


# --- 5. match / case: structural pattern matching (Python 3.10+) --------
def classify(record):
    match record:
        case {"gpa": g} if g >= 3.5:        # mapping pattern + guard
            return "honors"
        case {"gpa": _}:
            return "regular"
        case [first, *_]:                   # sequence pattern, capture the head
            return f"list starting with {first!r}"
        case _:                             # wildcard — the default
            return "unknown"

print("\nclassify:", classify({"gpa": 3.9}), "|", classify([10, 20]), "|", classify(42))


# --- 6. The Pythonic toolkit --------------------------------------------
roster = [Student("Ana", 3.9), Student("Ben", 1.8), Student("Cara", 3.2)]

print("\ngood standing:", [s.name for s in roster if s.gpa >= 2.0])   # comprehension
print("upper:", list(map(lambda s: s.name.upper(), roster)))         # map
at_risk = filter(lambda s: s.gpa < 2.0, roster)                      # filter the objects
print("at risk:", [s.name for s in at_risk])
print("all passing?", all(s.gpa >= 2.0 for s in roster))            # any/all over a generator

# reduce: fold a sequence down to a single value (here: product of gpas)
print("gpa product:", round(functools.reduce(lambda a, s: a * s.gpa, roster, 1.0), 2))

# itertools.groupby: group ADJACENT items — so sort by the key first!
by_standing = sorted(roster, key=lambda s: s.standing())
for standing, group in itertools.groupby(by_standing, key=lambda s: s.standing()):
    print(f"  {standing}: {[s.name for s in group]}")

# generator: produce values lazily; great for huge data
def gpas(students):
    for s in students:
        yield s.gpa

gen = gpas(roster)
print("\nmean gpa:", round(class_average(list(gen)), 2))
print("second pass:", list(gen))   # [] — a generator is exhausted after one pass

# walrus := : assign and test in one step
if (n := len(roster)) > 2:
    print(f"\n{n} students enrolled")
