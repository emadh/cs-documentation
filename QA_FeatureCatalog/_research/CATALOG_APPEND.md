## MAP — Map and locations

Layout is per user in `GridsterCoordinates2017`. The live map is `Map_CONTROL_2017` on `Map.aspx`. There is no right-click menu and no free resize. `Mobile/Map.aspx`, `Mobile/ProductEditorMap.aspx`, `mapDashboardTest.aspx`, `Map_CONTROL_MOBILE_2018`, `CS_Map.vb`, and `GridsterFunctions.vb` are not reachable customer UI. Compact tile sizes are compiled and skipped (`_setGridsterSize(0)`, comment “Compact Features Not yet released”).

Read-only users are redirected from `Map.aspx` to `Map_read_only.aspx`. A non-read-only user who opens the read-only page is sent back to `/Map`.

### MAP-001 — Open the inventory map
- **Page:** `Map.aspx`. **What:** Loads every location and places primary locations from this user’s saved coordinates. Nested locations draw inside their parent. **Access:** MAP menu. **Who:** Signed-in, not read-only. **Default:** Map type 1. **Result:** No inventory change. **Failure:** A Gridster init error is logged and the stage still tries to reveal. **Code:** `Map.aspx.vb` `Page_Init`; `Map_CONTROL_2017.ascx.vb` `Page_Load`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-002 — Read-only map
- **Page:** `Map_read_only.aspx`. **What:** Same canvas. Hover offers View, optional V/3D, and “View Location Details…”. The floating + is hidden. Clicking a location still opens the product peek. View sets `LocationID_VIEW` and opens `Products_read_only`. **Uncertain:** A move handle is still rendered. Whether a read-only user can drag it is not separately blocked. **Code:** `Map_read_only.aspx.vb`; `Map_Styling.GetLocationHoverDiv`. **Confidence:** Confirmed for the hover. Inferred for drag. **KB Status:** Not audited. **KB Article URL:**

### MAP-003 — Location types
- **Options:** 0 Building, 1 Warehouse, 2 Store, 3 Floor, 4 Room, 5 Closet, 6 Shelf, 7 Bin, 8 Vehicle. Anything else is “Location”. **Default for a missing type:** 0. **Missing parent:** -2. **Change after create:** no control was found. **Mobile create** rejects a type outside 0–8 with “Invalid location type.” **Code:** `Location.GetLocationTypeName`; toolbox `Map_CONTROL_2017.ascx` ~15905. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-004 — Quantity labels on tiles
- **What:** Own quantity > 0 uses the full style. Zero own quantity with stock only in children is ghosted, except a 3D parent, which is drawn full and gets a “3D” badge. Count text: both own and children → `own (children)`; only own → the number; only children → `(children)`; both 0 → hidden. Secondary tiles show own quantity only. **Drag** requires the tile’s own quantity > 0, not merely child stock. **Code:** `Map_Styling.vb` `GetLocationCountLabel`; `mapLocationElIsFull`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-005 — Create a location
- **Access:** Floating + (parent -2), a + on a designer tile (child of that tile), or Add on a 3D stack. **Steps:** Pick a type, name it in `NewLocation.aspx` (default `New {type}`), commit. **Duplicate:** “That location name is already in use!” **Who:** Not read-only. Empty-map coaching swallows the floating + click. **Result:** Inserts name, type, parent, path. Activity `LOCATION__CREATE`. A new primary location is highlighted. **Code:** `HoverAddClick`; `NewLocation.aspx.vb`; `Location.CreateNewLocation`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-006 — Rename a location
- **Page:** Location Editor name field. “All Locations” (`-2`) is not editable. **Duplicate:** “That location name is already in use!” **Code:** `LocationEditor.aspx.vb` `LoadNameField`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-007 — Location editor
- **URL:** `LocationEditor.aspx?LoadType=EXISTING&LocationID=`. **What:** Name, breadcrumb, children, ADD NEW toolbox, attachments, barcode, print, view products, check-in and check-out kiosk links. A `LoadType` other than EXISTING creates “New {type}” immediately. **Who:** Read-only goes to unauthorized. Unknown id → `Location Error.html`. **Code:** `LocationEditor.aspx.vb` `Page_Init`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-008 — Move primary locations
- **What:** Drag the diamond header. Nested locations move with the parent or by reparent. **Default:** map is locked, so an overlapping drop snaps back. **Unlocked:** overlaps are removed and coordinates save. **Limits:** no resize handle; `max_rows` 100. **Result:** This user’s coordinates only. Inventory unchanged. **Code:** `mapGetGridsterOptions`; `mapHookGridsterMapLock`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-009 — Map lock
- **Default:** locked. Absent token = locked. Token `-19` locked, `-21` unlocked. Button title while locked: “unlock map to move locations freely”. Turning the lock on cancels an in-progress reparent. **Hidden** on `MapDesignerNaked` (`DisableMobileView`). **Code:** `mapMapLockToggle`; `Gridster_Utilities.vb`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-010 — Move a location under a different parent
- **What:** The clasp starts a mode. Next click picks a parent tile or empty canvas (parent `-2` makes it primary). Confirm: “Move location?” / “Move this location? Nested locations stay with it.” Buttons Cancel and Move. Escape cancels. **Failure:** “Could not move location”. **Result:** Parent id changes. Quantities stay on the same location ids. **Code:** `mapReparentClaspClick`; `btn_hidden_reparent_coordinates_Click`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-011 — Tile size follows children
- **What:** Width and height grow from children. There is no resize handle. Minimum primary width is 2 grid cells. **Code:** `Gridster_Utilities.OpenGridsterItem`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-012 — Delete a location
- **Dialog:** “Are your sure you want to DELETE this location?” and “All sub-locations will be deleted. Existing products will be checked out automatically.” YES. There is no No button; closing the popup cancels. The “Include Any Sub-Locations” checkbox is hidden and never read. Descendants are always deleted. **Result:** If quantity > 0, activity `INVENTORY__CHECK_OUT` with comment `Items cleared before deleting location '{name}' ({id})`, then quantity rows are deleted. Then location rows are deleted and activity `LOCATION__DELETE`. A primary location is removed from this user’s coordinates. **Code:** `ConfirmationDialog.aspx.vb` `btn_yes_delete_Click`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-013 — Clone a location’s structure
- **Modal:** “Name the New Location”, max 255. Suggested name is the source plus ` (Copy)`, then ` (Copy 2)` up to 999. **Auto-Rename Sub-Locations** is off by default. Tip: a whole word or hyphen-separated part is replaced in sub-location names (A32-1 → B45-1). The new root keeps the typed name. Same name as the source or a sibling blocks confirm. **API:** `POST https://code.cyberstockroom.com/api/LocationClone`. **Uncertain:** whether that API copies quantities. The page treats this as structure. Inventory copy is MAP-014. **Code:** `cloneLocation`; `LocationApplicationService.ApplyKeywordRenameViaIdMap`. **Confidence:** Confirmed for the page. Uncertain for API copy rules. **KB Status:** Not audited. **KB Article URL:**

