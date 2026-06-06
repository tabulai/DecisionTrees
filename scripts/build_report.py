#!/usr/bin/env python3
"""Build the static HTML report from the source Markdown brief."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "deep-research-report.md"
HTML_OUT = ROOT / "index.html"
MANIFEST = ROOT / "references" / "manifest.json"

TITLE = "State of Decision Tree Algorithms: June 2026"
SUBTITLE = (
    "A literature review of tree induction, split criteria, pruning, "
    "tree ensembles, optimal sparse trees, streaming trees, and specialized forests."
)
AUTHOR = "Bojan Tunguz"
VERSION = "0.2"
REPORT_DATE = "June 6, 2026"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def extract_sections(markdown_text: str) -> list[tuple[str, str, str]]:
    sections: list[tuple[str, str, str]] = []
    parts = re.split(r"(?m)^## ", markdown_text)
    for part in parts[1:]:
        title, _, body = part.partition("\n")
        sections.append((title.strip(), slugify(title), body.strip()))
    return sections


def replace_citations(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        keys = [k.strip().lstrip("@") for k in match.group(1).split(";") if k.strip()]
        links = [
            f'<a class="citation" href="references/bibliography.bib" title="{html.escape(key)}">{html.escape(key)}</a>'
            for key in keys
        ]
        return "[" + "; ".join(links) + "]"

    return re.sub(r"\[@([^\]]+)\]", repl, text)


def inline_format(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    return replace_citations(text)


def render_table(lines: list[str]) -> str:
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return ""
    header = rows[0]
    body = rows[2:] if re.match(r"^\s*:?-+:?\s*$", rows[1][0]) else rows[1:]
    head_html = "".join(f"<th>{inline_format(c)}</th>" for c in header)
    body_rows = []
    for row in body:
        body_rows.append("<tr>" + "".join(f"<td>{inline_format(c)}</td>" for c in row) + "</tr>")
    return (
        '<div class="table-wrap"><table><thead><tr>'
        + head_html
        + "</tr></thead><tbody>"
        + "".join(body_rows)
        + "</tbody></table></div>"
    )


def markdown_to_html(markdown_text: str) -> str:
    out: list[str] = []
    lines = markdown_text.splitlines()
    i = 0
    in_code = False
    code_lines: list[str] = []
    paragraph: list[str] = []
    bullets: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            out.append("<p>" + inline_format(" ".join(paragraph)) + "</p>")
            paragraph = []

    def flush_bullets() -> None:
        nonlocal bullets
        if bullets:
            out.append("<ul>" + "".join(f"<li>{inline_format(b)}</li>" for b in bullets) + "</ul>")
            bullets = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines = []
                in_code = False
            else:
                flush_paragraph()
                flush_bullets()
                in_code = True
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue

        if not stripped:
            flush_paragraph()
            flush_bullets()
            i += 1
            continue

        if stripped.startswith("|") and "|" in stripped[1:]:
            flush_paragraph()
            flush_bullets()
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            out.append(render_table(table_lines))
            continue

        if stripped.startswith("# "):
            flush_paragraph()
            flush_bullets()
            out.append(f"<h1>{inline_format(stripped[2:].strip())}</h1>")
        elif stripped.startswith("## "):
            flush_paragraph()
            flush_bullets()
            title = stripped[3:].strip()
            out.append(f'<h2 id="{slugify(title)}">{inline_format(title)}</h2>')
        elif stripped.startswith("### "):
            flush_paragraph()
            flush_bullets()
            out.append(f"<h3>{inline_format(stripped[4:].strip())}</h3>")
        elif stripped.startswith("- "):
            flush_paragraph()
            bullets.append(stripped[2:].strip())
        elif re.match(r"^\d+\. ", stripped):
            flush_paragraph()
            flush_bullets()
            paragraph.append(stripped)
        else:
            flush_bullets()
            paragraph.append(stripped)
        i += 1

    flush_paragraph()
    flush_bullets()
    return "\n".join(out)


def build_html() -> None:
    md = SOURCE.read_text(encoding="utf-8")
    sections = extract_sections(md)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    body = markdown_to_html(md)
    nav = "\n".join(f'<a href="#{slug}">{html.escape(title)}</a>' for title, slug, _ in sections)
    html_text = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(TITLE)}</title>
  <style>
    :root {{
      --ink: #172033;
      --muted: #5b667a;
      --line: #d8deea;
      --paper: #fffaf2;
      --panel: #ffffff;
      --accent: #0f766e;
      --accent-2: #9a3412;
      --tint: #edf7f4;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background: var(--paper);
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.62;
    }}
    header {{
      background: linear-gradient(135deg, #0f766e 0%, #172033 62%, #3b2f2f 100%);
      color: white;
      padding: 56px 24px 38px;
    }}
    .wrap {{ max-width: 1120px; margin: 0 auto; }}
    .eyebrow {{ font-size: 0.78rem; letter-spacing: 0.08em; text-transform: uppercase; opacity: 0.84; }}
    h1 {{ font-size: clamp(2.1rem, 5vw, 4.3rem); line-height: 1.05; margin: 14px 0 18px; max-width: 920px; }}
    .subtitle {{ max-width: 820px; font-size: 1.12rem; color: #dce8e5; }}
    .meta {{ margin-top: 24px; display: flex; flex-wrap: wrap; gap: 10px; }}
    .pill {{ border: 1px solid rgba(255,255,255,0.26); border-radius: 999px; padding: 6px 12px; color: #ecfeff; font-size: 0.9rem; }}
    main {{ display: grid; grid-template-columns: 260px minmax(0, 1fr); gap: 28px; padding: 30px 24px 64px; }}
    nav {{
      position: sticky;
      top: 18px;
      align-self: start;
      background: rgba(255,255,255,0.78);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
    }}
    nav h2 {{ font-size: 0.82rem; margin: 0 0 10px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); }}
    nav a {{ display: block; color: var(--accent); text-decoration: none; padding: 6px 0; font-size: 0.94rem; }}
    article {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px clamp(18px, 4vw, 42px) 44px;
      box-shadow: 0 18px 60px rgba(23,32,51,0.08);
    }}
    article h1 {{ display: none; }}
    article h2 {{ margin-top: 32px; padding-top: 18px; border-top: 1px solid var(--line); font-size: 1.72rem; line-height: 1.18; }}
    article h2:first-of-type {{ border-top: 0; }}
    article h3 {{ margin-top: 28px; font-size: 1.18rem; }}
    a {{ color: var(--accent); }}
    code {{ background: var(--tint); padding: 0.12em 0.35em; border-radius: 4px; }}
    pre {{ overflow-x: auto; background: #111827; color: #e5e7eb; padding: 16px; border-radius: 8px; }}
    .citation {{ color: var(--accent-2); font-size: 0.88em; text-decoration: none; }}
    .table-wrap {{ overflow-x: auto; margin: 20px 0; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.94rem; }}
    th, td {{ border: 1px solid var(--line); padding: 9px 11px; vertical-align: top; }}
    th {{ background: #f3f7f5; text-align: left; }}
    footer {{ color: var(--muted); border-top: 1px solid var(--line); padding: 24px; }}
    @media (max-width: 860px) {{
      main {{ display: block; padding: 18px 12px 44px; }}
      nav {{ position: static; margin-bottom: 16px; }}
      article {{ padding: 14px 16px 34px; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <div class="eyebrow">Literature review</div>
      <h1>{html.escape(TITLE)}</h1>
      <p class="subtitle">{html.escape(SUBTITLE)}</p>
      <div class="meta">
        <span class="pill">Author: {html.escape(AUTHOR)}</span>
        <span class="pill">Version {html.escape(VERSION)}</span>
        <span class="pill">Audit date: {html.escape(REPORT_DATE)}</span>
        <span class="pill">{manifest.get("count", 0)} references</span>
      </div>
    </div>
  </header>
  <main class="wrap">
    <nav aria-label="Report sections">
      <h2>Sections</h2>
      {nav}
    </nav>
    <article>
      {body}
    </article>
  </main>
  <footer>
    <div class="wrap">
      Generated from <code>deep-research-report.md</code>. Bibliography:
      <a href="references/bibliography.bib">references/bibliography.bib</a>.
    </div>
  </footer>
</body>
</html>
"""
    HTML_OUT.write_text(html_text, encoding="utf-8")
    print(f"Wrote {HTML_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    build_html()
