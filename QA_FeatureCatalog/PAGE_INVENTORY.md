# CyberStockroom page inventory

Code-grounded inventory of user-facing pages and shared UI. Marketing landing pages, SEO pages, blog posts, case studies, and internal `_admin` tools are listed only in the exclusion section.

Routes use ASP.NET friendly URLs (`App_Code/RouteConfig.vb`), so `/Products` and `/Products.aspx` are the same page.

Confidence: page existence, master page, and the permission rules below are confirmed in source. Detailed feature behavior is cataloged separately in `FEATURE_CATALOG.md`. Feature IDs are listed in `SUMMARY.md`. This inventory matches website commit `e8172b5c35b4e32a77ea28569ae82ad28ed83f8e` (see `CATALOG_BASELINE.txt`).

## Access model

| Rule | What the user experiences | Code |
| --- | --- | --- |
| Not signed in | Any page on `UserPage.master` redirects to `/Login.aspx` | `UserPage.master.vb` `Page_Init` |
| Read-only | No Start menu, no Add Products, no Tools menu (Quickscan / Mobile Web), no collapsed Check In / Check Out / Transfer / QuickScan | `HideSectionsForReadOnlyUsers` |
| Account has no products | Start menu and collapsed Check In / Check Out / Transfer are hidden. QuickScan in that group stays. Does not apply to read-only (those items are already hidden). | `HideInventoryActionsWhenAccountHasNoProducts` |
| Expirations flag off | Expirations icon in the Products menu and the mobile Expirations link stay hidden | `hidden_expiration_on` from `UserCredentials.SHOW_EXPIRATIONS` |
| Kitting flag off | Kitting icon in the Products menu stays hidden | `hidden_kitting_on` from `UserCredentials.SHOW_KITTING` |
| Trial expired | Sent to Settings until a plan is chosen, unless `SuppressUpgradeAlert` | `BillingAccessGate.Enforce` |
| Payment delinquent | Sent to Settings until payment is updated, unless `SuppressPaymentAlert`. Requires `ConfirmedPayment = 1`. | `BillingAccessGate.Enforce` |
| Blank profile name | Profile setup popup (`ProfileRequired.aspx`) is opened from the master page | `OpenProfilePopupIfNameBlank` |

Roles stored on the user (`User_Legacy.TypeOfUserAccount`):

| Role | Effective role | Settings they can open |
| --- | --- | --- |
| ADMIN | ADMIN | Profile, team, custom fields, default locations, API, Lansweeper request block, display settings, share-map-layout, account settings (time zone, currency), subscription |
| USER | USER | Profile, team, custom fields, default locations, API, display settings. No Lansweeper section, no account settings, no subscription. Share-map-layout row is admin-only. |
| READ_ONLY / READ-ONLY | READ_ONLY | Profile, custom fields, API, display settings. No team, default locations, Lansweeper, account settings, or subscription. |
| MOBILE | Treated as USER | Same as USER. Legacy database value. Badge markup for "Mobile" still exists on the profile. |
| SUPER_USER | Not remapped | Comment says "Multiple Admin Accounts". `ShowAllowedMenu` has no case for it, so Settings sections stay `visible=false`. No other app branch was found that grants this role a distinct UI. Status: uncertain / possibly unused. |

Settings menu icons (`Settings.aspx`): Profile & Team, Custom Fields, Default Locations, Integrations, Options, Subscription Plan. Each icon is shown only when the matching `section_menu_*` control is visible.

## Application shell

| ID | Surface | Route / host | Purpose | Who | How users get there |
| --- | --- | --- | --- | --- | --- |
| PG-SHELL-DESKTOP | Desktop header | `UserPage.master` | Logo, global search, Start / Map / Products, activity, tools, help, account menu | Signed-in users | Wrapped around main pages |
| PG-SHELL-MOBILE-NAV | Hamburger menu | Same master, narrow layout | Home, Map, map lock, ABC sort, shared maps, Products, Expirations, Activity, Check In, Check Out, Transfer, QuickScan, tablet mode, Help, Settings, Logout | Signed-in; inventory actions hidden for read-only | Hamburger on the header |
| PG-SHELL-MOBILE | Mobile chrome | `MOBILE_MasterPage.master` | Mobile header and menu for the mobile page set | Signed-in | Mobile pages |
| PG-SHELL-NOMENU | Popup chrome | `UserPageNoMenu.master` | Pages opened in a Fancybox or full-screen overlay without the main menu | Signed-in (page code-behind still loads the account) | Links from other pages |