### MAP-014 — Copy stock with Ctrl+drop
- **What:** Hold Ctrl, drag a full location, drop on a different location. Confirm: “Are you sure you want to copy the contents to this location? Any existing items will be cleared first.” **API:** `POST .../api/inventory?action=clone`. Cleared-first behavior is the confirm text plus that API. **Blocked** while multi-select is active, and skipped when a product chip is the drag (that drop is a transfer). **Code:** `MapProcessEvent_JS` case `DROP`; `_cloneContents`. **Confidence:** Confirmed for the prompt. **KB Status:** Not audited. **KB Article URL:**

### MAP-015 — ABC sort
- **Default:** off. Token `-20` means on. **What:** Direct children sort by name, then id. Fewer than 2 children skips the sort. **Failure:** “`[Map] ABC_SORT_TOGGLE: could not save coordinates.`” and the page does not reload. **Code:** `mapAbcSortToggle`; `CS_Map_Reusable.GetChildLocationsForRender`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-016 — Use a shared map layout
- **What:** Gear → Shared Maps. Empty text: “No shared maps. Admins can share their maps in the Settings page.” Choosing a person opens “Sync your Map Layout” with “If you sync to this layout, you will lose your existing layout. Are you sure you want to continue?” Buttons **Keep my layout** and **Sync**. **Copies** coordinates, both zooms, vertical parents, 3D parents, and the vertical-migrated flag. Not inventory. **Failures:** “Could not load shared maps.” “Sync is not available. Please refresh the page.” “Could not save the synced layout. Please try again.” **Related:** DSP-001. **Code:** `mapSyncLayoutModalConfirm`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-017 — Zoom
- **Buttons and keys** +/− multiply by 1.1 or 0.9. Pinch on touch. **Desktop** min 0.1, max 1. **Touch** min 0.15, max 2.2. **Initial** 1 on desktop, 0.74 on the mobile track. Tokens `-6` (standard) and `-7` (mobile). Narrow layout (about 900px) uses the mobile number. Ctrl+wheel does not zoom the browser page. Keys are ignored while typing, during the one-location coach, or while a modal is open. **Code:** `mapZoomStepIn`; `document.onkeydown`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-018 — Search the map
- **Placeholder:** “Search Map...”. Enter cycles matches. Escape clears. Narrow chrome uses a > button. **API:** `GET https://code.cyberstockroom.com/api/map?mapFilter=`. On API error the page falls back to matching location titles. Empty results disable export (“No results to download”). The same text is passed as `MAP_FILTER` when a transfer opens. **Uncertain:** which fields the API matches. **Code:** `mapFilterStartSearch`. **Confidence:** Confirmed for the client. **KB Status:** Not audited. **KB Article URL:**

### MAP-019 — Low and high quantity colors
- **What:** During search highlight, quantity at or above max highlight is `map-qty-tier-max` (tooltip prefix `MAX level`). At or below the quantity threshold is low. Otherwise mid. Quantity ≤ 0 is a plain location highlight. Both numbers 0 → mid only when quantity > 0. **Settings:** DSP-006 and DSP-007. **Code:** `mapResolveQuantityTier`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-020 — Check in from the map
- **What:** Opens transfer with source `-2` and this location as destination. URL `isCheckin=true`. Narrow layout uses `MOBILE_Transfer.aspx`. Onboarding adds `HideImportFile=true`. Empty locations and destination `-2` do not open the page. Phone layout can instead prime `MOBILE_Process` CHECK_IN. **Related:** XFR-001. **Code:** `_dragToCheckin`; `Map.aspx` `checkin`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-021 — Check out from the map
- **What:** Source is the location, destination `-2`. Dragging a full location shows “Drag inventory here to check out”. Empty locations cannot start the drag. The strip is hidden during onboarding. **Related:** XFR-002. **Code:** `_dragToCheckout`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-022 — Drag stock between locations
- **What:** Drop a full location or a peek row onto another location. Same id, source `-2`, and destination `-2` are ignored. A single unit opens MAP-023. Otherwise Transfer opens (Fancybox on a wide layout, full page on a narrow one). **Code:** `mapOpenInventoryTransferPage`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-023 — Move one unit and comment
- **What:** When the dragged product quantity is exactly 1, or the location’s own quantity is exactly 1 and the lookup finds one product: “Moving this item.” / “Any comments about this transaction?” Cancel aborts. The button starts as **Skip Comment**. Onboarding skips this and opens the full transfer page. **Edge:** The commit sets the source cookie quantity to 0 for that SKU, so the backend sets source stock to 0 even if the location had more than 1. That is not the Transfer page’s “move 1, keep the rest” rule. **Code:** `mapBeginSingleUnitTransfer`; `mapCommitSingleUnitTransfer`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-024 — See products inside a location
- **What:** Click a location. Up to 25 products load from `api/products`. While the map search is active, `SearchTerms` is included. Rows are draggable. Escape closes the peek. A custom-field chip can filter. Expiration lookups are capped at 25 uids. **Code:** `peekAtProducts`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-025 — Popup details
- **What:** Gear → “Popup details”. The field list is built per account. Do not invent field names. Token `-23` stores selected custom-field indexes. Description stays on in the save path that was read. Expiration appears only when the account has expiration data. **Default when the token is absent:** description only. **Related:** CFL-001 and CFL-002 are stored in the same coordinate string and are edited in Settings, not in this popup. **Code:** `mapPopupDetailCatalog`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-026 — Change quantity on the product map
- **Page:** Product editor map, type 2. Instruction: “Click a location. Type new quantity. Press Enter.” Up/Down step the value on a fine pointer. Escape closes without saving. Invalid input is replaced with 0 and reselected. **API:** `action=adjust` with source and destination equal to the location. Comment: `Quantity for '{uid}' was adjusted from {old} to {new}`. Timeout 3 seconds. The on-screen number updates when the request is sent, not only after success. Error log: “There was a problem updating the quantity in this location...”. **Who:** Read-only on a product-editor map goes to unauthorized. **Code:** `UpdateCount`; `updateQuantity`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-027 — Open the product list for a location
- **What:** Hover View stores `LocationID_VIEW` and opens Products or Products_read_only. Location Editor **View Products** does the same. **Code:** `ProcessHover`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-028 — Vertical stack
- **What:** Hover “More actions”, then V, or the mobile footer **Vertical**. Needs at least two direct children. A child that has its own children must already be 3D. Tooltips include “Needs at least two children”, “Turn off 3D first”, and “A child has its own locations. Turn that child to 3D first”. Hidden inside a 3D stack. Token `-8`. Layout only. **Code:** `LocationEligibleForVerticalStack`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-029 — 3D stack
- **What:** Hides children in an overlay. Click the parent to open or close. Click outside to close. Add on the stack creates a child. Token `-22`. Empty parents can become 3D. Not allowed when a child is already 3D or a child has children. Tooltips include “Already inside a 3D stack” and “Remove child locations before turning off 3D”. Search and drag can open the stack. **Code:** `LocationEligibleForThreeDStack`; `map3dToggleStack`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-030 — Move several locations
- **What:** Desktop only (off while touch controls are on). Ctrl or Cmd-click primary tiles, or Ctrl-drag a rectangle on empty map. Drag the group. Escape cancels. Invalid drops (collision or off-grid) are not saved. Move threshold 5 px. Ctrl+drop inventory copy is suppressed while a selection is active. **Code:** `mapMultiSelectOnPointerDown`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-031 — Minimap
- **Title:** “Minimap (picture-in-picture)”. Click scrolls the big map. A drag over the minimap can drop at the center of the view. Open/closed state is tokens `-10` / `-11`. It can auto-open on a large map when no state is saved. Canvas 240×160. **Code:** `mapViewFinderInit`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-032 — Download a quantity report
- **Button:** “Download Quantity Report”, hidden until some visible location has quantity > 0. Disabled during an empty search. **Options:** Group by Location (default) or Group by Product. Columns by location: Location ID, Location, Product Number, Description, Quantity, including empty locations. By product: Product Number, Description, Quantity summed. File name starts `CyberStockroom - Group by Location` or `Group by Product`, date `MMM d yyyy`, cut at 200 characters. SQL starts from `Quantity > 0`. **Who:** Signed in (401 otherwise). No separate read-only ban in the export method. **Code:** `BuildMapQuantityCsv`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-033 — Tablet mode
- **What:** Touch UI, selection footer, edge scroll. Token `-5`. The switch is hidden until the device allows a user toggle. Multi-select turns off. Narrow designer uses a bottom bar: Edit, Clone, Vertical, 3D, Delete, Close. First tap selects. **Code:** `mapTabletModeToggle`; footer actions ~5659. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-034 — Map keyboard shortcuts
- **Keys:** +/− zoom; Enter in the filter cycles hits; Escape in the filter clears it; Escape closes clone, sync, export, reparent, unit-transfer, peek, and the check-in lesson, and clears multi-select; Ctrl+drop copies inventory; Ctrl/Cmd-click and Ctrl-drag select; Enter saves a product-map quantity; arrows step that quantity on a fine pointer; Enter confirms clone and the single-unit modal. **Code:** `Map_CONTROL_2017.ascx` key handlers listed in the research file. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-035 — Pan and scroll to origin
- **What:** Drag empty canvas. The origin button (“Scroll to map origin (top-left)”) appears when the user is scrolled away. Background grab-pan script is on `Map.aspx`, not copied onto the read-only page. The control’s drag-scroll still loads with the control. **Code:** `Map.aspx` pan script; `mapInitScrollToOriginControl`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-036 — Empty-map coaching
- **What:** Designer maps can show a getting-started card, a check-in lesson titled “2 min lesson about checking in your products”, an empty-map prompt that pins the add toolbox, and one-location tips “Create Sub-Locations” and “Create New Location”. Product count is queried only for the designer map. **Uncertain:** which card wins for every mix of zero products and zero locations. **Code:** `mapShowGettingStartedCard`; `mapShowEmptyLocationPrompt`. **Confidence:** Confirmed that the pieces exist. **KB Status:** Not audited. **KB Article URL:**

