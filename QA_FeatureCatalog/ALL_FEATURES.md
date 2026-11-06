# CyberStockroom — complete feature listing

One listing of every user-facing feature traced in the website repository. Identifiers are stable. Knowledge-base status for every entry is **Not audited**. Target: https://cyberstockroom.helpscoutdocs.com/

This is a code-grounded listing, not a claim of absolute completeness. External inventory APIs, `productDeleter`, and a few unwired screens are called out at the end. Marketing pages and `_admin` tooling are excluded.

Roles: **Admin**, **User**, **Read-only**. A legacy Mobile type is treated as User. Read-only users are sent to read-only map, products, and product editor pages, and away from Transfer, Settings writes, import, and create.

---

## SET — Settings shell

| ID | Feature | What it does |
| --- | --- | --- |
| SET-001 | Settings sections | `Settings.aspx` left menu scrolls to Profile & Team, Custom Fields, Default Locations, API & Integrations, Options, or Subscription. Hidden items are skipped. Time zone and currency sit further down the same page and have no menu item. |
| SET-002 | Text fields save on change | Name, email, custom-field names, currency, and the create-field box remember the value on focus. Enter saves. Escape restores the previous value and does not save. |
| SET-003 | One settings write at a time | Invite, custom-field changes, and API-key create/delete disable those controls while a request runs. Overlap shows “Another action is currently in progress. Please wait for it to complete.” |

## ACC — Sign-in and profile

| ID | Feature | What it does |
| --- | --- | --- |
| ACC-001 | Log in with email | Email and password on the login page. Success opens the app. |
| ACC-002 | Log in with Google | Google sign-in. The invitation path is confirmed. The exact failure text for an ordinary Google login that is not an invitation was not fully traced. |
| ACC-003 | Forgot password | Reset email. The reset form has no minimum length. The host in the mail is hard-coded to www.cyberstockroom.com. |
| ACC-004 | Accept an invitation | Invited person sets a password and joins the account. |
| ACC-005 | Choose a plan during signup | Signup plan choice is an iframe, not a Settings control. |
| ACC-006 | Welcome page | `Welcome.aspx` redirects to `/Map` before any wizard runs. It is not a customer step. |
| ACC-007 | Required name | A name is required before the rest of the app is usable. |
| ACC-008 | Profile picture | Preset avatars 1–15, or an upload under 3 MB (png, jpeg, gif, webp). |
| ACC-009 | Your name | Max 50 characters. Must be unique on the account. |
| ACC-010 | Your email | Change email. A same-as-old check compares against first name rather than the current email. |
| ACC-011 | Update your password | Minimum 6 characters. Hidden when the user signed in with Google (`GoogleID` set). |
| ACC-012 | Link Google | Attach Google to an existing email user. |
| ACC-013 | Role badge | Shows Admin, User, or Read-only on the profile card. |
| ACC-014 | Subscription update confirmation | `SuccessSignup` after a plan change. |
| ACC-015 | Allow or deny an OAuth connection | Allow and Cancel on the consent screen. Scope labels live outside this repo. |

## TEAM — Team members

| ID | Feature | What it does |
| --- | --- | --- |
| TEAM-001 | Team list | Page size 12. Search and role pills appear when the account has more than 12 people. |
| TEAM-002 | Change a teammate’s role | Roles are ADMIN, USER, and READ-ONLY. There is no last-admin guard. |
| TEAM-003 | Remove a teammate | Deletes that user from the account. |
| TEAM-004 | Invite a teammate | Form can be visible to a User; the API is admin-only. An email that already belongs to this account does not change that person’s role. The invite copies the inviter’s expiration flag and map coordinates, with the share-map marker stripped. |

## CFL — Custom fields

Custom fields are named text fields, optionally with presets. There is no date, number, or dropdown field type. Names and presets are account-wide. Order, visibility, and personalized sort are per user. Create, rename, delete, and presets are Admin only.

| ID | Feature | What it does |
| --- | --- | --- |
| CFL-001 | Personalized sort | Off by default. When on, this user can order fields independently. |
| CFL-002 | Show or hide Buy Price and Sell Price | Shown in Settings only while personalized sort is on. Default is visible. |
| CFL-003 | Add a custom field | Admin. No duplicate-name check was found. |
| CFL-004 | Rename a custom field | Admin. Renames the account-wide label. |
| CFL-005 | Delete a custom field | Admin. Warning says the stored data is erased. Whether every related row is removed was not fully read. |
| CFL-006 | Preset choices | Admin. Optional “Other (Specify)”. Commas in stored presets become underscores. The preset popup does not refresh Settings when it closes, and presets are not offered in the product modal’s field list the same way. |

