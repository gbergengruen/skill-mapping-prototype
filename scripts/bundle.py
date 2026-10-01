#!/usr/bin/env python3
"""Unpack / repack the prototype template inside the self-contained index.html.

  python3 scripts/bundle.py unpack   # index.html -> src/template.html
  python3 scripts/bundle.py pack     # src/template.html -> index.html

Only the template (markup + logic) is edited. The asset manifest (runtime,
React, fonts, iOS frame) inside index.html is left untouched.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
TEMPLATE = ROOT / "src" / "template.html"

TEMPLATE_RE = re.compile(r'(<script type="__bundler/template">)(.*?)(</script>)', re.S)
TITLE = "Skill Mapping — prototype"
FAVICON = (
    '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 100 100%27%3E'
    '%3Crect width=%27100%27 height=%27100%27 rx=%2722%27 fill=%27%231cabe2%27/%3E%3Ctext x=%2750%27 y=%2766%27 '
    'text-anchor=%27middle%27 font-family=%27system-ui,sans-serif%27 font-size=%2744%27 font-weight=%27700%27 '
    'fill=%27%23fff%27%3ESM%3C/text%3E%3C/svg%3E">'
)
THUMB = (
    '<div id="__bundler_thumbnail"><svg xmlns="http://www.w3.org/2000/svg" '
    'sc-camel-view-box="0 0 100 100"><rect width="100" height="100" fill="#1cabe2"></rect>'
    '<text x="50" y="62" text-anchor="middle" font-family="system-ui,sans-serif" '
    'font-size="34" font-weight="700" fill="#fff">SM</text></svg></div>'
)


def unpack():
    html = INDEX.read_text(encoding="utf-8")
    m = TEMPLATE_RE.search(html)
    TEMPLATE.parent.mkdir(exist_ok=True)
    TEMPLATE.write_text(json.loads(m.group(2)), encoding="utf-8")
    print(f"wrote {TEMPLATE.relative_to(ROOT)}")


def pack():
    html = INDEX.read_text(encoding="utf-8")
    encoded = json.dumps(TEMPLATE.read_text(encoding="utf-8"), ensure_ascii=False)
    encoded = encoded.replace("</", "<\\u002F")
    m = TEMPLATE_RE.search(html)
    html = html[: m.start(2)] + "\n" + encoded + "\n  " + html[m.end(2):]
    html = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", html, count=1)
    if 'rel="icon"' not in html:
        html = html.replace("</title>", "</title>\n  " + FAVICON, 1)
    html = re.sub(r'<div id="__bundler_thumbnail">.*?</div>', THUMB, html, count=1, flags=re.S)
    INDEX.write_text(html, encoding="utf-8")
    print(f"wrote {INDEX.relative_to(ROOT)}")


if __name__ == "__main__":
    {"unpack": unpack, "pack": pack}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: sys.exit(__doc__))()
