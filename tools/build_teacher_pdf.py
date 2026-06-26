#!/usr/bin/env python3
"""
Build the Teacher Edition PDF from the markdown curriculum.

Pipeline:  markdown -> styled HTML (print CSS) -> chromium --print-to-pdf

Run with a Python that has the `markdown` package, e.g.:
    /path/to/venv/bin/python tools/build_teacher_pdf.py
Requires `chromium` (or `chromium-browser`) on PATH for the final print step.
"""
from __future__ import annotations
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import re

import markdown  # provided by the build venv

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"

_LIST_RE = re.compile(r"^\s*(?:[-*+]\s|\d+\.\s)")


def normalize_lists(md: str) -> str:
    """Insert a blank line before a list that directly follows a paragraph line.

    python-markdown's `sane_lists` only starts a list when a blank line precedes it;
    the teacher syllabus packs lists right under bold labels (e.g. the minute clocks),
    so without this they render as run-together prose. This restores proper bullets.
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

# Main document + appendices a teacher needs in one place.
PARTS = [
    ("curriculum/syllabus-teacher.md", None),
    ("curriculum/course-outline.md", "Appendix A — Master Course Outline"),
    ("curriculum/connection-map.md", "Appendix B — Connection Map (education-research bridges)"),
    ("assessments/quizzes.md", "Appendix C — Per-Session Quizzes & Answer Keys"),
]

PRINT_CSS = """
@page { size: A4; margin: 18mm 16mm 20mm 16mm; }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html { font-size: 11pt; }
body { font-family: -apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
       color:#1c2330; line-height:1.5; margin:0; }
.cover { text-align:center; padding-top:32%; page-break-after:always; }
.cover h1 { font-size:30pt; margin:0 0 6pt; letter-spacing:-.5pt; }
.cover .sub { font-size:14pt; color:#2f6df0; font-weight:600; }
.cover .meta { margin-top:20pt; color:#5b6675; font-size:11pt; }
.cover .rule { width:60pt; height:4pt; background:#2f6df0; margin:14pt auto; border-radius:2pt; }
h1 { font-size:19pt; border-bottom:2px solid #2f6df0; padding-bottom:3pt; }
h2 { font-size:15pt; margin-top:16pt; color:#13203a; border-bottom:1px solid #d8deea; padding-bottom:2pt; }
h3 { font-size:12.5pt; margin-top:12pt; color:#243; }
/* page break before each major section heading (but not the first) */
h2 { page-break-before: always; page-break-after: avoid; }
h3 { page-break-after: avoid; }
.appendix-title { page-break-before: always; }
p, li { orphans:3; widows:3; }
ul,ol { margin:.3em 0 .6em; padding-left:1.3em; }
code { font-family:'SF Mono',Menlo,Consolas,monospace; font-size:9.5pt;
       background:#eef1f6; padding:.5pt 3pt; border-radius:3pt; }
pre { background:#f4f6fa; border:1px solid #d8deea; border-left:3px solid #2f6df0;
      border-radius:5pt; padding:7pt 9pt; font-size:8.6pt; line-height:1.42; overflow:visible;
      white-space:pre-wrap; word-break:break-word; page-break-inside:avoid; }
pre code { background:none; padding:0; font-size:8.6pt; }
blockquote { margin:.6em 0; padding:.3em .8em; border-left:3px solid #2f6df0;
             background:#eef3fd; color:#33415c; border-radius:0 4pt 4pt 0; }
table { border-collapse:collapse; width:100%; margin:.6em 0; font-size:9.3pt; page-break-inside:avoid; }
th,td { border:1px solid #c9d2e2; padding:4pt 6pt; text-align:left; vertical-align:top; }
th { background:#eef2fb; }
hr { border:0; border-top:1px dashed #c9d2e2; margin:1em 0; }
a { color:#1f4fc0; text-decoration:none; }
strong { color:#13203a; }
"""

COVER = f"""
<div class="cover">
  <div class="sub">Python for an Education Researcher</div>
  <h1>Teacher Edition</h1>
  <div class="rule"></div>
  <p style="font-size:12pt;color:#33415c">Minute-by-minute session playbooks · transition scripts ·
     predicted misconceptions · Socratic prompts</p>
  <div class="meta">
     A 9-session (8–10 hour) accelerated Python course<br>
     for a PhD-in-Education learner with no prior coding experience.<br><br>
     Generated {date.today().isoformat()} · Instructional content original
  </div>
</div>
"""


def render() -> str:
    md = markdown.Markdown(extensions=[
        "extra", "tables", "fenced_code", "sane_lists", "toc", "attr_list",
    ])
    sections = [COVER]
    for rel, appendix_title in PARTS:
        text = (ROOT / rel).read_text()
        if appendix_title:
            sections.append(f'<h1 class="appendix-title">{appendix_title}</h1>')
        md.reset()
        sections.append(md.convert(normalize_lists(text)))
    body = "\n".join(sections)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Teacher Edition — Python for an Education Researcher</title>
<style>{PRINT_CSS}</style></head><body>{body}</body></html>"""


def main() -> None:
    OUT.mkdir(exist_ok=True)
    html_path = OUT / "teacher-edition.html"
    pdf_path = OUT / "teacher-edition.pdf"
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
    else:
        print("PDF generation failed:\n" + r.stderr, file=sys.stderr)


if __name__ == "__main__":
    main()