## DEF — Default locations

| ID | Feature | What it does |
| --- | --- | --- |
| DEF-001 | Default check-in location | Per user (`CheckInLocationDefault`). Clear stores `-2`, shown as none. Saving sets `cookie_refresh_settings` so Settings reloads the label. Read-only users hitting the picker go to `/_admin/_unauthorized`. |
| DEF-002 | Default check-out location | Same pattern for `CheckOutLocationDefault`. |

## API — API keys

| ID | Feature | What it does |
| --- | --- | --- |
| API-001 | Create and delete an API key | Only if the account is on `CS_API_v0._betaList`. The plaintext key is shown once. |
| API-002 | API documentation link | Opens the Postman collection at `https://documenter.getpostman.com/view/1256102/2sB34ZqPYv`. |

## LSW — Lansweeper

| ID | Feature | What it does |
| --- | --- | --- |
| LSW-001 | Request the integration | The live Settings sentence asks the customer to email support. Connect, sync, and disconnect on Settings are commented out. The sentence contains the typo “conenct”. |
| LSW-002 | Choose sites | Popup exists. It is not linked from current Settings. |
| LSW-003 | Match a Lansweeper field | Popup exists. Not linked. How the pairing is stored was not fully traced. |
| LSW-004 | Match a category to a location | Popup exists. Not linked. Two code-behind files declare the same class; the live href uses `_locationSelectorToggle`. |
| LSW-005 | Link, sync, and progress | Popups exist. Not linked from current Settings. Two success pages inherit the same class name. |

## DSP — Display settings

These live in the signed-in user’s `GridsterCoordinates2017` string unless noted. Layout is per user. The map is locked by default.

| ID | Feature | What it does |
| --- | --- | --- |
| DSP-001 | Share Map Layout | Admin only. Token marks the map shareable so others can copy this user’s layout (MAP-016). Inventory is not shared. |
| DSP-002 | Product Images | Shows product photos in the product list. The stored property name is spelled `SHOW_PRORDUCT_IMAGES`. |
| DSP-003 | Zero Quantity Products | When off, the product grid drops zero-quantity rows. |
| DSP-004 | Expirations | Per-user `SHOW_EXPIRATIONS`. Turns the expiration list and product-editor date on. |
| DSP-005 | Expiring Soon | Default window 60 days. Month is stored as 30, year as 365. Stored `0` means off. Stored `-1` means 60 and on. |
| DSP-006 | Quantity Threshold | Off is 0. Turning it on starts at 1. Locations with quantity 0 stay white. |
| DSP-007 | Max Highlight | Must be greater than the threshold. Off displays as 10. Used with DSP-006 for map quantity colors (MAP-019). |
| DSP-008 | Kitting toggle | The Settings checkbox is `display:none` and unwired. Do not document it as a switch. The `SHOW_KITTING` flag still exists; nothing else in this repo sets it. |

## ACCSET — Account settings

| ID | Feature | What it does |
| --- | --- | --- |
| ACCSET-001 | Time zone | Account-wide, offsets −12 through 13. Two labels share value 5. Fallback is −5. Half-hour zones were not confirmed. |
| ACCSET-002 | Currency symbol | Account-wide free text. Default `$`. Used in product headers. Not used by the subscription card. |

## SUB — Subscription and billing

Self-serve plan changes appear only when the stored payment method contains “Stripe”. Do not publish dollar amounts; they are images. The Enterprise image has no click. `UpdateAccount` blocks Read-only only, not non-admin. Billing history is admin-only.

Unpaid trial is 14 days from `Accounts.DateCreated` while `ConfirmedPayment` is 0. A delinquent Stripe account (`ConfirmedPayment` = 1) is sent to `/Settings` from every other page unless upgrade or payment alerts are suppressed. The trial, upgrade, and payment banners exist in markup and stay `display:none`. Their toggle functions are never called. Do not document a plan-capacity limit.

| ID | Feature | What it does |
| --- | --- | --- |
| SUB-001 | Subscription summary | Shows the current plan on Settings. |
| SUB-002 | Change a Stripe subscription | Update Plan, Change Card, and Cancel. Live price ids: monthly `price_1O6zRX4D3SV7Y45Utyewx37h`, annual `price_1O6zS34D3SV7Y45UCZ8p3YaG`. |
| SUB-003 | Billing history | Admin. Charges table. An invoice table is built and not added to the page. |
| SUB-004 | Trial end and failed payment | Gate described above. Settings remains reachable. |

