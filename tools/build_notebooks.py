"""
build_notebooks.py — generate one Jupyter notebook per session from the existing
examples (examples/session-NN/demo.py + practice.md).

    python3 tools/build_notebooks.py

Writes docs/notebooks/session-NN.ipynb. The notebooks are self-contained so they run
unchanged in JupyterLite (Pyodide), Google Colab, local Jupyter, or VS Code: the two
sessions that read local files (S4 CSVs, S5 grades.py module) get a setup cell that
writes those files into the working directory first.
"""
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"
OUT = ROOT / "docs" / "notebooks"

# Reuse the session titles/descriptions from the site builder (single source of truth).
_spec = importlib.util.spec_from_file_location("bs", ROOT / "tools" / "build_site.py")
_bs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_bs)
SESSIONS = _bs.SESSIONS

# Every session's demo is demo.py.
DEMO_NAME: dict[int, str] = {}

# A line that begins a new logical block -> a new code cell. The PART A/PART B banners
# (rows of '#====') also start a new cell so the two halves split cleanly.
SECTION_RE = re.compile(r'^(# -{2,}|# \d+[\).]|# ={3,}|print\("(\\n)?=== )')


def strip_module_docstring(src: str) -> str:
    """Drop a leading triple-quoted module docstring (its 'Run me' note is moot here)."""
    m = re.match(r'\s*(?:"""|\'\'\').*?(?:"""|\'\'\')\s*\n', src, re.DOTALL)
    return src[m.end():] if m else src


def split_code_cells(src: str) -> list[str]:
    """Split demo source into cells at section headers; preamble joins the first cell."""
    cells, cur = [], []
    for line in src.split("\n"):
        if SECTION_RE.match(line) and any(l.strip() for l in cur):
            cells.append("\n".join(cur).strip("\n"))
            cur = [line]
        else:
            cur.append(line)
    if cur:
        cells.append("\n".join(cur).strip("\n"))
    return [c for c in cells if c.strip()]


def setup_cell(n: int) -> str | None:
    """Return notebook-only setup code for sessions that depend on local files."""
    if n == 4:   # the Files half reads CSVs
        students = (EXAMPLES / "session-04" / "students.csv").read_text()
        survey = (EXAMPLES / "session-04" / "survey.csv").read_text()
        return (
            "# Setup (notebook only): write the data files Part B of this session reads.\n"
            "from pathlib import Path\n"
            f"Path('students.csv').write_text({students!r})\n"
            f"Path('survey.csv').write_text({survey!r})\n"
            "print('wrote students.csv, survey.csv')"
        )
    if n == 5:   # the Modules/OOP half imports grades.py
        grades = (EXAMPLES / "session-05" / "grades.py").read_text()
        return (
            "# Setup (notebook only): write the module Part B imports, then make it importable.\n"
            "import sys\n"
            "from pathlib import Path\n"
            f"Path('grades.py').write_text({grades!r})\n"
            "sys.path.insert(0, '.')\n"
            "print('wrote grades.py')"
        )
    return None


def patch_demo(n: int, src: str) -> str:
    """Make file-reading demos work without __file__ (notebooks have no __file__)."""
    if n == 4:
        src = src.replace(
            "HERE = Path(__file__).parent     # so it works no matter where you run it",
            'HERE = Path(".")                 # notebook: files are written by the setup cell',
        )
    return src


def banner_topic(src: str, ab: str) -> str:
    """Pull the topic name out of a `# PART A — ...` / `# PART B — ...` banner."""
    m = re.search(rf"^# PART {ab} — (.+)$", src, re.M)
    return m.group(1).strip() if m else ""


def split_demo_halves(src: str) -> tuple[str, str]:
    """Split demo source at the PART B banner; strip both banners from the halves."""
    parts = re.split(r"(?m)^# ={3,}\n# PART B — .*\n# ={3,}\n?", src, maxsplit=1)

    def strip_banners(s: str) -> str:
        return re.sub(r"(?m)^# ={3,}\n# PART [AB] — .*\n# ={3,}\n?", "", s)

    a = strip_banners(parts[0])
    b = strip_banners(parts[1]) if len(parts) == 2 else ""
    return a, b


def practice_cells_for(label: str, tasks: str, solution: str) -> list[dict]:
    """A practice block for one half: tasks, a scratch cell, then collapsed solutions."""
    cells = [
        md(f"## Now you try — {label}\n\n{tasks}"),
        code("# Your practice work — type here. Predict before you run.\n"),
    ]
    if solution:
        cells.append(md(
            f"<details>\n<summary><strong>Show {label} solutions</strong></summary>\n\n"
            + solution + "\n\n</details>"
        ))
    return cells


