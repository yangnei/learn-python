# 第 3 课 —— 练习：控制流：条件与循环

每个答案都自己敲一遍。**运行之前先预测输出。** 参考答案在最后。

## 课堂练习

### 任务 1 —— 分数分档器
写 `letter_grade(score)`，按 90/80/70/60 的界限返回 A/B/C/D/F，超出 0–100 返回
`"Invalid"`。**测试边界值：** 90、89.999、0、100、-5、101。

### 任务 2 —— 布尔逻辑
1. `5 and 0` 是什么？`"" or "N/A"` 呢？为什么它们不是 `True`/`False`？
2. 用 Pythonic 的方式重写 `if attended == True:`。

### 任务 3 —— 平均分 + 及格/不及格（循环）
给定 `names = ["Ana","Ben","Cara","Dev"]` 和 `scores = [91, 58, 73, 64]`：
1. 用循环和累加变量算平均分。
2. 用 `zip` 打印 `"<name>: PASS"`（≥60）或 `"<name>: FAIL"`。
3. 用 `sum(s >= 60 for s in scores)` 数及格人数。

### 任务 4 —— 输入校验循环
写一个真正的 `while True:` 提示循环，直到用户输入 0–100 的整数才停。

### 任务 5 —— 陷阱检查
这段代码为什么会跳过元素？怎么修？
```python
xs = [1, 2, 3, 4]
for x in xs:
    if x % 2 == 0:
        xs.remove(x)
```

### 任务 6 —— 双重标签 bug
这段代码本想只打印一个标签，95 分却打了三个。解释原因，然后**在不改任何条件的
前提下**修好它：
```python
if score >= 60: print("passing")
if score >= 80: print("strong")
if score >= 90: print("excellent")
```

### 加餐 —— Python 惯用法速练
盖住 `# ->` 后面的答案，逐行预测，再运行。

```python
nums = [80, 92, 45]
print(all(n >= 60 for n in nums))    # -> False   （45 不及格）
print(any(n >= 90 for n in nums))    # -> True    （92 达标）
print(92 in nums, 60 in nums)        # -> True False
```

## 课堂练习——更进一步（第二小时）

### E1 —— 改写成链式比较
各用一个链式比较重写：
1. `if x >= 0 and x <= 100:`
2. `if lo < value and value < hi:`
3. `if a == b and b == c:`

### E2 —— 倒计时
打印 10 → 1 再打印 `Go!`——先用 `range`，再用 `while`。**两端**的差一错误都要当心。

### D1 —— `match/case` 重写
用 `match/case` 重写你的李克特分类器：5/4 → `"agree"`、3 → `"neutral"`、
1/2 → `"disagree"`、其他 → `"invalid"`。这里哪个版本更好读——为什么？

### D2 —— `for/else` 查找
在 `[91, 73, 84, 58, 90]` 中找出第一个低于 60 的分数并打印；如果没有，打印
`"everyone passed"`——**不许**用 `found` 旗标变量。

### D3 —— 一趟找出最高和最低
在对 `[73, 91, 58, 84]` 的一次循环里同时跟踪迄今最高和迄今最低（不用
`max()`/`min()`）。两个都打印出来。

### D4 —— 把判断本身返回出去
把下面每个改写成单行 `return`，然后挑一个在 `if` 里裸用（不写 `== True`）：
```python
def is_passing(score):
    if score >= 60:
        return True
    else:
        return False

def is_full_class(roster):
    if len(roster) >= 30:
        return True
    return False
```

## 课后作业（第 4 课之前）

*约 30–45 分钟，课外完成——不计入课堂时间。先都试一遍，再看答案。*

### H1 —— 出勤标注器
写 `label(pct)` → `"perfect"`（恰好 100）、`"good"`（≥ 80）、`"at risk"`（≥ 50），
其余 `"critical"`；超出 0–100 返回 `"invalid"`。对
`[100, 92.5, 80, 79.9, 50, 12, -3, 104]` 循环打印 `pct -> label`。**测试每个边界。**

### H2 —— 猜数字游戏
设 `secret = 37`。循环：读入一个猜测（校验它是 1–100 的整数——复用今天的校验循环
模式），打印 `higher` / `lower` / `got it in N tries`。统计次数。

