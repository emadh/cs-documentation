# Inventory movement — code audit

Scope is the pages and classes named in the audit request. Application source was not modified.

Modes that exist in this code: **check-in**, **check-out**, and **transfer** (location to location). Quick Scan chooses one of those three from which locations are filled. Quick Add creates a catalog product and does not move quantity. **Quantity adjust is not a mode** of Transfer, Start, or the mobile process. Batch, lot, expiration, and kitting are not read or written by these pages.

Location id **-2** is the sentinel for “all locations” / no real location. Check-in uses it as a virtual catalog source. Check-out uses it as a virtual destination (stock leaves the source and is not added anywhere). It is not a valid real source for transfer or check-out, and not a valid real destination for transfer or check-in.

Activity codes used when these pages save (from `Activity.vb`): `INVENTORY__CHECK_IN = 1`, `INVENTORY__CHECK_OUT = 3`, `INVENTORY__TRANSFER = 4`. `INVENTORY__ADJUST = 25` is not registered by the files in this audit.

Quantity SQL is `Product.UpdateProductLocationQuantity` (`Product.vb` 625–658):

- `OverwriteQuantity = False`: `INSERT ... ON DUPLICATE KEY UPDATE Quantity = Quantity + @new`.
- `OverwriteQuantity = True` (default): set `Quantity` to the passed value.
- `CHECKOUT = True`: `Quantity = GREATEST(Quantity - checkoutQty, 0)`.

Standard accounts (`AccountType = 0`) run that SQL. Records accounts (`AccountType = 1`) skip the quantity SQL and call `RecordsApp.AssignRecord` / `RemoveRecord` / `TransferRecord`, which still register the same check-in, check-out, or transfer activity with quantity 1 per record.

---

## Page inventory

| Page / class | Role |
| --- | --- |
| `Transfer.aspx` + `Transfer.aspx.vb` | Shared UI for check-in, check-out, and transfer. Mode from `isCheckout` / `isCheckin`. |
| `MOBILE_Transfer.aspx` + `.vb` | Mobile shell. Iframe loads `Transfer.aspx` with the same query string plus `MobileShell=1`. |
| `Start.aspx` + `.vb` | Older quick-start menu: create, check-in, transfer, check-out, Quick Scan. Query flags auto-open a flow. |
| `ProductSelector.aspx` | Popup used by Start (not mobile). Picks location(s) and products, then Start commits. |
| `CheckInCreatedProducts.aspx` + `.vb` + `CheckInCreatedProductsDone.aspx` | Check in products just created. Overlaps check-in when `ReturnToTransfer=1`. |
| `CreatedProductCheckIn.vb` | Stages that batch in cookie `CHECKIN_CREATED_BATCH`. Does not use Transfer cookies until the return URL. |
| `MOBILE_Process.aspx` + `.vb` | Mobile router: location steps, then either the Transfer shell or a legacy product-list commit. `?CommitTransfer=1` runs `TransferFunctions`. |
| `MOBILE_LocationSelector.aspx` + `.vb` | Pick source, destination, or a location to view. |
| `MOBILE_ProductSelector.aspx` + `.vb` | Legacy product list for mobile check-in/out/transfer. Not the default path anymore. |
| `MOBILE_QuickAdd.aspx` + `.vb` | Create one product from an unknown scan on the product selector. |
| `mobile_main.aspx` + `.vb` | Mobile home. Footer check-in/out for a primed location. Clears process cookies on load. |
| `MOBILE_MasterPage.master` | Inventory menu: Check In, Check Out, Transfer, QuickScan. |
| `UserPage.master` | Narrow-layout menu calls `mapMobilePrimeInventoryFlow`. Desktop tools menu opens Quick Scan. |
| `Popups/QuickScan.aspx` + `.vb` + `Scripts/Popups/QuickScan/QuickScan.js` | Barcode kiosk: scan locations and products, then POST check-in, check-out, or transfer. |
| `MOBILE_QuickScan.aspx` + `.vb` | Iframe of `Popups/QuickScan.aspx` plus the current query string. |
| `TransferFunctions.vb` | Commits Transfer cookies to quantities and one activity. |
| `Quantity.vb` | `ListProduct` inserts a `Quantities` row (product + location only). No movement UI. |
| `Cookies.vb` | Cookie name constants for transfer and mobile process. |
| `Controls/MOBILE_ProcessProgress.ascx` | Step labels on location selector, product selector, and process page. Not on the Transfer iframe. |
| `Features/Transfers.aspx` | Marketing page. Not an inventory workflow. |

---

## Cross-page sequences

1. **Desktop map check-in.** `MapProcessEvent_JS` case `CHECKIN` calls `_dragToCheckin`. Writes cookies source `-2` and destination = location. Opens `Transfer.aspx?isCheckin=true&MAP_FILTER=...&SourceID=-2&DestinationID=...` in a fancybox, or `MOBILE_Transfer.aspx` with the same flags when the map viewport is narrow. Narrow path also sets `MOBILE_ReturnAfterProcess` to the current map path (must contain `.aspx`). Onboarding appends `HideImportFile=true`. Empty locations are refused (`mapLocationElIsFull`). Destination `-2` returns without opening the page. (`Map_CONTROL_2017.ascx` `_dragToCheckin` ~9685–9709.)

2. **Desktop map check-out.** Same pattern with `_dragToCheckout`: refuses source `-2` and empty locations. Destination cookie `-2`. URL `isCheckout=true`. (~9656–9678.)

3. **Desktop map location-to-location drag.** Drop refuses same location, source `-2`, or destination `-2`, and empty sources. If a single-unit drag is recognized and onboarding is off, a small comment modal commits quantity 1 through the same cookies and `btn_hidden_transfer_products` (no Transfer page). Otherwise `mapOpenInventoryTransferPage` opens `Transfer.aspx` or `MOBILE_Transfer.aspx` with no `isCheckin`/`isCheckout` (plain transfer) plus `SourceID` and `DestinationID`. (~9364–9436, `mapCommitSingleUnitTransfer` ~9629–9653.)

4. **Desktop save of the Transfer popup.** Save sets `CookieRefreshRequired=1` and closes the parent fancybox. Map `afterClose` sees cookie value `1` and clicks `btn_hidden_transfer_products`, which calls `TransferFunctions.TransferProductsBackend` and reloads. (`Transfer.aspx` `finishSaveAndCloseAfterComment` ~3035–3079; `Map_CONTROL_2017.ascx` ~10385–10429 and `btn_hidden_transfer_products_Click` 299–302.)

5. **Mobile Transfer save.** If `isTransferMobileView` or `MobileShell=1`, save navigates the top window to `MOBILE_Process.aspx?CommitTransfer=1`, which calls the same `TransferProductsBackend`, clears transfer and mobile process cookies, then redirects. A return path is used only when it contains `.aspx` and does not contain `..`. The token `Map` (no `.aspx`) falls through to `MOBILE_main` plus a success banner. (`MOBILE_Process.aspx.vb` `CompleteMobileTransferFlow` 51–93.)

6. **Map location buttons on a phone layout.** `Map.aspx` `checkin(id)` / `checkout(id)` call `mapMobilePrimeInventoryFlow` when `mapIsMobileNarrowLayout()` is true. Otherwise they go to `/Start?checkin=true&id=` or `/Start?checkout=true&id=`. There is no matching `transfer=true` from these two functions. (`Map.aspx` 47–58.)

7. **Start forced open.** `?checkin=true`, `?checkout=true`, `?transfer=true` set `ProcessName` and cookie `forceLocationID` from `id`, then click the matching menu image. `?add=true` opens create. Fancybox close with `SELECTOR_PROCEED=TRUE` posts `btn_finish_add`, `btn_finish_checkout`, or `btn_transfer_complete`. (`Start.aspx` 216–335.)

8. **Start product selector.** `ProductSelector.aspx?Type=CheckIn|CheckOut|Transfer`. `forceLocationID` greater than `-2` pre-selects the location. Transfer asks for source, then destination, and refuses the same location. Check-in and check-out store `START_LocationID`. Proceed writes `SELECTOR_PROCEED=TRUE`. (`ProductSelector.aspx.vb` 114–189; `ProductSelector.aspx` ~768.)

9. **Create products, then check in, then return to check-in Transfer.** Check-in “New Products” or a zero-hit search goes to `AddProducts.aspx?ReturnToTransfer=1&isCheckin=true&SourceID&DestinationID&MAP_FILTER` (optional `PreloadDescription`). After create, `CheckInCreatedProducts.aspx` can Continue (rewrites the batch quantities, returns `Transfer.aspx` or `MOBILE_Transfer.aspx?isCheckin=true&ApplyCreatedCheckIn=1`) or Skip (expires the batch, returns without applying). Apply pre-loads those lines onto the destination side. (`Transfer.aspx` `buildCreateProductsUrl` 1624–1631; `CreatedProductCheckIn.TransferReturnUrl` 212–221; `Transfer.aspx` created-item apply ~2287–2318.)

10. **Import file into a movement.** “import file” goes to `ImportFromFile.aspx?CREATE_NEW=FALSE&Type=TRANSFER&ReturnPage=Transfer` plus source, destination, map filter, and the mode flags. Return with `ApplyImportedTransfer=1` builds the destination selection and locks the page in review mode.

11. **Mobile menu / home.** Menu and `mapMobilePrimeInventoryFlow` set `MOBILE_Process` and clear product cookies, then open `MOBILE_Process.aspx`. Home footer does the same for check-in or check-out and, when a location is primed and not `-2`, writes that id as destination or source. `mobile_main` `Page_Init` clears process cookies, so landing on home abandons an in-progress process. (`mobile_main.aspx.vb` `ResetCookies` 907–912.)

