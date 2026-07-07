# 第 1 课 —— 练习：运行 Python、变量与类型

每个答案都自己敲一遍。**运行之前先预测输出。** 参考答案在最后。

## 课堂练习

### 任务 1 —— REPL 热身
在 REPL（`python3`）里查看这些的类型：`42`、`42.0`、`"42"`、`True`、`None`、`7/2`、`7//2`。
*哪个让你意外？*（提示：`7/2`。）

### 任务 2 —— GPA 报告器（`gpa.py`）
读入姓名和 GPA（小数）。打印：
`"<name>'s GPA is <保留两位小数>, which is <87.5%> of a 4.0 scale."`

### 任务 3 —— 问卷年龄段（`age.py`）
读入年龄（整数）。打印年龄，以及"活过的月份数"（年龄 × 12）。
然后故意输入 `twenty` 而不是数字，**读一读报错的最后一行。**

### 任务 4 —— 进阶：字符串陷阱
不做转换时，输入 `2` 和 `3`，`input("a: ") + input("b: ")` 会打印什么？
现在修好它，让它打印 `5`。

### 加餐 —— Python 惯用法速练
盖住 `# ->` 后面的答案，逐行预测，再运行。

```python
a, b = 1, 2
a, b = b, a;          print(a, b)        # -> 2 1   （交换，不用临时变量）
print(f"{a + b = }")                     # -> a + b = 3   （自带说明的 f-string）
print("CS50".lower(), "  hi ".strip())   # -> cs50 hi
print("@" in "ana@uni.edu", len("data")) # -> True 4   （成员判断 + 长度）
```

## 课堂练习——更进一步（第二小时）

### E1 —— f-string 格式化速练
给定 `pi = 3.14159265`、`n = 9876543`、`rate = 0.4567`，精确打印出：
`3.14` · `9,876,543` · `45.7%` · `pi = 3.14159265`（自带说明的形式）。

### E2 —— 入学周数
扩展 `age.py`：再报告年龄折合的**周数**（每年 52 周），带千位分隔符。

### D1 —— 对齐的成绩单行
把三名学生（`name, score, rate`）打印成对齐的列：姓名左对齐补到 10 位、
分数右对齐保留 1 位小数、比率用百分数。三行必须对得整整齐齐。

### D2 —— 姓名清洗器
用*链式*字符串方法把 `"  aDA lovelace "` 变成 `"Ada Lovelace"`，然后报告结果的
`len()`，以及它是否 `.startswith("Ada")`。

### D3 —— 整份 + 余数
1. 用 `//` 和 `%` 把 130 分钟换算成 `2 h 10 min`。
2. 用 `%` 把学号 `[101, 102, 103, 104, 105, 106]` 轮流分进 0/1/2 三个讨论组。

## 课后作业（第 2 课之前）

*约 30–45 分钟，课外完成——不计入课堂时间。先都试一遍，再看答案。*

### H1 —— 单位换算器（`convert.py`）
读入英里数（可以是小数）。打印公里数（`× 1.60934`，保留 2 位小数）和带千位
分隔符的米数：
`5.0 miles = 8.05 km (8,047 meters)`

### H2 —— 报错演练
在脚本里逐个故意写坏下面三行，运行，并抄下每个报错的最后一行：
1. `int("ten")`
2. `"age: " + 21`
3. 在 `name = "Ada"` 之后写 `print(nmae)`（故意打错）
然后各用一句话说明：错误的*名字*告诉了你什么？

### H3 —— 类型预测表
先预测每个的 `type(...)`（或输出），再到 REPL 里验证：
`7/2` · `7//2` · `7.0//2` · `"7"*2` · `int("7")*2` · `7 == 7.0` · `None` · `input`
（不加括号！）· `print("hi")`

---

## 参考答案

### 课堂练习

```python
# 任务 2 —— gpa.py
name = input("Name: ")
gpa = float(input("GPA: "))
print(f"{name}'s GPA is {gpa:.2f}, which is {gpa/4:.1%} of a 4.0 scale.")

# 任务 3 —— age.py
age = int(input("Age: "))
print(f"You are {age} years old, about {age*12} months.")
# 输入 "twenty" -> ValueError: invalid literal for int() with base 10: 'twenty'

# 任务 4
# "2" + "3" -> "23"  （字符串拼接）
a = int(input("a: ")); b = int(input("b: "))
print(a + b)          # 5
```

### 课堂练习——更进一步

```python
pi, n, rate = 3.14159265, 9876543, 0.4567
print(f"{pi:.2f}")        # 3.14
print(f"{n:,}")           # 9,876,543
print(f"{rate:.1%}")      # 45.7%
print(f"{pi = }")         # pi = 3.14159265

# E2
age = int(input("Age: "))
print(f"That's about {age * 52:,} weeks.")

# D1
for name, score, rate in [("Ana", 91.456, 0.873), ("Ben", 58.0, 0.412), ("Cara", 73.2, 0.65)]:
    print(f"{name:<10}{score:>8.1f}{rate:>8.1%}")

# D2
clean = "  aDA lovelace ".strip().title()
print(clean, len(clean), clean.startswith("Ada"))   # Ada Lovelace 12 True

# D3
minutes = 130
print(f"{minutes // 60} h {minutes % 60} min")      # 2 h 10 min
for sid in [101, 102, 103, 104, 105, 106]:
    print(sid, "-> group", sid % 3)
```

### 课后作业

```python
# H1 —— convert.py
miles = float(input("Miles: "))
km = miles * 1.60934
print(f"{miles} miles = {km:.2f} km ({round(km * 1000):,} meters)")
```

H2 —— 最后一行及其含义：
1. `ValueError: invalid literal for int() with base 10: 'ten'` —— 参数*类型*对，值不能用。
2. `TypeError: can only concatenate str (not "int") to str` —— 类型本身与操作不匹配。
3. `NameError: name 'nmae' is not defined` —— 用了从未赋值过的名字（通常是笔误）。

```python
# H3 —— type() 会说什么
7 / 2         # float —— / 永远给浮点数（3.5）
7 // 2        # int   —— 两个整数的整除（3）
7.0 // 2      # float —— 值取整，类型是浮点（3.0）
"7" * 2       # str   —— 重复："77"，不是数学
int("7") * 2  # int   —— 14
7 == 7.0      # bool  —— True（数字按值比较）
None          # NoneType
input         # builtin_function_or_method —— 函数也是值
print("hi")   # 打印 hi，然后求值为 None（print 不返回东西）
```
