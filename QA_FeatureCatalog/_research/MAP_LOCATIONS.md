# Map and locations — code audit

Source: CyberStockroom at `c:\Users\emadh\Documents\code\cs-website`. Traced from pages, controls, and `App_Code`. No application source was changed.

Live designer map is `Map.aspx` hosting `Controls/Map_CONTROL_2017.ascx` with `data--type-of-map="1"`. Almost all map behavior is inline JavaScript in that control plus `App_Code/Classes/Service Layer/Mapping/*`. `Scripts/Controls/mapControlJS.js` is not loaded by `Map.aspx`.

Layout for the 2017 map is stored per user in `CS_ADMIN.Users.GridsterCoordinates2017` (`Gridster_Utilities.ReadCoordinatesFromDB` / `WriteCoordinatesToDB`, about lines 1375–1386). Older `GridsterFunctions.vb` reads and writes `GridsterCoordinates` (no `2017`) and has no callers elsewhere in this repo.

Map type integers (`MapType.vb` and comments on the pages):

| Value | Enum | Where used |
| --- | --- | --- |
| 1 | Designer | `Map.aspx`, `MapDesignerNaked.aspx` |
| 2 | ProductEditor | `MapProductEditorNaked.aspx`. `Mobile/ProductEditorMap.aspx` sets 2 but the page redirects away |
| 3 | Minimalist | `_locationSelectorToggle.aspx`. `Mobile/Map.aspx` sets 3 but the page redirects away |
| 4 | Read_Only | `Map_read_only.aspx` |
| 5 | ProductEditor_ReadOnly | Defined. No page in this scope sets 5 |
| other | forced to Read_Only | `Map_CONTROL_2017.ascx.vb` `Page_Load` |

Parent id `-2` means the root (“All Locations”). Primary locations are children of `-2` and sit on the Gridster canvas. Nested locations are drawn inside a parent tile, not as their own Gridster widgets.

There is no right-click / `contextmenu` handler on the map. Location actions are a hover strip (desktop) or a bottom selection footer (narrow tablet designer). Multi-select ignores any pointer button other than the primary button (`e.button !== 0`).

External HTTP APIs (implementation is not in this repo; failure behavior below is only what the page does when the call fails):

- `https://code.cyberstockroom.com/api/LocationClone`
- `https://code.cyberstockroom.com/api/inventory?action=adjust`
- `https://code.cyberstockroom.com/api/inventory?action=clone`
- `https://code.cyberstockroom.com/api/map?mapFilter=`
- `https://code.cyberstockroom.com/api/products`
- `https://code.cyberstockroom.com/api/expiration/CS_PRODUCT_IN_HEADER`
- `/webAPI/settings.aspx/GetSharedMaps` and `GetSharedMapLayoutParts` (`webAPI/webAPI.js`)

---

## 1. Page inventory

| Route / control | Purpose | Who can access | How navigated | Key features |
| --- | --- | --- | --- | --- |
| `Map.aspx` | Designer inventory map | Signed-in users who are not `READ_ONLY`. Read-only users are sent to `Map_read_only`. Not signed in: map control sends `~/Login.aspx` | Main menu “Map” (`UserPage.master` `simpleRedirect('Map')`) | Create, move, lock, clone, delete, search, peek, check-in/out, drag transfer, zoom, settings |
| `Map.aspx.vb` | Page shell | Same as `Map.aspx` | — | View-location hover redirects to `Products`. Refresh event redirects to `Map` |
| `Map_read_only.aspx` | Same control, type 4 | Only `TypeOfUser = READ_ONLY`. Anyone else is sent to `/Map` | Redirect from `Map.aspx` | View products, location details, zoom, search. No floating “+”. Hover strip is view + details (+ V / 3D if eligible) |
| `MapDesignerNaked.aspx` | Designer map with no site chrome, for an iframe | Control still requires login. Page itself has no extra role check in `MapDesignerNaked.aspx.vb` | Loaded as an iframe (onboarding calls `parent.IFRAME_RELOAD`). `DisableMobileView="true"` | Designer tools. Hides hover strip, zoom label, and (when `welcome=1`) the reparent clasp. Two dismissible helpers stored in `localStorage` keys `helper1_closed` and `helper2_closed` |
| `MapProductEditorNaked.aspx` | Product quantity map, no site chrome | Control requires login. Read-only users hitting a ProductEditor map are sent to `/_admin/_unauthorized` | Query `ProductNumber`. Refresh reloads the same page | Click a location, type a quantity, Enter. Helpers `helper3_closed` / `helper4_closed`. `DisableMapStageLoader="true"` |
| `Mobile/Map.aspx` | Old mobile shell around `Map_CONTROL_MOBILE_2018` type 3 | **Unreachable.** `Mobile/Map.aspx.vb` `form1_Init` always `Response.Redirect("/_admin/_unauthorized")` | — | Would have been a minimalist map. Never rendered |
| `Mobile/ProductEditorMap.aspx` | Old mobile product map, type 2 on the 2018 control | **Unreachable.** `MAP_CONTROL_1_Init` always redirects to `/_admin/_unauthorized` | — | Never rendered |
| `Controls/Map_CONTROL_2017.ascx` | The live map | Login required. Designer or ProductEditor plus `READ_ONLY` → `/_admin/_unauthorized` | Embedded by the pages above and by `_locationSelectorToggle.aspx` | See features |
| `Controls/Map_CONTROL_MOBILE_2018.ascx` | Older, smaller map control (Gridster drag + zoom token `-6` only) | Only referenced by the two Mobile pages that immediately redirect | — | Not on the live Map page |
| `Controls/mapDashboard.ascx` | Prototype that calls `reMap()` in `mapControlJS.js` | Host page is unreachable | `mapDashboardTest.aspx` | Button “General Remap” with hardcoded `generalThresholdValue:10` |
| `mapDashboardTest.aspx` | Host for the dashboard control | **Unreachable.** `Init` redirects to `/_admin/_unauthorized` | — | — |
| `LocationEditor.aspx` | Edit one location: name, icon type, children, barcode, attachments, kiosk links | `READ_ONLY` → `/_admin/_unauthorized`. Missing/unknown location → `Location Error.html` | Hover **Edit**, or `LocationEditor.aspx?LoadType=EXISTING&LocationID=` | Rename, add child by type, view products, barcode, print barcode, attachments, check-in/out kiosk |
| `NewLocation.aspx` | Name a location that is about to be created | `READ_ONLY` → unauthorized | Fancybox from map toolbox or Location Editor toolbox. Query `ParentID`, `LocationType` | Single name field. Default text is `New {type name}` |
| `Popups/PeekLocationDetails.aspx` | Read-only location card: attachments list and barcode | Login via master. Unknown location → `Location Error.html`. Comment in the page: “THIS IS A READ ONLY PAGE” | Read-only hover **View Location Details** (`READ_ONLY` event) | Download existing attachments. Print barcode link. Upload control is hidden and has no click handler that opens it |
| `_locationSelectorToggle.aspx` | Pick a location on a minimalist map | `READ_ONLY` → unauthorized | Settings popups. Query `type=LANSWEEPER|DEFAULTCHECKIN|DEFAULTCHECKOUT` plus Lansweeper `id`, `category`, `name` | Click a location to save. **CLEAR Selection** |
| `Controls/LocationSelector_CONTROL.ascx` | Breadcrumb + nested menu of locations | Used inside editors and transfer UI, not a standalone page | Hover the breadcrumb | Pick a location; transfer page uses left/right of x=350 as FROM/TO |
| `MobileCreateLocation.ashx` → `MobileCreateLocationHandler.vb` | JSON create of a **root** location for the mobile main flow | 401 if not signed in. 403 if read-only. Parent must be `-2` | Not a page. POST JSON `{name, locationType, parentId}` | Inserts a location and writes activity `LOCATION__CREATE` |
| `Scripts/Controls/mapControlJS.js` | Older client map builder (`reMap`, hover icons) | Loaded only by `mapDashboard.ascx` | — | Not the live map. Hover onclick strings still contain VB leftovers (`" & LocationID & "`) |
| `App_Code/.../CS_Map.vb` | Older HTML-table map (`ReloadMap`) | No references found (`CS_Map.` / `New CS_Map`) | — | Treat as unused by current pages |
| `App_Code/.../GridsterFunctions.vb` | Older coordinate cookie/column helper | No callers found | — | Not the 2017 save path |

Gridster cell size actually applied on the live map (`Page_Load` calls `_setGridsterSize(0)`; comment: “Compact Features Not yet released”): width **100**, height **60**, horizontal margin **15**, vertical margin **30**, extra cols **100**, extra rows **100**, bottom padding rows **6**, right padding cols **6**. Compact sizes 40 / 25 / 15 exist in `_setGridsterSize` but are not selected. Minimum primary widget width is 2 cells (`Gridster_Utilities.OpenGridsterItem`: `Width = Math.Max(2, Width)`). `max_rows` in Gridster options is **100**.

---

## 2. Features

### Open the designer map

- Pages: `Map.aspx`, menu in `UserPage.master`
- What it does: Loads every location for the account and lays primary locations on a Gridster canvas using that user’s saved `GridsterCoordinates2017`. Nested locations are drawn inside their parent.
- Why a user uses it: See where stock sits and start check-in, check-out, transfer, or location edits.
- How to access: Main menu link “Map” → `simpleRedirect('Map')`.
- Steps: Sign in as a non-read-only user. Open Map.
- Options/settings and defaults: Map type 1. Stage loader is shown until layout finishes (`map-stage-loading`), unless the host sets `DisableMapStageLoader`.
- Permissions / visibility conditions: `Map.aspx.vb`: `If MO.UserCredentials.TypeOfUser = User_Legacy.TypeOfUserAccount.READ_ONLY Then Response.Redirect("Map_read_only")`. Control: `If UserSettings.isLoggedIn = False Then Response.Redirect("~/Login.aspx")`.
- Validation, limits, failure behavior: If Gridster init throws, the page logs `[Map] Gridster init failed` and still tries to reveal the stage.
- Expected result and side effects: `RegisterPage(..., "Map", ...)`. No inventory change.
- Edge cases: `AutoHighlight` query uses `Session("LocationID_VIEW")` as the product-editor default location. That query is read on every map type, but auto-open of the quantity box only runs for ProductEditor.
- Related features: Read-only map, zoom, search.
- Code evidence: `Map.aspx` lines 145–155; `Map.aspx.vb` lines 8–18; `Map_CONTROL_2017.ascx.vb` `Page_Load` lines 109–258; `CS_Map_Reusable.GetMap` line 28.
- Confidence: Confirmed
- Suggested KB title: Open the inventory map

### Read-only map

- Pages: `Map_read_only.aspx`
- What it does: Same canvas as the designer map, but the hover strip only offers View, optional V/3D toggles, and “View Location Details…”. The floating “+” is hidden. Clicking a location still opens the product peek.
- Why a user uses it: A read-only account can see the map and open the product list without editing locations or quantities.
- How to access: Automatic redirect from `Map.aspx` when the user type is read-only. A non-read-only user who opens this page is sent to `/Map`.
- Steps: Sign in as read-only. The app lands on this page instead of `Map.aspx`.
- Options/settings and defaults: `data--type-of-map="4"`.
- Permissions / visibility conditions: `Map_read_only.aspx.vb`: `If MO.UserCredentials.TypeOfUser <> User_Legacy.TypeOfUserAccount.READ_ONLY Then Response.Redirect("/Map")`. Designer/ProductEditor plus read-only inside the control: `Response.Redirect("/_admin/_unauthorized")` (embedded maps).
- Validation, limits, failure behavior: View click sets `LocationID_VIEW` and the page redirects to `Products_read_only`.
- Expected result and side effects: No create/move/delete/transfer controls on the hover strip. Gridster still emits a move handle for Read_Only (`OpenGridsterItem` adds `<header class="gridster-move-handle">` for Designer **or** Read_Only). Whether a read-only user can actually drag is not separately blocked in `mapGetGridsterOptions`. Confidence on “read-only users cannot drag” is **Inferred** as weaker than the hover-strip restriction: the handle is still rendered.
- Edge cases: Floating add tab `Visible = False` for types 2, 4, and 5.
- Related features: Peek products, peek location details, view products.
- Code evidence: `Map_read_only.aspx` line 33; `Map_read_only.aspx.vb` lines 11–20; `Map_Styling.GetLocationHoverDiv` lines 192–206; `Map_CONTROL_2017.ascx.vb` lines 219–233.
- Confidence: Confirmed for the redirect and hover contents. Inferred for whether the move handle still drags.
- Suggested KB title: Read-only inventory map

### Location types and icons

- Pages: Map toolbox, Location Editor toolbox, `NewLocation.aspx`, `Location.GetLocationTypeName`
- What it does: Each location has an integer type that picks a sprite (`location-small-{n}` / `Images/Locations/{n}.png`).
- Why a user uses it: Tell buildings, rooms, bins, and vehicles apart on the map.
- How to access: Chosen when the location is created. The editor shows the current type image. This audit did not find a control that changes type after create.
- Steps: Pick a type in the toolbox, then name the location.
- Options/settings and defaults: From `Location.GetLocationTypeName` lines 521–543:

  | Type | Name | Toolbox label |
  | --- | --- | --- |
  | 0 | Building | BUILDING |
  | 1 | Warehouse | WAREHOUSE |
  | 2 | Store | STORE |
  | 3 | Floor | FLOOR |
  | 4 | Room | ROOM |
  | 5 | Closet | CLOSET |
  | 6 | Shelf | SHELF |
  | 7 | Bin | BIN |
  | 8 | Vehicle | VEHICLE |
  | else | Location | — |

  Location Editor `InitializeNewLocation` defaults a missing/negative type to **0** (building) and a missing parent to **-2**.
