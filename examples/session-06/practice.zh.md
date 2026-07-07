# 第 6 课 —— 练习：递归与递归思维

每个答案都自己敲一遍。**运行之前先预测输出。** 参考答案在最后。

## 课堂练习

### 任务 1 —— 递归求和
**用递归**（不用循环）写 `total(scores)` 对分数列表求和：
`scores[0] + total(rest)`，以空列表为基例。先大声说出基例是什么。
测试 `total([91, 58, 73])` 和 `total([])`。

### 任务 2 —— 递归 vs 迭代
写递归版 `reverse(s)` 反转字符串，再写循环版。你觉得哪个更好读？
测试 `reverse("data")`。

### 任务 3 —— 摊平嵌套数据
写 `flatten(xs)`，把任意深度的列表套列表变成一个平铺列表：
`flatten([1, [2, [3, 4]], 5])` → `[1, 2, 3, 4, 5]`。处理嵌套 JSON/导出数据就靠这招。

### 任务 4 —— 嵌套有多深？
写 `depth(xs)`，返回列表的嵌套深度：
`depth([1, [2, [3, [4]]]])` → `4`，`depth([1, 2, 3])` → `1`，`depth(5)` → `0`。

### 任务 5 —— 陷阱检查
1. 这段为什么抛 `RecursionError`？怎么修？
   ```python
   def f(n):
       return n + f(n - 1)
   ```
2. 这段返回 `None` 而不是数字——为什么？
   ```python
   def orderings(n):
       if n <= 1:
           return 1
       n * orderings(n - 1)
   ```
3. 举一个普通循环比递归更合适的场景。

### 加餐 —— Python 惯用法速练
一个装饰器就能让指数级的递归瞬间完成——靠记住算过的调用。

```python
import functools

@functools.cache                     # 记忆化：每个 n 只算一次
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
print(fib(35))                       # -> 9227465   （去掉 @cache 再试试……慢慢等吧）
```

## 课堂练习——更进一步（第二小时）

### 任务 1 —— 递归倒计时
`countdown(3)` 打印 `3 2 1 Go!`。动手之前先说出基例。

### 任务 2 —— 纸上追踪
像幻灯片追踪 `orderings(3)` 那样，写出 `total([5, 10, 20])`（任务 1）的完整
展开——每一次挂起的调用，然后逐层返回。

### 任务 3 —— 数步数的二分查找
写递归版 `find(sorted_names, target)`，顺便统计它看了几个名字。在 7 个名字的
有序列表里查找，然后想象 1000 个——大约要几步？为什么？

### 任务 4 —— 数组织树
`org = {"name": ..., "reports": [...]}` 任意嵌套。写 `count_people(node)`；
再写 `deepest(node)`，返回这棵树有几层。

### 任务 5 —— 不用递归摊平
用显式的待访问列表（不写递归调用）重写 `flatten`。在 `[1, [2, [3, 4]], 5]` 上
验证与递归版一致——并解释为什么它能扛住一万层的深度。

## 课后作业（第 7 课之前）

*约 30–45 分钟，课外完成——不计入课堂时间。先都试一遍，再看答案。*

### 任务 1 —— `sum_digits(n)`
`sum_digits(4823)` → `17`，用递归。（提示：`n % 10` 是最后一位，`n // 10` 是
其余部分。哪个最小的数的数字和一眼便知？）

### 任务 2 —— `deep_count(obj)`
数嵌套结构里出现了多少个**数字**（int/float——但 bool 不算！）。处理字典、
列表/元组和标量。
`deep_count({"quiz": [90, 85], "final": {"written": 88, "oral": 92}, "note": "great"})` → `4`。

### 任务 3 —— 用自己的话
一段话：哪种形状的问题更适合普通循环？深度到 1000 左右时递归*具体*会出什么
问题？（说出错误名。）

---

## 参考答案

### 课堂练习

