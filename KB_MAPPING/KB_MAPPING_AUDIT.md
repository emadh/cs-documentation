# Knowledge base mapping audit

## What was retrieved

- Live sitemap: https://cyberstockroom.helpscoutdocs.com/sitemap.xml on 6 Nov 2026.
- Article titles, categories, and URLs: `CyberStockroom_KB_Article_URLs.csv`. All 55 URLs were also in the sitemap.
- Category descriptions retrieved from the live category pages: Getting Started, Products & Inventory, Inventory Operations.
- Category descriptions not retrieved: Map & Locations, Search, Activity & Reports, Team & Account Settings, Advanced Features & Integrations, Troubleshooting & FAQs. Names and URLs for those categories are from the sitemap and the CSV. Their descriptions were not invented.
- Individual article bodies and summaries: not retrieved. Every article file says so.

## Counts

- Categories: 8
- Articles: 55
- Feature IDs examined: 151
- Primary coverage: 134
- Supporting coverage only: 3
- Internal only: 10
- Coverage gaps: 3
- Needs investigation as the disposition: 1
- Unmapped: 0

## Internal-only features

- ACC-006 — Welcome.aspx redirects to the map before any wizard runs. Do not publish a welcome wizard.
- DSP-008 — The Settings kitting checkbox is hidden and unwired. Do not publish it as the way to turn kitting on.
- KIT-003 — The kit Manage button builds invalid JavaScript and is a copy of the expiration wizard. Do not publish it.
- LSW-002 — Site picker exists but is not linked from current Settings.
- LSW-003 — Field-match popup is not linked from current Settings. Stored pairing was not fully traced.
- LSW-004 — Category-to-location match is not linked from current Settings.
- LSW-005 — Link, sync, and progress popups are not linked from current Settings. Duplicate class binding is unverified.
- PED-017 — Document Editor buttons are literal text with no handlers. Not product attachments.
- PED-018 — Old clone popup, quantity-only delete dialog, SuccessProducts, and batches are not on the live click path.
- XFR-010 — Legacy mobile product list and Quick Add are not the live auto path. Quick Add creates a catalog row and does not check it in.

## Coverage gaps

- KIT-001 and KIT-002. Kitting has no article. Workflow WF-012 has no article either. The Settings switch that might have been expected is hidden and unwired. The component editor has confirmed defects. Do not write a tutorial that says quantity edit and remove work.
- RPT-002. The AI insights page has no menu link and its generator was not in the website files that were read.

## Needs investigation inside articles that do exist

- ACC-015 OAuth scope text, on the API article only as a do-not-write.
- EXP-002 stock effect of each replace or clone radio.
- XFR-011 and the kiosk article: Quick Scan stock math.
- MAP-013 whether a structure clone copies quantities.
- SRCH-001 and MAP-018 match fields.
- productDeleter cascade on delete articles.
- Read-only map drag.
- Some transfer-import skip sentences.

## Suggested new articles

Do not create these in Help Scout until the behavior is safe to document.

1. Kits. Cover KIT-001 only, and say KIT-002 quantity edit and same-quantity delete are not reliable. Do not mention KIT-003 or the Settings kitting checkbox.
2. AI inventory insights. Cover RPT-002 only after the page is linked from the product and the generator can be described. Until then, leave it out.

## Structure notes

- Getting Started overlaps the dedicated map, product, import, and check-in articles. Keep the first-15-minutes article short and link out.
- Understanding Inventory Actions overlaps the three how-to articles. Use it for the Start page and for the difference between Start and Transfer.
- Searching and Finding Products and Finding Products and Locations with Search are different searches. Do not merge them.
- Understanding Products and Quantities, Changing Inventory Quantities Directly, and Understanding Inventory Values overlap. Keep quantities, direct edits, and cost columns in those three articles.
- No article should absorb kitting, the AI report, or the unlinked Lansweeper sync screens.

## Ready for the documentation agent

Yes, for the 55 existing articles, with the publication restrictions in each handoff file. Not ready to document kits, the AI report, OAuth scopes, or external API stock math as confirmed behavior.

No website code and no Help Scout article was edited.