- Permissions / visibility conditions: Toolbox is designer-only (floating “+” hidden for non-designer types).
- Validation, limits, failure behavior: `MobileCreateLocationHandler` rejects `locationType` outside 0–8 with “Invalid location type.”
- Expected result and side effects: Type is stored in `Locations.LocationType`. Create activity records the type.
- Edge cases: “All Locations” (`-2`) uses `Images/Locations/-2.png` in the editor.
- Related features: Create location, 3D badge.
- Code evidence: `Location.vb` `GetLocationTypeName` lines 521–543; toolbox markup `Map_CONTROL_2017.ascx` lines 15905–15944; `LocationEditor.aspx` lines 170–262.
- Confidence: Confirmed
- Suggested KB title: Location icons and types

### Full, ghosted, and child quantity labels

- Pages: Every map type, drawn in `Map_Styling.ApplyStyling` and `GetLocationCountLabel`
- What it does: A location with its own quantity greater than 0 gets the `--full` class. A location with zero of its own and quantity only in children gets `--ghosted`, except a 3D parent, which is drawn `--full` when children hold quantity (and `map-3d-parent--empty` when its own quantity is 0). A 3D parent also gets a “3D” badge.
- Why a user uses it: See which tiles actually hold stock versus which only contain stock in children.
- How to access: Automatic on render.
- Steps: None.
- Options/settings and defaults: Primary count text rules (`GetLocationCountLabel`): own and children both > 0 → `own (children)`; only own → own number; only children → `(children)` plus `map-label-count--children-only`; both 0 → label hidden. Secondary tiles show own quantity only, except a 3D parent with children-only stock shows `(children)`.
- Permissions / visibility conditions: Applied for all map types (“Color: Full/Ghosted - [All Map Types]”).
- Validation, limits, failure behavior: Quantities come from `Map_Utilities.GetQuantityinLocation` / `GetQuantityinChildren`.
- Expected result and side effects: Display only until a later edit changes quantity.
- Edge cases: Drag-from-location requires `mapLocationElIsFull`. A 3D parent is “full” for drag only when its **own** `qty` attribute is > 0, not merely because children have stock.
- Related features: Search coloring, product peek, drag transfer.
- Code evidence: `Map_Styling.vb` lines 224–261 and 326–418; `mapLocationElIsFull` lines 9152–9160.
- Confidence: Confirmed
- Suggested KB title: How location tiles show quantity

### Create a location from the map

- Pages: Designer map (`Map.aspx`, `MapDesignerNaked.aspx`)
- What it does: Opens a type toolbox, then `NewLocation.aspx` in a Fancybox (550×180) so the user names the new location. Saving creates the row and asks the map to reload.
- Why a user uses it: Add a building, room, bin, vehicle, or other place.
- How to access:
  - Floating **+** at the right (`floating_add_tab`, title “Create a new location...”) calls `HoverAddClick(..., -2)` so the parent is the root.
  - Hovering a designer tile calls `ShowHoverChild`, which can show a small **+** on that tile. That **+** calls `HoverAddClick` with the tile’s location id (child of that location).
  - 3D stack has an **Add** button (`aria-label` “Add a location to this stack”) because hover-add is hidden on 3D parents and on locations inside a 3D stack (`LocationParentHidesChildHoverAdd`).
- Steps:
  1. Click **+** (map corner, tile, or 3D stack).
  2. Click a type (BUILDING through VEHICLE).
  3. Fancybox opens `NewLocation.aspx?ParentID=&LocationType=`.
  4. Edit the name (default `New {type}`) and commit the editable field.
  5. Map reloads. A new primary location is highlighted (`COOKIE_MAP_HIGHLIGHT_NEW_LOCATION_ID`).
- Options/settings and defaults: Nine types, 0–8. Default name from `NewLocation.aspx.vb`: `"New " & LocationTypeName`. Name field uses `FieldType.NEW_LOCATION_NAME` with the message “That location name is already in use!”
- Permissions / visibility conditions: Floating **+** hidden when map type is 2, 4, or 5. Read-only users never get the designer page. `NewLocation.aspx.vb`: read-only → `/_admin/_unauthorized`. Empty-map prompt swallows the floating **+** click (`mapEmptyPromptIsActive`).
- Validation, limits, failure behavior: Duplicate-name message is supplied to the editable-field control; the actual uniqueness check lives in that control (not re-traced here). `CreateLocation_FASTER_DEBUG` (prompt + `location_create`) is **not** called; `CreateLocation` is the live path and only opens the Fancybox.
- Expected result and side effects: `Location.CreateNewLocation` inserts `Name`, `LocationType`, `ParentID`, `LocationPath` and registers activity `LOCATION__CREATE` with quantity array `"1"`. Cookies: `COOKIE_LOCATION_EDITOR_PAGE_RELOAD=TRUE`, `COOKIE_MAP_PAGE_RELOAD=TRUE`. If parent is `-2`, `CookieRefreshRequired=2` (primary, so coordinates get a new slot). Otherwise `CookieRefreshRequired=1`. After a primary create, `btn_hidden_create_new_location_Click` appends coordinates via `_getNewCoordinates` and highlights the newest primary id.
- Edge cases: Clicking the dimmed tarp or leaving the toolbox calls `ClearHoverAdd`. On a one-location map, coach text says “Create Sub-Locations” on the tile and “Create New Location” near the floating **+**.
- Related features: Location Editor add-child, mobile create handler, clone.
- Code evidence: `HoverAddClick` lines 4949–4990; `CreateLocation` lines 9735–9750; toolbox 15905–15944; `NewLocation.aspx.vb` lines 11–78; `Location.CreateNewLocation` lines 321–359; `btn_hidden_create_new_location_Click` lines 305–338; `LocationParentHidesChildHoverAdd` lines 461–467.
- Confidence: Confirmed
- Suggested KB title: Add a location on the map

### Name a new location (`NewLocation.aspx`)

- Pages: `NewLocation.aspx`
- What it does: Shows the type thumbnail and an editable name. On save it closes the Fancybox. The insert itself is done by the editable-field handler (`FieldType.NEW_LOCATION_NAME`), not by `CreateNewLocation` in this page. `HANDLER_FIELD_EDITED` only sets reload cookies and `CookieRefreshRequired`.
- Why a user uses it: Give the new place a name before it appears on the map.
- How to access: Fancybox from `CreateLocation` or from Location Editor `forceDrop` / `drop`.
- Steps: Change the name. Commit the field. Fancybox closes. Parent map reloads.
- Options/settings and defaults: Query `ParentID`, `LocationType`. Image `/Images/Locations/{type}.png`.
- Permissions / visibility conditions: Read-only redirected to unauthorized.
- Validation, limits, failure behavior: Duplicate message string “That location name is already in use!” is passed into the field. If query values throw, `Page_Init` exits before building the field.
- Expected result and side effects: Same cookies as map create. Activity row is written by the field-save path (same family as `CreateNewLocation`; the page comment says the path must match `NEW_LOCATION_NAME`).
- Edge cases: `ParentID = -2` sets refresh cookie `2`; any other parent sets `1`.
- Related features: Create from map, Location Editor toolbox.
- Code evidence: `NewLocation.aspx.vb` lines 21–78.
- Confidence: Confirmed for the page flow. The SQL insert is inside the editable-field control, not this file.
- Suggested KB title: Name a new location

### Rename a location

- Pages: `LocationEditor.aspx`
- What it does: The location name is an editable field (`FieldType.LOCATION_NAME`). “All Locations” (`id = -2`) is shown as the text “All Locations” and is not editable (`PropertiesContstruct` editable flag false).
- Why a user uses it: Fix a label without recreating the place.
- How to access: Map hover or mobile footer **Edit** → `LocationEditor.aspx?LoadType=EXISTING&LocationID=`. Then edit the name at the top.
- Steps: Open the editor. Change the name. Commit the field. `HANDLER_FIELD_EDITED` runs.
- Options/settings and defaults: Duplicate message: “That location name is already in use!”
- Permissions / visibility conditions: Read-only cannot open Location Editor.
- Validation, limits, failure behavior: Uniqueness is enforced by the editable-field control (message is wired here). This page does not show a separate rename dialog.
- Expected result and side effects: Name update. Map is not given a highlight cookie from this handler (that cookie is for create/clone). Editor sets `COOKIE_LOCATION_EDITOR_PAGE_RELOAD=FALSE` on entry and writes `COOKIE_LOCATION_EDITOR_ID`.
- Edge cases: Clone’s “Auto-Rename Sub-Locations” is a different feature and does not rename the new root.
- Related features: Clone keyword rename, location path breadcrumbs.
- Code evidence: `LocationEditor.aspx.vb` `LoadNameField` lines 250–273; `MapProcessEvent_JS` case `EDIT` lines 9252–9255.
- Confidence: Confirmed
- Suggested KB title: Rename a location

### Location Editor

- Pages: `LocationEditor.aspx`, `LocationEditor.aspx.vb`, `Scripts/Pages/LocationEditor/LocationEditor.js`
- What it does: One-location workspace. Shows type image, editable name, breadcrumb location selector, child table, “ADD NEW” type toolbox, attachments, barcode, print barcode, view products, and check-in/out kiosk links.
- Why a user uses it: Rename, add children, attach files, print a location barcode, or jump to products in that place.
- How to access: Map **Edit**. Direct URL `LocationEditor.aspx?LoadType=EXISTING&LocationID=`. `LoadType` other than `EXISTING` calls `InitializeNewLocation`, which immediately creates “New {type}” and redirects to the existing editor for the new id.
- Steps: Open editor. Use the toolbox (click or HTML5 drag onto the page) to add a child via `NewLocation.aspx`. Click a child row to open that child. Click **View Products**.
- Options/settings and defaults: Toolbox labels match the nine types. Barcode box starts from the stored barcode. Attachment delete asks `confirm('Are you sure you want to delete this attachment?')`.
- Permissions / visibility conditions: `If MO.UserCredentials.TypeOfUser = READ_ONLY Then Response.Redirect("/_admin/_unauthorized")`. Unknown id → `Location Error.html`.
- Validation, limits, failure behavior: Barcode save (`hidden_barcode_btn_Click`): if `_repo._barcodeExists` is true, the text box turns background `#AF5756` with white text and does not save. Enter in the barcode box posts only when the value changed.
- Expected result and side effects: Sets `DisplaySettings.LocationID_VIEW` to this location. **View Products** uses that so the products page opens filtered here (same idea as map View). Child create uses `Location.CreateNewLocation` when `LoadType` is not EXISTING.
- Edge cases: `LocationEditor.js` `drop` / `forceDrop` only open `NewLocation.aspx`; they do not insert by themselves. Kiosk links: `buildQuickScanKioskUrl` → `/Popups/QuickScan.aspx` or, when `matchMedia("(max-width: 900px)")`, `/MOBILE_QuickScan.aspx`, with `?mode=checkin|checkout&locationID=`.
- Related features: Attachments, barcode, peek details, create child.
- Code evidence: `LocationEditor.aspx.vb` `Page_Init` 125–171, `LoadCorrectMode` 175–247, barcode 620–638; `LocationEditor.aspx` toolbox 160–262, kiosk 402–416 and 605–619; `LocationEditor.js` lines 25–66.
- Confidence: Confirmed
- Suggested KB title: Edit a location

### Move primary locations on the canvas

- Pages: Designer map (and the move handle is also emitted for Read_Only)
- What it does: Drag the diamond header (`gridster-move-handle`, character `&#10070;`) to change a primary location’s column and row. On drop, coordinates are saved.
- Why a user uses it: Arrange the top-level map.
- How to access: Drag the header on a primary tile. Not available as a separate menu item. Nested locations do not have their own Gridster header; they move with the parent or via the reparent clasp.
- Steps: Unlock the map if it is locked (default is locked). Drag the header. Release.
- Options/settings and defaults: Gridster: `avoid_overlapped_widgets: true`, `shift_larger_widgets_down: false`, `shift_widgets_up: false`, `helper: 'clone'`, `autoscroll: false`, `collision.wait_for_mouseup: true`, `max_rows: 100`. There is **no** `resize` option, so users do not drag a corner to resize. Tile width/height are computed from how many children the location has (`ComputePrimaryGridsterRowSpan` and column units).
- Permissions / visibility conditions: Handle markup only when type is Designer or Read_Only. Drag start is cancelled when multi-select is blocking that widget.
- Validation, limits, failure behavior: While locked, overlap is highlighted and the drop snaps back (`mapHookGridsterMapLock`, `mapLockFlashCancelledWidget`). Unlocked drops call `RemoveOverlaps` then `_saveCoordinates`.
- Expected result and side effects: Updates `GridsterCoordinates2017` for this user only. Inventory is unchanged.
- Edge cases: Dragging near the viewport edge scrolls the map (`mapEdgeScroll*`) and can show a light ghost. Dropping onto the minimap can commit the widget at the viewport center (`mapViewFinderPortalCommitGridsterDropAtCenter`). iOS suppresses native HTML5 drag on tiles so the OS does not open multi-window UI.
- Related features: Map lock, multi-select move, minimap, reparent.
- Code evidence: `mapGetGridsterOptions` lines 2988–3078; `Gridster_Utilities.OpenGridsterItem` lines 93–105; `mapHookGridsterMapLock` lines 2886–2916.
- Confidence: Confirmed
- Suggested KB title: Move locations on the map

### Map lock

