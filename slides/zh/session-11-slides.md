---
marp: true
title: "第 11 课 — NumPy 与 pandas：处理研究数据"
paginate: true
---

# 第 11 课
## NumPy 与 pandas：处理研究数据

---

## 为什么是现在？🧠

第 8 课里，你**手工**算出了全班均值、各专业均值和问卷每题的均值：循环、
`setdefault`、一个 `to_int` 清洗函数。这正是用意——现在你知道底层到底要做什么了。

今天，两个库让每件事都只需一行：

- **NumPy** —— 快速的数值数组（引擎）。
- **pandas** —— 建在 NumPy 之上、带标签的表格（用代码驱动的电子表格）。

```bash
pip install numpy pandas        # Colab 和浏览器笔记本已预装
```

```python
import numpy as np              # 社区通用的简称
import pandas as pd
```

---

## 列表 vs 数组

```python
scores = [91, 58, 73]
scores * 2                 # [91, 58, 73, 91, 58, 73]   <- 列表是**重复**

import numpy as np
arr = np.array([91, 58, 73])
arr * 2                    # array([182, 116, 146])     <- 数组是**相乘**
arr.dtype, arr.shape       # (dtype('int64'), (3,))
```

NumPy 数组把**同一种类型**放在**一整块内存**里，运算在编译好的 C 代码中执行。更快，*也*更短。

```python
np.zeros(3)                # array([0., 0., 0.])
np.arange(0, 10, 2)        # 类似 range()：array([0, 2, 4, 6, 8])
np.linspace(0, 1, 5)       # 5 个等距点，两端都包含
```

---

## 向量化：说"做什么"，而不是"怎么做"

```python
arr + 5                    # 每个分数都加 5 分
arr / 100                  # 换成小数
arr.mean(), arr.std()      # 整个数组的统计量
np.sqrt(arr)
```

第 3 课你写的是：`for s in scores: new.append(s + 5)`。
NumPy 写成：`scores + 5`。循环仍然存在，只是在 C 里跑，而不是在 Python 里。

⚠️ 整数数组保持整数：`np.array([1, 2]) / 2` 得到浮点数，但把浮点数**赋值进**
整数数组会被截断。

---

## 布尔掩码——最有用的一招

对数组做比较，会得到一个 `True`/`False` 数组——用它来**筛选**：

```python
scores = np.array([91, 58, 73, 64, 88])
passed = scores >= 60            # array([ True, False,  True,  True,  True])
scores[passed]                   # array([91, 73, 64, 88])
passed.sum()                     # 4 —— True 算作 1（第 2 课！）
scores[(scores >= 60) & (scores < 80)]    # 用 & | ~，每个条件都要加括号
np.where(scores >= 60, "pass", "fail")    # 向量化的 if/else
```

⚠️ 对数组用 `and` / `or` 会抛出 **ValueError: truth value … is ambiguous**。Python
没法把五个布尔值变成一个。请用 `&`、`|`、`~`。

---

## 二维数组与 `axis`

```python
# 行 = 学生，列 = 小测
quizzes = np.array([[8, 9, 7, 10],
                    [5, 6, 4, 7],
                    [9, 9, 10, 8]])
quizzes.shape            # (3, 4)
quizzes[1, 2]            # 4 —— 第 1 行、第 2 列
quizzes[0]               # 第一个学生的一行
quizzes[:, 3]            # 每个学生的第 3 次小测
quizzes.mean(axis=0)     # **每次小测**一个均值（压掉行）
quizzes.mean(axis=1)     # **每个学生**一个均值（压掉列）
```

记忆口诀：**`axis` 指的是会消失的那个维度。**

---

## pandas：Series 与 DataFrame

- **Series** —— 一列带标签的数据。
- **DataFrame** —— 共用同一个行索引的多个 Series 组成的表。

```python
import pandas as pd
students = pd.read_csv("students.csv")   # 一行代替你的 DictReader 循环
students.head()           # 前 5 行
students.shape            # (6, 3)
students.info()           # 列、类型、非空计数——**先**看这个
students.describe()       # 数值列的 count/mean/std/min/四分位数/max
```

和 `csv` 不同，`read_csv` 会**推断类型**：`score` 读进来就是数字，不是字符串。

---

## 选取数据

