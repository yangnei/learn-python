# 第 11 课 —— 练习：NumPy 与 pandas：处理研究数据

每道题都自己敲一遍。**运行之前先预测每一行输出。** 参考答案在最后。

## 课堂练习

提供的文件：`students.csv`、`survey.csv`（和第 8 课是同一份数据）。每个脚本开头都写上 `import numpy as np` 和 `import pandas as pd`。

### 任务 1 —— 向量化第 8 课
把分数 `[91, 58, 73, 64, 88, 79]` 放进一个 NumPy 数组。不用循环，打印：均值、每个分数加 5 分（用 `np.minimum` 封顶 100），以及及格（分数 >= 60）的人数。

### 任务 2 —— 小测成绩表
用你自己的数字建一个 3×4 数组（3 个学生、4 次小测）。打印每个学生的均值和每次小测的均值。哪个 `axis` 对应哪个？然后打印最高分，以及**是哪个学生**拿到的（在正确的轴上用 `np.argmax`）。

### 任务 3 —— 读进来看一看
`pd.read_csv("students.csv")`。打印 `.shape`、`.head()`、`.info()` 和
`["score"].describe()`。把均值和你第 8 课手算的结果对比一下。

### 任务 4 —— 筛选并打标签
只显示分数低于 80 的 Education 学生。然后用 `pd.cut` 加一列 `grade`
（A ≥ 90、B ≥ 80、C ≥ 70、D ≥ 60，否则 F），按分数排序后打印。

### 任务 5 —— 按专业的描述统计
用一次 `groupby(...).agg(...)`，做出每个专业的 `n`、`mean_score`、`min_score`、
`max_score`，并按 `mean_score` 排序。

### 陷阱检查
先预测，再运行：`np.array([60, 75]) > 70 and np.array([60, 75]) < 90`。会发生什么？应该怎么写？

### 加餐 —— Python 惯用法速练
盖住 `# ->` 后面的答案，逐行预测，再运行。

```python
import numpy as np
a = np.array([3, 1, 2])
print(a * 2)                  # -> [6 2 4]        （列表会重复：[3, 1, 2, 3, 1, 2]）
print(a[a > 1])               # -> [3 2]          （掩码：保留为 True 的位置）
print(np.sort(a)[::-1])       # -> [3 2 1]        （先排序，再反转）
print((a > 1).mean())         # -> 0.666...       （True 所占的比例）
```

## 课堂练习——更进一步（第二小时）

### 任务 1 —— 用广播算 z 分数
对任务 2 的小测成绩表，用一个表达式算出每个格子**在其所在小测列内**的 z 分数。检查每一列的均值现在是否约等于 0。

### 任务 2 —— 视图带来的意外
令 `a = np.arange(5)`，取 `b = a[1:3]`，执行 `b[:] = 0`。预测 `a`。再用
`.copy()` 重做一遍，确认 `a` 安然无恙。

### 任务 3 —— 清洗问卷
读取 `survey.csv`，让 `"N/A"` 变成缺失值。打印每列的缺失数、每道 `q*` 题的均值，以及完整行的数量。为什么 `q2_clarity` 变成了 `float64`？

### 任务 4 —— 变成长表
把问卷 melt 成每行一个（受访者、题目、评分）。做出每道题的 `mean` 和 `count`
表，再做一个题目 × 评分的 `crosstab`。

### 任务 5 —— 谁高于本专业平均？
用 `groupby(...).transform("mean")` 加一列 `major_mean`，然后列出分数高于本专业平均分的学生。

### 任务 6 —— 连接导师信息
创建 `advisors`（Education → Dr. Lee，Psychology → Dr. Okafor）。用
`validate="many_to_one"` 把它左连接到学生表上。哪些学生得到了 `NaN`？加上
`indicator=True` 再跑一次来确认。

### 任务 7 —— 每周登录
用 `rng = np.random.default_rng(1)` 构造 21 天的登录数（`pd.date_range` +
`rng.integers(10, 50, size=21)`）。用 `resample("W")` 打印每周合计，再打印 3 天移动平均。

## 课后作业（毕业项目之前）

*约 30–45 分钟，课外完成——不计入课堂时间。先全部尝试，再看参考答案。*

### 任务 1 —— 用 pandas 重写第 8 课
拿出你第 8 课的问卷汇总（每题均值和 `n_valid`，写入 `survey_summary.csv`）。用 pandas **最多六行**重做一遍。对比两份输出文件：数字一致吗？

### 任务 2 —— 一次模拟
用带种子的生成器，模拟 10,000 个班级，每班 30 个学生，分数为
`rng.normal(72, 12)`（截断到 0–100）。均值**高于 75** 的班级占多少比例？用同一个种子跑两次，再换一个种子跑。

