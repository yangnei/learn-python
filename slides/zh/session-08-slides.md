---
marp: true
title: "第 8 课 — 文件、库与研究数据"
paginate: true
---

# 第 8 课
## 文件、库与研究数据

---

## 用 `with` 打开文件

```python
with open("notes.txt") as f:
    text = f.read()
# 到这里文件自动关闭，即使代码崩了也一样
```

`with` = 上下文管理器：替你搭好、拆好资源。
永远优先用它，而不是裸的 `open()`/`close()`。

---

## 文件模式（当心陷阱）

| 模式 | 含义 |
|---|---|
| `"r"` | 读取（默认） |
| `"w"` | 写入 —— **先把文件清空！** |
| `"a"` | 追加 |
| `"r+"` | 读 + 写 |

⚠️ 用 `"w"` 打开了不该动的文件 → 内容瞬间蒸发。

```python
with open("log.txt", "a") as f:       # 追加：写到末尾，绝不清空
    f.write("cleaned survey.csv\n")   # 写入时 \n 由你自己负责
```

（`"rb"`/`"wb"` 读写**二进制**——图片、PDF。默认是文本模式。）

---

## 读取文本

```python
with open("notes.txt") as f:
    whole = f.read()           # 一整个大字符串
    # 或者
    for line in f:             # 逐行读（省内存）
        print(line.rstrip())
```

⚠️ 文件对象读完一遍就"耗尽"了——想再读要重新打开。

---

## 读 CSV：每行一个字典 🧠

```python
import csv
with open("students.csv", newline="") as f:
    for row in csv.DictReader(f):
        print(row["name"], row["score"])   # row 是以表头为键的字典
```

`csv.DictReader` 把每一行变成字典——正是第 4 课的"字典列表"数据集。
（`newline=""` 防止 Windows 上出现空行。）

你*可以*自己用 `.split(",")` 拆行——直到某个字段里也有逗号。
这个问题，加上引号和表头，就是 `csv` 存在的理由。

---

## 写 CSV

```python
with open("summary.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["name", "score"])
    w.writeheader()
    w.writerow({"name": "Ana", "score": 91})
```

---

## 研究者常用的库

```python
import statistics
statistics.mean(xs); statistics.median(xs); statistics.stdev(xs)

import random
random.choice(xs); random.randint(1, 6); random.shuffle(xs)

from datetime import date
date.today()

from pathlib import Path
Path("students.csv").exists()
```

```python
# pip install cowsay          # PyPI 上有约 50 万个包
import cowsay
cowsay.cow("pip install anything")
```

`pip install <名字>`，然后 `import`——第三方库的全部故事就这么多。
（对，连搞笑的包也有：重点是安装易如反掌。）

---

## 轮到你了

`examples/session-08/practice.md`（用到 `survey.csv`）：
1. 读 `students.csv`；用 `statistics.mean` 打印全班平均分。
2. 计算问卷各题的均值；写出 `survey_summary.csv`。

---

# 更进一步
## 真实的数据工作

---

## `pathlib`，完整巡礼

```python
from pathlib import Path
data = Path("data")
f = data / "students.csv"          # / 拼接路径，任何系统都行
f.exists(), f.stat().st_size       # 存在吗？多大？
list(data.glob("*.csv"))           # 这里的每个 CSV
list(data.rglob("*.csv"))          # ……连同所有子文件夹里的
data.mkdir(exist_ok=True)
notes = f.with_suffix(".txt").read_text()   # 小文件：一行搞定
```

---

## 编码（Excel 之坑）

```python
open("survey.csv", newline="", encoding="utf-8")        # 明说出来
open("from_excel.csv", newline="", encoding="utf-8-sig") # 吃掉 Excel 的 BOM
```

- 乱码（`é` 变 `Ã©`）= 字节被用错误的编码读了。
- Excel 常存成 `cp1252` 或带 BOM 的 UTF-8——后者用 `utf-8-sig` 处理。

---

## `csv`，进阶版

```python
csv.reader(f)        # 每行是列表（没有表头/表头重复时用）
csv.DictReader(f)    # 每行是字典（默认首选）
w.writerows(report)  # 一次写入多个字典
csv.DictReader(f, delimiter=";")   # 欧洲版 Excel 导出
```

---

## 嵌套数据用 JSON

```python
import json
snapshot = {"course": "ED101",
            "items": {"q1": {"mean": 4.2, "n": 28}, "q2": {"mean": 3.8, "n": 27}}}
Path("snapshot.json").write_text(json.dumps(snapshot, indent=2))
back = json.loads(Path("snapshot.json").read_text())
```