# --- minimal nbformat v4.5 emitters -------------------------------------------
_counter = [0]


def _cell(kind: str, source: str, **extra) -> dict:
    _counter[0] += 1
    cell = {"cell_type": kind, "id": f"cell-{_counter[0]}", "metadata": {}, "source": [source]}
    cell.update(extra)
    return cell


def md(source: str) -> dict:
    return _cell("markdown", source)


def code(source: str) -> dict:
    return _cell("code", source, execution_count=None, outputs=[])


TIPS = (
    "**Tips:** press **Tab** to autocomplete a name, **Shift + Tab** for a function's help. "
    "Need a library? Run `%pip install <name>` in a cell (e.g. `%pip install pandas`) — in the "
    "browser (JupyterLite) it fetches a Pyodide build and lasts for the session."
)


def _nb(cells: list[dict]) -> dict:
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python (Pyodide)", "name": "python"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def _session_data(n: int):
    demo_src = patch_demo(n, strip_module_docstring(
        (EXAMPLES / f"session-{n:02d}" / "demo.py").read_text()))
    src_a, src_b = split_demo_halves(demo_src)
    topic_a, topic_b = banner_topic(demo_src, "A"), banner_topic(demo_src, "B")
    ta, sa, tb, sb = _bs.split_practice((EXAMPLES / f"session-{n:02d}" / "practice.md").read_text())
    return src_a, src_b, topic_a, topic_b, ta, sa, tb, sb


def build_notebook(n: int, title: str, desc: str) -> dict:
    """The full session (both halves) — offered as the top-of-page download."""
    _counter[0] = 0
    src_a, src_b, topic_a, topic_b, ta, sa, tb, sb = _session_data(n)
    intro = (f"# Session {n} — {title}\n\n> {desc}\n\n"
             "Two halves (**Part A**, **Part B**); each ends with its own practice (solutions "
             "collapsed). Predict each cell, then **Shift + Enter**.\n\n" + TIPS)
    cells = [md(intro)]
    s = setup_cell(n)
    if s:
        cells.append(code(s))
    cells.append(md(f"## Part A — {topic_a}"))
    cells.extend(code(c) for c in split_code_cells(src_a))
    cells.extend(practice_cells_for("Part A", ta, sa))
    cells.append(md(f"## Part B — {topic_b}"))
    cells.extend(code(c) for c in split_code_cells(src_b))
    cells.extend(practice_cells_for("Part B", tb, sb))
    return _nb(cells)


def build_half(n: int, part: str) -> dict:
    """One half (A or B): just that topic's demo + practice — embedded on the page."""
    _counter[0] = 0
    src_a, src_b, topic_a, topic_b, ta, sa, tb, sb = _session_data(n)
    if part == "A":
        topic, src, tasks, sol, setup = topic_a, src_a, ta, sa, None
    else:
        topic, src, tasks, sol, setup = topic_b, src_b, tb, sb, setup_cell(n)
    intro = (f"# Session {n}, Part {part} — {topic}\n\n"
             "Read each cell, **predict** the output, then run it with **Shift + Enter**. "
             "The practice (solutions collapsed) is at the end.\n\n" + TIPS)
    cells = [md(intro)]
    if setup:
        cells.append(code(setup))
    cells.extend(code(c) for c in split_code_cells(src))
    cells.extend(practice_cells_for("Practice", tasks, sol))
    return _nb(cells)


def build_scratch() -> dict:
    """A blank sandbox notebook for the 'Try it yourself' slot."""
    _counter[0] = 0
    cells = [
        md("# Scratch notebook\n\nYour own playground — type Python and press "
           "**Shift + Enter** to run.\n\n" + TIPS),
        code("# Try anything here.\n"),
    ]
    return _nb(cells)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for n, title, desc, _key in SESSIONS:
        variants = {
            f"session-{n:02d}": build_notebook(n, title, desc),
            f"session-{n:02d}-a": build_half(n, "A"),
            f"session-{n:02d}-b": build_half(n, "B"),
        }
        for stem, nb in variants.items():
            (OUT / f"{stem}.ipynb").write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
            count += 1
    (OUT / "scratch.ipynb").write_text(json.dumps(build_scratch(), indent=1, ensure_ascii=False) + "\n")
    count += 1
    print(f"Wrote {count} notebooks to {OUT.relative_to(ROOT)}/ "
          f"({len(SESSIONS)} full + {2*len(SESSIONS)} halves + 1 scratch)")


if __name__ == "__main__":
    main()