```python
# 1
def total(scores):
    if not scores:                  # 基例：空列表的和是 0
        return 0
    return scores[0] + total(scores[1:])   # 第一个分数 + 其余的和
print(total([91, 58, 73]), total([]))      # 222 0

# 2
def reverse(s):
    if s == "":                     # 基例：空字符串
        return ""
    return reverse(s[1:]) + s[0]    # 去头反转，再接上头
print(reverse("data"))             # "atad"
# 循环版："".join(reversed(s)) —— 平铺字符串通常这样更清楚

# 3
def flatten(xs):
    out = []
    for x in xs:
        if isinstance(x, list):
            out.extend(flatten(x))  # 递归进子列表
        else:
            out.append(x)
    return out
print(flatten([1, [2, [3, 4]], 5]))   # [1, 2, 3, 4, 5]

# 4
def depth(xs):
    if not isinstance(xs, list):
        return 0                              # 非列表没有嵌套
    return 1 + max((depth(x) for x in xs), default=0)
print(depth([1, [2, [3, [4]]]]), depth([1, 2, 3]), depth(5))   # 4 1 0

# 5
# 1) 没有可达的基例 -> 调用永不停止 -> 栈溢出。
#    修法：在开头加 `if n == 0: return 0`（或 n <= 0）。
# 2) 递归步算了 n*orderings(n-1) 却没有 RETURN，
#    函数走到结尾返回 None。加上 `return`。
# 3) 平铺序列的简单处理循环更好；或者深度可能超过 ~1000 时
#    （Python 没有尾调用优化，深递归会 RecursionError，循环则没事）。
```

### 课堂练习——更进一步

```python
# 任务 1
def countdown(n):
    if n == 0:            # 基例
        print("Go!")
        return
    print(n)
    countdown(n - 1)      # 递归步，朝 0 走

# 任务 2 —— 追踪
# total([5, 10, 20])
# = 5 + total([10, 20])
# =     10 + total([20])
# =          20 + total([])
# =               0            <- 基例
# 回程：20 + 0 = 20 ; 10 + 20 = 30 ; 5 + 30 = 35

# 任务 3
def find(names, t, lo=0, hi=None, steps=1):
    if hi is None:
        hi = len(names)
    if lo >= hi:
        return False, steps
    mid = (lo + hi) // 2
    if names[mid] == t:
        return True, steps
    if names[mid] < t:
        return find(names, t, mid + 1, hi, steps + 1)
    return find(names, t, lo, mid, steps + 1)

roster = sorted(["Ana", "Ben", "Cara", "Dev", "Eve", "Fay", "Gus"])
print(find(roster, "Fay"))     # (True, 2-3 步)
# 1000 个名字 -> 约 10 步：每步把范围减半（2**10 = 1024）。

# 任务 4
def count_people(node):
    return 1 + sum(count_people(r) for r in node["reports"])

def deepest(node):
    if not node["reports"]:
        return 1
    return 1 + max(deepest(r) for r in node["reports"])

# 任务 5
def flatten_iter(xs):
    out, to_visit = [], list(xs)
    while to_visit:
        x = to_visit.pop(0)
        if isinstance(x, list):
            to_visit = x + to_visit
        else:
            out.append(x)
    return out

print(flatten_iter([1, [2, [3, 4]], 5]))   # [1, 2, 3, 4, 5]
# 没有递归调用 -> 没有栈帧 -> ~1000 帧的上限根本不适用。
```

### 课后作业

```python
# 任务 1
def sum_digits(n):
    if n < 10:                       # 一位数：数字和就是它自己
        return n
    return n % 10 + sum_digits(n // 10)

print(sum_digits(4823))              # 17

# 任务 2
def deep_count(obj):
    if isinstance(obj, bool):        # bool ⊂ int —— 开关标志不算数字（第 2 课！）
        return 0
    if isinstance(obj, (int, float)):
        return 1
    if isinstance(obj, dict):
        return sum(deep_count(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return sum(deep_count(x) for x in obj)
    return 0

print(deep_count({"quiz": [90, 85], "final": {"written": 88, "oral": 92},
                  "note": "great"}))   # 4
```

任务 3 —— 参考回答：平铺序列（列表求和、逐行处理）用循环最清楚。每个挂起的递归调用
都占一个栈帧，而 Python 没有尾调用优化，所以到约 1000 帧就抛 `RecursionError`——
循环则可以一直跑。递归的价值在于*数据本身*是嵌套/自相似的时候。