### MAP-037 — Highlight a new location
- **What:** After create or clone, the next load scrolls to the new id and clears the cookie. A keyword rename can also show a notice. **Code:** `mapApplyPendingNewLocationHighlight`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-038 — View barcode and attachments (read-only)
- **Page:** `Popups/PeekLocationDetails.aspx`. **What:** Download attachments (names longer than 30 characters show 20 plus `...`). Barcode is disabled. Print opens `PrintBarcode`. Upload is not wired. **Who:** Signed in. No extra read-only check in this file. Unknown location → `Location Error.html`. **Code:** `PeekLocationDetails.aspx.vb`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-039 — Attach a file to a location
- **Page:** Location Editor. **What:** Paperclip upload. Delete confirm: “Are you sure you want to delete this attachment?” **Who:** Not read-only. **Code:** `LocationEditor.aspx.vb` `_upload_attachment`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-040 — Location barcode
- **What:** Editor label “Barcode # (scan to change)”. Enter saves if the value changed and `_barcodeExists` is false. A taken barcode turns the box `#AF5756` with no alert. Print tooltip “Print Barcodes”. Peek barcode cannot be edited. **Code:** `LocationEditor.aspx.vb` `hidden_barcode_btn_Click`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-041 — Location kiosk
- **What:** “Checkin Kiosk” and “Checkout Kiosk” open a new tab: `/Popups/QuickScan.aspx?mode=checkin|checkout&locationID=` or `MOBILE_QuickScan.aspx` at max-width 900px. **Related:** XFR-011. **Code:** `LocationEditor.aspx` `wireKioskLinks`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-042 — Location breadcrumb
- **What:** “ALL LOCATIONS” plus the path. Hover opens children. On a transfer popup, a click left of x=350 is FROM and otherwise TO. **Code:** `LocationSelector_CONTROL.ascx` `SetZone`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-043 — Create a top-level location from mobile
- **What:** POST JSON `name`, `locationType` 0–8, `parentId` must be `-2`. **Failures:** “Not signed in.” “Read-only users cannot create locations.” “Invalid location type.” “Invalid parent.” “Please enter a name.” “That location name is already in use.” “Could not create location.” **Result:** Activity `LOCATION__CREATE`. **Code:** `MobileCreateLocationHandler.vb`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### MAP-044 — Map on a phone
- **What:** Same 2017 control. About 900px or tablet mode: separate zoom (default 0.74), bottom selection bar, transfer goes to `MOBILE_Transfer.aspx`, search has a > button, multi-select is off, hover tooltips are off. `user-scalable=no` so the browser pinch does not fight the map. **Code:** `mapIsMobileFooterSelectionMode`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

---

## XFR — Inventory movement

There is no adjust mode on Transfer, Start, or the mobile process. Activity type 25 is written elsewhere (the product map and the product-list quantity editor). Batch, lot, expiration, and kitting are not fields on these movement screens.

If both `isCheckout=true` and `isCheckin=true` are present, check-out wins.

Read-only users are sent away from `Transfer.aspx` and from the mobile master (`/Map_read_only`).