Desktop header actions confirmed in `UserPage.master`:

- Logo goes to `/Map` on desktop and `MOBILE_main` on a phone-class device (`userPageHeaderLogoNavigate`).
- Start opens a hover menu: Check In (`/Start?checkin=true&id=-2`), Transfer (`/Start?transfer=true&id=-2`), Check Out (`/Start?checkout=true&id=-2`).
- Map goes to `Map`.
- Products hover: View Products (`Products?clear=true`), Create (`/AddProducts`, hidden for read-only), Expirations, Kitting.
- Activity icon goes to `ActivityHistory` and shows a popup of the latest activity plus "View Activity History".
- Tools: Quickscan (`Popups/QuickScan.aspx`), Mobile Web (`MOBILE_main`). Hidden for read-only.
- Help: video list, Search Topics, Email Support (Groove widget).
- Account menu: Settings, Tools submenu, Logout.

Global search is `Controls/CS_SearchBox.ascx`. It raises location search, product search, and free-text query search into the master page.

`?printable=true` on a user page runs `makePrintable()` (`UserPage.master.vb`).

Leaving the Products or Product Editor path clears the product search cookie and the "keep view" cookie. `Products?clear=true` also resets the location view filter to all locations (`LocationID_VIEW = -2`) and redirects to `/Products`.

## Primary pages

| ID | Page | Route | Master | Purpose | Who | Navigation |
| --- | --- | --- | --- | --- | --- | --- |
| PG-LOGIN | Login | `/Login.aspx` | Landing master | Sign in, Google sign-in, password reset | Signed-out | Direct, or redirect from a protected page |
| PG-MAP | Map | `/Map` | User page | Visual inventory map | Signed-in. Read-only uses a restricted control mode. | Header MAP, logo on desktop |
| PG-MAP-RO | Map read-only | `/Map_read_only.aspx` | User page | Read-only map host | Read-only path | Separate page; confirm which entry points redirect here during feature trace |
| PG-PRODUCTS | Products | `/Products` | User page | Product grid, search, columns, bulk actions | Signed-in. Delete and multi-edit are on the editable page only. | Products menu "view", or `Products?clear=true` |
| PG-PRODUCTS-RO | Products read-only | `/Products_read_only.aspx` | User page | Product grid without delete or multi-edit. Export and print barcodes remain. | Read-only | Feature trace must confirm the redirect from `/Products` |
| PG-START | Start | `/Start` | User page | Batch check-in, check-out, and transfer workspace | Hidden for read-only and for accounts with no products | Start menu |
| PG-ACTIVITY | Activity history | `/ActivityHistory` | User page | Filterable activity list and report download | Signed-in | Activity icon |
| PG-EXPIRATIONS | Expirations | `/Expirations` | User page | Products approaching or past expiration | Shown when `SHOW_EXPIRATIONS` is on | Products menu, mobile menu |
| PG-EXPIRATIONS-RO | Expirations read-only | `/Expirations_read_only.aspx` | User page | Read-only expirations list | Read-only when expirations are on | Feature trace must confirm the switch |
| PG-KITTING | Kitting | `/Kitting` | User page | Kit definitions and kit inventory | Shown when `SHOW_KITTING` is on | Products menu |
| PG-SETTINGS | Settings | `/Settings` | User page | Profile, team, fields, defaults, API, display, account, subscription | Signed-in; sections vary by role | Account menu, mobile menu, billing gate |
| PG-MOBILE-HOME | Mobile home | `/mobile_main.aspx` (`MOBILE_main`) | Mobile master | Mobile launcher | Signed-in | Tools "Mobile Web", phone logo, hamburger Home |

## Editors, dialogs, and secondary pages

These use `UserPageNoMenu.master` unless noted. Most open in a Fancybox iframe from a parent page. On a narrow layout the master page uses its own bottom-sheet iframe instead of Fancybox.

