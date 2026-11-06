# Products — code feature catalog

Source audit of CyberStockroom products. Application source was not modified. Behavior below is traced from the files in scope. Nothing here was confirmed by running the application.

- Branch: `mobile-responsive`
- Commit: `e8172b5`
- Date of audit: 2026-11-05
- Confidence labels: **Confirmed** = read in the named code. **Inferred** = a reasonable reading of that code, not a second path. **Uncertain** = the source does not settle it.

Out of scope except where a products control opens them: Settings (where show-images, zero-quantity, and expirations are stored), the map control’s internal quantity editor, the custom-field editor modal, and the full Export Report query. Those are described only at the hand-off.

---

## Page inventory

| Page | Role | Who can open it |
|---|---|---|
| `Products.aspx` | Product grid, toolbar, search chips, columns, multi-edit, delete, export, print barcodes | Any signed-in user who is not Read only. Read only is redirected to `Products_read_only`. |
| `Products_read_only.aspx` | Same grid without create, delete, multi-edit, or inline quantity | Read only only. Other users are redirected to `/Products`. |
| `ProductEditor.aspx` | One product: fields, image, attachments, barcode, clone, delete, expiration, map | Not Read only. Read only is redirected to `ProductEditor_read_only` with the same product number. Missing or unknown product number goes to `Product Error.html`. |
| `ProductEditor_read_only.aspx` | Same layout with fields, dropdowns, expiration, and image upload disabled | Read only only. Other users are redirected to `/ProductEditor`. |
| `AddProducts.aspx` | Create one or more products, optional image, then stage check-in | Not Read only (`/_admin/_unauthorized`). |
| `ImportFromFile.aspx` | CSV column match for create, check-in/out, or transfer | Not Read only. |
| `CheckInCreatedProducts.aspx` | Quantity and location for products just created | Not Read only. |
| `CheckInCreatedProductsDone.aspx` | Closes the modal and reloads the parent | No server permission check. Markup only. |
| `SuccessProducts.aspx` | Static “Success” page and a products-reload cookie | No caller in this repo. See UNCERTAIN. |
| `PrintBarcode.aspx` | Code 128 label preview and print | No Read-only bounce in `Page_Init`. Opened from the grid and the editor. |
| `ExportReport.aspx` | CSV download opened from the products download button | Not fully in scope. Launch and visible options are recorded under Export. |
| `ProductSelector.aspx` | Pick products for Check In, Check Out, or Transfer | Not Read only. |
| `Popups/CloneProduct.aspx` | Older clone form | Not Read only. No save control in the markup. The editor’s Clone button that called it is commented out. |
| `Popups/FixedMultiFields.aspx` | Preset values for one custom field | Admin only. Opened from `js/business/custom-fields.js`, not from the products grid. |
| `Dialogs/ProductDeleteConfirmation.aspx` | Delete quantities from one location or all locations | Not Read only. No caller sets `Session("ProductsToDelete")` or links this page. The live delete path does not use it. |
| `DocumentEditor.aspx` | Reads one purchase order, sales order, or kit and lists its lines | Not Read only. Header actions are literal text, not buttons. No link from the product pages. |
| `Controls/EDITABLE_FIELD.ascx` | Inline text/currency field used by the product editor | Used when the editor builds product name, buy price, sell price, and free-text custom fields. |
| `Samples/Products.csv` | Sample for create import | Header only recorded below. |
| `Samples/ProductList.csv` | Sample for check-in/out without locations | Header only. |
| `Samples/ProductListLocation.csv` | Sample for check-in/out with one location | Header only. |
| `Samples/ProductListLocationTransfer.csv` | Sample for transfer | Header only. |

Supporting code that is not a page: `Products.js`, `ProductsGridUrlCells.js`, `ProductEditorClone.js`, `ProductEditorCfUrlOpenLink.js`, `EDITABLE_FIELD.js`, `ProductSelector_v2.js`, `Product.vb`, `Products_Helper.vb` (empty class), `Quantity.vb`, `Batch_Class.vb`, `CSV_Class.vb`, `BarcodePngGenerator.vb`, `CS_Document_Class.vb`, `CreatedProductCheckIn.vb` (staging and check-in after create/import).

User types that change these pages (`User_Legacy.TypeOfUserAccount`): Read only, and Admin (column/field editor links). Account type `0` is the standard app. Account type `1` is treated in code as the records app and hides or skips prices. Buy price and sell price also depend on `ShowBuyPriceField` and `ShowSellPriceField`. Product images and zero-quantity rows depend on the user flags `SHOW_PRODUCT_IMAGES` and `SHOW_ZERO_QUANTITY`. Expirations depend on `SHOW_EXPIRATIONS`.

---

### Products grid

- Pages: `Products.aspx`, `Products.aspx.vb`, `Products_read_only.aspx`, `Products_read_only.aspx.vb`
- What it does (traced): Loads products for the location in `DisplaySettings.LocationID_VIEW`. Location `-2` is labeled ALL LOCATIONS. A specific location shows products whose quantity at that location is greater than 0. If that location’s own quantity list is empty, the page then loads products that have quantity greater than 0 in child locations and shows “This location is empty but its sub-locations are not”. Page size is 50. The grid is custom-paged. A cookie `COOKIE_PRODUCTS_KEEP_VIEW` stores `page|sortDirection|sortExpression` and is restored on the next open.
- Why: The inventory list for one location or the whole account.
- How to access and visibility conditions: Main Products menu (`UserPage.master` marks the Products tab when the page class is `Products`). Read-only users never stay on `Products.aspx`. On viewports at or under 900px the location selector is hidden and a plain path is shown (`lbl_products_mobile_location_path`). Wider viewports show `LocationSelector`.
- Steps: Open Products. Change location with the selector. The page saves `LocationID_VIEW` and reloads, keeping page and sort.
- Options and defaults: Default sort expression `DEFAULT`, which the query turns into `ProductNumber` ascending (`SortDirection` 0 = ASC, 1 = DESC). Default page index 0.
- Permissions: Signed-in account user. Read only uses the read-only page.
- Validation/limits/failures: If the readable location path throws, the mobile label falls back to “ALL LOCATIONS”.
- Result and side effects: Writes cookies `LocationType=VIEW` and clears `STOCKROOM_BATCH` on every products init. Sets `Session("LocationID_VIEW")` for the editor.
- Edge cases: All Locations appends products with total quantity 0, or with no quantity row, after the in-stock page is filled (`GetInactiveInventory`). A specific location does not append those zero rows in that function; zero quantity at the selected location is excluded by `Quantity > 0`. Users with `SHOW_ZERO_QUANTITY = False` drop quantity 0 rows while the display table is built. Search replaces the location filter (see Search).
- Related: Columns, sort, empty states, inline quantity, product editor.
- Code: `Products.aspx.vb` `Page_Init` 45–74, `GRIDVIEW_INIT` 90–124, `InventoryGetAndDisplay` 1557–1707, `getInventoryInSubLocations` 1455–1555, `GetInactiveInventory` 1709–1773, `LocationSelector_control_LocationChanged` 2124–2134. Read-only gate: `Products_read_only.aspx.vb` `Page_Init` 46–53.
- Confidence: Confirmed
- Suggested KB title: View products by location

### Empty inventory messages

- Pages: `Products.aspx`
- What it does (traced): If the grid has no rows and sub-locations are also empty: at All Locations, “No products yet” and “Click to create” open `AddProducts.aspx?LastPage=Products`. At a specific location, “Location is empty...” and “Click to Check in” go to `Start.aspx?checkin=true&id={location}`. If only sub-locations have stock, the dashed message is not a link.
- Why: First-run and empty-location prompts.
- How to access and visibility conditions: `div_empty_products`, `div_empty_location`, `div_subLocationsFull` start `visible=false` and are turned on in `MessageNoProductsShow`.
- Steps: Land on an empty list.
- Options and defaults: None.
- Permissions: The create link is on the editable products page. Read-only markup was not given the Add Products empty link in the toolbar; the read-only empty-state markup was not separately verified beyond the shared method names. Treat the create link as editable-page only.
- Validation/limits/failures: During search with no matches, `lbl_no_result_A` is set to “No matches found!” and `lbl_no_result_B` is hidden.
- Result and side effects: Navigation only.
- Edge cases: A search that returns rows does not show these panels.
- Related: Add products, check-in.
- Code: `Products.aspx` 737–754; `Products.aspx.vb` `MessageNoProductsShow` 243–256, search no-match 1644–1646.
- Confidence: Confirmed for the editable page. Read-only empty copy is Inferred to share `MessageNoProductsShow` because that method exists on the read-only code-behind, but the read-only markup for those three divs was not re-read line by line.
- Suggested KB title: What you see when a location has no products

### Columns

- Pages: `Products.aspx`, `Products_read_only.aspx`
- What it does (traced): Columns are Product Number (header “Product Number”), Quantity, Product Name (header “Description”), Buy Price, Sell Price, each account custom field (`CF_{index}`), and Cost Value (quantity times buy price). Product Number cannot be unchecked (`disabled`, class `fixed-sort-item`). The Columns image opens a checkbox list. SAVE COLUMNS posts `btn_AdjustColumns`, writes `CS_ADMIN.Users.ColumnOrder` for this user, and reloads while keeping page and sort. Header cells are draggable; dropping rewrites the `ColumnOrder` cookie and clicks SAVE COLUMNS. Unchecking a box rewrites that cookie immediately through `ToggleColumnDisplay` / `ColumnCheckClicked`.
- Why: Each user chooses which product attributes appear and in what order.
- How to access and visibility conditions: Columns image, tooltip “Select the columns to display in your inventory”. Admin users on the editable page also get EDIT COLUMNS, which calls `openCustomFieldEditor()` (the custom-field modal, not this catalog). Read-only has SAVE COLUMNS and no EDIT COLUMNS placeholder in `Page_Init`.
- Steps: Hover or mouse-over the columns control (`ColumnsDropdownShow`). Check or uncheck. Drag the list or drag a grid header onto another header. Save.
- Options and defaults: If the server column string is empty and the browser cookie is missing, empty, or does not contain “Product Number”, `ColumnsDefaultDisplay` writes ` Product Number, Quantity, Product Name, Buy Price, Sell Price, Cost Value, ` plus every `CF_{index}` and reloads. Server value wins over the browser cookie when the server value is non-empty.
- Permissions: Any products user can save their own column order (`AccountID` + `UserIndex`). EDIT COLUMNS is Admin.
- Validation/limits/failures: A stale `CF_` index expires the column cookie. An unknown token calls `ColumnsDefaultDisplay`.
- Result and side effects: `UPDATE CS_ADMIN.Users SET ColumnOrder`. Cost value is calculated in the page, not stored.
- Edge cases: Buy and sell headers include the account currency. The unchecked Cost Value label in one branch is “Cost Value” without the currency (`CheckboxesCreate` line 403) while the checked label includes the currency. Description cells that are only `&nbsp;` display `UNTITLED (Product Number : {number})`. Prices format as `0.00`. Cost value formats as `###,###,##0.00`.
- Related: Custom fields, export field list (separate page).
- Code: `Products.aspx.vb` `CheckboxesCreate` 327–416, `ColumnsDefaultDisplay` 692–728, `ColumnsToDisplayGet` 755–856, `btn_ColumnAdjust` 730–734, `SetColumnOrderDB` 744–754, `GridView1_RowDataBound` 857–1032. `Products.js` `ToggleColumnDisplay` 98–134, `drop_col` 172–187. `Products.aspx` 568–610.
- Confidence: Confirmed
- Suggested KB title: Choose and reorder product columns

### Sort

- Pages: `Products.aspx`, `Products_read_only.aspx`
- What it does (traced): Header link buttons sort. First click on a column sets direction 0 (ASC). Clicking the same column again flips 0 and 1. Page index returns to 0. The active header gets `sort-indicator sort-asc` or `sort-desc`. While sort expression is `DEFAULT` or `ProductNumber`, the Product Number header is treated as the current sort.
- Why: Order the grid.
- How to access and visibility conditions: Any visible data column header. The checkbox column is not sortable.
- Steps: Click a header.
- Options and defaults: See grid defaults.
- Permissions: Same as the grid.
- Validation/limits/failures: Quantity sorts by `SUM(Quantities.Quantity)`. Cost value sorts by `SUM(Quantity)*BuyPrice`. Custom fields sort by `Products.CF_{index}`.
- Result and side effects: View state and `COOKIE_PRODUCTS_KEEP_VIEW` update inside `InventoryGetAndDisplay`.
- Edge cases: `GridviewSortDirectionGet` (1115–1142) stores ASC/DESC strings and is not called by `GridView1_Sorting`. The live path uses integer 0/1. All Locations still splits in-stock rows from zero-quantity rows, so a sort does not mix those two groups into one sequence.
- Related: Pagination.
- Code: `Products.aspx.vb` `GridView1_Sorting` 1085–1113, `GetColumnNameFromIndex` 1034–1054, `HeaderTextWithSortIndicator` 1056–1068.
- Confidence: Confirmed
- Suggested KB title: Sort the product list

### Pagination and select-all

- Pages: `Products.aspx`, `Products_read_only.aspx`
- What it does (traced): Pager is numeric with first and last images, top and bottom. `hidden_FullCount` is the product-table count on first load (`SELECT COUNT(*) FROM {account}.Products`). For a specific location the count is replaced with the count of products that have quantity > 0 there. Checking the header checkbox selects the rows on this page and shows: “The {n} Products on this page are selected” plus “Select all {full count} products.” Choosing that sets `hidden_SELECT_ALL_COMPLETE` to 1. Clearing it unchecks the page.
- Why: Move through 50-row pages and apply bulk actions to the page or the whole catalog.
- How to access and visibility conditions: Pager when `VirtualItemCount > 50`, except during search (`hidden_HasPagination` is set to 0 and `VirtualItemCount` is set to 1).
- Steps: Use the pager. Or check the header box, then the “select all” link.
- Options and defaults: Page size 50 (`PageSize`).
- Permissions: Same as the grid. On the editable page, selection enables Delete, Multi-edit, and Print barcodes. On the read-only page, selection enables Print barcodes only.
- Validation/limits/failures: `CheckedProductsGelCompleteInventoryList` is `SELECT ProductNumber FROM {account}.Products` with no location and no search filter. “All products” means every product in the account.
- Result and side effects: Page changes call `InventoryGetAndDisplay` and rewrite the keep-view cookie.
- Edge cases: The SQL limit is `LIMIT {page*50}, {page*50+50}`. MySQL reads that as offset, row count, so page 0 returns 50 rows and later pages request more than 50 rows. Search does not paginate, so a search uses whatever page index is already in view state and then hides the pager. Inactive products are only merged onto a page when the active query returned fewer than 50 rows.
- Related: Delete, multi-edit, print barcodes.
- Code: `Products.aspx` 1163–1263 (select-all script, from the earlier match), `EnableHiddenButtons` 789–814. `Products.aspx.vb` `GridView1_PageIndexChanging` 675–680, `CheckedProductsGet` 2054–2067, limit string 1602.
- Confidence: Confirmed for the select-all SQL and the limit string. The exact select-all script text is Confirmed from the line matches in `Products.aspx` 1233 and 1259.
- Suggested KB title: Pages and selecting every product

