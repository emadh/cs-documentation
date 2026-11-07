# Workflow catalog

Cross-page sequences for the knowledge base. Each step is what the user does. The feature ID in parentheses is the walkthrough in `FEATURE_CATALOG.md`. IDs here are stable (`WF-###`). Do not renumber them.

These match website commit `a4f1fc6b686294b7c00c692b744565efd5dc447d`. Product behavior is unchanged from `e8172b5c35b4e32a77ea28569ae82ad28ed83f8e`. Where an API outside this repo finishes the stock change, the step says that outcome is Uncertain.

## WF-001 — Create products and check them in

- **Who:** Signed in, not read-only. Prices are disabled for account type 1.
- **Steps:**
  1. On the product list, click **Add** (PRD-011). Or, from header search with no matches, click **Create New Product** (SRCH-001). Or, on the Start page, click **Create** (XFR-006).
  2. On Add Products, leave **AUTO** on or type a product number. Type a description. Empty description becomes the product number. Optional: set buy price, sell price, and custom fields. Optional: upload a photo (PED-011). Click save (PED-010).
  3. Or, instead of typing, upload a CSV and match at least a product number (PED-012, PED-013). Existing product numbers are not updated. Their quantity is only staged for check-in.
  4. The check-in page opens (XFR-007), unless this was the single add from a mobile transfer. That path does not check in.
  5. Click a location. The suggested location is the default check-in location (DEF-001). Enter whole-number quantities. At least one line must be 1 or more. Save. Stock is added and a check-in is recorded.
  6. Click **Skip** instead to leave the products in the catalog with no placed stock.
  7. If every imported line already names a location, the map stays hidden and each line checks into that location.
  8. If you came from an open transfer, **Continue** does not change stock yet. Save the transfer later (XFR-001).
- **Outcome:** New catalog rows. Stock only if check-in was saved.

## WF-002 — Check in

- **Who:** Signed in, not read-only. The menu item is hidden when the account has no products. Quick Scan stays available.
- **Steps:**
  1. On the map, start a check-in on a location that already has a destination and is not empty (MAP-020). Or open **Check In** from Start (XFR-006) or from the mobile menu (XFR-008, XFR-012).
  2. On Transfer, the left list is the whole catalog, shown with an infinity mark. The source is All Locations. Click a product to move 1. Type a quantity of at least 1 when the badge asks. There is no **Check In Everything** (XFR-001).
  3. Click **Check In**. The chosen quantities are added at the destination. One check-in activity is written. You can skip the comment.
  4. On the Start page the same button adds quantity, but the comment box appears only after the stock is already written. If the location cookie is missing, Start saves nothing.
  5. On a phone, finishing from mobile home clears the in-progress process (XFR-012).
- **Do not merge these paths.** The Transfer save overwrites the source cookie quantity. The Start page adds.

## WF-003 — Check out

- **Who:** Signed in, not read-only.
- **Steps:**
  1. On the map, drag a full location to **Drag inventory here to check out**, or open check-out so the destination is All Locations (MAP-021).
  2. On Transfer, the left list is stock at the source. Click to move 1, up to what is on hand. Drag a row to move the rest. **Check-Out Everything** loads the location in pages of 500 and hides while a map-filter badge is on (XFR-002).
  3. Click **Check Out**. Source stock becomes the quantity you left behind. The activity stores the quantity that moved.
  4. On the Start page, check-out subtracts and stops at 0. That is not the Transfer overwrite (XFR-006).
- **If both check-in and check-out are requested:** Check-out wins (XFR-001).

## WF-004 — Transfer between two locations

- **Who:** Signed in, not read-only. The two locations must be different.
- **Steps:**
  1. On the map, drop a full location or a product row onto a different location (MAP-022). The same location, or All Locations, is ignored. A wide screen opens Transfer in a popup. A narrow screen opens the mobile transfer page.
  2. When the dragged quantity is exactly 1, a comment box says **Moving this item.** Saving that path sets the source quantity of that product to 0 (MAP-023). That is not “move 1 and keep the rest.”
  3. Otherwise, on Transfer, click to move 1 or drag to move what remains. Click **Transfer**. The destination becomes its current quantity plus the amount moved. The source becomes the quantity you left behind (XFR-003).
  4. On the Start page, pick a source and then a destination. The same place shows “The Source can't be the Destination!” Start subtracts from the source and adds to the destination (XFR-006).
  5. On a phone, pick source and destination (XFR-009). The **default** badge opens the Settings location picker (DEF-001, DEF-002). Save uses the Transfer backend (XFR-008).
