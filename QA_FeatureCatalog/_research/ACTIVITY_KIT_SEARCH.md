# Activity, expirations, kitting, search, reports, confirmation, onboarding

Code audit of the scoped pages. Phrases in quotes are copied from source. Activity type names below are the `ActivityCodeIndex` constants and the strings returned by `GetActivityDescription`. Nothing else was invented.

No undo action exists on these pages. A repo-wide search for an activity undo control only hits CSS comments and a Products delete confirmation that says the delete cannot be undone.

---

## Page inventory

| Page | Title / master | Role | Who can open it |
| --- | --- | --- | --- |
| `ActivityHistory.aspx` (+`.vb`) | "Activity History (CyberStockroom)", `UserPage.master` | Filterable activity list, CSV of the current filter | Any logged-in user. No `SHOW_*` flag. Read-only users are not redirected away. |
| `ActivityDetails.aspx` (+`.vb`) | "Activity Details (CyberStockroom)", `UserPageNoMenu.master` | One activity in a Fancybox iframe, plus single-activity CSV | Same login gate as the no-menu master. Opened with `?ActivityID=`. `?download=1` streams CSV. Missing id shows "Activity not found" or HTTP 404 on download. |
| `App_Code/Classes/Business Objects/Activity.vb` | class `Activity` | Register, query, describe, filter, and CSV-write activities | Not a page. |
| `Expirations.aspx` (+`.vb`) | "Expirations (CyberStockroom)", `UserPage.master` | Expiration list, counts, replace/clone wizard | `SHOW_EXPIRATIONS` must be true, else redirect `Settings#expirationsAnchor`. Read-only users are sent to `Expirations_read_only.aspx`. |
| `Expirations_read_only.aspx` (+`.vb`) | same title | Same list and colors, no Manage button | Only read-only users stay here; everyone else is sent to `/Expirations`. Same `SHOW_EXPIRATIONS` gate. |
| `App_Code/Classes/Service Layer/ProductExpirations.vb` | class `ProductExpirations` | POST/DELETE `https://code.cyberstockroom.com/api/expiration` | Called from product create/import/delete, not from the Expirations page itself. Failures are swallowed. |
| `Kitting.aspx` (+`.vb`) | "Kitting (CyberStockroom)", `UserPage.master` | Kit list, create, components, delete | `SHOW_KITTING` must be true, else redirect `Settings#kittingAnchor`. Read-only users are sent to `Kitting_read_only`. **That page file is not in this repo.** |
| `ExportReport.aspx` (+`.vb`) | empty title, `UserPageNoMenu.master` | "Download Product Report" CSV | Logged-in. No read-only or feature flag in `Page_Init`. Opened from Products (Fancybox) as `ExportReport` or `ExportReport?LocationID=`. Page name registered as `ExportProductReport`. |
| `ai-report.aspx` (+`.vb`) | "AI Insights Report", `UserPage.master` | Renders one stored insights report | Logged-in. Requires `?id=`. On any exception, redirect `Map`. **No link to this URL exists anywhere else in this repo.** It is a user-facing page (full app master, visible title) that is unlinked from navigation. |
| `Controls/CS_SearchBox.ascx` (+`.vb`) | header control | Global autocomplete on `UserPage.master` (`CS_SEARCHBOX1`) | Every page that uses `UserPage.master`, including Activity, Expirations, Kitting, and AI report. |
| `ConfirmationDialog.aspx` (+`.vb`) | no title, `UserPageNoMenu.master` | Delete-location confirm | Read-only users go to `/_admin/_unauthorized`. Opened from the map and `LocationEditor.aspx` as `ConfirmationDialog.aspx?ACTION=DELETE&LocationID=`. The `ACTION` value is read and then ignored; the page always sets up delete. |
| `pages/guides/getting-started.aspx` (+`.vb`) and `pages/guides/scripts/getting-started.js` | onboarding wizard | Step machine for profile, map, invites, products, import, finalize | **`Page_Init` redirects to `/Map` and returns before any wizard code runs.** The steps below are still in the page and script, but this request never reaches them. `Welcome.aspx.vb` and `map_demo.aspx.vb` still redirect *to* this URL. |

Print: none of these pages expose a print button. `UserPage.master` will call `makePrintable()` when the query string `printable=TRUE` is present. That flag is not linked from these pages.

---

## Activity type catalog (source of every name below)

`Activity.ActivityCodeIndex` in `Activity.vb` lines 206–243. Comment in source: numbers are legacy and out of order.

| Constant | Integer | Shown in Activity History filters | Standard phrase (`AccountType` 0) | Records / Arvig phrase (`AccountType` 1) |
| --- | --- | --- | --- | --- |
| `PRODUCT__CREATE` | 0 | Products → Create | created new products | created new records |
| `INVENTORY__CHECK_IN` | 1 | Inventory → Check In | checked in products | assigned records |
| `PRODUCT__DELETE` | 2 | Products → Delete | deleted products | deleted records |
| `INVENTORY__CHECK_OUT` | 3 | Inventory → Check Out | checked out products | deallocated records |
| `INVENTORY__TRANSFER` | 4 | Inventory → Transfer | transferred products | transferred records |
| `PRODUCT__EDIT` | 5 | Products → Edit | edited products | edited records |
| `LOCATION__CREATE` | 6 | Location → Create | created a new location | created a new location |
| `LOCATION__DELETE` | 7 | Location → Delete | deleted a location | deleted a location |
| `LOCATION__EDIT` | 8 | Location → Edit | renamed a location | renamed a location |
| `USER_CREATED` | 10 | not in any history query list | falls through to `activity [10]` | same |
| `USER_DELETED` | 11 | not listed | `activity [11]` | same |
| `USER_NAME_EDITED` | 12 | not listed | `activity [12]` | same |
| `ACCOUNT__CREATED` | 15 | not listed | `activity [15]` | same |
| `ACCOUNT__PLAN_CHANGED` | 16 | not listed | `activity [16]` | same |
| `ACCOUNT__CF_CREATED` | 17 | not listed | `activity [17]` | same |
| `ACCOUNT__CF_EDITED` | 18 | not listed | `activity [18]` | same |
| `ACCOUNT__CF_DELETED` | 19 | not listed | `activity [19]` | same |
| `ACCOUNT__TIMZONE_EDITED` | 20 | not listed (constant spelling is `TIMZONE`) | `activity [20]` | same |
| `ACCOUNT__CURRENCY_EDITED` | 21 | not listed | `activity [21]` | same |
| `USER_INVITED` | 22 | not listed | `activity [22]` | same |
| `USER_EMAIL_EDITED` | 23 | not listed | `activity [23]` | same |
| `USER_IMAGE_EDITED` | 24 | not listed | `activity [24]` | same |
| `INVENTORY__ADJUST` | 25 | Inventory → Adjust | adjusted a product quantity | adjusted a record |
| `UNDEFINED` | 100 | not listed | `activity [100]` | same |

Unknown `AccountType` returns `[ERROR-ACC1 - unkown account type]`.

History queries that pass `ONLY_DISPLAYABLE=True` use only `(0,1,2,3,4,5,6,7,8,25)`, narrowed by the category table in the next feature. The account and user constants above are declared and are not referenced by any other `.vb` file in this repo.

Comment machine tags (not activity types). Rendered as grey badges; hyphens become spaces; CSS uppercases them:

- `{{cs-transfer}}` (`TAG_TRANSFER`)
- `{{cs-quantity-adjusted}}` (`TAG_QUANTITY_ADJUSTED`)
- `{{cs-quantity-adjust}}` (`TAG_QUANTITY_ADJUST`)
- any `{{cs-…}}` matching `\{\{cs-([a-z0-9-]+)\}\}`

Quantity-adjust comments that drive check-in vs check-out placement must match:

`Quantity for '…' was adjusted from {old} to {new}.`

(`TryParseQuantityAdjustComment`, `Activity.vb` 1091–1104.)

---

### Activity History list
- Pages: `ActivityHistory.aspx`, `ActivityHistory.aspx.vb`, `Activity.vb`
- What it does (traced): Loads activities for the signed-in account, newest first, and paints one row per activity: avatar, green comment, "{You|name} {description}", timestamp, product count, location icons. Clicking the row opens Activity Details in a Fancybox iframe (`width` 95%, `height` 100%). Product and location names inside the row open Product Editor or Location Editor and do not open the details iframe (`stopPropagation`).
- How to access + visibility: Header activity icon, collapsed menu link labeled "Activity", activity popup button "View Activity History" (`UserPage.master`). Mobile master also links `ActivityHistory`. Direct URL `/ActivityHistory`. Visible to every logged-in user, including read-only.
- Steps: Open the page. Default filter set is applied in `Page_LoadComplete` when `IsPostBack` is false, then `LoadActivityWithFilters`.
- Options and defaults (real values or data source): Category `12` (button text "All Activity"). User filter `-1` (icon label "All"). Location filter `-2` (location selector label "All Locations"). Start date = today minus `DEFAULT_DAYS_TIMESPAN` **90** days, formatted `yyyy-MM-dd`. End date = today. Comment box empty, placeholder "search by keyword...", focused on init. Listing cap `LISTING_LIMIT` **15**. Hover/product cap `PRODUCT_LIST_LIMIT` **10**. A code comment says the default calendar is "last year (365 days)"; the constant is 90, and the date picker also uses `moment().subtract(90, 'days')`.
- Permissions: Login via `UserPage.master`. `RegisterPage(..., "ActivityHistory", ...)`. Adopted admin sessions skip the login-page audit insert (`Activity.RegisterPage`).
- Validation/failures: Empty result shows "No Activity..." / "details will appear here" and hides "Show More...". Product rows with an empty content list are skipped (`Continue While`) so the activity is omitted. Deleted locations display type `0` and name `[DELETED]` from `GetLocationName_LIGHT`. Missing profile image falls back to `Images/Icons/avatar.png` or `avatar_round.png`.
- Result: Rows in `div_activity`. Current user's name is replaced with "You" and highlighted `#558DC6` when `UserID` equals `AccountSettings.FirstName` (string compare, not user index).
- Edge cases: Timestamps are shifted by `AccountSettings.TimeZone` hours only when no user filter is applied. When a user filter is on, `GetActivitiesList_COMPLETE` selects raw `DateAndTime` with no `DATE_ADD` (`Activity.vb` 760). Server offset is hardcoded `0`. Product create/edit rows hide quantities. Check-in/out/adjust with both location ids `-2` shows "Multiple Locations" (`Images/Locations/-3.png`). Transfer per-line location `0` or `[DELETED]` is replaced by the activity header location. Location create stores location **type** in `LocationDestinationID`; that value is not a location id (`Activity.vb` 464–465). "Show More..." stays visible whenever at least one row was rendered, including when the full result set is already on screen (`DisplayHistory_FAST` sets it whenever `k` reaches the list end). Changing user, date, location, or category does **not** reset `ViewState("StartIndex")`. Activities whose type has product rows but zero content lines never appear. There is no undo.
- Code file+method+lines: `ActivityHistory.aspx.vb` `Page_Init` 19–29, `Page_LoadComplete` 31–52, `DisplayHistory_FAST` 378–1115, `Activity.vb` `GetActivitiesList_COMPLETE` 656–793, `GetActivityDescription` 116–174
- Confidence: Confirmed
- Suggested KB title: View activity history

