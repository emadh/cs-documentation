# One-shot catalog matrix update. Not retrieval material.
import csv
from pathlib import Path

p = Path(r"C:\Users\emadh\Documents\code\cs-documentation\QA_FeatureCatalog\FEATURE_MATRIX.csv")
with p.open(newline="", encoding="utf-8") as f:
    rows = list(csv.reader(f))

replacements = {
    "MAP-013": " Auto-rename matches a whole code. A space, a hyphen, or a change between a letter and a number starts a new code. A to B renames A1 to B1 and leaves A11 unchanged.",
    "MAP-016": " Syncing also replaces this user's barcode-label choice (DSP-009).",
    "MAP-017": " After a transfer window closes, the top-right zoom controls are shown again.",
    "XFR-007": " The map hides only when every line already has its own location. A missing location keeps the single-location map.",
}

# Phrase swaps applied wherever they appear in the description.
global_swaps = [
    (
        "Drag from left to right to Match the fields.",
        "Drag a column onto a field, or click a column and then a field.",
    ),
    (
        "The sample link on a create import is `Samples/Products.csv`.",
        "Sample CSV File downloads a sample built for this import. Create imports remember header matches. A create import rejects a row whose column count does not match the header, and a blank header that still has values. Trailing blank columns are dropped.",
    ),
    (
        "Sample header in `Samples/Products.csv`.",
        "The sample is built for this account. The existing-product notice says how many will be created and how many already exist.",
    ),
    (
        'the comment `Changed \'{field}\' to \'{value}\'`',
        "the comment `{field} for '{product number}' was changed from '{old}' to '{new}'`. An unchanged value is skipped. A whole-number quantity change records an adjust: `Quantity for '{product number}' was adjusted from {old} to {new}`",
    ),
    (
        "activity `PRODUCT__EDIT` with the comment `Changed '{label}' to '{value}'`",
        "activity `PRODUCT__EDIT` with the comment `{field} for '{product number}' was changed from '{old}' to '{new}'` when the stored value changes. An unchanged value does not write an activity",
    ),
]

notes = {
    "PED-014": " Check-in back to Transfer can create missing products. Check-out and transfer do not. Use this location keeps the chosen location. Titles switch to (Multiple Locations) when a location column is mapped.",
    "PED-015": " Product labels use the saved barcode-label fields (DSP-009), or the product name until a choice is saved. Location labels use the location name.",
    "PED-007": " Unchecking Auto suggests the source number plus -1, or the next hyphen ending. An automatic CSN- number keeps those digits and appends -1.",
    "PED-008": " A missing product opened from an activity opens the deleted-product page (ACT-008).",
    "PED-009": " A missing product opened from an activity opens the deleted-product page (ACT-008).",
    "ACT-004": " A product name opens the editor, or the deleted-product page when the product is gone (ACT-008).",
    "ACT-005": " A product name opens the editor, or the deleted-product page when the product is gone (ACT-008).",
    "ACT-007": " A field edit comment includes the old and new values.",
}

for r in rows[1:]:
    fid = r[0]
    text = r[6]
    if fid in replacements and replacements[fid] not in text:
        text = text.rstrip() + replacements[fid]
    for old, new in global_swaps:
        if old in text:
            text = text.replace(old, new)
    if fid in notes and notes[fid] not in text:
        text = text.rstrip() + notes[fid]
    r[6] = text

new_rows = [
    [
        "DSP-009",
        "Display",
        "Settings.aspx",
        "",
        "Barcode label details",
        "Setting",
        "Settings, Display Settings, Barcode Label, Edit. Visible to Admin, User, and Read-only. Saved for the signed-in person. Until a choice is saved, product labels print the product name and are not capitalized. After a change, the selected details print above the barcode, joined with a hyphen, in order: Product Name, custom fields, then Expiration when expirations are on. Empty values are left out. Capitalize uppercases that line. Turning every detail off leaves the line blank. The barcode and the number under it still print. Location barcodes do not use this choice. Moving the map does not clear it. Syncing another person's map layout replaces it. If it fails: Could not save. Try again.",
        "Admin, User, and Read-only",
        "Display Settings is visible",
        "Settings.aspx barcode modal; webAPI/settings.aspx.vb SaveBarcodeLabelFields; PrintBarcode.aspx.vb BuildProductLabelText",
        "Not audited",
        "",
        "Per person, stored with the map layout",
    ],
    [
        "ACT-008",
        "Activity",
        "ProductDeleted.aspx",
        "ACT-005",
        "Deleted product details",
        "Behavior",
        "Open a product name on an activity row or on one activity when that product is gone. The page says This Product has been deleted and shows the product number. When the activity stored a snapshot, Details at the time of this activity lists the name, sell price, buy price, and custom fields that had a value. Prices use the account currency and two decimals when numeric. Nothing is restored. Header search does not open this page. A missing product with no activity still goes to the product error page.",
        "Signed in",
        "The product name is clicked from an activity and the product is no longer in the catalog",
        "ProductDeleted.aspx.vb; CS_TOOLS.DeletedProductRedirect; ActivityHistory.aspx.vb; ActivityDetails.aspx.vb",
        "Not audited",
        "",
        "Confirmed",
    ],
    [
        "HELP-001",
        "Help",
        "UserPage.master",
        "",
        "Open help",
        "Navigation",
        "Help, Search Topics, and Email Support open the Help Scout window. On the phone map the floating help button is hidden so it does not cover the add button. Help in the menu still opens the window. If the window has not loaded, the click does nothing and there is no sentence. Do not describe the old Groove widget as the live help window.",
        "Signed in",
        "",
        "UserPage.master; MOBILE_MasterPage.master; css/masters/userPage.v1.0.css",
        "Not audited",
        "",
        "Confirmed",
    ],
]

existing = {r[0] for r in rows[1:]}
for row in new_rows:
    if row[0] in existing:
        raise SystemExit("already present " + row[0])
    if len(row) != len(rows[0]):
        raise SystemExit(f"{row[0]} has {len(row)} cols")
    rows.append(row)

with p.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerows(rows)

print("rows", len(rows) - 1)