12. **Mobile process steps (current path, product cookie empty).**
    - `CHECK_IN`: if `MOBILE_DestinationID` empty → `MOBILE_LocationSelector.aspx?LocationType=Destination`. Else → `MOBILE_Transfer.aspx?isCheckin=true`.
    - `CHECK_OUT`: if `MOBILE_SourceID` empty → `LocationType=Source`. Else → `MOBILE_Transfer.aspx?isCheckout=true`.
    - `TRANSFER`: source, then destination, then `MOBILE_Transfer.aspx` (no mode flag).
    - `LOCATIONS`: location contents only. Not a quantity movement.
    (`ShouldRedirectToMobileTransfer` 95–106; `Page_Load` 228–317.)

13. **Legacy mobile product list.** If `MOBILE_ListOfProducts` is already non-empty, process does not open Transfer. It shows “N Products Selected” and opens the comment modal, then `CheckIN_Handler` / `CheckOUT_Handler` / `TRANSFER_Handler`. The product selector still writes those cookies and `SignalNext` returns to `MOBILE_Process.aspx`. Quick Add returns to the product selector. Progress “back” for check-in step 1 still points at `MOBILE_ProductSelector.aspx`.

14. **Quick Scan.** Start menu and UserPage tools open `Popups/QuickScan.aspx` in a fancybox. Mobile menu opens `MOBILE_QuickScan.aspx`, which iframes the popup with the same query string. Kiosk URLs are `?mode=checkin|checkout&locationID=<positive integer>`.

15. **Standalone created-product check-in** (not returning to Transfer). User picks one map location, or each imported line already has a location. Save adds quantity and registers one check-in, then `CheckInCreatedProductsDone.aspx` closes the popup and reloads the parent (or goes to `/Products.aspx` if there is no parent).

---

### Check in (catalog to a location)

- Pages
  - `Transfer.aspx?isCheckin=true` (desktop fancybox or direct).
  - `MOBILE_Transfer.aspx?isCheckin=true` (iframe adds `MobileShell=1`).
  - Commit: map `TransferFunctions.TransferProductsBackend`, or `MOBILE_Process.aspx?CommitTransfer=1`.
  - Also the Start check-in path and created-product check-in (separate entries).
- What it does (traced)
  - Source is forced to **-2**. The source column title is the text `CHECK-IN`. The source location picker is hidden. Destination must be a real location; if the cookie or query destination is `-2` or equal to the source, the page picks another location with `GetAnyOtherLocationID(-2)`.
  - The left list is the product catalog from `api/search?SearchType=1` (limit 250), not stock at a location. Each row shows an infinity glyph. Cookie source quantity is the sentinel `999999999` (`CHECKIN_INFINITE_QTY_SENTINEL`).
  - Save adds the chosen quantities onto the destination. Source `-2` is not updated. One `INVENTORY__CHECK_IN` activity is stored with destination = that location and quantities = amounts moved. Optional comment is `CookieDNDtransferComment`.
- Steps (complete sequence)
  1. Open from the map check-in control, mobile Check In, or `Transfer.aspx?isCheckin=true`.
  2. Destination comes from `COOKIE_TRANSFER_DESTINATION`, then query `SourceID`+`DestinationID` (both required, and they must differ; check-in allows source `-2`), then the check-in override above. Changing destination (desktop, non-phone browser) writes the cookie and reloads `Transfer.aspx?isCheckin=true`. Phone browsers hide both pickers (`Request.Browser.IsMobileDevice`).
  3. Search or scan. Enter with exactly one visible row selects it. Otherwise an exact scan match moves 1. A miss on desktop alerts. A miss on mobile check-in opens Add Products in a frame.
  4. Click a row to move 1. Click the infinity badge to type a quantity of at least 1 (no max). Drag onto the destination also moves 1 (not the whole sentinel). Drag a destination row back to the source clears that line (`TransferFunction(..., -1, -1)`). Edit the destination badge to set the line quantity; 0 hides the line.
  5. There is no “Check-In Everything” button. Check-in `PopulateSourceTable` does not render it, and `TransferEverything(true)` returns immediately in check-in mode. “Clear All (N items)” returns every selected line.
  6. SAVE / Check In opens “Any comments about this transaction?”. Empty comment button reads “Skip Comment”; typed text switches it to “Save”. Enter (without Shift) and Escape both confirm. Backdrop click confirms.
  7. Desktop: close fancybox → map posts `TransferProductsBackend`. Mobile shell: `MOBILE_Process.aspx?CommitTransfer=1`.
  8. Backend: if destination cookie quantity &gt; 0 and source is `-2` and destination is not `-2`, destination quantity becomes existing destination quantity plus the moved amount (overwrite to that sum). Lines with destination quantity 0 are skipped. Product-number, quantity, and comment cookies are expired.
- Options/defaults
  - Catalog page size 250. Search debounce 250 ms.
  - Map filter query `MAP_FILTER` shows a badge, dims non-matching rows, and can be toggled. It does not remove rows.
  - “import file” and “New Products” show only while the destination selection is empty, unless `HideImportFile=true`.
  - New-product rows get a star and are pinned to the top of source and destination.
  - Save label is “Check In” (green pulse). Import review uses the same label.
- Permissions and visibility
  - Read-only users: `Transfer.aspx.vb` redirects to `/_admin/_unauthorized` (`Page_Init` 75–77).
  - Mobile master redirects every read-only user to `/Map_read_only` before any mobile page runs.
  - Inventory menu links (Check In / Check Out / Transfer) are hidden when the account has zero products. QuickScan stays visible.
  - Same-location destination change is ignored (`LocationSelector_Destination_LocationChanged` exits when ids match).
- Validation/failures (quote message strings you find)
  - Add quantity: `"Please enter a quantity of at least 1."`
  - Edit quantity: `"Please enter a quantity of 0 or greater."` and, when a max exists, `"Please enter a quantity up to " + max + "."` (check-in edit has no max).
  - Desktop unknown scan/search: `"Product Number '" + scanText + "' doesn't exist!"`
  - Add modal subtitle: `"How many of '" + productName + "' would you like to check in?"` Title: `"Check-in quantity"`. Button: `"Check In"`.
  - Edit subtitle uses the words `"check in"`.
  - Import strings are in the import entry. Check-in does not emit “not at this location” or reduced-quantity warnings (`hideNotAtLocationUi`).
  - If cookies are missing, `TransferProductsBackend` returns empty and writes nothing.
- Side effects
  - `Quantities` row for destination is inserted or increased.
  - Activity `INVENTORY__CHECK_IN` with product numbers, moved quantities, destination id, product snapshot (`ProductDetailsIfDeleted`), and comment.
  - File-import comment tag `{{cs-file-import}}` is appended only when the import review selection was not edited (`buildTransferCommentWithImportTag`).
  - `CookieRefreshRequired=1` on desktop save.
  - Mobile success cookie text: `"Check-in completed successfully."` Theme `CHECK_IN`. Shown on mobile home when the return path is not a real `.aspx` path.
  - Records accounts: `RecordsApp.AssignRecord` instead of quantity SQL.
- Edge cases
  - If both `isCheckout=true` and `isCheckin=true` are present, **check-out wins** (`Page_Init` 81–89).
  - Clicking a check-in row always moves 1, even though the badge is infinity.
  - Add-modal input defaults to 1. Values above a finite max are silently clamped; check-in has no clamp.
  - Destination quantity is added to stock that already exists. A failed `GetProduct` for the destination is treated as existing quantity 0, then the destination is overwritten to the moved amount only (`TransferFunctions.vb` 73–80, 86–87).
  - “Transfer Everything” is not available, so the user cannot dump the whole catalog in one gesture.
  - Phone `IsMobileDevice` hides location pickers even inside the desktop Transfer page. The mobile shell is a separate iframe path.
  - `LoadHeaders` (707–736) still reads old cookies `TRANSFER_FROM` / `TRANSFER_TO`. Nothing in `Page_Init` calls it.
- Code evidence file+function+lines
  - `Transfer.aspx.vb` `Page_Init` 81–93; `LocationsGetFromCookies` 136–184; `PopulateCheckinCatalogSourceTable` 294–320; `BuildImportedTransferSelectionString` check-in branch 470–480; `TransferPageUrlWithMode` 763–766.
  - `Transfer.aspx` `isTransferCheckinMode` 23–26; `TransferFunction` 2970–2978; `drop` 279–281; `TransferEverything` 2781; `transferLoadCheckinCatalog` 917–938; `transferApplyCameraScanToSearch` 1153–1156; `showTransferQtyModal` 146–150.
  - `TransferFunctions.vb` `TransferProductsBackend` 85–87 and 119–121.
- Confidence: Confirmed
- Suggested KB title
  - Check in products to a location

### Check out (location to nowhere)

- Pages
  - `Transfer.aspx?isCheckout=true`
  - `MOBILE_Transfer.aspx?isCheckout=true`
  - Start `?checkout=true` (separate entry)
  - Quick Scan with a source and no destination (separate entry)
- What it does (traced)
  - Destination is forced to **-2**. The destination header is the text `CHECKOUT`. The destination picker is hidden.
  - Source cannot stay `-2`. If the cookie source is `-2`, both source and destination are replaced with some other location, then destination is forced back to `-2`.
  - Left list is stock at the source location (`api/products?locationID=&pageSize=250`). Quantity 0 is not listed unless that product is already on the destination side.
  - Save sets the source `Quantities` row to the **remaining** cookie quantity (absolute overwrite, not a subtract in this backend). Destination `-2` is not updated. Activity is `INVENTORY__CHECK_OUT` with source location and the **moved** quantities (`QuantityDest`, not the remaining source).