- **Not this workflow:** There is no Adjust button on Transfer (XFR-004). Change a quantity from the product map (MAP-026) or the product list (PRD-010).

## WF-005 — Quick Scan and the location kiosk

- **Who:** Signed in, not read-only.
- **Steps:**
  1. Open **Quick Scan** from the menu (XFR-011). Or, in the location editor, click **Checkin Kiosk** or **Checkout Kiosk** (MAP-041). A kiosk locks one location. Transfer is not a kiosk mode.
  2. Scan products. Each scan adds the product or adds 1. The placeholder is “ready to scan...”.
  3. Outside a kiosk, the first location scan becomes the source and the next becomes the destination.
  4. Click save. Source only checks out. Destination only checks in. Both transfer. The page posts `api/inventory`.
- **Outcome:** The page shows “{N} Transactions completed successfully.” or, on mobile, “Transaction saved”. What the API does to stock is Uncertain. Quick Scan does not create a product. Quick Add (XFR-010) creates a catalog product and does not check it in.

## WF-006 — Move, reparent, delete, or clone a location

- **Who:** Signed in, not read-only. The map is locked until you unlock it (MAP-009).
- **Steps:**
  1. Click the floating **+**, a **+** on a tile, or **Add** inside a 3D stack. Pick **BUILDING**, **WAREHOUSE**, **STORE**, **FLOOR**, **ROOM**, **CLOSET**, **SHELF**, **BIN**, or **VEHICLE**. Name it. The default name is `New {type}` (MAP-005, MAP-003). A duplicate name shows “That location name is already in use!”
  2. To move a primary location, unlock the map, then drag the diamond header (MAP-008). Children move with it. Inventory stays on the same location ids. There is no resize handle (MAP-011).
  3. To put it under another parent, click the clasp, then click the new parent or empty canvas. Confirm **Move location?** Children stay with it. Empty canvas makes it primary (MAP-010).
  4. To delete, confirm **YES** on “Are your sure you want to DELETE this location?” Stock is checked out, then the location and its sub-locations are deleted (MAP-012). Closing the popup cancels. There is no No button.
  5. To clone the structure, name the copy. **Auto-Rename Sub-Locations** is off unless you turn it on. Confirm. The page posts `api/LocationClone`. Whether quantities copy is Uncertain (MAP-013).
  6. To copy stock, hold Ctrl and drop a full location onto another. Confirm the message that existing items there are cleared first (MAP-014). This is blocked while several locations are selected (MAP-030).
  7. Rename, attachments, barcode, and kiosk links are in the location editor, not on the canvas (MAP-006, MAP-007, MAP-039, MAP-040, MAP-041).

## WF-007 — Import a CSV to create products

- **Who:** Signed in, not read-only.
- **Steps:**
  1. From Add Products, upload a CSV (PED-012). It must be under 250 KB, UTF-8, comma-separated, at most 100 columns. The first row is the header.
  2. Drag columns from the left onto Product Number and any other fields (PED-013). You must map at least a product number. Sample headers are examples, not required names.
  3. Unmapped quantity stays 1, prices stay 0, and the location stays All Locations. Duplicate numbers in the file are rejected. Existing products keep their description, price, and custom fields.
  4. Continue into the check-in page (WF-001, step 5).

## WF-008 — Import a list into a movement

- **Who:** Signed in, not read-only. The import button is hidden once the destination selection is filled.
- **Steps:**
  1. From check-in, check-out, or transfer, click import before choosing the destination side (XFR-005, PED-014).
  2. Match by product number, description, or a custom field. A value that matches more than one product is skipped.
  3. Check-in keeps the quantity in the file. Check-out and transfer reduce it to what is on hand.
  4. Review the lines. The page stays locked until you save or cancel.
  5. Save uses the host mode (WF-002, WF-003, or WF-004). Cancel writes nothing.
