# AI search SEO + Wasmer checklist (October 23, 2026)

This repository contains existing educational guides and five additional AI-search-oriented guides. The optional SendSteed form submits externally. One affiliate-disclosure guide includes the owner-supplied WarriorPlus widget, a third-party script.

## Before domain-specific SEO is finalized
1. In Wasmer, confirm this GitHub repository is attached to the correct Edge app, with production branch `main`. Changing GitHub code does **not** prove Wasmer deployed it.
2. Confirm the **exact** public HTTPS hostname. No guessed Wasmer hostname is hard-coded into sitemap or canonical tags.
3. From a checkout, run `python3 tools/finalize_seo.py https://YOUR-ACTUAL-DOMAIN` to generate `sitemap.xml`, update `robots.txt`, and add per-page canonical links. Replace placeholder with the real live URL. Commit generated changes to the deployment branch.
4. Verify the property in Google Search Console; submit the sitemap and inspect pages. Do not promise indexing or AI Overview appearances.
5. Open the email form on desktop/mobile, validate provider consent/unsubscribe settings, and test the external WarriorPlus widget's privacy/performance impact. The owner must add an actual contact method to `privacy.html` before collecting large mailing lists.
6. Keep `resources.html` noindex and retain `rel="sponsored"` on paid referrals. Only link contextually in editorial articles. Avoid fabricated product testing, review ratings and broad earnings claims.
7. Five additional pages per day for twenty days is an editorial *target*. `EDITORIAL_CALENDAR.md` has 95 remaining ideas. They are **not** auto-generated; each must pass a human value and accuracy review before publication. Frequency should never override quality.

Official reading: https://developers.google.com/search/docs/appearance/ai-features and https://developers.google.com/search/docs/essentials/spam-policies