### XFR-001 — Check in
- **Pages:** `Transfer.aspx?isCheckin=true`, `MOBILE_Transfer.aspx?isCheckin=true`. **What:** Source is forced to `-2`. The left list is the catalog (`api/search`, limit 250), shown with an infinity glyph. Save **adds** the chosen quantities at the destination. One `INVENTORY__CHECK_IN`. **Steps:** Search or scan. Click moves 1. The infinity badge asks for a quantity of at least 1 with no max. Drag onto the destination moves 1, not the whole catalog. Drag back clears the line. There is no “check in everything”. **Comment:** “Any comments about this transaction?” Empty button is “Skip Comment”; typed text switches it to “Save”. Enter, Escape, and a backdrop click confirm. **Failures:** “Please enter a quantity of at least 1.” “Please enter a quantity of 0 or greater.” Desktop miss: “Product Number '{scan}' doesn't exist!” A mobile check-in miss opens Add Products. **New Products** and **import file** show only while the destination selection is empty, unless `HideImportFile=true`. **Code:** `Transfer.aspx` `isTransferCheckinMode`; `TransferFunctions.TransferProductsBackend`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### XFR-002 — Check out
- **What:** Destination is forced to `-2`. Left list is stock at the source (page size 250). Quantity 0 is omitted unless that product is already selected. Save sets the source row to the **remaining** cookie quantity (overwrite, not a subtract). Activity `INVENTORY__CHECK_OUT` stores the **moved** quantities. **Click** moves 1 up to on-hand. **Drag** moves all remaining. **“Check-Out Everything”** pages the location API at 500 and is hidden while the map-filter badge is on. **Failures:** “Product '{term}' was not found at this location.” “Please enter a quantity up to {max}.” The add-quantity modal still says “transfer” and its button says “Transfer” even in check-out. The edit subtitle uses “check out”. **Import reductions:** “Only {available} items were available at this location. Quantity adjusted from {requested} to {available}”. **Edge:** Start-page check-out subtracts and floors at 0. This Transfer backend overwrites. **Code:** `Transfer.aspx` `TransferEverything`; `TransferFunctions.vb`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### XFR-003 — Transfer between two locations
- **What:** Both locations are real and must differ. Source is set to the remaining quantity. Destination becomes existing destination quantity plus the amount moved. One `INVENTORY__TRANSFER`. **“Transfer Everything”** matches check-out’s all-remaining behavior. Partial lines use `draggable-partial-count`. **Save** label “Transfer”. No create-product button. **Start selector** if the same place is picked twice: “The Source can't be the Destination!” **Code:** `Transfer.aspx` `TransferFunction`; `LocationSelector_*_LocationChanged`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### XFR-004 — Quantity adjust is not a Transfer mode
- **What:** No `isAdjust` flag. These handlers never register activity 25. The word “adjusted” on Transfer is only the import warning that a requested quantity was cut to on-hand. **Where adjust does exist:** MAP-026 and PRD-010. **Code:** `Transfer.aspx.vb` `Page_Init`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### XFR-005 — Import a file into a movement
- **What:** The import button is hidden once the destination selection is non-empty. Return `ApplyImportedTransfer=1` locks the page into review until save or cancel. **Match:** blank or `PN` = product number; `DESC` = product name; `CF_{index}` = that custom field. More than one match is skipped. Check-out and transfer require on-hand stock and reduce the quantity when the file asks for more. Check-in keeps the requested quantity and does not warn “not at location”. **Failures include:** “The file could not be read. Please upload it again.” “The file did not contain any products.” “No quantity was provided for this product.” “Quantity must be a whole number.” “Quantity must be greater than 0.” “This value matched more than one product in {field}.” “This product was not found at the source location.” “The requested quantity is not available at the source location.” Titles: “Success!”, “Import Failed”, “No items imported”. **Save** is still the host mode’s activity. If the selection was not edited, the comment gains `{{cs-file-import}}`. Cancel does not commit. **Code:** `BuildImportedTransferSelectionString`; `renderImportStatusBox`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### XFR-006 — Start page
- **Page:** `Start.aspx`. **Who:** Not read-only. Zero products hides the menu and shows “You have not added any products yet” / “Click to create”. **Actions:** Check In (`ProcessName` `ADD`, **adds** quantity), Check Out (**subtracts**, floor 0), Transfer (subtract then add), Create (`AddProducts?LastPage=Start`), Quick Scan. Query `checkin`, `checkout`, `transfer`, or `add` plus `id` opens that action. **Product selector** titles are under PED-020. **Comment** appears after the inventory write: “Success!” / “You can leave a brief comment if you like.” “Save Comment” then goes to Map. A missing location cookie exits without saving. **Code:** `Start.aspx.vb` `FinishAddHandler`, `FinishCheckoutHandler`, `btn_transfer_complete_Click`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### XFR-007 — Check in products just created
- **Pages:** `CheckInCreatedProducts.aspx`, done page. **What:** Catalog rows already exist. This page adds stock, or returns the lines to an open check-in. **Standalone:** pick one location (default `CheckInLocationDefault`, or query `loc`). Title “{n} Product(s) created.” Map prompt “Click a location to Check it in.” Quantities must be whole numbers ≥ 0 and at least one line ≥ 1. Comment modal, then additive `INVENTORY__CHECK_IN`. Skip closes without `SaveCheckIn`. Done page reloads the parent or goes to `/Products.aspx`. **Imported locations:** if every line has a real location, the map is hidden and each line checks into its own location. One bad location aborts the whole save: “A location in this import could not be found.” **Return to transfer:** no map. “Skip ››” drops the batch. “Continue” rewrites quantities and returns with `ApplyCreatedCheckIn=1`. Stock changes on the later Transfer save, not here. **Other errors:** “No products are waiting to be checked in.” “Each quantity must be a whole number, 0 or greater.” “Select a location on the map before checking in.” “Enter a quantity of at least 1 for one product.” **Who:** Not read-only. **Code:** `CreatedProductCheckIn.vb`; `CheckInCreatedProducts.aspx.vb`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### XFR-008 — Mobile check-in, check-out, and transfer
- **What:** Cookie `MOBILE_Process` is `CHECK_IN`, `CHECK_OUT`, `TRANSFER`, or `LOCATIONS` (view only). The live path, when the product-list cookie is empty, redirects to the location selector and then to `MOBILE_Transfer.aspx`. Save is `MOBILE_Process.aspx?CommitTransfer=1`, which uses the same Transfer backend. **Return:** a path containing `.aspx` and not `..`. The token `Map` (no `.aspx`) falls through to mobile home plus “Check-in completed successfully.”, “Check-out completed successfully.”, or “Transfer completed successfully.” Opening mobile home clears the process cookies. **Set default:** “The location(s) will be saved for next time”. A transfer does not overwrite a saved default, because the method does nothing when both location cookies are set. **Legacy path:** if `MOBILE_ListOfProducts` is already filled, the older add/subtract handlers run instead of TransferFunctions. **Code:** `MOBILE_Process.aspx.vb` `CompleteMobileTransferFlow`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### XFR-009 — Mobile location picker
- **What:** Lists the tree from parent `-2`. Source pre-selects the check-out default. Destination pre-selects the check-in default. Badge “default” opens the Settings location picker. `Contents` writes the source cookie and is view-only. **Code:** `MOBILE_LocationSelector.aspx.vb`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### XFR-010 — Legacy mobile product list and Quick Add
- **What:** `MOBILE_ProductSelector` writes product cookies and returns to the process page, which then uses the legacy handlers. Enter on a known row adds 1. An unknown scan with category `FALSE` opens Quick Add. **Quick Add** creates a product at location `-2` (not placed), activity `PRODUCT__CREATE` quantity 1, and does not check it in. Empty description is still saved. Buttons CREATE and CANCEL. The current process page does not navigate here by itself. Progress “back” and Quick Add’s return URL still do. **Code:** `MOBILE_ProductSelector.aspx` `Try2Scan`; `MOBILE_QuickAdd.aspx.vb`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### XFR-011 — Quick Scan
- **Pages:** `Popups/QuickScan.aspx`, `MOBILE_QuickScan.aspx` (iframe). **What:** Placeholder “ready to scan...”. Instruction “Scan a product or location”. A product scan adds the product or adds 1. The first location fills source, the next fills destination, and scanning one that is already source or destination swaps them. **Mode is derived:** source only = check out; destination only = check in; both = transfer; otherwise no save. Save posts `api/inventory?action=checkin|checkout|transfer`. **Failures:** “You have to select at least one location and one product!” “There was a problem saving the transaction!” Success: “{N} Transactions completed successfully.” or, on mobile, “Transaction saved”. **Kiosk:** `mode=checkin|checkout` and a positive `locationID`. Instructions become “Scan products to check in” or “Scan products to check out”. Location scans are ignored. `transfer` is not a kiosk mode. A bad query falls through to normal Quick Scan. **Uncertain:** the API’s stock math and which activity it writes. This page does not call `TransferFunctions`. No on-hand check and no integer check before POST. No create-on-scan. **Who:** Read-only goes to unauthorized. **Code:** `getTransactionType`; `apiPostTransaction`. **Confidence:** Confirmed for the page. Uncertain for the API. **KB Status:** Not audited. **KB Article URL:**

