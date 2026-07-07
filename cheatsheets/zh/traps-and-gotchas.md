# Python 陷阱与坑 —— 主速查表

> 咬新手（也咬不少老手）的语言怪癖。以下每个行为都在 CPython 3.11+ 上实际运行并
> 验证过。看**惊讶**一栏、盖住**原因/修法**，先预测。
> 整门课程都把它开着。

---

## 1 — 相等 `==` vs 同一 `is`  *(第 2 课)*

| 表达式 | 结果 | |
|---|---|---|
| `a = [1,2]; b = [1,2]; a == b` | `True` | **值**相同 |
| `a = [1,2]; b = [1,2]; a is b` | `False` | 内存中是不同的**对象** |
| `a = [1,2]; b = a; a is b` | `True` | `b` 是*同一个*对象（别名） |

- **`==`** 问"值相同吗？"——几乎永远是你想要的。
- **`is`** 问"是同一个对象吗？"——**只**用于 `None`、`True`、`False`：
  ```python
  if x is None:        # ✅ 正确
  if x == None:        # ⚠️ 能跑，但不地道 —— 用 `is`
  ```
- **身份的小怪癖（千万别依赖）：** CPython 缓存小整数（−5 到 256）并驻留部分字符串，
  所以 `a = 256; b = 256; a is b` 为 `True`，到 `257` 就可能是 `False`。
  这是实现细节。**比值，永远用 `==`。**

🧠 *桥接：* GPA 相同的两名学生是 `==`；同一名学生才是 `is`。

---

## 2 — 布尔值就是整数  *(第 2 课)*

```python
True == 1            # True   （bool 是 int 的子类）
False == 0           # True
5 + True             # 6      对，布尔值能做算术
sum([True, False, True])   # 2   ← 数出 True 的个数
isinstance(True, int)      # True
type(True) is int          # False  （它的类型是 bool，一个子类型）
```
- **善用它：** `sum(conditions)` 是数"多少个为真"的 Python 惯用法。
- **陷阱：** 尽管 `True == 1`，`True is 1` 却是 `False`（不同对象）。用 `==` 比较。

🧠 *桥接：* 这就是语言内置的哑变量编码（1/0）——对标志求和就是在数个案。

---

## 3 — 浮点精度  *(第 2 课)*

```python
0.1 + 0.2            # 0.30000000000000004
0.1 + 0.2 == 0.3     # False  😱
```
- **原因：** 小数以二进制存储；大多数小数无法精确表示。不是 Python 的 bug——每门语言都这样。
- **修法：**
  ```python
  import math
  math.isclose(0.1 + 0.2, 0.3)     # True   ← 用容差比较浮点数
  round(0.1 + 0.2, 2) == 0.3       # True   ← 或者取整后展示/比较
  from decimal import Decimal       # 真正需要时用精确十进制（金钱、成绩）
  Decimal("0.1") + Decimal("0.2")  # Decimal('0.3')
  ```
- **法则：** 永远不要用 `==` 检验计算出的浮点数。用 `math.isclose`（或 `round`）。

🧠 *桥接：* 你本来就从不对两个测量分数做精确相等判断——直觉相同，原因换了
（二进制存储，不是测量误差）。

---

## 4 — 跨类型比较  *(第 2 课)*

```python
5 == "5"     # False   （类型不同 → 不相等，但不报错）
5 == 5.0     # True    （int 与 float 按数值比较）
5 > "5"      # 💥 TypeError: '>' not supported between 'int' and 'str'
```
- 不相干类型之间的**相等（`==`/`!=`）** → 直接 `False`，从不崩溃。
- 不兼容类型之间的**排序（`<`、`>`、`<=`、`>=`）** → **`TypeError`**。
- **修法：** 先转换。`int("5") == 5` → `True`。排序前用 `isinstance` 把关。

🧠 *桥接：* 计算机能跨类型回答"是不是一样？"，却无法给文本和数字*排名*——它们没有共同量尺。

