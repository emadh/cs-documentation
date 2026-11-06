# Catalog progress

Statuses: Not started | In progress | Cataloged | Second-pass verified | Blocked / requires investigation

This file is the session checklist. Stable feature IDs are assigned only in `FEATURE_CATALOG.md` and must not be renumbered later.

Baseline: website commit `e8172b5c35b4e32a77ea28569ae82ad28ed83f8e` on `mobile-responsive`. See `CATALOG_BASELINE.txt`. The next catalog update should diff that commit rather than re-read the whole application.

| Module | Status | Notes |
| --- | --- | --- |
| Page inventory | Cataloged | `PAGE_INVENTORY.md`. Not yet annotated with every feature ID. |
| Shell / navigation | Cataloged | Covered by page inventory and SRCH-001, ACT-006, XFR-012. No separate SHELL IDs. |
| Map and locations | Cataloged | `MAP-001` through `MAP-044` in `FEATURE_CATALOG.md`. |
| Products and product editor | Cataloged | `PRD-*` and `PED-*`. |
| Add products and import | Cataloged | `PED-010` through `PED-014`, workflows WF-001, WF-007, WF-008. |
| Inventory movement | Cataloged | `XFR-*`. Transfer and Start stock math stay separate. |
| Activity | Cataloged | `ACT-*`. |
| Expirations | Cataloged | `EXP-*`, window is `DSP-005`. |
| Kitting | Cataloged | `KIT-*`. Settings toggle remains unwired (`DSP-008`). |
| Settings, team, custom fields | Cataloged | `SET-*`, `TEAM-*`, `CFL-*`, `DEF-*`, `DSP-*`, `ACCSET-*`. |
| Subscription and billing | Cataloged | `SUB-*`. Banners are markup-only. |
| API and Lansweeper | Cataloged | `API-*`, `LSW-*`. Live UI is the support request. |
| Account, login, onboarding | Cataloged | `ACC-*`. Welcome and getting-started redirect to the map. |
| Search | Cataloged | `SRCH-001` and `PRD-006`. |
| Mobile home | Cataloged | `XFR-012`, `XFR-008`, `XFR-009`, `MAP-044`. |
| Second-pass traceability | Not started | `_extract/ui-controls.txt` and `event-handlers.txt` are not yet mapped ID by ID. |
| Workflows | Cataloged | `WORKFLOW_CATALOG.md`, `WF-001` through `WF-013`. |
| Discovery report and maintenance | Cataloged | Maintenance is `.cursor/commands/kb-update.md` in the website repo. A counts report was not given its own file. |

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