- Steps (complete sequence)
  1. Open from map check-out, mobile Check Out, or `?isCheckout=true`.
  2. Pick source on desktop. Changing source reloads `Transfer.aspx?isCheckout=true` unless the new source equals the destination (the forced `-2`, so a source of `-2` would be ignored by that guard; the earlier cookie guard already replaced `-2`).
  3. Search or scan. One visible row + Enter selects it. Exact scan match moves 1. A miss alerts `"Product '" + term + "' was not found at this location."` Mobile check-out does **not** open Add Products.
  4. Click moves 1, up to stock on hand. Quantity badge opens “Transfer quantity” (wording is still “transfer”; see edge cases) capped at remaining. Drag to the right moves **all remaining**. Drag back clears the line. Edit can set the moved quantity from 0 through the on-hand total.
  5. “Check-Out Everything” pages the location API at 500 products per call (`transferFetchAllLocationProducts`) and moves every on-hand quantity. The label becomes `"Check-Out Everything (N shown)"` after the visible rows load. Hidden while the map-filter badge is on.
  6. “Clear All (N items)” reverses the selection.
  7. Comment modal, then the same desktop or mobile commit as check-in.
- Options/defaults
  - Default source if cookies are missing: `LocationID_VIEW`, unless that is `-2`, in which case any other location. Default destination before the check-out override is another location, then overwritten to `-2`.
  - Import file is available (same button) and passes `isCheckout=true`.
  - “New Products” is check-in only.
  - Save label “Check Out” (red pulse).
- Permissions and visibility
  - Same read-only redirects as check-in.
  - Empty source location: the “Check-Out Everything” row is still rendered; product rows come back empty from the API. The unused empty message in markup is “Nothing to transfer in this location!” and `div_msg_empty` is set `Visible = False` in `PopulateSourceTable`.
- Validation/failures (quote message strings you find)
  - `"Please enter a quantity of at least 1."`
  - `"Please enter a quantity of 0 or greater."`
  - `"Please enter a quantity up to " + max + "."`
  - `"Product '" + scanText + "' was not found at this location."`
  - Add subtitle (shared with transfer, including check-out): `"How many of '" + productName + "' would you like to transfer? (Max: " + max + ")"` Button text on that add modal is `"Transfer"` even in check-out. Edit subtitle uses `"check out"`.
  - Import skip lines include `": This product was not found at the source location."`, `": None of this product is available at the source location."`, `": The requested quantity is not available at the source location."`
  - Reduced-quantity tooltip: `"Only " + availableQty + " items were available at this location. Quantity adjusted from " + requestedQty + " to " + availableQty`
- Side effects
  - Source quantity overwritten to the leftover amount in `CookieProductQuantityString`.
  - Activity `INVENTORY__CHECK_OUT`, source id, moved quantities, comment.
  - Mobile banner: `"Check-out completed successfully."`
  - Records accounts: `RecordsApp.RemoveRecord`.
  - Checkout SQL floor at 0 is **not** what this backend uses. This path overwrites. The subtract-and-floor SQL is used by Start and by the legacy mobile handlers.
- Edge cases
  - UI and cookies treat source quantity as “still here” and destination quantity as “leaving”. Backend writes source = remaining. If the cookie remaining is stale, stock is set to that stale number.
  - Moved quantity can be less than on-hand (partial check-out).
  - “Check-Out Everything” only includes products returned by the paged products API, then moves whatever source cookie quantity is &gt; 0.
  - Map will not start check-out from location `-2` or from an empty location. The Transfer page itself will still open if linked directly.
  - Check-out wins if both query flags are true.
- Code evidence file+function+lines
  - `Transfer.aspx.vb` 84–86, 137–140, 168–174, 239–240, 445–469.
  - `Transfer.aspx` `refreshTransferEverythingLabel` 1086–1095; `drop` 283–297; `TransferEverything` 2784–2797.
  - `TransferFunctions.vb` 88–93 and 116–118.
  - `Map_CONTROL_2017.ascx` `_dragToCheckout` 9656–9660.
- Confidence: Confirmed
- Suggested KB title
  - Check out products from a location

### Transfer between two locations

- Pages
  - `Transfer.aspx` with neither `isCheckout` nor `isCheckin`.
  - `MOBILE_Transfer.aspx` the same way.
  - Map drag between two real locations.
  - Map single-unit comment modal (quantity 1, same backend, no Transfer page).
  - Start `?transfer=true` (separate entry).
- What it does (traced)
  - Both locations are real. Source `-2` is rejected and replaced. Query overrides apply only when both ids parse, they differ, and source is not `-2`.
  - Stock moves from source to destination: source is set to the remaining quantity; destination becomes existing destination quantity plus the amount moved.
  - One `INVENTORY__TRANSFER` activity stores source, destination, and moved quantities.
- Steps (complete sequence)
  1. Open plain `Transfer.aspx`, mobile Transfer, or drop one full map location onto another.
  2. Set source and destination with the two location selectors (desktop). Reload keeps the mode-less URL. Selectors refuse a change that would make the two ids equal.
  3. Same search, scan, click-1, type-a-quantity, drag-all-remaining, drag-back, and edit behaviors as check-out.
  4. “Transfer Everything” / “Clear All” same as check-out, with the label `"Transfer Everything"`.
  5. Comment, then desktop fancybox commit or mobile `CommitTransfer=1`.
  6. Alternate: map single-unit modal writes cookies `CookieProductNumberString` = uid, source quantity `0`, destination quantity `1`, comment, and both location cookies, then clicks `btn_hidden_transfer_products` immediately.
- Options/defaults
  - Same 250-row source API and 500-row “everything” paging.
  - Import file URL sets `isCheckout=false&isCheckin=false`.
  - No create-product button (that is check-in only).
  - Save label “Transfer” (blue pulse).
  - Map filter and `HideImportFile=true` during onboarding.
- Permissions and visibility
  - Read-only blocked on Transfer and on the mobile master.
  - Map drop does nothing if source is empty, locations match, or either id is `-2`.
- Validation/failures (quote message strings you find)
  - Same quantity and “not found at this location” strings as check-out.
  - Add modal title `"Transfer quantity"`, button `"Transfer"`.
  - Edit title `"Update quantity"`, button `"Update"`, action word `"transfer"`.
  - Map clone (not this mode) uses a different confirm: `"Are you sure you want to copy the contents to this location? Any existing items will be cleared first."` That calls `api/inventory?action=clone`, not Transfer.aspx.
  - Start transfer, if the user picks the same place twice: `"The Source can't be the Destination! <br/>Please select a <b>Destination. </b>"` (`ProductSelector.aspx.vb` 160).
- Side effects
  - Source quantity overwritten to remaining. Destination overwritten to existing + moved.
  - Activity `INVENTORY__TRANSFER`.
  - Mobile banner: `"Transfer completed successfully."`
  - Records accounts: `RecordsApp.TransferRecord`.
  - Single-unit map transfer uses the same function, so quantity 1 is what the cookies say, added on top of destination stock, and source is set to 0 for that product only.
- Edge cases
  - Partial quantities are first-class: click adds 1 until remaining is 0; the row turns `draggable-empty` when source remaining hits 0 and `draggable-partial-count` while both sides are non-zero.
  - Drag moves all remaining in one gesture. A second click does not move more than what is left.
  - Products with API quantity 0 are omitted from the source list (`transferInsertSourceProduct` returns false when total is 0 and nothing is selected).
  - Same product can already exist at the destination; quantities add.
  - If destination `GetProduct` throws, existing destination quantity is assumed 0 and the destination is overwritten to only the moved amount.
  - Single-unit modal sets source cookie quantity to 0, so the backend sets source stock to 0 for that SKU even if the location had more than 1. That is a different rule from the Transfer page, which keeps a remaining quantity. Confirmed from `mapCommitSingleUnitTransfer` 9638–9641.
- Code evidence file+function+lines
  - `Transfer.aspx.vb` `LocationsGetFromCookies` 125–161; `LocationSelector_*_LocationChanged` 742–760.
  - `Transfer.aspx` `TransferOneItem` 329–344; `TransferFunction` 2942–2968; `AddButtonDestination` 2731–2770.
  - `TransferFunctions.vb` 88–93 and 122–124.
  - `Map_CONTROL_2017.ascx` `mapOpenInventoryTransferPage` 9417–9436; `mapCommitSingleUnitTransfer` 9629–9653; drop guards 9370–9372.
- Confidence: Confirmed
- Suggested KB title
  - Transfer products between locations

### Quantity adjust

- Pages
  - None of the scoped movement pages implement an adjust mode. No `isAdjust` (or similar) query flag exists on `Transfer.aspx`.
- What it does (traced)
  - `ActivityCodeIndex.INVENTORY__ADJUST` (25) exists on the activity object and is rendered in history. These movement handlers never call `RegisterActivity` with that code.
  - `Quantity.ListProduct` inserts `ProductNumber` and `LocationID` into `{account}.Quantities` and does not set a quantity and does not write an activity (`Quantity.vb` 4–13). Nothing in the scoped pages calls `ListProduct`.
  - The word “adjusted” inside Transfer is only the import warning when a requested quantity is cut down to on-hand stock. That is still a check-out or transfer, not activity type 25.
  - Destination quantity editors on Transfer change how many units are in the current movement. They do not post an adjust activity.
- Steps (complete sequence)
  - Not applicable. There is no adjust start or complete path in this scope.
