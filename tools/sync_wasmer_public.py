#!/usr/bin/env python3
"""Mirror public static website files from repository root into public/.

This repository keeps editable HTML pages at the root. A Wasmer Staticfile
serves only public/. Never copy README files, .git, tokens or other repository
metadata to the document root.
"""
from pathlib import Path
from shutil import copyfile

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "public"
EXTENSIONS = {".html", ".htm", ".css", ".js", ".mjs", ".svg", ".png",
              ".jpg", ".jpeg", ".webp", ".ico", ".webmanifest"}
SPECIAL = {"robots.txt", "sitemap.xml", "favicon.ico", "site.webmanifest"}
# Never mirror the GitHub Pages-only learning tools to the Wasmer web root.
GITHUB_PAGES_ONLY = {"traffic-roi-calculator.html", "backlink-quality-worksheet.html"}

def source_files():
    for path in sorted(ROOT.iterdir()):
        if path.is_file() and path.name not in GITHUB_PAGES_ONLY and (path.suffix.lower() in EXTENSIONS or path.name in SPECIAL):
            yield path

def main():
    originals = list(source_files())
    names = {p.name for p in originals}
    required = {"index.html", "traffic-to-leads-checklist.html", "styles.css",
                "robots.txt", "sitemap.xml"}
    if not required.issubset(names):
        raise SystemExit(f"Refusing partial publish: missing {sorted(required - names)}")
    DEST.mkdir(exist_ok=True)
    changed = 0
    for src in originals:
        target = DEST / src.name
        content = src.read_bytes()
        if not target.exists() or target.read_bytes() != content:
            target.write_bytes(content)
            changed += 1
    removed = 0
    for existing in DEST.iterdir():
        if existing.is_file() and existing.name not in names:
            if existing.name.startswith("."):
                continue
            existing.unlink()
            removed += 1
    for name in required:
        if not (DEST / name).is_file():
            raise SystemExit(f"Missing required generated asset: {name}")
    print(f"Static mirror verified: {len(originals)} files, {changed} updated, {removed} removed.")

if __name__ == "__main__":
    main()
