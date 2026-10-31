#!/usr/bin/env python3
"""Read-only, low-rate SEO indexing-readiness checks. NOT Google index verification.

Standard library only. Checks known owner-submitted site URLs; no SERP scraping,
backlink creation, mass indexing requests or third-party website submissions.
"""
import csv
import io
import json
import os
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "monitor" / "sites.json"
OUTPUT = ROOT / "reports" / "index-readiness"
USER_AGENT = "AffiliateSiteReadinessMonitor/1.0 (read-only; one daily run)"
MAX_BYTES = 850_000
TIMEOUT = 12


class HeadParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.robots = []
        self.canonicals = []
        self.titles = []
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        props = dict(attrs)
        if tag.lower() == "meta" and (props.get("name") or "").lower() in ("robots", "googlebot"):
            self.robots.append((props.get("content") or "").lower())
        elif tag.lower() == "link" and "canonical" in (props.get("rel") or "").lower().split():
            if props.get("href"):
                self.canonicals.append(props["href"])
        elif tag.lower() == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title and data.strip():
            self.titles.append(data.strip())


def fetch(url):
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html, application/xml, text/xml, text/plain"})
    try:
        with urlopen(request, timeout=TIMEOUT) as resp:
            return {
                "status": resp.status,
                "final_url": resp.url,
                "text": resp.read(MAX_BYTES + 1).decode("utf-8", errors="replace"),
                "x_robots": (resp.headers.get("X-Robots-Tag") or "").lower(),
            }
    except HTTPError as error:
        return {"status": error.code, "final_url": url, "text": "", "x_robots": "", "error": str(error)}
    except (URLError, TimeoutError, OSError, ValueError) as error:
        return {"status": None, "final_url": url, "text": "", "x_robots": "", "error": str(error)[:180]}


def normalize(url):
    parts = urlsplit(url)
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/") or "/", parts.query, ""))


def robots_blocks_all(text):
    """Flag only an unambiguous root-level User-agent: * / Disallow: / rule."""
    agent_star = False
    for raw in text.splitlines():
        line = raw.partition("#")[0].strip()
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip().lower(), value.strip()
        if key == "user-agent":
            agent_star = value == "*"
        elif key == "disallow" and agent_star and value == "/":
            return True
    return False


def sitemap_locs(xml_text):
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return None, []
    root_name = root.tag.rsplit("}", 1)[-1].lower()
    if root_name not in ("urlset", "sitemapindex"):
        return None, []
    found = []
    for node in root.iter():
        if node.tag.rsplit("}", 1)[-1].lower() == "loc" and node.text:
            found.append(node.text.strip())
    return root_name, found