- Options/defaults
  - Not applicable.
- Permissions and visibility
  - Not applicable on these pages.
- Validation/failures (quote message strings you find)
  - No adjust-specific messages in these files.
- Side effects
  - None from an adjust mode, because the mode is absent.
- Edge cases
  - Do not describe map or product-grid quantity edits as part of Transfer. They are outside this page set. History code can display adjust comments, which only proves the activity type exists elsewhere.
- Code evidence file+function+lines
  - `Transfer.aspx.vb` `Page_Init` 81–90 (only `isCheckout` and `isCheckin`).
  - `TransferFunctions.vb` 116–124 (only check-out, check-in, transfer).
  - `Quantity.vb` `ListProduct` 4–13.
  - `Activity.vb` `INVENTORY__ADJUST = 25` at line 212 (definition only).
- Confidence: Confirmed
- Suggested KB title
  - Quantity adjust is not part of Transfer or the mobile process

### Import a file into check-in, check-out, or transfer

- Pages
  - Button on `Transfer.aspx` → `ImportFromFile.aspx` → return `ApplyImportedTransfer=1` on `Transfer.aspx` (or the mobile shell).
- What it does (traced)
  - Before leaving, the page stores `IMPORT_TRANSFER_SOURCE` and `IMPORT_TRANSFER_DESTINATION`.
  - On return, `BuildImportedTransferSelectionString` reads `START_ListOfProducts` and `START_ListOfQuantities` (raw lists or GUIDs of server cookies) plus `IMPORT_COMMA_SKIPS`.
  - Match field query `MatchField`: blank or `PN` = product number; `DESC` = `Products.ProductName`; `CF_{index}` = that custom field when the account has it. Ambiguous matches (more than one row) are skipped.
  - Check-out and transfer: the product must be at the source with quantity &gt; 0. Requested quantity above on-hand is reduced to on-hand and counted as adjusted. Unknown and not-at-location rows are skipped.
  - Check-in: catalog match only. Requested quantity is kept. Sentinel quantity is the infinite value. No “not at location” and no reduced-quantity flag.
  - Payload per line: `encodedUid|sourceQty|qtyToMove|wasReduced|requestedQty`. The page then moves those quantities onto the destination and locks the UI (import review). Drag, search, and quantity clicks are removed until save or cancel.
- Steps (complete sequence)
  1. Destination selection must be empty or the import button is hidden.
  2. User imports. Page reloads with `ApplyImportedTransfer=1`. Those import location cookies are expired after they are read.
  3. START product cookies are expired after the payload is built.
  4. Status box: success with row counts, “No items imported”, or “Import Failed”.
  5. User can download unknown or not-found product numbers as CSV, or “Upload Corrected File”.
  6. Save runs the normal comment + commit for the current mode. If the selection was not edited, the comment gains ` {{cs-file-import}}` (or is only that tag).
- Options/defaults
  - Lists are comma-separated and may start with an empty first slot (the code skips index 0 when it is empty).
  - `HideImportFile=true` suppresses the button (map onboarding).
- Permissions and visibility
  - Same as the host Transfer mode. Review mode hides the left column and the normal save bar.
- Validation/failures (quote message strings you find)
  - `"The file could not be read. Please upload it again."`
  - `"The file did not contain any products."`
  - `"No quantity was provided for this product."` (prefixed with the product token)
  - `extraQtyRows + " row has a quantity but no product number."` or `" rows have a quantity but no product number."`
  - `"Row " & (i + 1) & ": No product number."`
  - `": Quantity is missing."`
  - `": Quantity must be a whole number."`
  - `": Quantity must be greater than 0."`
  - `": This value matched more than one product in " & matchFieldName & "."`
  - `": This value was not found in " & matchFieldName & "."`
  - `": This product number was not found in your catalog."`
  - `": This product was not found at the source location."`
  - `": None of this product is available at the source location."`
  - `": The requested quantity is not available at the source location."`
  - Exception path: `"The file could not be checked. Please try the import again."`
  - UI titles: `"Success!"`, `"Import Failed"`, `"No items imported"`, plus `" rows imported"`, `" adjusted quantities"`, `" rows skipped"`, `" unknown products"`, `" products not found at this location"`, link text `"(download)"`, button `"Upload Corrected File"`.
  - Heading in the drop zone: `"Importing from File"`.
  - Warning cleared when its text is exactly `"No valid products found"`.
- Side effects
  - Does not move stock until the user saves. Save is the normal mode’s activity.
  - Import cookies and START list cookies are cleared on the return load even if the user then cancels.
- Edge cases
  - Check-in import never reduces quantity and never lists “not at location”, even if the file named products missing from the catalog (those are “unknown”).
  - A reduced check-out/transfer line shows `!` on the destination quantity.
  - Cancelling review closes the popup and does not set `CookieRefreshRequired`, so the map does not commit.
  - Interaction lock is `isFileImportReturnSession && !isApplyingImportedTransferSelections`.
- Code evidence file+function+lines
  - `Transfer.aspx.vb` `BuildImportedTransferSelectionString` 356–491; `ReadImportMatchField` 519–554.
  - `Transfer.aspx` `buildImportFromFileUrl` 1615–1621; `renderImportStatusBox` 2095–2138; `isTransferInteractionLocked` 2335–2337; `buildTransferCommentWithImportTag` 2514–2525.
- Confidence: Confirmed
- Suggested KB title
  - Import a check-in, check-out, or transfer from a file

### Start page quick check-in, check-out, and transfer

- Pages
  - `Start.aspx`, `Start.aspx.vb`
  - Popup `ProductSelector.aspx?Type=CheckIn|CheckOut|Transfer`
  - Query: `checkin`, `checkout`, `transfer`, `add`, `id`
- What it does (traced)
  - Menu of five actions when the account has at least one product (count query uses page size 10, so “more than zero” is the real test). Zero products hides the menu and shows create-only empty state.
  - Check-in (`ProcessName = 'ADD'`) **adds** each quantity at one location (`OverwriteQuantity = False`). If the selector stored per-line locations (`START_ListOfLocation1` via a server-cookie GUID), each line uses its own location and the activity is registered with `LOCATIONS_REQUIRED` and location id `-2`.
  - Check-out **subtracts** (`CHECKOUT = True`) and floors at 0, then `INVENTORY__CHECK_OUT`.
  - Transfer subtracts from each source and adds to each destination, then `INVENTORY__TRANSFER`. Without per-line locations it uses `START_TRANSFER_SOURCE` and `START_TRANSFER_DESTINATION`.
  - This path does not use `TransferFunctions` or the Transfer drag UI.
- Steps (complete sequence)
  1. Page clears START product cookies and the hidden batch fields.
  2. User clicks Check In, Transfer, Check Out, Create, or Quick Scan. Query flags click those buttons on load and set `forceLocationID` to `id` (the string `"null"` if `id` is absent).
  3. Product selector: check-in/out require one location (`forceLocationID` must be &gt; `-2` to skip the picker). Instruction for transfer source is `"Please select a <br/><b>Destination </b> Location for the Transfer."` after the source is chosen (the label is the destination prompt). Same location is rejected with the string quoted above.
  4. User picks products in the selector. Close with `SELECTOR_PROCEED=TRUE` copies cookies into hidden fields and clicks the matching finish button. `forceLocationID` is reset to `-2` on every fancybox close.
  5. Finish runs immediately, then the page shows the comment step. “Save Comment” calls `WriteComment` and redirects to `Map`. The finish buttons’ client click is `ShowComments()`, so the comment UI appears even though the inventory write already happened on that postback.
  6. Comment placeholder: `"Any comments about this transaction?"`. After finish, instruction HTML is `"Success!<br/>"` and `"You can leave a brief comment if you like."`
- Options/defaults
  - If the location cookie is `-2` and there are no per-line locations, `GetAnyOtherLocationID(-2)` is used.
  - If the location cookie cannot be read and the handler was called with the default `-3`, the handler `Exit Sub` and saves nothing.
  - Per-line location lists set `LOCATIONS_REQUIRED` and, for check-in and check-out, force the single location id to `-2` while the line arrays carry the real ids.
  - Create (`add=true` or the create image) opens `AddProducts.aspx?LastPage=Start` and is not a movement.
- Permissions and visibility
  - Read-only users redirect to `Map_read_only` (`Start.aspx.vb` 18–20).
  - Zero products: `"You have not added any products yet"` and `"Click to create"`. The five-icon menu is not rendered.
  - `UserPage.master` hides the Start menu tab for read-only users and when the account has no products.
- Validation/failures (quote message strings you find)
  - Product selector: `"The Source can't be the Destination! <br/>Please select a <b>Destination. </b>"`
  - Product selector destination prompt: `"Please select a <br/><b>Destination </b> Location for the Transfer."`
  - A bad line (decode/quantity exception) is dropped from the arrays and counted in `NonExistingProductCount`. No user-visible message is set.
  - Missing location cookie: silent `Exit Sub`.
- Side effects
  - Check-in activity `INVENTORY__CHECK_IN` (add).
  - Check-out activity `INVENTORY__CHECK_OUT` (subtract, floor 0).
  - Transfer activity `INVENTORY__TRANSFER` (subtract then add).
  - Comment is a second write via `WriteComment` only if the user clicks “Save Comment”.
  - Records accounts use Assign / Remove / Transfer record helpers.
  - Start `Page_Init` expires `START_ListOfProducts`, names, quantities, item index, `START_NEW_PRODUCTS_CREATED`, and `COOKIE_PRODUCTS_PAGE_RELOAD` on every load, including the load that happens before a query-forced click.