### Activity category filters
- Pages: `ActivityHistory.aspx` buttons, `ActivityHistory.aspx.vb` `ApplyCategoryCSS` / `UpdateCategoryDisplay`, `Activity.vb` category `Select Case`
- What it does (traced): Left rail buttons set `ViewState("Category")` and post back. SQL `ActivityCode IN (...)` is chosen from that integer. Categories 1 and 2 then run a second in-memory filter.
- How to access + visibility: Always on the Activity History page, left column.
- Steps: Click a group or a child button.
- Options and defaults (real values or data source): Default category **12**, button "All Activity", CSS `btn-category-active`.

  Button label (account type 0) → category integer → SQL codes:

  | Button | Category | SQL `ActivityCode` list |
  | --- | --- | --- |
  | All Activity | 12 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 25 |
  | Inventory | 0 | 1, 3, 4, 25 |
  | Check In | 1 | 1, 4, 25 then in-memory filter |
  | Check Out | 2 | 3, 4, 25 then in-memory filter |
  | Transfer | 3 | 4 |
  | Adjust | 13 | 25 |
  | Products | 4 | 0, 2, 5 |
  | Create (under Products) | 5 | 0 |
  | Edit (under Products) | 7 | 5 |
  | Delete (under Products) | 6 | 2 |
  | Location | 8 | 6, 7, 8 |
  | Create (under Location) | 9 | 6 |
  | Edit (under Location) | 11 | 8 |
  | Delete (under Location) | 10 | 7 |

  Account type **1** (`SetButtonText`): Inventory→"Assignments", Check In→"Assign", Check Out→"Deallocate", Transfer stays "Transfer", Products→"Records". Child Create/Edit/Delete labels are not rewritten. Adjust is not rewritten.
- Permissions: Same as the history page.
- Validation/failures: Category values other than the cases above leave the SQL list at the default `(1,3,4,25)` inside `GetActivitiesList_COMPLETE` (the initial assignment before `Select Case`). The page only posts 0–13 as listed.
- Result: Active button turns green (`#00B050`). Child buttons use the small style.
- Edge cases: **Check In (1) and Check Out (2)** are not pure type filters.
  - Native check-in (1) always matches category 1. Native check-out (3) always matches category 2.
  - Adjust (25) matches Check In when the parsed comment has old qty **not greater** than new qty (increase, equal, or unparsed). It matches Check Out only when old qty **>** new qty. If the comment does not parse and the first content qty is `> 0`, old is treated as 0 and new as that qty, so the adjust is treated as a check-in.
  - Transfer (4) is **removed** from Check In and Check Out when no location is selected (`locationIds` is nothing). When a location is selected, a transfer stays on Check In only if a destination location is inside the selected location plus descendants **and** the source is not. Check Out is the opposite: source in scope, destination not. Moves that stay inside the filtered tree (warehouse to its own bin) are excluded. Source comment: `InventoryActivityMatchesCategoryFilter`.
  - Under Check In/Out, transfer rows are drawn with check-in or check-out icons (`GetInventoryIconDisplayType`) and the comment is prefixed with `{{cs-transfer}}` if that tag is absent. Adjust rows that map to check-in/out get `{{cs-quantity-adjust}}` and the quantity shown is `Abs(new-old)`, not the stored content qty (`GetAdjustDisplayQuantityDelta`).
  - Those badge tags are display-only. The stored comment is unchanged. Activity Details does not call `GetCommentForInventoryDisplay`, so the badges appear on the history row, not on the details page, unless the tag was already stored.
- Code file+method+lines: `ActivityHistory.aspx` 670–702; `ActivityHistory.aspx.vb` `ApplyCategoryCSS` 54–130, `UpdateCategoryDisplay` 1145–1167, category click handlers 1332–1400, `SetButtonText` 1173–1185; `Activity.vb` `GetActivitiesList_COMPLETE` 698–743, `FilterInventoryActivitiesByCategory` 1347–1358, `InventoryActivityMatchesCategoryFilter` 1321–1345, `GetInventoryIconDisplayType` 1115–1143, `GetCommentForInventoryDisplay` 1146–1156
- Confidence: Confirmed
- Suggested KB title: Filter activity by type

### Activity date range
- Pages: `ActivityHistory.aspx` `#reportrange`, `ActivityHistory.aspx.vb` `hidden_btn_date_filter_Click`
- What it does (traced): Bootstrap-daterangepicker writes `YYYY-MM-DD` into hidden fields and postbacks. Server parses start at midnight and adds **24 hours** to the end date so the end day is included (`GetFilters`).
- How to access + visibility: Top right of Activity History. `maxDate` is today. `autoApply: true`, calendars always shown, `showCustomRangeLabel: false`, opens left.
- Steps: Open the range control, pick a preset or two dates. Apply posts back.
- Options and defaults (real values or data source): Preset keys and ranges from the script:

  | Preset label | Start | End |
  | --- | --- | --- |
  | All Time | `01/01/2011` | tomorrow (`moment().add(1, 'days')`) |
  | Today | today | today |
  | Yesterday | yesterday | yesterday |
  | Last 7 Days | today minus 6 days | today |
  | Last 30 Days | today minus 29 days | today |
  | This Month | start of month | end of month |

  Page default when hidden fields are `-1`: last 90 days through today. Dropdowns for month/year are on (`showDropdowns: true`).
- Permissions: Same as history.
- Validation/failures: Parse failure in `GetFilters` falls back to last 90 days through now. SQL compares timezone-shifted `DateAndTime` to `@P2`/`@P3` only on the unfiltered-user query.
- Result: Label format `MMMM D, YYYY - MMMM D, YYYY`. Same range is written into the CSV pre-header as short dates.
- Edge cases: "All Time" end is tomorrow while `maxDate` is today; the picker may clamp the end. "This Month" can include future days of the current month, which `maxDate` may also clamp. End-exclusive +24h is server-side only. User-filtered queries do not apply the timezone expression (see list feature).
- Code file+method+lines: `ActivityHistory.aspx` 510–580; `ActivityHistory.aspx.vb` `GetFilters` 167–177, `hidden_btn_date_filter_Click` 1137–1143; `Activity.vb` `TimeRangeExpression` 681
- Confidence: Confirmed
- Suggested KB title: Filter activity by date

### Activity user filter
- Pages: `ActivityHistory.aspx.vb` `PopulateUserFilters`, `CreateUserIconControl`
- What it does (traced): Icon row. Click sets `ViewState("UserFilter")` to the user index and postbacks. `-1` means no user predicate. Any other index loads `FirstName` from `CS_ADMIN.Users` and passes that string as `UserID=@P1` (`WHERE UserID=@P1`). The query matches the stored first name, not the index, even though the click sends the index.
- How to access + visibility: Top left of Activity History.
- Steps: Click All, Me, or another user. Clicking the name inside a row calls `ToggleUserFilter` for that user's index.
- Options and defaults (real values or data source): "All" uses index `-1` and `Images/Pages/ActivityHistory/Everyone.png`. "Me" is the signed-in user. Other users come from `User_Legacy.GetUserTable(accountId, True)`, which keeps users with `CHAR_LENGTH(FirstLoginDate) > 1` and `TypeOfUser != 'READ-ONLY'`. The signed-in user is not duplicated in that loop. Display label is the first space-delimited token of an 8-character prefix, otherwise up to 8 characters, otherwise the full name. Tooltip is the full name.
- Permissions: Same as history. Read-only users do not appear as filter chips because of the SQL above. Their past rows can still show if `UserID` was stored.
- Validation/failures: If the first-name lookup throws, the page loads with no user filter (`DisplayHistory_FAST(Nothing, ...)`).
- Result: Selected chip opacity 1 and green border via `ToggleUserDisplay`.
- Edge cases: Two users with the same first name are indistinguishable in SQL. Renamed users no longer match old rows, because `Activities.UserID` stores the name captured at registration (`RegisterActivityHelper` comment: "Saved to UserID (Legacy)"). Chip click does not reset the 15-row window.
- Code file+method+lines: `ActivityHistory.aspx.vb` `PopulateUserFilters` 243–298, `CreateUserIconControl` 300–333, `hidden_btn_user_filter_Click` 1131–1135, `LoadActivityWithFilters` 219–241; `User_Legacy.vb` `GetUserTable` 136–155; `Activity.vb` user predicate 765–766
- Confidence: Confirmed
- Suggested KB title: Filter activity by user

### Activity location filter
- Pages: `ActivityHistory.aspx` `LocationSelector_control`, `Activity.vb` location-scope SQL
- What it does (traced): Location selector postback stores `LocationID`. `-2` means no location predicate (All Locations). Any other id limits rows to that location and descendants: `LocationID = @P5 OR LocationPath LIKE '%/{id}' OR LocationPath LIKE '%/{id}/%'`.
- How to access + visibility: Top right, beside the user icons.
- Steps: Pick a location. The selector repopulates itself from viewstate on the next load.
- Options and defaults (real values or data source): Default `-2`. When a location is selected, icon labels also append the ancestor path (`FormatLocationDisplayHtml`). Tooltip is name, path, and `Barcode # {barcode}`.
- Permissions: Same as history.
- Validation/failures: Empty viewstate falls back to `-2` and `SetLocationAndPopulate(-2, ...)`.
- Result: Inventory rows must match source, destination, or per-line `SourceID`/`DestinationID` in that scope. Location create/edit/delete (`ActivityCode` 6, 7, 8) match header `LocationSourceID` or a content `ProductNumber` that parses as a location id. `LocationDestinationID` is **not** used for those three types, because create stores a location type there.
- Edge cases: Descendant match depends on `Locations.LocationPath` text. Export Report rewrites those paths; Activity History does not. Internal transfers are dropped from Check In/Out when both ends are in scope (see category feature).
- Code file+method+lines: `ActivityHistory.aspx.vb` `LocationSelector_control_LocationChanged` 1124–1128, scope setup 383–391; `Activity.vb` `BuildLocationScopeSubquery` 456–458, `BuildActivityCompleteLocationScopeWhereClause` 468–473, `FilterLocationAdminActivitiesByLocationScope` 1362–1380
- Confidence: Confirmed
- Suggested KB title: Filter activity by location

### Activity keyword search
- Pages: `ActivityHistory.aspx` `txt_comment_search`, `Activity.vb` `CommentSearchExpression`
- What it does (traced): The text box is the panel default button target. The image button `btn_comment_search` has no server click handler; the postback still reloads the list and reads `txt_comment_search.Text`. There is no operator parser.
- How to access + visibility: Right side, placeholder "search by keyword...".
- Steps: Type and press Enter, or click the search image. Client click runs `ShowTarp()` and does not cancel the postback.
- Options and defaults (real values or data source): Empty string skips the predicate. Non-empty adds:

  `comment LIKE %term% OR ActivityContents.ProductNumber LIKE %term% OR ProductName LIKE %term% OR CF_{fieldIndex} LIKE %term%` for every account custom field.

  `ProductDetailsIfDeleted` is commented out and is not searched.
- Permissions: Same as history.
- Validation/failures: Term is a bound parameter (`@P6`), not concatenated into SQL. `%` and `_` in the term are still LIKE wildcards (no escape in this expression).
- Result: Activities whose comment, product number, product name, or custom field contains the term. Because the join is on content rows, a product match returns the whole activity.
- Edge cases: No AND/OR/quote syntax. The word "operators" is not implemented. Search does not reset the show-more index. CSV pre-header includes `Comment : {term}` when non-blank.
- Code file+method+lines: `ActivityHistory.aspx` 609–614; `ActivityHistory.aspx.vb` `GetFilters` 186–201; `Activity.vb` 683–696
- Confidence: Confirmed
- Suggested KB title: Search activity history