- Pages: Designer map footer (`#mapLockButton`), only when `DisableMobileView` is false (`<% If Not DisableMobileView %>`)
- What it does: When locked, a drag that would overlap or push another widget is cancelled, the tile flashes, and the lock button pulses. Unlocking allows free moves and runs `RemoveOverlaps` after a drop. Turning the lock on also cancels an in-progress reparent.
- Why a user uses it: Keep the layout from being nudged while dragging products, or unlock it to rearrange.
- How to access: Lock button in the map toolbar. `aria-label` / `title` while locked: “unlock map to move locations freely”. The button starts with class `map-lock-btn--on`.
- Steps: Click the lock. Layout preference is written and `_saveCoordinates()` runs (no full reload).
- Options/settings and defaults: **Default is locked.** `Gridster_Utilities` comment: “Absent = locked; ,-21 = unlocked.” Token `-19` = locked, `-21` = unlocked. JS: `mapLockedPref = (v !== mapUnlockedToken)` so any value other than -21, including a missing field, is locked. Markup hidden field starts at `Value=""` which is not -21.
- Permissions / visibility conditions: Button is inside the mobile-footer placeholder and inside `If Not DisableMobileView`. `MapDesignerNaked` sets `DisableMobileView="true"`, so that iframe does not render the lock button. The lock preference is still read from saved coordinates.
- Validation, limits, failure behavior: Save uses the same coordinate writer as other layout changes. No separate error dialog if save fails (the generic `_saveCoordinates` path).
- Expected result and side effects: Token `-19` or `-21` stored on the user’s coordinate string. No inventory change.
- Edge cases: `mapMapLockToggle` does not reload the page. Body class `map-layout-locked` is applied when locked.
- Related features: Move primary locations, reparent.
- Code evidence: Button lines 10637–10648; `mapMapLockToggle` 2540–2550; `mapReadMapLockedPreference` 1717–1726; `Gridster_Utilities.vb` lines 57–62; `mapHookGridsterMapLock` 2886+.
- Confidence: Confirmed
- Suggested KB title: Lock or unlock the map layout

### Snap a location onto a different parent (reparent)

- Pages: Designer map
- What it does: A clasp on the location (“Snap off location and move to a different parent.”) starts a mode where the next click chooses a new parent tile or empty canvas. Nested locations stay with it. Confirm dialog: title “Move location?”, body “Move this location? Nested locations stay with it.”, buttons **Cancel** and **Move**.
- Why a user uses it: Move a room from one building to another, or promote/demote a location, without deleting it.
- How to access: Click `.map-reparent-clasp`. Hidden on `MapDesignerNaked` when the query contains `welcome=1`.
- Steps:
  1. Click the clasp.
  2. Banner: “Click a new parent or empty space on the map to move this location.” **Cancel** or Escape aborts.
  3. Click a tile or empty map space.
  4. Confirm **Move**.
  5. Postback `btn_hidden_reparent_coordinates_Click` updates parent and coordinates, then the map reloads.
- Options/settings and defaults: Column/row default to 1 if the posted values are &lt; 1. New parent `-2` means “make it primary” (empty canvas).
- Permissions / visibility conditions: Clasp is built for locations in `GetLocationReparentClasp`. Not offered on the read-only hover strip (the clasp is separate from the hover icons). Designer naked + `welcome=1` hides `.map-reparent-clasp`.
- Validation, limits, failure behavior: Invalid targets get class `map-reparent-invalid`. Failures open “Could not move location” / “Could not move this location.” with **OK** (`mapReparentShowErrorModal`). Server parses ids with `Integer.TryParse`; bad values become 0.
- Expected result and side effects: Parent id and, for primary locations, the coordinate pair change. Inventory quantities are not moved by this click (stock stays on the same location ids).
- Edge cases: Turning the map lock on calls `mapReparentCancel`. Clicks on zoom, filter, modals, checkout strip, and similar chrome are ignored (`mapReparentIsChrome`).
- Related features: Map lock, move primary locations, clone (clone copies structure; reparent moves the same ids).
- Code evidence: `GetLocationReparentClasp` lines 215–221; `mapReparentClaspClick` 5218; banner 5092–5106; confirm modal 10801–10816; `btn_hidden_reparent_coordinates_Click` 342–365.
- Confidence: Confirmed for the UI and postback. The exact SQL that changes `ParentID` is inside the remainder of that click handler (file continues past line 365); the posted fields are location id, was-primary, old index, new parent, col, row.
- Suggested KB title: Move a location under a different parent

### Tile size (not a free resize)

- Pages: Designer map rendering
- What it does: Primary tile `data-sizex` / `data-sizey` grow from the number and layout of children (horizontal children add width; vertical stacks add height). Secondary tiles use `GetSecondaryTileColumnUnits`. An only-child chain with one column is set to width `186px`. Wider nests use `GRIDSTER_WIDTH_PX * columnUnits - 6` (constant comment: 106px per block, “6px addition”).
- Why a user uses it: The tile gets bigger when it has more children. There is no user “resize handle.”
- How to access: Add or remove children, or turn vertical / 3D on or off, then the map reloads or reflows.
- Steps: Add a sub-location or toggle V / 3D.
- Options/settings and defaults: Minimum primary width 2 grid cells. `mapReflowPrimaryOverlaps` can nudge primaries after a vertical layout load.
- Permissions / visibility conditions: Size is computed for every map type. Only designer drag can change position.
- Validation, limits, failure behavior: `max_rows: 100` on the Gridster widget. Extra rows/cols of the canvas are 100.
- Expected result and side effects: Layout only.
- Edge cases: Compact mode would shrink the cell to 40, 25, or 15 but `Page_Load` forces mode 0.
- Related features: Vertical stack, 3D stack, create child.
- Code evidence: `Gridster_Utilities.OpenGridsterItem` 93–96; `Map_Styling.vb` 420–437; `CS_Map_Reusable.GetPrimaryBlock` 120–122; `mapGetGridsterOptions` has no `resize` key.
- Confidence: Confirmed
- Suggested KB title: Why a location tile is wider or taller

### Delete a location

- Pages: Designer hover / mobile footer → `ConfirmationDialog.aspx?ACTION=DELETE&LocationID=`
- What it does: Confirms, checks out every quantity in that location and its children, deletes those location rows and their quantity rows, and if it was a primary location removes its coordinate pair.
- Why a user uses it: Remove a place that should no longer exist.
- How to access: Hover strip **Delete** (tooltip “Delete this location...”) or mobile footer **Delete**.
- Steps:
  1. Click Delete.
  2. Dialog shows the name, path, and type image.
  3. Message (verbatim): “Are your sure you want to DELETE this location?” plus “All sub-locations will be deleted. Existing products will be checked out automatically.”
  4. Click **YES** (`btn_yes_delete`).
- Options/settings and defaults: None beyond YES. (NO/cancel is the Fancybox close; not re-read here.)
- Permissions / visibility conditions: Delete icon is on the non-read-only hover strip only (`GetLocationHoverDiv` `If read_only`).
- Validation, limits, failure behavior: Cookie `LocationToDelete` must exist or the click does nothing. Checkout activity is skipped when total quantity is 0.
- Expected result and side effects:
  - Activity `INVENTORY__CHECK_OUT` with comment `Items cleared before deleting location '{name}' ({id})` when quantity &gt; 0. The code comment says “Check out products before deleting”; the implementation **registers that activity** and then **deletes the quantity rows**. It does not show a transfer page. Whether a separate checkout destination location is updated was not found in this function — quantities are removed by `DELETE FROM Quantities`.
  - Activity `LOCATION__DELETE` with comment `Deleted location '{name}' ({id})`.
  - Primary locations: `RemovePrimaryPairAtIndexFromDualLayout` on the saved coordinate string.
  - Map refresh is required (`_requireMapRefresh`).
- Edge cases: Children are included (`GetAllChildren` / `LocationAndChildrenAreEmpty` — the latter’s name collects ids; delete still runs). Order of primary coordinates is `ParentID = -2 ORDER BY LocationID ASC`.
- Related features: Check-out, activity history.
- Code evidence: `MapProcessEvent_JS` case `DELETE` 9258–9262; `ConfirmationDialog.aspx` lines 36–39; `ConfirmationDialog.aspx.vb` `btn_yes_delete_Click` 87–109, `CheckoutProductsBeforeDeletingLocation` 113–155, `DeleteLocationFunction` 185–220.
- Confidence: Confirmed
- Suggested KB title: Delete a location

### Clone a location (structure)

- Pages: Designer map clone modal
- What it does: Copies a location (server clone API), asks for a new name, and can rename sub-location names by a keyword. The new root keeps the typed name. After the API returns, the page postback highlights the new location and may apply vertical/3D paths and keyword renames.
- Why a user uses it: Duplicate a room or bin layout.
- How to access: Hover **Clone** (“Clone this location...”) or mobile footer **Clone**.
- Steps:
  1. Click Clone.
  2. Modal title “Name the New Location”. Name max length **255**.
  3. Optional switch **Auto-Rename Sub-Locations** (off by default; keyword fields start `disabled`). Tip: “Replaces a whole word or hyphen-separated part in sub-location names. For example, A32 to B45 renames A32-1 to B45-1. The new location itself keeps the name you entered.”
  4. Click **Clone** or Cancel.
- Options/settings and defaults: Suggested name is the source plus ` (Copy)`, then ` (Copy 2)`, ` (Copy 3)`, up to 999 tries, truncated so the whole name is ≤ 255. Keyword and “Replace with” max length 255. Switch starts off.
- Permissions / visibility conditions: Clone is not on the read-only hover strip. Blocked while a multi-select gesture is active (`mapMultiSelectIsBlockingClone` is about Ctrl+inventory copy, not this modal).
- Validation, limits, failure behavior:
  - Empty name: no specific string beyond the warning element.
  - Same name as the source (`mapCloneNameConflict` returns `'same'`) or a sibling (`'taken'`) blocks confirm via `mapCloneModalRefreshNameGate`.
  - API error: tarp hides, vertical-path and rename hidden fields are cleared, `console.log`. User stays on the map.
  - Keyword rename skips blank results and sibling-name collisions; one transaction; database error rolls back (`LocationApplicationService.ApplyKeywordRenameViaIdMap`).
- Expected result and side effects: POST `https://code.cyberstockroom.com/api/LocationClone` with headers `X-CS-TOKEN`, `X-CS-NEW-LOCATION-NAME`, `X-CS-CLONE-LOCATION-ID`. Then `btn_hidden_create_new_location_Click` runs `ApplyClonedSubtreePostProcessing` for vertical/3D and keyword rename, writes highlight and optional `COOKIE_MAP_CLONE_RENAME_NOTICE`, and reloads. Primary clones also get a new coordinate slot. Inventory copy is **not** this button (see Ctrl+drop).
- Edge cases: Matching is case-insensitive for the keyword. The new location’s own name is not keyword-replaced (tooltip and `mapSetCloneNameReplaceHidden` pass the typed name).
- Related features: Copy inventory with Ctrl, rename, vertical/3D (clone tries to preserve those layouts).
- Code evidence: Modal 10756–10798; `cloneLocation` 10251–10284; `mapCloneSuggestedName` 9863–9878; `Map_CONTROL_2017.ascx.vb` 305–338 and `ApplyClonedSubtreePostProcessing` 502; `LocationApplicationService.vb` 54–109.
- Confidence: Confirmed for the page. The clone API’s exact copy rules (whether quantities are copied) are **outside this repo** — Uncertain. The page treats it as a structure clone and does a separate inventory clone only for Ctrl+drop.
- Suggested KB title: Clone a location

### Copy inventory onto another location (Ctrl + drop)

- Pages: Designer map
- What it does: If Ctrl is held, dropping a full location onto another location asks to copy stock. Confirm text: “Are you sure you want to copy the contents to this location? Any existing items will be cleared first.”
- Why a user uses it: Make one location’s stock match another.
- How to access: Hold Ctrl (`_CloneTriggered = true` on keydown). Drag a full location. Drop on a different location. Not available during multi-select (Ctrl is used for selection, and `_CloneTriggered` is forced false).
- Steps: Hold Ctrl, drag, drop, confirm.
- Options/settings and defaults: None.
- Permissions / visibility conditions: Drag only starts when `mapLocationElIsFull`. Same location, or id `-2`, is ignored. Designer drag handlers are only attached for Designer (`EnableDragDrop`).
- Validation, limits, failure behavior: API error hides the tarp and logs `xhr.message`. No user-facing message in this function. Cancel on the confirm does not call the API.
- Expected result and side effects: POST `https://code.cyberstockroom.com/api/inventory?action=clone&SourceID=&DestinationID=` with `X-CS-TOKEN`. Success reloads the page. The confirm text says existing items at the destination are cleared first; that behavior is in the external API.
- Edge cases: If a product chip is being dragged (`_PeekDragProductFilter` length &gt; 0), this copy path is skipped and the drop is a transfer instead.
- Related features: Drag transfer, clone location structure.
- Code evidence: `MapProcessEvent_JS` case `DROP` 9378–9388; keydown 9164–9171; `_cloneContents` 9712–9732.
- Confidence: Confirmed for the prompt and call. Cleared-first behavior is the confirm string plus an external API.
- Suggested KB title: Copy stock from one location to another

### ABC sort

