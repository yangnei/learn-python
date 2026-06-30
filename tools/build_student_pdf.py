#!/usr/bin/env python3
"""
Build the Student Edition PDF (offline companion to the website) into docs/.

Pipeline:  markdown -> styled HTML (print CSS) -> chromium --print-to-pdf
It bundles, in reading order: the student syllabus, every session's lesson
(from slides/) + practice (from examples/), the cheat sheets, and the quizzes.

Run with a Python that has the `markdown` package, e.g.:
    /path/to/venv/bin/python tools/build_student_pdf.py
Requires `chromium` (or `chromium-browser`) on PATH for the final print step.
Output:  docs/learn-python-student.pdf  (served by the GitHub Pages site).
"""
from __future__ import annotations
import importlib.util
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import markdown  # provided by the build venv

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# Reuse the lesson/practice splitters from the site builder (single source of truth).
_bs_spec = importlib.util.spec_from_file_location("bs", ROOT / "tools" / "build_site.py")
_bs = importlib.util.module_from_spec(_bs_spec)
_bs_spec.loader.exec_module(_bs)

_traps_spec = importlib.util.spec_from_file_location("traps", ROOT / "tools" / "traps.py")
_traps = importlib.util.module_from_spec(_traps_spec)
_traps_spec.loader.exec_module(_traps)


def pdf_traps(n: int) -> str:
    """Printed traps reference: code, the common wrong guess, the real result, and why."""
    entries = _traps.TRAPS.get(n, [])
    if not entries:
        return ""
    out = ["## Traps — predict, then check\n",
           "Cover the result, predict each one, then check yourself.\n"]
    for i, t in enumerate(entries, 1):
        out.append(f"**{i}.**\n\n```python\n{_traps.display_code(t)}\n```\n")
        out.append(f"Result: `{_traps.reveal(t)}`. {t['why']}\n")
    return "\n".join(out)


def pdf_practice(heading: str, tasks: str, solution: str) -> str:
    """Practice markdown for the PDF — solutions shown (a printed <details> would hide them)."""
    out = f"## {heading}\n\n{tasks}\n"
    if solution:
        out += f"\n### Solutions\n\n{solution}\n"
    return out

# Sessions that have a lesson deck + practice file (capstone is an appendix).
N_SESSIONS = 5

_LIST_RE = re.compile(r"^\s*(?:[-*+]\s|\d+\.\s)")


def normalize_lists(md: str) -> str:
    """Insert a blank line before a list that directly follows a paragraph line.

    python-markdown's `sane_lists` only starts a list when a blank line precedes it.
    """
    out: list[str] = []
    in_code = False
    for line in md.splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
        if (not in_code and _LIST_RE.match(line) and out
                and out[-1].strip() and not _LIST_RE.match(out[-1])):
            out.append("")
        out.append(line)
    return "\n".join(out)


def strip_frontmatter(md: str) -> str:
    """Remove a leading YAML front-matter block (--- ... ---) from slide markdown."""
    if md.startswith("---"):
        end = md.find("\n---", 3)
        if end != -1:
            nl = md.find("\n", end + 1)
            return md[nl + 1:].lstrip() if nl != -1 else ""
    return md


PRINT_CSS = """
@page { size: A4; margin: 18mm 16mm 20mm 16mm; }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html { font-size: 11pt; }
body { font-family: -apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
       color:#1c2330; line-height:1.5; margin:0; }
.cover { text-align:center; padding-top:30%; page-break-after:always; }
.cover h1 { font-size:32pt; margin:0 0 6pt; letter-spacing:-.5pt; }
.cover .sub { font-size:15pt; color:#2f6df0; font-weight:700; }
.cover .meta { margin-top:20pt; color:#5b6675; font-size:11pt; }
.cover .rule { width:60pt; height:4pt; background:#2f6df0; margin:14pt auto; border-radius:2pt; }
.pagebreak { page-break-before: always; }
h1 { font-size:20pt; border-bottom:2px solid #2f6df0; padding-bottom:3pt; page-break-after:avoid; }
h2 { font-size:14pt; margin-top:15pt; color:#13203a; border-bottom:1px solid #d8deea; padding-bottom:2pt; page-break-after:avoid; }
h3 { font-size:12pt; margin-top:11pt; color:#243; page-break-after:avoid; }
p, li { orphans:3; widows:3; }
ul,ol { margin:.3em 0 .6em; padding-left:1.3em; }
code { font-family:'SF Mono',Menlo,Consolas,monospace; font-size:9.5pt;
       background:#eef1f6; padding:.5pt 3pt; border-radius:3pt; }
pre { background:#f4f6fa; border:1px solid #d8deea; border-left:3px solid #2f6df0;
      border-radius:5pt; padding:7pt 9pt; font-size:8.8pt; line-height:1.42; overflow:visible;
      white-space:pre-wrap; word-break:break-word; page-break-inside:avoid; }
pre code { background:none; padding:0; font-size:8.8pt; }
blockquote { margin:.6em 0; padding:.3em .8em; border-left:3px solid #2f6df0;
             background:#eef3fd; color:#33415c; border-radius:0 4pt 4pt 0; }
table { border-collapse:collapse; width:100%; margin:.6em 0; font-size:9.3pt; page-break-inside:avoid; }
th,td { border:1px solid #c9d2e2; padding:4pt 6pt; text-align:left; vertical-align:top; }
th { background:#eef2fb; }
hr { border:0; border-top:1px dashed #c9d2e2; margin:1em 0; }
a { color:#1f4fc0; text-decoration:none; }
strong { color:#13203a; }
details { margin:.4em 0; }
summary { font-weight:600; color:#2f6df0; }
"""