### Activity "Show More..." pagination
- Pages: `ActivityHistory.aspx` `btn_load_more`, `ActivityHistory.aspx.vb`
- What it does (traced): Not page numbers. `StartIndex` begins at 0. Each click adds **15**. The SQL `LIMIT` is `StartIndex + 15`, so the page reloads from the newest row and shows a longer list. `BuildCompleteActivitiesSelectSql` limits **distinct activity ids**, then joins contents. The `PRODUCT_LIST_LIMIT` argument is not applied as a SQL limit (comment at `Activity.vb` 675).
- How to access + visibility: Button text "Show More...", under the list. Hidden when zero rows were rendered.
- Steps: Click the button.
- Options and defaults (real values or data source): Step size 15 (`LISTING_LIMIT`).
- Permissions: Same as history.
- Validation/failures: None.
- Result: More rows from the top of the same filter.
- Edge cases: Button appears even when every matching activity is already shown. Hover rendering stops adding lines when index `i > 10` (`If i <= PRODUCT_LIST_LIMIT`), so 11 product lines (0 through 10) can appear in the hover, and further products are counted in the total but not listed. The count label uses the full content array, not the hover cap.
- Code file+method+lines: `ActivityHistory.aspx.vb` 12–14, 380–381, 679, 1117–1122; `Activity.vb` `BuildCompleteActivitiesSelectSql` 633–654
- Confidence: Confirmed
- Suggested KB title: Load more activity

### Activity row product hover and editors
- Pages: `ActivityHistory.aspx` `ShowHover`, `callFancyBoxActivityDetails`; `ActivityHistory.aspx.vb` product block
- What it does (traced): Inventory and product activities (types 0, 2, 5, 1, 3, 4, 25) show a count chip. Hover reveals product name, number, and quantity. Create (0) and edit (5) omit quantity. Check-in with destination `-2` shows "to {location}" per line. Check-out with source `-2` shows "from {location}". Transfer shows "from {a} to {b}" as links. Adjust shows "at {location}". Product name click opens `ProductEditor.aspx?ProductNumber=`. Location click opens `LocationEditor.aspx?LoadType=EXISTING&LocationID=`.
- How to access + visibility: On rows that have content lines.
- Steps: Hover the product chip. Click a product or location in the hover, or click the row background for details.
- Options and defaults (real values or data source): Count text is `{n} Product(s)` or `{n} Products ({qty} Items)`. Singular at count 1.
- Permissions: Editors open in the parent page Fancybox. Further editor permissions are outside this audit.
- Validation/failures: If product details throw, the chip reads `{n} Products [DELETED]` and the hover lists raw product numbers.
- Result: Hover panel `#hover_{activityId}`.
- Edge cases: Deleted-product branch (`DELETED_PRODUCTS`) is never filled; the collecting loop is commented out, so the "deleted:" hover section does not run. Location delete icon is not clickable (the editor `onclick` is commented out). Location create and edit icons are clickable.
- Code file+method+lines: `ActivityHistory.aspx` 338–350, 417–449; `ActivityHistory.aspx.vb` 523–760, 831–1080
- Confidence: Confirmed
- Suggested KB title: Open an activity, product, or location from history

### Activity History CSV export
- Pages: `ActivityHistory.aspx` download image, `ActivityHistory.aspx.vb` `DownloadReport`
- What it does (traced): Image button `btn_download_report` (`Images/Icons/download5.png`, tooltip "Download spreadsheet file (.csv)") calls `DownloadReport`. Uses the **current** filters. Does not apply the 15-row page cap (`LIMIT` omitted). Runs the same category and location in-memory filters as the list. Writes a temp CSV, streams it, deletes the temp file.
- How to access + visibility: Top of Activity History, left of the date range. Checkbox "Readable Format" sits beside it.
- Steps: Set filters. Leave or clear "Readable Format". Click the download image. `beforeunload` hides the tarp after 1.5s.
- Options and defaults (real values or data source): `chk_report_group_items` text "Readable Format", **checked by default**. Tooltip: "If you need to manipulate your data more easily you can uncheck this box for a more uniform file." Checked = one summary line per activity, then product lines whose first columns are blank. Unchecked = every product line repeats date, user, activity, source, destination, comment.

  Column header constant `ActivityCsvColumnHeader`:

  `Date, User, Activity, Source, Destination, Comments, Product Number, Description, Quantity, FROM, TO, Buy Price, Sell Price, Old Quantity, New Quantity, Qty. Diff., Cost Diff.`

  Pre-header lines: report title, `Date Range : {start} to {end}`, `User : {first name}` when a user is selected, `Comment : {term}` when the keyword box is non-blank, then a blank line.

  Title: `CyberStockroom - {category label} Report`, plus ` at {location name}` when a location is selected and the name is not `[DELETED]`. Filename is `CS_FILENAME_SANITIZE(title)` trimmed to 200 characters plus `.csv`.

  Category labels for the standard account (`GetDownloadReportCategoryLabel`): 0 Inventory, 1 Checkin, 2 Checkout, 3 Transfer, 4 Products, 5 Create, 6 Delete, 7 Edit, 8 Location, 9 Create, 10 Delete, 11 Edit, 12 All Activity, 13 Adjust. Account type 1 uses Assignments, Assign, Deallocate, Transfer, Records for 0–4, and Adjust for 13. The Create/Delete/Edit words are shared by the product and location child filters, so the filename does not say which group.
- Permissions: Same as history. No separate export permission.
- Validation/failures: Commas in user, description, comment, product number, and product name are replaced with `_` (`CsvSanitize`). Location paths written into FROM/TO are **not** passed through `CsvSanitize`.
- Result: Browser download. Currency is not in this file (buy/sell prices are raw doubles from the product join: `BuyPrice`→`CheckInPrice`, `SellPrice`→`CheckoutPrice` in `PopulateActivityComplete`).
- Edge cases: Header columns "Old Quantity", "New Quantity", "Qty. Diff.", and "Cost Diff." are **never written** by `WriteActivityCsv`. Adjust rows exported while category is 1 or 2 use the absolute delta as Quantity and, for a check-in-equivalent adjust under category 1, move the formatted source into the Destination column and clear Source (`ApplyCheckInAdjustCsvLocationColumns`). Adjust export type is remapped to check-in or check-out before choosing FROM/TO columns. Create/edit/delete product lines are number and description only. When both header locations are `-2`, FROM/TO come from per-line locations. Grouped mode with no product lines writes only the summary row.
- Code file+method+lines: `ActivityHistory.aspx` 497–498, 788–793; `ActivityHistory.aspx.vb` `DownloadReport` 1255–1329, `GetDownloadReportCategoryLabel` 1187–1225, `WriteDownloadReportPreHeader` 1243–1253; `Activity.vb` `ActivityCsvColumnHeader` 878, `WriteActivityCsv` 968–1068
- Confidence: Confirmed
- Suggested KB title: Download an activity report

### Activity details
- Pages: `ActivityDetails.aspx`, `ActivityDetails.aspx.vb`
- What it does (traced): `GetActivityCompleteById` loads one activity with contents and current product fields, timezone-shifted. Renders user ("You" if first name matches), description, timestamp, comment, location rows, and a product table. Download link is the same URL with `&download=1`.
- How to access + visibility: History row click → Fancybox iframe `ActivityDetails.aspx?ActivityID={guid}`. Not in the main menu.
- Steps: Click a history row. Click a product name to open Product Editor in the **parent** window (`openParentProduct`). Click a location row to open Location Editor the same way. Click the download image for CSV.
- Options and defaults (real values or data source): Product table columns: Product, Number, and Qty unless type is create (0) or edit (5). Extra location columns only when **both** header location ids are `-2`:
  - check-in: "To"
  - check-out: "From"
  - adjust: "Location"
  - transfer: "From" and "To"
  - other types: no extra columns even if per-line locations exist, except the header location list from `CollectFromToLocationIds`
- Permissions: Login. No extra flag. Download of a missing id returns status 404 and ends the response.
- Validation/failures: Empty or unknown id: panel text "Activity not found" / "This activity may have been removed or is not available on this account." SQL errors return the same empty listing. Blank product numbers are stripped (`StripEmptyActivityProducts`). Blank product name displays `[DELETED]`.
- Result: Full product list (no 10-line cap). Qty is `Max(QuantityIn, QuantityOut)`. Location path uses `GetFormattedValuePath` and is shown in parentheses when it differs from the name.
- Edge cases: Comment quotes are omitted for location create/edit/delete and product create only. Product edit **is** quoted here; on the history list, product create is the one excluded (the history `Select Case` lists `PRODUCT__CREATE` three times and never `PRODUCT__EDIT` or `PRODUCT__DELETE`). Details CSV always calls `WriteActivityCsv` with `groupItems=True` and `category=12`, so check-in adjust column swapping does not apply. Details do not re-badge transfer/adjust for the check-in filter. There is no undo and no edit of the comment on this page (`WriteComment` exists on `Activity` and is not called here).
- Code file+method+lines: `ActivityDetails.aspx.vb` `Page_Init` 17–42, `RenderDetails` 74–114, `RenderLocations` 116–135, `RenderProducts` 251–365, `StreamCsv` 49–72; `Activity.vb` `GetActivityCompleteById` 880–927; `ActivityDetails.aspx` 233–247, 252–278
- Confidence: Confirmed
- Suggested KB title: View one activity and download it

### Header activity popup (recent inventory)
- Pages: `UserPage.master` activity icon and `#div_activity_summary`, `UserPage.master.vb` `CreateNotificationSummary`
- What it does (traced): On every `UserPage.master` page, including Activity History, Expirations, Kitting, and AI report, the header builds a short list of recent **inventory** rows and links to Activity History.
- How to access + visibility: Activity icon. Popup button text "View Activity History".
- Steps: Open the popup. Click the button or the icon (`simpleRedirect('ActivityHistory')`).
- Options and defaults (real values or data source): First query is category **0** (codes 1, 3, 4, 25), from two years ago through now, `ONLY_DISPLAYABLE=True`, limit `5 * 2 = 10`. If that returns nothing, a backup query uses category **2** (codes 3, 4, 25) — the backup is the check-out SQL list, not "all activity". Display keeps at most **5** rows, and the loop then skips any type that is not check-in, check-out, transfer, or adjust. So the popup can show fewer than five even when the query returned five.
- Permissions: Same login as the master page.
- Validation/failures: None on screen. `GetActivitiesList` for category 2 does **not** run `FilterInventoryActivitiesByCategory`, so transfers and all adjusts can appear in the backup list without the check-in/out direction rules used on the history page.
- Result: Avatar, description, comment badges, time. Comment for the current user is suffixed " - You"; for others it is suffixed with `UserIndex` (the numeric index), not the name (`AppendNotificationActivityRow` 235–238).
- Edge cases: Popup rows are not clickable to Activity Details. Only the "View Activity History" button navigates.
- Code file+method+lines: `UserPage.master.vb` `CreateNotificationSummary` 155–198, `AppendNotificationActivityRow` 200–275; `UserPage.master` 1390–1396
- Confidence: Confirmed
- Suggested KB title: Recent activity in the header