def site_audit(base, sample_limit):
    record = {"site": base, "home_http": "", "robots_http": "", "sitemap_http": "",
              "sampled_pages": 0, "issues": [], "sample_urls": [], "checked_utc": datetime.now(timezone.utc).isoformat()}
    origin = urlsplit(base)
    home = fetch(base)
    record["home_http"] = home["status"] if home["status"] is not None else "unreachable"
    if home["status"] != 200:
        record["issues"].append("Homepage unreachable or non-200 (may be transient or bot-blocked)")
    else:
        parser = HeadParser()
        parser.feed(home["text"])
        if "noindex" in ",".join(parser.robots + [home["x_robots"]]):
            record["issues"].append("Homepage has a noindex directive")
        if not parser.canonicals:
            record["issues"].append("Homepage missing canonical (recommendation, not an indexing block)")
        else:
            canonical = urljoin(home["final_url"], parser.canonicals[0])
            if normalize(canonical) != normalize(home["final_url"]):
                record["issues"].append("Homepage canonical points to " + canonical[:150])
        if normalize(home["final_url"]) != normalize(base):
            record["issues"].append("Homepage redirects to " + home["final_url"][:150])
        if not parser.titles:
            record["issues"].append("Homepage has no HTML title")
    robots_url = urljoin(base, "/robots.txt")
    robots = fetch(robots_url)
    record["robots_http"] = robots["status"] if robots["status"] is not None else "unreachable"
    if robots["status"] == 200:
        if robots_blocks_all(robots["text"]):
            record["issues"].append("robots.txt has a User-agent: * Disallow: / block")
    elif robots["status"] in (404, 410):
        record["issues"].append("No robots.txt (optional; add Sitemap: directive if useful)")
    else:
        record["issues"].append("robots.txt unavailable (verify bot accessibility)")
    sitemap_url = urljoin(base, "/sitemap.xml")
    site_map = fetch(sitemap_url)
    record["sitemap_http"] = site_map["status"] if site_map["status"] is not None else "unreachable"
    if site_map["status"] != 200:
        record["issues"].append("sitemap.xml unavailable (recommended for discovery)")
        return record
    kind, urls = sitemap_locs(site_map["text"])
    if kind is None:
        record["issues"].append("sitemap.xml is invalid XML or not a sitemap")
        return record
    if not urls:
        record["issues"].append("sitemap.xml has no URLs")
        return record
    if kind == "sitemapindex":
        candidate = next((u for u in urls if urlsplit(u).hostname == origin.hostname and urlsplit(u).scheme == "https"), None)
        if candidate:
            child = fetch(candidate)
            if child["status"] == 200:
                _, urls = sitemap_locs(child["text"])
                urls = urls or []
            else:
                urls = []
                record["issues"].append("First sitemap index child is unavailable")
        else:
            urls = []
            record["issues"].append("No same-host HTTPS sitemap-index child")
    if not urls:
        record["issues"].append("No sample URLs available from sitemap")
    if kind == "urlset" and normalize(base) not in {normalize(u) for u in urls}:
        record["issues"].append("Homepage not listed in sitemap (may be intentional)")
    seen = set()
    for url in urls:
        if len(record["sample_urls"]) >= sample_limit:
            break
        if url in seen or urlsplit(url).scheme != "https" or urlsplit(url).hostname != origin.hostname:
            continue
        seen.add(url)
        page = fetch(url)
        record["sample_urls"].append({"url": url, "status": page["status"]})
        if page["status"] != 200:
            record["issues"].append("Sitemap URL non-200: " + url[:130])
        else:
            parser = HeadParser()
            parser.feed(page["text"])
            if "noindex" in ",".join(parser.robots + [page["x_robots"]]):
                record["issues"].append("Sitemap URL has noindex: " + url[:130])
            if parser.canonicals:
                canonical = urljoin(page["final_url"], parser.canonicals[0])
                if normalize(canonical) != normalize(url):
                    record["issues"].append("Sitemap URL canonical differs: " + url[:130])
    record["sampled_pages"] = len(record["sample_urls"])
    return record


def main():
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    sites = config["sites"]
    limit = max(0, min(int(config.get("max_sitemap_pages_per_site", 2)), 5))
    results = []
    for site in sites:
        parts = urlsplit(site)
        if parts.scheme != "https" or not parts.hostname or parts.username or parts.password:
            print("SKIP invalid or non-HTTPS configured site:", site)
            continue
        print("Checking", site, flush=True)
        results.append(site_audit(site, limit))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    (OUTPUT / "report.json").write_text(json.dumps({"checked": now, "results": results}, indent=2) + "\n", encoding="utf-8")
    with (OUTPUT / "report.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["site", "home_http", "robots_http", "sitemap_http", "sampled_pages", "issue_count", "issues"])
        for row in results:
            writer.writerow([row["site"], row["home_http"], row["robots_http"], row["sitemap_http"],
                             row["sampled_pages"], len(row["issues"]), "; ".join(row["issues"])])
    report = [f"# Affiliate SEO readiness monitor — {now}", "",
              "Read-only technical observations, **not confirmed Google indexing**. Check Search Console for actual index status.",
              "", "| Site | Home | Robots | Sitemap | Findings |", "|---|---:|---:|---:|---:|"]
    for row in results:
        report.append(f"| {row['site']} | {row['home_http']} | {row['robots_http']} | {row['sitemap_http']} | {len(row['issues'])} |")
    report += ["", "## Findings", ""]
    for row in results:
        report += [f"### {row['site']}", ""]
        report += [f"- {issue}" for issue in row["issues"]] or ["- No issue detected by these limited checks."]
        report.append("")
    report += ["", "**Scope:** Homepage, robots.txt, sitemap.xml, and up to "
               + str(limit) + " sampled same-host URLs per site. A failed request may reflect network restrictions, bot protections, or temporary downtime.",
               "No content is modified, no backlinks are created, and no automated Google search requests or sitemap re-submissions occur."]
    markdown = "\n".join(report) + "\n"
    (OUTPUT / "report.md").write_text(markdown, encoding="utf-8")
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as out:
            out.write(markdown[:180_000])
    print(f"Completed {len(results)} sites; {sum(len(x['issues']) for x in results)} findings. See reports/index-readiness/.")


if __name__ == "__main__":
    main()