---

## 5 — 序列逐元素比较  *(第 2 / 4 课)*

```python
[1, 2] == [1, 2]     # True
[1, 2] == (1, 2)     # False   ← 列表 vs 元组：类型不同，永不相等
(1, 2) < (1, 3)      # True    ← 逐位置比较（字典序）
"apple" < "banana"   # True    ← 字符串逐字符比较（近似字母序）
[1, 2] < [1, 2, 3]   # True    ← 前缀算"小于"
```
- **陷阱：** 内容完全相同的 `list` 和 `tuple` **永远不 `==`**——类型有一票否决权。
- 列表/元组/字符串从左到右比较；第一个不同的元素定胜负。

---

## 6 — 真值判断（什么算 False）  *(第 2 / 3 课)*

```python
# 这些都是"假值"：
bool(0) bool(0.0) bool("") bool([]) bool({}) bool(set()) bool(None)   # 全是 False
bool("0")   # True！ ← 非空字符串是真值，"0" 也不例外
bool([0])   # True   ← 非空列表是真值，哪怕装的是个 0
```
- **惯用法：** 直接判断"空不空"——`if scores:` 而不是 `if len(scores) > 0:`；
  `if name:` 而不是 `if name != "":`。
- **陷阱：** 字符串 `"0"` 和 `"False"` 都是**真值**。用户输入先转换再判断。

---

## 7 — `and` / `or` 返回操作数，不是布尔值  *(第 3 课)*

```python
5 and 0      # 0      （and → 第一个假值，否则最后一个值）
0 or "hi"    # "hi"   （or → 第一个真值，否则最后一个值）
"" or "N/A"  # "N/A"  ← 顺手的默认值惯用法
```
- **善用它：** `name = user_input or "Anonymous"` 提供默认值。
- **陷阱：** 别写 `if x == True`，直接 `if x:`。另外 `and`/`or` 短路——右侧可能
  根本不运行，别把副作用藏在那里。

---

## 8 — 可变默认参数  *(第 5 课)* —— 大名鼎鼎的那个

```python
def add_student(name, roster=[]):     # ❌ 危险
    roster.append(name)
    return roster

add_student("Ana")     # ['Ana']
add_student("Ben")     # ['Ana', 'Ben']  😱  默认列表跨调用一直存在
```
- **原因：** 默认的 `[]` 只在函数*定义*时创建**一次**，之后每次调用都复用它。
- **修法：**
  ```python
  def add_student(name, roster=None):   # ✅
      if roster is None:
          roster = []
      roster.append(name)
      return roster
  ```
- **法则：** 永远不要用可变默认值（`[]`、`{}`、`set()`）。用 `None`，在函数体内创建。

---

## 9 — 别名：变量是标签，不是盒子  *(第 4 课)*

```python
a = [1, 2, 3]
b = a            # b 是同一个列表，不是副本
a.append(4)
b                # [1, 2, 3, 4]  😱  b 也变了

b = a.copy()     # ✅ 现在 b 是独立的（浅）副本
import copy
b = copy.deepcopy(a)   # ✅ 连嵌套的列表/字典也独立
```
- **陷阱：** `grid = [[0] * 3] * 3` 造出**同一行的三个引用**——改 `grid[0][0]` 三行全变。
  要用 `[[0]*3 for _ in range(3)]`。
- **法则：** 赋值从不复制。`=` 只是给同一个对象再绑一个名字。

🧠 *桥接：* 变量是贴在对象上的便利贴，不是装着值的容器。

---

## 10 — `type()` vs `isinstance()`  *(第 2 课)*

```python
isinstance(x, int)              # ✅ 地道；尊重继承
isinstance(x, (int, float))     # ✅ "x 是某种数字吗？"
type(x) is int                  # 只认精确类型；很少是你要的
type(x) == int                  # 能跑，但类型身份请用 `is`
```
- **陷阱：** `isinstance(True, int)` 为 `True`（bool 是 int 的子类型）。必须排除布尔时，
  用 `type(x) is int` 或 `isinstance(x, int) and not isinstance(x, bool)`。

