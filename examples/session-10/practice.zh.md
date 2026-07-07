# 第 10 课 —— 练习：模块、面向对象与 Python 惯用法

每个答案都自己敲一遍。**运行之前先预测输出。** 参考答案在最后。

## 课堂练习

本文件夹的文件：`grades.py`（供你导入的模块）、`demo.py`（成品示例）。

### 任务 1 —— 使用模块
在新文件里 `from grades import letter_grade, class_average` 并调用两者。
为什么导入时 `grades.py` 里的 `if __name__ == "__main__":` 块**不会**运行？

### 任务 2 —— 带校验属性的类
写 `Student(name, gpa)`：
- `__str__` → `"Ana: 3.9 (Good)"`，
- `standing()` → gpa ≥ 2.0 时 `"Good"` 否则 `"Probation"`，
- `gpa` 的 `@property` setter：超出 0–4 抛 `ValueError`。
证明 setter 会拒绝 `5.0`。

### 任务 3 —— 继承
加 `GradStudent(Student)`：多存一个 `advisor`，用 `super().__init__(...)`；
重写 `__str__` 把导师名附在后面。

### 任务 4 —— Python 惯用法工具箱
给定一组 `Student`：
1. 状态良好者的姓名（列表推导式），
2. 大写的姓名（`map`），
3. 有风险的学生（`filter`），
4. 用一个 `yield` 每个 gpa 的**生成器**求平均 gpa——然后展示第二次遍历时它已空。

### 加餐 —— Python 惯用法速练
盖住 `# ->` 后面的答案，逐行预测，再运行。

```python
from dataclasses import dataclass

@dataclass                           # 自动 __init__、__repr__、__eq__
class Point:
    x: int
    y: int
print(Point(1, 2), Point(1, 2) == Point(1, 2))   # -> Point(x=1, y=2) True

def head(v):
    match v:                         # 结构化模式匹配（3.10+）
        case [first, *_]: return first
        case _: return None
print(head([9, 8]), head(5))         # -> 9 None
```

## 课堂练习——更进一步（第二小时）

### 任务 1 —— 亲眼看守卫
在 `grades.py` 顶部加 `print("running as", __name__)`。先直接运行文件，再在
REPL 里 `import grades`——各打印什么？为什么？

### 任务 2 —— `@dataclass` 版 Student
把普通（不带校验的）`Student` 改写成 `@dataclass`。白得了什么？
在两个等值学生上检查 `repr` 和 `==`。

### 任务 3 —— 可排序的学生
给 `Student` 写 `__repr__`、`__eq__` 和按 gpa 的 `__lt__`，让 `sorted(roster)`
**不用** `key=` 就能跑。证明它。

### 任务 4 —— 正确的 `dataclass`
写 `@dataclass class Course: name: str; roster: list = field(default_factory=list)`。
`roster: list = []` 为什么是错的——这是第 5 课哪个 bug 的类版本？

### 任务 5 —— `from_row`
给 `Student` 加 `from_row(cls, row)`：从 CSV 的 `DictReader` 行构造实例
（记得转换类型！）。为什么 `@classmethod` 是它的正确归宿？

### 任务 6 —— 两级管道
写生成器 `to_ints(cells)`（跳过转不动的）和 `in_range(vals, lo=1, hi=5)`；
串起来处理 `["5", "3", "N/A", "7", "1"]`。真正的计算发生在什么时候？

## 课后作业（毕业项目之前）

*约 30–45 分钟，课外完成——不计入课堂时间。先都试一遍，再看答案。*

### 任务 1 —— 课程与计算出的 GPA
扩展 `Student`：一个 `(课程名, 绩点)` 元组的 `courses` 列表、一个校验 0–4 的
`add_course(name, points)` 方法，并把 `gpa` 做成**计算属性**（课程绩点的均值；
没有课程时为 `None`）。不存任何会过期的 gpa。

