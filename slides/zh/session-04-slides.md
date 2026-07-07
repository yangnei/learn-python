---
marp: true
title: "第 4 课 — 数据结构"
paginate: true
---

# 第 4 课
## 数据结构

---

## 四种容器，四种职责

| 类型 | 语法 | 可变？ | 用途 |
|---|---|---|---|
| `list` | `[1, 2, 3]` | 是 | 有序、会变化的集合 |
| `tuple` | `(1, 2)` | 否 | 固定记录 / 坐标 |
| `dict` | `{"k": v}` | 是 | 键 → 值查找 |
| `set` | `{1, 2, 3}` | 是 | 去重后的唯一元素 |

---

## 列表与切片

```python
xs = [10, 20, 30, 40]
xs[0]      # 10     xs[-1]   # 40（最后一个）
xs[1:3]    # [20, 30]   （不含终点）
xs[:2]     # [10, 20]
xs[::-1]   # 反转
xs.append(50); xs.sort()      # 就地修改
```

⚠️ `xs.sort()` 返回 **None**——它就地排序。想要新列表用 `sorted(xs)`。

---

## 字典 = 带标签的记录

```python
student = {"name": "Ana", "gpa": 3.9}
student["name"]              # "Ana"
student.get("major", "N/A")  # 带默认值的安全访问
student["major"] = "Ed"      # 新增/更新
for key, val in student.items(): ...
```

---

## 字典列表 = 一个数据集 🧠

```python
roster = [
    {"name": "Ana", "score": 91},
    {"name": "Ben", "score": 58},
]
```

每个字典 = 一**行/一名受访者**；每个键 = 一个**变量/一列**。
在 pandas 登场（第 8 课）之前，这就是你的整洁数据集。

---

## 集合：唯一元素、快速成员判断

```python
answers = ["yes", "no", "yes", "maybe", "no"]
set(answers)            # {'yes', 'no', 'maybe'}  —— 去重
"yes" in set(answers)   # True，而且非常快
```

适合"不重复的回答有哪些"和"这个 ID 出现过吗？"

---

## 推导式

```python
[s["score"] for s in roster]                 # 列表
[s for s in roster if s["score"] >= 60]      # 带过滤
{s["name"]: s["score"] for s in roster}      # 字典
{s["score"] // 10 for s in roster}           # 分数段集合
```

读法：*表达式，对每个元素，（可选）如果满足条件。*

---

## 按键排序

```python
sorted(roster, key=lambda s: s["score"])               # 升序
sorted(roster, key=lambda s: s["score"], reverse=True) # 降序
```

`lambda s: s["score"]` = "按 score 字段排序"。

---

## 陷阱：别名（标签，不是盒子）

```python
a = [1, 2, 3]
b = a                # 同一个列表
a.append(4)
b                    # ？ 😱 ← 先预测（见下方陷阱区）

b = a.copy()         # ✅ 独立副本
```

`[[0]*3]*3` 造出的是同一行的 3 个引用——要用 `[[0]*3 for _ in range(3)]`。

---

## 轮到你了

`examples/session-04/practice.md`：
1. 构建名册（字典列表）；按分数排序。
2. 一行写出 `{name: score}` 字典推导式。
3. 把学生分进 pass/fail 两组。
4. 复现别名陷阱，然后修好它。

---

# 更进一步
## 容器工具箱

---

## 解包

```python
name, score = ("Ana", 91)        # 元组解包
head, *rest = [10, 20, 30, 40]   # head=10, rest=[20, 30, 40]
a, b = b, a                      # 交换，再看一眼
for name, score in zip(names, scores): ...   # zip 循环的本质就是解包
```

---

## 字典的强力方法

```python
student.get("major", "N/A")        # 带默认值的安全查找
student.pop("temp", None)          # 删除并返回（不存在则给默认值）
groups.setdefault("pass", []).append(name)   # 不存在就先创建，再使用
d1 | d2                            # 合并字典（右边优先，3.9+）
for key, val in student.items(): ...
```

---

## `collections.Counter`——一行搞定频数

```python
from collections import Counter
counts = Counter(["yes", "no", "yes", "maybe", "yes"])
counts                 # Counter({'yes': 3, 'no': 1, 'maybe': 1})
counts.most_common(1)  # [('yes', 3)]
```

🧠 你那整段"统计问卷答案"的循环，浓缩成一个表达式。它本质上就是个字典。

---

## `collections.defaultdict`——分组不费事

```python
from collections import defaultdict
by_major = defaultdict(list)          # 键不存在？先造一个 []
for s in roster:
    by_major[s["major"]].append(s["name"])
```

和 `setdefault` 干同样的活，规模大了更干净。

---

## 集合，完整工具箱

```python
fall & spring     # 交集：两学期都在
fall | spring     # 并集：任一学期在
fall - spring     # 差集：只在秋季
fall ^ spring     # 对称差：恰好只在一个学期
{1, 2} <= {1, 2, 3}   # 子集？True
list(dict.fromkeys(xs))   # 去重且保持顺序（set 做不到）
```

---

## 排序，进阶版

```python
sorted(roster, key=lambda s: (-s["score"], s["name"]))
# 分数从高到低，同分按姓名 A→Z
```

- 多键排序：让 `key` 返回一个**元组**——逐元素比较（第 2 课！）。
- Python 的排序是**稳定的**：键相同的元素保持原有顺序。

---

## `copy` vs `deepcopy`

```python
import copy
flat = a.copy()            # 新的外层列表 —— 内部对象仍然共享
full = copy.deepcopy(a)    # 一路复制到底
```

法则：有嵌套、还要改内层 → `deepcopy`。其余情况 `.copy()` 就够了。

---

## 轮到你了——第二轮

`examples/session-04/practice.md` → **In class — going deeper**：
用 `Counter` 和 `defaultdict` 重做、一次多键排序，以及保持顺序的去重。

---

## 陷阱回顾

- `=` 是别名；要复制用 `.copy()` / `copy.deepcopy()`。
- `.sort()` 返回 None（就地排）；`sorted()` 返回新列表。
- 内容相同，列表 ≠ 元组（第 2 课）。
- `dict.get(key, default)` 避免 `KeyError`。

## 小结
你已经能存储、查找、去重、排序和重塑数据。
**下一课：** 第 5 课——函数、作用域与复用。

---

## 课后作业（第 5 课之前）

*课外完成——不计入课堂时间。完整题目 + 参考答案：`examples/session-04/practice.md` → **Homework**。*

1. **成绩册字典操作** —— 增、改、安全查、删。
2. **频数统计器** —— 用普通字典统计问卷答案（不许 import）。
3. **修好网格** —— 复现 `[[0]*3]*3` 共享行 bug，再正确地重建。
