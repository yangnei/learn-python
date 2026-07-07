---
marp: true
title: "第 9 课 — 正则表达式与文本清洗"
paginate: true
---

# 第 9 课
## 正则表达式与文本清洗

---

## 研究者为什么要在乎

- 在 ID、邮箱、日期污染数据之前先做校验。
- 从自由文本里提取结构化的片段（编码、姓名、数字）。
- 清洗、规范开放式问卷回答。
- **定性编码**的第一遍粗筛（找出匹配某模式的所有回答）。

🧠 像在语料库里做检索过滤——但它匹配的是*形式*，不是含义。

---

## 永远用原始字符串

```python
import re
re.search(r"\d+", "id 42")     # r"..." = 原始字符串
```

不带 `r"..."`，Python 会吃掉反斜杠（`\d` → 报错/乱码）。
**规则：** 每个正则模式都写成原始字符串。

---

## 保命符号表

| 符号 | 匹配 |
|---|---|
| `.` | **任意**字符（换行除外） |
| `\d \w \s` | 数字 / 单词字符 / 空白 |
| `\D \W \S` | 以上的取反 |
| `+ * ?` | 1+、0+、0 或 1 |
| `{m}` `{m,n}` | 恰好 m 次 / m 到 n 次 |
| `^ $` | 字符串开头 / 结尾 |
| `[abc]` `[a-z]` `[^abc]` | 集合内 / 范围内 / 集合外 |
| `(...)` | 捕获组 |
| `a\|b` | a 或 b |

---

## `.` 的陷阱

```python
re.search(r".", "a.b").group()    # 'a'  —— 任意字符，不是点！
re.search(r"\.", "a.b").group()   # '.'  —— 想要真正的点就转义
```

想按字面意思用特殊字符时要转义：`\. \^ \$ \* \+ \? \( \) \[ \] \{ \} \|`

---

## 你需要的四个函数

```python
re.search(pattern, s)     # 任意位置的第一个匹配 -> 匹配对象或 None
re.fullmatch(pattern, s)  # 整个字符串必须匹配 -> 校验用
re.findall(pattern, s)    # 所有匹配的列表
re.sub(pattern, repl, s)  # 替换匹配 -> 清洗用
```

大小写不敏感用 `re.IGNORECASE`：`re.search(p, s, re.IGNORECASE)`。

---

## 校验（fullmatch 锁住两端）

```python
def valid_university_email(addr):
    return re.fullmatch(r"\w+@\w+\.edu", addr) is not None

valid_university_email("ana@university.edu")   # True
valid_university_email("ana@gmail.com")        # False
valid_university_email("ana@@x.edu")           # False
```

---

## 用捕获组提取

```python
m = re.search(r"([A-Z]{2})(\d{4})", "Course ED1234 meets Tue")
m.group(0)   # "ED1234"  完整匹配
m.group(1)   # "ED"      系别
m.group(2)   # "1234"    课号
```

`m.groups()` 一次交出所有捕获：`('ED', '1234')`。
没匹配到时 `m` 是 `None`——调 `.group()` 之前先检查。

---

## 清洗与挖掘自由文本

```python
re.sub(r"\s+", " ", messy).strip()        # 折叠空白
re.findall(r"#(\w+)", "love #python #stats")   # ['python', 'stats']

from collections import Counter
Counter(re.findall(r"#(\w+)", corpus))    # 主题词频
```

用分组重排：`re.sub(r"^(.+),\s*(.+)$", r"\2 \1", "Curie, Marie")` → `"Marie Curie"`。

---

## 什么时候不该用正则

```python
"a,b,c".split(",")     # 简单切分 —— 不需要正则
"  hi  ".strip()       # 去空白 —— 不需要正则
text.replace("X", "Y") # 固定子串 —— 不需要正则
url.removeprefix("https://")   # 去掉已知前缀 —— 不需要正则（3.9+）
```

正则擅长*可变*的模式。固定字符串用普通方法更好读。

---

## 轮到你了