### Registering an activity (write path, not a screen)
- Pages: `Activity.vb` `RegisterActivity` / `RegisterActivityHelper`. Called from check-in, check-out, transfer, quantity adjust, location create/delete, and `ConfirmationDialog` (checkout-then-delete). Not called by the history page.
- What it does (traced): Inserts `Activities` (new GUID, user first name, activity code, timestamp `yyyy-MM-dd HH:mm:ss`, source, destination, comment, user index) and `ActivityContents` rows. Also issues `ALTER TABLE` on `ActivityContents` on every complete-list read and on every register (add `ProductDetailsIfDeleted`, `SourceID`, `DestinationID`, and a four-column primary key). Failures there are unhandled in this method.
- How to access + visibility: No history-page control. Users create rows by checking in, checking out, transferring, adjusting, creating or deleting locations, and by the expiration replacement API (server outside this repo; the page only sends a comment).
- Steps: Not a user flow on Activity History.
- Options and defaults (real values or data source): A content row is inserted only when the product number length is `> 0` **and** the quantity is `> 0`. Location ids default `-2`. `LOCATIONS_REQUIRED=True` forces both header location ids to `-2` and keeps per-line locations.
- Permissions: Whatever page called `RegisterActivity`.
- Validation/failures: `INSERT IGNORE`. Per-row exceptions are swallowed.
- Result: New GUID returned. Comment can be updated later with `WriteComment` (not used by the pages in this audit).
- Edge cases: Zero-quantity lines are dropped, so an activity with only zero qty lines can exist as a header with no contents and then be hidden on the history page. No undo, no delete-activity method in this class.
- Code file+method+lines: `Activity.vb` `RegisterActivity` 245–326, `RegisterActivityHelper` 330–409, `ConstructActivityContent` 187–204
- Confidence: Confirmed
- Suggested KB title: What gets stored as an activity

---

### Expiration list, colors, and counts
- Pages: `Expirations.aspx`, `Expirations_read_only.aspx`, both codebehinds, `ProductExpirations.vb` is not used by the list
- What it does (traced): On load, counts every product returned by `productRepository.getByExpiration` (page 1, page size `10000000`, empty search). Then the browser GETs `https://code.cyberstockroom.com/api/expiration?pageIndex=1&pageSize=100&searchTerms=` with header `X-CS-TOKEN` from the `csToken` cookie. Each row is `{product.uid} - {product.description}` plus a status, and opens `ProductEditor.aspx?ProductNumber=` in Fancybox.
- How to access + visibility: Header image `#expiration_icon` and collapsed menu `#collapse-menu-expiration` ("Expirations") only when `hidden_expiration_on` is `1` (`SHOW_EXPIRATIONS`). Direct URL `/Expirations` redirects to Settings if the flag is off, or to the read-only page if the user is read-only.
- Steps: Open Expirations. Read the two count chips. Click a row for the product editor. On the editable page, click "manage" for the replacement wizard.
- Options and defaults (real values or data source): Client `pageSize = 100`, `pageIndex = 1`. Search box placeholder "search...". Colors, compared on the **date only** (time zeroed):

  | Condition | CSS class | Colors | Text |
  | --- | --- | --- | --- |
  | expiration date **<** today | `alert-danger` | background `#AF5756`, white text | `expired ({yyyy-mm-dd})` |
  | window `> 0` and expiration date **<=** today + window days | `alert-warning` | background `#FFD966`, text `#454545` | `will expire in {diffDays} days ({date})` |
  | otherwise | `alert-standard` | background `#EEEEEE`, border `#BBBBBB`, text `#454545` | `will expire on {date}` |

  Count chips: "Expiring Soon" `#FFD966` / `#454545`; "Expired" `#AF5756` / white. Chip counts use server `Now` (includes time): `expirationDate <= Now` is expired; else if window `> 0` and `expirationDate <= Now.AddDays(window)` it is expiring soon. The list uses date-only `< today` for the red state. A product expiring later **today** can be in the red count and in the yellow or grey list, or the reverse, depending on the time component.
- Permissions: `SHOW_EXPIRATIONS`. Read-only: list and product click only. The read-only markup does not render "manage" or the wizard.
- Validation/failures: API error handler is empty (editable page) or logs nothing useful. Duplicate `uid`s in one response are skipped (`isOnDisplay`). Missing token: the request still goes out with an empty header; `ProductExpirations.Save` would no-op, but this list does not call that class.
- Result: Rows in `#expirationList`. Counts in `#count-expired` and `#count-expiring-soon`.
- Edge cases: `searchTerms` is concatenated, not `encodeURIComponent`. No page controls: page index stays 1 and page size stays 100, so products past the first 100 API rows are counted in the chips (server count uses up to 10,000,000) but not listed. Keypress handler checks `e.keycode` (wrong case) so Enter-in-wizard prevention likely does not run. Date string is cut at the first `T`. `diffDays` can be 0 for "today" when today is not `<` expDate; today is not red on the list (`<` not `<=`). If the window is 0, the yellow chip gets class `count-expiring-soon-hidden` and no row is yellow. JS default `expiringSoonWindowDays = 60` is overwritten by the hidden field; `parseInt(...) || 0` turns `NaN` into 0.
- Code file+method+lines: `Expirations.aspx` `getExpirations` 54–84, `addListing` 90–149, colors 173–216 and 279–292, search input 305; `Expirations.aspx.vb` `Page_Init` 14–40, `_getExpirationCounts` 47–70; `Expirations_read_only.aspx` `addListing` 88–136 (no manage button); `Expirations_read_only.aspx.vb` 14–23
- Confidence: Confirmed for page behavior. The API's match rules for `searchTerms` are not in this repo (Uncertain).
- Suggested KB title: See which products are expired or expiring

### Expiring soon window
- Pages: Settings UI is outside the page list but is the only writer; Expirations reads it. `Gridster_Utilities.GetExpiringSoonWindowFromRaw`, `js/business/general-settings.js`, `webAPI/settings.aspx.vb` `SaveExpiringSoonWindow`
- What it does (traced): The window is a day count stored in the user's map coordinate string as the pair `-18,{days}`. Absent token (`-1` marker) means **60** days (`DefaultExpiringSoonWindowDays`). Stored `0` means disabled (no yellow state, chip hidden).
- How to access + visibility: Settings, under the Expirations toggle (`#expirationsAnchor` is actually on the previous row; `#kittingAnchor` is the empty section immediately above the Expirations toggle). The Expiring Soon block is shown only when the Expirations toggle is on. Turning Expiring Soon on while Expirations is off alerts "Enable Expirations before using Expiring Soon." The same sentence is thrown by `SaveExpiringSoonWindow`.
- Steps: Enable Expirations. Enable Expiring Soon. Set number and unit. Click "save" (or change the number, which also saves via `toggle.js`).
- Options and defaults (real values or data source): Number input `min=1`, default value **60**, unit options exactly: `days`, `weeks`, `months`, `years`. Conversion in `toExpiringSoonDays`: weeks `* 7`, months `* 30`, years `* 365`. Display picks the largest unit that divides the stored days (365, then 30, then 7, else days). Saved value is days, including 0 when the toggle is off. Invalid or non-positive alerts "Expiring soon window must be a valid duration greater than 0."
- Permissions: Settings save requires `webAPI_Utilities.isAllowed`. Expirations must already be enabled to store a positive window.
- Validation/failures: Toggle failure adds `toggle-error` and reverts the checkbox after 1.5s.
- Result: Next Expirations load (and the map, which reads the same helper) uses the new day count.
- Edge cases: Month=30 and year=365, not calendar months. A 60-day window displays as 60 days (60 is not divisible by 7). Turning the feature off stores 0, which is different from "token absent" (60).
- Code file+method+lines: `Gridster_Utilities.vb` constants 56, 74–75, `GetExpiringSoonWindowFromRaw` 702–707, `ApplyExpiringSoonWindowToCombined` 987–1015; `general-settings.js` `toExpiringSoonDays` 408–417, `initializeExpiringSoonControls` 494–510, `handleExpiringSoonToggle` 512–558; `webAPI/settings.aspx.vb` `SaveExpiringSoonWindow` 144–166; `Settings.aspx` 491–518
- Confidence: Confirmed
- Suggested KB title: Set the expiring soon period

### Replace or clone an expired product
- Pages: `Expirations.aspx` wizard `#wizard`. The same markup is copied into `Kitting.aspx` (see kitting feature). Read-only expirations omit it.
- What it does (traced): "manage" fills the modal title with description, uid, and date, and stores `data-uid`. Save POSTs `https://code.cyberstockroom.com/api/expirationReplacement?action={action}` with headers `X-CS-TOKEN`, `X-CS-EXPIRATION-OLD-UID`, `X-CS-EXPIRATION-NEW-UID`, `X-CS-EXPIRATION-NEW-DATE`, `X-CS-COMMENT`. Success navigates to `ActivityHistory`. The replacement work itself is not implemented in this website project.
- How to access + visibility: "manage" on each editable expiration row. Modal title "Manage this product's expirations".
- Steps: Click manage. Pick a future date. Enter a new product number or check Auto. Pick a radio (default is already selected). Click the green button.
- Options and defaults (real values or data source): Radio value, button label, `data-action`, and the disabled checklist the UI shows. Default radio is value `1` ("Replace and Delete"). The footer button's initial HTML is "Replace" while `data-action` is already `replace_delete`; the label updates only after `toggleRadio` runs. Image shown by default is `Images/Pages/Expirations/replace_delete.png`.

  | Radio | Button label | `action` query | Checklist left enabled in the UI |
  | --- | --- | --- | --- |
  | Replace and Delete | Replace and Delete | `replace_delete` | Check-out old product from all locations. Delete the old product. Create a new product. Check-in new product to the same locations. |
  | Replace only | Replace only | `replace` | Same, except "Delete the old product." is greyed and unchecked |
  | Clone and Delete | Clone and Delete | `clone_delete` | Check-in new product is greyed and unchecked |
  | Clone and Check-out | Clone and Check-out | `clone_checkout` | Delete old and check-in new are greyed |
  | Clone only | Clone only | `clone` | Check-out old, delete old, and check-in new are greyed. "Create a new product." stays checked |

  Checkboxes are `disabled`; they are a legend, not inputs. Comment sent:

  `Replacing expired product -  [Replace and Delete]` (and the matching bracket text for the other four actions). Note the two spaces before the bracket.

  Auto SKU: checkbox label "Auto". Checked value becomes the literal `[Automatic Product Number]`, and save substitutes `auto_sku_identifier` from `productRepository.get_AUTO_SKU_IDENTIFIER`.
- Permissions: Editable expirations page only (`SHOW_EXPIRATIONS`, not read-only).
- Validation/failures: Empty date: "You must select an expiration date." Date where `date_diff_indays(today, picked) <= 0`: "This date has already passed!" and the input turns `#AF5756`; save does not re-check that warning, it only checks empty. A date of today fails the onchange warning (`<= 0` because the helper adds 1 then floors, and same-day UTC diff is 0). Empty product number: "You must select a product number." Existing number: synchronous GET `https://code.cyberstockroom.com/api/products/CS_PRODUCT_IN_HEADER` with `X-CS-PRODUCT-NUMBER`. HTTP success means it exists and save stops with "That product number already exists!" HTTP error means it does not exist and save continues. API failure on the replacement POST only `console.log`s; the modal has already been faded to opacity 0. Cancel button text "Cancel".
- Result: Browser goes to Activity History. Which activity rows the API writes is outside this repo.
- Edge cases: Passed-date warning does not block save. Auto identifier is not checked for collision after substitution (the existence call uses the identifier string). Product number is not URL-encoded in the header.
- Code file+method+lines: `Expirations.aspx` `checkDate` 334–353, radios 444–590, `save` 614–660, `_post` 662–706, `_uidExists` 708–728; `Expirations.aspx.vb` 34–35 (`auto_sku_identifier`)
- Confidence: Confirmed for the wizard. What each `action` does to inventory is Uncertain (API not in this repo).
- Suggested KB title: Replace or clone an expiring product