---

## 11 — 整数除法 vs 浮点除法  *(第 1 / 2 课)*

```python
7 / 2      # 3.5   真除法永远返回浮点数
7 // 2     # 3     整除（向 −∞ 取整）
-7 // 2    # -4    ← 是向下取整，不是向零截断！
7 % 2      # 1     取余 —— 用 % 2 判断奇偶
7 / 0      # 💥 ZeroDivisionError
```
- **陷阱：** `/` 即使结果是整数也给浮点数（`4 / 2` 是 `2.0`）。要整数结果用 `//`。

---

## 12 — 字符串不可变；有些方法*返回*而不*修改*  *(第 1 / 9 课)*

```python
s = "  Hello  "
s.strip()          # "Hello"   ← 返回一个新字符串
s                  # "  Hello  "  ← s 原封不动
s = s.strip()      # ✅ 想留住结果就赋回去
```
- **陷阱：** `s.strip()` / `s.replace(...)` / `s.upper()` 对 `s` 毫无作用，除非重新赋值。
- 对比：列表方法如 `.append()`/`.sort()` **就地**修改并返回 `None`：
  ```python
  nums = [3, 1, 2]
  nums = nums.sort()    # ❌ nums 现在是 None！ .sort() 返回 None
  nums.sort()           # ✅ 就地排序；想要新列表用 sorted(nums)
  ```

---

## 13 — `range` 不含终点；差一错误  *(第 3 课)*

```python
list(range(1, 5))      # [1, 2, 3, 4]   ← 不包含 5
list(range(5))         # [0, 1, 2, 3, 4]
list(range(0, 10, 2))  # [0, 2, 4, 6, 8]
```
- **法则：** `range(a, b)` 是半开区间 `[a, b)`。

---

## 14 — 边遍历边修改列表  *(第 3 课)*

```python
xs = [1, 2, 3, 4]
for x in xs:
    if x % 2 == 0:
        xs.remove(x)     # ❌ 跳元素 / 行为不可预测
# ✅ 遍历副本，或构建新列表：
xs = [x for x in xs if x % 2 != 0]
```

---

## 15 — 文件：`"w"` 会覆盖；游标会耗尽  *(第 8 课)*

```python
open("data.csv", "w")    # ❗ 立即把文件清空
open("data.csv", "a")    # 追加
open("data.csv", "r")    # 读取（默认）

with open("data.csv") as f:
    rows = f.readlines()      # 读了一遍
    again = f.readlines()     # [] —— 游标已在文件末尾
```
- 永远优先 `with open(...) as f:` —— 即使代码崩溃也会把文件关好。
- Windows 上配合 `csv` 模块，打开时带 `newline=""` 以免出现空行。

---

## 16 — 正则：`.` 匹配*一切*；用原始字符串  *(第 9 课)*

```python
import re
re.search(r"\d+", "id 42")     # 用 r"..." 免得 \d 被当成 Python 转义
re.search(".", "a.b")          # 这个 "." 匹配到的是 "a"，不只是点！
re.search(r"\.", "a.b")        # 想要真正的点用 \.
```
- **法则：** 模式永远写成原始字符串 `r"..."`。转义 `. ^ $ * + ? ( ) [ ] { } | \`。

---

## 快速"先预测再运行"自测（盖住答案）
```python
print(True + True)            # 2
print(3 == 3.0)               # True
print(0.1 + 0.2 == 0.3)       # False
print(5 == "5")               # False
print([1,2] == (1,2))         # False
print(bool("0"))              # True
print(7 // 2, -7 // 2)        # 3 -4
x = [1]; y = x; x.append(2); print(y)   # [1, 2]
```
八道题的*为什么*都能讲清，你就掌握了多数新手漏掉的根基。
