# 环境配置与工具

在自己电脑上运行 Python 所需的一切——外加让学习提速的工具（和 AI 使用习惯）。

## 最快起步：什么都不装
本站每个示例都能**在浏览器里**运行——直接按 **Run** 就行。无需安装，
前几课用它正合适。想处理*自己的文件*时，再按下面的步骤本地安装 Python。

## 用 Jupyter 笔记本学整门课
每一课同时也是一个 **Jupyter 笔记本**——同样的示例和练习，做成可以逐格运行的文档。
三种用法，选顺手的：

- **浏览器里、免安装** —— 打开在线 JupyterLite 工作台：
  <https://yangnei.github.io/learn-python/jupyter/lab/index.html>。是真正的 Jupyter，
  完全在你的浏览器里运行；改动保存在本地浏览器中，什么都不会上传。
  每课页面也有直接打开该课笔记本的按钮。
- **Google Colab** —— 每课页面有 **Open in Colab** 按钮（免费，跑在 Google 云端，
  需要 Google 账号）。想存到 Drive 或做更重的数据工作时很方便。
- **本地 Jupyter** —— 装好 Python 后（见下）：`pip install jupyterlab`，运行
  `jupyter lab`，打开你从课程页面下载的 `.ipynb`。

**笔记本怎么开：** 点一个单元格，按 **Shift + Enter** 运行并跳到下一格。运行前先预测
输出——惊讶就是课程本身——然后改一改、再运行，做实验。

**自动补全与装库：** 按 **Tab** 补全名字，**Shift + Tab** 弹出函数帮助。要加包，
*在单元格里*运行 `%pip install <名字>`（如 `%pip install pandas`）。浏览器版
（JupyterLite）只支持兼容 Pyodide 的包——`pandas`、`numpy`、`matplotlib` 这些大件都行——
安装只在本次会话有效，内核重启后重跑那一格。本地 Jupyter 或 Colab 里，
`%pip install` 对该环境是永久的。

## 安装 Python（按你的系统选）

**Windows**
- 官方安装包：<https://www.python.org/downloads/windows/> —— 第一屏**勾选
  "Add python.exe to PATH"**，再点 *Install Now*。
- （备选）Microsoft Store → 搜索 **Python 3.12**。
- 验证成功——打开 **PowerShell** 运行：`python --version`
- 官方指南：<https://docs.python.org/3/using/windows.html>

**macOS**
- 官方安装包：<https://www.python.org/downloads/macos/>
- （备选）[Homebrew](https://brew.sh/)：`brew install python`
- 验证成功——打开**终端**运行：`python3 --version`
- 官方指南：<https://docs.python.org/3/using/mac.html>

**Linux**
- 通常已预装。若没有：`sudo apt install python3 python3-pip`（Debian/Ubuntu）或
  `sudo dnf install python3`（Fedora）。
- 验证成功：`python3 --version`
- 官方指南：<https://docs.python.org/3/using/unix.html>

**编辑器：** 安装 **VS Code**（<https://code.visualstudio.com/>）和微软出品的
**Python 扩展**。图文教程：<https://code.visualstudio.com/docs/python/python-tutorial>。
想要更轻量的？**Thonny**（<https://thonny.org/>）是自带变量查看器和调试器的新手 IDE。

**运行脚本：** 代码存成 `name.py`，然后在终端运行 `python name.py`（Windows）
或 `python3 name.py`（macOS/Linux）。

**装第三方包**（比如第 8 课的 pandas 预告）：`pip install pandas`（或 `pip3`）。

## 亲眼看代码怎么跑 —— Python Tutor
**<https://pythontutor.com/>** —— 贴上代码，**逐行单步执行**，实时看到变量、调用栈，
以及哪个名字指着哪个对象。对本课程反复告诫的那些坑，它是最好的可视化工具：
- **别名** —— 亲眼看 `b = a` 让两个名字指向*同一个*列表（第 4 课），
- **可变默认参数** bug（第 5 课），
- **递归调用栈**的堆起与展开（第 6 课）。

每当你想"等等，这为什么会这样？"——把代码片段丢进 Python Tutor。

## 用 AI 学习（但别让它替你干活）
AI 助手（Claude 等）是巨大的加速器——*前提是让它解释，而不是让它写*。
每个答案都要自己敲。适合本课程的提示词：
- **"给初学者总结这页文档，只要我需要的 5 件事：\<贴文本或 URL\>"** ——
  把密不透风的参考页变成能用的东西。
- **"解释这个报错和最可能的原因，指出是哪一行：\<贴回溯信息\>"**
- **"先预测这段代码打印什么，再解释为什么：\<代码\>"** —— 然后自己运行、对答案。
  这种先预测再运行的习惯*就是*本课程的方法论。
- **"按本课程的陷阱清单审查我的函数——同一 vs 相等、别名、可变默认值、差一错误——
  但不要替我重写。"**
- **"给我 3 道更难的同类练习，答案先藏起来。"**

经验法则：**让它解释，别让它代劳。** 如果它甩给你一段你读不懂每一行的代码，
让它慢下来逐行讲。

## 其他称手工具
- **regex101.com**（<https://regex101.com/>）—— 交互式构建并*解释*正则表达式，
  带实时匹配视图（第 9 课）。记得把 flavor 设为 **Python**。
- **官方文档** —— [Python 教程](https://docs.python.org/3/tutorial/)和
  [标准库参考](https://docs.python.org/3/library/)。都收藏好。
- **Google Colab**（<https://colab.research.google.com/>）—— 浏览器里跑 Python 笔记本，
  免安装；开始做真实数据工作后的自然一步。
- 本站的**[陷阱与坑](#traps)**速查表——整门课都开着它。
