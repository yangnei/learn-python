"""Chinese translations of every trap's "why" explanation, keyed by (session, index).

The trap code and its evaluated result are language-neutral (they ARE the Python);
only the explanation is translated. Index is the 0-based position within
traps.TRAPS[session] — keep in step with tools/traps.py.
"""

WHY_ZH: dict[tuple[int, int], str] = {
    # ---- Session 1 ----
    (1, 0): "这两个是字符串（`input()` 给的永远是字符串）：`+` 拼接文本。先转换：`int(score) + int(bonus)`。",
    (1, 1): "文本和数字不能用 `+` 粘在一起。用 f-string——`f\"Age: {age}\"`——或 `print('Age:', age)`。",
    (1, 2): "`int()` 向零截断，不做四舍五入。想四舍五入用 `round(gpa)`。",
    (1, 3): "字符串不可变：`.upper()` **返回**新字符串，原来的不动。要赋回去：`name = name.upper()`。",
    # ---- Session 2 ----
    (2, 0): "`==` 比较**值**（`ana_scores == ben_scores` 为 True）；`is` 比较**身份**——是否是内存中的同一个对象。Ana 和 Ben 的列表只是恰好相同。比值用 `==`，`is` 留给 `None`。",
    (2, 1): "`backup = roster` 不会复制：两个名字指向同一个列表，通过 `roster` 追加也会在 `backup` 里出现。复制用 `list(roster)` 或 `roster[:]`。",
    (2, 2): "`bool` 是 `int` 的子类：`True == 1`、`False == 0`——这正是电子表格里的 1/0 与 Python 的 True/False 对得上的原因。",
    (2, 3): "算术中 `True` 相当于 `1`（`False` 相当于 `0`）——给标志加一分的快捷方式。",
    (2, 4): "对布尔值求和就是数 `True` 的个数——统计多少学生通过的顺手办法。",
    (2, 5): "浮点数按二进制存储，0.1 和 0.2 都没有精确表示，小误差累加了。",
    (2, 6): "因为 `0.1 + 0.2` 是 `0.30000000000000004`。永远别用 `==` 检验计算出的分数；用 `math.isclose(a, b)`。",
    (2, 7): "`NaN`（缺失/无效的数）定义为不等于任何东西，连自己都不等于。用 `math.isnan(x)` 检测。",
    (2, 8): "`/` 永远是浮点（真）除法，所以平均值算出来是 `3.5`。想要整数用 `//`。",
    (2, 9): "`//` 向负无穷取整，不是向零，所以 `-7 // 2 == -4`（每人扣 4 分，不是 3 分）。",
    (2, 10): "Python 不做文本/数字的自动转换，CSV 里的字符串和数字就是不相等（也不报错）。先转换：`int(score) == 5`。",
    (2, 11): "数字和文本排大小会抛 TypeError——不存在合理的顺序。先转换：`5 > int(score)`。",
    (2, 12): "列表永远不等于元组，内容一样也不行。",
    (2, 13): "`type()` 是精确匹配，而 `passed` 的类型是 `bool`，不是 `int`。要认子类就用 `isinstance`。",
    (2, 14): "`isinstance` 尊重子类关系，而 `bool` 确实**是**一种 `int`。",
    (2, 15): "任何**非空**字符串都是真值，包括 '0' 和 'False'。只有空字符串是假值——所以问卷文本要先转换再判断。",
    (2, 16): "空容器（`[]`、`{}`、`''`、`0`、`None`）都是假值，所以 `if submissions:` 读作\"有没有内容？\"。",
    (2, 17): "CPython 预缓存了小整数（-5..256），在那个范围里 `is` 会碰巧看似 True；运行时构造的 257 是两个不同对象。比值永远用 `==`，绝不用 `is`。",
    # ---- Session 3 ----
    (3, 0): "`or` 返回第一个真值**操作数**（否则返回最后一个），`and` 返回第一个假值——不是布尔值。这就是默认值惯用法。",
    (3, 1): "`range(start, stop)` 在 `stop` **之前**停下，这里是第 1–4 周。",
    (3, 2): "`all()` 只有在**每个**元素都通过时才为 True；55 不及格，所以是 False。",
    # ---- Session 4 ----
    (4, 0): "`[[0]*3]*3` 造出对**同一行**的三个引用，改一处等于改三处。要用 `[[0]*3 for _ in range(3)]`。",
    (4, 1): "键不存在时 `.get()` 返回 `None`（或默认值）而不是抛错——`gpa['Ben']` 则会抛 KeyError。",
    (4, 2): "步长为 -1 的切片返回一个反转的**副本**——常见的 Python 惯用法。",
    # ---- Session 5 ----
    (5, 0): "默认值在 def 时只创建**一次**，同一个列表跨调用一直存在。用 `roster=None` 然后 `roster = roster or []`。",
    (5, 1): "打印不是返回。没有 `return` 的函数给出 `None`。",
    (5, 2): "闭包捕获的是**变量** `score`，不是它的值；等到调用时循环已把 `score` 留在 73。修法是绑定当前值：`lambda score=score: score`。",
    # ---- Session 6 ----
    (6, 0): "每个递归函数都需要基例。没有它，Python 会在递归上限（约 1000 层）处以 RecursionError 停下。",
    (6, 1): "第二个分支算出了 `score + 5` 又扔掉了：前面没有 `return`，函数走到结尾就交回 `None`。在递归函数里，同样的手滑会悄悄毒化整条调用链。",
    (6, 2): "每个未完成的调用都占一个栈帧，CPython 默认给栈设了上限（约 1000），超过就抛 RecursionError。递归不免费——平铺的深层工作交给循环。",
    # ---- Session 7 ----
    (7, 0): "`int()` 只解析整数文本；'3.0' 不是合法的整数字面量。用 `int(float(score))`。",
    (7, 1): "Python 用银行家舍入（一半时取偶数）：`round(2.5) == 2` 而 `round(3.5) == 4`。汇总数据时当心。",
    (7, 2): "累加各项时浮点误差会累积：0.1+0.2+0.3 是 0.6000000000000001。比较总和用 `math.isclose`，展示时再取整。",
    (7, 3): "Python 接受下划线作数字分隔符，连 `int()` 的文本里也接受。",
    # ---- Session 8 ----
    (8, 0): "每个 CSV 值到手都是**字符串**——`'91' + 1` 不是加法，是崩溃。先转换：`int(row['score']) + 1`。",
    (8, 1): "JSON 是另一门语言：Python 的 `True` 写成小写的 `true`（`None` 变成 `null`）。`json.load` 会翻译回来。",
    (8, 2): "文件对象是一个游标，不是容器：读完一遍后停在末尾，再读返回空。重新打开（或 `seek(0)`），或者一次性读进列表。",
    # ---- Session 9 ----
    (9, 0): "`+` 是贪婪的——能抓多少抓多少。想要最短匹配用 `+?`：`r'\\[(.+?)\\]'`。",
    (9, 1): "`re.match` 锚定在字符串**开头**。想在任意位置找匹配用 `re.search`。",
    (9, 2): "`.` 匹配**任意**字符，所以 `gradesXcsv` 也符合模式。想要真正的点就转义——`r'grades\\.csv'`。",
    # ---- Session 10 ----
    (10, 0): "生成器是一次性的：完整遍历一遍后就耗尽了。要么重建，要么需要用两次就先存成列表。",
    (10, 1): "`@dataclass` 自动写了逐字段比较的 `__eq__`，所以值相同的成绩 `==` 成立（尽管 `g1 is g2` 为 False）。",
    (10, 2): "`students` 是所有实例共享的**类**变量。在 `__init__` 里给每个实例自己的：`self.students = []`。",
}

# Chinese text for the generated traps section (page + reveal chrome).
SECTION_HEADING = "陷阱 —— 先预测，再揭晓"
SECTION_INTRO = ("先读每段代码、想好它会做什么，**再**揭晓答案。"
                 "想逐行运行、随手改动它们，请打开下方的 **▸ 陷阱 —— 先预测，再运行**。\n")
REVEAL_SUMMARY = "查看结果"