### Saving and deleting expiration dates (service, not the list page)
- Pages: `ProductExpirations.vb`. Used from product save/delete and import, not from `Expirations.aspx`.
- What it does (traced): `Save` POSTs `application/x-www-form-urlencoded` to `https://code.cyberstockroom.com/api/expiration` as `Expirations[i][productUID]` and `Expirations[i][expirationDateTime]`. `Delete` DELETEs `https://code.cyberstockroom.com/api/expiration/CS_PRODUCT_IN_HEADER` once per product number, header `X-CS-PRODUCT-NUMBER`.
- How to access + visibility: No button on the Expirations page. The list does not edit the date in place.
- Steps: Happen inside product editor / import / product delete (out of scope except this class).
- Options and defaults (real values or data source): No-op when the dictionary is empty or the `csToken` cookie is missing/blank.
- Permissions: Token cookie.
- Validation/failures: All exceptions, including HTTP errors, are empty `Catch`. Callers are not told the save failed.
- Result: Silent success or silent failure.
- Edge cases: Delete uses the literal path segment `CS_PRODUCT_IN_HEADER` and passes the real uid only as a header.
- Code file+method+lines: `ProductExpirations.vb` `Save` 7–45, `Delete` 47–77
- Confidence: Confirmed
- Suggested KB title: Where expiration dates are stored

---

### Kit list
- Pages: `Kitting.aspx`, `Kitting.aspx.vb`
- What it does (traced): Counts kits with `kitRepository.getAll` (page 1, size `10000000`) into "N Kits". Browser GETs `https://code.cyberstockroom.com/api/kit?pageIndex=1&pageSize=100&searchTerms=` with `X-CS-TOKEN`. Each kit shows the name in `#00A27D`, then `{content.length} Products included`. Clicking the row toggles a component list (`toggleSubListing`).
- How to access + visibility: Header image `#kitting_icon` only when `hidden_kitting_on` is `1`. There is **no** collapsed-menu Kitting link (Expirations has one; Kitting does not). Direct `/Kitting` without the flag redirects to `Settings#kittingAnchor`. The Settings checkbox `toggle_show_kitting` (label "Kitting") sits in `<tr style="display: none;">`, so the switch is not visible. Nothing else in this repo sets `SHOW_KITTING`. The flag is read from `CS_ADMIN.Users.SHOW_KITTING` (`Account.vb` 880–884).
- Steps: Open Kitting. Click a kit to expand components.
- Options and defaults (real values or data source): `pageSize` 100, `pageIndex` 1. Count chip class uses the page CSS for kits (the visible string is `{n} Kits`).
- Permissions: `SHOW_KITTING`. Read-only redirect target `Kitting_read_only` is missing from the repo, so a read-only user with the flag on is sent to a URL this project does not implement.
- Validation/failures: GET error logs `xhr[0]`. Empty list leaves `#kitsList` empty. The count can be larger than the 100 rendered rows.
- Result: Kit rows. No build action and no break action exist in this file. Those words are not in `Kitting.aspx`.
- Edge cases: `addListing` is declared `function addListing(product)` but reads the global `kit` from the loop. Component markup injects `productUID` and `name` into inline JavaScript strings without encoding.
- Code file+method+lines: `Kitting.aspx` `getKits` 46–89, `addListing` 109–186, search box 511; `Kitting.aspx.vb` `Page_Init` 13–35, `_getkitCounts` 37–46; `UserPage.master` 1354–1384; `Settings.aspx` 526–536
- Confidence: Confirmed
- Suggested KB title: View kits

### Create a kit
- Pages: `Kitting.aspx` `createNewKit`
- What it does (traced): Button "+ NEW KIT" prompts "New Kit Name:" and POSTs JSON to `https://code.cyberstockroom.com/api/kit`: `{"id":-1, "name":"{typed}", "content":[]}`. Success clears `KitsRaw` and reloads page 1 with an empty search.
- How to access + visibility: Top right of the kit search row.
- Steps: Click + NEW KIT. Enter a name. Accept the prompt.
- Options and defaults (real values or data source): New id is the number `-1` (stringified). Content is an empty array. No description, location, or quantity fields.
- Permissions: Same as the kit page.
- Validation/failures: Cancel (`null`) still posts, and the name becomes the string `null` because it is concatenated. Empty string posts `"name":""`. No trim, no duplicate check. POST error is swallowed. No confirm.
- Result: List refresh. Whether id `-1` means "insert" is defined by the API (not in this repo). The local reload uses `searchTerms` empty even if the search box has text.
- Edge cases: Quotes in the name break the hand-built JSON.
- Code file+method+lines: `Kitting.aspx` `createNewKit` 544–548, `sendKitContent` 293–314
- Confidence: Confirmed for the request. API persistence rules: Uncertain.
- Suggested KB title: Create a kit

### Kit components (add, quantity, remove)
- Pages: `Kitting.aspx` component row, `#addItemToKit`, `changeQty`, `deleteItem`, `selectProduct`
- What it does (traced): Expanded kit lists `{qty} x {description} ({productUID})`. The quantity number calls `changeQty`. "x" calls `deleteItem`. "+ Add New" opens modal "Add Item to Kit : {name}". That modal searches `https://code.cyberstockroom.com/api/products?pageIndex=1&pageSize=10&searchTerms={term}` and lists `description (uid)`. Click, or Enter, calls `selectProduct`, which calls `changeQty(kitId, uid, 1, kitName)`. `changeQty` prompts "Please enter the new quantity for Product : {uid} in Kit: {name}". `deleteItem` confirms "Are you sure you want to remove this item from the kit?" Then both POST the full kit JSON to `api/kit`.
- How to access + visibility: Inside an expanded kit.
- Steps: Expand kit. Click + Add New, search, pick a product, answer the quantity prompt. Or click the green quantity and answer the prompt. Or click x and confirm.
- Options and defaults (real values or data source): Product search page size **10**, page index 1. Enter in the product box selects `response[0]` only. Prompt cancel or `newQty <= 0` returns without POST. `newQty` is a string from `prompt`.
- Permissions: Same as the kit page.
- Validation/failures: Confirm is the only delete check. No numeric check beyond `<= 0` (non-numeric text is not `<= 0` in JavaScript, because `NaN <= 0` is false, so it continues).
- Result: Intended result is an updated kit content array and a list refresh.
- Edge cases: **Quantity edit does not write the new quantity.** When the product is already in the kit, the JSON uses `kit.content[j].quantity` (the old qty). `newQty` is appended only when the uid was not found. `selectProduct` always passes original qty `1` and then `changeQty` prompts, but an existing line still keeps the old qty. **Remove drops the wrong lines.** The keep condition is `productUID != target AND quantity != originalQty`. Any other component with the same quantity is omitted, and the targeted line is omitted. Trailing commas can be written into the JSON when a later line is skipped. Adding a product therefore depends on the prompt and on the product not already being in `KitsRaw`. There is no "build kit into inventory" and no "break kit" operation.
- Code file+method+lines: `Kitting.aspx` `changeQty` 197–255, `deleteItem` 257–291, `getProducts` 576–614, `selectProduct` 629–638, modal 643–674
- Confidence: Confirmed
- Suggested KB title: Add or remove products in a kit

### Delete a kit
- Pages: `Kitting.aspx` `deleteKit`
- What it does (traced): Button "Delete Kit" on the row DELETEs `https://code.cyberstockroom.com/api/kit/{id}` with `X-CS-TOKEN` and an empty body. No confirm. Success reloads the first page of kits with an empty search.
- How to access + visibility: On each kit row, appended inside the listing div, so a click also hits the row toggle.
- Steps: Click Delete Kit.
- Options and defaults (real values or data source): None.
- Permissions: Same as the kit page.
- Validation/failures: Error swallowed. No undo.
- Result: List refresh after HTTP success.
- Edge cases: The button is inside the clickable listing, so the expand handler also runs. Id is interpolated into the URL with no encoding.
- Code file+method+lines: `Kitting.aspx` `deleteKit` 316–336, button 175–178
- Confidence: Confirmed
- Suggested KB title: Delete a kit

### Kit search
- Pages: `Kitting.aspx` `#searchFilter`
- What it does (traced): `onkeyup` calls `getKits(event, 1, 100, this.value)`. Enter's `onkeydown` calls `preventDefault`. No operators. `searchTerms` is not encoded.
- How to access + visibility: Above the list, placeholder "search...".
- Steps: Type. Each keyup replaces the list.
- Options and defaults (real values or data source): Always page 1, page size 100.
- Permissions: Same as the kit page.
- Validation/failures: API decides the match. This repo does not show which kit fields are searched.
- Result: Filtered kit rows, or an empty list.
- Edge cases: Fast typing can complete out of order (no request sequence number, unlike the header search). Create/delete refresh ignores the text still in the box.
- Code file+method+lines: `Kitting.aspx` 511, `getKits` 46–63
- Confidence: Confirmed for the call. Match rules: Uncertain.
- Suggested KB title: Search kits

### Kitting "manage" modal (expiration wizard copy)
- Pages: `Kitting.aspx` `#wizard`
- What it does (traced): The kit page includes a second modal whose labels are the expiration replacement wizard: "New Expiration Date", "New Product Number", Replace and Delete, Replace only, Clone and Delete, Clone and Check-out, Clone only, and the same `api/expirationReplacement` POST. The "manage" button tries to set `#modal_kit_content` and then open this modal. The generated script is not valid JavaScript: `innerHTML=` is concatenated with the kit name without quotes (`addListing` line 165), so the click throws before the modal logic runs. `auto_sku_identifier` is declared and the hidden field exists, but `Kitting.aspx.vb` never assigns it (unlike Expirations).
- How to access + visibility: "manage" button on each kit row.
- Steps: Clicking manage does not complete the wizard as written.
- Options and defaults (real values or data source): Same five actions as the expiration wizard, if the modal were opened another way. Default image and `data-action="replace_delete"`. Footer button initial text "Replace".
- Permissions: Same as kitting.
- Validation/failures: Same date and product-number checks as Expirations, if `save` were reached. `old_uid` would be the kit id stored on the title, not a product uid.
- Result: Not a kit build or kit break. Success path would still be `window.location.href = "ActivityHistory"`.
- Edge cases: This block is a copy of `Expirations.aspx`, including image paths under `Images/Pages/Expirations/`. It should not be documented as a working kitting feature.
- Code file+method+lines: `Kitting.aspx` 165–169, 676–1062
- Confidence: Confirmed
- Suggested KB title: Do not document as a kit action (dead expiration copy)

---

