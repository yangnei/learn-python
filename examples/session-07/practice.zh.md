# 第 7 课 —— 练习：异常与防御式编程

每个答案都自己敲一遍。**运行之前先预测输出。** 参考答案在最后。

## 课堂练习

### 任务 1 —— `safe_int`
写 `safe_int(value)`：返回 `int(value)`，失败时返回 `None`。用
`"42"`、`"N/A"`、`""`、`None`、`3.0` 测试。

### 任务 2 —— 清洗一列问卷数据
给定 `raw = ["5","3","N/A","7","","1","two","4"]`，产出：
- `clean` —— 有效的李克特整数（1–5）列表，以及
- `rejected` —— `(值, 原因)` 对的列表。
用一个对越界或非整数**抛出** `ValueError` 的 `clean_likert(n)` 来实现。

### 任务 3 —— 写一个测试
把 `clean_likert` 放进 `clean.py`，用 pytest 写 `test_clean.py`：
一个通过用例 + 一个 `pytest.raises(ValueError)` 用例。运行 `pytest`。

### 任务 4 —— 讨论
裸 `except:` 为什么危险？举一个它会藏起来、而你更想看到的错误。

### 加餐 —— Python 惯用法速练
盖住 `# ->` 后面的答案，逐行预测，再运行。

```python
class LikertError(ValueError):       # 你自己的异常类型
    pass
print(issubclass(LikertError, ValueError))   # -> True （所以 except ValueError 也接得住）

try:
    assert 1 == 2, "values differ"   # assert：廉价的内部自检
except AssertionError as e:
    print(e)                         # -> values differ
```

## 课堂练习——更进一步（第二小时）

### E1 —— 哪个异常？
不运行，说出每个会抛什么异常：
`int("3.5")` · `{"a": 1}["b"]` · `[1, 2][5]` · `1/0` · `open("nope.csv")` · `len(42)`

### E2 —— 你自己的异常
定义 `class SurveyError(ValueError)`，对越界的李克特值抛出它。证明
`except ValueError:` 仍然接得住——这就是子类化在起作用。

### D1 —— 修好 except 顺序
这段对坏单元格永远打印 `"unexpected"`——为什么？怎么修？
```python
try:
    n = int(cell)
except Exception:
    print("unexpected")
except ValueError:
    n = None
```

### D2 —— 携带证据的 `SurveyError`
写 `class SurveyError(ValueError)`，把出错的值存进 `.value`。在清洗循环里接住
`int()` 的底层 `ValueError`，用 `raise SurveyError(cell, ...) from e` 重新抛出。
展示一次两层的回溯。

### D3 —— 记日志，别打印
把你的拒收记录换成 `logging`：每个被拒的单元格 `logging.warning`，最终统计
`logging.info`。把格式配置成显示级别名。

### D4 —— 参数化
把三个作业测试改写成**一个** `@pytest.mark.parametrize` 测试，覆盖
`["3", True, None, 0, 9]`。运行 `pytest -q`。

## 课后作业（第 8 课之前）

*约 30–45 分钟，课外完成——不计入课堂时间。先都试一遍，再看答案。*

### H1 —— `ask_int(prompt, lo, hi)`
用 EAFP 重写第 3 课的输入校验循环：用 `try: n = int(raw)` /
`except ValueError` 替代 `.isdigit()`——这样 `"-5"` 和 `" 42 "` 也能处理。
循环到输入有效为止；返回整数。

### H2 —— 再加三个 pytest 用例
给 `clean_likert` 补测试：`clean_likert(True)` 要抛错（布尔不是评分！）、
`clean_likert("3")` 要抛错（字符串，哪怕是数字样子）、`clean_likert(None)` 要抛错。
运行 `pytest -q` 直到全绿。

### H3 —— 报错分诊
对每条信息，说出异常类名和一行修法：
1. `invalid literal for int() with base 10: 'N/A'`
2. `unsupported operand type(s) for +: 'int' and 'str'`
3. `'score'`（来自字典查询）
4. `division by zero`
5. `[Errno 2] No such file or directory: 'survy.csv'`

---

