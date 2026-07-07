---
marp: true
title: "第 10 课 — 模块、面向对象与 Python 惯用法"
paginate: true
---

# 第 10 课
## 模块、面向对象与 Python 惯用法

---

## 模块：把代码拆进多个文件

```python
# grades.py
def letter_grade(score): ...
def class_average(scores): ...

# analysis.py
from grades import letter_grade, class_average
```

一个 `.py` 文件就是一个**模块**。`import` 让它的函数在别处复用 → 不再复制粘贴。

---

## `__main__` 守卫

```python
# grades.py
if __name__ == "__main__":
    print(letter_grade(85))   # 只在直接执行 grades.py 时运行
```

被 `import grades` 时，`__name__` 是 `"grades"`，这块代码就被跳过。
一个文件既能当脚本运行，又能当库导入。

---

## OOP：为领域实体建模

```python
class Student:
    def __init__(self, name, gpa):   # 构造器
        self.name = name
        self.gpa = gpa
    def __str__(self):               # 打印时的样子
        return f"{self.name} ({self.gpa})"

ana = Student("Ana", 3.9)
print(ana)        # Ana (3.9)
```

🧠 类就是一份*操作性定义*：哪些属性和行为"算"一个 Student。
`self` = "眼下这一个学生"。

---

## @property：赋值时校验

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

现在 `ana.gpa = 5.0` 会抛错——对象捍卫自己的完整性。
（`_gpa` 的前导下划线是"内部实现，请勿触碰"的约定；
Python 选择信任你，而不是强制。）

---

## 继承

```python
class GradStudent(Student):
    def __init__(self, name, gpa, advisor):
        super().__init__(name, gpa)    # 复用父类的初始化
        self.advisor = advisor
    def __str__(self):
        return super().__str__() + f" — {self.advisor}"
```

`GradStudent` *是一种* `Student`，再加点料。`super()` 调用父类。

---

## Python 惯用法工具箱（巡礼）

```python
[s.name for s in roster if s.gpa >= 2.0]   # 推导式（第 4 课）
list(map(lambda s: s.name.upper(), roster))# map：对每个都应用
list(filter(lambda s: s.gpa < 2.0, roster))# filter：留下符合的
for i, s in enumerate(roster): ...          # 序号 + 元素
for a, b in zip(names, scores): ...         # 并排走
```

---

## 生成器与海象运算符

```python
def gpas(students):
    for s in students:
        yield s.gpa          # 一次产出一个 —— 大数据也不占内存

g = gpas(roster)
list(g)   # ？
list(g)   # ？ ← 跑两次——有什么变化？（见下方陷阱区）

if (n := len(roster)) > 30:   # 海象 := ：赋值 + 判断一步完成
    print(f"{n} students")
```

---

## 轮到你了

`examples/session-10/practice.md`：
1. 从 `grades.py` 导入。2. 写带校验的 `Student` 类。
3. 加上用 `super()` 的 `GradStudent`。4. 推导式 + `map` + `filter` + 一个生成器。

---

# 更进一步
## 用对象做设计

---

## `__repr__` 和它的伙伴们

```python
class Student:
    def __repr__(self):                    # 给开发者看（REPL、列表、日志）
        return f"Student({self.name!r}, {self.gpa})"
    def __eq__(self, other):
        return (self.name, self.gpa) == (other.name, other.gpa)
    def __lt__(self, other):               # "小于" —— sorted() 直接可用
        return self.gpa < other.gpa

sorted(roster)                              # 不再需要 key=
```

双下方法让你的对象举止如内置类型：可打印、可比较、可排序——
甚至**可相加**：定义 `__add__(self, other)`，`total = quiz + final` 就能跑。
所谓"运算符重载"，仅此而已。

---

## `@dataclass`，进阶版

```python
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    gpa: float = 0.0
    courses: list = field(default_factory=list)   # 千万别写 courses: list = []
```

`default_factory=list` 就是第 5 课"可变默认值"法则的类版本——每个实例
一个新列表。`@dataclass(frozen=True)` 给你一条不可变记录。

---

## `@classmethod`：备选构造器

```python
@dataclass
class Student:
    name: str
    score: int

    @classmethod
    def from_row(cls, row):                # CSV 行（第 8 课）-> 对象
        return cls(row["name"], int(row["score"]))

roster = [Student.from_row(r) for r in csv.DictReader(f)]
```

`cls` 就是类本身。套路：**文件格式挡在边缘，程序内部全是对象**。
（`@staticmethod` 是第三种口味：住在类命名空间里的普通函数——
没有 `self`，也没有 `cls`。）

---

## 组合优先于继承

```python
class Cohort:                    # Cohort 拥有 Student（组合 ✅）
    def __init__(self, name):
        self.students = []

class GradStudent(Student):      # GradStudent 是一种 Student（继承 ✅）
    ...
```

只有真正的"是一种"关系才继承。拿不准时，让对象持有对象——
更灵活，也更好测试。

---

## 类属性 vs 实例属性——铁律

```python
class Course:
    school = "Ed School"         # 类属性：所有实例共享 —— 只放常量
    def __init__(self):
        self.students = []       # 实例属性：每个对象自己一份
```

可变数据永远放进 `__init__`。（你踩过那个共享列表陷阱——这就是它教的法则。）
想用 `global` 的时候：能活过一次函数调用的状态，应该住在对象上。

---

## 生成器管道

```python
def to_ints(rows):
    for r in rows:
        try:
            yield int(r)
        except ValueError:
            pass

def in_range(vals, lo=1, hi=5):
    yield from (v for v in vals if lo <= v <= 5)

clean = list(in_range(to_ints(raw)))    # 消费之前，什么都不会跑
```

一级产出交给下一级——**惰性**、常数内存，百万行的文件也照吃。
（水面之下，每个 `for` 说的都是同一套协议：`iter()` 拿到迭代器，
`next()` 取到空为止。生成器就是天生会说这门话的对象。）

---

## 从脚本到项目

```text
survey_tool/
├── clean.py        # 校验函数
├── stats.py        # 汇总统计
├── report.py       # 主入口：python3 report.py
└── tests/test_clean.py
```

一个模块管一件事；`report.py` 导入其余部分；测试放旁边。`report.py` 里的惯例：

```python
def main():                      # 程序的正事，集中一处
    ...

if __name__ == "__main__":
    main()
```

每一种原料你都已经认识——这只是摆盘。（若 `pytest` 找不到 `tests/`，
在里面放一个空的 `__init__.py`，把它标记为包。）

---

## 轮到你了——第二轮

`examples/session-10/practice.md` → **In class — going deeper**：
可排序的 `Student`、带 `default_factory` 的 dataclass、`from_row`，
以及一条两级生成器管道。

---

## 陷阱回顾

- `self` 就是"这一个实例"——没有魔法。
- 生成器只能遍历**一次**，之后就空了。
- `__main__` 守卫防止被导入的模块跑演示代码。
- 函数或字典能解决的，别硬上类。

## 小结
你已经能把代码组织成模块和类，写出地道的 Python。
**下一步（可选）：** 毕业项目——把一切串起来。

---

## 课后作业（毕业项目之前）

*课外完成——不计入课堂时间。完整题目 + 参考答案：`examples/session-10/practice.md` → **Homework**。*

1. **`Student.courses`** —— 课程列表 + *计算出的* `gpa`——数据和守护它的规则在一起。
2. **`Cohort` 类** —— 装着一群 `Student`；`mean_gpa()`、`at_risk()`。
3. **Pythonic 重写** —— 三个给定循环 → 推导式、生成器、`map`。