## MAP — Map and locations

Live map is `Controls/Map_CONTROL_2017.ascx` on `Map.aspx`. There is no right-click menu and no free resize. `Mobile/Map.aspx` and `Mobile/ProductEditorMap.aspx` redirect to unauthorized. Phone uses the same 2017 control. Location id `-2` is All Locations. Types 0–8: Building, Warehouse, Store, Floor, Room, Closet, Shelf, Bin, Vehicle.

| ID | Feature | What it does |
| --- | --- | --- |
| MAP-001 | Open the inventory map | MAP menu. Places this user’s saved coordinates. Nested locations draw inside their parent. Map type 1. Read-only users are sent to `Map_read_only.aspx`. |
| MAP-002 | Read-only map | Same canvas. Hover: View, optional V/3D, View Location Details. Floating + is hidden. Whether the still-rendered move handle can drag is not separately blocked. |
| MAP-003 | Location types | Toolbox types 0–8. New locations default to type 0 and parent `-2`. No control was found to change type after create. |
| MAP-004 | Quantity labels on tiles | Own quantity uses the full style. Zero own quantity with stock only in children is ghosted, except a 3D parent, which is drawn full. Drag requires the tile’s own quantity > 0. |
| MAP-005 | Create a location | Floating +, a tile +, or Add inside a 3D stack opens New Location. Duplicate name: “That location name is already in use!” Activity is location create. Empty-map coaching swallows the floating + click. |
| MAP-006 | Rename a location | Location Editor name field. All Locations (`-2`) is not editable. Duplicate name is rejected. |
| MAP-007 | Location editor | Name, breadcrumb, children, add-new toolbox, attachments, barcode, print, view products, kiosk links. Read-only goes to unauthorized. Unknown id shows Location Error. A load type other than EXISTING creates immediately; the map always sends EXISTING. |
| MAP-008 | Move primary locations | Drag the diamond header. Nested locations move with the parent. No resize. Overlap is rejected while the map is locked. Inventory does not move. |
| MAP-009 | Map lock | Default on (no token = locked). Unlock allows free moves. Lock cancels an in-progress reparent. Hidden on the naked designer used inside some hosts. |
| MAP-010 | Move under a different parent | Clasp, then click a parent or empty canvas (parent `-2` makes it primary). Confirm “Move location?” Nested locations stay with it. Inventory stays on the same location ids. Failure: “Could not move location”. |
| MAP-011 | Tile size follows children | Width and height grow from children. Not a user resize. Compact sizes exist in code and are forced off (“Compact Features Not yet released”). |
| MAP-012 | Delete a location | Confirm “Are your sure you want to DELETE this location?” plus “All sub-locations will be deleted. Existing products will be checked out automatically.” YES checks quantities out, then deletes the location and descendants. The “Include Any Sub-Locations” checkbox is hidden and unread. Closing the popup cancels. There is no No button. |
| MAP-013 | Clone a location’s structure | Name max 255. Suggested “ (Copy)” up to 999. Auto-rename sub-locations is off by default (whole word or hyphen part). Posts `api/LocationClone`. Whether quantities copy is outside this repo. Sibling or same-name is blocked. |
| MAP-014 | Copy stock with Ctrl+drop | Ctrl-drag a full location onto another. Confirm says existing items will be cleared first. Posts `api/inventory?action=clone`. Blocked during multi-select and when the drag is a product chip. |
| MAP-015 | ABC sort | Off by default. Children sort by name, then id. Fewer than two children is skipped. Display order only. |
| MAP-016 | Use a shared map layout | Gear → Shared Maps. Sync warns that the current layout will be lost. Copies coordinates, zooms, and vertical/3D ids. Not inventory. Empty: “No shared maps. Admins can share their maps in the Settings page.” Who can share is DSP-001. |
| MAP-017 | Zoom | Desktop min 0.1 max 1, default 1. Touch min 0.15 max 2.2, default 0.74. Keys +/− multiply by 1.1 or 0.9. Pinch. Narrow layout (~900px) uses the mobile zoom. |
| MAP-018 | Search the map | “Search Map...”. Enter cycles matches. Escape clears. `GET api/map?mapFilter=`. API failure falls back to local title match. Which fields the API matches is outside this repo. The same text is passed into Transfer as `MAP_FILTER`. |
| MAP-019 | Low and high quantity colors | At or above max highlight, at or below threshold, or in between. Quantity 0 is not colored as a tier. Numbers come from DSP-006 and DSP-007. |
| MAP-020 | Check in from the map | Opens Transfer with source `-2` and this location as destination. Empty location and destination `-2` are refused. Narrow layout uses mobile transfer. Phone can prime the mobile process instead. |
| MAP-021 | Check out from the map | Destination forced to `-2`. A full location can be dragged to “Drag inventory here to check out”. That strip is hidden during onboarding. |
| MAP-022 | Drag stock between locations | Drop a full location or a peek row on another location. Same location or `-2` is ignored. Desktop opens Transfer in a large popup. Narrow layout opens the full mobile transfer page. |
| MAP-023 | Move one unit and comment | Only when quantity is exactly 1 and onboarding is off. “Moving this item.” Commit sets that SKU’s source cookie quantity to 0, so source stock of that product becomes 0. That is not the Transfer page’s “move 1, keep the rest” rule. |
| MAP-024 | See products inside a location | Click a location. Up to 25 products. Rows are draggable. Escape closes the peek. On the designer map a row can start a quantity edit. |
| MAP-025 | Popup details | Gear → Popup details. The field list is built per account. Do not invent field names. Description stays on in the save path that was read. Expiration appears only when the account has expiration data. Buy/sell visibility is edited in Settings, not here. |
| MAP-026 | Change quantity on the product map | Product editor map, type 2. Click a location, type a whole number, Enter. Posts `action=adjust` with source and destination equal to that location. The on-screen number updates when the request is sent. Failure: “There was a problem updating the quantity in this location...” Timeout 3 seconds. Arrows step only on a fine pointer. |
| MAP-027 | Open the product list for a location | Hover View, or Location Editor “View Products”, stores the location and opens Products or the read-only product list. |
| MAP-028 | Vertical stack | Needs at least two children. A child that has its own children must already be 3D. Layout only. |
| MAP-029 | 3D stack | Hides children in an overlay. Click the parent to open. Add creates a child. Not allowed when a child is already 3D or a child has children. Search and drag can open the stack. |
| MAP-030 | Move several locations | Desktop only. Ctrl/Cmd-click or Ctrl-drag a rectangle. Escape cancels. Inventory unchanged. Suppresses Ctrl inventory copy while a selection is active. |
| MAP-031 | Minimap | 240×160. Click scrolls the big map. A drop on the minimap commits at the center of the view. Can auto-open on a large map. |
| MAP-032 | Download a quantity report | Hidden until some visible location has quantity > 0. Group by Location (default) or Group by Product. By-location file includes empty locations. Empty search disables the button. |
| MAP-033 | Tablet mode | Touch UI and a selection footer: Edit, Clone, Vertical, 3D, Delete, Close. First tap selects. Multi-select turns off. |
| MAP-034 | Map keyboard shortcuts | +/− zoom. Enter/Escape in the filter. Escape closes clone, sync, export, reparent, the one-unit modal, and the peek. Ctrl+drop copies inventory. Enter saves a product-map quantity. |
| MAP-035 | Pan and scroll to origin | Drag empty canvas. The origin button appears after the user scrolls away. |
| MAP-036 | Empty-map coaching | Getting-started card, a two-minute check-in lesson, and prompts to add the first location or sub-locations. Which card wins for every mix of zero products and zero locations was not fully separated. |
| MAP-037 | Highlight a new location | After create or clone, the next load scrolls to the new id. |
| MAP-038 | View barcode and attachments (read-only) | Peek popup. Downloads attachments. Barcode is disabled. Print opens the barcode page. The upload icon does not upload. |
| MAP-039 | Attach a file to a location | Location Editor paperclip. Delete asks “Are you sure you want to delete this attachment?” |
| MAP-040 | Location barcode | Label “Barcode # (scan to change)”. A duplicate turns the box red (`#AF5756`) and does not save. Print tooltip “Print Barcodes”. |
| MAP-041 | Location kiosk | Checkin Kiosk and Checkout Kiosk open Quick Scan in a new tab with `mode=checkin\|checkout` and `locationID`. Narrow width uses the mobile Quick Scan page. |
| MAP-042 | Location breadcrumb | Root label “ALL LOCATIONS”. On a transfer popup, a click left of x=350 is FROM; otherwise TO. |
| MAP-043 | Create a top-level location from mobile | JSON create. Type must be 0–8. Parent must be `-2`. Read-only is rejected. |
| MAP-044 | Map on a phone | Same 2017 control. About 900px: mobile zoom, bottom bar, transfer goes to the mobile transfer page, multi-select off. `user-scalable=no`. `Mobile/Map.aspx` itself is not reachable. |