COVER = f"""
<div class="cover">
  <div class="sub">Learn Python</div>
  <h1>Student Edition</h1>
  <div class="rule"></div>
  <p style="font-size:12pt;color:#33415c">5 two-hour sessions + capstone · runnable examples ·
     trap cheat sheets · self-check quizzes</p>
  <div class="meta">
     An accelerated, self-study Python course<br>
     for a researcher with no prior coding experience.<br><br>
     Offline companion to the interactive website.<br>
     Generated {date.today().isoformat()} · Instructional content original
  </div>
</div>
"""


def render() -> str:
    md = markdown.Markdown(extensions=[
        "extra", "tables", "fenced_code", "sane_lists", "toc", "attr_list",
    ])
    slides_dir = ROOT / "slides"
    examples_dir = ROOT / "examples"
    cheats_dir = ROOT / "cheatsheets"

    def convert(text: str) -> str:
        md.reset()
        return md.convert(normalize_lists(text))

    sections = [COVER]

    # Front matter: the student syllabus.
    sections.append(convert((ROOT / "curriculum" / "syllabus-student.md").read_text()))

    # Each session, two halves: Part A lesson + practice, then Part B lesson + practice.
    for n in range(1, N_SESSIONS + 1):
        lesson_a, lesson_b = _bs.split_lesson(
            strip_frontmatter((slides_dir / f"session-{n:02d}-slides.md").read_text()))
        practice_path = examples_dir / f"session-{n:02d}" / "practice.md"
        ta = sa = tb = sb = ""
        if practice_path.exists():
            ta, sa, tb, sb = _bs.split_practice(practice_path.read_text())
        sections.append(f'<div class="pagebreak"></div>{convert(lesson_a)}')
        if ta:
            sections.append(convert(pdf_practice("Practice — Part A", ta, sa)))
        if lesson_b:
            sections.append(f'<div class="pagebreak"></div>{convert(lesson_b)}')
            if tb:
                sections.append(convert(pdf_practice("Practice — Part B", tb, sb)))
        traps_md = pdf_traps(n)
        if traps_md:
            sections.append(f'<div class="pagebreak"></div>{convert(traps_md)}')

    # Appendices: cheat sheets and quizzes.
    for fname in ("setup-and-tools.md", "traps-and-gotchas.md", "quick-reference.md", "glossary.md"):
        sections.append(f'<div class="pagebreak"></div>{convert((cheats_dir / fname).read_text())}')
    sections.append(f'<div class="pagebreak"></div>{convert((ROOT / "assessments" / "quizzes.md").read_text())}')

    body = "\n".join(sections)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Student Edition — Learn Python</title>
<style>{PRINT_CSS}</style></head><body>{body}</body></html>"""


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    html_path = DOCS / "learn-python-student.html"
    pdf_path = DOCS / "learn-python-student.pdf"
    html_path.write_text(render())
    print(f"Wrote {html_path}")

    chrome = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
    if not chrome:
        print("No chromium found — open the HTML and 'Print to PDF' manually.", file=sys.stderr)
        return
    cmd = [chrome, "--headless", "--no-sandbox", "--disable-gpu",
           "--no-pdf-header-footer", "--virtual-time-budget=8000",
           f"--print-to-pdf={pdf_path}", html_path.as_uri()]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if pdf_path.exists():
        print(f"Wrote {pdf_path} ({pdf_path.stat().st_size:,} bytes)")
        html_path.unlink(missing_ok=True)  # keep docs/ clean; the PDF is the artifact
    else:
        print("PDF generation failed:\n" + r.stderr, file=sys.stderr)


if __name__ == "__main__":
    main()
