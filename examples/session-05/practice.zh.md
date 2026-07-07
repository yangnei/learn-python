# 第 5 课 —— 练习：函数、作用域与复用

每个答案都自己敲一遍。**运行之前先预测输出。** 参考答案在最后。

## 课堂练习

### 任务 1 —— 成绩函数库
写三个带文档字符串和类型标注的函数：
- `class_average(scores: list[float]) -> float`
- `letter_grade(score: float) -> str`（复用第 3 课）
- `pass_rate(scores: list[float], passing: float = 60) -> float`（及格比例，0–1）

`pass_rate` 用布尔求和（回想 `sum(s >= passing for s in scores)`）。

### 任务 2 —— 复现并修复可变默认值 bug
写 `add_note(text, notes=[])`：追加并返回。连调三次，看列表越长越大。
然后用 `None` 模式修好，并证明每次调用都从空列表开始。

### 任务 3 —— *args 汇总
写 `summary(*scores)`，返回字典 `{"n":..., "mean":..., "max":..., "min":...}`。
分别以 `summary(91, 58, 73)` 和 `summary(*my_list)` 两种方式调用。

### 加餐 —— Python 惯用法速练
盖住 `# ->` 后面的答案，逐行预测，再运行。

```python
def f(a, *, b):          # * 之后的参数只能用关键字传
    return a, b
print(f(1, b=2))                     # -> (1, 2)
print(f(**{"a": 1, "b": 9}))         # -> (1, 9)   （** 把字典摊开成参数）
```

## 课堂练习——更进一步（第二小时）

### 任务 1 —— 仅关键字参数
改写 `letter_grade(score, plus_minus)`，让 `plus_minus` **必须**用关键字传
（`letter_grade(95, plus_minus=True)`）；按位置传要抛 `TypeError`。

### 任务 2 —— 打磨文档字符串
给 `pass_rate` 写一个文档字符串：说明返回什么、`passing` 是什么意思、附一个
用法示例。一小段就好，不要废话。

### 任务 3 —— 自己写 `map`
写 `apply_to_all(func, values)`，返回把 `func` 应用到每个值的新列表。
用 `abs` 和一个加 5 分的 lambda 测试。

### 任务 4 —— 函数工厂
写 `make_curver(bonus)`，返回一个"加 `bonus` 分、上限 100"的函数。构造
`gentle = make_curver(5)` 和 `strict = make_curver(1)`，证明两者不同。

### 任务 5 —— 第一个装饰器
写 `@announce`：在被包装函数运行前打印 `calling <name> with <args>`。装饰你的
`letter_grade` 并调用。

### 任务 6 —— 一个 doctest
给 `class_average` 的文档字符串加两个 `>>>` 示例，然后运行
`python -m doctest your_file.py -v`，看它们通过。

## 课后作业（第 6 课之前）

*约 30–45 分钟，课外完成——不计入课堂时间。先都试一遍，再看答案。*

### 任务 1 —— 迷你统计库
三个函数，都带文档字符串和类型标注：
- `validate_score(x) -> float` —— 接受 0–100 内的 int/float/数字字符串；否则
  `raise ValueError`（并拒绝 `bool` —— 记得第 2 课！），
- `curve(scores: list[float], bonus: float = 5) -> list[float]` —— 加分、封顶 100，
  **不许修改输入列表**，
- `summarize(scores: list[float]) -> dict` —— `n` / `mean` / `min` / `max`。

### 任务 2 —— `mean_ignoring_none(*values)`
`mean_ignoring_none(90, None, 80, None, 70)` → `80.0`。清洗后什么都不剩时返回
`None`，而不是除以零。

### 任务 3 —— 作用域预测
这段代码打印什么——哪里会坏？*先预测*再运行：
```python
count = 0

def tally(xs):
    total = 0
    for x in xs:
        total += x
    return total

def bump():
    count = count + 1   # ← 在这里多想想

print(tally([1, 2, 3]))
bump()
```

---

## 参考答案

### 课堂练习