## XFR — Check-in, check-out, transfer, Quick Scan

There is no adjust mode on Transfer, Start, or the mobile process. If both check-in and check-out flags are set, check-out wins. Batch, lot, expiration, and kitting are not fields on these screens. Read-only users cannot open Transfer.

Two stock engines exist. Transfer (and the live mobile commit) **overwrites** the source to the remaining cookie quantity and **adds** that amount at the destination. Start and the legacy mobile handlers **add** on check-in and **subtract, floored at 0,** on check-out.

| ID | Feature | What it does |
| --- | --- | --- |
| XFR-001 | Check in | Source forced to `-2`. Left list is the catalog (search limit 250) with an infinity glyph. Click moves 1. There is no check-in-everything. Save label “Check In”. Comment can be skipped. Activity is check-in. New Products and import show only while the destination selection is empty, unless import is hidden. A missing desktop scan says the product number doesn’t exist. A mobile check-in miss opens Add Products. |
| XFR-002 | Check out | Destination forced to `-2`. Left list is on-hand stock (page 250). Click moves 1 up to on-hand. Drag moves all remaining. “Check-Out Everything” pages 500 and hides while a map-filter badge is on. Save overwrites source to the remaining quantity. Activity stores the moved quantity. The add-quantity modal still says Transfer. |
| XFR-003 | Transfer between two locations | Both locations are real and must differ. Destination quantity becomes existing destination quantity plus the amount moved. Save label “Transfer”. Same product quantities add. If loading the destination product throws, destination quantity is treated as 0 and then set to the moved amount only. |
| XFR-004 | Quantity adjust is not a Transfer mode | No adjust button on Transfer. Activity type 25 is written by the map and product-list quantity editors (MAP-026, PRD-010). |
| XFR-005 | Import a file into a movement | Match by product number, description, or a custom field. Ambiguous matches are skipped. Check-in keeps the requested quantity. Check-out and transfer cut the quantity to on-hand. Review locks the page until save or cancel. Unedited imports tag the comment `{{cs-file-import}}`. Cancel does not move stock. |
| XFR-006 | Start page | Check In, Check Out, Transfer, Create, Quick Scan. Query flags open that action. Zero products: “You have not added any products yet”. Check-in adds. Check-out subtracts and floors at 0. The comment box appears **after** inventory is already written. A missing location cookie exits without saving. |
| XFR-007 | Check in products just created | Products already exist. Standalone: one location (default is the check-in default), quantities are whole numbers ≥ 0, at least one line ≥ 1, then an additive check-in. Skip does not place them. Imported per-line locations hide the map. Return-to-transfer does not change stock until the later Transfer save. |
| XFR-008 | Mobile check-in, check-out, and transfer | Live path uses the same Transfer backend when the old product-list cookie is empty. Opening mobile home clears an in-progress process. “Set default” alerts that locations will be saved next time, and does nothing on a transfer if both location cookies are already set. A return token of `Map` without `.aspx` lands on mobile home, not the map. |
| XFR-009 | Mobile location picker | Source, destination, or contents. Pre-selects the user’s check-in or check-out default. The “default” badge opens the Settings location picker. |
| XFR-010 | Legacy mobile product list and Quick Add | Not the live auto path. An unknown scan can open Quick Add, which creates a catalog product at location `-2` and does not check it in. Empty description is allowed. |
| XFR-011 | Quick Scan | Mode is derived: source only = check out, destination only = check in, both = transfer. Save posts `api/inventory`. Kiosk accepts check-in or check-out plus a location id; transfer is not a kiosk mode. No create-on-scan. Stock math is outside this repo. |
| XFR-012 | Mobile home | Menu: Home, Map, Products, Activity, Check In, Check Out, Transfer (if products exist), Quick Scan, Help, Settings, Logout. Footer after a location is primed: check in, view, check out. No footer Transfer. Empty recent locations: “No recent locations.” |

