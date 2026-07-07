---
marp: true
title: "第 6 课 — 递归与递归思维"
paginate: true
---

# 第 6 课
## 递归与递归思维

---

## 每个递归的模样

真实例子：一门课的先修链有多深？

```python
prereq_of = {"ED700": "ED600", "ED600": "ED500",
             "ED500": "ED400", "ED400": None}   # ED400 没有先修课

def prereqs_deep(course):
    earlier = prereq_of[course]
    if earlier is None:               # 基例 —— 到此停下
        return 0
    return 1 + prereqs_deep(earlier)  # 递归步 —— 往回退一门
```

永远是两部分：
- 一个**基例（base case）**负责停下，
- 一个**递归步（recursive case）**朝基例*靠近*。

---

## 追踪调用栈

`orderings(n)` = 给 *n* 名学生排名的方式数 = n!

```python
orderings(3)
= 3 * orderings(2)
=     3 * (2 * orderings(1))
=         3 * (2 * 1)          # 基例返回 1
= 6
```

每次调用都在等待它内部的那次调用。调用层层堆起，再层层返回。

🧠 每个未完成的调用是一个**栈帧**——马上就会用到这个概念。

---

## 递归 vs 迭代

```python
def orderings(n):                 # n 名学生的排名方式数（n!）
    if n <= 1:
        return 1
    return n * orderings(n - 1)   # ← 必须 RETURN 这次调用

def orderings_loop(n):
    total = 1
    for k in range(2, n + 1):
        total *= k
    return total
```

答案相同。对平铺的计数问题，**循环**通常更清晰。

---

## 递归的主场：嵌套数据

```python
def deep_sum(obj):
    if isinstance(obj, (int, float)):
        return obj
    if isinstance(obj, dict):
        return sum(deep_sum(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return sum(deep_sum(x) for x in obj)
    return 0

deep_sum([1, [2, [3, 4]], {"a": 6}])   # 16
```

嵌套 JSON、文件夹树、盖楼式回复——单层循环够不到底，递归可以。

---

## 陷阱：没有基例

```python
def runaway(n):
    return runaway(n + 1)     # 永不停止
```

```
RecursionError: maximum recursion depth exceeded
```

Python **没有尾调用优化**——每次调用都保留栈帧
（默认上限 ≈ 1000）。太深的递归*一定*会撞到天花板。

---

## 轮到你了

`examples/session-06/practice.md`：
1. 递归版 `total(scores)`——先大声说出基例是什么。
2. `flatten([1, [2, [3, 4]], 5])` → 一个平铺列表。
3. `depth(...)`——列表嵌套有多深？

---

# 更进一步
## 荒野中的递归

---

## 记忆化：记住算过的调用

```python
def fib(n):                       # 朴素版：fib(35) 会把 fib(5) 重算几千次
    return n if n < 2 else fib(n - 1) + fib(n - 2)

import functools
@functools.cache                  # 记住每一对（输入 -> 输出）
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

朴素版 `fib(35)`：数秒。加缓存：瞬间。代码没变——是装饰器（第 5 课！）干的活。
当递归会重复解**同一个子问题**时，缓存它。

---

## 分而治之：二分查找

```python
def find(sorted_names, target, lo=0, hi=None):
    if hi is None:
        hi = len(sorted_names)
    if lo >= hi:
        return False                   # 基例：区间空了
    mid = (lo + hi) // 2
    if sorted_names[mid] == target:
        return True
    if sorted_names[mid] < target:
        return find(sorted_names, target, mid + 1, hi)
    return find(sorted_names, target, lo, mid)
```

每次调用把问题**减半**：1 000 个名字 ≈ 10 步，一百万 ≈ 20 步。
（前提是数据有序——第 4 课的 `sorted` 派上用场。）

---

## 树形数据

```python
org = {"name": "Dean",
       "reports": [{"name": "Chair A", "reports": []},
                   {"name": "Chair B",
                    "reports": [{"name": "Prof C", "reports": []}]}]}

def count_people(node):
    return 1 + sum(count_people(r) for r in node["reports"])

count_people(org)      # 4
```

组织架构图、文件夹树、盖楼回复、层级编码——函数的形状**照着数据的形状长**。
诀窍全在这里。

---

## 逃出上限：显式栈

```python
def flatten_iter(xs):
    out, to_visit = [], list(xs)
    while to_visit:
        x = to_visit.pop(0)
        if isinstance(x, list):
            to_visit = x + to_visit    # 原地拆箱
        else:
            out.append(x)
    return out
```

逻辑相同，**没有调用栈帧**——嵌套一万层也没问题。数据可能深过
约 1000 层时，自备一个待访问列表。

---

## 怎么选：循环、递归，还是缓存？

| 场景 | 选它 |
|---|---|
| 平铺序列 | 普通**循环** |
| 自相似 / 嵌套数据 | **递归** |
| 重复的子问题 | 递归 + **`@cache`** |
| 可能非常深 | 循环 + **显式栈** |

递归是工具，不是美德——按*数据的形状*来挑。

---

## 轮到你了——第二轮

`examples/session-06/practice.md` → **In class — going deeper**：
带步数统计的二分查找、组织树计数，以及不用递归的 `flatten`。

---

## 陷阱回顾

- 每个递归都需要**可达的基例**，否则栈会溢出。
- 要 **return** 递归调用——忘了就得到悄无声息的 `None`。
- 递归不免费：每次调用占一个栈帧（没有尾调用优化）。
- 平铺序列和超深任务，用普通**循环**更好。

## 小结
你已经能解决"以自身定义"的问题——尤其是嵌套数据。
**下一课：** 第 7 课——异常与防御式编程。

---

## 课后作业（第 7 课之前）

*课外完成——不计入课堂时间。完整题目 + 参考答案：`examples/session-06/practice.md` → **Homework**。*

1. **`sum_digits(n)`** —— 对数字而不是列表做递归。
2. **`deep_count(obj)`** —— 数一数嵌套成绩册里的所有分数。
3. **用自己的话** —— 一段话：什么时候循环是更好的工具？