`examples/session-09/practice.md`：
1. 邮箱校验器。2. 提取系别+课号。3. 折叠空白。
4. 统计各回答中的 #话题标签。5. 翻转 `"Last, First"`。6. 一个该用 `.split()` 的场景。

---

# 更进一步
## 正则的火力升级

---

## 标志位

```python
re.findall(r"stress", corpus, re.IGNORECASE)   # Stress、STRESS、stress
re.findall(r"^\d+", text, re.MULTILINE)        # ^ 和 $ 按行匹配
re.search(p, s, re.IGNORECASE | re.MULTILINE)  # 用 | 组合
re.search(r"a.b", text, re.DOTALL)             # . 也能跨过换行
```

---

## `re.compile`——给模式起名字

```python
EMAIL = re.compile(r"\w+@\w+\.edu")
COURSE = re.compile(r"[A-Z]{2}\d{4}")

EMAIL.fullmatch(addr)        # 同样四个函数，现在是方法
COURSE.findall(text)
```

编译一次，处处复用——模式有了一个读者可以信任的*名字*。

---

## 可读的模式：`re.VERBOSE`

```python
EMAIL = re.compile(r"""
    \w+          # 用户名部分
    @
    \w+          # 域名
    \.edu        # 一个真正的点，然后是 edu
""", re.VERBOSE)
```

空白被忽略、允许注释——未来的自己也能审阅的正则。

---

## 分组，进阶版

```python
m = re.search(r"(?P<dept>[A-Z]{2})(?P<num>\d{4})", "ED1234")
m.group("dept"), m.groupdict()     # 名字胜过序号

r"(?:Prof|Dr)\.?\s+(\w+)"        # (?:...) 只分组、不捕获
```

要提取的组起个名字；只为分组的括号用 `(?:...)`。

---

## 贪婪 vs 惰性

```python
re.search(r"\[(.+)\]",  "[ED101][ED102]").group(1)   # 'ED101][ED102'  😱
re.search(r"\[(.+?)\]", "[ED101][ED102]").group(1)   # 'ED101'
```

`+` 和 `*` 能吞多少吞多少；`+?` / `*?` 能少吞就少吞。
括号里的、引号里的内容，几乎总是想要**惰性**。

---

## `re.sub` 传入函数：匿名化器

```python
ids = {}
def anonymize(m):
    name = m.group(0)
    ids.setdefault(name, f"P{len(ids) + 1:03d}")
    return ids[name]

re.sub(r"\b(?:Ana|Ben|Cara)\b", anonymize, transcript)
# "P001 said ... P002 replied ... P001 agreed"
```

替换内容需要*计算*时，传一个函数——每个匹配都会经过它。
（对 `ids` 的闭包——第 5 课的回报。）

---

## 正则遇上文件

```python
text = Path("responses.txt").read_text(encoding="utf-8")
emails = sorted(set(EMAIL.findall(text)))
```

第 8 课 + 第 9 课，两行搞定：读文件、挖模式、用集合去重。

---

## 轮到你了——第二轮

`examples/session-09/practice.md` → **In class — going deeper**：
带注释的 `VERBOSE` 邮箱模式、匿名化器，以及双格式日期收割。

---

## 陷阱回顾

- `.` 匹配**任意**字符——真正的点用 `\.`。
- 忘写 `r"..."` 会毁掉你的反斜杠。
- `re.search` 没匹配到返回 `None`——先判断再 `.group()`。
- 字符串方法更清晰的地方，别上正则。

## 小结
你已经能校验、提取和清洗真实世界的文本。
**下一课：** 第 10 课——模块、面向对象与 Python 惯用法。

---

## 课后作业（第 10 课之前）

*课外完成——不计入课堂时间。完整题目 + 参考答案：`examples/session-09/practice.md` → **Homework**。*

1. **模式练习** —— 学号、美式电话、ISO 日期：各写一个 `fullmatch` 模式。
2. **脏姓名清洗** —— 用 `re.sub` 规范一列爬来的姓名。
3. **域名收割** —— 从一段文字里提取所有邮箱域名。