### Search

- Pages: `Products.aspx`, `UserPage.master`, `Products.js`
- What it does (traced): The master search box (`CS_SEARCHBOX1`) on query search appends the text to cookie `COOKIE_PRODUCT_SEARCH_FILTER` and redirects to `/Products.aspx`. The products page, when that cookie has text, forces the location selector to All Locations and filters with AND across comma-separated terms. Each term is `LIKE` on product number, product name, and every custom field. Terms are shown as chips. One chip runs `ClearSearchFilter`. If more than one term is present, an ALL chip runs `ClearAllSearchFilters`. A `?Search=` query string expires the old cookie, writes that one term, and searches. Leaving Products or Product Editor clears the search cookie and the keep-view cookie (`UserPage.master` `Page_Init` when the path does not contain `Products` or `ProductEditor`).
- Why: Find products without staying inside one location.
- How to access and visibility conditions: Global search on the signed-in shell. Chips appear in `DIV_SEARCH_FILTER` only when a term exists. `Products.js` `custom_search()` writes cookie `custom_search` and clicks `FORCE_CUSTOM_SEARCH`, and the server handler still appends that cookie, but `Products.aspx` does not assign `JS_HANDLE__FORCE_CUSTOM_SEARCH`. That function is not wired on the current products markup.
- Steps: Search from the master box. Remove a chip or ALL. Or open `/Products?Search=term`.
- Options and defaults: No field picker. Search does not include buy price, sell price, or quantity.
- Permissions: Same as the grid, including read-only (`SearchIfRequested` is on both code-behinds).
- Validation/limits/failures: Duplicate terms in the cookie are removed before display. Blank terms are skipped.
- Result and side effects: Location view is set to -2 for the request. The saved `LocationID_VIEW` is not what this search displays. “No matches found!” replaces the create prompt. `hidden_FullCount` becomes -1.
- Edge cases: Because pagination is suppressed, only one limited slice of matches is shown. The location SQL is removed (`SQL_CLAUSE_SEARCH.Substring(4)`), so search is account-wide even if a location was selected. Spaces inside a term are not turned into wildcards by `SearchTermWrite`; `SearchTermsGet` replaces spaces with `%` but the display path uses the raw cookie.
- Related: Columns (custom fields are searchable even when hidden — the SQL loops all account custom fields, not the visible columns).
- Code: `UserPage.master.vb` `CS_SEARCHBOX1_AC_QuerySearchRequested` 339–344 and cookie clear 90–95. `Products.aspx.vb` `SearchIfRequested` 519–550, `SearchFiltersShow` 566–608, `SQLSearchClauseGet` 1952–1985, `SearchFunctionNoAutopostback` 636–646. `Products.js` `ClearSearchFilter` 24–44, `custom_search` 79–85.
- Confidence: Confirmed
- Suggested KB title: Search products

### Open a product

- Pages: `Products.aspx`, `Products_read_only.aspx`
- What it does (traced): Every data cell’s click calls `callFancyBoxProductDetails` with `ProductEditor.aspx?ProductNumber={encoded}&AutoHighlight=TRUE`, or `ProductEditor_read_only.aspx` on the read-only grid. `AutoHighlight` is only placed on the query string; `ProductEditor.aspx.vb` `Page_Init` does not read it.
- Why: Edit or view one product from the list.
- How to access and visibility conditions: Any product row. The checkbox column is index 0 and is not given this click in the loop that starts at cell 1.
- Steps: Click a row cell.
- Options and defaults: None.
- Permissions: Editor page then applies its own read-only redirect.
- Validation/limits/failures: Product number is URL-encoded. If thumbnails are on, the product-number cell HTML includes an image; delete/print selection strips text after `<br/>`.
- Result and side effects: Opens the editor in the fancybox hook `hidden-clicker-autocomplete-product-details` after clearing `#autocomplete_search`.
- Edge cases: Quantity cells that are in edit mode stop propagation on the input, arrows, and OK image. URL pills also stop propagation.
- Related: Product editor, URL pills, inline quantity.
- Code: `Products.aspx.vb` `GridView1_RowDataBound` 1005–1013. `Products.js` `callFancyBoxProductDetails` 1–7. Read-only row script: `Products_read_only.aspx.vb` 961.
- Confidence: Confirmed. Effect of `AutoHighlight` inside the editor is Uncertain because it is unread.
- Suggested KB title: Open a product from the list

### URL pills in the grid

- Pages: `Products.aspx` (script also included from the products page head; read-only page was not confirmed to include `ProductsGridUrlCells.js`)
- What it does (traced): After load and after async postback, cells whose entire text is an http(s) URL, a protocol-relative URL, a `www.` host, or a bare domain become a pill. The pill shows the host (leading `www.` removed, port kept), opens in a new tab, and does not open the product editor.
- Why: Custom-field or description values that are links can be opened from the list.
- How to access and visibility conditions: Any data cell except the checkbox column, and not cells that already contain an image, button, input, select, textarea, label, the quantity editor, or an existing pill.
- Steps: Show a column whose value is a URL. Click the pill.
- Options and defaults: None.
- Permissions: Script runs for whoever loads `Products.aspx`.
- Validation/limits/failures: Non-URL text is left unchanged. `javascript:` and other schemes are rejected.
- Result and side effects: Display only. The stored value is kept on `data-products-url-original`.
- Edge cases: A cell with extra words around a URL is not converted, because the whole text must match.
- Related: Product editor custom-field open-link icon.
- Code: `Scripts/Pages/Products/ProductsGridUrlCells.js` `normalizeUrl` 11–63, `enhanceGrid` 165–221. `Products.aspx` 12–27.
- Confidence: Confirmed for `Products.aspx`. Whether the read-only page includes this script was not re-checked in the read-only head. Uncertain for read-only.
- Suggested KB title: Open a web address from the product list

### Product images on the grid

- Pages: `Products.aspx`, `Products.aspx.vb`
- What it does (traced): If `UserCredentials.SHOW_PRORDUCT_IMAGES` is true, each product-number cell gets a 40×40 image from `imageProcessor.getProductImage`. On error, demo SKUs that start with `CS_DEMO_` use `Images/Pages/Products/{sku}.png`. Others use `Images/icons/cam_small.png`. The toolbar camera button `btn_image_toggle` is commented out, and `btn_image_toggle_Click` is commented out. The flag is a user setting, not a products-page toggle.
- Why: Recognize products in the list.
- How to access and visibility conditions: Only when the user flag is on. There is no working Hide/Show button on this page.
- Steps: Turn the setting on elsewhere (Settings reads `toggle_show_product_images`). Reopen Products.
- Options and defaults: Thumbnail side 40 (`CONST__THUMBNAIL_IMG_WIDTH`).
- Permissions: Per user, not per account.
- Validation/limits/failures: HTML-looking SKUs (first character `<`) skip the image. Exceptions are swallowed.
- Result and side effects: Display only.
- Edge cases: The image is in the product-number cell, so row click and barcode/delete parsing have to deal with `<img>...<br/>{sku}<br/>`.
- Related: Editor image upload.
- Code: `Products.aspx.vb` `StylingRefresh` 273–278, `GridviewImagesAdd` 1144–1178. Commented button: `Products.aspx` 676–684.
- Confidence: Confirmed
- Suggested KB title: Product photos in the list

### Inline quantity

- Pages: `Products.aspx` only
- What it does (traced): On a specific location (id > -2), when the row is in stock (color index 2), and the page is not in search and not in the “sub-locations are full” state, clicking the quantity cell replaces it with a text box, up and down arrows, and an OK image. Enter or OK posts JSON to `https://code.cyberstockroom.com/api/inventory?action=adjust` with source and destination equal to that location and `quantity` set to the new absolute number. Header `X-CS-COMMENT` records the old and new numbers. Success reloads and keeps the view. Failure alerts “There was a problem updating the quantity in this location...”. The request times out at 3 seconds. Escape or opening another cell restores the original text. Down arrow stops at 0. Non-numeric values do not submit. Arrow keys step the value only when the browser matches `(hover: hover) and (pointer: fine)`. Mobile width (max 900px) sets `inputmode=numeric`. Pinch zoom scales the grid between 0.18 and 1.8 on that same breakpoint.
- Why: Change stock at the location you are viewing without opening the editor.
- How to access and visibility conditions: In-stock quantity cells only, and only on the editable page. Read-only always applies class `all-locations` and does not assign `QtyQuickAdjust`. All Locations, search results, and the sub-location summary do not get the editor. Out-of-stock cells (color index other than 2) do not get it, and those rows are the ones with quantity 0.
- Steps: Select a location. Click a green quantity. Type or step. Press Enter or OK.
- Options and defaults: None.
- Permissions: Uses cookie `csToken`. Read only cannot reach this page.
- Validation/limits/failures: `isNumeric` must pass. The API error path is a single alert. No in-page message for a timeout versus a rejected quantity.
- Result and side effects: Inventory adjust at one location. The page does not itself write SQL for this action.
- Edge cases: Only one editor is open. Product numbers are decoded from HTML before the call. Zero-quantity rows are not clickable even at a specific location.
- Related: Product editor map instruction “Click a location. Type new quantity. Press Enter.” Multi-edit quantity overwrites rather than going through this API.
- Code: `Products.aspx` `QtyQuickAdjust` 259–346, `submitQtyQuickAdjust` 213–257. `Products.aspx.vb` `GridViewRowRepaint` 494–508. Read-only: `Products_read_only.aspx.vb` 453–462.
- Confidence: Confirmed for the request the page sends. What the API does with an adjust when source equals destination is outside this file. Inferred that it sets the location quantity because the body field is `quantity` and the comment says “adjusted from {old} to {new}”.
- Suggested KB title: Change quantity from the product list

### Add products button

- Pages: `Products.aspx`
- What it does (traced): Image button tooltip “Add one or more products to your inventory” is wrapped in a link to `AddProducts.aspx?LastPage=Products` (`fancybox-add-products`). The same link wraps the empty-catalog message.
- Why: Start the create flow from the list.
- How to access and visibility conditions: Always on the editable toolbar. Not on the read-only toolbar (no `btn_Add` in `Products_read_only.aspx`).
- Steps: Click the add image.
- Options and defaults: Query `LastPage=Products`.
- Permissions: Add Products itself blocks Read only.
- Validation/limits/failures: None on the button.
- Result and side effects: Opens the add page in the fancybox class used for add-products.
- Edge cases: The image button’s `Text` attribute says “Select Columns”; the tooltip is the real instruction.
- Related: Add products, import.
- Code: `Products.aspx` 503–505 and 737–743.
- Confidence: Confirmed
- Suggested KB title: Add products from the product list

### Delete selected products

- Pages: `Products.aspx`, `Product.vb`
- What it does (traced): Delete stays disabled (`hidden-btn`, opacity 0.1, no pointer events) until at least one checkbox is on. Click runs `confirm('Are you sure you want to delete the selected products from your inventory? This action cannot be undone!')`. OK posts `btn_delete_Click`, which loads the page selection or, if select-all-complete is on, every product number in the account, then `Product.DeleteProducts`. The page reloads and keeps the view.
- Why: Remove product records from the account.
- How to access and visibility conditions: Editable products toolbar only. Tooltip “Delete selected products from your inventory.”
- Steps: Check rows. Click delete. Confirm.
- Options and defaults: None. There is no “this location only” choice on this button.
- Permissions: Not available to Read only.
- Validation/limits/failures: Cancel stays on the page. An empty selection does not enable the button.
- Result and side effects: `DeleteProducts` URL-decodes each number, constructs `productDeleter`, calls `delete()`, registers activity `PRODUCT__DELETE` with quantity `1` per product, commits the unit of work, and calls `ProductExpirations.Delete`. The class `productDeleter` is not in the repository files that were searched, so image, attachment, and quantity deletion inside that class are Uncertain. Older methods `_DeleteProduct` and `_DeleteProducts` do delete the product row, the quantity rows, and images, and they are not the method the button calls.
- Edge cases: Select-all-complete deletes every product in the account, including products outside the current location and outside the search. The confirm text says the action cannot be undone. `Dialogs/ProductDeleteConfirmation.aspx` is a different, unwired page that only deletes quantity rows.
- Related: Delete one product in the editor. Orphan delete dialog.
- Code: `Products.aspx` `DeleteConfirmation` 137–143, button 513. `Products.aspx.vb` `btn_delete_Click` 2136–2142. `Product.vb` `DeleteProducts` 58–85, `_DeleteProduct` 26–56.
- Confidence: Confirmed for the button and `DeleteProducts`. Uncertain for the deleter’s extra tables.
- Suggested KB title: Delete products from the list

### Multi-edit

- Pages: `Products.aspx`
- What it does (traced): The edit image stays disabled until one or more rows are checked. It opens a panel “For All Selected Items” with SET {field} TO {textbox}, Update, and Cancel. Update runs `CheckedProductsMultiEdit` and, on success, clears the textbox and reloads.
- Why: Write one value onto many products.
- How to access and visibility conditions: Editable page only. Dropdown is filled in `MultiEditDropDownPopulate`: Product Name; Quantity only when the viewed location is not -2; Buy Price and Sell Price with the account currency; then each custom field name. At All Locations, Quantity is omitted and the index map shifts.
- Steps: Select a location if you need quantity. Check products. Open multi-edit. Pick a field, type a value, Update.
- Options and defaults: No default value. Cancel only hides the panel (`MultiEditDropdownShow` toggles it).
- Permissions: Not Read only. Account type 1 does not run the SQL update; it calls `RecordsApp.AdjustRecord("", SourceID, MO, , True, ProductList)`.
- Validation/limits/failures: Empty value: “Please enter a value”. Buy and sell must be numeric. At All Locations the numeric check also requires `CInt(value) < 0` to fail, so a non-numeric or negative integer fails with “Value must be numeric!”. At a real location, buy, sell, and quantity only check `IsNumeric` (negatives pass that check). Custom fields must be in `validValues` unless the list is empty or contains “Other (Specify)”. Otherwise “Value is not allowed for this field.” A bad dropdown index: “Invalid field selected.”
- Result and side effects: Name, prices, and custom fields: `UPDATE Products SET {column}=@P1 WHERE ProductNumber=...`. Quantity: `INSERT INTO Quantities (Quantity, ProductNumber, LocationID) VALUES (...) ON DUPLICATE KEY UPDATE Quantity=@P1` at the current location. That overwrites the location quantity. Activity `PRODUCT__EDIT` is recorded with the field label and the new text. The activity quantity list is the string `"1"` per product, not the quantity you typed.
- Edge cases: Select-all-complete updates every product in the account. Quantity is the same number at one location for each selected product; it does not add. Custom-field preset lists are enforced here, but “Other (Specify)” allows any text. Decimal buy/sell values are stored as typed when the numeric check passes. `CInt` on the All Locations path can round a decimal before the negative test, so a small negative decimal can pass that test. Confirmed from the `CInt` call; not executed.
- Related: Editor field edit, inline quantity (different API), fixed presets.
- Code: `Products.aspx` 520–540. `Products.aspx.vb` `MultiEditDropDownPopulate` 228–241, `CheckedProductsMultiEdit` 1235–1394, `cfValueIsAllowed` 1206–1228, `btn_MultiEdit_UPDATE_Click` 2117–2121.
- Confidence: Confirmed
- Suggested KB title: Change one field on many products