- Pages: Map settings popup, designer toolbar (`#mapSettingsAbcSortSwitch`)
- What it does: When on, each parent’s direct children are sorted by name (case-insensitive), then by location id. When off, children stay in location-id order (the comment on the token: “Absent = LocationID order”).
- Why a user uses it: Find bins alphabetically inside a parent.
- How to access: Gear **Map settings** → row “ABC Sort”. Title: “When on, child locations are shown in alphabetical order.”
- Steps: Turn the switch on or off. The page shows a loader, saves coordinates, and reloads.
- Options/settings and defaults: **Default off.** Token `-20` means on. Hidden field initial `Value="0"`. JS `mapAbcSortPref` is true only when the hidden value is `-20`.
- Permissions / visibility conditions: Row is inside `If Not DisableMobileView`, so `MapDesignerNaked` does not show this settings popup. The saved flag still affects render anywhere `GetAbcSortFromRaw` is read (`CS_Map_Reusable.GetChildLocationsForRender`).
- Validation, limits, failure behavior: If `_saveCoordinates` returns false, loader hides and the console logs `[Map] ABC_SORT_TOGGLE: could not save coordinates.` The switch has already been flipped in memory; the reload does not happen.
- Expected result and side effects: Only child **display** order. Primary Gridster positions are a separate coordinate list. No inventory change.
- Edge cases: Sort is skipped when there are fewer than 2 children. 3D stack children use the same sorted list (`GetChildLocationsForRender`).
- Related features: Shared map sync (layout string includes the ABC token), vertical/3D.
- Code evidence: Popup row 10673–10685; `mapAbcSortToggle` 2514–2537; `CS_Map_Reusable.GetChildLocationsForRender` 128–136; `Gridster_Utilities` lines 59–60 and `ApplyAbcSortToCombined` 1051.
- Confidence: Confirmed
- Suggested KB title: Sort child locations alphabetically

### Shared maps

- Pages: Map settings → “Shared Maps”; settings page is where an admin turns sharing on (empty-state copy only; settings UI was not fully traced in this pass)
- What it does: Lists other users on the account whose layout is marked shareable. Choosing one opens “Sync your Map Layout” with that person’s name and email. Warning: “If you sync to this layout, you will lose your existing layout. Are you sure you want to continue?” Buttons: **Keep my layout** and **Sync**.
- Why a user uses it: Adopt a teammate’s arrangement instead of dragging every tile.
- How to access: Gear menu → Shared Maps. Empty text: “No shared maps. Admins can share their maps in the Settings page.” Load failure: “Could not load shared maps.”
- Steps: Open the submenu (loads once and caches). Pick a person. Read the warning. Click **Sync** or **Keep my layout**. Escape or backdrop = cancel, unless a sync is in flight.
- Options/settings and defaults: Share flag in the coordinate string is token `-16` plus the marker `CS_MAP_SHAREABLE_ON`. This map page reads `hidden_SHARE_MAP_LAYOUT` but the gear menu here does not contain the switch that turns sharing on. That switch is on Settings (stated by the empty message; the settings control itself is outside this file).
- Permissions / visibility conditions: `get_shared_maps` posts the csToken to `/webAPI/settings.aspx/GetSharedMaps`. Server-side who appears in the list is in `settings.aspx` (not fully opened here). The map control only renders what that method returns.
- Validation, limits, failure behavior: Missing `get_shared_map_layout_parts`: “Sync is not available. Please refresh the page.” Save failure: “Could not save the synced layout. Please try again.” Exception: “Could not sync this layout. Please try again.” Button text while working: “Syncing…”.
- Expected result and side effects: Copies the other user’s coordinate segment, standard zoom, mobile zoom, vertical parent ids, 3D parent ids, and vertical-migrated flag into this user’s hidden fields, saves, and reloads. The warning says the existing layout is lost. Inventory is not part of the payload (coordinates and layout flags only).
- Edge cases: Submenu shows “Loading…” until the call returns. Cache means a later open does not refetch until reload.
- Related features: Map lock, ABC sort, zoom (those ride inside the coordinate string).
- Code evidence: Menu row 10707–10712; `mapLoadSharedMapsSubmenu` 2210–2246; modal 10858–10877; `mapSyncLayoutModalConfirm` 2344–2417; `webAPI.js` `get_shared_maps` 97–117 and `get_shared_map_layout_parts` 120–130; `ShareMapLayoutToken` line 52.
- Confidence: Confirmed for sync UX. Who is allowed to enable sharing is **Inferred** from the empty-state sentence (“Admins can share…”), not from a settings permission check in this scope.
- Suggested KB title: Use a teammate’s map layout

### Zoom

- Pages: `Map.aspx` and `Map_read_only.aspx` (top-right “Type +/- to zoom”), and the in-control toolbar when mobile chrome is on
- What it does: Scales the map. Buttons and the + / − keys multiply zoom by 1.1 or 0.9. Pinch works on touch. Each layout track stores its own zoom.
- Why a user uses it: See the whole warehouse or read a small bin.
- How to access: Zoom in / zoom out buttons. Keyboard + and − when focus is not in a text field. Two-finger pinch (`mapPinchZoomInit`).
- Steps: Click + or −, or press the keys, or pinch.
- Options/settings and defaults:
  - Desktop min **0.1**, max **1** (`getMapZoomMin` / `getMapZoomMax` when not a touch client).
  - Touch min **0.15**, max **2.2**.
  - Initial zoom if nothing is stored: mobile track or touch client **0.74** (`mapDefaultMobileZoom` and `MAP_TOUCH_INITIAL_ZOOM`); otherwise **1**.
  - Stored zoom uses token `-6` (standard) and `-7` (mobile), scaled by 1000 in the coordinate string (`ZoomScale`). `DefaultStandardZoom = 1.0`, `DefaultMobileZoom = 0.74`.
  - Narrow viewport (`mapZoomLayoutUsesMobileTrack`, breakpoint comment max-width 900px) uses the mobile zoom number.
- Permissions / visibility conditions: `Map.aspx` hides `.zoom-instructions` at `max-width: 900px` because the in-control toolbar has its own zoom. Keyboard zoom is blocked while the single-location coach is active, while clone/other modals are open, or while typing in input/textarea/select/contenteditable (`mapShouldBlockKeyboardZoom`, `mapIsTypingTarget`).
- Validation, limits, failure behavior: `mapNormalizeZoomForStorage` replaces NaN or ≤ 0 with the fallback. Ctrl+mousewheel is `preventDefault` so the browser does not zoom the whole page (`$(window).bind('mousewheel'...`).
- Expected result and side effects: Zoom is written into the coordinate string on a debounced save (`mapScheduleZoomPersist`). No inventory change. Product-editor quantity arrows are counter-scaled so they stay readable (`updateProductEditorQtyControlScale`).
- Edge cases: Key codes for minus: 109, 189, 173. Plus: 107, 187, 61. Enter in `#mapFilter` does not zoom and does not submit the page.
- Related features: Minimap, tablet mode, search pan.
- Code evidence: `Map.aspx` 145–151; `mapZoomStepIn` / `mapZoomStepOut` 7880–7885; keydown 7910–7930; `getMapZoomMin` 6131–6136; `Gridster_Utilities` `DefaultMobileZoom` line 83; pinch `mapPinchZoomInit` 15751.
- Confidence: Confirmed
- Suggested KB title: Zoom the map

### Search the map

- Pages: `#mapFilter`, placeholder “Search Map...”
- What it does: Types a query, calls the map filter API, highlights matching locations, and pans to them. Enter cycles to the next match. Escape clears. A pill shows the current term. On narrow chrome a **>** button applies the filter.
- Why a user uses it: Find a product or a location name without scanning the canvas.
- How to access: The search box. `onkeyup` calls `filterMap`. Mobile **>** calls `mapFilterMobileSubmitClicked`.
- Steps: Type. Wait for the request. Matching tiles highlight and the view pans. Press Enter to jump to the next match. Escape or the × clears.
- Options/settings and defaults: API `GET https://code.cyberstockroom.com/api/map?mapFilter=` with header `X-CS-TOKEN`. Page size is not set on this call. Highlight classes include `map-highlight` / `map-highlight-location`. Quantity tiers while filtering use the user’s general threshold and max highlight (see next feature).
- Permissions / visibility conditions: Shown on the map control. Drag-and-drop onto the search box is cancelled (`mapFilterBlockDragDrop`) so a product drag does not fill the box.
- Validation, limits, failure behavior: API error still calls `mapFilterPaint(..., null, 2)` so the UI can fall back to local title matching (`mode` 2). Aborted requests are ignored. Empty result adds `map-filter-container--empty` and disables export (“No results to download”).
- Expected result and side effects: Display only. The same text is later passed as `MAP_FILTER` when opening Transfer from the map. 3D stacks open when a hit is a child inside a closed stack (`mapFilterSync3dStackForTarget`).
- Edge cases: Enter while the keyword is unchanged cycles matches (`mapPanToFilterCycleResult`). Clearing restores the previous scroll position (`mapFilterRestoreScrollPosition`).
- Related features: Quantity colors, export, transfer filter, minimap filter drawing.
- Code evidence: Input 10622; `mapFilterStartSearch` 13617–13670; `filterMap` 13673+; `mapFilterKeydown` 13458.
- Confidence: Confirmed for the client. Which fields the API matches is **outside this repo**. Local fallback matches location title text (`mapFilterTitleMatches`).
- Suggested KB title: Search the map

### Quantity colors (low, mid, max)

- Pages: Map, especially during search highlight
- What it does: Colors a location by comparing its quantity to two saved numbers. Tooltip prefix `MAX level` when the quantity is at or above the max highlight.
- Why a user uses it: Spot low stock and over-full locations while searching.
- How to access: Automatic when thresholds are non-zero. Values come from hidden fields filled from the coordinate string and from `UserSettings._generalThreshold`.
- Steps: None. Search highlights call `mapApplyQuantityThresholdToLocation`.
- Options/settings and defaults:
  - `hidden_GENERAL_THRESHOLD` = `UserSettings._generalThreshold` (per user; no numeric default in the map control).
  - `hidden_MAX_HIGHLIGHT` = `GetMaxHighlightFromRaw`. Token `-9` in the coordinate string. If missing or &lt; 0, JS treats it as **0**.
  - If both threshold and max are 0, filter coloring uses `map-qty-tier-mid` only when quantity &gt; 0.
  - If max &gt; 0 and qty ≥ max → class `map-qty-tier-max`.
  - Else if threshold &gt; 0 and qty ≤ threshold → `map-qty-tier-low`.
  - Else → `map-qty-tier-mid`.
  - qty ≤ 0 during filter → `map-highlight-location` and no tier.
- Permissions / visibility conditions: Any user who can see the map. The numbers are per user (threshold on the user settings object; max inside that user’s coordinate string).
- Validation, limits, failure behavior: Non-numeric values become 0.
- Expected result and side effects: CSS classes and the title attribute. No quantity change.
- Edge cases: `mapDashboard.ascx` hardcodes `generalThresholdValue:10` for its prototype button. That page is unreachable and is not the live map.
- Related features: Search, popup details.
- Code evidence: `mapResolveQuantityTier` 13555–13581; `Page_Load` hidden fields 150–151; `GetMaxHighlightFromRaw` in `Gridster_Utilities.vb` line 660.
- Confidence: Confirmed for the comparison. Where the user edits “general threshold” and “max highlight” in Settings was not in this scope.
- Suggested KB title: Low-stock and max-level colors on the map

### Check in from the map

- Pages: Designer hover **Check IN** → `Transfer.aspx` or `MOBILE_Transfer.aspx`
- What it does: Opens the transfer page in check-in mode with this location as the destination and source `-2`.
- Why a user uses it: Add stock into a place without leaving the map.
- How to access: Hover icon tooltip “Check IN products to this location...”. Also `Map.aspx` function `checkin(id)` which, on a narrow layout, calls `mapMobilePrimeInventoryFlow('CHECK_IN', id)` and otherwise goes to `/Start?checkin=true&id=`.
- Steps: Hover the location. Click the check-in icon. Complete the transfer page. Closing the Fancybox with `CookieRefreshRequired=1` posts `btn_hidden_transfer_products`, which calls `TransferFunctions.TransferProductsBackend`.
- Options/settings and defaults: URL `Transfer.aspx?isCheckin=true&MAP_FILTER={search}&SourceID=-2&DestinationID={id}` or `MOBILE_Transfer.aspx` when `mapCoordsViewportIsNarrow()`. Onboarding adds `&HideImportFile=true`. Cookies `COOKIE_TRANSFER_SOURCE` and `COOKIE_TRANSFER_DESTINATION`.
- Permissions / visibility conditions: Icon only on the non-read-only hover strip. Designer drag/click wiring. Narrow layout uses a full-page navigation and sets cookie `MOBILE_ReturnAfterProcess` to the current map URL (24h, `max-age=86400`).
- Validation, limits, failure behavior: `_dragToCheckin` returns false if destination is `-2`.
- Expected result and side effects: Inventory changes happen on the transfer page / `TransferProductsBackend`, not in the map click itself. Map scroll position is saved so it can be restored.
- Edge cases: Getting-started card can open a “2 min lesson about checking in your products” (`#mapCheckinLessonModal`). Escape closes the lesson.
- Related features: Check-out, drag transfer, kiosk links, default check-in location.
- Code evidence: `Map_Styling` check-in tooltip lines 141–171; `MapProcessEvent_JS` case `CHECKIN` 9227–9230; `_dragToCheckin` 9685–9709; `Map.aspx` `checkin` 47–51; `btn_hidden_transfer_products_Click` 299–302.
- Confidence: Confirmed
- Suggested KB title: Check products in from the map

### Check out from the map