### H3 —— 闰年判断
`is_leap(year)`：能被 4 整除，但整百年除外，除非能被 400 整除——写成**一个**布尔
表达式。验证：2024 → True、1900 → False、2000 → True、2026 → False。

---

## 参考答案

### 课堂练习

```python
# 1
def letter_grade(score):
    if not 0 <= score <= 100: return "Invalid"
    for cutoff, g in [(90,"A"),(80,"B"),(70,"C"),(60,"D")]:
        if score >= cutoff: return g
    return "F"
# 90->A, 89.999->B, 0->F, 100->A, -5->Invalid, 101->Invalid

# 2
# 5 and 0 -> 0 ; "" or "N/A" -> "N/A"  （and/or 返回操作数，不是布尔值）
result = "pass" if attended else "absent"     # 判断就写 `if attended:`

# 3
total = 0
for s in scores: total += s
print(total / len(scores))                    # 71.5
for name, score in zip(names, scores):
    print(f"{name}: {'PASS' if score >= 60 else 'FAIL'}")
print("passes:", sum(s >= 60 for s in scores))   # 3

# 4
while True:
    raw = input("Score 0–100: ")
    if raw.isdigit() and 0 <= int(raw) <= 100:
        print("Got", int(raw)); break
    print("Try again.")

# 5  边遍历边删除会让下标错位，元素被跳过。
xs = [x for x in xs if x % 2 != 0]            # 改为构建新列表 -> [1, 3]

# 6  三个独立的 if 是三个互不相干的问题 —— 95 对三个都答"是"。
#    串成梯子，最具体的放最前，只有第一个命中的运行：
if score >= 90:
    print("excellent")
elif score >= 80:
    print("strong")
elif score >= 60:
    print("passing")
```

### 课堂练习——更进一步

```python
# E1
0 <= x <= 100
lo < value < hi
a == b == c

# E2
for n in range(10, 0, -1):    # 从 10 开始，到 0 之前停，步长 -1
    print(n)
print("Go!")

n = 10
while n >= 1:
    print(n)
    n -= 1
print("Go!")

# D1
def likert_label(answer):
    match answer:
        case 5 | 4:
            return "agree"
        case 3:
            return "neutral"
        case 1 | 2:
            return "disagree"
        case _:
            return "invalid"
# 这里 match 胜出：每个分支都在拿同一个值对比字面量。

# D2
for s in [91, 73, 84, 58, 90]:
    if s < 60:
        print("first failing:", s)
        break
else:
    print("everyone passed")

# D3
scores = [73, 91, 58, 84]
best = worst = scores[0]
for s in scores[1:]:
    if s > best:
        best = s
    if s < worst:
        worst = s
print("best:", best, "worst:", worst)    # 91 58

# D4
def is_passing(score):
    return score >= 60             # 比较结果本来就是 bool

def is_full_class(roster):
    return len(roster) >= 30

if is_passing(72):                 # 裸用 —— 永远别写 `== True`
    print("through!")
```

### 课后作业

```python
# H1
def label(pct):
    if not 0 <= pct <= 100:
        return "invalid"
    if pct == 100:
        return "perfect"
    if pct >= 80:
        return "good"
    if pct >= 50:
        return "at risk"
    return "critical"

for pct in [100, 92.5, 80, 79.9, 50, 12, -3, 104]:
    print(pct, "->", label(pct))
# 100 perfect · 92.5 good · 80 good · 79.9 at risk · 50 at risk · 12 critical ·
# -3 invalid · 104 invalid

# H2
secret, tries = 37, 0
while True:
    raw = input("Guess 1-100: ")
    if not (raw.isdigit() and 1 <= int(raw) <= 100):
        print("Whole number 1-100, try again.")
        continue
    tries += 1
    guess = int(raw)
    if guess < secret:
        print("higher")
    elif guess > secret:
        print("lower")
    else:
        print(f"got it in {tries} tries")
        break

# H3
def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

print(is_leap(2024), is_leap(1900), is_leap(2000), is_leap(2026))
# True False True False
```
