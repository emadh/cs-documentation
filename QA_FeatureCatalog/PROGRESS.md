# Catalog progress

Statuses: Not started | In progress | Cataloged | Second-pass verified | Blocked / requires investigation

This file is the session checklist. Stable feature IDs are assigned only in `FEATURE_CATALOG.md` and must not be renumbered later.

| Module | Status | Notes |
| --- | --- | --- |
| Page inventory | In progress | `PAGE_INVENTORY.md` drafted from masters, routes, and code-behind visibility |
| Shell / navigation | In progress | `UserPage.master`, `MOBILE_MasterPage.master` |
| Map and locations | In progress | Parallel code trace of `Map_CONTROL_2017.ascx` and location editors |
| Products and product editor | In progress | Products grid, editor, clone, delete, images, documents, barcodes |
| Add products and import | In progress | `AddProducts.aspx`, `ImportFromFile.aspx` |
| Inventory movement | In progress | Start, Transfer, map drag, mobile process, QuickScan |
| Activity | In progress | History, details, filters, export |
| Expirations | In progress | Page plus display settings |
| Kitting | In progress | Page exists; Settings kitting toggle is `display:none` |
| Settings, team, custom fields | Cataloged | Research in `_research/SETTINGS_ACCOUNT.md`. IDs `SET-*`, `TEAM-*`, `CFL-*`, `DEF-*`, `DSP-*`, `ACCSET-*` in `FEATURE_CATALOG.md`. Second pass not done. |
| Subscription and billing | Cataloged | IDs `SUB-*`. Banners are markup-only. Stripe self-serve is conditional. |
| API and Lansweeper | Cataloged | Live UI is request-access. Popup pipeline recorded as not linked from Settings (`LSW-*`, `API-*`). |
| Account, login, onboarding | Cataloged | IDs `ACC-*`. Welcome redirects to Map and is not a wizard. Getting-started guide is still with the activity trace. |
| Search | In progress | Global `CS_SearchBox` |
| Mobile home | In progress | `mobile_main.aspx` |
| Second-pass traceability | Not started | Compare `_extract/ui-controls.txt` and `event-handlers.txt` to catalog IDs |
| Workflows | Not started | After feature IDs exist |
| Discovery report and maintenance | Not started | After counts are stable |

## Confirmed access rules (do not rediscover)

- Logged-out users hitting `UserPage.master` are redirected to `/Login.aspx` (`UserPage.master.vb` `Page_Init`).
- Roles in `User_Legacy.TypeOfUserAccount`: ADMIN, USER, SUPER_USER, MOBILE (legacy, treated as USER by `GetEffectiveUserType`), READ_ONLY.
- Read-only users lose Start, Add Products, Tools submenu, and the collapsed Check In / Check Out / Transfer / QuickScan group (`HideSectionsForReadOnlyUsers`).
- If the account has zero products, Start and the collapsed inventory actions are hidden for non-read-only users.
- Expirations and Kitting nav icons appear only when `SHOW_EXPIRATIONS` / `SHOW_KITTING` is 1 on the user row.
- Billing gate (`BillingAccessGate.Enforce`): expired trial (unless `SuppressUpgradeAlert`) or delinquent confirmed payment (unless `SuppressPaymentAlert`) redirects every authenticated page except Settings to `/Settings`.
- Settings section visibility is in `Settings.aspx.vb` `ShowAllowedMenu` / `ShowAllowedSections`. SUPER_USER has no Case and is not remapped to ADMIN. Recorded as uncertain whether any live user still has that role.
- `InitLansweeper()` is commented out. The Lansweeper settings block tells admins to email support. Sync and disconnect buttons are inside an ASP comment.
- The Kitting display toggle in Settings is inside `<tr style="display: none;">`.

## Extraction artifacts

- `QA_FeatureCatalog/_extract/ui-controls.txt`
- `QA_FeatureCatalog/_extract/event-handlers.txt`
- Module research notes (when written): `QA_FeatureCatalog/_research/`