### Download product report (Export Report)
- Pages: `ExportReport.aspx`, `ExportReport.aspx.vb`. Linked from `Products.aspx` (`btn_export_report` tooltip "Download Product Report", Fancybox on `#hidden_clicker_export_report`). Not linked from Activity, Expirations, or Kitting.
- What it does (traced): "Download Product Report". User picks fields and clicks "Download File". Before the query, `sanitizeLocationPathAndReturnReadablePaths` **rewrites every `Locations.LocationPath` in the account** from parent links, then the CSV is built from `Products` left-joined to `Quantities`.
- How to access + visibility: Products download icon opens this page in a Fancybox iframe. Query `LocationID` selects the location. Changing the selector redirects to `ExportReport?LocationID={id}`.
- Steps: Open from Products. Choose location. Set the two include-checkboxes and the field checkboxes. Click Download File.
- Options and defaults (real values or data source):

  | Control | Default | Effect |
  | --- | --- | --- |
  | Location selector | query `LocationID`, or the selector's own populate | `-2` is all locations. The sub-location checkbox is **hidden** when query `LocationID` is `-2`. |
  | Include Products with 0 Quantity | unchecked | When checked, products that are not already in the positive-qty result are appended with quantity 0. Also forced on when the positive-qty query returns **zero rows**. |
  | Include Products in Sub-Locations | unchecked | When checked and location is not all, SQL is self-and-descendants (`LocationID = id OR LocationPath LIKE '%/id' OR '%/id/%'`). |
  | Product Number | checked, **disabled** | Always selected. Header "Product Number". |
  | Description | checked | `ProductName` → header "Description". |
  | Quantity | checked | Sum, or per-location qty. Unchecking disables "breakdown by location" in the browser. |
  | breakdown by location | checked | Adds "Location Path" and "Location Name". SQL does not `GROUP BY` and keeps `LocationID`. Path is `Parent > … > Name` from the rewrite. Name is the segment after the last `>`. |
  | Buy Price | checked | Header `Buy Price ({currency})`. Currency is `AccountSettings.Currency`. |
  | Cost Value | checked | Header `Cost Value ({currency})`. Value is `Round(quantity * buyPrice, 2, AwayFromZero)` using invariant decimals, formatted `F2`. If this is on and Buy Price or Quantity is off, those columns are still queried and then removed after the cost column is filled. |
  | Sell Price | checked | Header `Sell Price ({currency})`. |
  | One checkbox per custom field | all checked | Label is `FieldName`. Header replaces commas with `_`. SQL column `CF_{FieldIndex}`. |
  | Product Image | unchecked | Adds column "Image URL" from `imageProcessor.getProductImage(productNumber)`. |

  Positive quantity filter is `` Quantity > 0 ``. Join is `LEFT JOIN`. Filename is the readable location path plus `  - [DATE : {Now.ToLongDateString}]`, sanitized, max 200 characters, or `ALL LOCATIONS  - [DATE : {long date}]` when the path is empty. Extension `.csv`.
- Permissions: Logged-in. No read-only check on this page. `RegisterPage` name `ExportProductReport`.
- Validation/failures: Download exceptions are swallowed. `DataSet2CSV` is the writer (shared tool). If zero-qty is combined with location breakdown, the inactive query does **not** select `LocationID` (`FieldsSQLGet(..., ActiveProducts:=False)`), then `Merge`s into the location-shaped table.
- Result: CSV download. Side effect: location paths in the database are updated for the whole account on every download.
- Edge cases: `SQL_CLAUSE_SEARCH` is always empty; this page does not apply the Products search box. Cost and buy price use SQL column order, then `AppendCostValueColumn` looks up columns named `BuyPrice` and `Quantity`. A location named with `>` will split the name wrong. Sub-location SQL reads `LocationPath` after the rewrite in the same request, so the descendant list uses the cleaned paths.
- Code file+method+lines: `ExportReport.aspx` 51–122; `ExportReport.aspx.vb` `Page_Init` 17–30, `ExportReport` 51–167, `DownloadFile` 353–418, `AppendCostValueColumn` 317–351, `GetInactiveInventory` 481–502, `location_selector_LocationChanged` 519–521; `Products.aspx` 146–147, 456, 662
- Confidence: Confirmed
- Suggested KB title: Download a product report

### AI insights report
- Pages: `ai-report.aspx`, `ai-report.aspx.vb`
- What it does (traced): User-facing page. `Page_Init` loads `SDK.Reports.AI.InsightsReport(accountId).getReport(Request.QueryString("id"))`. Header is fixed text "Your Inventory Insights" plus `dateGenerated.ToLongDateString`. Badge text "AI-GENERATED". Each content item is a card: title, italic bullet paragraphs, footer "RECOMMENDATION" plus the recommendation string. A badge image is chosen from `reportContentItemType`: `General` → `/Images/Icons/card-general.png`, `Location` → `card-location.png`, `Product` → `card-product.png`, `User` → `card-user.png`. The badge image is added **before** the card div, as a sibling, not inside the card.
- How to access + visibility: **No menu link, no href, and no `Response.Redirect` to `ai-report` anywhere else in this repo.** A user can open `/ai-report?id={id}` directly if they know the id. Any exception, including a bad id, redirects to `Map`. `userFeedback` is read and not displayed. There is no export and no print button on the page.
- Steps: Open the URL with an id the SDK can load.
- Options and defaults (real values or data source): Query key `id` only. Card types are the four enum names above. Titles, bullets, and recommendations come from the report object. The SDK project is not source in the files read here (`Imports SDK.Reports.AI.InsightsReport`).
- Permissions: Login. `RegisterPage(..., "ai-report", ...)`. No `SHOW_*` flag.
- Validation/failures: `Catch` redirects to Map with no message. HTML for bullets and recommendations is assigned as `.Text` / literal HTML, so the report strings are not encoded.
- Result: A stack of cards under the date.
- Edge cases: Unlinked. Treat as a page a person can view, not as a feature discovered from Activity, Expirations, or Kitting. Empty `contents` shows only the header.
- Code file+method+lines: `ai-report.aspx.vb` `ai_report_init` 13–27, `displayHeader` 37–40, `displayInsight` 42–76, `cardTypes` 134–139; `ai-report.aspx` 116–131
- Confidence: Confirmed that it is user-facing and unlinked. How reports are generated and which ids exist: Uncertain (SDK).
- Suggested KB title: Open an AI inventory insights report

---

### Global header search
- Pages: `Controls/CS_SearchBox.ascx`, `CS_SearchBox.ascx.vb`, wired by `UserPage.master` / `UserPage.master.vb` `CreateAutoCompleteGlobal`
- What it does (traced): One text box in the top toolbar. Autocomplete `minLength` is **0**. Each request GETs `https://developers.cyberstockroom.com/api/search?API_TOKEN_ADMIN={cookie}&LIMIT=10` with query `term`. A newer response or a term that no longer matches the box is discarded. Results render with `item.icon`, `item.label`, and `item.desc`. Category headers render when `item.category` changes.
- How to access + visibility: Left side of the main toolbar on `UserPage.master` (`CS_SEARCHBOX1`). Placeholder is empty (`placeholder=""`). Read-only users still see it (`HideSectionsForReadOnlyUsers` does not hide the search box).
- Steps: Type. Click a row, or press Enter (the panel default button calls `custom_search`).
- Options and defaults (real values or data source): Limit **10**. Local product/location markup is **off**: `CreateAutoCompleteGlobal` sets `AC.AC_Locations = False` and `AC.AC_Products = False` with the comment "Set to false to use API data instead". `AUTOCOMPLETE_Enabled` is true, but `POPULATE_AUTOCOMPLETE_DATA` then adds nothing, so the hidden `AUTOCOMPLETE_DATA` field is empty. The in-page `source_data` parser (semicolon records `label,value,category,desc,icon`, product labels split on `||||`) is leftover and is not what the widget uses; the widget `source` is the remote function.

  Click behavior by `item.category` string:

  | Category | Navigation |
  | --- | --- |
  | `Products` | Cookie `COOKIE_AUTOCOMPLETE_PRODUCT_QUERY={value}`. Opens Fancybox `ProductEditor.aspx?ProductNumber={value}` via `#autocomplete-product-selector`. |
  | `Locations` | Cookie `COOKIE_AUTOCOMPLETE_LOCATION_QUERY={value}`. Opens Fancybox `LocationEditor.aspx?LoadType=EXISTING&LocationID={value}`. |
  | anything else | Falls into the mirror branch. |
  | synthetic `createProduct` | "Create New Product {term}". See the next feature. |

  Server handlers `CS_SEARCHBOX1_AC_ProductSearched` and `CS_SEARCHBOX1_AC_LocationSearched` only read the query string and do not redirect. Navigation is the Fancybox. Suppress-popup flags stay `"FALSE"` because the assignments in `Autocomplete_Initialize` are commented out.

  Closing the product Fancybox reloads the page if cookie `CookieRefreshRequired=1` or `COOKIE_PRODUCTS_PAGE_RELOAD=TRUE`. Closing the location Fancybox goes to `Products.aspx` if `REDIRECT_TO_PRODUCTS_REQUIRED=TRUE`, else reloads if `REFRESH_MAP_REQUIRED=TRUE`.
- Permissions: Login. API uses cookie `API_TOKEN_ADMIN`.
- Validation/failures: AJAX error returns an empty list (no create-product row on errors). Demo product numbers containing `CS_DEMO_` use `Images/Pages/Products/{value}.png`; other rows fall back to `Images/Icons/cam_small.png` on image error.
- Result: Product editor, location editor, Products page (Enter), or Add Products.
- Edge cases: **No search operators** are parsed. The term is sent as the `term` parameter. Which fields the API matches is not in this repo. The suppress-location branch is split across two lines (`JS_HANDLE__FORCE_LOCATION_` then `SEARCH.click();` at `CS_SearchBox.ascx` 207–208). That is invalid JavaScript inside `RegisterUserControlIndex`. The header never requests suppress mode, but the parser still has to accept the function. The non-product/location branch uses `if (MIRROR_DISPLAY = "TRUE")`, which assigns and is always true. `Autocomplete.vb` still knows how to emit local records for products (name, number, custom fields, icon), locations (`PATH > NAME`, id, category `Locations`), and custom-field terms (`term___,,{fieldIndex},,Images/Icons/right-arrow.png`). Those records are not loaded for the header. Batches, users, and settings are fields on `AutoCompleteSettings` and their events are commented out. Stale result race is guarded by `searchboxRequestSeq`.
- Code file+method+lines: `CS_SearchBox.ascx` `RegisterUserControlIndex` 67–266, `custom_search` 270–276, Fancybox 322–409; `CS_SearchBox.ascx.vb` `Autocomplete_Initialize` 40–53, `POPULATE_AUTOCOMPLETE_DATA` 58–98, click handlers 100–128; `UserPage.master.vb` `CreateAutoCompleteGlobal` 285–297, search events 329–344; `Autocomplete.vb` `GetProductMarkup` 44–86, `GetLocationMarkup` 87–111
- Confidence: Confirmed for the client. API result categories beyond the two strings this script handles: Uncertain.
- Suggested KB title: Search products and locations from the header

### Header search Enter (keyword on Products)
- Pages: `CS_SearchBox.ascx` `custom_search`, `UserPage.master.vb` `CS_SEARCHBOX1_AC_QuerySearchRequested`
- What it does (traced): Enter or the hidden default button writes cookie `COOKIE_AUTOCOMPLETE_CUSTOM_QUERY` to the raw text, shows `#tarp2`, and clicks `FORCE_CUSTOM_SEARCH`. The server appends `,` + that string onto `COOKIE_PRODUCT_SEARCH_FILTER` and redirects to `/Products.aspx`.
- How to access + visibility: Focus the header box and press Enter.
- Steps: Type a term. Press Enter. Land on Products.
- Options and defaults (real values or data source): The term is not parsed into operators here. Products then applies its own filter cookie (not part of this control).
- Permissions: Login.
- Validation/failures: If the autocomplete cookie is missing, the server handler does nothing (no redirect).
- Result: Products page with the term appended to the product search filter cookie.
- Edge cases: Master `Page_Init` clears `COOKIE_PRODUCT_SEARCH_FILTER` when the current path does not contain "Products" or "ProductEditor", then the search handler appends and redirects. Cookie value is not URL-encoded in `document.cookie`.
- Code file+method+lines: `CS_SearchBox.ascx` 270–276; `CS_SearchBox.ascx.vb` 100–108; `UserPage.master.vb` 339–344 and 89–95
- Confidence: Confirmed
- Suggested KB title: Search the product list from the header