### Recently created

- Pages: `Products.aspx`, `Products_read_only.aspx`
- What it does (traced): Hovering the recent-products image shows a panel “Recently Created” with up to 50 rows from activities whose `ActivityCode` is 0, newest first, joined to activity contents. Each line is `{local date} : {product number}` and opens that product in the editor (`AutoHighlight=TRUE`). Dates are shifted by `AccountSettings.TimeZone` hours. The server offset is hard-coded 0. If there are no rows: “No recent new products...”.
- Why: Jump back to products that were just created.
- How to access and visibility conditions: Toolbar image `recently_created.png`. Mouse over shows, mouse out hides. Present on both products pages; the read-only click target is `ProductEditor_read_only.aspx`.
- Steps: Hover. Click a product number.
- Options and defaults: Display limit 50. The query itself is not limited before the loop.
- Permissions: Same as the page.
- Validation/limits/failures: A bad activity row is skipped (`Try/Catch` per row).
- Result and side effects: Read only. Opens the editor.
- Edge cases: Activity code 0 is not named in this file. It is the code this panel treats as creation. Product numbers are not URL-encoded in the script string built here (`RecentProductsPopulate`), unlike the grid click.
- Related: Add products activity `PRODUCT__CREATE`.
- Code: `Products.aspx.vb` `RecentProductsPopulate` 186–227. `Products.aspx` 652–655.
- Confidence: Confirmed
- Suggested KB title: Recently created products

### Export from the products page

- Pages: `Products.aspx`, `ExportReport.aspx` (opened, not fully audited)
- What it does (traced): The download image, tooltip “Download Product Report”, is always enabled. Click reads `LocationID_VIEW` and runs `ForceExport`, which sets the hidden fancybox link to `ExportReport?LocationID={id}` and clicks it. The search cookie is read into a local variable and is not added to that URL. Export Report shows “Download Product Report”, a location selector, and Download File. Checkboxes: “Include Products with 0 Quantity” (default off), “Include Products in Sub-Locations” (default off), Product Number (checked, disabled), Description (checked), Quantity (checked) with “breakdown by location” (checked, disabled when Quantity is unchecked), Buy Price, Cost Value, Sell Price (all checked), one checked box per custom field, and “Product Image” (default off). Download builds a CSV.
- Why: Take a spreadsheet of the catalog, optionally for one location.
- How to access and visibility conditions: Toolbar on both the editable and read-only products pages.
- Steps: Click download. Adjust the export page. Click Download File.
- Options and defaults: As listed. Location starts as the products view location. All Locations is -2, and the export SQL then uses `LocationID IS NOT NULL` unless sub-locations logic changes it.
- Permissions: No extra check on the products button. Export Report’s own user-type gate was not read.
- Validation/limits/failures: Not traced past the download response type `application/octet-stream`.
- Result and side effects: Products page does not write inventory. Export Report’s `sanitizeLocationPathAndReturnReadablePaths` updates `Locations.LocationPath` before the file is built. That write is outside the products page but runs when this button’s destination is used.
- Edge cases: The current search chips are not passed to Export Report. Printable mode hides `.clickable`, which includes this image button.
- Related: Import, columns.
- Code: `Products.aspx.vb` `btn_export_report_Click` 2144–2148. `Products.aspx` `ForceExport` 145–150, button 662. `ExportReport.aspx` 53–120. `ExportReport.aspx.vb` `ExportReport` 51–70, `loadCustomFields` 32–48.
- Confidence: Confirmed for the launch and the visible options. The CSV column order inside `DownloadFile` was not line-audited. Inferred that checked boxes become columns because `HeaderString` appends them.
- Suggested KB title: Download a product report

### Print barcodes from the list

- Pages: `Products.aspx`, `Products_read_only.aspx`, `PrintBarcode.aspx`
- What it does (traced): The print image is hidden until at least one row is checked (editable page: class `print-barcodes-hidden`; read-only: `hidden-btn`). Tooltip “Print barcodes for selected products”. A normal selection opens `PrintBarcode?SKU={comma-separated encoded numbers}` and does not send names. Select-all-complete writes cookie `SKU2PRINT` with every encoded product number, clears `NAME2PRINT`, and asks `confirm('You are about to print barcodes for all {count} products. This may take a moment. Continue?')` before `PrintBarcode?Batch=1`.
- Why: Print labels for the current selection.
- How to access and visibility conditions: Both products pages, after a selection.
- Steps: Check products. Click the barcode image. On the print page, pick label stock and PREVIEW & PRINT.
- Options and defaults: See Print barcode labels.
- Permissions: Both user types that can open a products page.
- Validation/limits/failures: Empty encoded list returns without opening the page. Cancel on the all-products confirm does not open it.
- Result and side effects: Cookies `SKU2PRINT` and, for a single-SKU editor launch, `NAME2PRINT`. No inventory change.
- Edge cases: A long query string is used for page selections. The all-products path uses a cookie because the list can be large. Names are looked up later if the name cookie is empty.
- Related: Editor print button.
- Code: `Products.aspx.vb` `btn_print_barcodes_Click` 2150–2169, `CheckedProductsGetEncodedForPrint` 2070–2095. `Products.aspx` `ForcePrintBarcodes` 152–162.
- Confidence: Confirmed
- Suggested KB title: Print barcodes for selected products

### Printable products page

- Pages: `Products.aspx`, `Products_read_only.aspx`, `UserPage.master`
- What it does (traced): An image titled “pritnable version” (spelled that way) runs `window.open('/Products?printable=true')`. The master page, when `printable=TRUE`, calls `makePrintable()`, which hides `.navbar` and `.clickable`. The profile-name popup is skipped in printable mode.
- Why: A quieter page for printing the grid.
- How to access and visibility conditions: Bottom of both products pages. The image uses class `clickable`, so the opened page hides it along with the toolbar buttons.
- Steps: Click the image. Use the browser print dialog yourself. This page does not call `window.print`.
- Options and defaults: None.
- Permissions: Opening `/Products` still redirects Read only to `Products_read_only`, and that URL does not keep `printable=true`. Inferred from the redirect `Response.Redirect("Products_read_only")` with no query string.
- Validation/limits/failures: None.
- Result and side effects: Display only.
- Edge cases: Read-only’s own printable image also opens `/Products?printable=true`, which sends a read-only user to the read-only page without the flag. Confirmed from the two code lines; the combined navigation was not run.
- Related: Grid.
- Code: `Products.aspx` 891. `UserPage.master` `makePrintable` 99–103. `UserPage.master.vb` 97–102. `Products.aspx.vb` 50–52.
- Confidence: Confirmed for each line. The read-only redirect dropping the flag is Inferred.
- Suggested KB title: Printable product list

### Product editor fields

- Pages: `ProductEditor.aspx`, `ProductEditor.aspx.vb`, `Controls/EDITABLE_FIELD.ascx`
- What it does (traced): Shows PRODUCT NUMBER as a label (`lbl_ProductNumber`), not an editable field. Then an editable Product Name. Then, in `AccountSettings.ProductFieldOrder`: Buy Price if account type is 0 and `ShowBuyPriceField`; Sell Price if account type is 0 and `ShowSellPriceField`; otherwise the custom field with that index. Custom fields with no presets are text boxes. Custom fields with presets are a dropdown: “(none)”, each preset, and the current value if it is not in the list. Currency fields reject non-numeric and negative input and show the field’s error label. Product name error text is “The Product Name is not valid!” but the name field is not marked numeric, and `SaveField` does not check that string. Buy price error: “The Buy Price is not valid!”. Sell price: “The Sell Price is not valid!”. A custom text field’s error string is “The field {name} is not valid!” and is likewise not used unless the field is numeric. Saving writes `UPDATE Products SET {column}` and activity `PRODUCT__EDIT` with “Changed '{label}' to '{value}'”, then reloads the editor and sets `COOKIE_PRODUCTS_PAGE_RELOAD` so the list can refresh.
- Why: Maintain the product’s name, prices, and custom attributes.
- How to access and visibility conditions: Row click, recent-products click, or `ProductEditor.aspx?ProductNumber=`. Buy/sell hidden when the account flags or account type say so. Admin sees “Edit your fields”, which calls `openCustomFieldEditor()`.
- Steps: Open the product. Edit the text and leave the field so the editable-field postback runs (`hidden_button_single_postback`). For a preset dropdown, change the selection. “(none)” stores an empty string. “Other (Specify)” opens a modal titled “Other (Specify):” with Cancel and Save. Save posts the typed text. Cancel restores the previous selection. Empty “Other” keeps the original value.
- Options and defaults: Field order and names come from account settings. Dropdown starts at the stored value, or “(none)” if the stored value is empty and not matched.
- Permissions: Not Read only. Read only gets disabled fields on the other page.
- Validation/limits/failures: Currency: not numeric or negative stops the save and shows the error label. No max length is enforced in `SaveField`. Preset dropdowns do not call `cfValueIsAllowed`; any typed “Other” value is saved.
- Result and side effects: Product row update and an edit activity. Does not change quantities.
- Edge cases: A custom value that is not in the preset list is added as an extra dropdown option so it stays visible. Product number cannot be renamed here. Account type 1 still shows custom fields; prices are omitted by `GetVisibleProductFieldOrderTokens` because account type must be 0.
- Related: Multi-edit, add products, import columns, editable-field control.
- Code: `ProductEditor.aspx.vb` `LoadFieldControls` 232–375, `GetVisibleProductFieldOrderTokens` 377–396, `_dropDownChanged` 559–623. `ProductEditor.aspx` other-specify modal 415–425, `saveOtherSpecifyModal` 156–163. `EDITABLE_FIELD.ascx.vb` `hidden_button_single_postback_Click` 331–372, `SaveField` product case 387–439.
- Confidence: Confirmed
- Suggested KB title: Edit product name, price, and custom fields

### Custom-field URL icon on the editor

- Pages: `Scripts/Pages/ProductEditor/ProductEditorCfUrlOpenLink.js`
- What it does (traced): For inputs whose id contains `EDITABLE_FIELD_CF_` and `_CTRL_TXT_`, and for preset `<select>` elements with class `multi_select`, a value that normalizes as a URL gets an “open in new tab” icon. Same URL rules as the grid pills.
- Why: Open a link stored in a custom field without leaving the editor by accident.
- How to access and visibility conditions: The script file is in `Scripts/Pages/ProductEditor/`. The editor markup was not re-checked for the script tag in this pass. If the page includes it, the icon appears when the value is a URL.
- Steps: Put a URL in a custom field. Use the icon.
- Options and defaults: None.
- Permissions: Whoever has the editor open.
- Validation/limits/failures: Non-URLs get no icon.
- Result and side effects: New tab only.
- Edge cases: Works for both text and preset dropdowns, including the narrow mobile editor class, according to the file header.
- Related: Grid URL pills.
- Code: `ProductEditorCfUrlOpenLink.js` 1–6, `normalizeUrl` 8–34, `isCustomFieldTextInput` 36–42.
- Confidence: Confirmed for the script. Uncertain that every editor skin includes the script tag, because that include line was not re-read.
- Suggested KB title: Open a link stored on a product

### Product image upload

- Pages: `ProductEditor.aspx`
- What it does (traced): The thumbnail tooltip is “Click to update image...”. Click runs `ForceFileUpload` and posts `FileUpload_image` through hidden `btn_upload_image`. The file is saved to a temp path and `imageProcessor.saveProductImage(productNumber, , , filePath)`. The page reloads. `GetResizedFile` can resize to at most 200×132 PNG, but `_upload_image` does not call it. Demo SKUs get an `onerror` image under `Images/Pages/Products/`. If a Lansweeper asset has an image URL, the thumbnail `onclick` and title are cleared so upload is not offered.
- Why: Attach a photo to the product number.
- How to access and visibility conditions: Editor sidebar. Hidden when Lansweeper supplies an image. Not present as an upload control on the read-only editor (read-only shows the image through `_getImage` and has no upload handler in its method list).
- Steps: Click the photo. Choose a file.
- Options and defaults: No size or type check in `_upload_image`.
- Permissions: Not Read only.
- Validation/limits/failures: No file means nothing happens. Exceptions from the image processor are not shown in this handler.
- Result and side effects: Replaces the stored product image and sets the products-page reload cookie. Clone copies this image onto the new product number when it can.
- Edge cases: The unused resize function is not the live path.
- Related: Add-products temp images, grid thumbnails.
- Code: `ProductEditor.aspx.vb` `_getImage` 157–170, `_upload_image` 668–687, `_linkToLansweeper` 38–68. `ProductEditor.aspx` 487.
- Confidence: Confirmed
- Suggested KB title: Change a product photo

### File attachments on a product

- Pages: `ProductEditor.aspx`
- What it does (traced): The paperclip tooltip is “Click to attach file...”. It posts `FileUpload_attachment`. The file name is split on the last period into name and extension. A row is inserted with `attachmentRepository.Insert` (`attachToProduct`, uid = product number) and `attachmentProcessor.upload` stores the temp file. Existing attachments are listed as a button `{name}.{extension}` (name truncated to 20 characters plus `...` when longer than 30) and a red X. The name button downloads with `Content-Disposition: attachment`. X asks `confirm('Are you sure you want to delete this attachment?')`, then `attachmentProcessor.deleteAttachment` and `repo.deleteByID`.
- Why: Keep files on the product.
- How to access and visibility conditions: Editor sidebar. Read-only `Page_Init` calls `_showAttachments` but its method list has `_downloadAttachment` and no `_deleteAttachment`, and the read-only markup that was scanned has attachment buttons without the delete handler. Read-only download is Confirmed by the method. Read-only upload is absent (no `_upload_attachment`).
- Steps: Click the paperclip. Choose a file. Click the chip to download. Click X and confirm to delete.
- Options and defaults: None. No extension allow-list and no size check in this handler.
- Permissions: Upload and delete require the editable editor.
- Validation/limits/failures: No file means no insert. Invalid file-name characters in a download are replaced with `_`.
- Result and side effects: Attachment rows and stored file bytes. Not the Documents / purchase-order feature.
- Edge cases: Names with several periods keep all but the last as the file name. The list query is `getByUid(uid, True, False, ...)`.
- Related: `DocumentEditor.aspx` is a different feature and is not opened from here.
- Code: `ProductEditor.aspx.vb` `_showAttachments` 70–113, `_downloadAttachment` 115–137, `_deleteAttachment` 139–156, `_upload_attachment` 690–730. `ProductEditor.aspx` `DeleteAttachmentConfirmation` 118–125, paperclip 522.
- Confidence: Confirmed
- Suggested KB title: Attach a file to a product