- **Start page:** The same file can fill the Start page cookies. Start then adds or subtracts. That is not the Transfer overwrite (XFR-006).

## WF-009 — Invite a teammate and accept

- **Who:** An admin sends the invite. The form is also visible to a User, but the API rejects them with “Unable to Invite - Try Again?”
- **Steps:**
  1. On Settings, under **Invite a Team Member**, enter an email and a role. The unmarked default is `ADMIN` (TEAM-004).
  2. Send. The mail links to `Login.aspx?Invitation={guid}`.
  3. The invited person opens the link, creates a password, and submits (ACC-004). The role is not chosen on that page.
  4. An admin can later change the role (TEAM-002) or click **DELETE** (TEAM-003). Nothing stops you from removing the last admin.
- **Do not write:** Inviting an email that already belongs to this account does not change that person’s role.

## WF-010 — Share a map layout and sync to it

- **Who:** An admin turns sharing on. Any signed-in user can sync to a shared layout.
- **Steps:**
  1. On Settings, under **OPTIONS**, turn **Share Map Layout** on (DSP-001). Products and quantities are not shared.
  2. Another user opens the map gear, then **Shared Maps** (MAP-016).
  3. If none are shared, the text is “No shared maps. Admins can share their maps in the Settings page.”
  4. Pick a person. The warning says the current layout will be lost. Click **Sync**, or **Keep my layout**.
- **Outcome:** Coordinates, zooms, and vertical or 3D stacks are copied. Inventory is not copied.

## WF-011 — Review expirations and replace or clone

- **Who:** Expirations must be on (DSP-004). The window is DSP-005. Read-only users get the list without **manage**.
- **Steps:**
  1. Open **Expirations**. The list shows the first 100 rows. Expired rows are red. Rows inside the window are yellow (EXP-001).
  2. Click a row to open the product editor and change that product’s date (PED-005).
  3. On the editable list, click **manage** (EXP-002). Leave **Replace and Delete** selected, or choose **Replace only**, **Clone and Delete**, **Clone and Check-out**, or **Clone only**.
  4. Set a future date and a product number. A past date warns “This date has already passed!” and does not block save.
  5. Save. The browser goes to activity history (ACT-001).
- **Do not write:** What each radio does to stock. That API is outside this repo.

## WF-012 — Create and edit a kit

- **Who:** `SHOW_KITTING` must already be on. The Settings checkbox does not turn it on (DSP-008).
- **Steps:**
  1. Open **Kitting**. Click **+ NEW KIT**, type a name, and confirm (KIT-001). Cancel posts the name `null`.
  2. Expand the kit. Click **+ Add New**, search for a product, and enter a quantity (KIT-002).
  3. Do not rely on editing a quantity that is already in the kit. The page sends the old quantity. Removing a line also drops every other component with the same quantity.
  4. **Delete Kit** has no confirm.
- **Do not write:** The **manage** button (KIT-003). It throws before the modal. There is no build and no break into inventory.

## WF-013 — Find a product and change it

- **Who:** Signed in. Read-only users can search and open the view-only editor. They cannot add, edit, clone, or delete.
- **Steps:**
  1. Type in the header search and press Enter (SRCH-001, PRD-006). The product list opens at All Locations. Terms are combined with AND.
  2. Click a product row. The checkbox column does not open the editor (PRD-007).
  3. Change the name, prices, or custom fields (PED-001). The product number cannot be renamed. Presets offer **(none)**, each preset, and **Other (Specify)**.
  4. To change a quantity, use the product map: click a location, type a whole number, press Enter (PED-006, MAP-026). Or, on the product list at a real location, edit the in-stock quantity cell (PRD-010).
  5. **Clone Product** copies fields, not stock (PED-007). **Delete this product** uses the same delete as the grid (PED-008, PRD-011).
  6. The download icon opens the product report (RPT-001). The current search is not included. Every download rewrites location paths for the account.
