# AI Lead Automation setup checklist

This repository contains ten public, original educational pages plus a home page, an about page and a noindex link archive. It does not promise search rankings or earnings.

## Deployment

Publish the repository root as static files on Wasmer. Verify the exact production domain and that `/index.html`, `/styles.css`, `/resources.html`, and the interactive tools load correctly. The archive intentionally carries `noindex,follow` and contains unverified owner-supplied link references, not endorsements.

## Final-domain SEO (requires the actual Wasmer hostname)

1. Add accurate absolute canonical URL tags to each indexable HTML page based on its production URL.
2. Generate a valid `sitemap.xml` with the full HTTPS production URL for the home page and ten article pages, plus the about page. Do not add `resources.html` because it is noindex.
3. Add `Sitemap: https://YOUR-REAL-DOMAIN/sitemap.xml` to `robots.txt` after the sitemap is live.
4. Verify ownership in Google Search Console and submit the sitemap there; don't assume indexing or rankings.
5. Use a mobile browser to test links, headings, keyboard focus, and two in-page tools.
6. Keep external claims verified; archive links are not independently validated.

No guessed production host has been embedded. Structured data uses Organization and Article only, avoiding invented reviews or credentials. External affiliate URLs are clearly disclosed and marked sponsored/nofollow. The home page links to the archive only once in its introduction and through common navigation.

## Publishing standards

Every new page must solve a new reader task, include realistic limitations and actionable examples, be linked from navigation, and avoid repeating previous content for keywords alone. Prefer fewer pages to ten thin or templated pieces. Update existing material when that is more useful.
