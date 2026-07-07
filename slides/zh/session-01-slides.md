---
marp: true
title: "第 1 课 — 运行 Python、变量与类型"
paginate: true
---

# 第 1 课
## 运行 Python、变量与类型

---

## 为什么是 Python（对你而言）

- 免费、易读，是研究计算领域的通用语言。
- 是连接你的数据、统计与写作的"胶水"。
- 今天的目标：从零到"我跑通了一个程序"。

> 贯穿全课程的座右铭：**可读性至上**。

---

## 运行 Python 的两种方式

1. **REPL（交互式）** —— 输入 `python3`，出现 `>>>`，一次运行一行。适合做实验。
2. **脚本** —— 保存 `hello.py`，运行 `python3 hello.py`。适合正式工作。

```python
# hello.py
print("Hello, researcher")
```

---

## 变量 = 贴在对象上的标签

```python
n = 30          # 一个 int（整数）
mean = 3.7      # 一个 float（浮点数）
name = "Ada"    # 一个 str（字符串）
passed = True   # 一个 bool（布尔值）
missing = None  # "没有值"
```

`=` 是一个**动作**（"把这个标签贴到那个对象上"），**不是**数学等式。
所以 `n = n + 1` 完全合法。

🧠 统计里你也给量命名（`n`、`α`）——思路相同，只是这里的名字可以随时改贴。

---

## 五大核心类型

| 类型 | 示例 | 联想 |
|---|---|---|
| `int` | `30` | 计数 |
| `float` | `3.7` | 测量值 |
| `str` | `"Ada"` | 文本 |
| `bool` | `True`/`False` | 开关标志 |
| `NoneType` | `None` | 缺失 |

`type(x)` 会告诉你 x 是哪种类型。

---

## 输入与输出

```python
name = input("Your name: ")        # ⚠️ 永远是 str
age  = int(input("Your age: "))    # 立即转换
print("Hi", name, "— age", age)
```

**第一周的头号陷阱：** `input()` 给你的是文本。
`"5" + "3"` 是 `"53"`，不是 `8`。

---

## f-string（请用这个）

```python
score = 87.456
print(f"{name} scored {score:.1f}")   # 保留一位小数
print(f"{1234567:,}")                  # 1,234,567
print(f"{0.873:.1%}")                  # 87.3%
```

比用 `+` 拼接干净得多，也不会有类型错误。

---

## 类型转换

```python
int("42")     # 42
float("3.14") # 3.14
str(42)       # "42"
int(3.9)      # 3   （截断，不是四舍五入！）
round(3.9)    # 4
```

`int(input(...))` = 读入文本、转成数字，一步完成。

---

## 读懂报错信息（别慌）

```text
Traceback (most recent call last):
  File "x.py", line 3, in <module>
    age = int(input("Age: "))
ValueError: invalid literal for int() with base 10: 'thirty'
```

**先读最后一行。** 它说明了问题类型（`ValueError`）和出错的值（`'thirty'`）。

---

## 现场演示 & 轮到你了

- 演示：先写 `greet.py`，再做一个"距离毕业还有几年"的计算器。我们会故意弄坏一次。
- 你来：`examples/session-01/practice.md` —— 写一个 GPA/BMI 风格的小脚本。

---

# 更进一步
## 数字、字符串，以及它们周边的工具

---

## 算术运算，完整版

| 运算符 | 含义 | 示例 |
|---|---|---|
| `+ - *` | 常规运算 | `3 * 7` → `21` |
| `/` | 真除法 | `7 / 2` → `3.5` |
| `//` | 整除（向下取整） | `7 // 2` → `3` |
| `%` | 取余 | `7 % 2` → `1` |
| `**` | 乘方 | `2 ** 10` → `1024` |

优先级与数学一致（先 `**`，再 `* / // %`，最后 `+ -`）——拿不准时，**加括号**。
就地更新：`score += 5`、`count -= 1`、`total *= 2`。

---

## `%` 的用武之地

```python
n % 2 == 0            # 偶数？
student_id % 3        # 0、1 或 2 -> 轮流分进 3 个讨论组
minutes = 130
print(minutes // 60, "h", minutes % 60, "min")   # 2 h 10 min
```