### XFR-012 — Mobile home
- **What:** Clears movement cookies on every load. Menu: Home, Map, Products, Activity, then Check In, Check Out, Transfer when the account has products, then QuickScan, Help, Settings, Logout. After a location is primed, the footer shows Check In, view products, and Check Out. There is no footer Transfer. Empty recent locations: “No recent locations.” **Code:** `mobile_main.aspx` `Process`; `ResetCookies`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

---

## PRD — Product list

Read-only users do not stay on `Products.aspx`. They use `Products_read_only.aspx`. Page size is 50. Location `-2` is ALL LOCATIONS.

### PRD-001 — Product list
- **What:** A specific location lists products with quantity > 0 there. If that list is empty and children have stock: “This location is empty but its sub-locations are not”. All Locations also appends zero-quantity products unless DSP-003 is off. Default sort is product number ascending. The keep-view cookie stores page, direction, and column. **Code:** `Products.aspx.vb` `InventoryGetAndDisplay`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PRD-002 — Empty list
- **All Locations:** “No products yet” / “Click to create” → Add Products. **A location:** “Location is empty...” / “Click to Check in” → `Start?checkin=true&id=`. **Search:** “No matches found!” **Code:** `MessageNoProductsShow`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PRD-003 — Columns
- **Columns:** Product Number (cannot be unchecked), Quantity, Description, Buy Price, Sell Price, each custom field, Cost Value (quantity times buy price, calculated, not stored). SAVE COLUMNS writes this user’s `ColumnOrder`. Headers can be dragged. **Default** when nothing valid is stored: Product Number, Quantity, Product Name, Buy Price, Sell Price, Cost Value, then every custom field. **EDIT COLUMNS** is Admin and opens the custom-field modal. Prices show the account currency. An empty description displays `UNTITLED (Product Number : {number})`. **Code:** `ColumnsDefaultDisplay`; `btn_ColumnAdjust`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PRD-004 — Sort
- **What:** First click is ascending. The same header flips direction and returns to page 0. Quantity sorts by the sum. Cost value sorts by sum times buy price. **Code:** `GridView1_Sorting`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PRD-005 — Pages and select all
- **What:** Numeric pager, first and last, top and bottom, hidden during search and when the count is 50 or less. Header checkbox: “The {n} Products on this page are selected” and “Select all {full count} products.” Select-all means every product in the account, not the current location or search. **Edge:** the SQL limit string is `LIMIT {page*50}, {page*50+50}`, which MySQL reads as offset plus a growing row count. **Code:** `CheckedProductsGelCompleteInventoryList`; `GridView1_PageIndexChanging`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PRD-006 — Search the product list
- **What:** Header Enter appends the term to `COOKIE_PRODUCT_SEARCH_FILTER` and opens Products. Terms are chips. AND across comma-separated terms. Each term is `LIKE` on product number, name, and every custom field, including hidden ones. Not buy price, sell price, or quantity. Search forces All Locations for the request and hides the pager. `?Search=` replaces the cookie with that one term. Leaving Products or Product Editor clears the cookie. **Code:** `SQLSearchClauseGet`; `UserPage.master.vb` query-search handler. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PRD-007 — Open a product
- **What:** A data cell opens `ProductEditor.aspx?ProductNumber=` (or the read-only editor). The checkbox column does not. **Code:** `callFancyBoxProductDetails`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PRD-008 — Web addresses in the grid
- **What:** A cell whose entire text is an http(s) URL, a protocol-relative URL, a `www.` host, or a bare domain becomes a pill. It opens in a new tab and does not open the editor. Extra words around a URL are left as text. **Uncertain** on the read-only page. **Code:** `ProductsGridUrlCells.js`. **Confidence:** Confirmed for `Products.aspx`. **KB Status:** Not audited. **KB Article URL:**

### PRD-009 — Photos in the list
- **What:** 40×40 images when DSP-002 is on. The toolbar camera button is commented out. Demo SKUs `CS_DEMO_` fall back to `Images/Pages/Products/{sku}.png`. Others use `cam_small.png`. **Code:** `GridviewImagesAdd`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PRD-010 — Change quantity in the list
- **What:** Only on the editable page, at a real location, on an in-stock cell, and not during search or the sub-location summary. Enter or OK posts `api/inventory?action=adjust` with source and destination equal to that location. Down arrow stops at 0. Failure: “There was a problem updating the quantity in this location...”. Timeout 3 seconds. Arrow keys step only for a fine pointer. **Not** the multi-edit path. **Code:** `Products.aspx` `submitQtyQuickAdjust`. **Confidence:** Confirmed for the request. **KB Status:** Not audited. **KB Article URL:**

### PRD-011 — Add, delete, multi-edit, recent, export, print, printable
- **Add:** tooltip “Add one or more products to your inventory” → `AddProducts.aspx?LastPage=Products`. Not on the read-only toolbar.
- **Delete:** disabled until a checkbox is on. Confirm: “Are you sure you want to delete the selected products from your inventory? This action cannot be undone!” Select-all deletes every product in the account. `Product.DeleteProducts` registers `PRODUCT__DELETE` and calls `ProductExpirations.Delete`. **Uncertain:** `productDeleter` is not in this repo, so image, attachment, and quantity removal inside that class is not visible. The older `_DeleteProduct` does delete product, quantity, and image rows, and the button does not call it. `Dialogs/ProductDeleteConfirmation.aspx` is unwired and only deletes quantity rows.
- **Multi-edit:** “For All Selected Items”, SET {field} TO {value}. Fields: Product Name; Quantity only when a real location is selected; Buy Price; Sell Price; each custom field. Empty: “Please enter a value”. Non-numeric price: “Value must be numeric!” A preset that is not allowed: “Value is not allowed for this field.” “Other (Specify)” allows any text. Quantity **overwrites** at the current location. Activity `PRODUCT__EDIT` records quantity `"1"` per product, not the number typed. Account type 1 calls `RecordsApp.AdjustRecord` instead of the SQL update.
- **Recently created:** up to 50 activity-code-0 rows. “No recent new products...”.
- **Export:** always enabled. Opens RPT-001. The current search is not passed.
- **Print barcodes:** hidden until a selection. Select-all asks “You are about to print barcodes for all {count} products. This may take a moment. Continue?”
- **Printable:** image title is misspelled “pritnable version”. Opens `/Products?printable=true`. The master hides the navbar and `.clickable`. It does not call `window.print`. A read-only user hitting `/Products` is redirected without keeping the flag.
- **Code:** `Products.aspx.vb` `btn_delete_Click`, `CheckedProductsMultiEdit`, `btn_export_report_Click`, `btn_print_barcodes_Click`. **Confidence:** Confirmed, with the deleter uncertainty above. **KB Status:** Not audited. **KB Article URL:**

---

## PED — Product editor, create, import, labels

