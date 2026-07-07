# 第 8 课 —— 练习：文件、库与研究数据

每个答案都自己敲一遍。**运行之前先预测输出。** 参考答案在最后。

## 课堂练习

本文件夹提供：`students.csv`、`survey.csv`。

### 任务 1 —— 读取并汇总学生
用 `csv.DictReader` 读 `students.csv`。记住值是**字符串**——把 `score` 转成
`int`。用 `statistics` 模块打印全班均值和中位数。

### 任务 2 —— 按专业求均值
构建 `{major: mean_score}`。（提示：`dict.setdefault(key, []).append(...)`。）

### 任务 3 —— 清洗并汇总问卷
`survey.csv` 的数字列里混着 `"N/A"` 和空白。对每个 `q*` 题目，只对**有效**值求均值，
并统计有效个数。写出 `survey_summary.csv`，列为 `item,mean,n_valid`。

### 任务 4 —— pandas 预告（可选）
装了 `pandas` 的话：`pd.read_csv("students.csv")["score"].describe()`。把均值和你
手算的对比一下。

### 陷阱检查
如果不小心用 `"w"` 模式打开 `students.csv` 再去读，会发生什么？

### 加餐 —— Python 惯用法速练
盖住 `# ->` 后面的答案，逐行预测，再运行。

```python
import json
s = json.dumps({"n": 3, "ok": True})
print(s)                             # -> {"n": 3, "ok": true}   （Python 的 True -> JSON 的 true）
print(json.loads(s)["ok"])           # -> True                   （再翻译回 Python 布尔值）
```

## 课堂练习——更进一步（第二小时）

### E1 —— 再加一列
扩展问卷汇总：加一列 `pct_valid`（有可用值的行占比），保留一位小数。

### E2 —— pathlib 小巡游
用 `from pathlib import Path`：`students.csv` 存在吗？多少字节
（`.stat().st_size`）？列出本文件夹的每个 `.csv`（`.glob`）。

### D1 —— pathlib 盘点
用 `Path(".").glob` 和 `.stat().st_size` 把本文件夹每个 `.csv` 及其字节数
打印成对齐的行。

### D2 —— 日期运算
用 `strptime` 解析 `"2026-01-05"` 和 `"2026-07-06"`，打印两者相差的天数，
再用 `strftime` 把第一个日期打印成 `Jan 05, 2026`。

### D3 —— 可复现的抽样
先 `random.seed(42)`，再从 `students.csv` 的学生里 `random.sample` 抽 3 人。
跑两遍——同样 3 个人吗？论文的方法部分为什么在乎这一点？

### D4 —— CSV → JSON
把 `students.csv` 读成分数为 **int** 的字典列表，用 `indent=2` 写成
`students.json`。打开文件看看：引号和数字发生了什么？

### D5 —— 从命令行取文件名
把任务 1 改造成 `report.py`：读命令行指定的 CSV
（`python3 report.py students.csv`），打印全班均值；参数缺失或多余时输出用法
提示并退出。（`sys.argv`、`sys.exit`。）

### D6 —— 会动的前后对比
用 Pillow（`pip install pillow`）以 `Image.new("RGB", (60, 60), color)` 生成两帧
纯色图，存成一个循环播放的 GIF（`save_all=True`、`append_images=[...]`、
`duration=400`、`loop=0`）。打开文件——它在闪。这个二进制文件有多大（`pathlib`）？

## 课后作业（第 9 课之前）

*约 30–45 分钟，课外完成——不计入课堂时间。先都试一遍，再看答案。*

### H1 —— 出勤报告（完整管道）
自己创建 `attendance.csv`：一列 `name` 加五列 0/1 的 `s1..s5`，约六行——再偷偷放
一个脏单元格（`"?"`）。然后：用 `DictReader` 读入，计算每人出勤率（跳过脏值；
记住 0/1 整数直接可以求和），用 `DictWriter` 写出 `attendance_report.csv`，列为
`name,rate,n_valid`。全部放在 `with open(...)` 里。

### H2 —— JSON 往返
用 `json.dump` 把各题均值存进 `summary.json`（`indent=2`），用 `json.load` 读回，
验证 `loaded == original`。再用编辑器打开文件——`True` 变成了什么？

### H3 —— 你自己的数据
把这条管道对准你工作里的任何一个 CSV（需要的话从 Excel/表格导出一个）：
读入、数行数、算一个均值、打印两行报告。记下你遇到的第一个脏值和你的处理方式
——写进你的 bug 日志。