| 你想要 | 写法 |
|---|---|
| 一列（Series） | `df["score"]` |
| 多列 | `df[["name", "score"]]` |
| 按**标签** | `df.loc[0, "name"]`、`df.loc[0:2, ["name"]]` |
| 按**位置** | `df.iloc[0, 0]`、`df.iloc[-1]` |

⚠️ `loc` 切片**包含**结束标签；`iloc` 切片**不包含**结束位置（和普通 Python 一样）。
`df.loc[0:2]` 是 3 行；`df.iloc[0:2]` 是 2 行。

---

## 筛选行

和 NumPy 的掩码思路一样：

```python
students[students["score"] >= 75]
students[(students["major"] == "Education") & (students["score"] < 80)]
students[students["major"].isin(["Sociology", "Psychology"])]
students.query("score > 70 and major != 'Education'")   # 更易读的写法
```

---

## 新列、排序、计数

```python
students["passed"] = students["score"] >= 60
students["grade"] = pd.cut(students["score"], bins=[0, 59, 69, 79, 89, 100],
                           labels=["F", "D", "C", "B", "A"])
students["z"] = (students["score"] - students["score"].mean()) / students["score"].std()

students.sort_values("score", ascending=False)
students["major"].value_counts()          # 针对一列的 Counter
```

优先用这些向量化写法，而不是 `.apply(某个函数)`——后者每行都跑一次 Python，速度就没了。

---

## groupby：拆分 → 计算 → 合并 🧠

你第 8 课的整个"按专业"循环：

```python
students.groupby("major")["score"].mean()
```

一次算多个统计量，列名也干净（**具名聚合**）：

```python
students.groupby("major").agg(
    n=("name", "count"),
    mean_score=("score", "mean"),
    best=("score", "max"),
)
```

研究上的桥梁：这就是"按条件分组的描述统计"——大多数结果部分的第一张表。

---

## 轮到你了

`examples/session-11/practice.md`：
1. 用 NumPy 向量化第 8 课：全班均值、加分、及格人数。
2. 把学生数据读进 pandas，筛选，加一列等级。
3. 按专业 `groupby`：人数、均值、最高分。

---

# 更进一步
## 会伸缩的数组，会变形的表格

---

## 视图 vs 副本

```python
original = np.array([91, 58, 73, 64])
view = original[:2]       # 切片是同一块内存的**视图**
view[0] = 0
original                  # array([ 0, 58, 73, 64])   <- 变了！

safe = original[:2].copy()   # 独立的副本
```

第 2 课的别名问题又回来了：切**列表**会复制，切**数组**不会。（布尔索引和列表索引 `arr[mask]` 返回的是副本。）

---

## 广播

形状不同的数组也能一起运算：**从右往左**比较，每个维度要么相等，要么是 1。大小为 1 的维度会被拉伸。

```python
weights = np.array([0.1, 0.2, 0.3, 0.4])        # (4,)   每次小测一个权重
(quizzes * weights).sum(axis=1)                 # (3, 4) * (4,) -> 每个学生的加权总分

z = (quizzes - quizzes.mean(axis=0)) / quizzes.std(axis=0)   # 每一列都做 z 分数
```

不用循环行或列：均值那一行会被拉伸到所有学生身上。

---

## 可复现的随机数

```python
rng = np.random.default_rng(seed=42)    # 新式 Generator 接口
rng.integers(1, 7, size=8)              # 掷骰子
rng.normal(loc=70, scale=10, size=5)    # 模拟分数
rng.choice(["A", "B"], size=10)         # 随机分配到实验条件

sums = rng.integers(1, 7, size=(100_000, 2)).sum(axis=1)
(sums == 7).mean()                      # 约 0.167，两行代码完成一次模拟
```

同一个种子 → 同样的数字 → 可复现的方法部分（第 8 课的道理，放大版）。

---

## 缺失数据

```python
survey = pd.read_csv("survey.csv", na_values=["N/A"])   # "N/A" 和空白 -> NaN
survey.isna().sum()                    # 每列缺失多少
survey["q2_clarity"].mean()            # pandas 会**跳过** NaN（NumPy 的 .mean() 会得到 nan）
survey.dropna()                        # 只保留完整的行
survey.fillna(survey.median(numeric_only=True))   # 用各列中位数填补
```

⚠️ 只要有一个缺失值，整数列就会变成 **float64**，因为 NaN 是浮点数。你的 1–5 李克特量表列现在显示成 `4.0`。