- Edge cases
  - Hidden fields that contain a comma are split in the page. Values without a comma are treated as GUIDs of server cookies. A single product number that itself contains no comma would be parsed as a GUID and throw, then the line-level catch is inside the GUID branch’s caller differently: the GUID parse is outside the per-line try. A malformed GUID fails the whole handler.
  - Check-in button sets `ProcessName = 'ADD'`, not the word check-in. The server button is `btn_finish_add`.
  - `id` on the query string is written into `forceLocationID` even when it is missing (`"null"`). `ProductSelector` only forces the location when the cookie value is `&gt; -2`.
  - File-import locations are supported by the handlers (`Location1Array` / `Location2Array`) even though the Start menu itself does not collect them. `ImportFromFile.aspx.vb` writes `START_LocationID = -2` and `SELECTOR_PROCEED` (outside this page, but the Start handlers honor those cookies).
  - No barcode UI on Start itself. Quick Scan is a separate icon.
  - No lot, expiration, or kitting fields.
- Code evidence file+function+lines
  - `Start.aspx` 90–117, 165–173, 216–253, 315–335.
  - `Start.aspx.vb` `FinishAddHandler` 66–176; `FinishCheckoutHandler` 178–290; `btn_comment_save_Click` 299–306; `btn_transfer_complete_Click` 310–425.
  - `ProductSelector.aspx.vb` `_readyToForceSelect` 114–122; `_changeLocation` 132–189.
- Confidence: Confirmed
- Suggested KB title
  - Start a check-in, check-out, or transfer from the Start page

### Check in products that were just created

- Pages
  - `CheckInCreatedProducts.aspx` + `.vb`
  - `CheckInCreatedProductsDone.aspx`
  - `CreatedProductCheckIn.vb`
  - Overlap: return URL `Transfer.aspx` or `MOBILE_Transfer.aspx` with `isCheckin=true` and optional `ApplyCreatedCheckIn=1`
- What it does (traced)
  - `CreateNewAndStage` merges lines by product number (quantities add; negative quantities become 0), creates catalog rows that do not already exist, and stores a server-cookie batch in `CHECKIN_CREATED_BATCH`. It does not change location quantities. Comment in the class: the batch cookie is not used by Transfer until the return page reads it.
  - Three page shapes:
    1. **Return to Transfer** (`ReturnToTransfer=1`): no map. User sets quantities and Continue. Skip drops the batch and returns to check-in Transfer without selecting the new products. Continue with at least one quantity ≥ 1 rewrites the batch and returns with `ApplyCreatedCheckIn=1`. Transfer then puts those products on the destination list (infinite source, quantity from the batch) and expires the batch. The actual stock change waits for the Transfer save.
    2. **One location for the whole batch:** map column. Default location is query `loc` if it exists, else the user’s `CheckInLocationDefault` when that location exists and is not `-2`. Check In adds every line with quantity ≥ 1 at that one location.
    3. **Imported locations:** every line already has a location id other than `-2`. Map is hidden. Each line checks into its own location. One check-in activity uses `DestinationLocationID = -2`, `LOCATIONS_REQUIRED = True`, and a location id per line.
  - Lines with quantity 0 are omitted. Quantity must be a whole number ≥ 0. At least one line must be ≥ 1.
- Steps (complete sequence)
  1. Some create/import flow calls `CreateNewAndStage` (not inside Transfer itself).
  2. This page reads the batch. Empty batch title: `"No products are waiting to be checked in."` Empty placeholder: `"These products are no longer waiting to be checked in."`
  3. Titles: `"1 Product created."` / `"N Products created."` or, in return mode, `"1 Product was created. Set the quantity, then continue."` / `"N Products were created. Set quantities, then continue."` Map prompt: `"Click a location to Check it in."` / `"Click a location to Check them in."`
  4. Auto SKU note: `"1 product number was generated."` or `"N product numbers were generated."` Transfer shows the same note when `created_checkin_auto_sku_hidden` is set.
  5. Standalone check-in opens a comment modal (“Skip Comment” / “Save”) into `hidden_comment`, then `btn_checkin`.
  6. Success redirects to `CheckInCreatedProductsDone.aspx`, which closes the parent modal and reloads the parent, or sends a standalone window to `/Products.aspx`.
  7. Return-to-transfer Continue does **not** call `SaveCheckIn`. It only updates the batch and redirects.
- Options/defaults
  - Quantity text boxes start at the staged quantity. Steppers increment or decrement.
  - File-origin batches append `{{cs-file-import}}` on the activity comment (`AppendFileImportTag`).
  - `MarkProductsPageReload` sets `COOKIE_PRODUCTS_PAGE_RELOAD=TRUE`.
- Permissions and visibility
  - Read-only users redirect to `/_admin/_unauthorized` (`Page_Init` 16–18).
  - `SaveCheckIn` returns false if destination is `-2` or the location does not exist.
  - `SaveCheckInAtLineLocations` returns false if any included line’s location is `-2` or missing.
- Validation/failures (quote message strings you find)
  - `"Each quantity must be a whole number, 0 or greater."` (`e=qty`)
  - `"Select a location on the map before checking in."` (`e=location`)
  - `"A location in this import could not be found."` (`e=loc`)
  - `"Enter a quantity of at least 1 for one product."` (any other `e`, including `e=none`)
  - `"No products are waiting to be checked in."`
  - `"These products are no longer waiting to be checked in."`
  - Row tooltip: `"This quantity will be checked in to the selected location."` or `"This quantity will be checked in to this location."`
  - Buttons: `"Skip ››"`, `"Continue"`, `"Skip check-in"`, `"Check in"`, `"Check In"`.
- Side effects
  - Standalone save: add quantity (not overwrite) and one `INVENTORY__CHECK_IN`.
  - Per-line locations: same add, one activity, location list on the activity.
  - Return-to-transfer: no quantity change on this page. Transfer later does the check-in.
  - Batch cookie is expired after a successful standalone save, after skip, and after Transfer applies it.
  - Catalog create already happened in `CreateNewAndStage` before this page. Existing SKUs are reused (matched product number, case-insensitive).
- Edge cases
  - Duplicate product numbers in the create list are merged.
  - A line that no longer exists is skipped when Transfer builds the selection (`Product.ProductExists`).
  - Return mode hides the map even if the user still needs a destination; the destination is the Transfer page’s destination.
  - Mobile return path uses `MOBILE_Transfer.aspx` when `Request.Browser.IsMobileDevice` (`TransferReturnPagePath` 205–209).
  - Skip check-in on the imported-location and map layouts calls `closeCreatedProductsModal()` in the browser and does not by itself expire the batch (the done page is not hit). The batch can still be waiting on the next open unless another action expires it.
- Code evidence file+function+lines
  - `CreatedProductCheckIn.vb` `CreateNewAndStage` 26–63; `SaveCheckIn` 232–274; `SaveCheckInAtLineLocations` 281–323; `TransferReturnUrl` 212–221.
  - `CheckInCreatedProducts.aspx.vb` `Page_Init` 13–87; `btn_continue_transfer_Click` 141–182; `btn_checkin_Click` 185–242; `ShowQueryError` 265–281; `SaveImportedLocationCheckIn` 284–323.
  - `Transfer.aspx.vb` `BuildCreatedCheckInSelectionString` 494–516.
  - `Transfer.aspx` apply loop ~2287–2318.
- Confidence: Confirmed
- Suggested KB title
  - Check in products right after you create them

### Mobile process (check-in, check-out, transfer, view location)

- Pages
  - `MOBILE_Process.aspx` + `.vb`
  - `MOBILE_Transfer.aspx` (shell)
  - `MOBILE_LocationSelector.aspx`
  - `Controls/MOBILE_ProcessProgress.ascx`
  - Primers: `MOBILE_MasterPage.master` `mobileHeaderPrimeInventoryFlow`; `UserPage.master` `mapMobilePrimeInventoryFlow`; `mobile_main.aspx` `Process`
- What it does (traced)
  - Cookie `MOBILE_Process` is `CHECK_IN`, `CHECK_OUT`, `TRANSFER`, or `LOCATIONS`.
  - For the three movement kinds, once the required location cookies exist and `MOBILE_ListOfProducts` is empty, the page immediately redirects into the Transfer shell and copies locations into `COOKIE_TRANSFER_SOURCE` / `COOKIE_TRANSFER_DESTINATION` (`-2` for the virtual side).
  - `?CommitTransfer=1` is the save endpoint for that shell.
  - If a product list cookie is already present, the older handlers run instead of TransferFunctions. Those handlers add (check-in), subtract-and-floor (check-out), or subtract-then-add (transfer), then `WriteComment`.
- Steps (complete sequence)
  1. Primer clears `MOBILE_ListOfProducts`, names, quantities, and item index. Sets `MOBILE_Process` and `MOBILE_ReturnAfterProcess` to `Map` (the hamburger and home footer) or, from the map’s own helper, to the current path including `.aspx`.
  2. Check-in writes `MOBILE_DestinationID` when a location id is passed and it is not empty and not `-2`. Otherwise the destination cookie is cleared. Source cookie is cleared. Check-out is the mirror. Transfer clears both location cookies.
  3. `MOBILE_Process` redirects to the location selector until the required ids exist. Selector `SetLocation` writes `MOBILE_SourceID` or `MOBILE_DestinationID` and returns to `MOBILE_Process.aspx`.
  4. Process writes transfer cookies and redirects to `MOBILE_Transfer.aspx` with the mode query. The iframe loads Transfer. User completes the Transfer UI.
  5. Save goes to `CommitTransfer=1`. Stock and activity are the TransferFunctions rules (absolute remaining on source, add on destination, virtual `-2`).
  6. Redirect: full `.aspx` return path, else `MOBILE_main` on commit, or `mobile` on the legacy finish button. Success cookies are queued only when the return path is empty or unsafe.
  7. Legacy list path: comment modal “Add a comment?” with `"Skip"` and `"Save"`. Skip clears the comment. Then the matching handler and the same redirect rules. Button text in markup is `"FINISH"` but the chrome that would show it is hidden except for the LOCATIONS contents view (`pnl_process_chrome.Visible` only when process is LOCATIONS).
