#!/usr/bin/env python3
"""Read-only sitemap consistency check for the site's indexable root HTML.

Usage: python3 tools/check_search_indexing.py
Designed to fail CI before a stale sitemap is mirrored into public/.
Does not contact a search engine or claim a deployed URL is crawlable.
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = "https://masteraffiliate.wasmer.app"
ROBOTS_META = re.compile(r'<meta\b[^>]*name=["\']robots["\'][^>]*>', re.I)
CONTENT = re.compile(r'content=["\']([^"\']+)["\']', re.I)


def is_indexable(html: Path) -> bool:
    source = html.read_text(encoding="utf-8")
    for tag in ROBOTS_META.findall(source):
        match = CONTENT.search(tag)
        if match and "noindex" in {s.strip().lower() for s in match.group(1).split(",")}:
            return False
    return True


def main() -> int:
    eligible = {
        ORIGIN + ("/" if p.name == "index.html" else "/" + p.name)
        for p in ROOT.glob("*.html") if is_indexable(p)
    }
    try:
        xml = ET.parse(ROOT / "sitemap.xml")
    except (ET.ParseError, OSError) as exc:
        print(f"ERROR: cannot parse sitemap.xml: {exc}", file=sys.stderr)
        return 1
    actual = [
        (node.text or "").strip()
        for node in xml.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    ]
    missing = sorted(eligible - set(actual))
    extra = sorted(set(actual) - eligible)
    duplicates = sorted({u for u in actual if actual.count(u) > 1})
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    errors = []
    if missing: errors.append("Missing eligible pages from sitemap: " + ", ".join(missing))
    if extra: errors.append("Extra or noindex URLs in sitemap: " + ", ".join(extra))
    if duplicates: errors.append("Duplicate URLs: " + ", ".join(duplicates))
    if ("Sitemap: " + ORIGIN + "/sitemap.xml") not in robots:
        errors.append("robots.txt does not declare the matching sitemap origin")
    if errors:
        print("\n".join("ERROR: " + err for err in errors), file=sys.stderr)
        return 1
    print(f"OK: {len(eligible)} indexable HTML pages agree with sitemap.xml; noindex pages excluded.")
    print("Note: source checks do not verify live deployment, actual bot access or indexing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