- Pages: Designer hover, and the floating strip “Drag inventory here to check out”
- What it does: Opens transfer in checkout mode. Source is the location, destination is `-2`. Dragging a full location shows `#floating_checkout`; dropping there is the same checkout path.
- Why a user uses it: Remove stock from a place.
- How to access: Hover “Check OUT products from this location...”. Or drag the location (or a product chip) onto the checkout strip. `Map.aspx` `checkout(id)` → narrow `mapMobilePrimeInventoryFlow('CHECK_OUT', id)` or `/Start?checkout=true&id=`.
- Steps: Click the icon, or drag onto the strip, then finish the transfer page.
- Options/settings and defaults: URL `?isCheckout=true&MAP_FILTER=&SourceID={id}&DestinationID=-2`. Onboarding hides import. The strip is not shown when `isOnboarding()`.
- Permissions / visibility conditions: Hover icon only if not read-only. Drag checkout requires the source tile to be full and source ≠ `-2`.
- Validation, limits, failure behavior: Empty locations cannot start a drag (`js_event.preventDefault()` and `_TransferredTriggered = false`).
- Expected result and side effects: Same transfer backend as check-in. Activity is recorded by the transfer pipeline (not in the map click).
- Edge cases: Touch drag keeps the strip up until the finger ends (`mapMobileCheckoutTouchSessionActive`). Idle pointer activity hides it (`mapCheckoutIdleDismissInit`).
- Related features: Check-in, delete (delete also registers a check-out activity), single-unit transfer.
- Code evidence: `_dragToCheckout` 9656–9682; `DRAG_START` 9265–9326; floating strip 14962; `Map.aspx` `checkout` 54–60.
- Confidence: Confirmed
- Suggested KB title: Check products out from the map

### Drag stock from one location to another

- Pages: Designer map
- What it does: Drag a full location (or a product row from the peek) onto another location to open the transfer page with both ids. If the drag is a single unit, a small comment modal appears instead of the full transfer page.
- Why a user uses it: Move stock between places.
- How to access: Drag the location tile, or drag a product chip from the peek popup.
- Steps:
  1. Drag a full location or a peek row.
  2. Hover another location (it highlights; a 3D parent opens its stack).
  3. Drop.
  4. Either the transfer page opens, or the single-unit modal “Moving this item.” appears.
- Options/settings and defaults: Same-location drops are ignored. Destination or source `-2` is ignored for location-to-location (checkout/check-in use `-2` on purpose through the other functions). Narrow viewport uses `MOBILE_Transfer.aspx` and a full navigation; wide viewport uses a Fancybox (width 80%, height 95%).
- Permissions / visibility conditions: `EnableDragDrop` only for Designer. Ctrl held and not multi-selecting switches to copy-contents instead.
- Validation, limits, failure behavior: Drop on the same id breaks out of the handler. If the single-unit lookup fails, the code falls through to the full transfer page (`mapBeginSingleUnitTransfer` returns false).
- Expected result and side effects: Cookies `COOKIE_TRANSFER_SOURCE` and `COOKIE_TRANSFER_DESTINATION`. Query `SourceID` and `DestinationID`. On Fancybox close, `CookieRefreshRequired == 1` runs `TransferProductsBackend` and reloads safely (`CS_Security.RELOAD_SAFELY_W_HTTPS`). Onboarding calls `onboarding_dragdrop_triggered()`.
- Edge cases: 3D parent opens during drag-over so a child inside the stack can be the target. Minimap portal can complete a drop at the center of the viewport.
- Related features: Single-unit comment, check-in, check-out, Ctrl copy.
- Code evidence: `MapProcessEvent_JS` `DRAG_*` and `DROP` 9265–9398; `mapOpenInventoryTransferPage` 9417–9439; `EnableDragDrop` `Map_Styling.vb` line 493.
- Confidence: Confirmed
- Suggested KB title: Drag stock to another location

### Single-unit move comment

- Pages: `#mapUnitTransferModal` on the designer map
- What it does: When the dragged product quantity is exactly 1, or the whole location’s own quantity is exactly 1 and the lookup finds one product, the map asks “Moving this item.” / “Any comments about this transaction?” instead of opening the full transfer page. **Cancel** aborts. The commit button starts as **Skip Comment** and changes when the textarea has text (`mapUnitTransferSyncSaveButton`).
- Why a user uses it: Move one unit quickly and optionally leave a note.
- How to access: Automatic from a drop when quantity is 1. Onboarding skips this and always opens the transfer page (`isOnboarding() || !mapBeginSingleUnitTransfer`).
- Steps: Drop a single unit. Type a comment or leave it blank. Commit or Cancel. Escape cancels; Enter commits (`mapEnsureSingleUnitTransferModal` keydown).
- Options/settings and defaults: Location-level lookup uses page size **25** (`mapLookupSingleUnitLocationTransfer`).
- Permissions / visibility conditions: Only when not onboarding and the quantity is exactly 1. If the peek drag quantity is not 1, the function returns false and the full transfer page opens.
- Validation, limits, failure behavior: Lookup failure is not given a dedicated message in the portion read; the caller treats a false return as “open the transfer page.”
- Expected result and side effects: Commit posts `btn_hidden_transfer_products` → `TransferFunctions.TransferProductsBackend`. Comment text is included when the user does not skip (wired in `mapCommitSingleUnitTransfer`). Activity comment is whatever that backend stores.
- Edge cases: A location that shows `(children)` but has own quantity 0 is not “exactly 1” via `mapGetLocationQtyFromCountLabel` (that reads the `qty` attribute, which is own quantity).
- Related features: Drag transfer.
- Code evidence: Modal 10731–10741; `mapBeginSingleUnitTransfer` 9442–9458; `mapLookupSingleUnitLocationTransfer` 9461–9463.
- Confidence: Confirmed for when the modal opens. The exact comment header sent to the API is in `mapCommitSingleUnitTransfer` (around 9629) and the backend.
- Suggested KB title: Move a single item and add a comment

### Product peek (chips on a location)

- Pages: Designer and read-only maps (`peekContents` / `peekAtProducts`)
- What it does: Click a location to list products in a popup. Each row can show a quantity badge and optional custom-field chips. Rows are draggable. Up to 25 products are requested. While a search is active, the request includes `SearchTerms`. If a location is in the “highlight location” state, the filter is cleared so all products show.
- Why a user uses it: See what is inside a tile without opening the products page.
- How to access: Click the location (`onclick` `peekContents(...)`). 3D stack also gets a parent peek button (`map3dEnsureParentPeekButton`).
- Steps: Click the tile. Popup loads (“loading...”). Optionally drag a row. Click a custom-field chip to filter. Escape hides the peek (`hide_peek` keydown around 15083).
- Options/settings and defaults: `PageSize` **25**, `PageIndex` 1. URL `https://code.cyberstockroom.com/api/products?PageIndex=1&PageSize=25&LocationID=` plus `&SearchTerms=` when the map filter is non-empty. Expiration lookups are capped at **25** uids (`mapPeekLoadExpirations`). Description is shown unless popup-details hides it.
- Permissions / visibility conditions: Click wiring for Designer and Read_Only only. ProductEditor uses `ToggleQtyText` instead of peek. Minimalist does not get `peekContents`.
- Validation, limits, failure behavior: Failed expiration calls store an empty date for that product. Products beyond the first 25 are not requested.
- Expected result and side effects: Read-only unless the user then drags (transfer) or, on the product editor map, edits quantity. Designer peek quantity edit is a separate path (`mapPeekBeginQtyEdit`) that adjusts inventory.
- Edge cases: Hover tooltips are only for a fine pointer, and not in tablet mode or the mobile layout (comment at line 9922). On narrow tablet designer, the first tap selects the location for the footer instead of opening every hover icon.
- Related features: Popup details, drag transfer, view products.
- Code evidence: `ApplyStyling` onclick 362–363 and 453–455; `peekAtProducts` 3509–3527; `peekContents` 3199.
- Confidence: Confirmed
- Suggested KB title: See products inside a location

### Popup details (which fields appear)

- Pages: Map settings → “Popup details”
- What it does: Lets the user pick which product fields show as chips in the location popup, including an expiration switch when expiration data exists for the account.
- Why a user uses it: Show serial numbers, custom fields, or expiration in the peek without opening the product.
- How to access: Gear menu row “Popup details” (title “Choose which product fields show in the location popup.”). Modal title “Popup details”, hint “Select which product details to show in the popup.”, button **Done**.
- Steps: Open the row. Toggle fields. Click Done. Choices save with the coordinate string (`mapPopupDetailsSaveNow` → `_saveCoordinates`).
- Options/settings and defaults: The field list is JSON in `hidden_POPUP_DETAIL_CATALOG` (built in `LoadPopupDetailSettings`). **The catalog is dynamic per account; this audit does not list field names because they are not constants.** Token `-23` stores selected custom-field indexes. Token `-24` would hide description; the save function writes hide-description as `'0'` (description stays on in this save path). Token `-25` stores show-expiration. Comment in `Gridster_Utilities`: “Absent = description only” for popup fields, and “Absent = off” for expiration. Default expiring-soon window when the token is absent is **60** days (`DefaultExpiringSoonWindowDays`). Stored window token is `-18` (0 = disabled).
- Permissions / visibility conditions: Gear menu hidden when `DisableMobileView` is true. Expiration switch only if `hidden_POPUP_DETAIL_EXPIRATION_AVAILABLE` is `1`.
- Validation, limits, failure behavior: Bad JSON catalog becomes an empty list. Save is skipped if Gridster is not ready. Queued saves retry once.
- Expected result and side effects: Layout string updated. No inventory change. Peek chips follow the saved indexes (`mapPeekValueForField`).
- Edge cases: Buy/sell price visibility is separate tokens `-13` and `-14` (`hidden_SHOW_BUY_PRICE_FIELD` / `hidden_SHOW_SELL_PRICE_FIELD`, default from raw, absent means shown — `ApplyPricingVisibilityToCombined` default parameters `showBuyPrice`/`showSellPrice` = True). Personalized sort token `-15` is also in the coordinate string (`hidden_PERSONALIZED_SORT_ENABLED`). No gear-menu row for those three was found in the map settings table; they are persisted and consumed, but the toggle UI was not in this control’s settings popup.
- Related features: Product peek, search chips.
- Code evidence: Modal 10744–10753; `mapPopupDetailCatalog` 1892–1951; `Gridster_Utilities` lines 68–74 and 1122; `Page_Load` 158–167.
- Confidence: Confirmed for the modal and tokens. Exact catalog entries: dynamic. Buy/sell and personalized-sort toggles: not in this popup — Inferred they are edited elsewhere.
- Suggested KB title: Choose product fields in the location popup

### Edit quantity on the product map

- Pages: `MapProductEditorNaked.aspx` (type 2)
- What it does: Click a location to show a quantity box for the product in the query string. Type a new non-negative integer and press Enter. Up/Down arrows step the value on the standard (non-mobile) product map. Escape closes the box.
- Why a user uses it: Set how many of one product sit in each place.
- How to access: Open the naked product editor with `?ProductNumber=`. Helper text: “STEP 1 Select a product. STEP 2 Click a location. Type new quantity. Press Enter.”
- Steps: Click a location. Edit the number. Press Enter.
- Options/settings and defaults: Invalid input (not a positive integer per `csValidator.isValidPositiveInteger`, and the code then sets the box to `"0"`) is rejected and reselected. Arrow step only when `typeOfMap === 2` and `mapStandardViewAllowQtyArrowKeys()`.
- Permissions / visibility conditions: Read-only user on a ProductEditor map is redirected to `/_admin/_unauthorized`. Type 5 (`ProductEditor_ReadOnly`) exists in the enum (“Similar to Minimalist but with some different controls”) but no page in scope sets it.
- Validation, limits, failure behavior: API timeout **3000** ms. Error logs “There was a problem updating the quantity in this location...” and does not roll back the on-screen number (the label is updated in the same function after the request is sent, not only on success).
- Expected result and side effects: POST `https://code.cyberstockroom.com/api/inventory?action=adjust` with one transaction `product`, `source` = location, `destination` = location, `quantity` = new value. Header `X-CS-COMMENT`: `Quantity for '{uid}' was adjusted from {old} to {new}`. Success sets `CookieRefreshRequired=1`. The tile’s full/ghosted class and count label update immediately.
- Edge cases: If the location was the `AutoHighlight` / `LocationID_VIEW` target, the quantity box opens on load (`ToggleQtyText` with `IS_INITIALIZATION`).
- Related features: Peek quantity edit, transfer.
- Code evidence: `ToggleQtyText` 5803; `UpdateCount` 5932–5981; `updateQuantity` 5984–6018; `MapProductEditorNaked.aspx` helpers 163–174; `Map_Styling` ProductEditor onclick 354–359.
- Confidence: Confirmed
- Suggested KB title: Change a product’s quantity on the map

### View products for a location

- Pages: Designer `Map.aspx` and read-only map; also Location Editor **View Products**
- What it does: Stores `LocationID_VIEW` and redirects to the products page so that page opens on this location.
- Why a user uses it: Work with the full product grid for one place.
- How to access: Hover **View** (“View the products in this location...”). On the read-only strip, View is the primary icon. Location Editor button `onclick="ViewProducts();"`.
- Steps: Click View. Browser goes to `Products` (designer) or `Products_read_only` (read-only).
- Options/settings and defaults: None.
- Permissions / visibility conditions: View is on both hover strips. The redirect target depends on which page hosts the control.
- Validation, limits, failure behavior: `ProcessHover` swallows parse errors (“Need this try catch for Product Editor when pressing enter”).
- Expected result and side effects: `CS_TOOLS.UpdateDisplaySettings` with the new `LocationID_VIEW`. No quantity change.
- Edge cases: Read-only details is a different icon (`READ_ONLY` → `PeekLocationDetails.aspx`), not this redirect.
- Related features: Peek, location editor.
- Code evidence: `MapProcessEvent_JS` case `VIEW` 9237–9239; `ProcessHover` 273–290; `Map.aspx.vb` 20–22; `Map_read_only.aspx.vb` 18–20.
- Confidence: Confirmed
- Suggested KB title: Open the product list for a location

### Vertical stack (V)