### PED-001 — Edit name, price, and custom fields
- **What:** Product number is a label and cannot be renamed. Name, buy, sell, and custom fields follow account field order. Buy and sell show only for account type 0 and when CFL-002 says show. Presets are a dropdown: “(none)”, each preset, the current value if it is outside the list, and “Other (Specify)”. “(none)” stores empty. Currency rejects non-numeric and negative: “The Buy Price is not valid!” / “The Sell Price is not valid!” Name error text “The Product Name is not valid!” is not used unless the numeric check runs. Save writes the column and activity `PRODUCT__EDIT` (“Changed '{label}' to '{value}'”). Admin sees “Edit your fields”. **Code:** `ProductEditor.aspx.vb` `LoadFieldControls`; `EDITABLE_FIELD.ascx.vb` `SaveField`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PED-002 — Product photo
- **Tooltip:** “Click to update image...”. No size or type check in the upload handler. A Lansweeper image clears the click so upload is not offered. Read-only can see the image and cannot upload. **Code:** `_upload_image`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PED-003 — Product attachments
- **Tooltip:** “Click to attach file...”. Download chip. Delete confirm: “Are you sure you want to delete this attachment?” No extension allow-list and no size check. This is not Document Editor. Read-only can download and cannot upload or delete. **Code:** `_upload_attachment`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PED-004 — Lansweeper link on a product
- **What:** Shown when the asset lookup returns a URL. The asset-type custom field (tag `LS_CF_ASSET_TYPE_NAME`) can replace the photo. Failures hide the link. Both editor variants call it. **Code:** `_linkToLansweeper`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PED-005 — Expiration on the product
- **Who:** `SHOW_EXPIRATIONS`. Date `min=2018-01-01`, `max=2050-01-01`. Editor colors: green when more than 60 days remain, gold at 60 or fewer and still in the future, red when the day difference is 0 or less. Clearing sends DELETE. API errors are `console.log` only. Import rejects a non-`yyyy-MM-dd` date: “Row {n}: Expiration must be a date such as 2026-12-31.” Existing products in a create-import do not receive the file’s expiration. **Related:** EXP-001. **Code:** `ProductEditor.aspx` expiration script; `ProductExpirations.vb`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PED-006 — Product editor map
- **What:** Type 2 on the editable editor. Instruction “Click a location. Type new quantity. Press Enter.” Initial zoom cookie 0.9. Refresh reloads the editor. Read-only uses map type 5. Quantity behavior is MAP-026. Clone does not copy location quantities. **Code:** `ProductEditor.aspx` map host. **Confidence:** Confirmed for the host. **KB Status:** Not audited. **KB Article URL:**

### PED-007 — Clone a product
- **What:** “Clone Product”. Auto is checked. Placeholder “[Automatic Product Number]”. Uncheck Auto to type a number. “You must enter a product number.” “That product number already exists!” Copies visible fields and, when expirations are on, the date. Empty name becomes the new number. Missing prices become 0. **Result:** `INSERT IGNORE`, activity `PRODUCT__CREATE`, image copied when it can be, expiration posted. No quantities, no locations, no attachments. A “new” badge shows once. **Auto number:** `CSN-` plus nine digits. **Old popup** `Popups/CloneProduct.aspx` has no save and is not linked. **Code:** `ProductEditorClone.js`; `btn_clone_product_Click`; `GetNextAutoSKU`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PED-008 — Delete one product
- **What:** “Delete this product?” / “Deleting this product will also check it out of all locations on the map.” Same `DeleteProducts` path as the grid. The editor then redirects to that product number, which sends a missing product to `Product Error.html`. **Uncertain:** checkout of quantities is what the modal says; the deleter class is outside the repo. **Code:** `btn_delete2_Click`. **Confidence:** Confirmed for the click. **KB Status:** Not audited. **KB Article URL:**

### PED-009 — Read-only product editor
- **What:** Fields disabled. Print, attachment download, Lansweeper, and map type 5 remain. No clone, delete, image upload, or attachment upload. Non-read-only users are sent to `/ProductEditor`. **Code:** `ProductEditor_read_only.aspx.vb`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PED-010 — Create products by typing
- **Page:** `AddProducts.aspx`. **Fields:** product number with AUTO checked, description, then visible buy, sell, and custom fields. Empty description becomes the product number. Empty prices stay 0. A non-numeric or negative price stops the add. Blank manual number placeholder: “No Poduct Number!” Duplicate: “Product number already exists” or “Could not verify product number”. Account type 1 disables prices. **Save** calls `CreateNewAndStage` and, unless this is the single mobile-transfer add, opens check-in. Existing numbers are skipped, not updated. Staged quantity is 1. `ListProducts` also inserts a `Quantities` row at location `-2` with no quantity column. **Mobile single add** (`MobileTransferSingleAdd=1`) title “Add Product” and does not open check-in. **Code:** `btn_save_Click`; `GetNextAutoSKU`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PED-011 — Photo while creating
- **What:** Upload is stored as a temp image and copied onto the new product numbers on save. A fresh add session clears temp images. No type or size check. **Code:** `AddProducts.aspx.vb` `btn_upload_Click`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PED-012 — Import a CSV (shared rules)
- **What:** Upload, then “Drag from left to right to Match the fields.” **Limits and errors:** “This file is empty.” “This file is too large. Use a CSV smaller than 250 KB.” “This file is not a CSV...” “This file is not valid UTF-8...” “This file uses semicolons between columns...” “This file has more than 100 columns...” “Row {n} could not be read. Check the quotes and try again.” “This file has no products.” “You must select at least a Product Number to upload.” The first non-blank row is the header, never a product. Quoted commas are supported. **Who:** Not read-only. **Code:** `CSV_Class.ParseUpload`; `ImportFromFile.aspx.vb` `UploadFile`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PED-013 — Import to create products
- **Sample:** `Product Number, Product Name, Buy Price, Sell Price, Manufacturer, Supplier`. Those names are not required. **Slots:** Product Number, Description, Buy Price and Sell Price when shown, each custom field, optional Quantity (“You can include a quantity column to use during Check In”), Expiration when the flag is on, Location # or Location Name unless returning to a transfer. **Unmapped** number becomes `CSN-`. Unmapped description becomes the number. Unmapped prices stay 0. Unmapped quantity stays 1. Unmapped location stays -2. **Lengths:** 255 for number, description, and custom fields. **Prices:** “Row {n}: Buy Price must be a number such as 12.50.” **Quantity:** “Row {n}: Quantity must be a whole number such as 1 or 1.00.” **Duplicates in the file:** “Product number "{n}" is used on {count} rows.” **Existing products:** “Existing products keep their description, price, and custom fields. Their quantity is staged for check-in. New products are created from this file.” Expirations save only for new numbers. Presets are not enforced. Manufacturer and Supplier import only if dropped on custom fields. **Code:** `BuildCreateImport`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PED-014 — Import a list into check-in, check-out, or transfer
- **Check-in/out sample:** `Product Number, Quantity`. **With location:** `Product Number, Quantity, Location`. **Transfer sample:** `Product Number, Quantity, FROM, TO`. **Transfer identifier** can be Product Number, Description, or a custom field. This mode does not insert products. It stores start-page cookies and, for a transfer return, sends `ApplyImportedTransfer=1` (XFR-005). A non-transfer ragged row fails the file. A transfer ragged row is skipped. **Code:** `IsTransferMatchImport`; `CreateStartPageCookies`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PED-015 — Print barcode labels
- **Title:** “Print Barcode Labels”. **Stock, default first:** `30252 (1-1/8" × 3-1/2")`, `30336 (1" × 2-1/8")`, `30334 (2-1/4" × 1-1/4")`, `30330 (3/4" × 2")`. PREVIEW & PRINT builds Code 128. Missing name becomes “UNTITLED”. The page recommends a DYMO LabelWriter 450. `?Batch=1` uses the cookie from select-all. A comma in `SKU` clears the shared name. Unknown stock falls back to 30252. **Code:** `BarcodePngGenerator.GetLabelSpec`; `PrintBarcode.aspx`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PED-016 — Product selector
- **CHECKIN:** “Check In” / “Add Products to a Location” / “Please select a Check In Location.” Default `CheckInLocationDefault`. **CHECKOUT:** “Check Out” / “Remove Products from a Location”. Default check-out location. **TRANSFER:** “Transfer” / “Move Products between Location” / “Please select a Source Location for the Transfer.” Then “Please select a Destination Location for the Transfer.” Same place: “The Source can't be the Destination!” **Also:** “Search or scan...”, “+ New Products”, “Import From File”, “OR Import from File with Locations”. **Who:** Not read-only. **Uncertain:** the scan/filter script and the inventory write after `SignalNext` (that write is XFR-006). **Code:** `ProductSelector.aspx.vb` `Page_Init`. **Confidence:** Confirmed for titles and location rules. **KB Status:** Not audited. **KB Article URL:**