## PRD — Product list

Page size 50. Location `-2` is ALL LOCATIONS. Read-only users do not stay on `Products.aspx`.

| ID | Feature | What it does |
| --- | --- | --- |
| PRD-001 | Product list | A specific location lists products with quantity > 0 there. If that location is empty and children have stock: “This location is empty but its sub-locations are not”. All Locations appends zero-quantity products unless DSP-003 is off. Default sort is product number ascending. |
| PRD-002 | Empty list | All Locations: “No products yet” / “Click to create”. A location: “Click to Check in”. Search with no hits: “No matches found!” |
| PRD-003 | Columns | Product Number cannot be unchecked. Also Quantity, Description, Buy, Sell, each custom field, and Cost Value (quantity × buy, calculated). SAVE COLUMNS is per user. Header drag reorders. EDIT COLUMNS is Admin. Empty description shows `UNTITLED (Product Number : n)`. |
| PRD-004 | Sort | First click ascending, same header flips direction and returns to page 0. All Locations does not mix zero-quantity rows into the sorted in-stock sequence. |
| PRD-005 | Pages and select all | Pager hidden at 50 or fewer rows and during search. Header checkbox selects this page, then “Select all {count} products.” Select-all is every product in the account, ignoring location and search. The SQL limit grows with the page index, so later pages can return more than 50 rows. |
| PRD-006 | Search the product list | Header Enter stores comma-separated terms. They are AND. Each term matches product number, name, and every custom field, including hidden columns. Not buy, sell, or quantity. Search forces All Locations for that request. |
| PRD-007 | Open a product | A data cell opens the product editor. The checkbox column does not. `AutoHighlight=TRUE` is passed and the editor does not read it. |
| PRD-008 | Web addresses in the grid | A cell whose entire text is a URL becomes a pill and opens in a new tab. It does not open the editor. Read-only inclusion was not re-verified. |
| PRD-009 | Photos in the list | 40px images when DSP-002 is on. The toolbar camera button is commented out. Missing images use a camera placeholder. |
| PRD-010 | Change quantity in the list | Only on the editable page, at a real location, on an in-stock cell, and not during search. Enter posts adjust with source and destination equal to that location. Down stops at 0. Not the multi-edit path. |
| PRD-011 | Toolbar actions | **Add** opens Add Products. **Delete** confirms it cannot be undone; select-all deletes the whole catalog via `Product.DeleteProducts` (the `productDeleter` class is outside this repo). **Multi-edit** can set name, quantity (only at a real location; it overwrites, it does not add), buy, sell, and custom fields. **Recently created** lists up to 50 create-product activities. **Export** opens RPT-001 and does not pass the search. **Print barcodes** is hidden until a selection. **Printable** opens a print-styled list and does not call `window.print`. |