- Options/defaults
  - Location selector pre-selects `CheckOutLocationDefault` for `LocationType=Source` and `CheckInLocationDefault` for `Destination`, if that id still exists. Missing defaults become `-2` and are not shown as a header row. Children of `-2` (top of the tree) are listed.
  - Header badge text is `"default"`. Confirming it opens `/_locationSelectorToggle?type=defaultcheckin` or `defaultcheckout`.
  - `setDefaultLocation` on the process page alerts `"The location(s) will be saved for next time"` and stores `CheckOutLocationDefault` or `CheckInLocationDefault`. It does nothing when both source and destination cookies are non-empty, so a transfer does not overwrite a saved check-in or check-out default.
  - Progress labels: check-in and check-out `"Select Location"`, `"Select Products"`. Transfer `"Select Source"`, `"Select Destination"`, `"Select Products"`. Completed steps are links. Back clears the cookies for the steps being left (`mobileProgressBack` in the control).
  - LOCATIONS instructions: `"Locations"`, `"Select Location to view contents"`. Movement instructions (`"Select Products to Check In"`, `"Select Products to Check Out"`, `"Select Products to Transfer"`) are assigned but the step chrome is hidden on the auto-redirect path.
- Permissions and visibility
  - Entire mobile master: not logged in → `Login.aspx`. Read-only → `/Map_read_only`.
  - Menu inventory links hidden when product count is 0. QuickScan remains.
  - Home “new location” tile is omitted for read-only; the map tile remains (`mobile_main.aspx.vb` 523–528). The footer check-in/out markup is still in the page; it only shows after a location is primed in the client.
- Validation/failures (quote message strings you find)
  - `"The location(s) will be saved for next time"`
  - `"Add a comment?"`, placeholder `"Comments..."`, buttons `"Skip"` and `"Save"`.
  - `"Check-in completed successfully."`
  - `"Check-out completed successfully."`
  - `"Transfer completed successfully."`
  - `"Transaction completed successfully."` (process type other than the three)
  - Location change captions: `"Click to change Source"`, `"Click to change Destination"`, `"Click to change"`.
  - `"N Products Selected"` (legacy list).
  - A product line that throws in the legacy handlers is removed from the arrays with no message.
- Side effects
  - Live path: same as TransferFunctions for that mode.
  - Legacy path: add or subtract SQL, activity, `WriteComment` even when the comment is empty.
  - Default location columns on `CS_ADMIN.Users`.
  - Process cookies cleared after commit. `CookieDNDtransferComment` expired after commit.
  - Home load clears process cookies, so the success banner must be a different cookie (`MOBILE_MenuSuccessMessage`), which home reads and expires (`mobile_main.aspx.vb` 70–88).
- Edge cases
  - `mapMobilePrimeInventoryFlow` sets return cookie to `Map`. Commit only follows paths that contain `.aspx`, so this primer returns to mobile home, not the map. The map’s `mapSetMobileReturnAfterProcessToCurrentPage` is the path that actually returns to the map.
  - Progress control comments still say check-in finishes on the product selector. The live check-in path never opens that selector unless something else filled `MOBILE_ListOfProducts`.
  - Check-in progress back step 1 goes to `MOBILE_ProductSelector.aspx`. Check-out and transfer “Select Products” back goes to `MOBILE_Process.aspx`, which immediately sends the user to Transfer again.
  - `SetLocation` writes cookies without `path=/`. Other primers use `path=/`. A path-scoped cookie can disagree with a root cookie of the same name.
  - Legacy check-in **adds**. TransferFunctions check-in also adds, but by overwriting to existing+moved. Legacy check-out **subtracts**. TransferFunctions check-out **overwrites source to remaining**. Mixing a product-selector list with the Transfer shell is avoided only because a non-empty product list skips the Transfer redirect.
  - `CommitTransfer` does not look at `MOBILE_ListOfProducts`. It only reads the Transfer drag cookies.
  - LOCATIONS is a fourth process value. It shows contents and is not a movement.
- Code evidence file+function+lines
  - `MOBILE_Process.aspx.vb` `CompleteMobileTransferFlow` 51–93; `Page_Load` 167–322; handlers 369–557; `save_location` 574–595.
  - `MOBILE_Transfer.aspx` iframe line 17.
  - `UserPage.master` `mapMobilePrimeInventoryFlow` 1540–1573.
  - `MOBILE_MasterPage.master` menu 1001–1007; `mobileHeaderPrimeInventoryFlow` 2582–2605.
  - `Controls/MOBILE_ProcessProgress.ascx.vb` 19–53 and 97–138.
  - `mobile_main.aspx` `Process` 2626–2642; footer 2971–2986.
- Confidence: Confirmed
- Suggested KB title
  - Check in, check out, or transfer on mobile

### Mobile location selector

- Pages
  - `MOBILE_LocationSelector.aspx` + `.vb`
  - Query `LocationType` = `Source`, `Destination`, or `Contents`
- What it does (traced)
  - Lists the location tree from parent `-2`. Search filters rows and expands ancestors. Picking a row calls `SetLocation('SOURCE'|'DESTINATION', id)` and returns to the process page.
  - `Contents` uses the SOURCE cookie (`MOBILE_SourceID`) and is the “view this location” path, not a movement.
- Steps (complete sequence)
  1. Process page redirects here when the needed id is missing.
  2. Optional default row at the top when the user has a saved default that still exists.
  3. Tap a location. Cookie is set. Browser goes to `MOBILE_Process.aspx?`.
  4. Optional: tap `default`, then the pending badge, which opens the toggle URL in the mobile modal and reloads on success.
- Options/defaults
  - Badge label `"default"`.
  - Saved defaults are per user: check-out default for source, check-in default for destination.
- Permissions and visibility
  - Mobile master login and read-only gates.
- Validation/failures (quote message strings you find)
  - No alert strings in the selector code-behind. Failed defaults are treated as `-2` and omitted (`locationExists` 142–145).
- Side effects
  - Writes `MOBILE_SourceID` or `MOBILE_DestinationID` only. Does not move quantity.
  - Default toggle is a separate page (`/_locationSelectorToggle`).
- Edge cases
  - `Contents` and `Source` both call `SetLocation('SOURCE', ...)`.
  - Indent and expand are display only.
  - Progress bar is on this page (see process entry).
- Code evidence file+function+lines
  - `MOBILE_LocationSelector.aspx.vb` `LoadLocations` 129–152; click handlers 260–264 and 362–366.
  - `MOBILE_LocationSelector.aspx` `SetLocation` 505–517; default badge 520–579.
- Confidence: Confirmed
- Suggested KB title
  - Choose a source or destination on mobile

### Mobile product selector and Quick Add

- Pages
  - `MOBILE_ProductSelector.aspx` + `.vb`
  - `MOBILE_QuickAdd.aspx` + `.vb`
- What it does (traced)
  - Legacy picker. Loads products from `api/search` into rows. Quantity &gt; 0 is written to `MOBILE_ListOfProducts`, `MOBILE_ListOfProductNames`, `MOBILE_ListOfQuantities`, and `MOBILE_ItemIndex`. `SignalNext` returns to `MOBILE_Process.aspx`, which then uses the legacy handlers if the list is non-empty.
  - Enter in the search box: if that product row exists, quantity increases by 1. If not, search type 3 runs. Category `"FALSE"` sends the user to Quick Add. Otherwise a row is created at quantity 1.
  - Quick Add shows the query-string product number, a description box (`"Description..."`), `"CREATE"`, and `"CANCEL"`. Create calls `Product.CreateProduct(account, productNumber, description, -2)`, registers `PRODUCT__CREATE` with quantity 1, and redirects to `MOBILE_ProductSelector`. It does not set a location quantity. `Quantity.ListProduct` is not called. Location argument `-2` is “not placed”.
  - The current process page does not navigate here by itself. Progress back, the hidden step divs, and Quick Add’s return URL still do.
- Steps (complete sequence)
  1. Open `MOBILE_ProductSelector.aspx` while `MOBILE_Process` is already set.
  2. Search, tap, or scan (Enter) to raise quantities. Non-numeric quantity is replaced with 1 (`Qty_Adjust`).
  3. Next writes cookies and opens the process page, which shows the comment modal and commits with the legacy add/subtract rules.
  4. Unknown scan: Quick Add. Cancel is `history.back()`. Create returns to the selector; the new SKU is not auto-selected in the code-behind (the selector reloads from the API).
- Options/defaults
  - `DISPLAY_LIMIT = 250` is declared and unused. The old full-catalog hidden fields are commented out. The page sets only `HiddenFIeld_AccountID`.
  - Quick Add `DisplayLimit = 100` is unused.
- Permissions and visibility
  - Mobile master gates. No extra check on these two pages.
  - Quick Add is only reached from a failed selector scan in this scope. Check-in Transfer’s own “create product” path uses `AddProducts.aspx`, not Quick Add.