### Create a product from an empty header search
- Pages: `CS_SearchBox.ascx` `openAddProductsFromEmptySearch`
- What it does (traced): If the search API returns an empty array, the typed term is non-empty, and the page contains `#div_add_products a.fancybox-add-products` (or an id ending in `div_add_products`), the menu shows one row: "Create New Product " plus the term in a highlight span. Choosing it sets that anchor to `/AddProducts?PreloadDescription={encodeURIComponent(term)}`, clicks it, then sets the href back to `/AddProducts`.
- How to access + visibility: Only when Add Products is in the DOM. Read-only users have `div_add_products` hidden (`Visible = False`), so the row is not offered.
- Steps: Type a term that returns no hits. Click "Create New Product …".
- Options and defaults (real values or data source): None besides the typed term.
- Permissions: Same as Add Products. Hidden for read-only.
- Validation/failures: HTTP error does not show this row. Empty term does not.
- Result: Add Products Fancybox with the description preloaded.
- Edge cases: Depends on the API returning `[]` rather than an error or a "no results" object. `$.isArray` is required.
- Code file+method+lines: `CS_SearchBox.ascx` 163–175, 239–252, 279–291
- Confidence: Confirmed
- Suggested KB title: Create a product from search

---

### Confirm deleting a location
- Pages: `ConfirmationDialog.aspx`, `ConfirmationDialog.aspx.vb`. Opened from `LocationEditor.aspx` and `Controls/Map_CONTROL_2017.ascx` / `Map_CONTROL_MOBILE_2018.ascx` as `ConfirmationDialog.aspx?ACTION=DELETE&LocationID=`.
- What it does (traced): Shows the location thumbnail (`Images/Locations/{type}.png`), name, and formatted path. Message: "Are your sure you want to DELETE this location?" (source spelling) and "All sub-locations will be deleted. Existing products will be checked out automatically." YES runs checkout-then-delete. There is no No/Cancel button in the markup; closing the Fancybox is the cancel. Checkbox "Include Any Sub-Locations" is `Checked="true"` and `ClearLabelsAndButtons` sets `chk_sub_locations.Visible = False`, and **no code reads the checkbox**. Descendants are always deleted.
- How to access + visibility: Map or location editor delete, in a Fancybox (`UserPageNoMenu.master`). Not linked from Activity History. The delete then **writes** activity rows the history page will show.
- Steps: Open the dialog. Click YES.
- Options and defaults (real values or data source): `ACTION` is required by callers but ignored. `LocationID` is required. Cookie `LocationToDelete` is set for 1 day and is what YES reads.
- Permissions: Read-only users are redirected to `/_admin/_unauthorized` before the dialog. Logged-in non-read-only users can delete. `RegisterPage(..., "ConfirmationDialog", ...)`.
- Validation/failures: If `Location.LocationExists` is false, the page sets refresh cookies and runs `CloseFancyBoxAndUpdate()` with no message (stale session). YES with no cookie does nothing. Checkout is skipped when the summed quantity at the location and `GetAllChildren` is 0.
- Result: 1) For each quantity row at the location and children, `RegisterActivity` with `INVENTORY__CHECK_OUT` (code 3), source = the location being deleted, comment `Items cleared before deleting location '{name}' ({id})`. 2) If `ParentID = -2`, the location is removed from that user's map coordinates. 3) `DELETE` from `{account}.Locations` and `{account}.Quantities` for the id list. 4) `RegisterActivity` with `LOCATION__DELETE` (code 7), comment `Deleted location '{name}' ({id})`, one content "qty" of 1 per id in the list. 5) Cookies `REFRESH_MAP_REQUIRED=TRUE` and `CookieRefreshRequired=1`. 6) `parent.$.fancybox.close()`.
- Edge cases: `LocationAndChildrenAreEmpty` is not used as a guard; it only fills the id list. `BuildListOfDescendants` adds the parent again, so the id array can contain duplicates, and both the delete SQL and the location-delete activity can list the same id twice. Quantity checkout uses `GetAllChildren`, which may not be the same set as `BuildListOfDescendants`. Products are checked out in one activity; they are not moved. No undo. The visible checkbox does not change behavior because it is hidden and unread.
- Code file+method+lines: `ConfirmationDialog.aspx` 35–50; `ConfirmationDialog.aspx.vb` `Page_Init` 37–79, `btn_yes_delete_Click` 87–111, `CheckoutProductsBeforeDeletingLocation` 113–156, `DeleteLocationFunction` 185–223, `LocationAndChildrenAreEmpty` 232–260
- Confidence: Confirmed
- Suggested KB title: Delete a location and check out its products

---

### Getting started wizard (unreachable on this request)
- Pages: `pages/guides/getting-started.aspx`, `getting-started.aspx.vb`, `pages/guides/scripts/getting-started.js`
- What it does (traced): `Page_Init` executes `Response.Redirect("/Map")` and `Return` before token setup, status checks, or the wizard. The markup and script still define the flow. `window.onload` would GET `https://code.cyberstockroom.com/api/onboarding` and switch on `response.status`. `setStatus` POSTs `{"onboarding":[{"playbook","completed","status"}]}` to that API and refreshes. Checklist images are account (always the done-looking `checklist/account.png`), profile, map, test drive, finalize.
- How to access + visibility: Intended URL `/pages/guides/getting-started`. `Welcome.aspx.vb` and `map_demo.aspx.vb` redirect here. This page immediately leaves for `/Map`. Query `returning=1` would call `welcomeBack()`, whose body is empty. If `_onboardingCompleted = 1`, the server would have redirected to `/Map` after the early return that already does that. Master is `UserPageNoMenu.master` (no header search).
- Steps: Not reachable. Catalog of status keys and UI if the redirect were removed:

  | `_onboardingStatus` | What the script shows | Forward / choices |
  | --- | --- | --- |
  | `profile` | If `_firstName` is non-blank, playbook 1 goes to `finalize`, otherwise `map-build`, and returns. Else checklist position 1, header "Welcome to CyberStockroom!" / "Let's get your inventory account set up", iframe `/Welcome`. | Iframe `Next()` |
  | `map-build` | Checklist 2. "Let's start building your Inventory Map". Iframe `/Welcome`. Back to `profile`. Forward button hidden, then iframe-forward enabled. | Iframe `Next()` |
  | `product-demo-alert` | Checklist 3. "We created a few sample items for you" in warning color `#AF5756`. Billboard image `/pages/guides/billboards/product-demo-alert.png`. | Forward to `map-demo-peek` |
  | `map-demo-peek` | `location.href = "/map_demo"` | |
  | `map-demo-drag-drop` | `location.href = "/map_demo"` | |
  | `map-demo-filter` | `location.href = "/map_demo"` | |
  | `map-demo-product-selector` | `location.href = "/map_demo?ProductNumber=CS_DEMO_3"` | |
  | `invite` | Checklist 4. "You can invite others to your map!" Four name/email rows. | Skip → `invitation-complete`. Send → server |
  | `invitation-complete` | "Do you want to create some products now?" Survey images. | Choices `products` or `finalize` |
  | `products` | "How would like to create them?" | Choices `add-products-cfs` or `spreadsheet` |
  | `add-products-cfs` | "Set custom fields for your products". | Forward calls `saveCFs("add-products")` |
  | `add-products` | Iframe `/AddProducts?LastPage=getting-started`. | Iframe `Next()` |
  | `spreadsheet` | "We have to make sure the spreadsheet is formatted properly". | `spreadsheet-manual-cfs` or `spreadsheet-email` |
  | `spreadsheet-manual-cfs` | "The columns in your spreadsheet are called Custom Fields". Forces `cfs = ['Manufacturer','Supplier']` then shows the chip UI. | `saveCFs("spreadsheet-import")` |
  | `spreadsheet-import` | Iframe `/ImportFromFile?LastPage=getting-started`. Forward starts hidden. | Iframe `Next()` |
  | `spreadsheet-import-validate` | Warning header "There was a problem importing your file!" plus the email-us block. | Forward to `finalize`. Back to `spreadsheet-import` |
  | `spreadsheet-email` | "Email us your Spreadsheet" plus the same email block. Comment in script: `TO COMPLETE`. | Forward to `finalize` |
  | `lansweeper` | Case is commented out (`//show_lansweeper`). The function would show `thumbnails/lansweeper.png` linking to `https://app.lansweeper.com/authorize-app/985f4e62409cea0e1c6e7b37fcdb7af3` and a help URL on `cyberstockroom-help.instantdocsbase.com`. | Not entered |
  | `invitee-resources` | **Does not call `show_invitee_resources`.** It calls `show_finalize`. The resources markup (YouTube `IdgoznaxBZ4`, "Watch a short clip…", "Don't forget to unmute!") is therefore unused by the switch. | |
  | `finalize` | Playbook 1: "Welcome, {firstName}". Else: "You're ready to go Live!" Button "Start Using CyberStockroom!". | Server `btn_finalize` |
  | any other | Sets playbook to **1**, status `profile`, completed 0, and posts that. | |

  Custom field chips: Manufacturer and Supplier start active. Inactive chips: Style, Color, Height, Weight, Unit, Contact. "+ New Field" placeholder "Type and Press Enter...". Duplicate names are rejected case-insensitively. `saveCFs` POSTs `https://code.cyberstockroom.com/api/customFields` with `X-CS-TOKEN` and a JSON-like body of `CF1`…`CFn`. The copy says "CyberStockroom has 4 default fields": Product Number, Description, Buy Price, Sell Price.

  Invitations (`_sendInvitations`): up to 4 rows. A row is sent only when the name length is `> 0` and `User_Legacy.ValidEmail` accepts the email (`MailAddress` parse). Subject: `{FirstName} is inviting you to CyberStockroom. Details Inside.` Body links `https://www.cyberstockroom.com/Login.aspx?Invitation={guid}`. From `admin@cyberstockroom.com`, display name CyberStockroom. Then SQL sets `_onboardingCompleted=0` and `_onboardingStatus='invitation-complete'`.

  Spreadsheet check (`_validateSpreadsheetImport`), only if status is `spreadsheet-import-validate` **and** the early redirect did not run: if `productRepository.getAll` (page size 10) returns **more than 5** products, status is set to `finalize` and the page redirects to itself. Five or fewer leaves the user on the failure step. The code comment says demo items are the baseline.

  Finalize: sets `_onboardingCompleted=1`, status `finalize`, runs `EndWelcome()`, redirects to `/Map`. Emails `emadh@cyberstockroom.com` unless the account email contains `@cyberstockroom.com`. Playbook `1` uses subject `NEW *INVITED* CS USER` and calls the user a secondary/invited account. Playbook is not 1 for the other subject `NEW CS USER`.
