---
marp: true
title: "第 5 课 — 函数、作用域与复用"
paginate: true
---

# 第 5 课
## 函数、作用域与复用

---

## 定义与调用

```python
def class_average(scores):
    """Return the mean of a list of scores."""
    return sum(scores) / len(scores)

class_average([91, 58, 73])     # 74.0
```

🧠 函数就是公式/编码方案：同样的输入 → 同样的输出。

---

## return vs print

```python
def avg(xs): return sum(xs) / len(xs)   # 把值交回去
def show(xs): print(sum(xs) / len(xs))  # 只是显示

x = avg([1,2,3])     # x = 2.0
y = show([1,2,3])    # 打印 2.0，但 y 是 None！
```

`print` 是给人看的；`return` 才把值交给下一步。

---

## 参数：位置、关键字、默认值

```python
def grade(score, scale=100, passing=60):
    ...
grade(85)                 # 使用默认值
grade(85, passing=50)     # 关键字参数
```

⚠️ 默认值必须是**不可变的**（数字、字符串、`None`）——绝不要用 `[]` 或 `{}`。

---

## *args / **kwargs

```python
def total(*args):        # 任意个位置参数 -> 元组
    return sum(args)
total(1, 2, 3)           # 6

def tag(**kwargs):       # 任意个关键字参数 -> 字典
    return kwargs
tag(name="Ana", gpa=3.9) # {'name':'Ana','gpa':3.9}

func(*my_list)           # 把列表摊开成参数
func(**my_dict)          # 把字典摊开成关键字参数
```

---

## 陷阱：可变默认参数 😱

```python
def add_student(name, roster=[]):    # ❌
    roster.append(name)
    return roster

add_student("Ana")    # ？
add_student("Ben")    # ？ ← 列表会一直留着吗？（见下方陷阱区）
```

默认的 `[]` 只在**定义时创建一次**。下一页给出修法。

---

## 修法：默认用 None

```python
def add_student(name, roster=None):   # ✅
    if roster is None:
        roster = []
    roster.append(name)
    return roster
```

**法则：** 默认值想用可变对象？改用 `None`，在函数体内创建。

---

## 作用域（LEGB）与全局变量

Python 按此顺序查名字：**L**ocal → **E**nclosing → **G**lobal → **B**uilt-in。

```python
count = 0
def bump():
    count = count + 1   # 💥 UnboundLocalError
```
一旦给 `count` 赋值，它就成了局部变量。避免 `global`；**返回**新值再重新赋值。

---

## 文档字符串与类型标注

```python
def class_average(scores: list[float]) -> float:
    """Return the arithmetic mean of `scores`."""
    return sum(scores) / len(scores)
```

类型标注表达意图。**运行时并不强制执行**（`mypy` 可以检查）。
大型项目会规范文档字符串字段（`:param:`、`:return:`、`:raises:`），
这样 **Sphinx** 之类的工具能直接从代码生成文档网站。

---

## 轮到你了

`examples/session-05/practice.md`：
1. 一个小型成绩函数库（带文档字符串 + 类型标注）。
2. 复现可变默认参数 bug，然后修好它。
3. 用 `*args` 写 `summary(*scores)`。

---

# 更进一步
## 函数也是值

---

## 函数是对象

```python
f = letter_grade            # 不加 () —— 函数本体
f(85)                       # "B"
sorted(roster, key=grade_of)          # 第 4 课起你就在传函数了
stats = {"mean": class_average, "max": max}
stats["mean"]([91, 58, 73])           # 按名字调度
```

`key=lambda …` 从来不是魔法——你一直在把函数递给 `sorted`。

---

## `lambda`，说实话

```python
lambda s: s["score"]        # 只能是一个表达式，没有语句和文档字符串
```

作为一次性的 `key=` 很完美。一旦需要第二行、或需要名字才能看懂——
就升级成 `def`。

---

## 闭包：会记事的函数

```python
def make_curver(bonus):
    def curve(score):
        return min(score + bonus, 100)
    return curve             # 返回函数，`bonus` 随身携带

gentle = make_curver(5)
harsh_year = make_curver(2)
gentle(96)                   # 100
```

一个函数**工厂**。（前面那个"循环里的 lambda"陷阱就是它——
捕获的是变量，不是值。）

---

## 第一个装饰器

```python
def announce(f):
    def wrapper(*args, **kwargs):
        print(f"calling {f.__name__}{args}")
        return f(*args, **kwargs)
    return wrapper

@announce                    # 语法糖：curve = announce(curve)
def curve(score):
    return min(score + 5, 100)
```

装饰器**包裹**一个函数，附加额外行为。你会不停地*用到*它们
（`@property`、`@cache`、`@pytest.mark...`）——现在你知道 `@` 是什么了。

---

## 锁定调用方式

```python
def curve(scores, *, bonus=5):     # * 之后的参数只能用关键字传
    ...
curve(xs, bonus=3)     # ✅ 一目了然
curve(xs, 3)           # 💥 TypeError —— 不许来历不明的位置参数
```

仅关键字参数让一个月后的调用代码依然可读。

---

## 能自我检验的文档字符串

```python
def class_average(scores):
    """Mean of scores.

    >>> class_average([90, 80, 70])
    80.0
    """
    return sum(scores) / len(scores)
```

`python -m doctest grades.py` 会运行每个 `>>>` 示例并在不符时报错——
文档不再会悄悄过期。

---

## 轮到你了——第二轮

`examples/session-05/practice.md` → **In class — going deeper**：
自己写 `apply_to_all`、一个加分工厂、一个 `@announce` 装饰器，以及一个 doctest。

---

## 陷阱回顾

- 可变默认参数 → 用 `None`。
- `print` ≠ `return`（忘了 return → `None`）。
- 在函数内给全局变量赋值 → `UnboundLocalError`。
- 类型标注不强制执行。

## 小结
你已经能写出可复用、有文档、可复现的函数。
**下一课：** 第 6 课——递归。

---

## 课后作业（第 6 课之前）

*课外完成——不计入课堂时间。完整题目 + 参考答案：`examples/session-05/practice.md` → **Homework**。*

1. **迷你统计库** —— `validate_score`、`curve`、`summarize`，带文档字符串 + 类型标注。
2. **`mean_ignoring_none(*values)`** —— `*args` 遇上数据清洗。
3. **作用域预测** —— 先说出会打印什么，再运行验证。
