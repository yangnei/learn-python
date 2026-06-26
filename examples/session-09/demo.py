"""
Session 9 — Modules, OOP & the Pythonic Toolkit
Run me from this folder:  python3 demo.py
"""
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


ana = Student("Ana", 3.9)
print("\n", ana)                    # uses __str__
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

print("\n", GradStudent("Ben", 3.4, "Dr. Lee"))


# --- 4. The Pythonic toolkit --------------------------------------------
roster = [Student("Ana", 3.9), Student("Ben", 1.8), Student("Cara", 3.2)]

print("\ngood standing:", [s.name for s in roster if s.gpa >= 2.0])   # comprehension
print("upper:", list(map(lambda s: s.name.upper(), roster)))         # map
at_risk = filter(lambda s: s.gpa < 2.0, roster)                      # filter the objects
print("at risk:", [s.name for s in at_risk])

for i, s in enumerate(roster, start=1):                              # enumerate
    print(i, s.name)

# generator: produce values lazily; great for huge data
def gpas(students):
    for s in students:
        yield s.gpa

g = gpas(roster)
print("\nmean gpa:", round(class_average(list(g)), 2))
print("second pass:", list(g))     # [] — a generator is exhausted after one pass

# walrus := : assign and test in one step
if (n := len(roster)) > 2:
    print(f"\n{n} students enrolled")