- Pages: Designer hover “more” actions, mobile footer **Vertical**
- What it does: Stacks a parent’s direct children in a column instead of a row. Saves the parent id in the coordinate string (token `-8`) and reloads.
- Why a user uses it: Fit a tall rack without a wide row of tiles.
- How to access: Hover chevron “More actions” (›), then **V**. On a narrow tablet designer, select the tile and use footer **Vertical**.
- Steps: Click V. If the toggle is allowed, coordinates save and the page reloads.
- Options/settings and defaults: Off until the user turns it on. Eligibility (`LocationEligibleForVerticalStack`): at least **two** direct children, and a child may have its own children only when that child is a 3D parent.
- Permissions / visibility conditions: Control is hidden when the location is inside a 3D stack (`hideLayoutToggles` / footer filter). Disabled with a reason tooltip when not clickable:
  - “Stack children vertically” / “Turn off vertical stack”
  - “Needs at least two children”
  - “A child has its own locations. Turn that child to 3D first”
  - “Turn off 3D first” / “Turn off 3D on a child first”
  - “Vertical isn't available here.”
- Validation, limits, failure behavior: JS refuses a locked-on toggle and `console.error`s `[Map] VERTICAL_CHILDREN_TOGGLE: not allowed (locked on).` Save failure does not reload (same `_saveCoordinates` pattern as ABC sort).
- Expected result and side effects: Layout only. Children keep their ids and quantities.
- Edge cases: V cannot turn off while a child is 3D. 3D wins if the same node is both (`LocationVerticalToggleCanEnable` returns false when the node is already 3D).
- Related features: 3D stack, tile size, ABC sort (order inside the stack).
- Code evidence: `GetLocationHoverDiv` 99–117; `LocationEligibleForVerticalStack` 328–336; tooltips 414–430; `mapToggleVerticalChildrenParent` 685.
- Confidence: Confirmed
- Suggested KB title: Stack child locations vertically

### 3D stack

- Pages: Designer hover and mobile footer **3D**; the open stack is also used on read-only maps (children live in `.map-3d-stack`, hidden until opened)
- What it does: Hides direct children in an overlay stack on the parent. Click the parent to open or close the stack. Click outside to close. An **Add** button on the stack creates a child. Children inside a 3D stack do not show the normal hover-add **+**.
- Why a user uses it: Keep a parent compact when it has many children.
- How to access: Hover **3D** or footer **3D**. Click the parent tile to toggle the open stack (`map3dToggleStack`).
- Steps: Turn 3D on (saves token `-22` and reloads). Click the parent to open the stack. Click a child to peek or drag. Click outside or toggle again to close.
- Options/settings and defaults: Eligible when the node is not already inside a 3D parent, no direct child is itself 3D, and no child has children (`LocationEligibleForThreeDStack`). Empty parents may become 3D (comment: “Empty parents can still become 3D.”).
- Permissions / visibility conditions: Hidden for locations that are direct children of a 3D parent. Tooltips:
  - “Show children in a 3D stack” / “Turn off 3D stack”
  - “Already inside a 3D stack”
  - “A child is already 3D”
  - “A child has its own locations”
  - “Remove child locations before turning off 3D”
  - “3D isn't available here.”
- Validation, limits, failure behavior: Locked-on toggle logs `[Map] THREE_D_CHILDREN_TOGGLE: not allowed (locked on).` Stack height is capped (`map3dLimitStackHeight`).
- Expected result and side effects: Layout only. Dragging over a 3D parent opens the stack so the drop can hit a child. Search can open the stack when a child matches.
- Edge cases: A 3D parent with only child-quantity is drawn as full, but drag-from-parent still requires its own quantity &gt; 0.
- Related features: Vertical stack, create location, search, drag-drop.
- Code evidence: `LocationEligibleForThreeDStack` 305–311; tooltips 436–455; `map3dToggleStack` 1153; `mapToggleThreeDChildrenParent` 788; token `-22` in `Gridster_Utilities` lines 63–67.
- Confidence: Confirmed
- Suggested KB title: Show child locations in a 3D stack

### Multi-select and move several primary locations

- Pages: Designer map, desktop (touch UI disables it)
- What it does: Ctrl/Cmd-click primary tiles to select them. Ctrl-drag on empty map draws a marquee. Drag the selection to move the group by the same column/row delta. Escape cancels the drag or clears the selection. Invalid drops (collision or off-grid) are marked and not committed.
- Why a user uses it: Rearrange several buildings at once.
- How to access: Hold Ctrl (or Cmd on pointer-down). Click tiles or drag a rectangle on empty canvas. Then drag the group.
- Steps: Ctrl-click at least two primaries (or marquee). Drag. Release to save. Escape to abort.
- Options/settings and defaults: Move threshold **5** px (`MAP_MULTI_SELECT_MOVE_THRESHOLD_PX`) before a click becomes a drag. Only primary `li.gs-w` widgets qualify.
- Permissions / visibility conditions: `mapMultiSelectIsDesktopEnabled` is true only when touch controls are off. Right button is ignored. Reparent mode ignores the pointer handler. While a selection or Ctrl gesture is active, Ctrl+drop inventory clone is suppressed.
- Validation, limits, failure behavior: `mapMultiSelectIsInvalidDrop` blocks commit on collision or off-grid. Escape during group drag calls `mapMultiSelectGroupDragEnd(false)` (no save).
- Expected result and side effects: `_saveCoordinates` after a committed group move. Inventory unchanged.
- Edge cases: Ctrl-drag on empty space starts a marquee and also stops the page’s drag-to-scroll. The minimap draws selected widgets (`mapViewFinderDrawMultiSelectedOverlay`).
- Related features: Map lock, move one location, minimap.
- Code evidence: `mapMultiSelectOnPointerDown` 8925–8954; `mapMultiSelectOnKeyDown` 8883–8906; `mapMultiSelectIsDesktopEnabled` 8221–8222; threshold 8211.
- Confidence: Confirmed
- Suggested KB title: Select and move several locations

### Minimap (view finder)

- Pages: Map control `#mapViewFinderToggle`, title “Minimap (picture-in-picture)”
- What it does: A small picture of the canvas. Click to scroll the big map. Dragging a location or a product over the minimap scrolls the main map and can drop at the center of the view. The open/closed state is saved (tokens `-10` expanded, `-11` collapsed).
- Why a user uses it: Jump across a large map.
- How to access: The minimap toggle button. It can also auto-open when the map is large (`mapViewFinderMaybeAutoOpenFromMapSize`) if no saved state exists (`hidden_MAP_VIEW_FINDER_INITIAL` empty).
- Steps: Open the minimap. Click a spot to scroll there.
- Options/settings and defaults: Canvas element is 240×160. Saved state overrides auto-open. Embedded iframes can disable it (`mapViewFinderDisableIfEmbedded` / `mapViewFinderHostWantsMinimap`).
- Permissions / visibility conditions: Present with the map control. `Map.aspx` pan ignores events that start on `.map-view-finder`.
- Validation, limits, failure behavior: None specific beyond coordinate save failures.
- Expected result and side effects: Scroll position, and on drop, the same transfer or layout save as a normal drop. Open/closed flag is stored in the coordinate string.
- Edge cases: While a filter is active, cells are drawn with filter styles (`mapViewFinderGetCellFilterDrawStyle`). iOS inventory drag changes the minimap UI (`mapViewFinderBeginIosInventoryDragUi`).
- Related features: Zoom, search, drag-drop, multi-select.
- Code evidence: Toggle 14970–14973; `mapViewFinderInit` 7786; tokens `-10`/`-11` lines 42–45 of `Gridster_Utilities.vb` and JS 297–299.
- Confidence: Confirmed
- Suggested KB title: Use the map minimap

### Download quantity report

- Pages: `#mapExportButton` “Download Quantity Report”
- What it does: Downloads a CSV of quantities. Two modes: **Group by Location** (default, radio checked) or **Group by Product**.
- Why a user uses it: Export what the map is showing.
- How to access: The download button. It is `hidden` until `mapExportRefreshButton` decides there is something to export: either the filter returned no matches, or some visible location has quantity &gt; 0. An empty filter result disables the button (title “No results to download”).
- Steps: Optional: search. Click the download icon. Choose a grouping. Click **Download** or Cancel.
- Options/settings and defaults: Default radio `byLocation` / label “Group by Location”. Other option value `summed` / “Group by Product”. Hint: “You are about to download the product quantities across your map.” If a search is active, the modal shows “filtering by” plus the term. Columns:
  - By location: `Location ID,Location,Product Number,Description,Quantity` and empty locations are added (`MapExportEmptyLocationRows`).
  - By product: `Product Number,Description,Quantity` summed across locations.
  - File title: `CyberStockroom - Group by Location - {MMM d yyyy}` or `CyberStockroom - Group by Product - {date}`. Search term is inserted into the file name. Name sanitized and cut at **200** characters plus `.csv`.
- Permissions / visibility conditions: Button lives in the mobile-footer block (`Not DisableMobileView`). Export request on `Page_Init`: not logged in → HTTP **401** and `Response.End`. No separate read-only ban in `StreamMapQuantityExport`.
- Validation, limits, failure behavior: SQL only includes `Quantity > 0`, then by-location mode adds empty location rows. Filter match uses product number, description, and location path (`MapExportRowMatches`). Client error text is `mapExportSetError`.
- Expected result and side effects: File download. No inventory change. Sort is product number then location path (or location path then product number in the by-location file).
- Edge cases: Button can appear during an empty search (`mapFilterIsEmptyResult`) but is then disabled.
- Related features: Search.
- Code evidence: Button 10654–10655; modal 10820–10844; `mapExportRefreshButton` 14146–14155; `StreamMapQuantityExport` / `BuildMapQuantityCsv` `Map_CONTROL_2017.ascx.vb` 96–107 and 640–713.
- Confidence: Confirmed
- Suggested KB title: Download a quantity report from the map

### Tablet mode and touch map

- Pages: Map settings “Tablet mode”; floating tablet button
- What it does: Turns on touch map UI (larger targets, selection footer, edge scrolling). The same flag is the old “touch force” token `-5`.
- Why a user uses it: Use the map on a touch screen that the browser did not auto-detect, or turn that UI off.
- How to access: Settings row “Tablet mode”, or `#mapTabletModeButton`. Row is `hidden` until `mapRefreshTabletModeMenuUi` shows it. `mapTabletModeToggle` returns false when `csTabletMode.canUserToggle()` is false.
- Steps: Turn the switch. Loader, save, reload (`mapTabletModeToggle` continues past line 2577 with the same save-and-reload pattern as ABC sort).
- Options/settings and defaults: Token `-5` means on. Auto-detect: `mapDetectAutoTouchNeeded`. Narrow breakpoint used in comments and CSS is **900px**. `Map.aspx` sets `user-scalable=no` so the browser pinch does not fight the map pinch.
- Permissions / visibility conditions: Hidden entirely when `DisableMobileView` is true (naked designer iframe).
- Validation, limits, failure behavior: If the user is not allowed to toggle, the function returns false immediately.
- Expected result and side effects: Body classes `cs-tablet-mode` / `map-touch-ui`. Coordinate string updated. Multi-select turns off while touch is on. Hover “more” chevron only expands in tablet/touch (`mapHoverMoreToggle`).
- Edge cases: Narrow designer + touch uses a bottom selection bar (Edit, Clone, Vertical, 3D, Delete, Close) instead of the hover strip. First tap selects; actions are buttons. Tap outside clears the selection.
- Related features: Mobile differences, zoom, multi-select.
- Code evidence: `mapTabletModeToggle` 2573; token line 29–31; footer actions 5659–5684; `mapHoverMoreToggle` 5502–5514; `Map.aspx` viewport lines 7–9.
- Confidence: Confirmed
- Suggested KB title: Turn on tablet mode for the map

### Keyboard shortcuts

- Pages: Map control and `Map.aspx` / read-only zoom buttons
- What it does: See the table.
- Why a user uses it: Zoom, cancel, commit a quantity, or multi-select without the mouse.
- How to access: Keyboard, when the listed condition is true.

| Keys | Action | Condition |
| --- | --- | --- |
| `+` / `=` (key codes 107, 187, 61) | Zoom in ×1.1 | Not typing in a field; zoom not blocked by coach or modals |
| `-` / `_` (109, 189, 173) | Zoom out ×0.9 | Same |
| Ctrl + mouse wheel | Browser page zoom prevented | Map page |
| Enter in `#mapFilter` | Cycle to next search hit; do not submit the form | Filter focused |
| Escape in `#mapFilter` | Clear the filter | `mapFilterKeydown` |
| Escape | Close clone, sync, export, reparent, reparent error, unit-transfer, peek, check-in lesson, and clear multi-select | Whichever dialog is open; handlers are per feature |
| Ctrl (hold) | Next location drop copies inventory instead of transferring | Desktop, and not while multi-select is active |
| Ctrl or Cmd + click | Toggle a primary tile in the multi-selection | Touch controls off |
| Ctrl + drag on empty map | Marquee select | Touch controls off |
| Escape during multi-select | Abort drag or clear selection | Desktop multi-select |
| Enter | Save product-editor quantity | Quantity box focused, valid non-negative integer |
| Escape | Close quantity box without saving | Quantity box |
| Arrow up / down | Step product-editor quantity | Type 2 and `mapStandardViewAllowQtyArrowKeys()` |
| Enter in clone name/keyword fields | Confirm clone | Clone modal |
| Enter | Commit single-unit transfer | That modal |
| Escape | Cancel reparent | Reparent mode |

