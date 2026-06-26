---
marp: true
title: "Session 10 — Modules, OOP & the Pythonic Toolkit"
paginate: true
---

# Session 10
## Modules, OOP & the Pythonic Toolkit

Organize code into reusable pieces — and finish with the moves experts use.

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
[s.name for s in roster if s.gpa >= 2.0]   # comprehension (from S5)
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
list(g)   # [3.9, 1.8, ...]
list(g)   # []  ← a generator is exhausted after one pass

if (n := len(roster)) > 30:   # walrus := : assign + test in one step
    print(f"{n} students")
```

---

## Your turn

`examples/session-10/practice.md`:
1. Import from `grades.py`. 2. Build the validating `Student` class.
3. Add `GradStudent` with `super()`. 4. Comprehension + `map` + `filter` + a generator.

---

## Traps recap

- `self` is just "this instance" — not magic.
- A generator iterates **once**, then it's empty.
- The `__main__` guard keeps imported modules from running their demo code.
- Don't reach for a class when a function or dict will do.

## Summary
You can structure code into modules and classes and write idiomatic Python.
**Next (optional):** the capstone — put it all together.