| ID | Page | Route | Purpose | Typical opener |
| --- | --- | --- | --- | --- |
| PG-ADD | Add products | `/AddProducts` | Create one or more products; can hand off to import or to check-in | Products menu Create; `btn_Add` on Products |
| PG-IMPORT | Import from file | `/ImportFromFile.aspx` | Spreadsheet import | Add Products "import from file" |
| PG-CHECKIN-CREATED | Check in new products | `/CheckInCreatedProducts.aspx` | Place just-created products into a location, or skip | After create |
| PG-CHECKIN-CREATED-DONE | Check-in finished | `/CheckInCreatedProductsDone.aspx` | Completion screen. No code-behind. | After check-in of created products |
| PG-EDITOR | Product editor | `/ProductEditor.aspx` | Edit one product: fields, image, attachment, clone, delete, quantity map | Product row / name |
| PG-EDITOR-RO | Product editor read-only | `/ProductEditor_read_only.aspx` | View a product without edit handlers for clone, image, attachment, delete | Read-only product open |
| PG-CLONE | Old clone popup | `/Popups/CloneProduct.aspx` | Fields are locked and there is no save button. The live clone is a modal on Product Editor. No other page links here. | Direct URL only | Not the live clone |
| PG-DELETE-PRODUCT | Delete products confirm | `/Dialogs/ProductDeleteConfirmation.aspx` | Confirm product deletion | Products delete |
| PG-CONFIRM | Generic confirm | `/ConfirmationDialog.aspx` | Yes/delete confirmation. Map delete uses `?ACTION=DELETE&LocationID=` | Map delete |
| PG-FIXED-FIELDS | Fixed multi fields | `/Popups/FixedMultiFields.aspx` | Save preset values for a multi-value field | Product / custom field UI |
| PG-LOC-EDITOR | Location editor | `/LocationEditor.aspx` | Edit an existing location (`LoadType=EXISTING&LocationID=`) or create. Child list, barcode, attachment. | Map Edit |
| PG-NEW-LOC | New location | `/NewLocation.aspx` | Create-location popup (`fancybox-new_location`) | Map add toolbox |
| PG-PEEK | Location peek | `/Popups/PeekLocationDetails.aspx` | Read-only location contents | Map `READ_ONLY` action |
| PG-TRANSFER | Transfer workspace | `/Transfer.aspx` | Move quantities between two locations. Also used for map drag when more than one unit is involved. | Start, or map drop on a wide layout (`callFancyBoxTransfer`) |
| PG-QUICKSCAN | QuickScan | `/Popups/QuickScan.aspx` | Desktop barcode scan popup | Tools menu |
| PG-SELECTOR | Product selector | `/ProductSelector.aspx` | Pick products, with a location filter | Called by transfer / process flows |
| PG-PRINT | Print barcodes | `/PrintBarcode.aspx` | Barcode label preview | Products "Print barcodes" |
| PG-EXPORT | Export report | `/ExportReport.aspx` | Build and download a product/quantity report. Location selector included. | Products download; map "Download Quantity Report" opens a related modal on the map itself |
| PG-ACTIVITY-DETAIL | Activity details | `/ActivityDetails.aspx` | One activity record | Activity history row |
| PG-DOC | Document editor | `/DocumentEditor.aspx` | View or edit an attached document | Product or location attachment |
| PG-PROFILE | Required profile | `/ProfileRequired.aspx` | Force a display name (and related profile fields) | Auto-opened when the name is blank |
| PG-WELCOME | Welcome | `/Welcome.aspx` | Immediately redirects to `/Map`. The profile and demo-data code below that redirect does not run. | Any request to the page | Not a setup wizard |
| PG-GUIDE | Getting started | `/pages/guides/getting-started.aspx` | `Page_Init` redirects to `/Map` before the wizard runs. The step machine remains in the file and is not reachable on this request. | Direct URL, and older redirects from Welcome and `map_demo` | Not a live wizard |
| PG-UPDATE-ACCOUNT | Update account | `/UpdateAccount.aspx` | Monthly and annual Stripe checkout. Enterprise image has no click. `?Update=Payment` updates the card. `?Update=Plan` changes the plan. | Blocks read-only only. It does not require Admin. | Subscription “Update Plan” / “Change Card”, and the signup iframe |
| PG-UPDATE-ALERT | Plan or payment alert | `/UpdateAlert.aspx` | Banner plus an iframe of Update Account. Current query handling makes the trial sentence unreachable. Settings does not auto-open this page. | Hidden anchors on Settings | Not confirmed as a live step |
| PG-BILLING | Billing history | `/BillingHistory.aspx` | Next payment, then charges: Date, Amount, Subscription, Status | Admin only | “Billing History” when the payment method text contains “Stripe” |
| PG-LOC-DEFAULT | Default location picker | `/_locationSelectorToggle.aspx?type=defaultcheckin` or `defaultcheckout` | Pick or clear the user's default check-in or check-out location | Settings Default Locations |
| PG-SUCCESS-PRODUCTS | Products created | `/SuccessProducts.aspx` | Success screen after product creation | Create flow |
| PG-AI-REPORT | AI insights | `/ai-report.aspx?id=` | Renders one stored insights report (“Your Inventory Insights”, badge “AI-GENERATED”). Any exception, including a bad id, goes to Map. | Signed-in. No menu link anywhere in this repo. | Direct URL only |
| PG-OAUTH-AUTH | OAuth authorize | `/OAuth2/auth.aspx` | OAuth authorization entry | External API client |
| PG-OAUTH-CONSENT | OAuth consent | `/OAuth2/consent.aspx` | Allow or cancel an OAuth consent | External API client |
| PG-LS-CALLBACK | Lansweeper callback | `/_lansweeper-callback.aspx` and `/lansweeper-callback.aspx` | OAuth return for Lansweeper | Lansweeper redirect |
| PG-TERMS | Terms | `/Terms.aspx` | Terms text. Public page, not an inventory feature. | Footer / signup |