- Options/settings and defaults: Zoom limits in the Zoom feature.
- Permissions / visibility conditions: Multi-select shortcuts only when touch controls are off. Quantity arrows only on the product editor map.
- Validation, limits, failure behavior: Zoom keys call `preventDefault`. Typing targets (`INPUT`, `TEXTAREA`, `SELECT`, contenteditable) skip zoom so `+` and `-` can be typed.
- Expected result and side effects: Same as the matching buttons.
- Edge cases: `document.onkeydown` is assigned once for zoom, so it replaces any previous `document.onkeydown`. Other shortcuts use `addEventListener` and still run.
- Related features: Zoom, search, multi-select, quantity edit, reparent.
- Code evidence: `document.onkeydown` 7910–7930; filter 13458–13467; multi-select 8883–8936; quantity 5932–5979; clone Ctrl 9164–9171.
- Confidence: Confirmed
- Suggested KB title: Map keyboard shortcuts

### Pan, edge scroll, and scroll-to-origin

- Pages: `Map.aspx` (grab the background), in-control drag-scroll, `#mapScrollOriginButton`
- What it does: Drag empty canvas to scroll (`cursor: grab` / `grabbing`). A second jQuery drag-scroll is also installed (`$.dragScroll()`). While dragging a location or product near the screen edge, the map auto-scrolls. **Scroll to map origin (top-left)** jumps to the top-left. The button starts `hidden` and is shown by `mapInitScrollToOriginControl` when the user is scrolled away.
- Why a user uses it: Move around a map that is larger than the window.
- How to access: Drag the gray background. Use the corner origin button when it appears.
- Steps: Press on empty space and drag. Or click the origin button.
- Options/settings and defaults: `Map.aspx` pan ignores drags that start on a location, a draggable, the move handle, hover strip, add tab, checkout strip, peek, toolbox, minimap, or getting-started card.
- Permissions / visibility conditions: Background pan is on `Map.aspx` only (not on the read-only page’s markup — that page does not include the same script). The control’s `$.dragScroll` is inside the control, so it is on every host that renders the control.
- Validation, limits, failure behavior: Multi-select and Ctrl-held states cancel drag-scroll so selection still works.
- Expected result and side effects: Scroll only.
- Edge cases: One-finger touch pan on `Map.aspx` when the touch target is empty canvas. Two-finger pinch is zoom, not pan.
- Related features: Zoom, minimap, edge scroll during drag.
- Code evidence: `Map.aspx` 62–142; `$.dragScroll` 10288–10344; origin button 10724–10728; `mapInitScrollToOriginControl` 13360.
- Confidence: Confirmed
- Suggested KB title: Pan the map and return to the top-left

### Getting started and empty-map coaching

- Pages: Designer map
- What it does: If the account has no products (`hidden_PRODUCT_COUNT` from `SELECT COUNT(*) FROM {account}.Products`, designer only) the map can show a getting-started card and a check-in lesson. A map with no locations shows an empty prompt and pins the add toolbox. A map with exactly one location shows “Create Sub-Locations” and “Create New Location” tips.
- Why a user uses it: Learn the first check-in and where the add button is.
- How to access: Automatic from `mapShowGettingStartedCard`, `mapShowEmptyLocationPrompt`, `mapShowSingleLocationCoach`.
- Steps: Follow the card. Open the lesson. Escape closes the lesson (`mapCloseCheckinLesson`).
- Options/settings and defaults: Product count is only queried for Designer. Lesson title: “2 min lesson about checking in your products”.
- Permissions / visibility conditions: Product count hidden field is set only when type is Designer. `mapWelcomeForceStandardLayout` disables the narrow touch chrome.
- Validation, limits, failure behavior: Empty prompt makes the floating **+** a no-op (`HoverAddClick` returns immediately).
- Expected result and side effects: No inventory change until the user actually checks in.
- Edge cases: `MapDesignerNaked` has its own helpers (“Create Sub-Locations”, “Create New Location”) stored in `localStorage`, separate from these in-control tips.
- Related features: Create location, check-in.
- Code evidence: `Page_Load` product count 235–238; `mapShowEmptyLocationPrompt` 4603; `mapShowSingleLocationCoach` 4842; lesson title 15902; `MapDesignerNaked.aspx` 59–80 and 174–184.
- Confidence: Confirmed that the pieces exist. The exact “zero locations vs zero products” gate is split across `mapEmptyDesignerMap` / `mapCheckedInQuantity` (4544 and 4868); both were not line-read in full, so which card wins in every combination is **Inferred** from the function names.
- Suggested KB title: First-time hints on an empty map

### Highlight a new location

- Pages: Map after create or clone
- What it does: On the next load, scrolls to and highlights the new location id, then expires the cookie.
- Why a user uses it: See the place that was just added.
- How to access: Automatic. Cookie `COOKIE_MAP_HIGHLIGHT_NEW_LOCATION_ID` is written by the create/clone postback and cleared on read.
- Steps: Create or clone. After reload, the new tile is highlighted (`mapApplyPendingNewLocationHighlight`).
- Options/settings and defaults: None.
- Permissions / visibility conditions: Any user who can create.
- Validation, limits, failure behavior: Empty cookie → no highlight.
- Expected result and side effects: Visual only. Clone keyword results can also show a notice from `COOKIE_MAP_CLONE_RENAME_NOTICE` (`mapShowCloneRenameNotice`).
- Edge cases: Highlight id for a non-primary clone is the id returned by `ApplyClonedSubtreePostProcessing`, not always the newest primary.
- Related features: Create, clone.
- Code evidence: `Page_Load` 190–204; `btn_hidden_create_new_location_Click` 331–335; `mapApplyPendingNewLocationHighlight` 1496.
- Confidence: Confirmed
- Suggested KB title: Find a location you just added

### Location details popup (read-only)

- Pages: `Popups/PeekLocationDetails.aspx`
- What it does: Shows existing attachments as download buttons (file name truncated to 20 characters plus `...` when the stored name is longer than 30) and the location barcode with a print link. The attachment upload icon does not start an upload (`onclick="return false"` and the file input is `display:none` with no script that clicks it).
- Why a user uses it: See the barcode and files for a location without the full editor. Used from the read-only map.
- How to access: Read-only hover “View Location Details...” → `Popups/PeekLocationDetails.aspx?LocationID=`.
- Steps: Open the popup. Click a file name to download. Click the print image to open `PrintBarcode?SKU=&Name=` in a Fancybox.
- Options/settings and defaults: Barcode text box is `Enabled="false"`.
- Permissions / visibility conditions: Page comment says it is read-only. Unknown location → `~/Location Error.html`. No `READ_ONLY` role check in this code-behind (the master still requires a signed-in session via `Master.MO`).
- Validation, limits, failure behavior: Download strips invalid file-name characters. Missing location redirects.
- Expected result and side effects: Download only. No delete button on this page (the editor has delete).
- Edge cases: Designer users are not given this icon; they get Edit instead, which opens Location Editor (attachments can be uploaded there).
- Related features: Location Editor attachments, print barcode.
- Code evidence: `PeekLocationDetails.aspx` lines 6–46; `.aspx.vb` `Page_Init` 19–42 and `_showAttachments` 46–76; map event `READ_ONLY` 9241–9244.
- Confidence: Confirmed
- Suggested KB title: View a location’s barcode and attachments

### Attachments on the location editor

- Pages: `LocationEditor.aspx`
- What it does: Upload a file onto the location, download it, or delete it after confirm.
- Why a user uses it: Keep a photo, PDF, or spec with the place.
- How to access: Paperclip “Click to attach file...” in the editor.
- Steps: Click the paperclip. Choose a file. The change handler shows a loader and posts. To delete, confirm “Are you sure you want to delete this attachment?”
- Options/settings and defaults: None in the page. Storage is `attachmentRepository` / `attachmentProcessor` (same pattern as the peek page).
- Permissions / visibility conditions: Editor is blocked for read-only users.
- Validation, limits, failure behavior: Upload runs only `If FileUpload_attachment.HasFile`. Delete requires the confirm dialog to return true.
- Expected result and side effects: File stored for that location id. Page reloads on upload (`LocationEditor?LoadType=EXISTING&LocationID=`).
- Edge cases: Peek page can download but not upload.
- Related features: Peek location details.
- Code evidence: `LocationEditor.aspx` 292–317 and 331; `LocationEditor.aspx.vb` `_upload_attachment` 642+, `_deleteAttachment` 103, `_downloadAttachment` 79.
- Confidence: Confirmed
- Suggested KB title: Attach a file to a location

### Location barcode and print

- Pages: Location Editor and Peek Location Details
- What it does: Shows the location barcode. In the editor, typing a new value and pressing Enter saves it if it is not already used. Both pages link to `PrintBarcode` with `SKU` and `Name`.
- Why a user uses it: Scan a location or print a label for a shelf.
- How to access: Editor label “Barcode # (scan to change)”. Peek shows the barcode disabled. Print icon tooltip “Print Barcodes”.
- Steps (editor): Click the box (it selects all). Type. Press Enter. If the barcode is free, the page reloads. If not, the box turns `#AF5756`.
- Options/settings and defaults: Initial value is `_params.barcode` from `locationRepository.getByID`.
- Permissions / visibility conditions: Editor save is unavailable to read-only users. Peek barcode cannot be edited (`Enabled="false"`).
- Validation, limits, failure behavior: `_barcodeExists` true → no update, red background, white text. No alert string.
- Expected result and side effects: `locationModifier.set_barcode` and repository update. Print opens a Fancybox iframe (editor and peek).
- Edge cases: Enter does nothing if the text equals the saved barcode.
- Related features: Kiosk (separate), peek details.
- Code evidence: `LocationEditor.aspx.vb` 149–153 and 620–638; `LocationEditor.aspx` 396–405 and 426–438; `PeekLocationDetails.aspx.vb` 35–38.
- Confidence: Confirmed
- Suggested KB title: Set or print a location barcode

### Check-in and check-out kiosk from the editor

- Pages: `LocationEditor.aspx`
- What it does: Opens Quick Scan already aimed at this location.
- Why a user uses it: Leave a station in check-in or check-out mode for one place.
- How to access: Links “Checkin Kiosk” and “Checkout Kiosk” (`title` “Open Checkin Kiosk” / “Open Checkout Kiosk”). They open in a new tab.
- Steps: Open the editor. Click the kiosk link.
- Options/settings and defaults: URL `?mode=checkin|checkout&locationID={id}`. Page is `/Popups/QuickScan.aspx`, or `/MOBILE_QuickScan.aspx` when the viewport matches `(max-width: 900px)`. Location id comes from cookie `COOKIE_LOCATION_EDITOR_ID` or the query string.
- Permissions / visibility conditions: Editor blocked for read-only. If no location id, href stays `#`.
- Validation, limits, failure behavior: Non-numeric cookie/query is ignored.
- Expected result and side effects: Navigation only. Inventory changes happen in Quick Scan (not this page).
- Edge cases: Links are rewritten on load by `wireKioskLinks`.
- Related features: Map check-in/out, default check-in location.
- Code evidence: `LocationEditor.aspx` 409–416 and 605–619.
- Confidence: Confirmed
- Suggested KB title: Open a kiosk for one location

### Breadcrumb location selector

- Pages: `Controls/LocationSelector_CONTROL.ascx`, used by Location Editor and transfer UI
- What it does: Shows “ALL > …” breadcrumbs. Hovering opens a nested menu of child locations. Choosing one sets cookie `PageRelocationID` and clicks a hidden button so the host page reloads on that location.
- Why a user uses it: Jump to another place in the editor or pick the from/to location during a transfer.
- How to access: Hover the breadcrumb (`ShowLocationPicker` / `onmouseover`). On a transfer host, the first click uses `SetZone()`: if `event.clientX < 350`, zone is `FROM`, else `TO` (comment: “Assuming a Transfer Fancybox width of 700”).
- Steps: Hover. Click a location in the menu.
- Options/settings and defaults: Root label “ALL LOCATIONS”. `ParentFilterID` other than `-2` limits the tree and shows that parent’s readable path.
- Permissions / visibility conditions: The control itself does not check read-only; the host page does.
- Validation, limits, failure behavior: None in the control. `RelocatePage` shows a tarp loader before the postback.
- Expected result and side effects: Cookie `PageRelocationID`. Location Editor handles `LocationChanged` by redirecting to `LocationEditor.aspx?LoadType=EXISTING&LocationID=`.
- Edge cases: Dark theme swaps CSS classes when `DarkTheme` is true. Transfer uses two menus (`HidnNavMenus`), one per side.
- Related features: Location Editor, transfer.
- Code evidence: `LocationSelector_CONTROL.ascx` `RelocatePage` 18–33 and `SetZone` 40–49; `.ascx.vb` `SetLocationAndPopulate` 24–44 and `CreateBreadCrumb` 47–72; `LocationEditor.aspx.vb` `CS_LocationSelector1_LocationChanged` 611–612.
- Confidence: Confirmed
- Suggested KB title: Pick a location from the breadcrumb

### Choose a default check-in, check-out, or Lansweeper location

- Pages: `_locationSelectorToggle.aspx`
- What it does: A minimalist map (type 3). Clicking a location saves it and closes the Fancybox. **CLEAR Selection** stores `-2` instead.
- Why a user uses it: Set where check-in or check-out starts, or map a Lansweeper category onto a location.
- How to access: Settings popup. Query `type`:
  - `LANSWEEPER` — header `Select a Location to Match: '{name}'`. Also needs `id`, `category`.
  - `DEFAULTCHECKIN` — header “Select Default Check-In Location”.
  - `DEFAULTCHECKOUT` — header “Select Default Check-Out Location”.
- Steps: Click a location (minimalist map calls `sendLocationID`). Or click **CLEAR Selection**. Fancybox closes.
- Options/settings and defaults: Clear writes `-2`. Hover-add tabs are forced `opacity: 0` so this popup does not look like the designer. `ShowHoverChild` is an empty function so the minimalist hover does not throw.
- Permissions / visibility conditions: Read-only → `/_admin/_unauthorized`.
- Validation, limits, failure behavior: Unknown `type` leaves the header blank and the save `Select Case` does nothing, then still closes the Fancybox.
- Expected result and side effects:
  - Default check-in: `UPDATE CS_ADMIN.Users SET CheckInLocationDefault=@P3 WHERE AccountID=@P1 AND UserIndex=@P2`.
  - Default check-out: same with `CheckOutLocationDefault`.
  - Lansweeper: `locationTagger.replaceTag` or, on clear, `removeTagFromAllLocations`, then commit. Tag is `{siteID}_{category}`.
  - Cookie `cookie_refresh_settings=TRUE`.