```python
def class_average(scores: list[float]) -> float:
    """Mean of scores."""
    return sum(scores) / len(scores)

def letter_grade(score: float) -> str:
    """A/B/C/D/F by 90/80/70/60 cutoffs."""
    for cutoff, letter in [(90,"A"),(80,"B"),(70,"C"),(60,"D")]:
        if score >= cutoff:
            return letter
    return "F"

def pass_rate(scores: list[float], passing: float = 60) -> float:
    """Fraction of scores >= passing (0..1)."""
    return sum(s >= passing for s in scores) / len(scores)

# 任务 2
def add_note(text, notes=None):     # 修好的版本
    if notes is None:
        notes = []
    notes.append(text)
    return notes

# 任务 3
def summary(*scores):
    return {"n": len(scores), "mean": sum(scores)/len(scores),
            "max": max(scores), "min": min(scores)}
print(summary(91, 58, 73))
print(summary(*[91, 58, 73]))
```

### 课堂练习——更进一步

```python
# 任务 1
def letter_grade(score, *, plus_minus=False):   # * 让后面的参数只能用关键字
    ...
# letter_grade(95, True)            -> TypeError
# letter_grade(95, plus_minus=True) -> 正常

# 任务 2
def pass_rate(scores, passing=60):
    """Return the fraction (0..1) of scores at or above `passing`.

    `passing` is the cutoff, 60 by default: pass_rate([70, 50, 90]) -> 0.66...
    """

# 任务 3
def apply_to_all(func, values):
    return [func(v) for v in values]

print(apply_to_all(abs, [-3, 4, -5]))                 # [3, 4, 5]
print(apply_to_all(lambda s: min(s + 5, 100), [58, 97]))   # [63, 100]

# 任务 4
def make_curver(bonus):
    def curve(score):
        return min(score + bonus, 100)
    return curve

gentle, strict = make_curver(5), make_curver(1)
print(gentle(96), strict(96))    # 100 97

# 任务 5
def announce(f):
    def wrapper(*args, **kwargs):
        print(f"calling {f.__name__} with {args}")
        return f(*args, **kwargs)
    return wrapper

@announce
def letter_grade(score):
    for cutoff, letter in [(90, "A"), (80, "B"), (70, "C"), (60, "D")]:
        if score >= cutoff:
            return letter
    return "F"

print(letter_grade(85))          # calling letter_grade with (85,)  ->  B

# 任务 6
def class_average(scores):
    """Mean of scores.

    >>> class_average([90, 80, 70])
    80.0
    >>> class_average([100])
    100.0
    """
    return sum(scores) / len(scores)
# python -m doctest your_file.py -v  ->  2 passed.
```

### 课后作业

```python
# 任务 1
def validate_score(x) -> float:
    """Return x as a float score in 0-100, or raise ValueError."""
    if isinstance(x, bool):                  # bool 会冒充数字混过 float()！
        raise ValueError("bool is a flag, not a score")
    score = float(x)                         # 坏字符串在这里抛 ValueError
    if not 0 <= score <= 100:
        raise ValueError(f"{score} outside 0-100")
    return score

def curve(scores: list[float], bonus: float = 5) -> list[float]:
    """Return a NEW list with `bonus` added to each score, capped at 100."""
    return [min(s + bonus, 100) for s in scores]

def summarize(scores: list[float]) -> dict:
    """n, mean, min, max of `scores`."""
    return {"n": len(scores), "mean": sum(scores) / len(scores),
            "min": min(scores), "max": max(scores)}

# 任务 2
def mean_ignoring_none(*values):
    clean = [v for v in values if v is not None]
    return sum(clean) / len(clean) if clean else None

print(mean_ignoring_none(90, None, 80, None, 70))   # 80.0
print(mean_ignoring_none(None, None))               # None

# 任务 3
# tally([1, 2, 3]) 打印 6 —— `total` 是 tally 的局部变量，与谁都不冲突。
# bump() 抛 UnboundLocalError：那次赋值让 `count` 成为 bump 的局部变量，
# 于是右边读到的是一个还不存在的局部名。
# 修法不是 `global` —— 返回新值，在调用处重新赋值。
```
