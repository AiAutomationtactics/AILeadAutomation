# Free portfolio indexing-readiness monitor

This folder lists only the affiliate/business domains the owner supplied. **Qur'an and Sunnah websites are excluded.**

## Operation
The [Network Index Readiness GitHub Action](../.github/workflows/network-index-readiness.yml) runs daily and on demand. It reads `sites.json`, checks each homepage, `robots.txt`, `sitemap.xml` and at most two same-host sitemap URLs, then publishes an **Actions artifact** with Markdown/CSV/JSON results. It uses Python's standard library, no paid APIs, and no credentials. Hostname checks restrict sitemap inspection to the same owner-provided host.

View results: repository **Actions → Network Index Readiness → latest run → Summary**, or download `index-readiness-report` under Artifacts.

You can run locally: `python3 tools/network_index_monitor.py`. Edit only `monitor/sites.json` to add or remove sites. A missing sitemap is a recommendation, **not proof of a Google indexing problem**. Redirects, anti-bot controls, and transient failures may cause false alarms.

## What it does NOT do
- It does not claim a page is indexed in Google; actual index status needs an authorized Google Search Console URL Inspection API connection.
- It does not auto-submit sitemaps or indexing requests, create backlinks, buy traffic or manipulate search results.
- It does not alter any of the monitored websites or their hosting.
- It does not monitor religious sites; none are in the explicit site allowlist.

Google's guidance: [sitemap submission is a hint](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap); [automated link building can be link spam](https://developers.google.com/search/docs/essentials/spam-policies). The repository's existing `gsc-check.yml` supports authenticated Search Console operations separately, but only after the property and protected credentials are configured.