### Lansweeper link

- Pages: `ProductEditor.aspx`, `ProductEditor_read_only.aspx`
- What it does (traced): If `lansweeperAssetRepository.getByID` returns a non-empty URL, a Lansweeper image button is shown and opens that URL. The asset-type custom field is the one whose tags contain `LS_CF_ASSET_TYPE_NAME`, and its value picks a Lansweeper image that replaces the product photo and blocks upload.
- Why: Jump from a synced asset to Lansweeper.
- How to access and visibility conditions: Hidden unless that lookup succeeds. Failures are swallowed.
- Steps: Open a linked product. Click the Lansweeper image.
- Options and defaults: None on this page.
- Permissions: Both editor pages call `_linkToLansweeper`.
- Validation/limits/failures: Any exception hides the link.
- Result and side effects: A new window. No CyberStockroom write, except the image click is disabled when a Lansweeper image is applied.
- Edge cases: Only the first matching custom-field row is used.
- Related: Product image.
- Code: `ProductEditor.aspx.vb` `_linkToLansweeper` 38–68.
- Confidence: Confirmed
- Suggested KB title: Open a product in Lansweeper

### Expiration date

- Pages: `ProductEditor.aspx`, `AddProducts.aspx`, import, clone
- What it does (traced): If `SHOW_EXPIRATIONS` is on, the editor shows an EXPIRATION date input (`min=2018-01-01`, `max=2050-01-01`). It loads `GET https://code.cyberstockroom.com/api/expiration/CS_PRODUCT_IN_HEADER` with headers `X-CS-TOKEN` and `X-CS-PRODUCT-NUMBER`. The date is colored green when more than 60 days remain, gold at 60 days or fewer and still in the future, and red when the day difference is 0 or less. Changing the date POSTs `{Expirations:[{productUID, expirationDateTime}]}` to `https://code.cyberstockroom.com/api/expiration`. Clearing it sends DELETE to the product-header URL. Read-only shows the date disabled and does not write. Add Products shows `div_expirations` only when the flag is on and stores `EXP:{yyyy-MM-dd}` in the add-list cookie. Import accepts the same format and calls `ProductExpirations.Save` only for product numbers that were not already in the account. Clone copies the date onto the new product through the same API when the flag is on and the date box is non-empty.
- Why: Track a date on the product, separate from quantity.
- How to access and visibility conditions: User flag `SHOW_EXPIRATIONS`. The editor block starts `display:none` and is set to `block` in `LoadFieldControls`.
- Steps: Turn expirations on for the user. Open the product. Set or clear the date.
- Options and defaults: Warning window is 60 days in the editor script. No default date.
- Permissions: Read only can see and cannot edit.
- Validation/limits/failures: Import rejects any expiration that is not exactly `yyyy-MM-dd`: “Row {n}: Expiration must be a date such as 2026-12-31.” Add Products ignores an expiration that does not parse. API errors are only `console.log` in the editor.
- Result and side effects: Stored through the expiration API / `ProductExpirations`, not as a custom field. Deleting a product calls `ProductExpirations.Delete`.
- Edge cases: Existing products included in a create-import are not given the file’s expiration (`SaveCreatedExpirations`).
- Related: Clone, import, add products.
- Code: `ProductEditor.aspx` 664–782. `ProductEditor.aspx.vb` 368–374, `_setProductExpiration` 537–557. `AddProducts.aspx.vb` `ReadCachedExpiration` 278–295. `ImportFromFile.aspx.vb` 1859–1874 and `SaveCreatedExpirations` 1897–1916.
- Confidence: Confirmed
- Suggested KB title: Set a product expiration date

### Quantity on the product editor map

- Pages: `ProductEditor.aspx`
- What it does (traced): The right column loads `Map_CONTROL_2017` with `data--type-of-map="2"` (comment: Product Editor), `DisableMobileView=true`, `DisableMapStageLoader=true`. The header says “Click a location. Type new quantity. Press Enter.” A collapsed “Show details” tab toggles the field column. When the map raises `RefreshRequired`, the page sets cookie `CookieRefreshRequired=1` and reloads the editor. The read-only editor loads the same map control with `data--type-of-map="5"`.
- Why: See and change where the product is stocked.
- How to access and visibility conditions: Editor, right side. The actual click-to-edit behavior is inside the map control, which was not part of this read.
- Steps: Follow the on-page instruction. The map’s own steps are not traced here.
- Options and defaults: Initial map zoom cookie `COOKIE_CS_MAP_ZOOM=0.9` on first editor load.
- Permissions: Both editor variants host a map. Whether type 5 is view-only is Uncertain; the attribute differs and the map source was not read.
- Validation/limits/failures: Not in the editor code-behind.
- Result and side effects: A map refresh reloads the editor. Inventory writes happen in the map control or the inventory API, not in `ProductEditor.aspx.vb`.
- Edge cases: Clone does not copy location quantities (`InsertProductOnly` only).
- Related: Inline quantity on the list, check-in after create.
- Code: `ProductEditor.aspx` 818–841. `ProductEditor.aspx.vb` `MAP_CONTROL_1_RefreshRequired` 630–635, zoom cookie 187–189. Read-only map: `ProductEditor_read_only.aspx` 304.
- Confidence: Confirmed for the instruction and the refresh. Map edit rules are Uncertain.
- Suggested KB title: Change quantity on the product map

### Clone this product

- Pages: `ProductEditor.aspx`, `Scripts/Pages/ProductEditor/ProductEditorClone.js`
- What it does (traced): Two clone buttons (sidebar and map header), tooltip “clone this product”, open a “Clone Product” modal. Subtitle “Cloning: {current number}”. “New Product Number” has Auto checked by default, and the number box is disabled with placeholder “[Automatic Product Number]”. Unchecking Auto requires a number. Client warnings: “You must enter a product number.” and “That product number already exists!” The exists check is `GET https://code.cyberstockroom.com/api/products/CS_PRODUCT_IN_HEADER` with the token and product-number headers; HTTP success means it exists. The modal lists the same visible fields as the editor, prefilled from the current inputs, including preset dropdowns, “(none)”, and an extra “Other (Specify)” option. If expirations are on, the expiration date is copied into a date input. Clone posts hidden fields and `btn_clone_product_Click`.
- Why: Create a new product number from an existing one without copying stock.
- How to access and visibility conditions: Editable editor only. The old toolbar button that called `CloneProduct()` is commented out. Read only is redirected away before this markup is used. `Popups/CloneProduct.aspx` is a separate unused form.
- Steps: Open clone. Leave Auto on or type a new number. Adjust copied fields. Clone.
- Options and defaults: Auto on. Empty product name is replaced with the new product number. Missing buy/sell become 0. Custom fields not in the payload are stored as empty strings.
- Permissions: Not Read only. The popup page also blocks Read only, but it is not the live button.
- Validation/limits/failures: Blank manual number or a number that already exists stays in the modal. The server also exits without a message if the number is blank or `Product.ProductExists` is true. Auto SKU uses `GetNextAutoSKU`.
- Result and side effects: `InsertProductOnly` inserts the product (`INSERT IGNORE`) and records `PRODUCT__CREATE`. It does not insert quantities or locations. The source image is copied when `saveProductImage` succeeds; failures are ignored. Expiration is posted for the new number. Cookie `COOKIE_PE_CLONED_BADGE` shows a “new” badge once. The editor redirects to the new product. Attachments are not copied (no attachment call in the clone handler).
- Edge cases: The client “already exists” check treats any HTTP error as “does not exist”. A network failure could let a duplicate through to the server, which then exits quietly. Auto placeholder text is not the saved number; the server generates `CSN-` plus a zero-padded index.
- Related: Add products auto number, `Popups/CloneProduct.aspx`.
- Code: `ProductEditor.aspx` 427–455 and 473–475. `ProductEditorClone.js` `open` 212–251, `submit` 264–321. `ProductEditor.aspx.vb` `BuildCloneFieldMetadata` 398–464, `btn_clone_product_Click` 466–535. `Product.vb` `InsertProductOnly` 191–220, `GetNextAutoSKU` 246–255.
- Confidence: Confirmed
- Suggested KB title: Clone a product

### Delete this product

- Pages: `ProductEditor.aspx`
- What it does (traced): A trash button, tooltip “Delete this product”, opens “Delete this product?” with the sentence “Deleting this product will also check it out of all locations on the map.” Cancel closes the modal. Delete calls `Product.DeleteProducts` for that one number, sets the reload cookie, tries to close the parent fancybox, and then redirects to `ProductEditor.aspx?ProductNumber={same number}`.
- Why: Remove one product from its editor.
- How to access and visibility conditions: Bottom of the field column on the editable editor. Not on the read-only editor (no `btn_delete2` in that code-behind).
- Steps: Click the trash icon. Click Delete.
- Options and defaults: None.
- Permissions: Not Read only.
- Validation/limits/failures: Cancel does nothing.
- Result and side effects: Same `DeleteProducts` path as the grid, including expiration delete. The redirect targets the deleted number, and `Page_Init` sends unknown products to `Product Error.html`.
- Edge cases: The modal copy says quantities are checked out of every location. That outcome depends on `productDeleter`, whose body was not in the searched source. The older `_DeleteProduct` does delete quantity rows.
- Related: Grid delete.
- Code: `ProductEditor.aspx` 402–412, 103–116, 801. `ProductEditor.aspx.vb` `btn_delete2_Click` 732–738 and missing-product redirect 196–198.
- Confidence: Confirmed for the click path. Uncertain for every child row the deleter removes.
- Suggested KB title: Delete one product

### Print barcode from the editor

- Pages: `ProductEditor.aspx`, `ProductEditor_read_only.aspx`
- What it does (traced): The print image tooltip is “Print Barcodes”. The link is `PrintBarcode?SKU={encoded number}&Name={encoded name}`. `OnClientClick` returns false so the image button does not post the form; the anchor opens the fancybox. `PrintBarcode.aspx.vb` stores those cookies when there is a single SKU.
- Why: Print a label for the open product, including its name.
- How to access and visibility conditions: Both editor variants.
- Steps: Click the print image. Continue on the print page.
- Options and defaults: One label for this product.
- Permissions: No extra check on the editor button.
- Validation/limits/failures: None on the link.
- Result and side effects: Cookies only, until the user prints.
- Edge cases: A name that contains characters the URL encoder changes is decoded again on the print page.
- Related: Grid print, label stock.
- Code: `ProductEditor.aspx.vb` 235. `ProductEditor.aspx` 524–526. `PrintBarcode.aspx.vb` `Page_Init` 19–33.
- Confidence: Confirmed
- Suggested KB title: Print a barcode from the product page

### Read-only product editor

- Pages: `ProductEditor_read_only.aspx`
- What it does (traced): Same product lookup and missing-product redirect. Product name, prices, and custom text fields are constructed with `isEnabled=False`. Preset dropdowns are `Enabled=False`. Expiration input is `disabled`. Print, attachments download, Lansweeper, and a map (`data--type-of-map="5"`) remain. There is no clone handler, no delete button, no image upload, and no attachment upload in this code-behind. Non-read-only users are sent to `/ProductEditor`.
- Why: Let a read-only user inspect a product.
- How to access and visibility conditions: Automatic from the read-only grid, or if a read-only user hits the editable editor URL.
- Steps: Open a product from the read-only list.
- Options and defaults: Same visible fields as the editable editor, including the buy/sell flags.
- Permissions: `TypeOfUser = READ_ONLY` only.
- Validation/limits/failures: Disabled fields do not post saves through the text box (`Textbox.Enabled = False`).
- Result and side effects: No product write from the field controls. Map type 5 was not traced.
- Edge cases: `HANDLER_FIELD_EDITED` still exists and would reload the read-only editor if some other control raised it.
- Related: Read-only grid.
- Code: `ProductEditor_read_only.aspx.vb` `Page_Init` 26–32, `LoadFieldControls` 190–243, dropdown `Enabled = False` 259. `EDITABLE_FIELD.ascx.vb` 218–219.
- Confidence: Confirmed
- Suggested KB title: View a product without editing it

### Add products form

- Pages: `AddProducts.aspx`, `AddProducts.aspx.vb`
- What it does (traced): Title area is the create form. Fields, in `ProductFieldOrder`: PRODUCT NUMBER with AUTO checked; DESCRIPTION; then buy price, sell price, and custom fields that are visible. Preset custom fields are dropdowns with “(none)” and the presets. AUTO uses `GetNextAutoSKU` (`CSN-` plus a 9-digit index from the highest existing `CSN-` number). An empty description becomes the product number. Empty prices stay 0. Non-empty prices must be numeric and greater than or equal to 0 or the box is marked `lbl-error-numeric` and the add stops. A manual number that is blank shows placeholder “No Poduct Number!” (spelled that way). `ProductNumberExists` is a page method: “Product number already exists” or the box can show “Could not verify product number”. Account type 1 disables both price boxes. Admin sees “Edit your fields”. Expirations appear only when the user flag is on. The client builds an `ADD_LIST` cookie of lines separated by `||`. Save reads that cookie.
- Why: Type products in by hand instead of using a file.
- How to access and visibility conditions: From the products add button (`LastPage=Products`), from Product Selector “+ New Products” (`/Start?add=true` on the parent), and from import’s Go Back. Read only is unauthorized. Query `MobileTransferSingleAdd=1` changes the title to “Add Product”, hides the multi-add path, and posts the parent a `csMobileTransferAddProductSaved` message instead of opening check-in. Query `keepAddList=1` does not clear the add-list cookie.
- Steps: Leave AUTO on or type a number. Fill description and other fields. Add the row (client). Repeat. Save. The server creates the new products and, unless this is the single mobile-transfer add, redirects to `CheckInCreatedProducts.aspx`. If the add was started from a transfer return, it redirects back to the transfer with the batch staged.
- Options and defaults: AUTO checked. Quantity stored on each new `ProductDetails` is 1 (`P.Quantity = 1`), not typed on this form. Buy and sell default 0.
- Permissions: Not Read only. Prices hidden in the UI for account type 1 and when the show-price flags are off, same as the editor.
- Validation/limits/failures: Duplicates of an existing product, or a number already accepted in this batch, are skipped (`Continue For`). If every line is skipped and `LastPage=getting-started`, onboarding status is set to `finalize` and the parent goes to `/pages/guides/getting-started`. If the list cookie is missing, Save exits. Numeric price failure does not submit.
- Result and side effects: `CreatedProductCheckIn.CreateNewAndStage` inserts products that do not exist (`CreateProducts`, `INSERT IGNORE`), writes a check-in batch cookie, and sets the products reload cookie. `CreateProducts` also calls `ListProducts`, which inserts `Quantities` rows for location `-2` without a quantity column. Images cached for the batch are copied from temp files by thumbnail index. Expirations in the cookie are saved after create. The check-in page is where stock is actually added.
- Edge cases: Save does not update an existing product’s name or prices; it skips that number. The form does not ask for a location. Mobile single-add still creates the product and does not stage the check-in redirect.
- Related: Import, check-in, auto SKU, images.
- Code: `AddProducts.aspx.vb` `LoadDynamicInputs` 46–262, `btn_save_Click` 297–440, `ProductNumberExists` 442–466. `AddProducts.aspx` `beginAddProduct` 892–969. `Product.vb` `GetNextAutoSKU` 246–255, `CreateProducts` 139–189, `ListProducts` 222–238. `CreatedProductCheckIn.vb` `CreateNewAndStage` 26–64.
- Confidence: Confirmed
- Suggested KB title: Create products by typing them in