## PED — Product editor, create, import, labels

| ID | Feature | What it does |
| --- | --- | --- |
| PED-001 | Edit name, price, and custom fields | Product number cannot be renamed. Buy and sell show for inventory accounts when CFL-002 says show. Presets: (none), each preset, the current value if it is outside the list, and “Other (Specify)”. Currency rejects non-numeric and negative values. Activity records “Changed '{label}' to '{value}'”. |
| PED-002 | Product photo | Click to update. No size or type check in the upload handler. A Lansweeper image disables upload. Read-only can view and cannot upload. |
| PED-003 | Product attachments | Paperclip upload, download, delete with confirm. No extension or size limit. Not Document Editor. Read-only can download only. |
| PED-004 | Lansweeper link on a product | Shown when an asset URL exists. Failures hide the link. |
| PED-005 | Expiration on the product | Only when expirations are on. Date from 2018-01-01 through 2050-01-01. Green if more than 60 days remain, gold if 60 or fewer and still future, red if due or past. API errors are logged to the console only. |
| PED-006 | Product editor map | Instruction: “Click a location. Type new quantity. Press Enter.” Quantity behavior is MAP-026. Clone does not copy quantities. Read-only hosts map type 5. |
| PED-007 | Clone a product | Auto product number on by default (`CSN-` plus nine digits). Copies fields, image when it can, and expiration if set. Does not copy stock, locations, or attachments. The old `Popups/CloneProduct.aspx` has no save and is not the live clone. |
| PED-008 | Delete one product | Modal: “Deleting this product will also check it out of all locations on the map.” Same delete path as the grid. Checkout of quantity rows is what the modal says; the deleter class is outside the repo. |
| PED-009 | Read-only product editor | Fields disabled. Print, downloads, Lansweeper, and the view map remain. No clone, delete, or upload. |
| PED-010 | Create products by typing | AUTO number by default. Empty description becomes the product number. Prices must be ≥ 0. Blank manual number placeholder is misspelled “No Poduct Number!” Existing numbers are skipped, not updated. Staged quantity is 1. Save then opens check-in unless this is the single mobile-transfer add. A quantity row at location `-2` is inserted without a quantity column; the database default is uncertain. |
| PED-011 | Photo while creating | Temp image is copied onto the new products on save. A fresh visit clears temps. No type or size check. |
| PED-012 | Import a CSV (shared rules) | Under 250 KB, at most 100 columns, UTF-8, commas (not semicolons), first row is the header. Must map at least a product number. Read-only cannot import. |
| PED-013 | Import to create products | Sample headers (Product Number, Product Name, Buy Price, Sell Price, Manufacturer, Supplier) are examples, not required names. Unmapped quantity stays 1, prices 0, location `-2`. Duplicate numbers in the file are rejected. Existing products are not updated; their quantity is staged for check-in. Presets are not enforced. Expirations apply only to new numbers. |
| PED-014 | Import a list into a movement | Check-in/out sample is Product Number, Quantity. With locations, add Location. Transfer sample is Product Number, Quantity, FROM, TO. This mode does not insert products. It feeds XFR-005 or the Start page. |
| PED-015 | Print barcode labels | Stocks: 30252 (default, 1-1/8" × 3-1/2"), 30336, 30334, 30330. Code 128. Page mentions a DYMO LabelWriter 450. Unknown stock falls back to 30252. No database write. |
| PED-016 | Product selector | Check-in, check-out, and transfer titles, default locations, “+ New Products”, and import. Same source and destination: “The Source can't be the Destination!” |
| PED-017 | Document editor is not attachments | `DocumentEditor.aspx` can show Purchase Order, Sales Order, or Kit. Print, Save, Next, and Cancel are literal text with no handlers. No product page links here. Do not document it as editing a document. |
| PED-018 | Unwired product screens | Old clone popup, the quantity-only delete dialog, and `SuccessProducts.aspx` are not on the live click path. `Batch_Class` is not used by the product UI. Do not document batches. |