Lansweeper settings popups (admin integration UI; the main Settings block currently shows a request-access message and `InitLansweeper()` is commented out):

| ID | Page | Purpose |
| --- | --- | --- |
| PG-LS-FAIL | `pages/settings/popups/lansweeperConnectionFailure.aspx` | Connection failed |
| PG-LS-OK | `pages/settings/popups/lansweeperConnectionSuccess.aspx` | Connection succeeded; timer tick |
| PG-LS-SITES | `pages/settings/popups/lansweeperSiteSelector.aspx` | Choose Lansweeper sites and connect |
| PG-LS-FIELDS | `pages/settings/popups/lansweeperFieldToggle.aspx` | Choose which fields sync |
| PG-LS-CATS | `pages/settings/popups/lansweeperCategoryLocationToggle.aspx` | Map Lansweeper categories to locations |
| PG-LS-LINK | `pages/settings/popups/lansweeperLinkAndSync.aspx` | Link and sync |
| PG-LS-WEBHOOK | `pages/webhooks/lansweeper.aspx` | Inbound webhook. Not a page users browse. |

## Mobile pages

Master: `MOBILE_MasterPage.master`.

| ID | Page | Purpose |
| --- | --- | --- |
| PG-M-HOME | `mobile_main.aspx` | Mobile home. Logout and a hidden "view products" postback. |
| PG-M-PROCESS | `MOBILE_Process.aspx` | Check-in, check-out, or transfer started from the hamburger menu or a narrow map. Cookies `MOBILE_Process`, `MOBILE_SourceID`, `MOBILE_DestinationID`, `MOBILE_ReturnAfterProcess`. Finish, set default location, transfer-done modal. |
| PG-M-TRANSFER | `MOBILE_Transfer.aspx` | Transfer UI used when a map drop happens on a narrow viewport |
| PG-M-QSCAN | `MOBILE_QuickScan.aspx` | Full-page QuickScan |
| PG-M-QADD | `MOBILE_QuickAdd.aspx` | Create a product from a scan that did not match |
| PG-M-PRODUCTS | `MOBILE_Products.aspx` | Mobile product list |
| PG-M-EDITOR | `MOBILE_ProductEditor.aspx` | Mobile product editor |
| PG-M-LOC | `MOBILE_LocationSelector.aspx` | Pick a location during a mobile process |
| PG-M-PSEL | `MOBILE_ProductSelector.aspx` | Pick products during a mobile process |
| PG-M-MAP | `Mobile/Map.aspx` | Redirects to `/_admin/_unauthorized` before the 2018 map can render. The live phone map is `Map.aspx`. |
| PG-M-MAP-EDITOR | `Mobile/ProductEditorMap.aspx` | Same unauthorized redirect. Not a live editor. |