- Validation/failures (quote message strings you find)
  - No alert on an unknown product; the browser navigates to Quick Add.
  - UI: `"Create New Product"`, `"CREATE"`, `"CANCEL"`, placeholder `"Description..."`.
  - Empty description is still sent to `CreateProduct`. No message.
- Side effects
  - Selector: cookies only, until process finish.
  - Quick Add: new product row at location `-2` and a create activity, not a check-in activity.
  - `Qty_Adjust` uses `If (NEED_TO_UNESCAPE = true)`, which assigns true and always unescapes. That is an edge case in the legacy page (`MOBILE_ProductSelector.aspx` 426).
- Edge cases
  - Quantities are whatever the user types. The legacy check-out subtracts that number and floors at 0. It does not pre-check on-hand stock in the selector (the server load of quantities is commented out; new rows start at 0 until the user increments).
  - Multi-product: every row with quantity &gt; 0 is one line on one activity.
  - No lot, expiration, barcode format check, or kitting.
- Code evidence file+function+lines
  - `MOBILE_ProductSelector.aspx` `Try2Scan` 119–166; `Qty_Adjust` 424–436; `SignalNext` 529–531; `UpdateCookies` 535+.
  - `MOBILE_ProductSelector.aspx.vb` `Page_Load` 38–89 (catalog preload commented out).
  - `MOBILE_QuickAdd.aspx.vb` `btn_create_product_Click` 24–39.
  - `MOBILE_Process.aspx` step divs still link to `MOBILE_ProductSelector.aspx` at lines 344 and 354.
- Confidence: Confirmed
- Suggested KB title
  - Pick products on mobile (legacy) and quick-add a missing barcode

### Quick Scan

- Pages
  - `Popups/QuickScan.aspx` + `.vb`
  - `Scripts/Popups/QuickScan/QuickScan.js`
  - `MOBILE_QuickScan.aspx` + `.vb` (iframe of the popup, query string preserved)
  - Opened from `Start.aspx` (`Popups/QuickScan.aspx`) and `UserPage.master` tools (“Quickscan”) and the mobile menu (“QuickScan”)
- What it does (traced)
  - The barcode box stays focused. Enter calls `api/Scan` with headers `X-CS-TOKEN` (`csToken` cookie copied into a hidden field) and `X-CS-BARCODE`.
  - `response.type == 'product'`: append the product or add 1 to its count.
  - `response.type == 'location'`: fill source if empty, else destination if empty, else shift (old source becomes destination, scanned location becomes source). Scanning a location that is already source or destination swaps the two. Fixed kiosk mode ignores location scans.
  - Mode is derived, not chosen from a menu:
    - No products, or no locations: `invalid` (no save button).
    - Source set (not `-2`) and destination empty (`-2`): **check-out**.
    - Destination set and source empty: **check-in**.
    - Both set: **transfer**.
  - Save POSTs `Transactions[]` of `{product, source, destination, quantity}` to `https://code.cyberstockroom.com/api/inventory?action=checkin|checkout|transfer` with header `X-CS-COMMENT`. Check-in sends source `-2`. Check-out sends destination `-2`.
  - This page does not call `TransferFunctions` or `RegisterActivity`. Whatever activity the API writes is outside this page.
- Steps (complete sequence)
  1. Open the popup or the mobile iframe. Barcode field placeholder `"ready to scan..."`. Instruction `"Scan a product or location"`.
  2. Scan a location, then products, or products then a location. Delete icons clear a location back to id `-2` or remove a product. Quantity boxes are editable (`updateQuantity` on keyup).
  3. Save button text becomes `"Check In"`, `"Check Out"`, or `"Transfer"` (mobile shell button text stays `"Save"` and only the color changes).
  4. Optional comment placeholder `"Optional comment..."`. Enter in the comment field saves.
  5. Success: desktop shows `"N Transactions completed successfully."` and clears products, both locations, and the comment, ready for another scan. Mobile shows `"Transaction saved"` and does the same, unless kiosk mode is on.
  6. Kiosk: `?mode=checkout|checkin&locationID=` must be an integer &gt; 0. The page scans that id as a location barcode. Check-out locks the source and hides destination and the delete control. Check-in locks the destination. Instructions become `"Scan products to check out"` or `"Scan products to check in"`. After save, desktop reloads the same URL. Mobile resets in place so the success row stays visible.
- Options/defaults
  - Initial `source` and `destination` are empty objects treated as id `-2` (`getTransactionType`).
  - Each new scan of an existing uid adds 1. The user can type another quantity before save. There is no max and no on-hand check in this page.
  - `localStorage` key `nTrasactionsCompleted` is reset to 0 on load. The on-screen counter is in memory and also reset on load.
  - Images for location types are preloaded (`preLoadImages`).
- Permissions and visibility
  - Read-only: popup redirects to `/_admin/_unauthorized` (`QuickScan.aspx.vb` 13–15).
  - Mobile host page has no extra check; the master already blocks read-only, and the iframe would also redirect.
  - Fixed mode is rejected unless mode is exactly `checkout` or `checkin` and location id is a positive integer. `transfer` is not a kiosk mode. A bad query falls through to normal Quick Scan (`parseFixedModeFromQuery` returns false).
- Validation/failures (quote message strings you find)
  - `"You have to select at least one location and one product!"`
  - `"Kiosk mode is active; location and mode are fixed."`
  - `"There was a problem saving the transaction!"`
  - `"Transaction saved"`
  - `"N Transactions completed successfully."` (N is the in-page counter)
  - `"Scan a product or location"`
  - `"Scan products to check out"`
  - `"Scan products to check in"`
  - Empty labels `"Source"`, `"Destination"`, `"Products"`.
  - Scan HTTP errors are swallowed (empty error handler). Unknown `response.type` values do nothing.
  - If the kiosk location scan does not return `type == 'location'` with the same id, fixed mode is turned off and the page becomes a normal Quick Scan.
- Side effects
  - One API POST for the whole list (many transaction objects, one action).
  - Comment header only. Empty comment is still sent.
  - No local activity row and no local quantity SQL.
  - Mobile posts `{type:'csQuickScanMode', mode}` to the parent when the derived mode changes. The parent can recolor the shell. Failure to post is ignored.
- Edge cases
  - A transfer requires two different locations only because a scan of the current location swaps instead of filling both with the same id. The save payload does not re-check that source ≠ destination after a swap that might leave them equal if the API returns odd data.
  - Partial quantities: the number input is free text passed through as `products[i].count`. No integer check before POST.
  - Multi-product: one save, many transaction rows, one action type for all of them. You cannot mix check-in and check-out in one save; the mode is global.
  - Deleting the only location returns the screen to invalid and hides Save.
  - Kiosk save on desktop reloads, which resets the success counter because `window.onload` sets `nTrasactionsCompleted` back to 0. The success line is not useful across that reload. Mobile kiosk avoids the reload for that reason (comment in `resetKioskShellAfterSaveMobileEmbed`).
  - No create-on-scan. Unknown products depend on the API error or a non-product type, which this page does not surface.
  - No lot, expiration, or kitting fields in the payload.
  - `Features/Transfers.aspx` is unrelated. Quick Scan is the barcode movement UI.
- Code evidence file+function+lines
  - `Popups/QuickScan.aspx` `getTransactionType` 383–392; `save` 404–438; `apiPostTransaction` 448–491; `parseFixedModeFromQuery` 223–243; `processScan` 678–724; `appendProduct` 727–739.
  - `QuickScan.js` `showCheckin` 103–117; `showCheckout` 119–133; `showTransfer` 135–148; `_clearAll` 193–213; quantity input 234–244.
  - `Popups/QuickScan.aspx.vb` `Page_Init` 10–28.
  - `MOBILE_QuickScan.aspx` iframe line 6.
- Confidence: Confirmed for the page behavior. The API’s stock math and activity rows are **Uncertain** here because they are not in these files.
- Suggested KB title
  - Quick Scan to check in, check out, or transfer

### Mobile home actions (movement-related)

- Pages
  - `mobile_main.aspx` + `.vb`
  - Menu from `MOBILE_MasterPage.master`
- What it does (traced)
  - Home is not itself a movement form. It clears movement cookies on every load, shows recent locations, recent products, and history, and starts movements from the footer or the menu.
- Steps (complete sequence)
  - Menu: Home, Map, Products, Activity, then (if the account has products) Check In, Check Out, Transfer, then QuickScan, Help, Settings, Logout.
  - After the user primes a location, the footer shows Check In, a view-products button, and Check Out. Those call `Process('CHECK_IN'|'CHECK_OUT')` and copy the primed id into the matching mobile location cookie when it is not `-2`. There is no footer Transfer button.
  - View products posts `btn_view_products_hidden` with the primed location. That is navigation, not a movement.
  - Recent-product “+” opens a new-product modal (`csMobileOpenNewProductModal`). Not a check-in.
  - Recent locations include a new-location tile (hidden for read-only) and a map tile.
- Options/defaults
  - Success banner after a movement that returns here uses the theme cookie `CHECK_IN`, `CHECK_OUT`, or `TRANSFER`.
- Permissions and visibility
  - Read-only users never reach this page (master redirect). The read-only branch that hides the new-location tile is therefore only reachable if that redirect is removed.
  - Inventory menu group hidden at zero products (`HideInventoryActionsWhenAccountHasNoProducts`).
- Validation/failures (quote message strings you find)
  - Footer expand labels: `"Show check in and check out"` / `"Hide check in and check out"`.
  - Recent locations empty: `"No recent locations."` (`mobile_main.aspx.vb` 500).
- Side effects
  - `ResetCookies` writes empty product, process, source, and destination cookies and expires `MOBILE_ReturnAfterProcess`. Opening home abandons an unfinished mobile process.