## ACT — Activity

No undo. Account and user activity codes are declared and are not shown in history. Records accounts (account type 1) use Assignments, Assign, Deallocate, and Records instead of the inventory product phrases.

| ID | Feature | What it does |
| --- | --- | --- |
| ACT-001 | Activity history | Every signed-in user, including read-only. Default: all activity, all users, all locations, last 90 days (a comment says 365; the constant is 90), 15 rows. Empty: “No Activity...”. “You” when the stored name matches. Show More reloads a longer list from the top and can stay visible when everything is already shown. Changing filters does not reset the start index. |
| ACT-002 | Filter by type | All, Inventory, Check In, Check Out, Transfer, Adjust, and product or location Create/Edit/Delete. Check In and Check Out are not pure type filters: they keep adjusts that moved the matching direction, and transfers only when one end is inside the location filter. With no location selected, transfers are removed from both. |
| ACT-003 | Date, user, location, and keyword | Presets: All Time, Today, Yesterday, Last 7 Days, Last 30 Days, This Month. Users match the stored first name, not the user id. Read-only people are omitted from the chips; their old rows can still appear. Location includes descendants. Keyword matches comment, product number, product name, and every custom field. `%` and `_` stay LIKE wildcards. |
| ACT-004 | Activity row hover and CSV | Hover lists up to 11 product lines. Deleted products show “[DELETED]”. CSV “Readable Format” is on by default. Several trailing columns (old quantity, new quantity, difference, cost difference) are headers only and are never filled. Commas in some fields become underscores. |
| ACT-005 | One activity | Missing id: “Activity not found”. Quantity shown is the larger of quantity in and quantity out. No comment edit and no undo. |
| ACT-006 | Header activity popup | Up to 5 recent inventory rows. Button “View Activity History”. Rows do not open the detail page. The other-user suffix is a numeric user index, not the name. |
| ACT-007 | What is stored | Standard phrases: created, deleted, edited, checked in, checked out, transferred, adjusted a quantity, created/deleted/renamed a location. A product line is stored only when the product number is non-empty and the quantity is > 0. |

## EXP — Expirations

Requires `SHOW_EXPIRATIONS`, otherwise the page sends the user to Settings. The window is DSP-005. Read-only users get a list without manage.

