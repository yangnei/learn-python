---
marp: true
title: "第 3 课 — 控制流：条件与循环"
paginate: true
---

# 第 3 课
## 控制流：条件与循环

---

## 第一部分——条件语句

```python
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "F"
```

缩进划定代码块。只有**第一个**为真的分支会执行。

---

## `if` 与 `elif`——不可互换

```python
# BUG：三个独立的 if —— 95 分会把三个标签全打出来
if score >= 60: print("passing")
if score >= 80: print("strong")
if score >= 90: print("excellent")
```

- 并排的 `if` 是**互相独立的问题**——条件重叠时会全部触发。
- `elif` 把它们变成**一个带分支的问题**：第一个命中即止，其余跳过。
- 只有当多个条件*确实*可以同时成立时，才用并排的 `if`。

---

## 比较运算 + 链式比较

`==`  `!=`  `<`  `<=`  `>`  `>=`

```python
0 <= score <= 100      # 链式 —— 读起来像数学
```

🧠 不必写 `score >= 0 and score <= 100`——链起来。

---

## 逻辑运算符（附一个坑）

```python
passed and submitted     # 两者都
late or excused          # 任一
not flagged              # 取反
```

**短路求值：** `a and b` 在 `a` 为假时直接跳过 `b`。
而且 `and`/`or` 返回的是**操作数，不是布尔值**：

```python
5 and 0        # ？ ← 先预测，再到下方陷阱区揭晓
"" or "N/A"    # 默认值惯用法
```

所以写 `if x:`——永远不要写 `if x == True`。

---

## 第二部分——循环

```python
for s in scores:          # 直接遍历每个元素
    print(s)

for i in range(5):        # 0,1,2,3,4
    print(i)

while not done:           # 条件翻转前一直重复
    ...
```

⚠️ `range(1, 5)` → `1,2,3,4` —— **不含终点**（差一错误！）。
`for _ in range(3):` —— `_` 是"只管重复、不用这个值"的约定写法。

---

## break / continue

```python
for x in data:
    if x is None:
        continue          # 跳过这一个
    if x == "STOP":
        break             # 彻底离开循环
    process(x)
```

---

## 别再摆弄下标：enumerate 与 zip

```python
for i, name in enumerate(names):       # 序号 + 值
    print(i, name)

for name, score in zip(names, scores): # 两个列表并排走
    print(name, score)
```

🧠 一旦写出 `range(len(x))`，停下——改用 `enumerate`/`zip`。

---

## 输入校验循环（以后到处都用得上）

```python
while True:
    raw = input("Score 0–100: ")
    if raw.isdigit() and 0 <= int(raw) <= 100:
        score = int(raw)
        break
    print("Try again.")
```

---

## 轮到你了

`examples/session-03/practice.md`：
1. 分数分档器——测试边界值（89.999 / 90 / 90.001）。
2. 计算全班平均分，并用 `zip` 给每人标注 PASS/FAIL。
3. 一个健壮的"问到对为止"循环。
4. 双重标签 bug——三个本该合成一架梯子的并排 `if`。

---

# 更进一步
## 更多控制流

---

## 三元表达式——一行版的小 `if`

```python
label = "pass" if score >= 60 else "fail"
print(f"{name}: {'✔' if attended else '✘'}")
```

只用于**微小**的选择。要读两遍才懂的，就写成真正的 `if`。

---

## 把判断本身返回出去

```python
def is_passing(score):        # 笨拙
    if score >= 60:
        return True
    return False

def is_passing(score):        # Pythonic —— 比较结果本来就是 bool
    return score >= 60
```

然后直接裸用：`if is_passing(s):`——永远不要写 `if is_passing(s) == True:`。
🧠 一切"是/否"辅助函数都一样：`is_valid`、`is_missing`、`is_full`——每个一行 `return`。

---

## `match/case`——更好读的梯子（3.10+）

```python
match answer:
    case 5 | 4:
        label = "agree"
    case 3:
        label = "neutral"
    case 1 | 2:
        label = "disagree"
    case _:                 # 默认分支
        label = "invalid"
```

当每个分支都在拿**同一个值**对比字面量时，`match` 比 `elif` 梯子好读。

---

## `for/else`——不用旗标变量的查找

```python
for s in scores:
    if s < 60:
        print("first failing score:", s)
        break
else:                      # 只在循环没有 break 时运行
    print("everyone passed")
```

这个 `else` 属于 `for`。不需要 `found = False` 那套记账。

---

## 嵌套循环

```python
for section in ["A", "B"]:
    for student in roster:
        print(section, student)
```

- 外层每走一步，内层完整跑一遍（2 × 4 = 8 行输出）。
- `break` 只跳出**内层**——想两层都跳，就把循环放进函数里 `return`。

---

## 给你正在写的模式起个名字

| 模式 | 骨架 |
|---|---|
| **累加器** | `total = 0` … `total += x` |
| **计数器** | `n = 0` … `n += 1` |
| **迄今最优** | `best = xs[0]` … `if x > best: best = x` |
| **哨兵** | `while True:` … `if raw == "done": break` |

认得这些模式，"对着空编辑器发呆"就变成了"挑一副骨架"。

---

## 轮到你了——第二轮

`examples/session-03/practice.md` → **In class — going deeper**：
`match/case` 重写、`for/else` 查找、不用 `max()` 的迄今最优，以及
"把判断返回出去"的重写。

---

## 陷阱回顾

- `if x == True` → 直接 `if x:`；判断 None 用 `x is None`（不是 `== None`）。
- 并排的 `if` 是独立问题——会全部触发；`elif` 才是一架梯子。
- `=`（赋值）vs `==`（比较）——经典手滑。
- `range(1, 5)` 不含 5；测试你的边界值。
- 不要边遍历边修改列表；用 `enumerate`/`zip` 替代 `range(len(...))`。

*（速查表里还有：`match`/`case`、三元表达式、`for/else`。）*

## 小结
你已经能干净利落地分支与循环。
**下一课：** 第 4 课——数据结构。

---

## 课后作业（第 4 课之前）

*课外完成——不计入课堂时间。完整题目 + 参考答案：`examples/session-03/practice.md` → **Homework**。*

1. **出勤标注器** —— 对一列百分比使用链式比较 + `elif` 梯子。
2. **猜数字游戏** —— 带输入校验和次数统计的 `while` 循环。
3. **闰年判断** —— 一个布尔表达式搞定，用刁钻年份验证。