CSV 是矩形的；JSON 能嵌套。`True/None` 会写成 `true/null`——JSON 是
另一门语言，`json.load` 负责翻译回来。

---

## API：同样的 JSON，来自网络*（尝一口）*

```python
# pip install requests
import requests

r = requests.get("https://itunes.apple.com/search",
                 params={"term": "python", "media": "ebook", "limit": 3})
data = r.json()                     # 响应体，解析成字典/列表
for item in data["results"]:
    print(item["trackName"])
```

所谓"调用 API"不过是：请求一个 URL，解析它的 JSON——同一套 `json`
本领，换了个来源。（需要联网；本课程立足离线文件。）

---

## `datetime`——日期也是数据

```python
from datetime import date, datetime
d = datetime.strptime("2026-07-06", "%Y-%m-%d")   # 解析文本 -> datetime
d.strftime("%b %d")                                # 格式化 -> "Jul 06"
(date(2026, 7, 6) - date(2026, 1, 5)).days         # 182 —— 日期能做算术
date.fromisoformat("2026-07-06")                   # ISO 快捷方式
```

`strptime` = *解析*（字符串 → 日期），`strftime` = *格式化*（日期 → 字符串）。

---

## `random`，可复现版

```python
import random
random.seed(42)                 # 每次运行同样的"随机" —— 方法部分狂喜
random.choice(roster)           # 抽一个
random.sample(roster, 3)        # 抽三个，不重复
random.shuffle(order)           # 就地打乱 —— 随机分组
```

设了种子，随机分析就**可复现**——重跑脚本会抽出同一批样本。

---

## 带参数的脚本：`sys.argv`

```python
# report.py —— 运行方式：python3 report.py survey.csv
import sys

if len(sys.argv) != 2:                    # argv[0] 是脚本自己的名字
    sys.exit("Usage: python3 report.py <file.csv>")
filename = sys.argv[1]
```

- `sys.argv` 是命令行给的**字符串列表**——可以 `len()`、可以切片
  （`sys.argv[1:]` = 真正的参数）。
- 先设防、再信任：缺参数就是一个待爆的 `IndexError`；
  `sys.exit("提示")` 会停止程序并打印用法。
- 选项多起来（`--top 5 --verbose`）就升级到标准库的 `argparse`。

---

## 二进制文件实战：用 Pillow 处理图片

```python
# pip install pillow
from PIL import Image

before = Image.open("chart_2025.png")     # 二进制文件，解码成像素
after = Image.open("chart_2026.png")
before.save("growth.gif", save_all=True,
            append_images=[after],        # 多帧 -> 动图 GIF
            duration=500, loop=0)         # 每帧毫秒数；0 = 无限循环
```

- 文本模式把字节解码成字符；**二进制**格式（图片、PDF）需要懂行的库——
  图片这行的专家是 Pillow。
- 三个调用 = 一张结果图表的"前后对比"动图，直接进幻灯片。

---

## pandas 预告，加长版

```python
import pandas as pd
df = pd.read_csv("students.csv")
df["score"].describe()                    # 计数/均值/标准差/四分位
df.groupby("major")["score"].agg(["mean", "count"])
df[df["score"] < 60]                      # 筛选行
df.to_csv("report.csv", index=False)
```

五行 = 今天一整课。那是下一门课——而现在你知道每一行底下发生了什么。

---

## 轮到你了——第二轮

`examples/session-08/practice.md` → **In class — going deeper**：
`pathlib` 盘点、报名日期的日期运算、带种子的抽样，以及 CSV → JSON。

---

## 陷阱回顾

- `"w"` 会不声不响地覆盖——确认清楚文件名。
- 用 `csv` 模块 → 打开时带 `newline=""`。
- 文件读一遍就耗尽；重读要重新打开。
- 非 ASCII 文本记得指定 `encoding="utf-8"`。

## 小结
你已经能加载、汇总并写出真实的研究数据。
**下一课：** 第 9 课——正则表达式与文本清洗。

---

## 课后作业（第 9 课之前）

*课外完成——不计入课堂时间。完整题目 + 参考答案：`examples/session-08/practice.md` → **Homework**。*

1. **出勤报告** —— 读入、清洗、汇总、写出 CSV——完整管道。
2. **JSON 往返** —— 用 `json.dump` 保存汇总，读回来，验证相等。
3. **你自己的数据** —— 把这条管道对准你研究中的任意一个 CSV。