### Product image while adding

- Pages: `AddProducts.aspx`
- What it does (traced): `btn_upload_Click` stores `FileUpload1` in a temp file and `imageProcessor.saveProductImage` with the temp flag and a thumbnail index. The thumbnail src becomes `getTmpProductImage`. On first load of a new add session (`keepAddList` not `1`), temp images are cleared. On save, `copyProductImagesFromTmp` copies them onto the new product numbers in list order.
- Why: Set the photo before the product exists.
- How to access and visibility conditions: The thumbnail on the add form. Read only cannot open the page.
- Steps: Click the thumbnail, choose a file, then save the product list.
- Options and defaults: Index comes from `hidden_thumbnail_index` or, when `data_edit_index > 0`, that index plus 1.
- Permissions: Not Read only.
- Validation/limits/failures: No file means no change. No type or size check in this handler.
- Result and side effects: Temp file, then the product image after save.
- Edge cases: Leaving without save can leave temp files until the next fresh visit clears them.
- Related: Editor image upload.
- Code: `AddProducts.aspx.vb` `Page_Init` 37–39, `btn_upload_Click` 531–561, `SaveCachedImages` 505–514.
- Confidence: Confirmed
- Suggested KB title: Add a photo while creating a product

### Check in products you just created

- Pages: `CheckInCreatedProducts.aspx`, `CheckInCreatedProductsDone.aspx`
- What it does (traced): Reads the batch cookie. If there is no batch: “No products are waiting to be checked in.” and the map column is hidden. Otherwise the title is “{n} Product(s) created.” and the map title is “Click a location to Check it in.” or “Click a location to Check them in.” Each row shows the name, the product number when it differs, and a quantity box defaulting to the staged quantity (1 from Add Products, or the file quantity). Max length 9, numeric input. Up/down buttons change it. If any product number was auto-generated, a line says “{n} product number(s) was/were generated.”
- Why: New product records have no stock until this step, except the location `-2` quantity row inserted by `ListProducts`.
- How to access and visibility conditions: Redirect after Add Products save or after a create-import, unless the flow is returning to Transfer. Read only is unauthorized. The user’s `CheckInLocationDefault` is preselected when it exists and is not -2. Query `loc` overrides that when the location exists.
- Steps: Adjust quantities. Click a location on the map (map control; the page stores `hidden_locationID`). Confirm. A comment modal asks “Any comments about this transaction?” Cancel returns to the form. The action button reads “Skip Comment” until there is text, then “Save”. That posts `btn_checkin`. Or “Skip check-in”, which closes the modal and reloads the parent without calling `SaveCheckIn`.
- Options and defaults: Quantity defaults from the batch. Comment is optional and empty.
- Permissions: Not Read only.
- Validation/limits/failures: “Each quantity must be a whole number, 0 or greater.” (`e=qty`). “Select a location on the map before checking in.” (`e=location`). “Enter a quantity of at least 1 for one product.” (the `Case Else`, used for `e=none`). “A location in this import could not be found.” (`e=loc`). Lines with quantity 0 are omitted. If every remaining line is omitted, check-in returns false and the none-error is shown.
- Result and side effects: `SaveCheckIn` adds the quantity onto the chosen location (`Quantity = Quantity + new`), it does not replace it, and records `INVENTORY__CHECK_IN` with an optional comment. A file import’s comment is passed through `AppendFileImportTag`. The batch cookie is expired. `CheckInCreatedProductsDone.aspx` closes the fancybox or mobile modal and reloads the parent. If it is not in a frame, it goes to `/Products.aspx`.
- Edge cases: Products are already created before this page. Skip leaves them with no check-in. Negative quantities are rejected. Imported per-line locations hide the map; see Import.
- Related: Add products, import, transfer return.
- Code: `CheckInCreatedProducts.aspx.vb` `Page_Init` 13–88, `btn_checkin_Click` 185–243, `ShowQueryError` 265–282, `BuildRow` 326–383. `CheckInCreatedProducts.aspx` comment modal 899–906, skip 867. `CreatedProductCheckIn.vb` `SaveCheckIn` 232–275. `Product.vb` `UpdateProductLocationQuantity` 638–646. `CheckInCreatedProductsDone.aspx` 18–61.
- Confidence: Confirmed
- Suggested KB title: Check in products after you create them

### Check-in when the file named locations

- Pages: `CheckInCreatedProducts.aspx`
- What it does (traced): If every staged line has `LocationId` other than -2, and this is not a return to Transfer, the map is hidden. Each row shows the location path. The quantity tooltip is “This quantity will be checked in to this location.” Save calls `SaveCheckInAtLineLocations`, which adds each line’s quantity at that line’s location in one check-in activity. A missing location fails the whole save and shows `e=loc`.
- Why: A create-import can place stock without picking one map location.
- How to access and visibility conditions: Only when every product in the batch has a resolved location. One missing location id (`-2`) turns the map back on for the whole batch (`BatchUsesImportedLocations`).
- Steps: Review paths and quantities. Continue through the comment modal.
- Options and defaults: Quantities from the file, or 1 when the quantity column was not mapped.
- Permissions: Same as check-in.
- Validation/limits/failures: Same quantity rules. Any line with quantity >= 1 and a bad location aborts the entire check-in.
- Result and side effects: Additive quantities at each named location. Zero lines are skipped. If all are zero, nothing is checked in.
- Edge cases: Duplicate product numbers in the create file are rejected before this page. `MergeProducts` would add quantities if duplicates ever reached it.
- Related: Create import location column.
- Code: `CheckInCreatedProducts.aspx.vb` `BatchUsesImportedLocations` 98–108, `ApplyImportedLocationChrome` 90–96, `SaveImportedLocationCheckIn` 284–324. `CreatedProductCheckIn.vb` `SaveCheckInAtLineLocations` 281–308.
- Confidence: Confirmed
- Suggested KB title: Check in imported products to the locations in the file

### Return to a transfer after creating products

- Pages: `CheckInCreatedProducts.aspx`, `AddProducts.aspx`, `ImportFromFile.aspx`
- What it does (traced): When the create flow was opened with a stored transfer return, the check-in map is hidden. Title: “{n} Product(s) was/were created. Set the quantity, then continue.” Buttons: “Skip ››” and “Continue”. Skip expires the batch and the import transfer cookies and returns to the transfer without applying the new lines. Continue requires the same quantity rules, updates the batch quantities, and returns to the transfer with the apply flag. The products are already created.
- Why: Add items in the middle of a transfer and send them back to that transfer.
- How to access and visibility conditions: `CreatedProductCheckIn.IsReturnToTransfer` / `IsStoredReturnToTransfer`. Create-import also hides the location column in that case (`CreateImportShowsLocation` is false).
- Steps: Create or import. Set quantities. Continue or Skip.
- Options and defaults: Staged quantity 1 from Add Products.
- Permissions: Not Read only.
- Validation/limits/failures: `e=qty` and `e=none` are redirected back with the transfer query string.
- Result and side effects: Does not call `SaveCheckIn` on this page. The transfer page is expected to apply the batch. That transfer page was not audited here.
- Edge cases: A single mobile transfer add (`MobileTransferSingleAdd=1`) posts a message to the parent and does not use this page.
- Related: Product selector transfer, import.
- Code: `CheckInCreatedProducts.aspx.vb` `ApplyReturnModeChrome` 126–132, `btn_skip_return_Click` 134–139, `btn_continue_transfer_Click` 141–183. `ImportFromFile.aspx.vb` `CreateImportShowsLocation` 307–309.
- Confidence: Confirmed for this page. What the transfer page does with the return flag is Uncertain.
- Suggested KB title: Send newly created products back to a transfer

### Import a file — shared rules

- Pages: `ImportFromFile.aspx`, `CSV_Class.vb`
- What it does (traced): The page title flow is upload, then “Drag from left to right to Match the fields.” Sample links depend on the mode. Go Back (`btn_cancel`) returns to Add Products, or Product Selector with the type, or the transfer. Next (`btn_save`) is hidden until a file is stored. If some product numbers already exist, Next is hidden and Continue (`btn_confirm_existing`) is the second step. That second step is only on the create path.
- Why: Map spreadsheet columns onto CyberStockroom fields without requiring a fixed header row.
- How to access and visibility conditions: Add Products import button goes to `ImportFromFile.aspx?LastPage=AddProducts` (create mode, because `CREATE_NEW` defaults to true). Product Selector has “Import From File” (`CREATE_NEW=FALSE`) and “OR Import from File with Locations” (`CREATE_NEW=FALSE&LOCATION_REQUIRED=TRUE`), plus `&Type=`. Read only is unauthorized.
- Steps: Choose a CSV. Drag column chips onto field chips. Click a matched field to clear it. Next.
- Options and defaults: Unmatched slots stay `-1`. A remembered column map is applied for create imports and for transfer match imports when headers match a saved map. Match-field and location-key choices are stored in cookies `IMPORT_MATCH_FIELD` and `IMPORT_LOCATION_KEY`.
- Permissions: Not Read only. “Edit your fields” on the create field list is Admin only, and the custom-field modal is hidden when `CREATE_NEW` is false.
- Validation/limits/failures: “This file is empty.” “This file is too large. Use a CSV smaller than 250 KB.” (size must be `< 250000`). “This file is not a CSV. Save it as a comma-separated CSV and try again.” “This file is not valid UTF-8. Save it as CSV UTF-8 and try again.” “This file uses semicolons between columns. Save it as a comma-separated CSV and try again.” “This file has more than 100 columns. Remove the extra columns and try again.” “Row {n} could not be read. Check the quotes and try again.” “This file has no products.” “This file could not be read. Save it as CSV UTF-8 and try again.” “You must select at least a Product Number to upload.” when the column cookie is missing or still all `-1`. “The column matching could not be read. Match the fields again.” A ragged row on create, and on non-transfer imports, stops the file: “Row {n} has {c} columns and the header has {h}.” BOM is stripped. Blank rows are skipped. Quoted commas are supported (`HasFieldsEnclosedInQuotes`). Header is the first non-blank row. `TrimWhiteSpace` is false.
- Result and side effects: The parsed table is stored server-side (`StoreTable`) until import or cancel. No inventory write until Next succeeds.
- Edge cases: The first row is always a header, never a product. A header-only file is “This file has no products.”
- Related: The four sample files.
- Code: `ImportFromFile.aspx.vb` `UploadFile` 159–227, `clearErrors` 433–444, `RunImport` 454–476, `btn_cancel_Click` 765–793. `CSV_Class.vb` `ParseUpload` 29–105, `MaxColumns` 27. `ImportFromFile.aspx` samples 1162–1175, buttons 1056–1061.
- Confidence: Confirmed
- Suggested KB title: Upload a product CSV

### Import to create products

- Pages: `ImportFromFile.aspx`
- What it does (traced): Default mode (`CREATE_NEW` not `FALSE`). Sample `Samples/Products.csv` header: `Product Number, Product Name, Buy Price, Sell Price, Manufacturer, Supplier`. The matcher does not require those header names. Slots, in order: Product Number; Description; Buy Price (only if account type 0 and `ShowBuyPriceField`, labeled with currency, marked numeric); Sell Price (same flags); each custom field in `AccountSettings.CustomFields` order (not `ProductFieldOrder`); Quantity (optional chip, tip “You can include a quantity column to use during Check In”); Expiration if `SHOW_EXPIRATIONS` (tip “A date like 2026-12-31 (year-month-day).”); Location # if not returning to a transfer (tip “You can include a location column to check these products into those locations.”). Location # can be switched to Location Name.
- Why: Create many products, and optionally stage quantities and locations.
- How to access and visibility conditions: Add Products “import” button, or `ImportFromFile.aspx` with `CREATE_NEW` omitted or not `FALSE`.
- Steps: Upload. Match at least one column (a completely unmatched file is rejected). Next. If any product number already exists, review the notice and Continue.
- Options and defaults: Unmapped product number generates `CSN-` numbers (`autoSkuCount` is shown later). Unmapped description stays empty and `CreateNewAndStage` then copies the product number into the name. Unmapped buy/sell stay 0. Unmapped custom fields stay empty. Unmapped quantity stays 1. Unmapped location stays -2, which means “no imported location”.
- Permissions: Price slots hidden with the same flags as the editor. Expiration slot hidden without the user flag. Location slot hidden on a transfer return. Admin field-editor link only.
- Validation/limits/failures: Mapped product number, description, price, custom field, quantity, expiration, or location cell missing because the row is short: “Row {n} has {c} columns and a mapped column is past the end of the row.” Product number longer than 255: “Row {n}: Product number is longer than 255 characters.” Description longer than 255: “Row {n}: Description is longer than 255 characters.” Custom field longer than 255: “Row {n}: {field} is longer than 255 characters.” Buy/sell: “Row {n}: Buy Price must be a number such as 12.50.” and the sell equivalent. Empty price becomes 0. Commas, `$`, and `e`/`E` are rejected. A leading minus is allowed by the price regex. Quantity: “Row {n}: Quantity must be a whole number such as 1 or 1.00.” Empty, negative, or a non-integer decimal fails. `1.00` passes. Expiration: “Row {n}: Expiration must be a date such as 2026-12-31.” Blank expiration is allowed. Duplicate numbers in the file: “Product number "{n}" is used on {count} rows.” plus “Remove the duplicate and try again.” and each row number. No data rows after blanks: “This file has no products.” Location blank: “Row {n}: the location # is blank.” or “location name”. Unknown location: “Row {n}: location # "{value}" could not be found.” Location names match case-insensitively; if several locations share the name, the lowest id is used. If the file or the matching changes after the existing-product warning: “The file or column matching changed. Review the import and try again.”
- Result and side effects: New numbers are inserted. Existing numbers are not updated: the notice says “Existing products keep their description, price, and custom fields. Their quantity is staged for check-in. New products are created from this file.” The UI says “{n} product already exists” or “{n} products already exist” and lists `Row {n}: {product number}`. Expirations are saved only for numbers that were not already in the account. Quantities are not written to locations on this page. They are staged and added during check-in (additive). If every line has a location, check-in uses those locations. Otherwise the user picks one location and the staged quantities are added there. `CreateProducts` still inserts a `Quantities` row at location `-2` for each new product, without a quantity value in the INSERT.
- Edge cases: A mapped quantity of 0 is staged and then omitted at check-in. Custom fields are matched in account custom-field list order, which can differ from the editor’s `ProductFieldOrder`. Preset lists are not validated on import; any text up to 255 characters is stored. The sample’s Manufacturer and Supplier columns are only examples; they map only if the user drops them on custom fields that happen to use those names.
- Related: Check-in, samples, add products.
- Code: `ImportFromFile.aspx.vb` `PopulateFieldsList` 230–271, `BuildCreateImport` 1710–1895, `TryParseImportPrice` 1929–1942, `TryParseImportQuantity` 1944–1958, `SaveCreateImport` 1657–1708, `ShowExistingProductsNotice` 1987–2009, `CreateLocationResolveError` 1111–1144, `TryGetLocationIdFromName` 1173–1207. `CreatedProductCheckIn.vb` `CreateNewAndStage` 26–64, `MergeProducts` 358–395.
- Confidence: Confirmed
- Suggested KB title: Import a spreadsheet to create products

