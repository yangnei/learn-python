# 第 4 课 —— 练习：数据结构

每个答案都自己敲一遍。**运行之前先预测输出。** 参考答案在最后。

## 课堂练习

从这里开始：
```python
roster = [
    {"name": "Ana", "score": 91}, {"name": "Ben", "score": 58},
    {"name": "Cara", "score": 73}, {"name": "Dev", "score": 64},
]
```

### 任务 1 —— 排名
按分数从高到低打印姓名。

### 任务 2 —— 映射（字典推导式）
一行构建 `{name: score}`。

### 任务 3 —— 分组
用循环构建 `{"pass": [...姓名...], "fail": [...姓名...]}`。

### 任务 4 —— 去重
从 `["A","B","A","C","B"]` 得到不重复的值和它们的个数。

### 任务 5 —— 别名
演示 `b = roster` 之后 `roster.append({...})` 也会改变 `b`。再把 `b` 变成独立
副本，让它不再跟着变。（提示：嵌套字典 → `copy.deepcopy`。）

### 加餐 —— Python 惯用法速练
盖住 `# ->` 后面的答案，逐行预测，再运行。

```python
head, *tail = [10, 20, 30, 40]
print(head, tail)                    # -> 10 [20, 30, 40]   （星号解包）
print({"a": 1} | {"b": 2})           # -> {'a': 1, 'b': 2}  （字典合并，3.9+）
print({1, 2, 3} & {2, 3, 4})         # -> {2, 3}            （集合交集）
print(list(zip(*[(1, 2), (3, 4)])))  # -> [(1, 3), (2, 4)]  （转置）
```

## 课堂练习——更进一步（第二小时）

### E1 —— 切片速练
对 `xs = list(range(10))`，预测：
`xs[2:5]` · `xs[-3:]` · `xs[:-3]` · `xs[::2]` · `xs[::-1]` · `xs[5:2:-1]`。

### E2 —— 两个学期
`fall = {"Ana", "Ben", "Cara"}`、`spring = {"Ben", "Dev"}` —— 谁两个学期都在？
任一学期在？只在秋季？（`&`、`|`、`-`）

### D1 —— 一行 `Counter`
用 `collections.Counter` 重做答案统计（`["yes", "no", "yes", "maybe", "yes", "no"]`），
并用 `.most_common(1)` 打印最高票答案。

### D2 —— 用 `defaultdict` 分组
用 `collections.defaultdict(list)` 把 `roster`（带 `major` 字段的字典列表）分组成
`{major: [names]}`。

### D3 —— 多键排序
把 `[("Ana", 91), ("Ben", 73), ("Cara", 91)]` 按分数**降序**、同分按姓名**升序**
排——一次 `sorted()` 调用、一个元组键。

### D4 —— 保序去重
从 `["B", "A", "B", "C", "A"]` 得到 `["B", "A", "C"]`（按首次出现的顺序）。
为什么普通的 `set()` 保证不了这一点？

## 课后作业（第 5 课之前）

*约 30–45 分钟，课外完成——不计入课堂时间。先都试一遍，再看答案。*

### H1 —— 成绩册字典操作
从 `gradebook = {"Ana": 91, "Ben": 58}` 开始。依次：加入 Cara（73）；Ben 重交作业
（58 → 68）；查询 Dev 但**不许**出 `KeyError`（默认 `"no record"`）；删除 Ben；
按分数从高到低打印 `name: score` 行。

### H2 —— 频数统计器
用普通字典和 `.get(k, 0)`（不许 import）把
`answers = ["yes", "no", "yes", "maybe", "yes", "no"]` 变成
`{"yes": 3, "no": 2, "maybe": 1}`。再用 `max(counts, key=counts.get)` 打印最高票。

### H3 —— 修好网格
用 `[[0]*3]*3` 建一个 3×3 全零网格，执行 `grid[0][0] = 9`，打印——亲眼看到 bug。
再用推导式重建并证明修好了。

---

## 参考答案

### 课堂练习

```python
# 1
print([s["name"] for s in sorted(roster, key=lambda s: s["score"], reverse=True)])
# ['Ana', 'Cara', 'Dev', 'Ben']

# 2
name_to_score = {s["name"]: s["score"] for s in roster}

# 3
groups = {"pass": [], "fail": []}
for s in roster:
    groups["pass" if s["score"] >= 60 else "fail"].append(s["name"])

# 4
vals = ["A","B","A","C","B"]
distinct = set(vals); print(distinct, len(distinct))   # {'A','B','C'} 3

# 5
import copy
b = roster                       # 别名
roster.append({"name": "Eve", "score": 80})
# b 里现在也有 Eve。要保持独立：
b = copy.deepcopy(roster)        # 之后 roster 的改动不再影响 b
```

### 课堂练习——更进一步

```python
# E1
xs = list(range(10))
xs[2:5]     # [2, 3, 4]          （不含终点）
xs[-3:]     # [7, 8, 9]          （最后三个）
xs[:-3]     # [0, 1, 2, 3, 4, 5, 6]
xs[::2]     # [0, 2, 4, 6, 8]    （隔一个取一个）
xs[::-1]    # 反转的副本
xs[5:2:-1]  # [5, 4, 3]          （倒着走，不含终点）

# E2
fall & spring   # {'Ben'}            —— 两学期都在
fall | spring   # 四个名字全部       —— 任一学期
fall - spring   # {'Ana', 'Cara'}    —— 只在秋季

# D1
from collections import Counter
counts = Counter(["yes", "no", "yes", "maybe", "yes", "no"])
print(counts, counts.most_common(1))   # Counter({'yes': 3, ...}) [('yes', 3)]

# D2
from collections import defaultdict
by_major = defaultdict(list)
for s in roster:
    by_major[s["major"]].append(s["name"])

# D3
pairs = [("Ana", 91), ("Ben", 73), ("Cara", 91)]
print(sorted(pairs, key=lambda p: (-p[1], p[0])))
# [('Ana', 91), ('Cara', 91), ('Ben', 73)] —— 负号翻转分数，姓名决胜负

# D4
xs = ["B", "A", "B", "C", "A"]
print(list(dict.fromkeys(xs)))   # ['B', 'A', 'C'] —— 字典记得插入顺序；
                                 # 集合没有可保的顺序
```

### 课后作业

```python
# H1
gradebook = {"Ana": 91, "Ben": 58}
gradebook["Cara"] = 73                       # 新增
gradebook["Ben"] = 68                        # 更新
print(gradebook.get("Dev", "no record"))     # 安全查询
del gradebook["Ben"]                         # 删除
for name, score in sorted(gradebook.items(), key=lambda kv: kv[1], reverse=True):
    print(f"{name}: {score}")                # Ana: 91 / Cara: 73

# H2
answers = ["yes", "no", "yes", "maybe", "yes", "no"]
counts = {}
for a in answers:
    counts[a] = counts.get(a, 0) + 1
print(counts)                       # {'yes': 3, 'no': 2, 'maybe': 1}
print(max(counts, key=counts.get))  # yes

# H3
grid = [[0] * 3] * 3
grid[0][0] = 9
print(grid)   # [[9,0,0],[9,0,0],[9,0,0]] —— 三个标签贴着同一行（别名！）

grid = [[0] * 3 for _ in range(3)]
grid[0][0] = 9
print(grid)   # [[9,0,0],[0,0,0],[0,0,0]] —— 各自独立的行
```