### PED-017 — Document editor is not product attachments
- **Page:** `DocumentEditor.aspx?ID=`. Type 0 “Purchase Order”, type 1 “Sales Order”, type 2 “Kit”. Header text is the literal `[PRINT] [SAVE] [NEXT]`. Footer is the literal `[Cancel] [Save]`. No click handlers. No product page links here. Type 3 BOM is defined on the class and has no page case. **Do not document this as editing a document.** **Code:** `DocumentEditor.aspx.vb` `PopulateDocument`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### PED-018 — Unwired product screens
- **`Popups/CloneProduct.aspx`:** locked fields, no save. Not the live clone (PED-007).
- **`Dialogs/ProductDeleteConfirmation.aspx`:** would delete quantity rows only, “DELETE FROM ALL LOCATIONS” or one location. Nothing sets `Session("ProductsToDelete")`. Not the live delete (PRD-011).
- **`SuccessProducts.aspx`:** “You can now Check In these products to any location.” No caller in this repo. Live success is the check-in page.
- **`Batch_Class.vb`:** no in-scope page calls it. Products clears cookie `STOCKROOM_BATCH` on load.
- **Code:** those files’ `Page_Init`. **Confidence:** Confirmed they are unwired. **KB Status:** Not audited. **KB Article URL:**

---

## ACT — Activity

No undo. Account and user activity codes (10–12, 15–24) are declared and are not in the history query. Records accounts (type 1) use Assignments, Assign, Deallocate, and Records for the group labels.

### ACT-001 — Activity history
- **What:** Newest first. Row: avatar, comment, “{You|name} {description}”, time, product count, location icons. Click opens details. Product and location names in the row open editors and do not open details. **Defaults:** category All Activity, user All, location All Locations, last **90** days through today (a comment says 365; the constant is 90), keyword empty, 15 rows. Empty: “No Activity...”. The current user’s first name is shown as “You”. **Edge:** with a user filter, timestamps are not shifted by the account time zone. “Show More...” adds 15 by reloading a longer list from the top, and the button can remain when everything is already shown. **Who:** every signed-in user, including read-only. **Code:** `DisplayHistory_FAST`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### ACT-002 — Filter by type
- **Buttons and codes:** All Activity 0,1,2,3,4,5,6,7,8,25. Inventory 1,3,4,25. Check In is 1,4,25 then an in-memory filter. Check Out is 3,4,25 then a filter. Transfer is 4. Adjust is 25. Products 0,2,5. Create 0, Edit 5, Delete 2. Location 6,7,8. Create 6, Edit 8, Delete 7. **Check In** keeps native check-ins, adjusts that did not decrease, and transfers whose destination is in the selected location tree and whose source is not. **Check Out** is the reverse for adjusts and transfers. With no location selected, transfers are removed from both. Those rows are drawn with check-in or check-out icons and a display-only `{{cs-transfer}}` or `{{cs-quantity-adjust}}` badge. **Code:** `InventoryActivityMatchesCategoryFilter`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### ACT-003 — Date, user, location, and keyword
- **Date presets:** All Time (1 Jan 2011 through tomorrow, and the picker max is today), Today, Yesterday, Last 7 Days, Last 30 Days, This Month. The end day is included by adding 24 hours. **Users:** All, Me, and people who have logged in and are not read-only. The query matches the stored first name, not the user index. Two people with the same first name cannot be separated. A renamed person no longer matches old rows. **Location:** `-2` is all. Any other id includes that location and descendants. Location create stores a location **type** in the destination id, so that column is not used as a location for create/edit/delete. **Keyword:** comment, product number, product name, and every custom field. No AND/OR syntax. `%` and `_` stay LIKE wildcards. Placeholder “search by keyword...”. **Code:** `GetFilters`; `CommentSearchExpression`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### ACT-004 — Activity row hover and CSV
- **Hover:** “{n} Product(s)” or “{n} Products ({qty} Items)”. Create and edit omit quantity. Check-in can say “to {location}”. Check-out “from {location}”. Transfer “from {a} to {b}”. Adjust “at {location}”. The hover lists at most 11 product lines. Deleted products show “[DELETED]”. **CSV:** tooltip “Download spreadsheet file (.csv)”. “Readable Format” is checked by default. Tooltip: “If you need to manipulate your data more easily you can uncheck this box for a more uniform file.” Columns: `Date, User, Activity, Source, Destination, Comments, Product Number, Description, Quantity, FROM, TO, Buy Price, Sell Price, Old Quantity, New Quantity, Qty. Diff., Cost Diff.` The last four headers are never filled by `WriteActivityCsv`. The download ignores the 15-row cap. Commas in several text fields become `_`. **Code:** `DownloadReport`; `WriteActivityCsv`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### ACT-005 — One activity
- **Page:** `ActivityDetails.aspx?ActivityID=`. Missing: “Activity not found” / “This activity may have been removed or is not available on this account.” Download of a missing id is HTTP 404. Product table includes Qty except for create and edit. Extra From/To columns appear when both header locations are `-2`. No comment edit and no undo. **Code:** `ActivityDetails.aspx.vb` `RenderDetails`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### ACT-006 — Header activity popup
- **What:** Up to 5 recent inventory rows (check-in, check-out, transfer, adjust), from the last two years. If none, a backup query uses the check-out code list. Button “View Activity History”. Rows do not open details. The other-user suffix is the numeric user index, not the name. **Code:** `CreateNotificationSummary`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### ACT-007 — What is stored
- **Standard phrases:** created new products, deleted products, edited products, checked in products, checked out products, transferred products, adjusted a product quantity, created a new location, deleted a location, renamed a location. **Records phrases:** created/deleted/edited records, assigned records, deallocated records, transferred records, adjusted a record. Location phrases stay the same. A content row is stored only when the product number is non-empty and the quantity is > 0. **Code:** `GetActivityDescription`; `RegisterActivity`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

---

## EXP — Expirations