| ID | Feature | What it does |
| --- | --- | --- |
| EXP-001 | Expiration list | First 100 rows. Counts can include far more. Expired is red “expired (date)”. Inside the window is yellow “will expire in N days”. Otherwise grey “will expire on”. A product expiring later today can be counted differently from how it is listed, because chips use the clock and the list uses the date. |
| EXP-002 | Replace or clone an expiring product | Radios: Replace and Delete, Replace only, Clone and Delete, Clone and Check-out, Clone only. Default is Replace and Delete. A past date warns “This date has already passed!” and does not block save. Success opens Activity History. What each action does to stock is outside this repo. |

## KIT — Kitting

Requires `SHOW_KITTING`. The Settings switch that would turn it on is hidden (DSP-008). There is no build and no break. The read-only redirect target `Kitting_read_only` is missing from the repo.

| ID | Feature | What it does |
| --- | --- | --- |
| KIT-001 | Kit list, create, delete, search | “+ NEW KIT” prompts for a name and posts an empty kit. Cancel posts the name `null`. Delete has no confirm. Search runs on each keyup. First 100 API rows. |
| KIT-002 | Kit components | Add from a product search of 10. Quantity prompt and remove confirm exist. **Defects:** changing quantity of a product already in the kit sends the old quantity. Remove drops every other component that has the same quantity. Do not document this as a reliable editor. |
| KIT-003 | Kit “manage” is not a kit action | The button builds invalid JavaScript and throws. The modal is a copy of the expiration wizard. Do not publish it as kitting. |

## SRCH — Header search

| ID | Feature | What it does |
| --- | --- | --- |
| SRCH-001 | Header search | Suggestions from `developers.cyberstockroom.com/api/search`, limit 10. A product opens the product editor. A location opens the location editor. Enter stores the text and opens the product list (PRD-006). If the API returns nothing and Add Products is visible, one row offers “Create New Product {term}”. Hidden for read-only. Which fields the API matches is outside this repo. |

## RPT — Reports

| ID | Feature | What it does |
| --- | --- | --- |
| RPT-001 | Download a product report | From the product list. Defaults: skip zero quantity, skip sub-locations (that option hides on All Locations), include description, quantity, location breakdown, buy, cost, sell, and every custom field. Product image off. Cost is quantity × buy, rounded half away from zero. **Side effect:** every download rewrites every location path in the account. The product-list search is not applied. |
| RPT-002 | AI insights report | `/ai-report.aspx?id=` shows “Your Inventory Insights” with an AI-GENERATED badge. Any exception, including a bad id, goes to the map. No menu link in this repo. How reports are generated is outside the files that were read. |

---

## Not live customer features

Recorded so they are not documented as working UI.

| Item | Status |
| --- | --- |
| `Welcome.aspx` and `pages/guides/getting-started.aspx` | Redirect to `/Map` before their wizards run. |
| `Mobile/Map.aspx`, `Mobile/ProductEditorMap.aspx` | Redirect to unauthorized. |
| `Popups/CloneProduct.aspx` | Locked fields, no save. Live clone is PED-007. |
| `Dialogs/ProductDeleteConfirmation.aspx` | Unwired. Would delete quantity rows only. Live delete is PRD-011. |
| `SuccessProducts.aspx` | No caller. Live success is the check-in page. |
| `DocumentEditor.aspx` buttons | Literal text, no handlers. |
| Settings kitting checkbox | Hidden and unwired (DSP-008). |
| Lansweeper connect/sync on Settings | Commented out. Live path is an email request (LSW-001). |
| Trial, upgrade, and payment banners | Markup stays hidden. Toggle functions are never called. |
| Compact map tile sizes | Forced off. |
| Right-click map menu and free resize | Not implemented. |
| Product batches | `Batch_Class` is unused by the product UI. |

## Still outside this repository or not fully traced

- `api/inventory` stock math for Quick Scan, and the bodies of adjust, check-in, check-out, transfer, and clone.
- Whether `api/LocationClone` copies quantities.
- What each expiration replacement action does to stock.
- Kit API insert rules and which fields kit search matches.
- Which fields header search and map search match.
- What `productDeleter` removes besides the product row and the expiration call that is visible here.
- Database default quantity on the location `-2` row inserted when a product is created.
- Whether a read-only user can drag the map move handle.
- Which empty-map card wins for every zero-product / zero-location mix.
- OAuth scope labels, half-hour time zones, and the duplicate Lansweeper class binding.
- AI report generation and which ids are valid.

No runtime click-through was performed.