- Edge cases
  - `Process('LOCATIONS')` exists in script and is not wired to the footer.
  - History rows on this page can describe past check-ins, check-outs, transfers, and quantity-adjust comments (`IsAutoQuantityAdjustComment`). Display only.
- Code evidence file+function+lines
  - `mobile_main.aspx` footer 2949–2988; `Process` 2626–2642; `csMobileMainApplyPrimedCookiesForProcess` 1969–1983.
  - `mobile_main.aspx.vb` `ResetCookies` 907–912; `Page_Init` 53–56.
  - `MOBILE_MasterPage.master` 992–1013.
- Confidence: Confirmed
- Suggested KB title
  - Start a movement from the mobile home screen

---

## Shared rules (all Transfer-page modes)

- **What can be moved:** catalog products on check-in; products with on-hand quantity at the source on check-out and transfer. One save can include many products. One activity covers the whole save.
- **Partial quantities:** yes. Click = +1. Badge = typed amount. Drag to destination = all remaining (check-in drag = 1 because the source figure is the sentinel). Drag back = clear that line. Edit can set 0 to remove a line.
- **Barcodes:** the source box placeholder is `"search or scan"`. Camera scans call `transferApplyCameraScanToSearch`. There is no separate barcode symbology check; the text is matched to a product number.
- **Create on the fly:** check-in only (New Products, zero-hit “Create New Product …”, mobile unknown-scan Add Products frame). Check-out and transfer do not create.
- **Location required:** a real destination for check-in and transfer; a real source for check-out and transfer. The other side is `-2` for check-in and check-out.
- **History:** one inventory activity per successful `TransferProductsBackend` call when SQL was produced. Zero moved quantity produces no activity (`SQL_String` empty, function returns false).
- **Batch / lot / expiration / kitting:** no fields, cookies, or API parameters in Transfer, Start, mobile process, Quick Scan, or created-product check-in. The word “batch” in code is the created-product list or an API page of products, not a lot number.

Cookies that carry a Transfer-page movement:

| Cookie | Use |
| --- | --- |
| `COOKIE_TRANSFER_SOURCE`, `COOKIE_TRANSFER_DESTINATION` | Location ids, including `-2` |
| `CookieProductNumberString` | Encoded product numbers |
| `CookieProductQuantityString` | Remaining at source (or sentinel on check-in) |
| `CookieProductQuantityDestination` | Amount to move; only values &gt; 0 are written |
| `CookieDNDtransferComment` | Comment, possibly with `{{cs-file-import}}` |
| `CookieRefreshRequired` | `1` tells the map to commit |
| `IMPORT_TRANSFER_SOURCE`, `IMPORT_TRANSFER_DESTINATION` | Survive the import round-trip |
| `START_ListOfProducts`, `START_ListOfQuantities`, `IMPORT_COMMA_SKIPS` | Import payload |
| `CHECKIN_CREATED_BATCH` | Created-product staging; expired when Transfer applies it |

Mobile process cookies (`Cookies.vb` 48–63): `MOBILE_SourceID`, `MOBILE_DestinationID`, `MOBILE_Products`, `MOBILE_Process`, `MOBILE_ListOfProducts`, `MOBILE_ListOfProductNames`, `MOBILE_ListOfQuantities`, `MOBILE_ItemIndex`, `MOBILE_LocationID`, `MOBILE_ReturnAfterProcess`, `MOBILE_MenuPendingTarp`, `MOBILE_MenuSuccessMessage`, `MOBILE_MenuSuccessTheme`. `MOBILE_Products` and `MOBILE_LocationID` are reset with the others in `ResetAllCookies` but are not read by `MOBILE_Process.aspx.vb`.

---

## UNCERTAIN

- Quick Scan stock updates and activity rows happen in `api/inventory`. This repo’s Quick Scan page only shows success or `"There was a problem saving the transaction!"`. The exact quantity rule (add vs overwrite vs floor) is not in the scoped files.
- Quick Scan `api/Scan` responses other than `product` and `location` are ignored, including the error body. Whether an unknown barcode returns a type this page could show is not visible here.
- `TransferFunctions` destination `GetProduct` failure (any exception, not only “missing”) stores existing quantity as 0 and then overwrites destination stock to the moved amount. How often `GetProduct` throws for a product that is already stocked was not traced.
- Opening `Transfer.aspx` outside the map fancybox still sets `CookieRefreshRequired` and calls `transferParentPopupClose`. If no parent handles that cookie, the movement cookies may sit uncommitted until some later page clicks `btn_hidden_transfer_products`. Mobile shell avoids that by navigating to `CommitTransfer=1` itself.
- `MOBILE_LocationSelector` `SetLocation` omits `path=/` on the cookie write. Behavior depends on the browser’s default path. Not executed in a browser for this audit.
- `Qty_Adjust` assignment bug (`NEED_TO_UNESCAPE = true`) is visible in source. Runtime effect on already-decoded ids was not executed.
- Map clone (`api/inventory?action=clone`) and map single-unit transfer are movement, but they are map UI. Single-unit sets source quantity cookie to 0 (full clear of that SKU at the source) rather than “move 1 and keep the rest”. Confirmed in the map script; called out so it is not confused with the Transfer page’s partial-quantity rule.
- `LoadHeaders` in `Transfer.aspx.vb` looks unused. Old cookies `TRANSFER_FROM` / `TRANSFER_TO` may be dead.
- Records-account (`AccountType = 1`) quantity behavior is delegated to `RecordsApp`. This audit did not re-read that class beyond the call sites. Those call sites do not run `UpdateProductLocationQuantity`.
- No browser pass was run. Messages and control names are from source.

---

## CONTROLS CHECKLIST

### Transfer.aspx / MOBILE_Transfer iframe

- [ ] Source location selector (hidden on check-in and on `IsMobileDevice`)
- [ ] Destination location selector (hidden on check-out and on `IsMobileDevice`)
- [ ] Headers `CHECK-IN` and `CHECKOUT` when those modes force `-2`
- [ ] “Click or Drag” / “Drop Here”
- [ ] Search box placeholder “search or scan”, clear button, Enter behavior (one row vs exact scan)
- [ ] Map-filter badge when `MAP_FILTER` is set; toggle dims rows; hides Everything
- [ ] Product chips: full (green path class `draggable-full-count`), partial, empty
- [ ] Infinity badge on check-in
- [ ] Click chip moves 1; drag to destination moves all remaining (1 on check-in); drag back clears
- [ ] Quantity modal: add (≥ 1, cap at remaining except check-in), edit (0 through total, 0 removes)
- [ ] “Check-Out Everything” / “Transfer Everything (N shown)” — absent on check-in
- [ ] “Clear All (N items)”
- [ ] “import file” hidden once the destination has lines, and hidden when `HideImportFile=true`
- [ ] “New Products” and “Create New Product {term}” on check-in only
- [ ] Import review: left column hidden, drag disabled, titles Success / Import Failed / No items imported, download links, “Upload Corrected File”
- [ ] Reduced-quantity `!` tooltip on check-out and transfer imports
- [ ] Comment modal: “Any comments about this transaction?”, “Skip Comment” / “Save”, Escape confirms
- [ ] Save labels Check In / Check Out / Transfer; Cancel closes the parent
- [ ] Mobile unknown check-in scan opens Add Products iframe (`MobileTransferSingleAdd=1`)
- [ ] Star on products created during this visit
- [ ] Desktop commit via map fancybox; mobile commit via `MOBILE_Process.aspx?CommitTransfer=1`

### Start.aspx

- [ ] Empty account: “You have not added any products yet” / “Click to create”
- [ ] Icons: create, check-in, transfer, check-out, quick scan
- [ ] `?checkin=true&id=`, `?checkout=true&id=`, `?transfer=true&id=`, `?add=true` auto-open
- [ ] Product selector location step, including same-location transfer error
- [ ] Comment step: “Success!”, “You can leave a brief comment if you like.”, “Save Comment” → Map
- [ ] Read-only redirect

### CheckInCreatedProducts

- [ ] Quantity boxes and steppers
- [ ] Map picker vs imported location paths vs return-to-transfer (no map)
- [ ] “Skip check-in”, “Check in”, “Skip ››”, “Continue”
- [ ] Errors for qty, missing location, missing import location, and zero quantities
- [ ] Auto-generated product-number note
- [ ] Done page closes the parent and reloads

### Mobile process, selector, home, master

- [ ] Menu: Check In, Check Out, Transfer, QuickScan (inventory trio hidden at zero products)
- [ ] Home footer Check In / view products / Check Out after a location is primed
- [ ] Location tree, search, default badge, source vs destination vs contents
- [ ] Progress steps and back links (product-selector link is legacy)
- [ ] Transfer shell iframe
- [ ] Legacy comment modal “Add a comment?” only when a product list cookie is already set
- [ ] Success banners on mobile home
- [ ] Quick Add CREATE / CANCEL
- [ ] Read-only and logged-out redirects on the mobile master
- [ ] Home load clears in-progress process cookies

### Quick Scan

- [ ] Barcode field, Enter to scan, refocus
- [ ] Source, products, destination; delete location; delete product; quantity input
- [ ] Save appears only for check-in, check-out, or transfer
- [ ] Alerts for no location/product, kiosk mismatch, and save failure
- [ ] Success counter (desktop) or “Transaction saved” (mobile)
- [ ] Kiosk `mode` + `locationID` locks one location and reloads or resets after save
- [ ] Optional comment; Enter in comment saves
- [ ] Read-only redirect on the popup