Direct `/Expirations` without `SHOW_EXPIRATIONS` goes to `Settings#expirationsAnchor`. Read-only users go to `Expirations_read_only.aspx`. The window is DSP-005.

### EXP-001 — Expiration list
- **What:** Counts from the product repository (page size 10,000,000) and lists the first 100 API rows. Search placeholder “search...”. A row opens the product editor. **Colors:** expired date before today, red `#AF5756`, text `expired ({date})`. Within the window, yellow `#FFD966`, text `will expire in {n} days ({date})`. Otherwise grey `#EEEEEE`, `will expire on {date}`. Chips: “Expiring Soon” and “Expired”. Window 0 hides the yellow chip. The chip count uses the clock time; the list uses the date only, so a product expiring later today can disagree. Products past the first 100 are counted and not listed. **API match rules** for `searchTerms` are outside this repo. **Code:** `Expirations.aspx` `addListing`. **Confidence:** Confirmed for the page. **KB Status:** Not audited. **KB Article URL:**

### EXP-002 — Replace or clone an expiring product
- **Editable page only.** “manage” opens “Manage this product's expirations”. **Radios:** Replace and Delete (`replace_delete`), Replace only (`replace`), Clone and Delete (`clone_delete`), Clone and Check-out (`clone_checkout`), Clone only (`clone`). The checkboxes are a disabled legend, not inputs. Default radio is Replace and Delete. Comment sent: `Replacing expired product -  [Replace and Delete]` (two spaces, and the matching bracket text). Auto sends `auto_sku_identifier`. **Failures:** “You must select an expiration date.” “This date has already passed!” (the warning does not block save). “You must select a product number.” “That product number already exists!” Success goes to Activity History. **Uncertain:** what each action does to stock. The API is not in this repo. **Code:** `Expirations.aspx` `save`. **Confidence:** Confirmed for the wizard. **KB Status:** Not audited. **KB Article URL:**

---

## KIT — Kitting

`/Kitting` without `SHOW_KITTING` goes to `Settings#kittingAnchor`. The Settings checkbox is hidden (DSP-008). Nothing else in this repo sets the flag. Read-only users are sent to `Kitting_read_only`, and that file is not in the repo. There is no build and no break. There is no collapsed-menu Kitting link.

### KIT-001 — Kit list, create, delete, search
- **List:** “{n} Kits”. Each row is the name and “{n} Products included”. Click expands components. First 100 API rows. The count can be larger. **Create:** “+ NEW KIT” prompts “New Kit Name:” and posts `{"id":-1,"name":...,"content":[]}`. Cancel posts the name `null`. No duplicate check. **Delete:** “Delete Kit” with no confirm. **Search:** placeholder “search...”, each keyup, page size 100. Match rules are in the API. **Code:** `Kitting.aspx` `getKits`, `createNewKit`, `deleteKit`. **Confidence:** Confirmed for the requests. API persistence is uncertain. **KB Status:** Not audited. **KB Article URL:**

### KIT-002 — Kit components
- **What:** “{qty} x {description} ({uid})”. “+ Add New” searches products (page size 10). Quantity prompt: “Please enter the new quantity for Product : {uid} in Kit: {name}”. Remove confirm: “Are you sure you want to remove this item from the kit?” **Defects in the posted JSON:** editing a product that is already in the kit keeps the old quantity. Remove drops every other component that has the same quantity as the targeted line. Do not document this as a reliable editor until that JSON is fixed. There is no build-into-inventory action. **Code:** `Kitting.aspx` `changeQty`, `deleteItem`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### KIT-003 — Kit “manage” is not a kit action
- **What:** The manage button builds invalid JavaScript (the kit name is concatenated without quotes) and throws before the modal. The modal is a copy of the expiration replacement wizard, including `api/expirationReplacement`. Do not publish it as a kitting feature. **Code:** `Kitting.aspx` `addListing` ~165. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

---

## SRCH — Header search

### SRCH-001 — Header search
- **What:** Toolbar box, no placeholder. Autocomplete minimum length 0. `GET https://developers.cyberstockroom.com/api/search` with limit 10. Category `Products` opens the product editor. Category `Locations` opens the location editor. No search operators. **Empty API array,** a non-empty term, and Add Products visible: one row “Create New Product {term}” opens Add Products with `PreloadDescription`. Hidden for read-only. An HTTP error shows no create row. **Enter** appends the raw text to the product search cookie and opens Products (PRD-006). **Uncertain:** which fields the API matches, and categories other than Products and Locations. **Code:** `CS_SearchBox.ascx` `RegisterUserControlIndex`. **Confidence:** Confirmed for the client. **KB Status:** Not audited. **KB Article URL:**

---

## RPT — Reports

### RPT-001 — Download a product report
- **Page:** `ExportReport.aspx`, from the products download icon. **Title:** “Download Product Report”. **Defaults:** Include zero quantity off; include sub-locations off (hidden when the location is all); Product Number checked and disabled; Description, Quantity, breakdown by location, Buy Price, Cost Value, and Sell Price checked; every custom field checked; Product Image off. Cost value is quantity times buy price, rounded half away from zero to 2 decimals. Image adds “Image URL”. Filename is the location path or `ALL LOCATIONS`, plus the long date, max 200 characters. **Side effect:** every download rewrites `Locations.LocationPath` for the whole account before the query. The products search is not applied. **Who:** signed in. No read-only check on this page. **Code:** `ExportReport.aspx.vb` `DownloadFile`. **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### RPT-002 — AI insights report
- **Page:** `/ai-report.aspx?id=`. Header “Your Inventory Insights”, badge “AI-GENERATED”. Card types General, Location, Product, User. Any exception goes to Map. **No link** from the rest of this repo. Report text is not HTML-encoded. How reports are generated is in an SDK outside the files that were read. **Code:** `ai-report.aspx.vb`. **Confidence:** Confirmed that it is a signed-in page and unlinked. **KB Status:** Not audited. **KB Article URL:**

---

## Uncertain items added by the map, movement, product, and activity passes

- `api/LocationClone` copy rules (quantities or not).
- `api/inventory` stock math for Quick Scan, and for `action=adjust` beyond the request the pages send.
- `api/expirationReplacement` actions.
- `api/kit` insert rules and which fields kit search matches.
- `api/search` and `api/map` match fields.
- `productDeleter` child rows.
- Database default for `Quantities.Quantity` on the location `-2` insert during create.
- Whether a read-only user can drag the map move handle.
- Getting-started versus empty-map priority.
- `Kitting_read_only` is missing from the repo.
- Getting-started wizard steps exist and `Page_Init` redirects to Map before they run.
- Kit component quantity edit and remove drop the wrong lines (KIT-002). Document the defect, not a successful edit.
- Transfer opened outside the map fancybox may leave movement cookies uncommitted if no parent posts `btn_hidden_transfer_products`. The mobile shell commits itself.
- `MOBILE_LocationSelector` `SetLocation` omits `path=/` on the cookie.
- Map type 5 behavior beyond “the read-only editor hosts it”.
- Some transfer-import skip strings inside `AppendTransferImportRow` after the length check were not re-quoted.
- Product selector scan/filter functions were not fully read.
- AI report generation and valid ids.
- OAuth scope labels, Lansweeper stored field pairing, and the duplicate Lansweeper class binding remain from the settings pass.