## 参考答案

### 课堂练习

```python
def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def clean_likert(n):
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError(f"{n!r} not an int")
    if not 1 <= n <= 5:
        raise ValueError(f"{n} outside 1–5")
    return n

raw = ["5","3","N/A","7","","1","two","4"]
clean, rejected = [], []
for r in raw:
    try:
        clean.append(clean_likert(safe_int(r)))
    except ValueError as e:
        rejected.append((r, str(e)))
print(clean)      # [5, 3, 1, 4]
print(rejected)   # [('N/A', ...), ('7', ...), ('', ...), ('two', ...)]
```

```python
# test_clean.py
import pytest
from clean import clean_likert
def test_ok():   assert clean_likert(3) == 3
def test_bad():
    with pytest.raises(ValueError):
        clean_likert(9)
```

任务 4：裸 `except:` 连 `KeyboardInterrupt`（Ctrl+C）和你自己笔误产生的
`NameError` 都会接住——拼错的变量名会被悄悄吞掉，你永远看不到那个 bug。
永远只接你预料中的那个具体异常。

### 课堂练习——更进一步

```python
# E1
int("3.5")        # ValueError          （int() 只解析整数文本）
{"a": 1}["b"]     # KeyError
[1, 2][5]         # IndexError
1 / 0             # ZeroDivisionError
open("nope.csv")  # FileNotFoundError
len(42)           # TypeError           （整数没有长度）

# E2
class SurveyError(ValueError):
    pass

def clean_likert(n):
    if not 1 <= n <= 5:
        raise SurveyError(f"{n} outside 1-5")
    return n

try:
    clean_likert(9)
except ValueError as e:      # 父类接得住子类
    print("caught:", e)

# D1 —— except 子句自上而下匹配；Exception 是 ValueError 的父类，
# 放在前面就先命中，具体的处理器永远轮不到。先具体、后宽泛：
try:
    n = int(cell)
except ValueError:
    n = None
except Exception as e:
    print("unexpected:", e)
    raise

# D2
class SurveyError(ValueError):
    def __init__(self, value, message):
        super().__init__(message)
        self.value = value

def clean_cell(cell):
    try:
        n = int(cell)
    except ValueError as e:
        raise SurveyError(cell, f"{cell!r} is not a rating") from e
    return n
# 回溯里下层是起因 ValueError，上层是 SurveyError。

# D3
import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
kept, rejected = [], []
for cell in ["5", "N/A", "3", ""]:
    try:
        kept.append(clean_cell(cell))
    except SurveyError as e:
        rejected.append(e.value)
        logging.warning("rejected %r", e.value)
logging.info("kept %d, rejected %d", len(kept), len(rejected))

# D4 —— test_clean.py
import pytest
from clean import clean_likert

@pytest.mark.parametrize("bad", ["3", True, None, 0, 9])
def test_rejects(bad):
    with pytest.raises(ValueError):
        clean_likert(bad)
```

### 课后作业

```python
# H1
def ask_int(prompt, lo, hi):
    while True:
        raw = input(prompt)
        try:
            n = int(raw)                 # EAFP：直接试转换
        except ValueError:
            print("A whole number, please.")
            continue
        if lo <= n <= hi:
            return n
        print(f"Between {lo} and {hi}, please.")

# H2 —— test_clean.py
import pytest
from clean import clean_likert

def test_bool_rejected():
    with pytest.raises(ValueError):
        clean_likert(True)

def test_str_rejected():
    with pytest.raises(ValueError):
        clean_likert("3")

def test_none_rejected():
    with pytest.raises(ValueError):
        clean_likert(None)
```

H3 —— 分诊：
1. `ValueError` —— 先清洗/转换，或包进 `try/except ValueError`。
2. `TypeError` —— 转换其中一边：`str(n)` 或 `int(s)`。
3. `KeyError` —— 用 `row.get("score")`，或检查表头拼写。
4. `ZeroDivisionError` —— 除之前先挡住空数据的情况。
5. `FileNotFoundError` —— 文件名拼错了（`survey.csv`）；用 `Path(...).exists()` 检查。
