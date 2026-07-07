# 第 9 课 —— 练习：正则表达式与文本清洗

每个答案都自己敲一遍。**运行之前先预测输出。** 参考答案在最后。

## 课堂练习

永远用原始字符串 `r"..."`。每个结果先预测再运行。

### 任务 1 —— 校验
写 `valid_university_email(addr)`，只对 `something@something.edu` 返回 `True`。
测试：`"ana@university.edu"`、`"ana@gmail.com"`、`"a@b.edu.evil.com"`。

### 任务 2 —— 用分组提取
从 `"Course ED1234 meets Tue"` 中用一个带两个捕获组的正则取出系别（`ED`）和
课号（`1234`）。

### 任务 3 —— 清洗
把 `"  too    much\t space "` 里成串的空白折叠成单个空格并去掉首尾。

### 任务 4 —— 挖掘自由文本
统计一组开放式回答里每个 `#话题标签` 出现的次数
（用 `re.findall(r"#(\w+)", text)` 和 `collections.Counter`）。

### 任务 5 —— 重排
用一个正则 + 分组把 `"Curie, Marie"` 变成 `"Marie Curie"`。

### 任务 6 —— 判断力
举一个用普通字符串方法（`.split()`、`.strip()`、`.replace()`）比正则更好、
更清楚的任务。

### 加餐 —— Python 惯用法速练
盖住 `# ->` 后面的答案，逐行预测，再运行。

```python
import re
m = re.search(r"(?P<year>\d{4})", "class of 2026")
print(m.group("year"), m.groupdict())   # -> 2026 {'year': '2026'}   （命名分组）
print(re.split(r"\s*,\s*", "a, b ,c")) # -> ['a', 'b', 'c']        （按逗号带空格切分）
```

## 课堂练习——更进一步（第二小时）

### 任务 1 —— 命名分组
用 `(?P<dept>...)` / `(?P<num>...)` 重做系别+课号提取，打印 `m.groupdict()`。

### 任务 2 —— regex101 实地考察
把你的邮箱模式贴进 regex101.com（flavor 选 **Python**）。逐符号读左栏的解释——
它说的是你*想表达*的意思吗？

### 任务 3 —— 带注释的模式
用 `re.compile(..., re.VERBOSE)` 重写邮箱校验器，每个符号一行注释。行为必须
完全一致。

### 任务 4 —— 匿名化器
用 `re.sub` 传**函数**替换，把转录文本里出现的 Ana/Ben/Cara 全部替换成稳定编号
`P001`、`P002`……（同名 → 同编号）。

### 任务 5 —— 双格式日期收割
从 `"submitted 2026-07-06, revised 07/08/2026, due 2026-09-01"` 里用一次
`findall` + 一个候选分支，提取**全部**日期（`YYYY-MM-DD` 或 `MM/DD/YYYY` 两种
格式）。

### 任务 6 —— 忽略大小写的关键词计数
用标志位统计一段话里 "stress" 的出现次数、大小写不限——不许先把文本转小写。

## 课后作业（第 10 课之前）

*约 30–45 分钟，课外完成——不计入课堂时间。先都试一遍，再看答案。*

### 任务 1 —— 模式练习
各写一个 `re.fullmatch` 模式；每个用两个合法、两个非法的字符串测试：
1. 学号：两个大写字母 + 六位数字（`AB123456`）
2. 美式电话：`555-867-5309`（只有数字和连字符）
3. ISO 日期：`2026-07-06`（只验形状——不用检查月份范围）

### 任务 2 —— 脏姓名清洗
把 `["  smith,  ana", "LEE,BEN", "Garcia ,  Cara "]` 规范成 `"Ana Smith"`、
`"Ben Lee"`、`"Cara Garcia"`：按逗号（两侧可有空格）做正则切分，然后
`.strip()` + `.title()`，再交换顺序。