- Edge cases: If the popup is inside the mobile flow, close calls `parent.mobileFlowTransferModalClose(false)` and sets `CookieRefreshRequired=1`.
- Related features: Map check-in (uses the user’s default elsewhere), location tags.
- Code evidence: `_locationSelectorToggle.aspx` header and clear button 74–79; `.aspx.vb` 33–128.
- Confidence: Confirmed
- Suggested KB title: Set the default check-in or check-out location

### Mobile create-location API

- Pages: `MobileCreateLocation.ashx` / `MobileCreateLocationHandler.vb` (not the map page)
- What it does: Creates one **root** location for the mobile main flow.
- Why a user uses it: Add a top-level place from the mobile UI.
- How to access: POST JSON `{ "name": "...", "locationType": 0-8, "parentId": -2 }`.
- Steps: Client posts the body.
- Options/settings and defaults: `parentId` must be `-2`. Type 0–8.
- Permissions / visibility conditions: 401 “Not signed in.” 403 “Read-only users cannot create locations.”
- Validation, limits, failure behavior:
  - Wrong method → 405 “Method not allowed.”
  - Bad JSON → “Invalid request.”
  - Bad type → “Invalid location type.”
  - Parent not `-2` → “Invalid parent.”
  - Blank name → “Please enter a name.”
  - Duplicate under the same parent → “That location name is already in use.”
  - SQL failure → “Could not create location.” or “Could not verify location name.”
- Expected result and side effects: Insert into `{account}.Locations`. Activity `LOCATION__CREATE`. Cookies `COOKIE_LOCATION_EDITOR_PAGE_RELOAD`, `COOKIE_MAP_PAGE_RELOAD`, `CookieRefreshRequired=2`. Response JSON `{ok:true}` or `{ok:false, message}`.
- Edge cases: Comment says not to call `Location.CreateNewLocation` here because `LocationPath` must match the editable-field path. This handler only allows root parents, unlike the map toolbox which allows any parent.
- Related features: Create from the map.
- Code evidence: `MobileCreateLocationHandler.vb` lines 11–133.
- Confidence: Confirmed
- Suggested KB title: Create a top-level location from mobile

### Mobile map differences (live map, not `Mobile/Map.aspx`)

- Pages: `Map.aspx` at a narrow viewport, and tablet mode
- What it does: The live phone/tablet experience is still `Map_CONTROL_2017` inside `Map.aspx`, not `Mobile/Map.aspx` (that page always redirects to unauthorized).
- Why a user uses it: Same map on a small screen.
- How to access: Open Map on a viewport at or below about 900px, or turn on tablet mode.
- Steps: Use the bottom bar instead of the hover strip when `mapTouchDesignerNarrowChromeEnabled` (tablet mode and map type 1, and not `mapWelcomeForceStandardLayout`).
- Options/settings and defaults:
  - Separate mobile zoom **0.74** unless the user has changed it (token `-7`).
  - Transfer, check-in, and check-out go to `MOBILE_Transfer.aspx` as a full page, and the return path is stored in `MOBILE_ReturnAfterProcess`.
  - `Map.aspx` adds bottom padding for the toolbar and disables browser pinch (`user-scalable=no`) while the map handles pinch.
  - Search has a **>** submit button.
  - Multi-select is off.
  - Hover tooltips are off.
- Permissions / visibility conditions: Same login rules as the desktop map. Read-only users are still redirected to `Map_read_only.aspx`, which has the same narrow CSS but a smaller script (no grab-pan script).
- Validation, limits, failure behavior: Same as desktop features.
- Expected result and side effects: Layout and navigation differences only; inventory rules match the desktop transfer backend.
- Edge cases: `MapDesignerNaked` sets `DisableMobileView="true"`, which removes the lock, settings, zoom toolbar, ABC sort, shared maps, export, and tablet button from that iframe.
- Related features: Tablet mode, zoom, transfer.
- Code evidence: `Mobile/Map.aspx.vb` lines 4–6; `mapIsMobileFooterSelectionMode` 5534–5544; `mapOpenInventoryTransferPage` 9421–9433; `Map.aspx` media query 23–38.
- Confidence: Confirmed
- Suggested KB title: Map on a phone or tablet

---

## 3. UNCERTAIN / POSSIBLY UNREACHABLE

| Item | Why |
| --- | --- |
| `Mobile/Map.aspx` and `Mobile/ProductEditorMap.aspx` | Code-behind redirects to `/_admin/_unauthorized` before the 2018 control can render. |
| `Controls/Map_CONTROL_MOBILE_2018.ascx` | Only hosted by those two pages. |
| `mapDashboardTest.aspx` and `Controls/mapDashboard.ascx` | Test page redirects to unauthorized. The “General Remap” button and `generalThresholdValue:10` never run for a normal user. |
| `Scripts/Controls/mapControlJS.js` | Only referenced by the dashboard control. Hover handlers still contain the text `" & LocationID & "`, so they would not call a real id even if the script ran. |
| `App_Code/.../CS_Map.vb` (`ReloadMap`, table layout) | No `CS_Map.` or `New CS_Map` references in the repo. |
| `GridsterFunctions.vb` | No callers. It uses column `GridsterCoordinates`, not `GridsterCoordinates2017`. |
| Map type 5 `ProductEditor_ReadOnly` | Enum and a `Case 5` that hides the floating **+** exist. No page in scope sets `data--type-of-map="5"`. |
| Compact map sizes 40 / 25 / 15 | Implemented in `_setGridsterSize` and skipped. `Page_Load` comment: “Compact Features Not yet released”, then `_setGridsterSize(0)`. |
| `CreateLocation_FASTER_DEBUG` | Defined and not called. Live create opens `NewLocation.aspx`. |
| Right-click context menu | No `contextmenu` handler. Not a user feature. |
| Free resize of a tile | Gridster options include no `resize` block. Size follows children. |
| Gear-menu toggles for buy price, sell price, and personalized sort | Tokens `-13`, `-14`, `-15` are saved and read. They are not rows in `#mapSettingsPopupHost`. Where the user turns them on was not in this scope. |
| Who may turn on “share my map” | Empty submenu says “Admins can share their maps in the Settings page.” The settings permission check was not opened in this audit. |
| Whether read-only users can drag the move handle | The handle is rendered for Read_Only. Drag is not given a separate “if read only, cancel” in `mapGetGridsterOptions`. Hover actions are restricted. |
| Location-clone API contents | `api/LocationClone` is not in this repo. The page treats the call as creating a new location tree, then optionally keyword-renames and preserves vertical/3D. Whether quantities are copied is not visible here. |
| `CS_Map.vb` drag zones | `MakeDragZone` exists on the unused table map. Do not document it as the live drag behavior. |
| Getting-started vs empty-map priority | Both code paths exist. The exact combination of zero products and zero locations was not executed. |
| `LocationEditor` `LoadType` other than `EXISTING` | Still creates a location immediately (`InitializeNewLocation`) using query `ParentID` / `LocationType`. The map’s Edit link always sends `EXISTING`. A hand-built URL could still hit the create path. |
| Personalized sort of products inside the peek | Token is stored (`GetPersonalizedSortEnabledFromRaw`). The peek request does not add a sort parameter in `peekAtProducts`. Effect on the map UI is uncertain. |

---

## 4. CONTROLS CHECKLIST

| Control | Where | Traced? |
| --- | --- | --- |
| Main menu “Map” | `UserPage.master` | Yes → `Map.aspx` or read-only redirect |
| Zoom out / zoom in | `Map.aspx`, `Map_read_only.aspx`, in-control toolbar | Yes |
| “Type +/- to zoom” | Same buttons’ title | Yes, key codes listed |
| Search box “Search Map...” | `#mapFilter` | Yes, API + Enter cycle + Escape |
| Clear filter × | `#clearButton` and filter pill | Yes |
| Mobile search **>** | `#mapFilterSubmitMobile` | Yes |
| Lock button | `#mapLockButton` | Yes, default locked |
| Download quantity report | `#mapExportButton` | Yes, hidden until quantity or empty search |
| Gear “Map settings” | `#mapSettingsButton` | Yes |
| ABC Sort switch | Settings row | Yes, default off, reloads |
| Popup details row | Settings row | Yes, dynamic field catalog |
| Tablet mode switch | Settings row, may be hidden | Yes, token `-5` |
| Shared Maps submenu | Settings row | Yes, list + sync modal |
| Scroll to origin | `#mapScrollOriginButton` | Yes, starts hidden |
| Floating **+** | `.floating-add-tab` | Yes, parent `-2`, hidden on types 2, 4, 5 |
| Type toolbox BUILDING…VEHICLE | `#toolbox_narrow` and Location Editor | Yes, types 0–8 |
| Hover Check IN | Designer strip | Yes → transfer `isCheckin=true` |
| Hover Check OUT | Designer strip | Yes → `isCheckout=true` and floating strip |
| Hover more chevron › | “More actions” | Yes, expands only in tablet/touch |
| Hover View | Both strips | Yes → Products or Products_read_only |
| Hover Clone | Designer more-menu | Yes → name modal + external clone API |
| Hover Edit | Designer more-menu | Yes → Location Editor |
| Hover V | When eligible | Yes, rules and tooltips |
| Hover 3D | When eligible | Yes, rules and tooltips |
| Hover Delete | Designer more-menu | Yes → confirmation, checkout activity, delete rows |
| View Location Details | Read-only more-menu | Yes → PeekLocationDetails |
| Reparent clasp | “Snap off location…” | Yes, confirm + postback. Hidden on naked welcome |
| 3D stack Add | “Add a location to this stack” | Yes |
| 3D parent peek | `map3dEnsureParentPeekButton` | Yes, opens peek |
| Move handle diamond | `gridster-move-handle` | Yes, Designer and Read_Only markup |
| Floating checkout strip | “Drag inventory here to check out” | Yes |
| Clone modal Clone / Cancel | Name, auto-rename switch | Yes |
| Reparent Move / Cancel | “Move location?” | Yes |
| Reparent error OK | “Could not move location” | Yes |
| Sync / Keep my layout | Shared map modal | Yes |
| Export Download / Cancel | Group by Location (default) or Product | Yes |
| Unit transfer Cancel / Skip Comment | “Moving this item.” | Yes |
| Delete YES | Confirmation dialog | Yes. Message has the typo “Are your sure” |
| Location Editor View Products | Button | Yes, uses `LocationID_VIEW` |
| Location Editor barcode Enter | Text box | Yes, duplicate turns the box red |
| Print Barcodes | Editor and peek | Yes → `PrintBarcode` |
| Checkin Kiosk / Checkout Kiosk | Editor | Yes → QuickScan `mode` + `locationID` |
| Attachment paperclip | Editor | Yes, upload. Peek icon does **not** upload |
| Attachment delete confirm | Editor | Yes |
| Breadcrumb ALL LOCATIONS | Location selector | Yes |
| CLEAR Selection | `_locationSelectorToggle.aspx` | Yes, writes `-2` |
| Minimap toggle | “Minimap (picture-in-picture)” | Yes |
| Getting-started / lesson | Designer | Yes, lesson Escape closes |
| Naked helpers X | `MapDesignerNaked`, `MapProductEditorNaked` | Yes, `localStorage` |
| Dashboard “General Remap” | `mapDashboard.ascx` | Traced as unreachable |
| `mapControlJS.js` hover icons | Old script | Not on the live map |
| Right-click menu | — | Not implemented |
| Resize handle | — | Not in Gridster options |

---

## 5. Permissions summary

| Condition (quoted) | Result |
| --- | --- |
| `UserSettings.isLoggedIn = False` in the 2017 control | `Response.Redirect("~/Login.aspx")` |
| `TypeOfUser = READ_ONLY` on `Map.aspx` | Redirect `Map_read_only` |
| `TypeOfUser <> READ_ONLY` on `Map_read_only.aspx` | Redirect `/Map` |
| `READ_ONLY` and map type Designer or ProductEditor | `/_admin/_unauthorized` |
| `READ_ONLY` on Location Editor, New Location, `_locationSelectorToggle` | `/_admin/_unauthorized` |
| Export while logged out | HTTP 401 |
| `MobileCreateLocationHandler` not signed in | 401 “Not signed in.” |
| `MobileCreateLocationHandler` read-only | 403 “Read-only users cannot create locations.” |
| `Mobile/Map.aspx` and `Mobile/ProductEditorMap.aspx` and `mapDashboardTest.aspx` | Always `/_admin/_unauthorized` |

No other role (admin vs standard) is checked inside the map control’s `Page_Load`. Shared-map publishing is described as an admin Settings action by the empty-state string only.

Inventory side effects that **are** in this repo:

- Delete: check-out **activity** plus `DELETE` of quantity rows and location rows (children included).
- Product-editor quantity: external adjust API, comment `Quantity for '{uid}' was adjusted from {old} to {new}`.
- Map check-in, check-out, and drag: hand off to `Transfer.aspx` / `MOBILE_Transfer.aspx` and `TransferFunctions.TransferProductsBackend`.
- Ctrl+drop copy: external `inventory?action=clone`.
- Create: activity `LOCATION__CREATE`.
- Layout actions (move, lock, ABC, zoom, V, 3D, shared sync, popup fields): `GridsterCoordinates2017` only.