- Options and defaults (real values or data source): Playbook `1` is the short path (named in the default branch "shorter invitee onboarding"). A non-empty first name on `profile` skips the Welcome iframe. Checklist positions: 1 profile, 2 map, 3 test drive (map marked done), 4 finalize (map and test drive marked done).
- Permissions: Would require the no-menu master login. Dead before that logic now, except the redirect still runs inside `Page_Init` after the master has authenticated (master `Init` runs first).
- Validation/failures: `welcomeBack` is empty. `show_lansweeper` is unused. `offerToEmailSpreadsheet` tells the user to mail `support@cyberstockroom.com` with subject `Please import my spreadsheet for me!` and to attach the file from the signup address. Invalid emails are skipped with no message. Zero valid invitees still marks `invitation-complete`.
- Result: Today, the browser ends on `/Map`. The wizard does not render.
- Edge cases: `map_demo.aspx` still references this script and CSS for the demo steps that navigate with `location.href`. Those demo pages are outside this file but they are the only live callers of `show_map_demo_*` once the user is already on `/map_demo`. `getting-started.aspx.vb` `Page_LoadComplete` and every method below the redirect are unreachable.
- Code file+method+lines: `getting-started.aspx.vb` `Page_Init` 17–19 (the live path), remainder 27–192; `getting-started.aspx` `displayNext` 32–111, `setStatus` 137–158, invite form 215–240, custom fields 245–340, finalize 366–394; `getting-started.js` step functions 5–183
- Confidence: Confirmed
- Suggested KB title: Getting started checklist (currently skipped)

---

## Workflows

1. **Review what happened.** Header icon or menu "Activity" → Activity History (All Activity, last 90 days, all users, all locations) → optional user, location, date preset, category, keyword → row click → Activity Details → product or location editor, or the single-activity CSV. "Show More..." lengthens the same list by 15. "Readable Format" CSV uses the same filters and ignores the 15-row window.
2. **Check-in vs check-out vs a move.** Inventory shows check-in (1), check-out (3), transfer (4), and adjust (25). Check In adds transfers only when the destination is inside the chosen location tree and the source is outside, plus adjusts whose comment quantity did not go down. Check Out is the mirror. With All Locations, transfers do not appear under Check In or Check Out at all. The row icon and the `transfer` / `quantity adjust` badge are display-only.
3. **Delete a location.** Map or location editor → Confirmation Dialog → YES checks products out (activity code 3, comment `Items cleared before deleting location '…'`) and deletes the location (activity code 7, comment `Deleted location '…'`). Those rows show on Activity History. Sub-locations always go with it. No undo.
4. **Expirations.** Settings flag on → header expirations icon → list colored red `#AF5756` / yellow `#FFD966` / grey `#EEEEEE` using the `-18` day window (default 60, 0 hides yellow) → row opens the product → "manage" runs replace/clone against `api/expirationReplacement` → browser goes to Activity History. Read-only users get the list without "manage".
5. **Kits.** `SHOW_KITTING` (no visible settings switch in this repo) → header kitting icon → list → expand → add/search products, prompt for qty, or delete a line or the kit via `api/kit`. There is no build and no break. The manage button is a broken copy of the expiration wizard.
6. **Header search.** Type → API search limit 10 → click `Products` or `Locations` to open the editor, or Enter to append the term to the Products filter cookie and open Products. An empty hit list can offer "Create New Product {term}" when Add Products is on the page.
7. **Product CSV.** Products download icon → Export Report Fancybox → fields and location → CSV. This also rewrites stored location paths.
8. **AI report.** Only by opening `/ai-report?id=…`. Failure returns to the map. No in-app link.
9. **Onboarding.** Any request to getting-started is redirected to the map before the checklist runs.

---

## UNCERTAIN

- Search API (`developers.cyberstockroom.com/api/search`): which columns are matched, whether `term` supports operators, and which `category` strings can come back besides `Products` and `Locations`. The website only branches on those two strings.
- Expiration and kit `searchTerms`: matched fields and any operator syntax live in `code.cyberstockroom.com`, not this repo. The pages pass the raw string.
- `api/expirationReplacement` action effects (`replace_delete`, `replace`, `clone_delete`, `clone_checkout`, `clone`). The page sends the action name and a comment and then opens Activity History. Inventory changes are not in this solution.
- `api/kit` rules for `id: -1`, empty names, and invalid JSON from the hand-built body.
- `SDK.Reports.AI.InsightsReport.getReport`: where the id is created, and the full set of card payloads. Only the four `reportContentItemType` names in `ai-report.aspx.vb` are visible.
- Whether the split identifier at `CS_SearchBox.ascx` 207–208 is executed. It is invalid JavaScript in the suppress-location branch. The header always passes suppress `"FALSE"`, so that branch is not taken, but it still sits inside the function the page parses.
- Inactive-product rows in Export Report when "breakdown by location" is on: the zero-qty SQL omits `LocationID` and is merged into a table that has it. Column alignment was not executed.
- `Kitting_read_only`: referenced, file absent. Read-only behavior after the redirect is unknown.
- How `SHOW_KITTING` is turned on for a user. The only checkbox is inside `display: none`, and no other `.vb` assigns the column.
- Account/user activity constants (10, 11, 12, 15–24) have no writer in this repo. They may exist only as legacy numbers. History will not list them while `ONLY_DISPLAYABLE` is true.
- Getting-started API status values that might be stored for old users but are not in the `switch` (they fall through to playbook 1 / `profile`). The page never gets that far today.

---

## CONTROLS CHECKLIST

### Activity History
- [ ] Title "Activity History"
- [ ] Date control default label is the last 90 days through today
- [ ] Presets: All Time, Today, Yesterday, Last 7 Days, Last 30 Days, This Month
- [ ] User chips: All, Me, other signed-in non-read-only users; label truncated; tooltip full name
- [ ] Location selector default "All Locations"
- [ ] Keyword box placeholder "search by keyword..."
- [ ] "Readable Format" checked by default; download tooltip "Download spreadsheet file (.csv)"
- [ ] Categories: All Activity, Inventory, Check In, Check Out, Transfer, Adjust, Products, Create, Edit, Delete, Location, Create, Edit, Delete
- [ ] Account type 1 labels: Assignments, Assign, Deallocate, Transfer, Records
- [ ] Empty state "No Activity..." / "details will appear here"
- [ ] "Show More..." adds 15 to the window and reloads from the newest row
- [ ] Row click opens Activity Details; product and location clicks do not
- [ ] Check In with All Locations does not list transfers; with a location, only inbound boundary transfers
- [ ] Check Out is the outbound mirror; adjusts follow the comment `from {old} to {new}`
- [ ] Badges `transfer` and `quantity adjust` on those filtered rows
- [ ] Create/edit product rows have no quantity; other product rows do
- [ ] CSV header includes Old Quantity, New Quantity, Qty. Diff., Cost Diff. and the writer leaves them blank
- [ ] No undo control

### Activity Details
- [ ] "You" vs the stored name; description from the phrase table
- [ ] Missing id: "Activity not found"
- [ ] Download `?download=1` filename from description and `MMM d yyyy`
- [ ] Product, Number, Qty; Qty hidden for create and edit
- [ ] From/To/Location columns only when both header locations are -2
- [ ] `download=1` on a missing id returns 404

### Expirations
- [ ] Hidden unless `SHOW_EXPIRATIONS`; otherwise Settings
- [ ] Read-only page has no "manage"
- [ ] Chips "{n} Expiring Soon" and "{n} Expired"
- [ ] Yellow chip hidden when the window is 0
- [ ] Row colors `#AF5756` / `#FFD966` / `#EEEEEE`
- [ ] Search placeholder "search..."; no pager; page size 100
- [ ] Window default 60 days; units days, weeks (×7), months (×30), years (×365); 0 disables
- [ ] Wizard radios and actions: `replace_delete`, `replace`, `clone_delete`, `clone_checkout`, `clone`
- [ ] Warnings: "This date has already passed!", "You must select an expiration date.", "That product number already exists!", "You must select a product number."
- [ ] Auto fills `[Automatic Product Number]`
- [ ] Success goes to Activity History

### Kitting
- [ ] Icon only when `SHOW_KITTING`; settings Kitting checkbox row is `display: none`
- [ ] "{n} Kits", "+ NEW KIT", placeholder "search..."
- [ ] Prompt "New Kit Name:"
- [ ] Expand shows "{qty} x {description} ({uid})", "+ Add New", "x", "Delete Kit"
- [ ] Add-item search page size 10; Enter takes the first hit
- [ ] Quantity prompt; cancel or `<= 0` does not save
- [ ] Existing component qty is posted as the old qty (new number ignored)
- [ ] Delete-item confirm text; no confirm on Delete Kit
- [ ] No Build control and no Break control
- [ ] "manage" throws because the kit name is unquoted in the handler; modal underneath is the expiration wizard
- [ ] Read-only redirect `Kitting_read_only` has no page in this repo

### Export Report
- [ ] "Download Product Report", button "Download File"
- [ ] "Include Products with 0 Quantity" off; "Include Products in Sub-Locations" off and hidden for all-locations
- [ ] Product Number locked on; Description, Quantity, breakdown by location, Buy Price, Cost Value, Sell Price on; Product Image off; each custom field on
- [ ] Unchecking Quantity disables breakdown
- [ ] Cost header uses the account currency; value is qty × buy price to 2 decimals
- [ ] Filename is the location path or "ALL LOCATIONS" plus the long date
- [ ] Download rewrites `LocationPath` for every location

### AI report
- [ ] Title "AI Insights Report", badge "AI-GENERATED", heading "Your Inventory Insights"
- [ ] Card types General, Location, Product, User
- [ ] Footer label "RECOMMENDATION"
- [ ] No navigation link in this repo; bad id goes to Map
- [ ] No export button

### Header search
- [ ] Present on Activity, Expirations, Kitting, AI report (UserPage)
- [ ] Limit 10; term sent with no operator syntax
- [ ] Category `Products` → Product Editor; `Locations` → Location Editor
- [ ] Enter → `/Products.aspx` with the term appended to the product search cookie
- [ ] Empty list + Add Products visible → "Create New Product {term}" → `/AddProducts?PreloadDescription=`
- [ ] Read-only: search remains, create-product row does not (Add Products hidden)

### Confirmation dialog
- [ ] Title line "Are your sure you want to DELETE this location?"
- [ ] "All sub-locations will be deleted." / "Existing products will be checked out automatically."
- [ ] Button "YES" only
- [ ] "Include Any Sub-Locations" is checked but not rendered (`Visible = False`) and is not read
- [ ] Read-only → `/_admin/_unauthorized`
- [ ] Missing location closes the Fancybox and requests a map refresh
- [ ] YES writes check-out activity 3 and location-delete activity 7

### Getting started
- [ ] Request to `/pages/guides/getting-started` redirects to `/Map` immediately
- [ ] Checklist art: account, profile, map, test drive, finalize
- [ ] Status keys listed in the feature (profile through finalize), including unused `lansweeper` and `invitee-resources`
- [ ] Invite: 4 rows, placeholders "Name" and "Email", buttons "Skip" and "Send Invitations"
- [ ] Custom fields copy lists Product Number, Description, Buy Price, Sell Price; chips Manufacturer, Supplier, Style, Color, Height, Weight, Unit, Contact
- [ ] Finalize button "Start Using CyberStockroom!"
- [ ] Spreadsheet help: email `support@cyberstockroom.com`, subject `Please import my spreadsheet for me!`