`Controls/MOBILE_ProcessProgress.ascx` shows process progress on the mobile flow.

## Shared controls

| ID | Control | Role |
| --- | --- | --- |
| PG-C-MAP | `Controls/Map_CONTROL_2017.ascx` | Desktop and responsive map: locations, hover tools, drag, filter, zoom, settings, export, clone, 3D and vertical display |
| PG-C-MAP-M | `Controls/Map_CONTROL_MOBILE_2018.ascx` | Older mobile map control. Still has delete, save coordinates, update quantity, transfer, create, and view postbacks. |
| PG-C-DASH | `Controls/mapDashboard.ascx` | Map dashboard widget |
| PG-C-LOCSEL | `Controls/LocationSelector_CONTROL.ascx` | Location tree / breadcrumb used by Products, Activity, Transfer, Export, Product Selector |
| PG-C-SEARCH | `Controls/CS_SearchBox.ascx` | Header search |
| PG-C-FIELD | `Controls/EDITABLE_FIELD.ascx` | Inline editable field |
| PG-C-CF | `Controls/CustomFieldEditorModal.ascx` | Create or edit a custom field |
| PG-C-AVATAR | `Controls/ProfileIconPicker.ascx` | Profile photo or preset icon |
| PG-C-PROG | `Controls/MOBILE_ProcessProgress.ascx` | Mobile process steps |

## Map surface (confirmed controls)

Hosted by `Map.aspx` through `Map_CONTROL_2017.ascx`. These are controls, not yet the full behavior write-up:

- Search box "Search Map..." with clear, and a mobile submit button.
- Zoom in, zoom out.
- Map lock (starts in the locked presentation; button label says "unlock map to move locations freely").
- Map settings popup: ABC Sort, Popup details, Tablet mode (row hidden until the layout allows it), Shared Maps.
- Download Quantity Report button (hidden until enabled).
- Scroll to map origin (hidden until needed).
- Minimap toggle ("Minimap (picture-in-picture)").
- Floating "+" (`floating_add_tab`) opens the location-type toolbox.
- Location types in the toolbox: BUILDING, WAREHOUSE, STORE, FLOOR, ROOM, CLOSET, SHELF, BIN, VEHICLE (`data-location-type` 0 through 8).
- Location events handled in `MapProcessEvent_JS`: CLONE, CHECKIN, CHECKOUT, VIEW, READ_ONLY, VERTICAL_CHILDREN_TOGGLE, THREE_D_CHILDREN_TOGGLE, EDIT, DELETE, and drag/drop (DRAG_START through DROP).
- Drop onto the same location, or onto location id `-2` ("All Locations"), is ignored.
- Ctrl-drag copies contents after a confirm: "Are you sure you want to copy the contents to this location? Any existing items will be cleared first."
- A one-unit drag opens an in-map comment modal ("Moving this item.") instead of the full Transfer page. Larger moves open `Transfer.aspx` or `MOBILE_Transfer.aspx`.
- Clone modal: new name (max 255), optional Auto-Rename Sub-Locations with find/replace.
- Popup details modal: choose which product fields appear in the location popup. Field list is filled in script.
- Getting-started and check-in lesson modals exist on the map (`mapGettingStarted`, `mapCheckinLessonModal`).
- Narrow layout selects a location into a footer: Edit, Clone, Vertical, 3D, Delete, Close. Vertical and 3D are omitted when the location is not eligible.
- Check-out target `#floating_checkout` appears while a full location is dragged, except during onboarding.

## Products surface (confirmed controls)

Editable `Products.aspx` toolbar:

- Add products
- Delete selected (enabled only when a selection exists; client confirm `DeleteConfirmation()`)
- Multi-edit selected, then Update
- Column picker, Save Columns
- Download product report
- Print barcodes for the selection (shown when a selection exists)
- Show or hide product images
- Printable version (`/Products?printable=true`)
- Grid sorting and paging (first / last / numeric)
- Location selector
- Hidden postbacks for custom search, clear filter, check fields, custom properties, and load stockroom

Read-only products page keeps column adjust, search, sort, paging, location filter, export, and print barcodes. It does not wire delete or multi-edit.

## Settings surface (confirmed controls)

Profile: name, email, profile icon, password (old, new, repeat), optional Google account link, role badge.

Team (not read-only): user cards loaded by `loadUsers`, search and role pills when there are more than 12 users (Admin, User, Read-Only), invite by email plus role.

Custom fields: Personalized Sort toggle, field list, editor modal.

Default locations (not read-only): default check-in location, default check-out location.

API: dynamic key area, otherwise a request-access message and a link to Postman API documentation.

Lansweeper (admin section visible): request-access message. Synchronize and Disconnect markup is commented out.

Display settings:

- Share Map Layout (admin row only)
- Product Images
- Zero Quantity Products
- Expirations, and when on: Expiring Soon with a number (default markup value 60) and unit days / weeks / months / years
- Kitting toggle markup exists but the row is `display:none`
- Quantity Threshold, default markup value 1. Zero-quantity locations stay white on the map.
- Max Highlight, default markup value 10. Must be greater than the quantity threshold. Cannot turn on unless the quantity threshold is on.

Account settings (admin): time zone list from GMT-12 through GMT+13 (two entries share value `5`), currency symbol (markup default `$`).

Subscription (admin): card filled by `js/business/subscription.js`. Self-serve Update Plan, Change Card, Cancel, and Billing History render only when the payment-method text contains “Stripe”. Other methods show a note to email admin@cyberstockroom.com. Trial, upgrade, and payment banners exist in the page and stay `display: none`. Nothing in the current Settings load calls `ToggleExpiry`, `ToggleUpgrade`, or `TogglePayment`. Do not describe a plan-capacity limit; no writer for the “exceeded the capacity” banner was found.

Trial length, used by the billing gate, is 14 days from `Accounts.DateCreated` while `ConfirmedPayment` is 0.

## Pages reviewed and excluded

| Area | Why excluded |
| --- | --- |
| `Home.aspx`, `Features/*`, `Inventory/*` industry pages, `SEO/*`, `blog/*`, `Case-Study/*`, `PressKit.aspx` | Marketing site |
| `_admin/_crm.aspx`, `_admin/_demo.aspx`, `_admin/_demoCatalog.aspx`, `_admin/_lansweeper.aspx`, `_admin/_unauthorized.aspx` | Internal staff tools. Adopted-session query handling in the master page is an admin impersonation hook, not a customer feature. |
| `_cvr/*` | Conversion / signup tracking pages |
| `map_demo.aspx`, `mapDashboardTest.aspx` | Demo or test hosts |
| `ViewSwitcher.ascx` | ASP.NET browser view switcher, not a product feature |
| `GeneralError.htm` | Generic error page |
| `webAPI/*.aspx` except as the backing endpoints for Settings | HTTP endpoints. Customer-facing API key management is on Settings. |

`pages/webhooks/lansweeper.aspx` is an inbound endpoint, listed above so it is not mistaken for a screen.

## Uncertain pages (do not treat as confirmed features)

| Item | Why it is unresolved |
| --- | --- |
| `ai-report.aspx` | File and Init handler exist. No header link found yet. |
| `MapDesignerNaked.aspx`, `MapProductEditorNaked.aspx` | Map hosts without the normal chrome. Used as embedded designers; user entry points still being traced. |
| `SUPER_USER` | Enum and database read exist. No Settings case and no other UI branch. |
| How `SHOW_KITTING` is turned on | The Settings checkbox row is hidden. The Products menu still reads the flag. |
| Whether `/Products` redirects read-only users to `Products_read_only.aspx` | Both pages exist. The redirect itself is part of the products trace. |
| `SuccessSignup.aspx` / `SecureRegistration.aspx` | Signup completion. Public registration, not day-to-day inventory. Included only if the signup trace shows user-facing steps beyond marketing. |
