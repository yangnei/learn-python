# 第 2 课 —— 练习：动态类型陷阱

每个答案都自己敲一遍。**运行之前先预测输出。** 参考答案在最后。

## 课堂练习

### 预测输出闯关
对每一行，写出*为什么*（一句话）。先预测，再运行验证。

```python
True + True            # 2     —— 布尔值是整数；True 是 1
3 == 3.0               # True  —— 数字按值比较
0.1 + 0.2 == 0.3       # False —— 二进制浮点舍入
5 == "5"               # False —— 类型不同，不报错
5 > "5"                # 💥    —— int 和 str 无法排大小
[1,2] == (1,2)         # False —— 列表和元组是不同类型
bool("0")              # True  —— 非空字符串是真值
x=[1]; y=x; x.append(2); y   # [1,2] —— y 是 x 的别名
```

### 编写 `clean_score()`
写一个函数，把值安全地转成 0–100 范围内的浮点数：

```python
def clean_score(value):
    """
    接受 87、87.0 或 "87"，返回 87.0（浮点数）。
    - 超出 0..100 的值给出明确提示并拒绝（返回 None）。
    - 浮点比较要安全（不用精确 ==）。
    """
```
用这些测试：`87`、`87.0`、`"87"`、`"eighty"`、`120`、`True`。
*`True` 会怎样？为什么？（提示：bool 是一种 int……）*

### 加餐 —— Python 惯用法速练
盖住 `# ->` 后面的答案，逐行预测，再运行。

```python
x = int("257"); y = int("257")
print(x == y, x is y)                # -> True False   （值相等，对象不同）
print(float("nan") == float("nan"))  # -> False        （NaN 不等于任何东西，包括它自己）
```

## 课堂练习——更进一步（第二小时）

### E1 —— isinstance 速练
逐个预测，再运行：
```python
isinstance(True, int)
type(True) is int
isinstance(3.0, int)
isinstance("3", (int, float))
isinstance(3, (int, float))
```

### E2 —— 值相同，对象相同吗？
不运行：执行 `a = [1, 2]; b = [1, 2]; c = a` 之后，`a == b`、`a is b`、`a is c`
各是什么？接着 `c.append(3)` —— `a` 变成什么？运行验证全部四问。

### D1 —— 类型转换预测表
逐个预测，再运行：`int("42")` · `int("4.2")` · `float("4.2")` · `int(4.9)` ·
`int(float("4.2"))` · `str(4.2) + "!"` · `bool("False")`。

### D2 —— `Decimal` 重算
证明 `Decimal("0.1") + Decimal("0.2") == Decimal("0.3")` 而浮点版为 False——
再检查成绩权重：`0.1 + 0.2 + 0.3 == 0.6` 用 `Decimal` 能修好吗？
为什么 Decimal 必须**从字符串**构造？

### D3 —— `describe(x)`
`None` 返回 `"missing"`、`""` 返回 `"empty"`、`0`/`0.0` 返回 `"zero"`（但 `False`
**不算**），其余返回 `"value"`。在 `[None, "", 0, 0.0, False, "0", 5]` 上验证。
（小心：`False == 0` —— 正是第 2 课自己的陷阱。哪个工具能区分它们？）

## 课后作业（第 3 课之前）

*约 30–45 分钟，课外完成——不计入课堂时间。先都试一遍，再看答案。*

### H1 —— 陷阱日志
从今天约 18 个陷阱中挑出**最让你意外的五个**。每个写下：那行代码、你原本的
错误预期、以及 Python 为什么那样回答——一句话，用自己的话。（这本日志是你
专属速查表的种子。）

### H2 —— `approx_equal(a, b, tol=1e-9)`
写出你从今往后替代 `==` 的浮点比较；它必须让 `approx_equal(0.1 + 0.2, 0.3)`
得到 `True`。手写一版（`abs`），再用 `math.isclose` 写一版。

### H3 —— `is_missing(x)`
**只**对 `None` 返回 `True`——对 `0`、`0.0`、`""`、`False` 都不行。在全部五个值
上验证。（提示：这正是 `is` 的用武之地。）

---

## 参考答案

### 课堂练习

```python
import math

def clean_score(value):
    # 显式拒绝 bool —— 否则它会冒充 int 混进来（True == 1）。
    if isinstance(value, bool):
        print(f"Rejected {value!r}: looks like a flag, not a score.")
        return None
    try:
        score = float(value)              # 同时处理 int、float 和数字字符串
    except (ValueError, TypeError):
        print(f"Rejected {value!r}: not a number.")
        return None
    if not 0 <= score <= 100:
        print(f"Rejected {value!r}: out of range 0–100.")
        return None
    return score

for v in [87, 87.0, "87", "eighty", 120, True]:
    print(v, "->", clean_score(v))
# 87->87.0, 87.0->87.0, "87"->87.0, "eighty"->None, 120->None, True->None
```
关键教训：`float(True)` 是 `1.0`，不显式检查 bool 的话，一个开关标志就会冒充
有效分数。这就是 `bool ⊂ int` 陷阱进了真实函数的样子。

### 课堂练习——更进一步

```python
# E1
isinstance(True, int)          # True  —— bool 是 int 的子类
type(True) is int              # False —— 精确类型是 bool
isinstance(3.0, int)           # False —— float 不是 int 的子类
isinstance("3", (int, float))  # False —— 长得像数字的字符串仍是 str
isinstance(3, (int, float))    # True  —— 元组表示"其中任意一种"

# E2
a == b   # True  —— 值相同
a is b   # False —— 两个不同的列表对象
a is c   # True  —— c 是 a 的对象上的另一个标签
# c.append(3) 之后：a == [1, 2, 3] —— 通过 c 的修改透过 a 显现

# D1
int("42")          # 42
# int("4.2")       -> ValueError —— int() 只解析整数文本
float("4.2")       # 4.2
int(4.9)           # 4  （截断）
int(float("4.2"))  # 4  （两步走）
str(4.2) + "!"     # '4.2!'
bool("False")      # True —— 任何非空字符串都是真值！

# D2
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))                    # True
print(Decimal("0.1") + Decimal("0.2") + Decimal("0.3") == Decimal("0.6"))   # True
# 要从字符串构造：Decimal(0.1) 会把浮点数的二进制误差原样带进来。

# D3
def describe(x):
    if x is None:
        return "missing"
    if x == "":
        return "empty"
    if isinstance(x, bool):        # bool ⊂ int —— 先查开关标志
        return "value"
    if isinstance(x, (int, float)) and x == 0:
        return "zero"
    return "value"

for v in [None, "", 0, 0.0, False, "0", 5]:
    print(repr(v), "->", describe(v))
# None missing · "" empty · 0 zero · 0.0 zero · False value · "0" value · 5 value
```

### 课后作业

H1 —— 任选五个，例如：`0.1 + 0.2 == 0.3`（二进制浮点）、`True == 1`（bool ⊂ int）、
`5 == "5"`（不做跨类型转换）、`[1, 2] == (1, 2)`（列表 ≠ 元组）、对相等列表用 `is`
（同一 ≠ 相等）。用自己的话写*为什么*比挑哪个更重要。

```python
# H2
import math

def approx_equal(a, b, tol=1e-9):
    return abs(a - b) <= tol
    # 或者：return math.isclose(a, b, abs_tol=tol)

print(approx_equal(0.1 + 0.2, 0.3))   # True

# H3
def is_missing(x):
    return x is None          # 身份判断 —— 只有 None 本身能通过

for v in [None, 0, 0.0, "", False]:
    print(repr(v), "->", is_missing(v))   # 只有 None -> True
```
