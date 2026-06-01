#!/usr/bin/env python3
"""Generate resume/vivek_resume_full.pdf from the portfolio Markdown file.

Pipeline: Markdown  ->  styled HTML  ->  PDF (via headless Google Chrome).

Usage:
    python3 resume/generate_resume.py
    python3 resume/generate_resume.py --keep-html        # also keep the intermediate HTML
    CHROME_BIN="/path/to/chrome" python3 resume/generate_resume.py

Requirements:
    pip install markdown
    A Chromium-based browser (Google Chrome / Chromium / Brave / Edge).
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("Missing dependency. Install it with:  pip install markdown")

# Paths are resolved relative to the repo root (parent of this script's folder).
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DEFAULT_INPUT = REPO_ROOT / "Vivek Sharma - Portfolio.md"
DEFAULT_OUTPUT = SCRIPT_DIR / "vivek_resume_full.pdf"

# Candidate locations for a Chromium-based browser (macOS first, then Linux).
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "brave-browser",
    "microsoft-edge",
]

CSS = """
@page {
  size: A4;
  margin: 16mm 14mm;
}

* { box-sizing: border-box; }

body {
  font-family: "Segoe UI", Helvetica, Arial, sans-serif;
  color: #1f2937;
  font-size: 10.5pt;
  line-height: 1.45;
  margin: 0;
}

/* Name */
h1:first-of-type {
  font-size: 22pt;
  color: #1e40af;
  margin: 0 0 0.2rem;
  letter-spacing: 0.3px;
}

/* Company / major section headers */
h1 {
  font-size: 15pt;
  color: #1e40af;
  border-bottom: 2px solid #1e40af;
  padding-bottom: 0.2rem;
  margin: 1.4rem 0 0.6rem;
  break-after: avoid;
}

/* Subsection headers (Summary, Key Projects, Tech Stack, ...) */
h2 {
  font-size: 11.5pt;
  color: #1e40af;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid #d1d5db;
  padding-bottom: 0.15rem;
  margin: 1.1rem 0 0.5rem;
  break-after: avoid;
}

p { margin: 0 0 0.55rem; }

/* Contact line directly under the name */
h1:first-of-type + p strong,
h1:first-of-type + p { color: #4b5563; }

a { color: #1e40af; text-decoration: none; }

ul { margin: 0.3rem 0 0.6rem; padding-left: 1.1rem; }
li { margin-bottom: 0.25rem; }

table {
  width: 100%;
  border-collapse: collapse;
  margin: 0.4rem 0 0.8rem;
  font-size: 9.6pt;
  break-inside: auto;
}

th, td {
  border: 1px solid #e2e8f0;
  padding: 0.45rem 0.55rem;
  text-align: left;
  vertical-align: top;
}

th {
  background: #eff6ff;
  color: #1e40af;
  font-weight: 700;
}

tr { break-inside: avoid; }

hr {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 1rem 0;
}

strong { color: #111827; }

/* Keep each company block from being orphaned at the bottom of a page. */
h1, h2 { page-break-after: avoid; }
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Vivek Sharma — Resume</title>
<style>{css}</style>
</head>
<body>
{body}
</body>
</html>
"""


def find_chrome(explicit: str | None) -> str:
    """Return a usable Chrome/Chromium executable path or exit with guidance."""
    candidates = []
    if explicit:
        candidates.append(explicit)
    if os.environ.get("CHROME_BIN"):
        candidates.append(os.environ["CHROME_BIN"])
    candidates.extend(CHROME_CANDIDATES)

    for cand in candidates:
        if os.path.sep in cand:
            if Path(cand).exists():
                return cand
        else:
            found = shutil.which(cand)
            if found:
                return found

    sys.exit(
        "Could not find a Chromium-based browser.\n"
        "Install Google Chrome, or point the script at one:\n"
        '    CHROME_BIN="/path/to/chrome" python3 resume/generate_resume.py'
    )


def render_html(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8")
    body = markdown.markdown(
        text,
        extensions=["tables", "sane_lists", "smarty"],
    )
    return HTML_TEMPLATE.format(css=CSS, body=body)


def html_to_pdf(chrome: str, html_path: Path, pdf_path: Path) -> None:
    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--no-sandbox",
        f"--print-to-pdf={pdf_path}",
        html_path.as_uri(),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not pdf_path.exists():
        sys.exit(
            "Chrome failed to render the PDF.\n"
            f"Command: {' '.join(cmd)}\n"
            f"stderr:\n{result.stderr}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert the portfolio Markdown to a PDF resume.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Source Markdown file.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Destination PDF file.")
    parser.add_argument("--chrome", default=None, help="Path to a Chrome/Chromium executable.")
    parser.add_argument("--keep-html", action="store_true", help="Keep the intermediate HTML file.")
    args = parser.parse_args()

    if not args.input.exists():
        sys.exit(f"Input Markdown not found: {args.input}")

    chrome = find_chrome(args.chrome)
    html = render_html(args.input)

    if args.keep_html:
        html_path = args.output.with_suffix(".html")
        html_path.write_text(html, encoding="utf-8")
        cleanup = False
    else:
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", delete=False, encoding="utf-8", dir=str(args.output.parent)
        )
        tmp.write(html)
        tmp.close()
        html_path = Path(tmp.name)
        cleanup = True

    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        html_to_pdf(chrome, html_path, args.output)
        print(f"Generated {args.output}")
        if args.keep_html:
            print(f"Kept intermediate HTML at {html_path}")
    finally:
        if cleanup and html_path.exists():
            html_path.unlink()


if __name__ == "__main__":
    main()