---

## 参考答案

### 课堂练习

见本文件夹的 `demo.py`——任务 1–3 的完整实现。关键行：

```python
scores = [int(s["score"]) for s in students]     # 字符串要转换！
statistics.mean(scores)                           # 75.5

by_major = {}
for s in students:
    by_major.setdefault(s["major"], []).append(int(s["score"]))

def to_int(x):
    try: return int(x)
    except (ValueError, TypeError): return None   # 处理 N/A 和 ""
```

陷阱：用 `"w"` 打开会**立刻把文件清空**——你还没读，数据就没了。
读取用 `"r"`（默认值）。

### 课堂练习——更进一步

```python
# E1 —— 在问卷题目循环里
vals = [to_int(r[item]) for r in rows]
good = [v for v in vals if v is not None]
writer.writerow({"item": item,
                 "mean": round(statistics.mean(good), 2),
                 "n_valid": len(good),
                 "pct_valid": f"{100 * len(good) / len(vals):.1f}"})

# E2
from pathlib import Path
p = Path("students.csv")
print(p.exists())                      # True（在本文件夹）
print(p.stat().st_size)                # 字节数
print(sorted(Path(".").glob("*.csv"))) # 这里的每个 CSV

# D1
for p in sorted(Path(".").glob("*.csv")):
    print(f"{p.name:<24}{p.stat().st_size:>8,} bytes")

# D2
from datetime import datetime
a = datetime.strptime("2026-01-05", "%Y-%m-%d")
b = datetime.strptime("2026-07-06", "%Y-%m-%d")
print((b - a).days)                    # 182
print(a.strftime("%b %d, %Y"))         # Jan 05, 2026

# D3
import csv, random
with open("students.csv", newline="", encoding="utf-8") as f:
    names = [r["name"] for r in csv.DictReader(f)]
random.seed(42)
print(random.sample(names, 3))         # 每次运行同样 3 人 —— 种子固定了随机数，
                                       # 你的"随机"抽样因此可复现。

# D4
import json
with open("students.csv", newline="", encoding="utf-8") as f:
    rows = [{**r, "score": int(r["score"])} for r in csv.DictReader(f)]
Path("students.json").write_text(json.dumps(rows, indent=2))
# 文件里：键/字符串带双引号，分数是光秃秃的（真正的 JSON 数字）。

# D5 —— report.py
import csv, statistics, sys

if len(sys.argv) != 2:                     # argv[0] 是 report.py 自己
    sys.exit("Usage: python3 report.py <file.csv>")

with open(sys.argv[1], newline="", encoding="utf-8") as f:
    scores = [int(r["score"]) for r in csv.DictReader(f)]
print(f"n={len(scores)}  mean={statistics.mean(scores):.1f}")

# D6
from PIL import Image
from pathlib import Path

a = Image.new("RGB", (60, 60), "steelblue")
b = Image.new("RGB", (60, 60), "goldenrod")
a.save("pulse.gif", save_all=True, append_images=[b], duration=400, loop=0)
print(Path("pulse.gif").stat().st_size, "bytes")   # 几百字节 —— 小，但是真二进制
```

### 课后作业

```python
# H1
import csv

with open("attendance.csv", newline="") as f:
    rows = list(csv.DictReader(f))

report = []
for r in rows:
    marks = []
    for key in list(r)[1:]:            # "name" 之后的每一列
        try:
            marks.append(int(r[key]))
        except ValueError:
            pass                       # 跳过脏单元格——但按无效计
    rate = sum(marks) / len(marks) if marks else 0.0
    report.append({"name": r["name"], "rate": round(rate, 2), "n_valid": len(marks)})

with open("attendance_report.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["name", "rate", "n_valid"])
    w.writeheader()
    w.writerows(report)

# H2
import json

original = {"q1": 4.2, "q2": 3.8, "all_valid": False}
with open("summary.json", "w") as f:
    json.dump(original, f, indent=2)
with open("summary.json") as f:
    loaded = json.load(f)
print(loaded == original)   # True —— 而文件里 Python 的 False 写成了 JSON 的
                            # false（小写）：JSON 是另一门语言。
```

H3 —— 是套路，不是标准答案：`with` 里 `rows = list(csv.DictReader(f))`，
`len(rows)` 数行数，选一个数字列过 `to_int`/`to_float` 清洗后求均值。
第一个脏值和它抛的异常写进你的 bug 日志。
