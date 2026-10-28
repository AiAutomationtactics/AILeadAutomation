# Authorized Google Search Console connector

**Purpose:** Audit the Google Search Console property `https://leadgflow.vercel.app/` automatically about every three hours, or deliberately submit its sitemap when needed. The connector is for an account with access granted by `arhamawn7861@gmail.com`; merely knowing an email address does not establish authorization.

**Status:** Connector code and GitHub Actions workflow are installed. Google access remains *unconfirmed* until the repository secret is configured and an audit succeeds.

## One-time setup

1. In Google Search Console, verify ownership of the exact URL-prefix property `https://leadgflow.vercel.app/` while signed into the intended Google account. The site's verification meta tag is present publicly.
2. In the desired Google Cloud project, enable **Google Search Console API** and create a service account. Add that service-account email to the verified Search Console property as a **Full user**.
3. Create a service-account JSON key **only if your security policy permits it**. Keep the original JSON on your device, do not paste it into a public issue, source file, chat, or commit. Prefer keyless workload identity in environments that support it.
4. Open this repository's **Settings → Secrets and variables → Actions → New repository secret**. Name it `GSC_SERVICE_ACCOUNT_JSON`. Paste the full original service-account JSON directly into the **protected secret** field, not the source code or a chat message. If you've already configured `GSC_SERVICE_ACCOUNT_JSON_B64` with a base64-encoded JSON key, that also works. Do not use both unless you intend the raw JSON secret to take priority.
5. Optionally configure Actions variables `GSC_PROPERTY` and `GSC_SITEMAP`. The safe defaults are `https://leadgflow.vercel.app/` and `https://leadgflow.vercel.app/sitemap.xml`.
6. Open Actions → Authorized Search Console audit → Run workflow → `audit` to check the Google API connection. A successful run lists the property and sitemap state.
7. If the sitemap is missing, manually choose **Run workflow → submit-sitemap** *once*. Do not continuously submit unchanged sitemaps.

**Security:** Only `contents: read` permissions are granted to the GitHub workflow. The Actions secret is not printed by the connector. Remove Search Console access and revoke any service-account key to disconnect.

**Limitations:** Search Console acceptance of a sitemap does not guarantee indexing or lead generation. Automated runs only check status and never automatically submit or request indexing. The URL Inspection API is read-only and does not request general website indexing.

**Workflow:** [gsc-check.yml](../../.github/workflows/gsc-check.yml)

**Documentation:** https://developers.google.com/webmaster-tools/v1/how-tos/authorizing and https://developers.google.com/webmaster-tools/v1/sitemaps/submit