### 任务 3 —— 你自己的数据
用 `pd.read_csv` 读入你自己工作中的一个 CSV。运行 `.info()` 和 `.isna().sum()`，然后做一张你会放进论文的 `groupby` 表。写下你做的每一个清洗决定（删了？填补了？改名了？），因为这份清单*就是*你方法部分的一部分。

---

## 参考答案

### 课堂练习

```python
import numpy as np
import pandas as pd

# 任务 1
scores = np.array([91, 58, 73, 64, 88, 79])
print(scores.mean())                      # 75.5
print(np.minimum(scores + 5, 100))        # [96 63 78 69 93 84]
print((scores >= 60).sum())               # 5

# 任务 2
q = np.array([[8, 9, 7, 10], [5, 6, 4, 7], [9, 9, 10, 8]])
print(q.mean(axis=1))                     # 每个学生（压掉列）
print(q.mean(axis=0))                     # 每次小测（压掉行）
print(q.max(), "by student", q.max(axis=1).argmax())   # 10，学生 0（并列时取第一个）

# 任务 3
students = pd.read_csv("students.csv")
print(students.shape)                     # (6, 3)
students.info()
print(students["score"].describe())       # 均值 75.5——和第 8 课一样

# 任务 4
print(students[(students["major"] == "Education") & (students["score"] < 80)])
students["grade"] = pd.cut(students["score"], bins=[0, 59, 69, 79, 89, 100],
                           labels=["F", "D", "C", "B", "A"])
print(students.sort_values("score", ascending=False))

# 任务 5
table = students.groupby("major").agg(
    n=("name", "count"), mean_score=("score", "mean"),
    min_score=("score", "min"), max_score=("score", "max"),
).sort_values("mean_score", ascending=False)
print(table)
```

陷阱：`ValueError: The truth value of an array with more than one element is ambiguous`。
`and` 需要**一个** True/False，但两边都是整个数组。写成
`(a > 70) & (a < 90)`，括号不能少，因为 `&` 比 `>` 绑定得更紧。

### 课堂练习——更进一步

```python
# 任务 1
z = (q - q.mean(axis=0)) / q.std(axis=0)  # (3,4) - (4,) 沿行向下广播
print(z.mean(axis=0).round(10))           # 全是 0（"-0." 也是 0）

# 任务 2
a = np.arange(5); b = a[1:3]; b[:] = 0
print(a)                                  # [0 0 0 3 4] —— b 是视图
a = np.arange(5); b = a[1:3].copy(); b[:] = 0
print(a)                                  # [0 1 2 3 4]

# 任务 3
survey = pd.read_csv("survey.csv", na_values=["N/A"])
items = [c for c in survey.columns if c.startswith("q")]
print(survey.isna().sum())
print(survey[items].mean().round(2))
print(len(survey.dropna()))               # 6
# q2 有一个空白 -> NaN，而 NaN 是浮点数，所以整列变成 float64。

# 任务 4
long = survey.melt(id_vars="respondent", value_vars=items, var_name="item", value_name="rating")
print(long.groupby("item")["rating"].agg(["mean", "count"]).round(2))
print(pd.crosstab(long["item"], long["rating"]))

# 任务 5
students["major_mean"] = students.groupby("major")["score"].transform("mean")
print(students[students["score"] > students["major_mean"]]["name"].tolist())   # ['Ana', 'Eve']

# 任务 6
advisors = pd.DataFrame({"major": ["Education", "Psychology"], "advisor": ["Dr. Lee", "Dr. Okafor"]})
joined = students.merge(advisors, on="major", how="left", validate="many_to_one", indicator=True)
print(joined[["name", "major", "advisor", "_merge"]])   # Dev（Sociology）-> NaN，left_only

# 任务 7
rng = np.random.default_rng(1)
logins = pd.Series(rng.integers(10, 50, size=21),
                   index=pd.date_range("2026-09-01", periods=21, freq="D"))
print(logins.resample("W").sum())
print(logins.rolling(3).mean().round(1).tail())
```

### 课后作业

```python
# 任务 1 —— 六行
survey = pd.read_csv("survey.csv", na_values=["N/A"])
items = [c for c in survey.columns if c.startswith("q")]
out = pd.DataFrame({"item": items,
                    "mean": survey[items].mean().round(2).values,
                    "n_valid": survey[items].count().values})
out.to_csv("survey_summary_pandas.csv", index=False)
print(out)

# 任务 2
rng = np.random.default_rng(7)
classes = np.clip(rng.normal(72, 12, size=(10_000, 30)), 0, 100)   # 每行 = 一个班
print((classes.mean(axis=1) > 75).mean())   # 约 0.08：班级均值超过 75 很少见
```

任务 3 由你自己完成：套路是 `read_csv` → `info()` / `isna().sum()` → 清洗 →
`groupby(...).agg(...)`，再加上那份写下来的决定清单。
