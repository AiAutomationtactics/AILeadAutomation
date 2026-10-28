# Traffic-to-leads launch and measurement checklist

Updated: 2026-10-28
Repository: https://github.com/AiAutomationtactics/AILeadAutomation
Owner-designated production hostname (NOT verified live): https://masteraffiliate.wasmer.app/
Proposed public worksheet after deployment: https://masteraffiliate.wasmer.app/traffic-to-leads-checklist.html

## What was changed
- Added \`traffic-to-leads-checklist.html\`: a complete free seven-point educational worksheet, available without signup.
- Linked the worksheet from the homepage hero and a prominent explanatory section.
- Added an **optional** SendSteed subscription form with an explicit required consent checkbox and candid explanatory copy.
- Added one contextual sponsored LeadsLeap referral and nearby plain-language disclosure.
- No tracking scripts, forced redirects, checkout buttons, bulk-posting workflow, artificial traffic generator or guarantees were added.
- The website's unindexed \`resources.html\` archive stays unchanged.

## Required checks before promoting the new page

1. **Verify hosting:** In the authorized Wasmer workspace confirm the app actually deploys this repo's \`main\` branch. Confirm HTTPS and status 200 for homepage, stylesheet, worksheet, robots and sitemap. A GitHub commit alone is not deployment.
2. **Confirm exact canonical:** Open view source on the live worksheet and ensure the canonical and OG URL reflect the real public hostname. If production host is different, use the repo's \`tools/finalize_seo.py\` only after confirming the real host.
3. **Update sitemap only after verifying live route:** Existing \`sitemap.xml\` may be incomplete and its older URLs unverified. When the worksheet truly loads on production with an indexable canonical, add its actual canonical URL. Don't submit unverified URLs or claim Search Console indexing.
4. **Email provider QA:** The form POSTs to \`https://www.sendsteed.com/subscribe/\` with email \`e98460\`, name \`n98460\`, \`lllid=98460\`, \`lluid=awanraheel0\`. Confirm these parameters remain correct in the *owner's* SendSteed account. Use a consented test inbox, verify confirmation/processing, suppression and unsubscribe. Never count form clicks as subscribed leads. Verify whether SendSteed records the checkbox/consent evidence; custom HTML field presence does not establish stored consent.
5. **Compliance before email campaigns:** Add and verify required sender identification, valid physical mailing address where applicable, working contact method and unsubscribe handling in messages and provider configuration (e.g., Canadian CASL). Do not broadcast until these are configured.
6. **Referral QA:** The visible link is \`https://leadsleap.com/?r=awanraheel0\`. Check current merchant rules and whether attribution is credited in the actual affiliate dashboard. Commission eligibility, click counts and purchases cannot be inferred from a functioning link.
7. **Mobile and accessibility:** Test 320px and desktop views, form labels, contrast, focus, link destinations and reading order. Confirm the checkbox requirement does not accidentally block free worksheet access (it must not).
8. **Privacy:** Never commit subscriber details, CRM exports, login credentials, analytics secrets, provider tokens or tracked personal information to this Git repository.

## Organic, distinct social content ideas (drafts only; not posted)
Only use profiles the owner has explicitly approved for the relevant campaign, and only through a correctly authenticated supported integration.

### Instagram educational carousel
Goal: help beginners recognize three parts of a working funnel. Frames: (1) "More clicks are not a plan"; (2) "Match the post to the page"; (3) "Give the reader something useful"; (4) "Make email optional"; (5) "Measure confirmed results." CTA: "Use the free seven-point traffic-to-leads checklist at the link in bio (only when the page is live)." No affiliate link in the image itself.

### YouTube Short
Hook: "Before you buy traffic, check these three things." Script: "One: Does your post promise exactly what the landing page provides? Two: Can visitors get the useful resource without handing over an email? Three: Are you measuring actual signups separately from clicks? You can use our free seven-point checklist to test your own funnel." Description: "Free worksheet: [verified deployed URL]. Affiliate links, if added later, must have a visible disclosure." No guaranteed results.

### Pinterest educational Pin
Title: "Free Traffic-to-Leads Checklist: Seven Checks Before Promoting"
Visual: a three-stage schematic using non-human icons for relevant content → useful page → optional signup, plus a large clear checklist headline. Description: "A free worksheet for beginner affiliate marketers: message match, mobile page checks, consent-based email signup and genuine measurement. No signup is required to read it." Link to the real live worksheet only after verification. Provide descriptive alt text.

## Source-of-truth measurement sheet

| Metric | Record from | Meaning | Do not confuse with |
| --- | --- | --- | --- |
| Content impressions | Platform analytics | Views of a post | Site visitors |
| Landing-page sessions | Website analytics | Sessions, with attribution limitations | Unique people |
| Form submissions | SendSteed request logs (if available) | Attempts, not necessarily confirmed | Consented subscribers |
| Confirmed subscribers | SendSteed subscriber status | Confirmed permission-based leads | Purchasers |
| Affiliate referral clicks | LeadsLeap dashboard | Tracked clicks | Purchases |
| Verified commissions | LeadsLeap payout/commission record | Recorded commission, subject to program terms | Guaranteed cash receipts |

Use the same calendar date range and timezone when comparing. Do not save sensitive contact data here.

## Remaining blockers as of October 28, 2026
- Wasmer production URL was inaccessible to the assistant's public web check; deployment not confirmed.
- GitHub connector can commit source but cannot establish Wasmer deployment or Search Console indexing.
- SendSteed signup/double opt-in, consent recordkeeping and delivery have not been tested via owner access.
- Mailing address and unsubscribe configuration for commercial emails have not been verified.
- No verified analytics or affiliate sales data is available through this GitHub repository.