### Import for check-in or check-out (no new products)

- Pages: `ImportFromFile.aspx`, `ProductSelector.aspx`
- What it does (traced): `CREATE_NEW=FALSE`. Sample without locations: `Samples/ProductList.csv` header `Product Number, Quantity`. With locations: `Samples/ProductListLocation.csv` header `Product Number, Quantity, Location`. Fields: Product Number, Quantity (required numeric), and Location # when `LOCATION_REQUIRED=TRUE`. Quantity must pass `CheckIfColumnNumeric` or the label “The selected field must be numeric!” is shown. This mode does not call `BuildCreateImport` and does not insert products. It fills `ProductDetails` and writes start-page cookies (`START_ListOfProducts`, quantities, locations) plus `SELECTOR_PROCEED=TRUE`, then closes the parent fancybox. Blank product numbers are replaced with auto SKUs unless this is an alternate-identifier transfer match.
- Why: Load a list of existing items into Check In, Check Out, or Transfer.
- How to access and visibility conditions: Product Selector import links. Type query is CHECKIN, CHECKOUT, or TRANSFER.
- Steps: Start a check-in, check-out, or transfer. Import. Match product number and quantity. Match location if that link was used. Next.
- Options and defaults: Location key defaults to barcode (“Location #”), cookie-remembered, and can be “Location Name”.
- Permissions: Not Read only.
- Validation/limits/failures: Quantity column must be mapped and numeric for the non-transfer path. Location names that do not match fail the file with “Row {n}: the location name is blank.” or “Row {n}: location name "{value}" could not be found.” Transfer rows are validated per row instead of failing the file (next feature). Ragged rows fail the file when it is not a transfer match import.
- Result and side effects: No product create and no quantity write inside ImportFromFile. The cookies are for the page that opened the importer. For a non-transfer return, the fancybox closes. What Start or Product Selector does with `SELECTOR_PROCEED` was not traced in this audit.
- Edge cases: `ProductFillIn` for a non-create quantity assigns `P.Quantity = NewValue` with no integer check beyond the earlier column numeric test. `IsNumeric` allows decimals. Create mode is stricter. Location ids are resolved with `getIDFromBarcode` unless the key is NAME.
- Related: Product selector, transfer import.
- Code: `ImportFromFile.aspx.vb` `PopulateFieldsList` else branch 272–287, `RunImport` 503–601, `ProductFillIn` 677–762, `CreateStartPageCookies` 621–676. `ProductSelector.aspx` 99 and 152. `ProductSelector.aspx.vb` 27–28.
- Confidence: Confirmed for the import page. The consuming check-in screen after `SELECTOR_PROCEED` is Uncertain.
- Suggested KB title: Import a list into check-in or check-out

### Import into a transfer

- Pages: `ImportFromFile.aspx`
- What it does (traced): `CREATE_NEW=FALSE`, `LOCATION_REQUIRED=TRUE`, `Type=TRANSFER`, `ReturnPage=TRANSFER`. Sample `Samples/ProductListLocationTransfer.csv` header: `Product Number, Quantity, FROM, TO`. Fields: an identifier (default Product Number), Quantity, FROM (Location #), TO (Location #). The identifier dropdown (`BindMatchFieldOptions`) is Product Number (`PN`), Description (`DESC`), and each custom field (`CF_{index}`). The choice is remembered. Location chips can switch to Location Name. A transfer match import does not reject the whole file for a ragged row; that row is skipped: “Row {n}: this row has {c} columns and the header has {h}, so it was skipped.” Other bad rows are also skipped into `IMPORT_COMMA_SKIPS` (the helper name is `AppendTransferImportRow`). Quantity must be mapped or “The selected field must be numeric!” is shown. After a successful run the page redirects back to the transfer with `ApplyImportedTransfer=1`, source, destination, map filter, check-in/out flags, and `MatchField`.
- Why: Move many items between locations from a spreadsheet.
- How to access and visibility conditions: Only when the return page is TRANSFER. The match-field chevron is on field 0 in that mode.
- Steps: Match the identifier, quantity, from, and to. Next.
- Options and defaults: Identifier defaults to Product Number. Location key defaults to barcode.
- Permissions: Not Read only.
- Validation/limits/failures: Per-row skips include identifier length over 255 (`AppendTransferImportRow` 840). Location name misses use “FROM location name” or “TO location name”. Unmatched location names are checked before the row loop when the key is NAME. The exact skip strings inside `AppendTransferImportRow` beyond the length and ragged-row messages were not all copied in this pass; the function starts at line 829.
- Result and side effects: Does not create products and does not update quantities in this page. It stores the accepted rows the same way as the other non-create import (`CreateStartPageCookies`) and returns to the transfer. Column map is saved with `SaveTransferColumnMap`.
- Edge cases: Description or custom-field matching must not invent a product number for a blank identifier cell (`IsAlternateIdentifierMatch`). A blank product-number match still gets an auto SKU.
- Related: Check-in import, product selector transfer.
- Code: `ImportFromFile.aspx.vb` `IsTransferMatchImport` 923–933, `BindMatchFieldOptions` 935–942, `RunImport` transfer branch 503–598, `AppendTransferImportRow` 829, `GetTransferReturnPagePath` 811. Sample link: `ImportFromFile.aspx` 1174–1175.
- Confidence: Confirmed for the mode, fields, and redirect. Individual skip messages inside `AppendTransferImportRow` after line 829 are Confirmed only for the length check at 840 and the ragged-row skip at 554. Other skip texts in that method were not re-read line by line. Mark those other skip strings Uncertain until that method is quoted.
- Suggested KB title: Import a transfer list

### Sample CSV headers

- Pages: `Samples/*.csv`, linked from `ImportFromFile.aspx`
- What it does (traced): The files are examples. The importer uses whatever headers are in the upload and lets the user match them. It does not require these names.
- Why: Show a starting layout.
- How to access and visibility conditions: “Sample CSV File” link for the active mode.
- Steps: Open the link. The target is `_blank`.
- Options and defaults: Create → `Products.csv`: `Product Number, Product Name, Buy Price, Sell Price, Manufacturer, Supplier`. Check-in/out → `ProductList.csv`: `Product Number, Quantity`. With location → `ProductListLocation.csv`: `Product Number, Quantity, Location`. Transfer → `ProductListLocationTransfer.csv`: `Product Number, Quantity, FROM, TO`.
- Permissions: Static files.
- Validation/limits/failures: None.
- Result and side effects: None.
- Edge cases: Manufacturer and Supplier in the create sample are not built-in fields. They only import if matched to custom fields.
- Related: Import modes.
- Code: sample links `ImportFromFile.aspx` 1162–1175. Headers are the first lines of the four files.
- Confidence: Confirmed
- Suggested KB title: Sample product CSV files

### Print barcode labels

- Pages: `PrintBarcode.aspx`, `BarcodePngGenerator.vb`
- What it does (traced): Title “Print Barcode Labels”. Dropdown LABEL STOCK defaults to `30252 (1-1/8" × 3-1/2")`. Other items: `30336 (1" × 2-1/8")`, `30334 (2-1/4" × 1-1/4")`, `30330 (3/4" × 2")`. PREVIEW & PRINT builds one label per SKU: decoded product name, a Code 128 PNG, and the product number. If the name cookie is missing, the name is loaded from the product, or “UNTITLED”. Preview opens a window with a PRINT BARCODE button and `@page` size from the stock. The page recommends a DYMO LabelWriter 450 and links to an Amazon product URL. `?Batch=1` skips the query-string cookie write and uses the cookie already set. A comma in `SKU` clears the name cookie so mixed names are not applied to every label.
- Why: Print scan labels on common DYMO stock.
- How to access and visibility conditions: Fancybox from the grid or the editor. No read-only redirect in this page’s init.
- Steps: Choose stock. PREVIEW & PRINT. In the new window, PRINT BARCODE, then the browser print dialog.
- Options and defaults: Stock `30252`. Generator specs: 30252 is 3.5 × 1.125 in with bar height 0.56 in; 30336 is 2.125 × 1.0 in, bar 0.48; 30334 is 2.25 × 1.25 in, bar 0.62; 30330 is 2.0 × 0.75 in, bar 0.26. DPI 203. Quiet zones 10, 8, 9, and 6 modules. Print size is the stock minus 0.0625 in width and 0.125 in height. Unknown stock ids fall back to 30252. Format is ZXing `CODE_128`, `PureBarcode=true`.
- Permissions: Uses the master account from the request. No type check in this file.
- Validation/limits/failures: Empty value returns an empty image. A thrown exception in preview is swallowed. An empty SKU cookie produces no labels.
- Result and side effects: Images in the page. No database write in these two files.
- Edge cases: The on-screen CSS sizes (for example 30252 at 3.4375 × 1 in) are not the same numbers as the generator’s physical stock (3.5 × 1.125). The print window’s `@page` uses yet another pair (`3.5in 1.125in` for 30252). Confirmed from the three definitions.
- Related: Grid and editor print buttons.
- Code: `PrintBarcode.aspx` 185–210 and `PreviewDiv` 21–45. `PrintBarcode.aspx.vb` `PrintBarcodeBatch` 85–115, `ResolveProductName` 177–190. `BarcodePngGenerator.vb` `GetLabelSpec` 42–57, `GenerateCode128Base64` 59–84.
- Confidence: Confirmed
- Suggested KB title: Print barcode labels

### Product selector

- Pages: `ProductSelector.aspx`, `ProductSelector.aspx.vb`, `Scripts/Popups/ProductSelector/ProductSelector_v2.js`
- What it does (traced): Query `Type` sets the screen. CHECKIN: title “Check In”, subtitle “Add Products to a Location”, instruction “Please select a Check In Location.”, default `CheckInLocationDefault`. CHECKOUT: “Check Out”, “Remove Products from a Location”, “Please select a Check Out Location.”, default `CheckOutLocationDefault`. TRANSFER: “Transfer”, “Move Products between Location”, “Please select a Source Location for the Transfer.” After a source is chosen, the instruction becomes “Please select a Destination Location for the Transfer.” The same location twice shows “The Source can't be the Destination! Please select a Destination.” When source and destination are different, or both are in the query string `Source` and `Destination`, the location picker hides and the selection panel shows. The panel has “Search or scan...”, a clear X, “+ New Products” (parent `/Start?add=true`), “Import From File”, and a Select button (`btn_save`) that is hidden until something is selected (`SignalNext` and `parent.$.fancybox.close()`). Cookie `forceLocationID` skips the picker when it is greater than -2.
- Why: Choose a location, then the products and quantities, for check-in, check-out, or transfer.
- How to access and visibility conditions: Not from the products grid toolbar. Read only is sent to `/_admin/_unauthorized`. The import links append `&Type=`.
- Steps: Pick a location (and a destination for transfer). Search or scan. Select. Or create products, or import a file.
- Options and defaults: Location defaults as above. The list UI is mostly client script in the page and `ProductSelector_v2.js` (53 lines). The scan/filter functions (`FilterList`, `Try2Scan`) live in the page script and were not fully read.
- Permissions: Not Read only.
- Validation/limits/failures: Location id must be greater than -2 or the instruction panel stays up. Transfer source and destination must differ.
- Result and side effects: Writes `START_LocationID`, or `START_TRANSFER_SOURCE` and `START_TRANSFER_DESTINATION`. Selecting products closes the fancybox via `SignalNext`. The inventory movement after that is not in this code-behind.
- Edge cases: The subtitle string for transfer says “between Location” (singular) in source. Image paths for the two transfer endpoints are assigned in `Page_Init` as source image from the destination type and destination image from the source type (lines 75–76). That swap is in the source. Whether it is visible depends on the CSS that was not compared with the rendered page.
- Related: Import, add products.
- Code: `ProductSelector.aspx.vb` `Page_Init` 16–100, `_changeLocation` 132–202. `ProductSelector.aspx` 99–181.
- Confidence: Confirmed for location choice, titles, and import links. The product-list filtering and the post-`SignalNext` inventory write are Uncertain.
- Suggested KB title: Select products to check in, check out, or transfer

### Editable field control

- Pages: `Controls/EDITABLE_FIELD.ascx`, `EDITABLE_FIELD.ascx.vb`, `Scripts/Controls/EDITABLE_FIELD.js`
- What it does (traced): A label plus a text box used for product properties and also for locations, batches, and custom-field definitions (`FieldType` switch in `SaveField`). On the product editor, type `PRODUCT_PROPERTY` updates `Products.{SQL_FieldName}`. Currency style parses a decimal. `isEnabled=False` disables the box. `isNumeric` blocks save when the value is not numeric or `CInt` is negative, and shows `CTRL_LBL_ERROR_{id}`. The error string passed in for product name is not shown unless that numeric check fails. Autocomplete data adds CSS class `ausomeplete`. The product editor turns autocomplete on for custom fields through `InitializeAutocompleteAPI` (admin API token cookie). `EDITABLE_FIELD.js` is 42 lines and was not required to explain the save; the postback is the hidden button in the control.
- Why: One control for click-to-edit text across products and other records.
- How to access and visibility conditions: Instantiated by the product editor for name, buy, sell, and non-preset custom fields. Preset custom fields are a separate `DropDownList`, not this control.
- Steps: Edit the box. The control posts and saves.
- Options and defaults: Placeholder “New...” when the content is empty (`CreateControlElements` around 320).
- Permissions: Disabled on the read-only editor.
- Validation/limits/failures: Numeric rule above. Currency conversion uses `CType(..., Decimal)` after that check. A non-numeric currency should already have been stopped. No length limit in the product branch.
- Result and side effects: SQL update, products reload cookie, `PRODUCT__EDIT` activity. Other field types in the same control update locations, batches, or custom-field names. Those types are not what the product editor requests.
- Edge cases: `CInt` on a decimal numeric value rounds before the negative test.
- Related: Product editor fields.
- Code: `EDITABLE_FIELD.ascx.vb` `PropertiesContstruct` 141–175, `hidden_button_single_postback_Click` 331–372, `SaveField` 375–439, disable 218–219.
- Confidence: Confirmed for the product-property path. The 42-line script was not quoted; its behavior is Uncertain beyond the file existing.
- Suggested KB title: How inline product fields save

### Custom-field presets popup

- Pages: `Popups/FixedMultiFields.aspx`
- What it does (traced): Title “Set Defaults for '{field name}'”. A text box and “+ Add” append an option. Choosing a list item shows Remove. Checkbox “Allow other values”. Save is hidden until the list changes, an item is removed, the checkbox is clicked, or the list starts empty. Save writes `CustomFieldService.SavePresets` and closes the fancybox. Commas typed into a value are stored as underscores (`updateHiddenField`). “Other (Specify)” is not listed as a normal row; it checks “Allow other values”.
- Why: Limit a custom field to a list, which the product editor and multi-edit then use.
- How to access and visibility conditions: Admin only. Non-admins go to `/_admin/_unauthorized`. The products grid does not link here. `js/business/custom-fields.js` sets `link.href = "/Popups/FixedMultiFields.aspx?id=" + index`. Query `id` is the custom-field index.
- Steps: Add or remove values. Optionally allow other values. Save.
- Options and defaults: Existing presets are loaded. Allow other is on when a stored value equals “Other (Specify)”.
- Permissions: Admin.
- Validation/limits/failures: Blank add is ignored. Remove requires a selected option.
- Result and side effects: Preset list on that custom field. Product editor dropdowns and multi-edit `cfValueIsAllowed` read it later. This page does not change existing product values.
- Edge cases: A comma in a preset cannot round-trip; it becomes an underscore before save.
- Related: Editor dropdowns, multi-edit validation, import (import does not enforce presets).
- Code: `FixedMultiFields.aspx` 8–106. `FixedMultiFields.aspx.vb` `Page_Init` 20–28, `DisplayCustomFieldPresets` 33–55, `SavePresets` 66–80.
- Confidence: Confirmed
- Suggested KB title: Set a list of allowed custom-field values

### Document editor

- Pages: `DocumentEditor.aspx`, `CS_Document_Class.vb`
- What it does (traced): Query `ID` loads one row from `{account}.Documents`. Type 0 shows “Purchase Order” in `#ff9900`, the vendor placeholder, and the process placeholder. Type 1 shows “Sales Order” in `#00cc66`, the customer placeholder, and the process placeholder. Type 2 shows “Kit” in `#006699` and hides vendor, customer, and process. The number label is `#{DocumentID_custom}`. Lines from `DocumentContents` render as `{product number} X {quantity} @ {price} {currency}`. Price errors become -1. The header shows the literal text `[PRINT] [SAVE] [NEXT]`. The footer shows the literal text `[Cancel] [Save]`. Vendor, customer, and process panels contain the literal text `[VENDOR]`, `[CUSTOMER]`, and `[PROCESS]`. There are no click handlers. Nothing in the product pages links to `DocumentEditor.aspx`.
- Why: A document record can list product numbers. This page does not attach that document to a product, and it does not edit the document.
- How to access and visibility conditions: Direct URL `DocumentEditor.aspx?ID=`. Read only is unauthorized. No products-grid button.
- Steps: Open with an id. Read the lines.
- Options and defaults: None that work. `CS_Document_Class` also defines type BOM as integer 3, but the page has no Case 3, so a BOM would not set a title.
- Permissions: Not Read only.
- Validation/limits/failures: An empty document list would throw when reading `DocumentContainer(0)`. Not guarded.
- Result and side effects: Read only. `Create_CS_Document` exists on the class and is not called by this page.
- Edge cases: This is not the product attachment feature. Product files use the editor paperclip.
- Related: Product attachments.
- Code: `DocumentEditor.aspx` 54–84. `DocumentEditor.aspx.vb` `PopulateDocument` 25–63, `ListContents` 66–78. `CS_Document_Class.vb` `Get_CS_Documents` 46–86, `Get_CS_DocumentContents` 88–111, `Create_CS_Document` 113–129.
- Confidence: Confirmed
- Suggested KB title: View a purchase order, sales order, or kit

### Orphan clone popup

- Pages: `Popups/CloneProduct.aspx`
- What it does (traced): If the product exists, it shows “New Product Details” and “Cloning Product {number}”. It builds PRODUCT NUMBER with AUTO checked, DESCRIPTION, BUY PRICE, SELL PRICE, and every custom field. Every field except the product number is `Enabled=False` and filled from the source. There is no save button in the markup and no click handler in the code-behind. The editor button that referenced `CloneProduct()` is commented out. No other `.aspx`, `.vb`, or `.js` file references `CloneProduct` except this popup and that comment.
- Why: Left in the project. It is not the clone feature users get from the product editor.
- How to access and visibility conditions: Direct URL only, and not for Read only (`/_admin/_unauthorized`). Unknown product goes to `Product Error.html`.
- Steps: None that save.
- Options and defaults: AUTO checked. Prices and description locked.
- Permissions: Not Read only.
- Validation/limits/failures: None beyond the gates above.
- Result and side effects: Display only.
- Edge cases: Do not document this as the way to clone. Use the editor modal.
- Related: Clone this product.
- Code: `CloneProduct.aspx` 42–52. `CloneProduct.aspx.vb` `Page_Init` 22–44, `LoadDynamicInputs` 46–195. Commented button: `ProductEditor.aspx` 791.
- Confidence: Confirmed
- Suggested KB title: Do not use — old clone screen (internal)

### Orphan delete dialog

- Pages: `Dialogs/ProductDeleteConfirmation.aspx`
- What it does (traced): Expects `Session("ProductsToDelete")` as comma-separated product numbers. Lists `{name} - ({number})`. CANCEL closes the fancybox. At All Locations the only destructive button is “DELETE FROM ALL LOCATIONS”, which deletes quantity rows for those product numbers and does not delete the product row. At a specific location there is also “DELETE FROM LOCATION [ALL > {path}]”, which deletes quantity rows for those products at `LocationID_VIEW` only. Both destructive buttons also call `parent.$.fancybox.close()` on the client click, so the postback may be cut off by the close. No file outside this dialog reads or sets `ProductsToDelete`. The live grid delete does not open this page.
- Why: An older quantity-only delete. It is not wired.
- How to access and visibility conditions: Direct URL. Read only is unauthorized. Without the session value, `LoadProductsToDelete` exits and the list stays empty; the buttons still render.
- Steps: Not reachable from Products.
- Options and defaults: Location comes from `LocationID_VIEW`.
- Permissions: Not Read only.
- Validation/limits/failures: Empty session returns immediately. A null session would throw on `.Length` before that check.
- Result and side effects: If a postback completed, only `Quantities` rows would be deleted. No activity registration in this file. No product-row delete.
- Edge cases: Do not describe the products delete button as offering “this location” versus “all locations”. That choice is only on this unwired page. The live button deletes products through `DeleteProducts`.
- Related: Grid delete, editor delete.
- Code: `ProductDeleteConfirmation.aspx.vb` `LoadProductsToDelete` 22–44, `DELETE_FROM_ALL_LOCATIONS` 46–52, `DELETE_FROM_SINGLE_LOCATION` 55–59, `ShowButtons` 85–149.
- Confidence: Confirmed
- Suggested KB title: Do not use — old delete-quantities dialog (internal)

### Success page

- Pages: `SuccessProducts.aspx`
- What it does (traced): Sets `COOKIE_PRODUCTS_PAGE_RELOAD` to TRUE. Shows “Success!” and “You can now Check In these products to any location.” On load, if `isOnboarding()` is true, it calls `parent.GoToPage(4)`. Nothing in the repository redirects to `SuccessProducts.aspx`. A copy exists under `_cvr/`.
- Why: An older end screen for creating products. The live path is `CheckInCreatedProducts.aspx`.
- How to access and visibility conditions: Direct URL only, from the references that were searched.
- Steps: None in the current create flow.
- Options and defaults: None.
- Permissions: No user-type check in the code-behind.
- Validation/limits/failures: None.
- Result and side effects: Reload cookie only.
- Edge cases: Onboarding behavior depends on `isOnboarding` in `CS_Core.js`, which was not read.
- Related: Check-in after create.
- Code: `SuccessProducts.aspx` 15–38. `SuccessProducts.aspx.vb` 7–11.
- Confidence: Confirmed that the page exists and that no caller was found. Uncertain whether an external link or an unsearched binary opens it.
- Suggested KB title: Do not use — old product-success page (internal)

### Auto product numbers

- Pages: `Product.vb`, used by add, clone, and import
- What it does (traced): `GetCurrentIndexAuto` is the max integer after `CSN-` among product numbers matching `^CSN-[0-9]+`, or 0. `GetNextAutoSKU` adds the offset and formats `CSN-` plus `00000000#` (nine digits). Examples in code shape: the first is `CSN-000000001`.
- Why: Create a product without typing a number.
- How to access and visibility conditions: Add Products AUTO checkbox (default on). Clone Auto checkbox (default on). Create-import when the product-number cell is unmapped or blank. Check-in import when the identifier cell is blank and the match is not description/custom field.
- Steps: Leave Auto on, or leave the product-number column blank.
- Options and defaults: Offset defaults to 1. Batches pass an increasing offset so one save does not reuse a number.
- Permissions: Same as the create path.
- Validation/limits/failures: The index query only considers numbers that already look like `CSN-` plus digits. A hand-typed `CSN-` number that is not all digits is ignored by the max. A generated number that collides is skipped on Add Products (`ProductExists`) and ignored by `INSERT IGNORE` on `CreateProducts`.
- Result and side effects: The new product number is the primary id. It is not edited later on the product editor.
- Edge cases: Clone’s server path regenerates when Auto is posted as `HF_clone_auto_sku=1`. The client’s placeholder is not saved.
- Related: Add, clone, import.
- Code: `Product.vb` `GetCurrentIndexAuto` 240–244, `GetNextAutoSKU` 246–255.
- Confidence: Confirmed
- Suggested KB title: Automatic product numbers

### What create and delete do to inventory data

- Pages: `Product.vb`, `Quantity.vb`, `CreatedProductCheckIn.vb`
- What it does (traced): `CreateProducts` inserts product number, name, buy price, sell price, and `CF_{index}` columns with `INSERT IGNORE`, then `ListProducts` inserts into `Quantities` (`ProductNumber`, `LocationID`) at the passed location, default `-2`, with no quantity column. It registers `PRODUCT__CREATE`. `InsertProductOnly` (clone) inserts the product and the activity and does not call `ListProducts`. `Quantity.ListProduct` is the same insert for one product and one location; the products page does not call it directly. Check-in adds quantity at a real location. Grid multi-edit quantity overwrites quantity at the viewed location. Inline quantity calls the adjust API. `DeleteProducts` is the live delete. `_DeleteProduct` / `_DeleteProducts` are the older SQL deletes of product, quantities, and images.
- Why: Separate the catalog record from stock.
- How to access and visibility conditions: Through add, import, clone, delete, multi-edit, and check-in.
- Steps: Covered in those features.
- Options and defaults: New staged quantity is 1 unless a file set another non-negative integer.
- Permissions: Covered above.
- Validation/limits/failures: `INSERT IGNORE` means a duplicate product number does not change the existing row.
- Result and side effects: Activities `PRODUCT__CREATE`, `PRODUCT__EDIT`, `PRODUCT__DELETE`, and `INVENTORY__CHECK_IN` depending on the path. Expirations are deleted with `DeleteProducts` and saved on create when a date was supplied.
- Edge cases: Location `-2` quantity rows from `ListProducts` are a side effect of create, not a user-selected location. Their quantity depends on the database default for `Quantities.Quantity`, which is not set in this INSERT. Uncertain what number those rows show.
- Related: All create and stock features.
- Code: `Product.vb` `CreateProducts` 139–189, `ListProducts` 222–238, `InsertProductOnly` 191–220, `DeleteProducts` 58–85, `UpdateProductLocationQuantity` 625–658. `Quantity.vb` 3–14.
- Confidence: Confirmed, except the database default quantity on the `-2` insert.
- Suggested KB title: What is stored when you create or delete a product

### Batch helper

- Pages: `Batch_Class.vb`. `Products.aspx.vb` only clears cookie `STOCKROOM_BATCH`.
- What it does (traced): The class can create, delete, and rename a batch, add or update a product and quantity in `BatchContents`, remove a product, and list batches. No in-scope page calls these methods. `Products_Helper.vb` is an empty class.
- Why: Batches exist in the database API. They are not a products-page feature in the files that were read.
- How to access and visibility conditions: Not from the products toolbar, editor, add page, or import page.
- Steps: None on these pages.
- Options and defaults: None exposed here.
- Permissions: Not applicable on these pages.
- Validation/limits/failures: Not applicable.
- Result and side effects: The products page clears `STOCKROOM_BATCH` on load so a previous batch cookie is not kept while viewing products.
- Edge cases: `EDITABLE_FIELD` can update a batch name when its field type is the batch type. The product editor does not construct that type.
- Related: Transfer cookie comment in `CookiesInitialize`.
- Code: `Batch_Class.vb` 17–141. `Products.aspx.vb` `CookiesInitialize` 280–287. `Products_Helper.vb` 1–6.
- Confidence: Confirmed that these pages do not call the batch methods. Uncertain whether the map or transfer pages do.
- Suggested KB title: Batches are not edited on the products page

### Records-account branch

- Pages: `Products.aspx.vb`, `AddProducts.aspx.vb`, `ProductEditor.aspx.vb`, `ImportFromFile.aspx.vb`
- What it does (traced): When `AccountSettings.AccountType = 1`, multi-edit does not run the product SQL; it calls `RecordsApp.AdjustRecord`. Add Products disables buy and sell. The editor and the create-import omit buy and sell unless account type is 0. The code comment calls account type 1 “RECORDS APP (Arvig)”.
- Why: That account type does not use the standard price columns in these screens.
- How to access and visibility conditions: Account type on the signed-in account.
- Steps: Same screens, with prices removed or the multi-edit write replaced.
- Options and defaults: Prices are not offered.
- Permissions: Same user gates.
- Validation/limits/failures: `RecordsApp.AdjustRecord` was not read.
- Result and side effects: Standard accounts (`AccountType = 0`) use the SQL described in multi-edit and create. Type 1 multi-edit side effects are Uncertain beyond the method call.
- Edge cases: Custom fields still appear for type 1.
- Related: Multi-edit, add, import, editor.
- Code: `Products.aspx.vb` 1376–1388. `AddProducts.aspx.vb` 99–113. `ProductEditor.aspx.vb` `GetVisibleProductFieldOrderTokens` 377–396. `ImportFromFile.aspx.vb` 238–243.
- Confidence: Confirmed for what these pages skip. Uncertain for `RecordsApp.AdjustRecord`.
- Suggested KB title: Products on a records-style account

---

## UNCERTAIN

These are gaps, not guesses about features that should exist.

1. `productDeleter.delete()` is the live delete. Its source file was not in the repository search. It is not confirmed whether it deletes quantity rows, images, attachments, batch lines, or document lines. `Product.vb` does delete stored expirations after it, and it does write a delete activity. The editor modal claims quantities are checked out of every location. That sentence is confirmed as UI copy, not as proof of the deleter.
2. `CreateProducts` → `ListProducts` inserts `Quantities` at location `-2` without a quantity value. The number stored depends on the table default, which was not in these files.
3. `?AutoHighlight=TRUE` is added to editor links and never read in `ProductEditor.aspx.vb`.
4. Map control type 2 and type 5 quantity editing, permissions, and validation were not read. The editor only hosts the control and shows the instruction.
5. `ProductEditorCfUrlOpenLink.js` behavior is confirmed. Whether `ProductEditor.aspx` includes that script was not re-checked in this pass.
6. `EDITABLE_FIELD.js` (42 lines) was not traced. Saves that were traced go through the control’s postback.
7. After a non-create import, `SELECTOR_PROCEED` and the START cookies are written and the fancybox closes. The page that consumes them was not audited, so the exact check-in or check-out result of that import is not fully confirmed.
8. Transfer return (`ApplyImportedTransfer=1` and the check-in Continue redirect) leaves this scope. This audit confirms the redirect, not the transfer page’s write.
9. `AppendTransferImportRow` skip messages other than the length limit and the ragged-row skip were not quoted line by line.
10. Export Report builds the CSV and also rewrites location paths. Column-by-column CSV layout past the checkbox list was not fully read. Search text is not sent to it.
11. `SuccessProducts.aspx` has no caller in the searched source. `isOnboarding()` was not read.
12. `GridviewSortDirectionGet` is unused by the live sort handler. It should not be documented as the sort rule.
13. `GetResizedFile` on the editor is unused by the upload handler.
14. `Products.js` functions `custom_search`, `RelocateStockroom`, `DeleteConfirmationPrep`, and `TransferPrep` are not connected to elements in the current `Products.aspx` script block (only column dropdown, column save, and the grid are assigned). The server still has `RelocateStockroom` and `FORCE_CUSTOM_SEARCH`, but the markup that was read does not call them.
15. Read-only printable opens `/Products?printable=true`, and that page redirects read-only users to `Products_read_only` with no query string. The flag is therefore dropped. Not run in a browser.
16. `ProductsGridUrlCells.js` on the read-only page was not confirmed.
17. `RecordsApp.AdjustRecord` was not read.
18. `Batch_Class` may be used outside this scope. It is unused by the pages in the inventory above.
19. Document type BOM (3) has a class enum value and no page layout.
20. The products delete confirm and the editor delete modal were not executed, so the fancybox-close timing versus the postback was not observed. The editor sets a flag and then clicks the button after closing the modal in script; the grid uses `confirm()` before the postback. Those code paths are confirmed. The orphan dialog’s client `fancybox.close()` on the same click as a server delete is a race that was not run.

---

## CONTROLS CHECKLIST

Status is what the markup and code-behind do, not a test run.

### Products.aspx toolbar and grid

| Control | Label or tooltip | When it shows | Action | Notes |
|---|---|---|---|---|
| `LocationSelector_control` | Location path | Width over 900px | Saves `LocationID_VIEW`, reloads | `-2` is ALL LOCATIONS |
| `lbl_products_mobile_location_path` | Path or ALL LOCATIONS | Width at or under 900px | Display only | |
| `btn_Add` / link `A2` | Tooltip “Add one or more products to your inventory” | Always | `AddProducts.aspx?LastPage=Products` | Image `Text` says “Select Columns” |
| `btn_delete` | “Delete selected products from your inventory.” | Disabled until a row is checked | Confirm, then `DeleteProducts` | Not a location-only delete |
| `btn_MultiEdit` | “Multi-Edit: Change all of the selected items at once” | Disabled until a row is checked | Opens the SET/TO panel | |
| `drpdown_Multiedit_Field` | Product Name, Quantity (specific location only), Buy Price, Sell Price, custom fields | Inside the panel | Chooses the column | |
| `txt_MultiEdit_Value` | Empty | Inside the panel | The new value | Required |
| `btn_MultiEdit_UPDATE` | Update | Inside the panel | Writes and reloads | |
| Cancel button | Cancel | Inside the panel | Hides the panel | Not a server post |
| `btn_columns` | “Select the columns to display in your inventory” | Always | Shows the checkbox list | |
| Column checkboxes | Product Number (locked), Description, Quantity, Buy Price, Sell Price, custom names, Cost Value | In the list | Cookie `ColumnOrder` | Product Number cannot be cleared |
| `btn_AdjustColumns` | SAVE COLUMNS | In the list | Saves column order on the user row | |
| EDIT COLUMNS | EDIT COLUMNS | Admin only | `openCustomFieldEditor()` | |
| Recent image | No tooltip in markup | Always | Hover list of activity code 0 | Max 50 lines shown |
| `btn_export_report` | “Download Product Report” | Always | Fancybox `ExportReport?LocationID=` | Search is not passed |
| `btn_print_barcodes` | “Print barcodes for selected products” | Hidden until a selection | `PrintBarcode` | All-products path asks for confirm |
| `btn_image_toggle` | “Hide Product Images” | Commented out | Commented-out handler | Setting lives on the user record |
| Header `SelectAll` | Checkbox | Grid header | Selects this page, offers select-all | Select-all is every product in the account |
| Row `CheckBox1` | Checkbox | Each row | Enables delete, multi-edit, print | |
| `BtnUpdate` | Save, inside edit template | Not used by a traced edit mode | `CommandName=Update` | No `RowUpdating` handler was found in the code-behind method list |
| Column headers | Field names | Visible columns | Sort | Drag to reorder |
| Quantity cell | Number | When the column is on | Opens inline editor only in the cases under Inline quantity | Read-only page does not |
| Row cells | Product data | Always | Open product editor | URL pills steal the click |
| Empty create panel | “No products yet” / “Click to create” | No products at All Locations | Add Products | |
| Empty location panel | “Location is empty...” / “Click to Check in” | Empty location and empty children | `Start.aspx?checkin=true&id=` | |
| Sub-location note | “This location is empty but its sub-locations are not” | Children have stock | Display | Cursor is not a link |
| Search chips | The term, and ALL | When a search cookie or `?Search=` exists | Remove one term or all | Forces All Locations |
| Printable image | title “pritnable version” | Bottom of the page | `/Products?printable=true` | Hides `.navbar` and `.clickable` |
| `HiddenBtn`, `HiddenBtn2`, `HiddenBtn_LOCATION`, `BTN_HIDDEN`, `FORCE_CUSTOM_SEARCH`, `FORCE_CLEAR_FILTER` | Hidden | Not shown | Various reloads | `custom_search()` is not wired in the page script |
| Pinch zoom | None | Viewport max 900px | Scales the grid 0.18–1.8 | |

### Products_read_only.aspx differences

| Control | Difference |
|---|---|
| Add, Delete, Multi-edit | Not in the toolbar |
| EDIT COLUMNS | Not turned on |
| Columns, Save columns, Recent, Export, Print barcodes, location, printable, search, sort, pager | Present |
| Print barcodes | Enabled by row checkboxes only |
| Quantity cell | No `QtyQuickAdjust` |
| Row click | `ProductEditor_read_only.aspx` |
| Who can stay | Read only only |

### ProductEditor.aspx

| Control | Label | Action |
|---|---|---|
| `lbl_ProductNumber` | PRODUCT NUMBER | Display |
| Clone buttons (two) | “clone this product” | Opens clone modal |
| `img_thumbnail_html` | “Click to update image...” | File upload, unless Lansweeper replaced the image |
| `img_attachment` | “Click to attach file...” | Upload attachment |
| Print image | “Print Barcodes” | `PrintBarcode?SKU=&Name=` |
| `lansweeper_link` | Lansweeper image | Hidden until a URL exists. Opens the URL |
| Attachment name button | `{name}.{ext}` | Download |
| Attachment X | X | Confirm, then delete |
| Product name, buy, sell, text custom fields | Field label | `EDITABLE_FIELD` save |
| Preset dropdown | Field label, “(none)”, presets | Postback save. “Other (Specify)” opens a modal |
| Expiration date | EXPIRATION | Shown only if the user flag is on. API get/post/delete |
| “Edit your fields” | Edit your fields | Admin. `openCustomFieldEditor()` |
| `btn_delete2` | Tooltip “Delete this product” | Modal, then `DeleteProducts` |
| Map | “Click a location. Type new quantity. Press Enter.” | Map control type 2 |
| Details tab | “Show details” | Toggles the field column |
| Clone modal Auto | Auto, default checked | Server generates `CSN-` |
| Clone modal fields | Same visible fields | Copied, then editable for the new product |
| Clone expiration | Expiration | Only if the user flag is on |
| Clone button | Clone | `InsertProductOnly`, copy image, optional expiration |
| Delete modal | “Delete this product?” | Cancel or Delete |

### ProductEditor_read_only.aspx

Fields and dropdowns disabled. Expiration disabled. Print, attachment download, Lansweeper, and map type 5 remain. No clone, no delete, no image upload, no attachment upload, no “Edit your fields”.

### AddProducts.aspx

| Control | Label | Action |
|---|---|---|
| Product number | PRODUCT NUMBER | Manual, or AUTO (default on) |
| AUTO checkbox | AUTO | Default checked |
| Description | DESCRIPTION | Empty becomes the product number on save |
| Buy / sell | BUY PRICE / SELL PRICE plus currency | Hidden or disabled for account type 1 and when show-price flags are off. Must be blank or a number ≥ 0 |
| Custom fields | Uppercase field name | Text or preset dropdown with “(none)” |
| Expiration | Shown with the user flag | Optional `yyyy-MM-dd` |
| Thumbnail | “Change image” after upload | Temp image, copied on save |
| Import | Server `btn_import_from_file` | `ImportFromFile.aspx?LastPage=AddProducts` |
| Save | `btn_save` | Creates products and opens check-in, or returns to transfer, or posts a mobile message |
| Edit your fields | Admin link | `openCustomFieldEditor()` |

### ImportFromFile.aspx

| Control | Label | Action |
|---|---|---|
| File upload | Posted file | CSV checks, then column chips |
| Instruction | “Drag from left to right to Match the fields.” | After a good file |
| Field chips | Mode-specific | Drop target. Click clears |
| Column chips | Header text | Drag source |
| Quantity / expiration / location info | Tips quoted in the import sections | Icons on those chips |
| Match-field chevron | “Choose the field that identifies each product” | Transfer return only. Product Number, Description, custom fields |
| Location-key chevron | “Choose how locations are identified” | Location required. Location # (default) or Location Name |
| Sample link | Sample CSV File | One of the four samples |
| Edit your fields | Edit your fields | Create mode and Admin |
| `btn_cancel` | Go Back | Add Products, Product Selector, or transfer |
| `btn_save` | Next | Hidden until a file is stored. Hidden again when the existing-product panel is open |
| `btn_confirm_existing` | Continue | Create mode after the existing-product notice |
| Error labels | Messages in the import sections | `lbl_error_message_empty`, `_commas`, `_numeric`, `_location` |

`lbl_error_message_commas` is cleared in `clearErrors` and no assignment of its text was found in the sections that were read. Whether it still appears is Uncertain.

### CheckInCreatedProducts.aspx

| Control | Label | Action |
|---|---|---|
| Title | “{n} Product(s) created.” or the transfer wording | Display |
| Map title | “Click a location to Check it in/them in.” | Hidden for imported locations and transfer return |
| Auto-SKU note | “{n} product number(s) was/were generated.” | When count > 0 |
| Quantity box | Per product | Default staged quantity. Whole number ≥ 0. At least one ≥ 1 to check in |
| Step buttons | Increase / decrease | Client only |
| Location path | On imported-location rows | Display |
| Skip check-in | Skip check-in | Closes and reloads parent. Products stay created |
| `btn_checkin` | Hidden Check In | After the comment modal |
| Comment modal | “Any comments about this transaction?” | Skip Comment, or Save if text is present. Cancel |
| `btn_skip_return` | Skip ›› | Transfer return only |
| `btn_continue_transfer` | Continue | Transfer return only |
| Error label | The four `e=` messages | After a failed post |

### CheckInCreatedProductsDone.aspx

No buttons. Script closes the modal and reloads the parent, or goes to `/Products.aspx`.

### PrintBarcode.aspx

| Control | Label | Default |
|---|---|---|
| `ddl_label_stock` | LABEL STOCK | 30252 |
| `btn_preview` | PREVIEW & PRINT | Builds labels and opens the print window |
| Print window button | PRINT BARCODE | `window.print()` |
| Amazon link | DYMO LabelWriter 450 | External |

### ProductSelector.aspx

| Control | Label | Notes |
|---|---|---|
| `location_selector` | Instruction depends on Type | Required before the list |
| Transfer source / destination images and labels | Location names | After both are chosen, or from the query string |
| `txt_search_filter` | “Search or scan...” | Enter triggers `Try2Scan` |
| `clearButton` | X | Clears the filter |
| `link_import` | Import From File | `CREATE_NEW=FALSE` |
| `link_import_w_locations` | OR Import from File with Locations | Also `LOCATION_REQUIRED=TRUE` |
| New products link | + New Products | Parent `/Start?add=true` |
| `btn_save` | Select | Hidden until a selection. `SignalNext`, close fancybox |

### FixedMultiFields.aspx

| Control | Label |
|---|---|
| `txt_new_default` | Empty text box |
| `btn_add_default` | + Add |
| `listbox` | Current presets |
| `btn_remove` | Remove. Hidden until a row is selected |
| `chk_allow_other` | Allow other values |
| `btn_cancel` | Cancel. Closes fancybox |
| `btn_save` | Save. Hidden until a change. Admin only |

### DocumentEditor.aspx

| Control | What it is |
|---|---|
| `lbl_document_type` | Purchase Order, Sales Order, or Kit |
| `lbl_document_number` | `#{custom id}` |
| `[PRINT] [SAVE] [NEXT]` | Literal text |
| `[VENDOR]` `[CUSTOMER]` `[PROCESS]` | Literal text, some hidden by type |
| `div_dynamic_list` | One label per line: product, quantity, price |
| `[Cancel] [Save]` | Literal text |

### Dialogs/ProductDeleteConfirmation.aspx (not linked)

| Control | Label |
|---|---|
| Title | Delete Products |
| `txt_products` | Read-only list of name and number |
| CANCEL | Closes fancybox |
| DELETE FROM ALL LOCATIONS | Deletes quantity rows for those products |
| DELETE FROM LOCATION [ALL > path] | Only when a location is selected. Deletes quantity rows at that location |

### Popups/CloneProduct.aspx (not linked)

| Control | Label |
|---|---|
| Title | New Product Details |
| `lbl_cloneID` | Cloning Product {number} |
| Product number | PRODUCT NUMBER, AUTO default on |
| Other boxes | DESCRIPTION, BUY PRICE, SELL PRICE, custom fields. Disabled |
| Save | None |

### Samples

Headers only, as listed under Sample CSV headers. Data rows in the samples were not treated as product behavior.