### 任务 3 —— 域名收割
从含有多个邮箱地址的一段文字里，用一次 `findall` + 一个 `set` 提取**不重复的**
域名（如 `{"university.edu", "gmail.com"}`）。

---

## 参考答案

### 课堂练习

见本文件夹的 `demo.py`——六个任务的完整实现。关键行：

```python
re.fullmatch(r"\w+@\w+\.edu", addr) is not None      # 1（fullmatch 锁住两端）
m = re.search(r"([A-Z]{2})(\d{4})", s); m.group(1), m.group(2)   # 2
re.sub(r"\s+", " ", messy).strip()                   # 3
from collections import Counter; Counter(re.findall(r"#(\w+)", text))   # 4
m = re.search(r"^(.+),\s*(.+)$", s); f"{m.group(2)} {m.group(1)}"      # 5
```
任务 6：按逗号切 `"a,b,c"` 就是 `"a,b,c".split(",")` —— 不需要正则。
只有模式真正*可变*（数字、可选部分、锚点）时才请出正则。

陷阱提醒：`.` 匹配**任意**字符——真正的点用 `\.`；永远别忘 `r"..."` 前缀，
否则反斜杠会变成 Python 的转义序列。

### 课堂练习——更进一步

```python
# 任务 1
import re
m = re.search(r"(?P<dept>[A-Z]{2})(?P<num>\d{4})", "Course ED1234 meets Tue")
print(m.group("dept"), m.group("num"))   # ED 1234
print(m.groupdict())                     # {'dept': 'ED', 'num': '1234'}
```

任务 2 —— 重点是习惯：regex101 的解释器能在你的数据咬你之前，先抓住
"`.` 匹配任意字符"这类失误。

```python
import re

# 任务 3
EMAIL = re.compile(r"""
    \w+          # 用户名部分
    @
    \w+          # 域名
    \.edu        # 一个真正的点，然后是 edu
""", re.VERBOSE)
print(EMAIL.fullmatch("ana@university.edu") is not None)   # True

# 任务 4
ids = {}
def anonymize(m):
    name = m.group(0)
    ids.setdefault(name, f"P{len(ids) + 1:03d}")
    return ids[name]

text = "Ana said X. Ben said Y. Ana agreed."
print(re.sub(r"\b(?:Ana|Ben|Cara)\b", anonymize, text))
# P001 said X. P002 said Y. P001 agreed.

# 任务 5
s = "submitted 2026-07-06, revised 07/08/2026, due 2026-09-01"
print(re.findall(r"\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}", s))
# ['2026-07-06', '07/08/2026', '2026-09-01']

# 任务 6
para = "Stress was high. Some stress is normal. STRESS!"
print(len(re.findall(r"stress", para, re.IGNORECASE)))     # 3
```

### 课后作业

```python
# 任务 1
import re

sid   = r"[A-Z]{2}\d{6}"        # AB123456 ✓  CD000001 ✓  ab123456 ✗  AB12345 ✗
phone = r"\d{3}-\d{3}-\d{4}"    # 555-867-5309 ✓  555-8675309 ✗
date  = r"\d{4}-\d{2}-\d{2}"    # 2026-07-06 ✓  2026-7-6 ✗

for s in ["AB123456", "ab123456"]:
    print(s, re.fullmatch(sid, s) is not None)

# 任务 2
def clean_name(raw):
    last, first = re.split(r"\s*,\s*", raw.strip(), maxsplit=1)
    return f"{first.strip().title()} {last.strip().title()}"

for raw in ["  smith,  ana", "LEE,BEN", "Garcia ,  Cara "]:
    print(clean_name(raw))      # Ana Smith · Ben Lee · Cara Garcia

# 任务 3
text = "Write ana@university.edu or ben@gmail.com; cc cara@university.edu today."
print(set(re.findall(r"\w+@([\w.]+\.\w+)", text)))
# {'university.edu', 'gmail.com'}  —— 集合顺手去了重
```
