# Python 语法速查 —— 那些总记不住的写法

> "那个来着怎么写？"专用表。按课程分组。

## 输入输出与类型  *(第 1 课)*
```python
name = input("Name: ")          # 永远返回 str
age  = int(input("Age: "))      # 立即转换
print("Hi", name, age)          # 空格分隔
print(f"Hi {name}, age {age}")  # f-string（首选）
print(f"{score:.2f}")           # 两位小数
print(f"{count:,}")             # 千位分隔符：1,234
print("no newline", end="")     # 去掉行尾的 \n
int("42"), float("3.14"), str(42), bool(0)   # 类型转换
type(x)                          # x 是什么类型？
```

## f-string 格式化小抄
| 写法 | 示例 | 输出 |
|---|---|---|
| `:.2f` | `f"{3.14159:.2f}"` | `3.14` |
| `:,` | `f"{1234567:,}"` | `1,234,567` |
| `:>8` | `f"{'hi':>8}"` | `      hi`（右对齐） |
| `:<8` | `f"{'hi':<8}"` | `hi      `（左对齐） |
| `:^8` | `f"{'hi':^8}"` | `   hi   `（居中） |
| `:.1%` | `f"{0.873:.1%}"` | `87.3%` |

## 条件  *(第 3 课)*
```python
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "F"

90 <= score <= 100              # 链式比较
grade = "pass" if score >= 60 else "fail"   # 三元表达式

match command:                   # Python 3.10+
    case "start": ...
    case "stop" | "halt": ...    # 多个值
    case _: ...                  # 默认分支
```

## 循环  *(第 3 课)*
```python
for i in range(5): ...                  # 0..4
for x in items: ...                     # 每个元素
for i, x in enumerate(items): ...       # 序号 + 元素
for a, b in zip(names, scores): ...     # 两个列表并排走
while condition: ...
while True:                             # 输入校验循环
    x = input("...")
    if valid(x):
        break
# break / continue 控制流程
```

## 序列与切片  *(第 4 课)*
```python
xs = [1, 2, 3]; xs.append(4); xs[0]; xs[-1]   # 最后一个
xs[1:3]      # [2, 3]   （含起点，不含终点）
xs[:2]       # 前两个
xs[::-1]     # 反转
t = (1, 2)                       # 元组（不可变）
d = {"name": "Ana", "gpa": 3.9}  # 字典
d["name"]; d.get("missing", 0)   # 访问；带默认值的安全访问
d.keys(); d.values(); d.items()
s = {1, 2, 2, 3}                 # 集合 -> {1, 2, 3}（去重）
```

## 推导式  *(第 4/10 课)*
```python
[x*2 for x in xs]                       # 列表
[x for x in xs if x > 0]                # 带过滤
{name: 0 for name in names}             # 字典
{x % 3 for x in xs}                     # 集合
(x*x for x in xs)                       # 生成器（惰性）
```

## 排序  *(第 4 课)*
```python
sorted(xs)                              # 新的有序列表
sorted(xs, reverse=True)
sorted(students, key=lambda s: s["gpa"])          # 按字段
sorted(students, key=lambda s: s["gpa"], reverse=True)
xs.sort()                               # 就地排序（返回 None！）
```

## 函数  *(第 5 课)*
```python
def avg(nums: list[float]) -> float:
    """Return the mean of nums."""      # 文档字符串
    return sum(nums) / len(nums)

def greet(name, greeting="Hello"): ...  # 默认参数（不许用可变对象！）
def total(*args): ...                   # 任意个位置参数 -> 元组
def config(**kwargs): ...               # 任意个关键字参数 -> 字典
func(*my_list)                          # 列表摊开成参数
func(**my_dict)                         # 字典摊开成关键字参数
```

## 异常  *(第 7 课)*
```python
try:
    n = int(value)
except ValueError:
    n = None
except (KeyError, IndexError) as e:
    print(e)
else:
    print("ok")          # 只在没有异常时运行
finally:
    print("always")      # 收尾，总会运行

raise ValueError("score must be 1–5")
assert n > 0, "n must be positive"
```

## 文件与 CSV  *(第 8 课)*
```python
with open("f.txt") as f:          # 读取，自动关闭
    text = f.read()
with open("f.txt", "w") as f:     # 写入（会覆盖！）
    f.write("line\n")

import csv
with open("data.csv", newline="") as f:
    for row in csv.DictReader(f):    # row 是以表头为键的字典
        print(row["name"])

with open("out.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["name", "gpa"])
    w.writeheader()
    w.writerow({"name": "Ana", "gpa": 3.9})
```

## 顺手的标准库  *(第 8 课)*
```python
import statistics; statistics.mean(xs); statistics.median(xs); statistics.stdev(xs)
import random; random.choice(xs); random.randint(1, 6); random.shuffle(xs)
from datetime import date; date.today(); date(2026, 6, 26)
from pathlib import Path; Path("data.csv").exists()
import json; json.dumps(obj, indent=2); json.loads(text)
```

## 正则  *(第 9 课)*
```python
import re
re.search(r"pattern", text)      # 任意位置的第一个匹配（或 None）
re.fullmatch(r"\d{5}", zip)      # 整个字符串必须匹配
re.sub(r"\s+", " ", text)        # 折叠空白
m = re.search(r"(\w+)@(\w+)", s)
m.group(1)                        # 第一个捕获组
```
| 符号 | 含义 |
|---|---|
| `.` | 任意字符（换行除外） |
| `\d \w \s` | 数字 / 单词字符 / 空白 |
| `+ * ?` | 1+、0+、0 或 1 |
| `{m,n}` | m 到 n 次 |
| `^ $` | 开头 / 结尾 |
| `[...] [^...]` | 集合内 / 集合外 |
| `(...)` | 捕获组 |
| `a\|b` | a 或 b |

## 类  *(第 10 课)*
```python
class Student:
    def __init__(self, name, gpa):
        self.name = name
        self._gpa = gpa
    def __str__(self):
        return f"{self.name} ({self._gpa})"
    @property
    def gpa(self):
        return self._gpa
    @gpa.setter
    def gpa(self, value):
        if not 0 <= value <= 4:
            raise ValueError("gpa out of range")
        self._gpa = value

s = Student("Ana", 3.9)
print(s)            # 使用 __str__
```

## 程序骨架  *(每个脚本)*
```python
def main():
    ...

def helper():
    ...

if __name__ == "__main__":
    main()
```