### 任务 2 —— `Cohort` 类
`Cohort(name)` 装着一群 `Student`：`add(student)`、`mean_gpa()`（跳过没有 gpa
的学生）、`at_risk(threshold=2.0)` 返回姓名，`__str__` →
`"Fall-26 (3 students)"`。想清楚学生列表放哪——记得类变量陷阱。

### 任务 3 —— Pythonic 重写
把每段改写成一行推导式 / 生成器 / `map`：
```python
# 1 -> 列表推导式
out = []
for s in roster:
    if s.gpa is not None and s.gpa >= 3.5:
        out.append(s.name)

# 2 -> sum() 里的生成器（不建列表）
total = 0
for s in roster:
    total += len(s.courses)

# 3 -> map（或推导式——说说你选哪个、为什么）
labels = []
for s in roster:
    labels.append(str(s))
```

---

## 参考答案

### 课堂练习

见 `demo.py`——任务 2–4 的完整实现。要点：

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

[s.name for s in roster if s.gpa >= 2.0]          # 推导式
list(map(lambda s: s.name.upper(), roster))        # map
[s.name for s in filter(lambda s: s.gpa < 2.0, roster)]   # filter
def gpas(rs):
    for s in rs: yield s.gpa                        # 生成器（遍历一次即耗尽）
```
任务 1：`__name__` 只有在文件被**直接运行**时才是 `"__main__"`；被 `import` 时
它是 `"grades"`，那段演示代码被跳过——这就是一个文件既能当脚本又能当库的原理。

### 课堂练习——更进一步

```python
# 任务 1
# python3 grades.py   -> "running as __main__"  （这个文件就是程序本体）
# >>> import grades   -> "running as grades"    （于是 __main__ 块被跳过）

# 任务 2
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    gpa: float

# 白得的：__init__、好读的 __repr__、逐字段的 __eq__：
print(Student("Ana", 3.9) == Student("Ana", 3.9))   # True

# 任务 3
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
print(sorted(roster))    # Ben、Cara、Ana —— __lt__ 教会了 sorted() 怎么排

# 任务 4
from dataclasses import dataclass, field

@dataclass
class Course:
    name: str
    roster: list = field(default_factory=list)
# `roster: list = []` 会让所有 Course 共用同一个列表 —— 第 5 课的可变默认值
# bug 换了件类的外衣。default_factory 给每个实例现造一个新列表。

# 任务 5
@dataclass
class Student2:
    name: str
    score: int

    @classmethod
    def from_row(cls, row):
        return cls(row["name"], int(row["score"]))
# 它构造的是类本身的实例，所以属于类（cls）而不属于任何一个对象——
# "备选构造器"模式。

# 任务 6
def to_ints(cells):
    for c in cells:
        try:
            yield int(c)
        except ValueError:
            pass

def in_range(vals, lo=1, hi=5):
    yield from (v for v in vals if lo <= v <= hi)

pipeline = in_range(to_ints(["5", "3", "N/A", "7", "1"]))
print(list(pipeline))    # [5, 3, 1] —— 直到 list() 把值拉过来才真正运行
```

### 课后作业

```python
# 任务 1
class Student:
    def __init__(self, name):
        self.name = name
        self.courses = []                      # (课程, 绩点) 元组

    def add_course(self, course, points):
        if not 0 <= points <= 4:
            raise ValueError(f"{points} outside 0-4")
        self.courses.append((course, points))

    @property
    def gpa(self):                             # 计算出来的 —— 永不过期
        if not self.courses:
            return None
        return sum(p for _, p in self.courses) / len(self.courses)

    def __str__(self):
        return f"{self.name} (GPA {self.gpa})"

# 任务 2
class Cohort:
    def __init__(self, name):
        self.name = name
        self.students = []                     # 放在实例上 —— 千万不是类变量！

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

# 任务 3
names  = [s.name for s in roster if s.gpa is not None and s.gpa >= 3.5]
total  = sum(len(s.courses) for s in roster)      # 生成器 —— 内存里不建列表
labels = list(map(str, roster))   # 或 [str(s) for s in roster] —— 都行；
                                  # 多数人觉得推导式更好读
```
