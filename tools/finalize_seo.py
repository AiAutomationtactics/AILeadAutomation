#!/usr/bin/env python3
"""Finalize canonical URLs and XML sitemap for a known deployed static-site domain.

Usage: python3 tools/finalize_seo.py https://your-actual-domain.example
No remote calls; only uses standard library.
"""
import re
import sys
from pathlib import Path
from urllib.parse import urlparse
from xml.etree.ElementTree import Element, SubElement, ElementTree

root = Path(__file__).resolve().parent.parent
if len(sys.argv) != 2:
    raise SystemExit("Usage: python3 tools/finalize_seo.py https://YOUR-EXACT-PRODUCTION-HOST")
base = sys.argv[1].strip().rstrip("/")
parsed = urlparse(base)
if parsed.scheme != "https" or not parsed.netloc or parsed.path not in ("", "/") or parsed.query or parsed.fragment:
    raise SystemExit("Provide an HTTPS origin with no path/query, e.g. https://real-site.wasmer.app")
if "YOUR-" in base.upper() or "EXAMPLE" in parsed.netloc.upper():
    raise SystemExit("Please provide the real deployed hostname, not a placeholder.")

ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
urlset = Element("urlset", xmlns=ns)
count = 0
for p in sorted(root.glob("*.html")):
    body = p.read_text(encoding="utf-8")
    if re.search(r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex', body, re.I):
        continue
    preferred = base + ("/" if p.name == "index.html" else "/" + p.name)
    tag = '<link rel="canonical" href="' + preferred + '">'
    if re.search(r'<link\s+rel=["\']canonical["\'][^>]*>', body, re.I):
        body = re.sub(r'<link\s+rel=["\']canonical["\'][^>]*>', tag, body, count=1, flags=re.I)
    else:
        body = body.replace("</head>", tag + "</head>", 1)
    p.write_text(body, encoding="utf-8")
    SubElement(SubElement(urlset, "url"), "loc").text = preferred
    count += 1

ElementTree(urlset).write(root / "sitemap.xml", encoding="utf-8", xml_declaration=True)
(root / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: " + base + "/sitemap.xml\n", encoding="utf-8")
print(f"Updated {count} pages, robots.txt and sitemap.xml for {base}")