🧠 `//` 和 `%` 搭配，把一个量拆成"整份 + 余数"——小时/分钟、页数/张数、分组/余下。

---

## 字符串自带方法

```python
name = "  aDA lovelace "
name.strip()          # "aDA lovelace"   （去掉首尾空白）
name.strip().title()  # "Ada Lovelace"   （可以链式调用！）
"CS50".lower()        # "cs50"
"a,b,c".count(",")    # 2
"ana@uni.edu".startswith("ana")   # True
"@" in "ana@uni.edu"  # True  （成员判断）
len("data")           # 4
```

方法**返回新字符串**——原来的从不改变（字符串不可变）。
字符串还能"乘"：`"ab" * 3` → `"ababab"` —— `print("=" * 40)` 画一条分隔线。

---

## f-string 进阶——对齐的报表

```python
name, score, rate = "Ana", 91.456, 0.873
print(f"{name:<10}{score:>8.1f}{rate:>8.1%}")
# Ana           91.5   87.3%
```

- `:<10` 左对齐补到 10 位 · `:>8` 右对齐到 8 位
- `:.1f` 一位小数 · `:,` 千位分隔 · `:.1%` 百分比
- `{score=}` 会打印 `score=91.456` ——调试神器。

---

## `print()`，微调版

```python
print("Ana", "Ben", "Cara", sep=" | ")   # Ana | Ben | Cara
print("Loading", end="...")              # 不换行——下一个 print 接着打
print('She said "wow"')                  # 换一种引号……
print("She said \"wow\"")                # ……或者用反斜杠转义
print("line one\nline two")              # \n = 字符串里的换行符
```

- `sep=` 决定参数之间的连接符（默认空格）；`end=` 决定行尾（默认 `"\n"`）。
- `\n` 和 `\"` 是**转义序列**——戴着反斜杠帽子的单个字符。

---

## 借用工具箱：`import`

```python
import math
math.sqrt(144)     # 12.0
math.floor(3.9)    # 3
math.ceil(3.1)     # 4
math.pi            # 3.141592653589793
```

一行代码借来一整个库。（`import` 的完整故事——连同 `pip`——在第 8 课。）

---

## 直接问 Python 本人

```python
help(round)      # 单个函数的说明书
dir(str)         # 字符串的全部方法
```

在 REPL 里，`_` 保存着上一个结果。这三个习惯能替你省下一半的网络搜索。

---

## 起不咬人的名字

- 变量和函数用 `snake_case`（蛇形命名）：`class_average`，而不是 `ClassAvg`。
- 名字要说明**它是什么**：`n_students`，而不是 `x`。
- 常量的约定写法：`MAX_SCORE = 100`（Python 不会强制——全大写是提醒人类的）。
- 注释解释**为什么**，而不是"是什么"：代码本身已经说明了是什么。
- 动手之前，先用大白话把步骤写出来（**伪代码**）——然后再翻译成代码。

---

## 轮到你了——第二轮

`examples/session-01/practice.md` → **In class — going deeper**：
格式化练习、姓名清洗器，以及 `%` 分组练习。

---

## 陷阱回顾

- `input()` → **永远是字符串**；用 `int()`/`float()` 转换。
- `print(a, b)`（逗号 → 空格）vs `print(a + b)`（必须同类型）。
- `int(3.9)` 截断成 `3`；要四舍五入用 `round()`。

## 小结
你已经会运行代码、给值命名、转换类型、格式化输出、读懂报错。
**下一课：** 第 2 课——动态类型陷阱。

---

## 课后作业（第 2 课之前）

*课外完成——不计入课堂时间。完整题目 + 参考答案：`examples/session-01/practice.md` → **Homework**。*

1. **单位换算器** —— 一个脚本：读入数值，用 f-string 漂亮地输出换算结果。
2. **报错演练** —— 故意弄坏三行代码；逐个读最后一行，说出错误名称。
3. **类型预测表** —— 先预测十个表达式的 `type(...)`，再到 REPL 里验证。
