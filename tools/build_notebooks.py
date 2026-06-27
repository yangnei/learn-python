"""
build_notebooks.py — generate one Jupyter notebook per session from the existing
examples (examples/session-NN/demo.py + practice.md).

    python3 tools/build_notebooks.py

Writes docs/notebooks/session-NN.ipynb. The notebooks are self-contained so they run
unchanged in JupyterLite (Pyodide), Google Colab, local Jupyter, or VS Code: the two
sessions that read local files (S8 CSVs, S10 grades.py module) get a setup cell that
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

# Each session has one demo script; most are demo.py, S2 is traps_demo.py.
DEMO_NAME = {2: "traps_demo.py"}

# A line that begins a new logical block -> a new code cell.
SECTION_RE = re.compile(r'^(# -{2,}|# \d+[\).]|print\("(\\n)?=== )')


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
    if n == 8:
        students = (EXAMPLES / "session-08" / "students.csv").read_text()
        survey = (EXAMPLES / "session-08" / "survey.csv").read_text()
        return (
            "# Setup (notebook only): write the data files this session reads.\n"
            "from pathlib import Path\n"
            f"Path('students.csv').write_text({students!r})\n"
            f"Path('survey.csv').write_text({survey!r})\n"
            "print('wrote students.csv, survey.csv')"
        )
    if n == 10:
        grades = (EXAMPLES / "session-10" / "grades.py").read_text()
        return (
            "# Setup (notebook only): write the module this session imports, then make it importable.\n"
            "import sys\n"
            "from pathlib import Path\n"
            f"Path('grades.py').write_text({grades!r})\n"
            "sys.path.insert(0, '.')\n"
            "print('wrote grades.py')"
        )
    return None


def patch_demo(n: int, src: str) -> str:
    """Make file-reading demos work without __file__ (notebooks have no __file__)."""
    if n == 8:
        src = src.replace(
            "HERE = Path(__file__).parent     # so it works no matter where you run it",
            'HERE = Path(".")                 # notebook: files are written by the setup cell',
        )
    return src


def practice_cells(n: int) -> list[dict]:
    """Tasks as markdown, a scratch code cell to work in, then collapsed solutions."""
    path = EXAMPLES / f"session-{n:02d}" / "practice.md"
    if not path.exists():
        return []
    text = path.read_text()
    m = re.search(r"(?m)^#{2,4}\s+Solutions?\b.*$", text)
    tasks = (text[:m.start()] if m else text).rstrip()
    cells = [md(tasks)]
    cells.append(code("# Your practice work — type here. Predict before you run.\n"))
    if m:
        sols = text[m.end():].lstrip("\n").rstrip()
        cells.append(md(
            "<details>\n<summary><strong>Show solutions</strong></summary>\n\n"
            + sols + "\n\n</details>"
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


def build_notebook(n: int, title: str, desc: str) -> dict:
    _counter[0] = 0
    intro = (
        f"# Session {n} — {title}\n\n"
        f"> {desc}\n\n"
        "**How to use this notebook:** read each cell, **predict** what it prints, "
        "then run it with **Shift + Enter**. Change one thing and predict again — the "
        "surprise is the lesson. Practice tasks (with collapsed solutions) are at the bottom.\n\n"
        "**Tips:** press **Tab** to autocomplete a name, and **Shift + Tab** for a function's "
        "help. Need a library? Run `%pip install <name>` in a cell (e.g. `%pip install pandas`) — "
        "in the browser (JupyterLite) that fetches a Pyodide build and lasts for the session."
    )
    cells = [md(intro)]

    s = setup_cell(n)
    if s:
        cells.append(code(s))

    demo_src = (EXAMPLES / f"session-{n:02d}" / DEMO_NAME.get(n, "demo.py")).read_text()
    demo_src = patch_demo(n, strip_module_docstring(demo_src))
    for chunk in split_code_cells(demo_src):
        cells.append(code(chunk))

    cells.append(md("## Now you try — practice"))
    cells.extend(practice_cells(n))

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python (Pyodide)", "name": "python"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for n, title, desc, _key in SESSIONS:
        nb = build_notebook(n, title, desc)
        path = OUT / f"session-{n:02d}.ipynb"
        path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
        print(f"   {path.relative_to(ROOT)}  ({len(nb['cells'])} cells)")
    print(f"Wrote {len(SESSIONS)} notebooks to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
