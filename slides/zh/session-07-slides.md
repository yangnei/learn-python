---
marp: true
title: "第 7 课 — 异常与防御式编程"
paginate: true
---

# 第 7 课
## 异常与防御式编程

---

## try / except

```python
try:
    n = int(value)
except ValueError:
    n = None        # 处理坏情况
```

代码可能在运行时失败，就包起来。`except` 捕获指定名字的错误。
`try` 块要保持**小**——只放可能失败的那一行——这样捕获就不会
误伤你本没打算原谅的代码。

`except ValueError: pass` 是最小化处理——一次*看得见的、故意的*"跳过"。
真要跳过时没问题；但凡你可能会问"跳过了什么？"，就改成记日志。

---

## 常见异常类型

| 异常 | 何时发生 |
|---|---|
| `ValueError` | 类型对、值不行：`int("N/A")` |
| `TypeError` | 类型不对：`5 > "5"` |
| `KeyError` | 字典缺键：`d["nope"]` |
| `IndexError` | 列表下标越界：`xs[99]` |
| `ZeroDivisionError` | `x / 0` |
| `FileNotFoundError` | `open("missing.csv")` |

---

## try / except / else / finally

```python
try:
    n = int(value)
except ValueError:
    print("not a number")
else:
    print("ok:", n)      # 仅当没有异常时
finally:
    print("always runs")  # 收尾清理
```

---

## 主动抛出

```python
def clean_likert(n):
    if not 1 <= n <= 5:
        raise ValueError(f"{n} not in 1–5")
    return n
```

`raise` 是有意抛出异常——如何处理交给调用者决定。

---

## EAFP vs LBYL

```python
# LBYL —— "三思而后行"
if value.isdigit():
    n = int(value)

# EAFP —— "先斩后奏"（Pythonic）
try:
    n = int(value)
except ValueError:
    n = None
```

两者都合法。当"事先检查"困难或有竞态时，EAFP 更亮眼。

---

## assert（开发者检查，不是输入校验）

```python
assert len(scores) > 0, "scores must not be empty"
```

给*你自己*开发时做的合理性检查。它可以被关闭（`python -O`），
所以**绝不要**用 `assert` 校验不可信输入——用 `raise`。

---

## 第一个 pytest 测试

```python
# clean.py
def clean_likert(n):
    if not 1 <= n <= 5:
        raise ValueError("1–5 only")
    return n

# test_clean.py
import pytest
from clean import clean_likert

def test_valid():    assert clean_likert(3) == 3
def test_invalid():
    with pytest.raises(ValueError):
        clean_likert(9)
```
运行：`pytest`

---

## 轮到你了

`examples/session-07/practice.md`：
1. `safe_int(value)`：返回 int 或 None。
2. 清洗一列脏问卷数据：收集有效值 + 一份拒收记录。
3. 写一个 `pytest` 测试。

---

# 更进一步
## 更稳健的程序

---

## 异常家族树

```text
Exception
 ├── ValueError        ├── KeyError / IndexError (LookupError)
 ├── TypeError         └── OSError (FileNotFoundError, ...)
```

```python
try:
    n = int(raw)
except (ValueError, TypeError):   # 一次捕获多个具体异常
    ...
```

**顺序很重要**：`except` 子句自上而下匹配——先具体、后宽泛；末尾的
`except Exception as e:` 只用来记录并停止，绝不用来无视。

---

## 携带证据的自定义异常

```python
class SurveyError(ValueError):
    def __init__(self, value, message):
        super().__init__(message)
        self.value = value            # 把证据留下

raise SurveyError(raw, f"{raw!r} is not a 1-5 rating")
```

调用者可以专门捕 `SurveyError`——也可以宽泛地捕 `ValueError`——
并且仍能看到*哪个*值出的问题。

---

## `raise ... from`——留住起因

```python
try:
    n = int(cell)
except ValueError as e:
    raise SurveyError(cell, "bad rating cell") from e
```

回溯信息会**两层都显示**：上面是你的领域级错误，下面是真正的底层起因。
凌晨调试的未来的你会感谢现在的你。

---

## `finally` 与清理思维

```python
try:
    f = open("data.csv")
    ...
finally:
    f.close()        # 无论上面发生什么都会运行
```

`with open(...)`（第 8 课）正是这套模式的成品包装。法则：谁申请资源，
谁保证释放。

---

## 诊断信息，`logging` 胜过 `print`

```python
import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logging.info("processing %s rows", len(rows))
logging.warning("rejected %r: out of range", raw)
```

- `print` 输出程序的*结果*；`logging` 记录程序的*日记*。
- 级别（`DEBUG/INFO/WARNING/ERROR`）让你不删代码就能调低音量。

---

## pytest，进阶版

```python
import pytest
from clean import clean_likert

@pytest.mark.parametrize("bad", ["3", True, None, 0, 9])
def test_rejects(bad):
    with pytest.raises(ValueError):
        clean_likert(bad)
```

一个测试、五个输入、五条独立报告。套路：**准备、执行、断言**——
并且测*边界*（临界值、错误类型），而不是舒适区。

只会 `print` 的函数没法断言。让函数**返回**值、在边缘处打印——
这才是可测试的代码（第 5 课 `return` vs `print` 的回报）。

---

## 轮到你了——第二轮

`examples/session-07/practice.md` → **In class — going deeper**：
修一个 except 顺序 bug、写带 `raise ... from` 的 `SurveyError`、
把拒收记录换成 `logging`，以及参数化你的测试。

---

## 陷阱回顾

- **绝不**裸写 `except:`——写明异常名。
- 别捕得太宽，别悄悄吞掉错误。
- `assert` ≠ 输入校验（用 `raise`）。
- 捕你*预料中*的那个具体错误。

## 小结
你已经能校验脏输入，并在该失败时大声失败。
**下一课：** 第 8 课——文件与研究数据。

---

## 课后作业（第 8 课之前）

*课外完成——不计入课堂时间。完整题目 + 参考答案：`examples/session-07/practice.md` → **Homework**。*

1. **`ask_int(prompt, lo, hi)`** —— 用 EAFP 重写第 3 课的输入校验循环。
2. **再加三个 pytest 用例** —— `clean_likert` 的边界情况（`True`、`"3"`、`None`）。
3. **报错分诊** —— 五条真实报错信息：说出异常类名和修法。
