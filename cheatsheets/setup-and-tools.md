# Setup & Tools

Everything you need to run Python on your own machine — plus the tools (and AI habits) that make
learning this material faster.

## Fastest start: no install at all
Every example on this site runs **in your browser** — just press **Run**. Nothing to
install, great for the first sessions. When you want to work on *your own files*, install Python
locally with the steps below.

## Install Python (pick your OS)

**Windows**
- Official installer: <https://www.python.org/downloads/windows/> — on the first screen, **check
  "Add python.exe to PATH"**, then *Install Now*.
- (Alternative) Microsoft Store → search **Python 3.12**.
- Check it worked — open **PowerShell** and run: `python --version`
- Official guide: <https://docs.python.org/3/using/windows.html>

**macOS**
- Official installer: <https://www.python.org/downloads/macos/>
- (Alternative) [Homebrew](https://brew.sh/): `brew install python`
- Check it worked — open **Terminal** and run: `python3 --version`
- Official guide: <https://docs.python.org/3/using/mac.html>

**Linux**
- Usually already installed. If not: `sudo apt install python3 python3-pip` (Debian/Ubuntu) or
  `sudo dnf install python3` (Fedora).
- Check it worked: `python3 --version`
- Official guide: <https://docs.python.org/3/using/unix.html>

**An editor:** install **VS Code** (<https://code.visualstudio.com/>) and its **Python extension**
(by Microsoft). Step-by-step: <https://code.visualstudio.com/docs/python/python-tutorial>.
Prefer something lighter? **Thonny** (<https://thonny.org/>) is a beginner IDE with a built-in
variable viewer and debugger.

**Run a script:** save your code as `name.py`, then in a terminal run `python name.py` (Windows)
or `python3 name.py` (macOS/Linux).

**Install a package** (e.g. for the Session 8 pandas teaser): `pip install pandas` (or `pip3`).

## Visualize what your code does — Python Tutor
**<https://pythontutor.com/>** — paste code and **step through it line by line**, watching
variables, the call stack, and which names point at which objects. It's the single best tool for
the things this course keeps warning you about:
- **aliasing** — see `b = a` make both names point at the *same* list (Session 4),
- the **mutable-default-argument** bug (Session 5),
- the **recursion call stack** building up and unwinding (Session 6).

Whenever you think *"wait, why did that happen?"* — drop the snippet into Python Tutor.

## Use AI to learn (without it doing the work for you)
An AI assistant (Claude, etc.) is a huge accelerator *if you ask it to explain rather than to
write*. Type every solution yourself. Prompts that fit this course:
- **"Summarize this doc page for a beginner, just the 5 things I need: \<paste text or URL\>"** —
  turn a dense reference page into something usable.
- **"Explain this error and its most likely cause, and point me to the line: \<paste the traceback\>"**
- **"Predict what this prints, then explain why: \<code\>"** — then run it and compare. That
  predict-then-run habit *is* the method this course is built on.
- **"Review my function for the traps in this course — identity vs value, aliasing, mutable
  defaults, off-by-one — but don't rewrite it for me."**
- **"Give me 3 harder practice tasks like this one, with the solutions hidden."**

Rule of thumb: **ask it to explain, not to do.** If it hands you code you can't read line by line,
ask it to slow down and walk you through it.

## Other handy tools
- **regex101.com** (<https://regex101.com/>) — build and *explain* regular expressions
  interactively, with a live match view (Session 9). Set the flavor to **Python**.
- **Official docs** — the [Python Tutorial](https://docs.python.org/3/tutorial/) and the
  [Library Reference](https://docs.python.org/3/library/). Bookmark both.
- **Google Colab** (<https://colab.research.google.com/>) — run Python notebooks in the browser,
  no install; a natural next step once you start doing real data work.
- This site's **[Traps & Gotchas](#traps)** sheet — keep it open the whole course.