删掉还是填补，是一个**方法学决定**：要在论文里写明。

---

## transform：把分组统计放回每一行

`agg` 缩成每组一行；`transform` 保持原来的形状：

```python
students["major_mean"] = students.groupby("major")["score"].transform("mean")
students["vs_major"] = students["score"] - students["major_mean"]
```

"每个学生离本专业平均分有多远？"——不需要 merge。

---

## 变形：宽 ↔ 长

问卷导出的数据是**宽**的（每题一列）。大多数分析想要**长**的（每个回答一行）：

```python
long = survey.melt(id_vars="respondent", var_name="item", value_name="rating")
long.groupby("item")["rating"].agg(["mean", "count"])
pd.crosstab(long["item"], long["rating"])        # 频数表：每题有几个 1、几个 2……

students.pivot_table(index="major", columns="passed", values="score",
                     aggfunc="count", fill_value=0)   # 长 -> 宽的汇总
```

---

## merge：连接两张表

```python
advisors = pd.DataFrame({"major": ["Education", "Psychology", "History"],
                         "advisor": ["Dr. Lee", "Dr. Okafor", "Dr. Ruiz"]})
students.merge(advisors, on="major", how="left", validate="many_to_one")
```

| `how=` | 保留 |
|---|---|
| `"inner"`（默认） | 两边都有的键 |
| `"left"` | 左表的每一行（没匹配上 → NaN） |
| `"outer"` | 全部 |

`validate=` 能抓住意外重复的键；`indicator=True` 会加一列 `_merge`，显示每行来自哪边。连接后"丢了行"时，两个都用上。

---

## 日期与时间序列

```python
logins["day"] = pd.to_datetime(logins["day"])   # 或 read_csv(..., parse_dates=["day"])
logins["day"].dt.day_name()                     # .dt = 针对一列的日期工具
weekly = logins.set_index("day")["logins"].resample("W").sum()   # 每周合计
logins["logins"].rolling(7).mean()              # 7 天移动平均
```

`.str` 对文本列做同样的事：`df["name"].str.upper()`、
`.str.contains("ED")`、`.str.strip()`。

---

## 链式调用

每一步都返回一个新的 DataFrame，所以整个分析从上读到下：

```python
report = (
    students
    .query("passed")
    .groupby("major", as_index=False)
    .agg(n=("name", "count"), mean_score=("score", "mean"))
    .sort_values("mean_score", ascending=False)
)
report.to_csv("report.csv", index=False)
```

---

## 唯一的赋值规则 ⚠️

```python
students[students["score"] < 60]["grade"] = "D"      # ✗ 改的是一个临时副本
students.loc[students["score"] < 60, "grade"] = "D"  # ✓ 一次 .loc：行、列
```

第一行先筛选出一个**副本**，再在副本上赋值，所以 `students` 根本没变（pandas 会发出警告）。改值永远用一次 `.loc[行, 列]`。

---

## 轮到你了——第二轮

`examples/session-11/practice.md` → **In class — going deeper**：用广播算 z 分数、清洗问卷的缺失值、把问卷 melt 成长表、merge 导师信息，以及按周 resample。

---

## 陷阱回顾

- 列表 `* 2` 是重复；数组 `* 2` 是相乘。
- 对数组用 `and`/`or` → ValueError；用带括号的 `&`/`|`/`~`。
- 数组切片是**视图**；需要独立就 `.copy()`。
- 一个 NaN 就能把整数列变成浮点数。
- `loc` 切片包含结尾；`iloc` 不包含。
- 改值用一次 `.loc[行, 列]`，绝不用 `df[mask]["col"] = ...`。

## 小结
第 8 课里手工做的一切，现在都是一两行代码——而且你知道每一行底下在做什么。
**下一步（可选）：** 毕业项目。愿意的话，用 pandas 来做。

---

## 课后作业（毕业项目之前）

*课外完成——不计入课堂时间。完整题目 + 参考答案：`examples/session-11/practice.md` → **Homework**。*

1. **用 pandas 重写第 8 课。** 六行写出问卷汇总；对比两份输出。
2. **一次模拟。** 10,000 个带种子的班级：均值超过 75 的有多常见？
3. **你自己的数据。** 一张能放进论文的 `groupby` 表，外加你的清洗决定清单。
