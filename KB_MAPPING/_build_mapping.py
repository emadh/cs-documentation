# -*- coding: utf-8 -*-
"""Build KB mapping files from the verified article list and the feature catalog."""
import csv
import re
from pathlib import Path

ROOT = Path(r"C:\Users\emadh\Documents\code\cs-documentation\KB_MAPPING")
CATALOG = Path(r"C:\Users\emadh\Documents\code\cs-documentation\QA_FeatureCatalog")
ART = ROOT / "KB_ARTICLES"

names = {}
for line in (CATALOG / "SUMMARY.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^\| ([A-Z]+-\d+) \| ([^|]+) \|", line)
    if m:
        names[m.group(1)] = m.group(2).strip()

# category, title, url  — order is the permanent KB ID order
ARTICLES = [
("Getting Started", "How CyberStockroom Is Organized", "https://cyberstockroom.helpscoutdocs.com/article/155-how-cyberstockroom-is-organized"),
("Getting Started", "Getting Started: Your First 15 Minutes", "https://cyberstockroom.helpscoutdocs.com/article/156-getting-started-your-first-15-minutes"),
("Getting Started", "Creating Your First Map", "https://cyberstockroom.helpscoutdocs.com/article/157-creating-your-first-map"),
("Getting Started", "Adding Your First Products", "https://cyberstockroom.helpscoutdocs.com/article/158-adding-your-first-products"),
("Getting Started", "Checking In Inventory for the First Time", "https://cyberstockroom.helpscoutdocs.com/article/159-checking-in-inventory-for-the-first-time"),
("Getting Started", "Understanding Inventory Actions", "https://cyberstockroom.helpscoutdocs.com/article/160-understanding-inventory-actions"),
("Map & Locations", "Understanding the Inventory Map", "https://cyberstockroom.helpscoutdocs.com/article/162-understanding-the-inventory-map"),
("Map & Locations", "Creating, Editing, and Deleting Locations", "https://cyberstockroom.helpscoutdocs.com/article/163-creating-editing-and-deleting-locations"),
("Map & Locations", "Moving and Reorganizing Locations", "https://cyberstockroom.helpscoutdocs.com/article/164-moving-and-reorganizing-locations"),
("Map & Locations", "Viewing Inventory Inside Locations", "https://cyberstockroom.helpscoutdocs.com/article/165-viewing-inventory-inside-locations"),
("Map & Locations", "Navigating the Map", "https://cyberstockroom.helpscoutdocs.com/article/166-navigating-the-map"),
("Map & Locations", "Organizing the Map with Vertical and 3D Stacks", "https://cyberstockroom.helpscoutdocs.com/article/167-organizing-the-map-with-vertical-and-3d-stacks"),
("Map & Locations", "Cloning Locations and Copying Inventory", "https://cyberstockroom.helpscoutdocs.com/article/168-cloning-locations-and-copying-inventory"),
("Map & Locations", "Sharing Map Layouts with Your Team", "https://cyberstockroom.helpscoutdocs.com/article/169-sharing-map-layouts-with-your-team"),
("Map & Locations", "Finding Locations and Inventory on the Map", "https://cyberstockroom.helpscoutdocs.com/article/170-finding-locations-and-inventory-on-the-map"),
("Map & Locations", "Location Settings and Tools", "https://cyberstockroom.helpscoutdocs.com/article/171-location-settings-and-tools"),
("Products & Inventory", "Understanding Products and Quantities", "https://cyberstockroom.helpscoutdocs.com/article/173-understanding-products-and-quantities"),
("Products & Inventory", "Adding and Editing Products", "https://cyberstockroom.helpscoutdocs.com/article/174-adding-and-editing-products"),
("Products & Inventory", "Importing Products from CSV Files", "https://cyberstockroom.helpscoutdocs.com/article/175-importing-products-from-csv-files"),
("Products & Inventory", "Using the Product List", "https://cyberstockroom.helpscoutdocs.com/article/176-using-the-product-list"),
("Products & Inventory", "Searching and Finding Products", "https://cyberstockroom.helpscoutdocs.com/article/177-searching-and-finding-products"),
("Products & Inventory", "Editing Multiple Products at Once", "https://cyberstockroom.helpscoutdocs.com/article/178-editing-multiple-products-at-once"),
("Products & Inventory", "Changing Inventory Quantities Directly", "https://cyberstockroom.helpscoutdocs.com/article/179-changing-inventory-quantities-directly"),
("Products & Inventory", "Managing Product Images, Attachments, and Barcodes", "https://cyberstockroom.helpscoutdocs.com/article/180-managing-product-images-attachments-and-barcodes"),
("Products & Inventory", "Cloning and Deleting Products", "https://cyberstockroom.helpscoutdocs.com/article/181-cloning-and-deleting-products"),
("Inventory Operations", "How to Check In Inventory", "https://cyberstockroom.helpscoutdocs.com/article/183-how-to-check-in-inventory"),
("Inventory Operations", "How to Check Out Inventory", "https://cyberstockroom.helpscoutdocs.com/article/184-how-to-check-out-inventory"),
("Inventory Operations", "How to Transfer Inventory Between Locations", "https://cyberstockroom.helpscoutdocs.com/article/185-how-to-transfer-inventory-between-locations"),
("Inventory Operations", "Using Quick Scan", "https://cyberstockroom.helpscoutdocs.com/article/186-using-quick-scan"),
("Inventory Operations", "Setting Up Check-In and Checkout Kiosks", "https://cyberstockroom.helpscoutdocs.com/article/187-setting-up-check-in-and-checkout-kiosks"),
("Inventory Operations", "Importing Inventory Movements from CSV Files", "https://cyberstockroom.helpscoutdocs.com/article/188-importing-inventory-movements-from-csv-files"),
("Inventory Operations", "Managing Inventory on Mobile Devices", "https://cyberstockroom.helpscoutdocs.com/article/189-managing-inventory-on-mobile-devices"),
("Search, Activity & Reports", "Finding Products and Locations with Search", "https://cyberstockroom.helpscoutdocs.com/article/191-finding-products-and-locations-with-search"),
("Search, Activity & Reports", "Understanding Activity History", "https://cyberstockroom.helpscoutdocs.com/article/192-understanding-activity-history"),
("Search, Activity & Reports", "Filtering and Investigating Inventory Activity", "https://cyberstockroom.helpscoutdocs.com/article/193-filtering-and-investigating-inventory-activity"),
("Search, Activity & Reports", "Exporting Activity History to CSV", "https://cyberstockroom.helpscoutdocs.com/article/194-exporting-activity-history-to-csv"),
("Search, Activity & Reports", "Downloading Inventory Reports", "https://cyberstockroom.helpscoutdocs.com/article/195-downloading-inventory-reports"),
("Search, Activity & Reports", "Understanding Inventory Values and Report Columns", "https://cyberstockroom.helpscoutdocs.com/article/196-understanding-inventory-values-and-report-columns"),
("Team & Account Settings", "Signing In and Managing Your Password", "https://cyberstockroom.helpscoutdocs.com/article/198-signing-in-and-managing-your-password"),
("Team & Account Settings", "Managing Your Profile", "https://cyberstockroom.helpscoutdocs.com/article/199-managing-your-profile"),
("Team & Account Settings", "Inviting and Managing Team Members", "https://cyberstockroom.helpscoutdocs.com/article/200-inviting-and-managing-team-members"),
("Team & Account Settings", "Understanding User Roles and Permissions", "https://cyberstockroom.helpscoutdocs.com/article/201-understanding-user-roles-and-permissions"),
("Team & Account Settings", "Configuring Custom Fields", "https://cyberstockroom.helpscoutdocs.com/article/202-configuring-custom-fields"),
("Team & Account Settings", "Customizing Your Map and Display Settings", "https://cyberstockroom.helpscoutdocs.com/article/203-customizing-your-map-and-display-settings"),
("Team & Account Settings", "Setting Default Locations, Time Zone, and Currency", "https://cyberstockroom.helpscoutdocs.com/article/204-setting-default-locations-time-zone-and-currency"),
("Team & Account Settings", "Managing Your Subscription and Billing", "https://cyberstockroom.helpscoutdocs.com/article/205-managing-your-subscription-and-billing"),
("Advanced Features & Integrations", "Tracking Product Expirations", "https://cyberstockroom.helpscoutdocs.com/article/207-tracking-product-expirations"),
("Advanced Features & Integrations", "Using the CyberStockroom API", "https://cyberstockroom.helpscoutdocs.com/article/208-using-the-cyberstockroom-api"),
("Advanced Features & Integrations", "Lansweeper Integration", "https://cyberstockroom.helpscoutdocs.com/article/209-lansweeper-integration"),
("Troubleshooting & FAQs", "Why Can't I See a Product or Location?", "https://cyberstockroom.helpscoutdocs.com/article/211-why-cant-i-see-a-product-or-location"),
("Troubleshooting & FAQs", "Why Doesn't My Inventory Quantity Match What I Expected?", "https://cyberstockroom.helpscoutdocs.com/article/212-why-doesnt-my-inventory-quantity-match-what-i-expected"),
("Troubleshooting & FAQs", "Why Can't I Edit, Import, or Move Something?", "https://cyberstockroom.helpscoutdocs.com/article/213-why-cant-i-edit-import-or-move-something"),
("Troubleshooting & FAQs", "Why Was My CSV Import Rejected or Partially Imported?", "https://cyberstockroom.helpscoutdocs.com/article/214-why-was-my-csv-import-rejected-or-partially-imported"),
("Troubleshooting & FAQs", "Why Did Moving a Location Not Move Its Inventory?", "https://cyberstockroom.helpscoutdocs.com/article/215-why-did-moving-a-location-not-move-its-inventory"),
("Troubleshooting & FAQs", "Common Questions About Product Numbers, Duplicates, and Deleted Items", "https://cyberstockroom.helpscoutdocs.com/article/216-common-questions-about-product-numbers-duplicates-and-deleted-items"),
]

assert len(ARTICLES) == 55
KB = {i + 1: ARTICLES[i] for i in range(55)}

def kb(n):
    return f"KB-{n:03d}"

# primary lists by KB number
PRIMARY = {
1: ["MAP-001", "PRD-001", "XFR-001", "XFR-002", "XFR-003"],
2: ["MAP-036"],
3: ["MAP-005", "MAP-003", "MAP-036"],
4: ["PED-010", "PED-011", "PED-013"],
5: ["XFR-007"],
6: ["XFR-006", "PED-016"],
7: ["MAP-001", "MAP-004"],
8: ["MAP-005", "MAP-003", "MAP-006", "MAP-012", "MAP-037"],
9: ["MAP-008", "MAP-009", "MAP-010", "MAP-011", "MAP-030"],
10: ["MAP-024", "MAP-027"],
11: ["MAP-017", "MAP-031", "MAP-034", "MAP-035", "MAP-015", "MAP-042"],
12: ["MAP-028", "MAP-029"],
13: ["MAP-013", "MAP-014"],
14: ["MAP-016", "DSP-001"],
15: ["MAP-018", "MAP-019"],
16: ["MAP-007", "MAP-038", "MAP-039", "MAP-040"],
17: ["PRD-001"],
18: ["PED-001", "PED-010", "PED-011", "CFL-006"],
19: ["PED-012", "PED-013"],
20: ["PRD-001", "PRD-002", "PRD-003", "PRD-004", "PRD-005", "PRD-007", "PRD-008", "PRD-009", "PRD-011"],
21: ["PRD-006"],
22: ["PRD-011"],
23: ["PRD-010", "MAP-026", "PED-006", "XFR-004"],
24: ["PED-002", "PED-003", "PED-015", "MAP-040", "DSP-002"],
25: ["PED-007", "PED-008", "PRD-011"],
26: ["XFR-001", "MAP-020"],
27: ["XFR-002", "MAP-021"],
28: ["XFR-003", "MAP-022", "MAP-023"],
29: ["XFR-011"],
30: ["MAP-041", "XFR-011"],
31: ["XFR-005", "PED-014"],
32: ["XFR-012", "XFR-008", "XFR-009", "MAP-044", "MAP-043", "MAP-033"],
33: ["SRCH-001", "PRD-006", "MAP-018"],
34: ["ACT-001", "ACT-005", "ACT-006", "ACT-007"],
35: ["ACT-002", "ACT-003"],
36: ["ACT-004"],
37: ["RPT-001", "MAP-032"],
38: ["PRD-003", "RPT-001", "ACCSET-002"],
39: ["ACC-001", "ACC-002", "ACC-003", "ACC-011", "ACC-012"],
40: ["ACC-007", "ACC-008", "ACC-009", "ACC-010", "ACC-013"],
41: ["TEAM-001", "TEAM-002", "TEAM-003", "TEAM-004", "ACC-004"],
42: ["MAP-002", "PED-009", "TEAM-002", "ACC-013"],
43: ["CFL-001", "CFL-002", "CFL-003", "CFL-004", "CFL-005", "CFL-006"],
44: ["DSP-001", "DSP-002", "DSP-003", "DSP-004", "DSP-005", "DSP-006", "DSP-007", "MAP-025", "MAP-019"],
45: ["DEF-001", "DEF-002", "ACCSET-001", "ACCSET-002"],
46: ["SUB-001", "SUB-002", "SUB-003", "SUB-004", "ACC-005", "ACC-014"],
47: ["EXP-001", "EXP-002", "PED-005", "DSP-004", "DSP-005"],
48: ["API-001", "API-002"],
49: ["LSW-001", "PED-004"],
50: ["DSP-003", "PRD-002", "PRD-006", "MAP-018"],
51: ["MAP-023", "XFR-001", "XFR-002", "XFR-006"],
52: ["MAP-009", "SUB-004", "MAP-002", "PED-009"],
53: ["PED-012", "PED-013", "XFR-005"],
54: ["MAP-008", "MAP-010"],
55: ["PED-001", "PED-007", "PED-008", "PED-010", "PRD-011"],
}

# extra supporting (not already primary on that article)
SUPPORTING = {
1: ["SET-001", "ACT-001"],
2: ["MAP-005", "PED-010", "XFR-007", "MAP-001"],
3: ["MAP-009", "MAP-001"],
4: ["XFR-007", "PED-012", "PRD-002"],
5: ["XFR-001", "DEF-001", "PED-010", "MAP-020"],
6: ["XFR-001", "XFR-002", "XFR-003", "XFR-004"],
7: ["MAP-044", "MAP-009"],
8: ["MAP-007", "MAP-043"],
9: ["MAP-015"],
10: ["MAP-004", "PRD-001", "MAP-020"],
11: ["MAP-001", "MAP-044"],
12: ["MAP-004", "MAP-011"],
13: ["MAP-005"],
14: ["TEAM-004"],
15: ["DSP-006", "DSP-007", "MAP-025"],
16: ["MAP-041", "MAP-042", "MAP-006"],
17: ["PRD-010", "MAP-004", "DSP-003"],
18: ["PRD-007", "PED-009", "CFL-002", "PRD-011"],
19: ["XFR-007", "PED-010"],
20: ["DSP-002", "DSP-003", "PRD-006", "SET-001"],
21: ["SRCH-001"],
22: ["PRD-005", "CFL-006", "PED-001"],
23: ["XFR-004", "PED-006"],
24: ["PRD-009", "PRD-011", "MAP-039"],
25: ["PRD-005"],
26: ["XFR-006", "XFR-007", "XFR-008", "DEF-001", "PED-016"],
27: ["XFR-006", "XFR-008", "DEF-002", "MAP-004"],
28: ["XFR-006", "XFR-008", "XFR-009", "XFR-004", "MAP-042"],
29: ["MAP-041"],
30: ["XFR-012"],
31: ["PED-012", "XFR-006"],
32: ["XFR-001", "XFR-002", "XFR-003", "XFR-010", "MAP-017"],
33: ["MAP-018", "PRD-007"],
34: ["ACT-004", "ACCSET-001"],
35: ["ACT-001", "MAP-042"],
36: ["ACT-001", "ACT-002"],
37: ["PRD-011", "PRD-006"],
38: ["ACCSET-002", "PRD-003", "CFL-002"],
39: ["ACC-004", "SET-002"],
40: ["SET-002", "ACC-012", "ACC-011"],
41: ["SET-003", "ACC-013"],
42: ["TEAM-001", "TEAM-004", "PRD-001", "XFR-001"],
43: ["SET-002", "SET-003", "PED-001", "PRD-003"],
44: ["CFL-002", "MAP-015", "MAP-016", "EXP-001"],
45: ["SET-002", "XFR-007", "XFR-009", "ACT-001"],
46: ["SET-001"],
47: ["MAP-025", "PED-001"],
48: ["SET-003", "ACC-015"],
49: ["LSW-002", "LSW-003", "LSW-004", "LSW-005", "PED-002"],
50: ["MAP-002", "DSP-002", "PRD-001", "MAP-004"],
51: ["XFR-003", "PRD-010", "MAP-026"],
52: ["TEAM-002", "PED-012", "MAP-008", "CFL-003"],
53: ["PED-014", "IMP-placeholder"],
54: ["MAP-011", "MAP-014"],
55: ["PED-018", "CFL-003"],
}
SUPPORTING[53] = ["PED-014", "XFR-006"]

INTERNAL = {
"ACC-006": "Welcome.aspx redirects to the map before any wizard runs. Do not publish a welcome wizard.",
"DSP-008": "The Settings kitting checkbox is hidden and unwired. Do not publish it as the way to turn kitting on.",
"KIT-003": "The kit Manage button builds invalid JavaScript and is a copy of the expiration wizard. Do not publish it.",
"LSW-002": "Site picker exists but is not linked from current Settings.",
"LSW-003": "Field-match popup is not linked from current Settings. Stored pairing was not fully traced.",
"LSW-004": "Category-to-location match is not linked from current Settings.",
"LSW-005": "Link, sync, and progress popups are not linked from current Settings. Duplicate class binding is unverified.",
"PED-017": "Document Editor buttons are literal text with no handlers. Not product attachments.",
"PED-018": "Old clone popup, quantity-only delete dialog, SuccessProducts, and batches are not on the live click path.",
"XFR-010": "Legacy mobile product list and Quick Add are not the live auto path. Quick Add creates a catalog row and does not check it in.",
}

NEEDS = {
"ACC-015": "OAuth Allow and Cancel are real, but scope labels are outside this website repo. Do not list scope names.",
"RPT-002": "AI insights page exists at /ai-report.aspx?id= and has no menu link. Report generation is outside the files that were read.",
"EXP-002": "The replace-or-clone wizard is real. What each radio does to stock is an API outside this repo.",
"XFR-011": "Quick Scan posts api/inventory. The stock math of that API was not in this repo.",
"MAP-013": "Location clone posts api/LocationClone. Whether quantities copy was not in this repo.",
"KIT-001": "Kit create posts api/kit. Insert rules are outside this repo, and there is no help article.",
"KIT-002": "Kit component edit has confirmed page defects. Persistence is outside this repo, and there is no help article.",
"SRCH-001": "Header search calls developers.cyberstockroom.com. Which fields match is outside this repo.",
"MAP-018": "Map search calls api/map. Which fields match is outside this repo. Local title fallback is confirmed.",
}

GAPS = {"KIT-001", "KIT-002", "RPT-002"}

# workflows cited
WF = {
"WF-001": [4, 5, 19],
"WF-002": [5, 6, 26],
"WF-003": [6, 27],
"WF-004": [6, 28],
"WF-005": [29, 30],
"WF-006": [3, 8, 9, 13],
"WF-007": [4, 19],
"WF-008": [31],
"WF-009": [41],
"WF-010": [14, 44],
"WF-011": [47],
"WF-012": [],
"WF-013": [18, 21, 23, 33],
}

CODE = {
1: "UserPage.master; Map.aspx; Products.aspx; Start.aspx",
2: "Map_CONTROL_2017.ascx mapShowGettingStartedCard",
3: "Map_CONTROL_2017.ascx HoverAddClick; NewLocation.aspx.vb",
4: "AddProducts.aspx.vb btn_save_Click; ImportFromFile.aspx.vb",
5: "CheckInCreatedProducts.aspx.vb; CreatedProductCheckIn.vb",
6: "Start.aspx.vb FinishAddHandler, FinishCheckoutHandler",
7: "Map.aspx.vb Page_Init; Map_Styling.vb GetLocationCountLabel",
8: "NewLocation.aspx.vb; LocationEditor.aspx.vb; ConfirmationDialog.aspx.vb",
9: "Map_CONTROL_2017.ascx mapMapLockToggle, mapReparentClaspClick",
10: "Map_CONTROL_2017.ascx peekAtProducts, ProcessHover",
11: "Map_CONTROL_2017.ascx mapZoomStepIn, mapViewFinderInit, mapAbcSortToggle",
12: "Map_CONTROL_2017.ascx LocationEligibleForVerticalStack, map3dToggleStack",
13: "Map_CONTROL_2017.ascx cloneLocation, _cloneContents",
14: "webAPI/settings.aspx.vb SaveShareMapLayout; mapSyncLayoutModalConfirm",
15: "Map_CONTROL_2017.ascx mapFilterStartSearch, mapResolveQuantityTier",
16: "LocationEditor.aspx.vb; PeekLocationDetails.aspx.vb",
17: "Products.aspx.vb InventoryGetAndDisplay",
18: "ProductEditor.aspx.vb LoadFieldControls; AddProducts.aspx.vb",
19: "CSV_Class.ParseUpload; ImportFromFile.aspx.vb BuildCreateImport",
20: "Products.aspx.vb ColumnsDefaultDisplay, GridView1_Sorting",
21: "Products.aspx.vb SQLSearchClauseGet",
22: "Products.aspx.vb CheckedProductsMultiEdit",
23: "Products.aspx submitQtyQuickAdjust; Map_CONTROL_2017.ascx UpdateCount",
24: "ProductEditor.aspx.vb _upload_image; PrintBarcode.aspx; BarcodePngGenerator",
25: "ProductEditorClone.js; Product.DeleteProducts",
26: "Transfer.aspx isTransferCheckinMode; TransferFunctions.TransferProductsBackend",
27: "Transfer.aspx TransferEverything",
28: "Transfer.aspx TransferFunction; mapOpenInventoryTransferPage",
29: "Popups/QuickScan.aspx getTransactionType, apiPostTransaction",
30: "LocationEditor.aspx wireKioskLinks",
31: "Transfer.aspx BuildImportedTransferSelectionString",
32: "mobile_main.aspx; MOBILE_Process.aspx.vb; MOBILE_LocationSelector.aspx.vb",
33: "CS_SearchBox.ascx RegisterUserControlIndex",
34: "ActivityHistory DisplayHistory_FAST; ActivityDetails.aspx.vb",
35: "ActivityHistory InventoryActivityMatchesCategoryFilter, GetFilters",
36: "ActivityHistory DownloadReport, WriteActivityCsv",
37: "ExportReport.aspx.vb DownloadFile; Map BuildMapQuantityCsv",
38: "Products.aspx.vb cost column; ExportReport.aspx.vb",
39: "Login.aspx.vb btn_login_Click; Settings.aspx.vb btn_password_reset_click",
40: "ProfileRequired.aspx.vb; profile.js; ProfileIconPicker.ascx.vb",
41: "webAPI/invitations.aspx.vb SendInvitation; webAPI/users.aspx.vb",
42: "UserPage.master.vb HideSectionsForReadOnlyUsers; Map_read_only.aspx.vb",
43: "js/business/custom-fields.js; webAPI/customFields.aspx.vb",
44: "js/business/general-settings.js; webAPI/settings.aspx.vb",
45: "_locationSelectorToggle.aspx.vb; webAPI/settings.aspx.vb SetTimeZone, SetCurrencySymbol",
46: "js/business/subscription.js; BillingAccessGate.vb; BillingHistory.aspx.vb",
47: "Expirations.aspx; ProductEditor.aspx expiration script",
48: "js/business/api-keys.js; ApiKeyApplicationService.vb",
49: "Settings.aspx Lansweeper heading; ProductEditor _linkToLansweeper",
50: "Products.aspx.vb MessageNoProductsShow; Map mapFilterStartSearch",
51: "mapCommitSingleUnitTransfer; TransferFunctions.vb; Start.aspx.vb",
52: "mapMapLockToggle; BillingAccessGate.Enforce",
53: "CSV_Class.ParseUpload; BuildImportedTransferSelectionString",
54: "mapHookGridsterMapLock; mapReparentClaspClick",
55: "GetNextAutoSKU; ProductEditor.aspx product number label; DeleteProducts",
}

# Per-article narrative. Keys are KB numbers.
BODY = {}

def add(n, **kw):
    BODY[n] = kw

add(1,
audience="A new signed-in user.",
objective="See how the map, the product list, and inventory actions fit together.",
concepts=["The map is the layout of locations. Products are the catalog. Quantities live at locations. All Locations is not a physical place.", "Check-in, check-out, and transfer are different actions."],
prereqs=["A signed-in user. Read-only users can look, not create."],
steps=["Sign in.", "Open Map and notice locations as tiles.", "Open Products and notice the catalog, including All Locations.", "Open the activity icon and notice that history is a record, not an undo button."],
options="None on this overview.",
results="No data changes.",
errors="None.",
limits=["Do not describe Welcome or getting-started as a wizard. Both redirect to the map.", "Do not describe a plan-capacity limit."],
examples="A storeroom uses the map for rooms and shelves, the product list for item names, and check-in to place quantities on a shelf.",
screens=[("Map", "Click Map", "The location canvas", "The map is the home view of places"),
         ("Products", "Click Products", "The product grid", "The catalog is separate from the map")],
verify=["Live menu labels for Map, Products, and Activity."],
do_not=["Welcome wizard", "Dollar amounts", "Kitting as a Settings switch"],
uncertain=["None on this overview."])

add(2,
audience="A new admin setting up an empty account.",
objective="Finish a first location, a first product, and a first check-in.",
concepts=["Empty-map coaching appears on the designer map.", "Creating a product does not place stock until check-in is saved."],
prereqs=["Signed in, not read-only. An account with no locations or no products."],
steps=["Open Map.", "Follow the on-screen prompt to add a location.", "Open Products and click Click to create if the list is empty.", "Save the product, then check it into the location or skip."],
options="The two-minute check-in lesson title is “2 min lesson about checking in your products”.",
results="A location and, if check-in was saved, stock at that location.",
errors="Duplicate location name: “That location name is already in use!”",
limits=["Which coaching card wins for every mix of zero products and zero locations was not fully separated.", "This article overlaps the dedicated first-map, first-product, and first-check-in articles. Keep this one short and link to them."],
examples="A new warehouse adds one room, one item, and checks in a quantity of 1.",
screens=[("Map", "Open Map on an empty account", "Coaching card or empty-map prompt", "Where a new user starts"),
         ("Add Products", "Click create", "The add form with AUTO checked", "Products are created before they are placed")],
verify=["Which card shows for zero locations versus zero products."],
do_not=["A multi-step getting-started wizard that no longer runs."],
uncertain=["Card priority."])

add(3,
audience="A user building the first locations.",
objective="Create a top-level location and a nested location.",
concepts=["Types are Building, Warehouse, Store, Floor, Room, Closet, Shelf, Bin, and Vehicle.", "New locations default to Building when the type is missing, and parent All Locations.", "Type cannot be changed later."],
prereqs=["Signed in, not read-only. Map unlocked is not required to create."],
steps=["Click the floating +.", "Pick a type.", "Name it. The suggested name is New plus the type.", "Save.", "Click + on that tile to add a child."],
options="Nine location types. Default name New {type}.",
results="A location is created. Activity records a location create. Inventory does not move.",
errors="“That location name is already in use!” Empty-map coaching can swallow the floating + click.",
limits=["No control was found to change type after create.", "Mobile create only allows a top-level parent."],
examples="Add a Room named Office, then a Shelf named A1 inside it.",
screens=[("Map", "Click +", "Type toolbox", "The nine types"),
         ("New Location", "After picking a type", "Name field", "Default name and duplicate error")],
verify=["Toolbox labels BUILDING through VEHICLE."],
do_not=["Changing a location type later."],
uncertain=["None."])

add(4,
audience="A user creating catalog items.",
objective="Add one product by typing, or many from a CSV, then decide whether to check them in.",
concepts=["AUTO product numbers look like CSN- plus nine digits.", "An empty description becomes the product number.", "Existing product numbers are skipped, not updated."],
prereqs=["Signed in, not read-only. Account type 1 hides prices."],
steps=["On Products, click Add.", "Leave AUTO on, or type a number.", "Enter a description and optional prices.", "Save.", "On the next page, check the products into a location or skip."],
options="Prices must be 0 or greater. Staged quantity is 1. Sample CSV headers are examples, not required names.",
results="Catalog rows exist. Stock exists only if check-in is saved.",
errors="“Product number already exists”. “Could not verify product number”. Blank manual number shows the placeholder “No Poduct Number!”",
limits=["A quantity row at All Locations is inserted without a quantity column. The database default is uncertain. Do not promise a visible quantity from create alone."],
examples="Add “Safety glasses” with AUTO on, then check in 10 to a shelf.",
screens=[("Add Products", "Open Add", "AUTO checked", "How a number is assigned"),
         ("Check-in after create", "After save", "Map prompt", "Create and check-in are separate")],
verify=["The misspelled placeholder if a manual number is left blank."],
do_not=["Updating existing products from a create import."],
uncertain=["Database default quantity on the All Locations row."])

add(5,
audience="A user who just created products.",
objective="Place those new products into one location.",
concepts=["The catalog rows already exist.", "This page adds stock. It does not create the products.", "Skip leaves them with no placed stock."],
prereqs=["A batch of just-created products. Signed in, not read-only."],
steps=["When the check-in page opens, click a location. The suggested one is the default check-in location.", "Enter whole-number quantities. At least one line must be 1 or more.", "Save, or add a comment.", "Or click Skip."],
options="If every imported line names a location, the map is hidden and each line uses its own location.",
results="An additive check-in. Returning to an open transfer does not change stock until that transfer is saved.",
errors="“No products are waiting to be checked in.” “Each quantity must be a whole number, 0 or greater.” “Select a location on the map before checking in.” “A location in this import could not be found.”",
limits=["One bad imported location aborts the whole save."],
examples="Three new products, all checked into Receiving.",
screens=[("Check-in created products", "After creating products", "Map and quantity boxes", "One location for the batch")],
verify=["Skip versus Continue when opened from a transfer."],
do_not=["Saying create itself placed the stock."],
uncertain=["None for the page. Stock write uses the in-repo check-in path."])

add(6,
audience="A user choosing among check-in, check-out, and transfer.",
objective="Pick the right action and know that the Start page is not the same as Transfer.",
concepts=["Check-in adds. Check-out removes from a place. Transfer moves between two places.", "There is no Adjust action on Transfer or Start.", "Start writes stock before it asks for a comment. Transfer asks as part of save.", "Start check-out subtracts and stops at 0. Transfer check-out sets the source to the quantity you left behind."],
prereqs=["Signed in, not read-only. The Start menu hides when the account has no products."],
steps=["Open Start.", "Choose Check In, Check Out, Transfer, Create, or Quick Scan.", "Pick locations. The same place twice on a transfer says “The Source can't be the Destination!”", "Finish. Then, if you want, save a comment. That comment is a second write."],
options="A query can open check-in, check-out, transfer, or add directly.",
results="Stock changes before the comment box on Start.",
errors="A missing location cookie exits without saving. Zero products: “You have not added any products yet”.",
limits=["Do not tell readers the Start page and the Transfer page update quantities the same way."],
examples="Use check-in when goods arrive, check-out when they leave, transfer when they move from one shelf to another.",
screens=[("Start", "Open Start", "The action choices", "The five actions"),
         ("Start comment", "After finish", "Comment box", "The comment appears after the stock change")],
verify=["Comment timing on a Start check-in in a test account."],
do_not=["An Adjust button on Transfer or Start."],
uncertain=["None for Start’s own math."])

add(7,
audience="Any signed-in user looking at the map.",
objective="Read a location tile correctly.",
concepts=["A tile’s own quantity and its children’s quantity are different.", "A ghosted tile has stock only in children.", "A 3D parent can look full because of children and still not be draggable.", "Read-only users see the same canvas with a shorter hover menu."],
prereqs=["Signed in. Read-only users are sent to the read-only map."],
steps=["Click Map.", "Read a tile: a number is its own quantity, a number in parentheses is in children.", "Try to drag only a tile whose own quantity is above 0."],
options="None.",
results="Display only.",
errors="None.",
limits=["Do not say a ghosted tile can be dragged.", "Do not claim read-only users cannot drag. The move handle is still drawn and drag was not separately blocked."],
examples="A room shows 0 (12) because the shelves inside hold the stock.",
screens=[("Map", "Open Map", "A parent and a child tile", "Own quantity versus child quantity")],
verify=["A 3D parent with only child stock does not start a drag."],
do_not=["Right-click menu.", "Free resize."],
uncertain=["Whether a read-only user can drag the move handle."])

add(8,
audience="A user maintaining the location tree.",
objective="Create, rename, and delete a location.",
concepts=["Delete always includes sub-locations.", "Delete checks products out of those locations.", "The include-sub-locations checkbox is hidden and unread.", "There is no No button. Closing the popup cancels."],
prereqs=["Signed in, not read-only."],
steps=["Create from + as in the first-map article.", "Open the location editor and change the name.", "Delete and read the confirm: “Are your sure you want to DELETE this location?” and the line that sub-locations will be deleted and products checked out.", "Click YES, or close the popup to cancel."],
options="All Locations cannot be renamed.",
results="Rename keeps the same location id. Delete removes the location and descendants after a check-out activity.",
errors="Duplicate name: “That location name is already in use!” Unknown id shows Location Error.",
limits=["The confirm contains the typo “Are your sure”. Quote it or paraphrase without pretending the product says “you”.", "Do not offer a choice to keep sub-locations."],
examples="Rename Shelf A to Shelf B. Delete an empty closet and its bins.",
screens=[("Location editor", "Open a location", "Name field", "Rename"),
         ("Delete confirm", "Delete", "The warning text", "Sub-locations and check-out")],
verify=["YES checks quantities out before the location row disappears."],
do_not=["A No button.", "Keeping child locations while deleting the parent."],
uncertain=["None."])

add(9,
audience="A user arranging the map.",
objective="Move locations, change a parent, and unlock the map.",
concepts=["The map is locked by default.", "Dragging moves the tile, not the inventory.", "Reparent keeps nested locations with the one you move.", "Tile size follows children. There is no resize handle."],
prereqs=["Signed in, not read-only. Desktop for multi-select."],
steps=["If a drop snaps back, unlock the map.", "Drag the diamond header to move a primary location.", "Use the clasp, click a new parent or empty canvas, and confirm Move location?", "Hold Ctrl and click several tiles, or Ctrl-drag a rectangle, then drag the group."],
options="Empty canvas makes the location primary. ABC sort is display order only and is covered in Navigating the Map.",
results="Coordinates change for this user. Inventory stays on the same location ids.",
errors="“Could not move location”. Lock on cancels an in-progress reparent.",
limits=["Fewer than two children skips ABC sort. Overlap is rejected while locked."],
examples="Drag Receiving to the left. Move Bin 3 from Shelf A onto Shelf B.",
screens=[("Map", "Locked map", "Unlock control", "Default is locked"),
         ("Reparent", "Clasp then a parent", "Move location? confirm", "Children stay with the location")],
verify=["Unlock, overlap a tile, and confirm it stays. Relock and confirm a bad drop snaps back."],
do_not=["Saying a move relocates quantities. That misconception has its own article."],
uncertain=["None."])

add(10,
audience="A user who wants the items inside a place.",
objective="Peek at a location and open its product list.",
concepts=["Peek shows up to 25 products.", "View opens the product list filtered to that location."],
prereqs=["Signed in."],
steps=["Click a location.", "Read the rows. Escape closes the peek.", "Use View, or View Products in the editor, to open Products for that location."],
options="While map search is active, the peek includes the search terms.",
results="No stock change from viewing.",
errors="None.",
limits=["A specific location’s product list shows quantity greater than 0 there. If the location is empty but children are not, the list says so."],
examples="Click a truck tile, see three products, then open the full list.",
screens=[("Map", "Click a location with stock", "Peek list", "Products inside one location")],
verify=["Escape closes the peek."],
do_not=["None."],
uncertain=["None."])

add(11,
audience="A user moving around a large map.",
objective="Zoom, pan, search the canvas, sort children, and use the minimap.",
concepts=["Desktop zoom defaults to 1 and stays between 0.1 and 1.", "Touch zoom defaults to 0.74 and can go up to 2.2.", "Keys + and - multiply by 1.1 or 0.9.", "ABC sort orders children by name. It does not change inventory."],
prereqs=["Signed in."],
steps=["Click + or - or pinch.", "Drag empty canvas to pan. Use Scroll to map origin when you are away from the top left.", "Type in Search Map, press Enter to cycle matches, Escape to clear.", "Open the minimap and click it to scroll.", "Turn ABC sort on from the map controls if children should be alphabetical."],
options="Minimap is 240 by 160 and can auto-open. Narrow layout uses the mobile zoom.",
results="This user’s view and, for ABC sort, this user’s display order.",
errors="Empty search disables quantity-report download with “No results to download”. API search failure falls back to matching location titles.",
limits=["Which fields the map API matches is Uncertain. Do not list fields beyond the title fallback."],
examples="Zoom out, find “Dock” with Search Map, then jump back with the minimap.",
screens=[("Map", "Zoom in", "A closer canvas", "Zoom limits"),
         ("Search Map", "Type a name and press Enter", "A highlighted tile", "Enter cycles matches")],
verify=["+ and - while not typing in a field."],
do_not=["Browser Ctrl+wheel as the map zoom. The page blocks that."],
uncertain=["Map API match fields."])

add(12,
audience="A user with locations that contain other locations.",
objective="Stack children vertically or in 3D.",
concepts=["Vertical needs at least two children.", "A child that has its own children must already be 3D.", "3D hides children in an overlay. These are layout only."],
prereqs=["Signed in, not read-only. A parent with children."],
steps=["Hover More actions, then V, or use Vertical on a narrow screen.", "If the tooltip says to turn a child to 3D first, do that, then try Vertical again.", "Click 3D on a parent. Click the parent to open the stack. Click Add inside it to create a child."],
options="None beyond the two modes.",
results="This user’s layout. Inventory unchanged.",
errors="Tooltips include “Needs at least two children”, “Turn off 3D first”, and “A child has its own locations. Turn that child to 3D first”.",
limits=["Vertical is hidden inside a 3D stack.", "Do not call the sloped tile edge a 3D label."],
examples="Turn a closet with three shelves into a vertical stack.",
screens=[("Map", "Hover a parent with two children", "Vertical and 3D", "When each action is offered")],
verify=["A parent with one child does not offer a successful vertical stack."],
do_not=["None."],
uncertain=["None."])

add(13,
audience="A user duplicating a room or its stock.",
objective="Clone a location’s structure, or copy stock with Ctrl+drop.",
concepts=["Structure clone and stock copy are different.", "Ctrl+drop warns that existing items at the destination are cleared first.", "Auto-rename of sub-locations is off by default."],
prereqs=["Signed in, not read-only. Ctrl+drop needs a location with its own quantity above 0, and multi-select must be off."],
steps=["Open clone, type a name up to 255 characters. The suggestion is the name plus (Copy).", "Leave Auto-Rename Sub-Locations off unless a word or hyphen part should change in the children.", "Confirm.", "Separately, hold Ctrl, drag a full location onto another, and confirm the clear-first message."],
options="Copy names run up to (Copy 999). Same name as the source or a sibling is blocked.",
results="Structure clone creates locations. Whether it copies quantities is Uncertain. Ctrl+drop is a stock copy.",
errors="Could not complete the clone if the API fails. Do not invent the error text.",
limits=["Do not say the structure clone copies quantities.", "Blocked during multi-select and when the drag is a product chip."],
examples="Clone Aisle A to Aisle B and rename A- bins to B-. Then Ctrl-drop one bin’s stock onto an empty bin.",
screens=[("Clone modal", "Start clone", "Name and auto-rename", "Structure only"),
         ("Ctrl+drop", "Drop onto a location", "Clear-first confirm", "Stock copy")],
verify=["Auto-rename off leaves child names unchanged except the new root name."],
do_not=["Quantities copied by LocationClone."],
uncertain=["api/LocationClone quantity copy. api/inventory clone body."])

add(14,
audience="An admin and a teammate who wants that admin’s layout.",
objective="Share a map layout and sync to it.",
concepts=["Sharing copies coordinates, zooms, and vertical or 3D stacks. It does not copy inventory.", "Only an admin can turn sharing on.", "An invite copies coordinates with the share marker stripped."],
prereqs=["Admin for the switch. Any signed-in user can sync."],
steps=["In Settings, under Options, turn Share Map Layout on.", "As another user, open the map gear, then Shared Maps.", "Pick a person. Read the warning that your layout will be lost.", "Click Sync, or Keep my layout."],
options="Default sharing is off.",
results="The other user’s layout is replaced only if they click Sync.",
errors="“No shared maps. Admins can share their maps in the Settings page.” “Could not load shared maps.” “Could not save the synced layout. Please try again.”",
limits=["Teammates cannot edit the shared original."],
examples="An admin arranges the building. A new hire syncs to that layout.",
screens=[("Settings Options", "Share Map Layout", "The toggle", "Admin-only switch"),
         ("Shared Maps", "Gear, Shared Maps", "Sync warning", "Keep my layout versus Sync")],
verify=["A non-admin does not see the share switch."],
do_not=["Sharing products or quantities."],
uncertain=["None."])

add(15,
audience="A user looking for a place or a low or high quantity.",
objective="Search the map and read quantity colors.",
concepts=["Enter cycles matches. Escape clears.", "Colors use the threshold and max highlight from Settings.", "Quantity 0 is not colored as a low or high tier."],
prereqs=["Signed in. Threshold and max highlight are optional."],
steps=["Type in Search Map and press Enter.", "Turn on Quantity Threshold and Max Highlight in Settings if you want color.", "Search again and read low, mid, and max colors."],
options="Threshold off is 0. Turning it on starts at 1. Max highlight must be above the threshold. Off displays as 10.",
results="Highlight only. Inventory unchanged.",
errors="“No results to download” when a search matches nothing and a report is requested.",
limits=["Do not list the API’s match fields. On API failure the page matches location titles."],
examples="Search “bin” and cycle with Enter. Set threshold 5 and see low tiles.",
screens=[("Map search", "Enter a term", "Highlighted tiles", "Cycling matches"),
         ("Settings", "Quantity threshold", "The number and the white-zero sentence", "Where the color rules are set")],
verify=["A zero-quantity location stays white."],
do_not=["Invented search fields."],
uncertain=["api/map match fields."])

add(16,
audience="A user editing one location’s details.",
objective="Rename, attach a file, set a barcode, print it, and open the kiosk.",
concepts=["Read-only peek can download files and print. It cannot edit the barcode or upload.", "A duplicate barcode turns the box red and does not save.", "Kiosk links are covered in their own article."],
prereqs=["Editor: not read-only. Peek: signed in."],
steps=["Open the location editor.", "Change the name.", "Use the paperclip to attach a file. Delete asks “Are you sure you want to delete this attachment?”", "Scan or type a barcode and press Enter.", "Use Print Barcodes if needed."],
options="Barcode label is “Barcode # (scan to change)”.",
results="Name, file, or barcode saved on that location.",
errors="Duplicate barcode: red box, no alert. Duplicate name: “That location name is already in use!”",
limits=["All Locations is not editable.", "A Load Type other than EXISTING creates immediately. The map always sends EXISTING. Do not tell users to change Load Type."],
examples="Attach a floor plan PDF and set the room barcode.",
screens=[("Location editor", "Open a location", "Name, barcode, paperclip", "The tools on one location")],
verify=["A taken barcode does not save."],
do_not=["Upload from the read-only peek. The icon does not upload."],
uncertain=["None."])

add(17,
audience="A user learning what a product quantity means.",
objective="Tell catalog quantity, location quantity, and All Locations apart.",
concepts=["All Locations is the catalog view.", "A specific location lists products with quantity above 0 there.", "Zero-quantity rows can be hidden by a per-user setting.", "Cost value is quantity times buy price. It is calculated, not stored."],
prereqs=["Signed in."],
steps=["Open Products on All Locations.", "Switch to one location.", "If the location is empty but children are not, read that sentence.", "Compare a quantity edited on the product map with the number in the list."],
options="Show zero-quantity products is a Settings option.",
results="Display. Editing quantity is a different article.",
errors="Empty catalog: “No products yet”. Empty location: “Location is empty...”",
limits=["Search forces All Locations for that request."],
examples="All Locations shows 20. The truck shows 3. The rest is in other places.",
screens=[("Products", "All Locations", "Quantity column", "Catalog versus one place")],
verify=["A location with stock only in children shows the empty-but-children message."],
do_not=["None."],
uncertain=["None."])

add(18,
audience="A user adding or editing a product.",
objective="Create a product and edit its name, prices, and custom fields.",
concepts=["The product number cannot be renamed.", "Buy and sell show only when those prices are visible and the account is not a records account.", "Presets offer (none), each preset, the current value if it is outside the list, and Other (Specify)."],
prereqs=["Signed in, not read-only. Presets are account-wide. Price visibility is per user."],
steps=["Click Add, or click a product row.", "Edit the name. Leave prices blank to keep 0, or enter a number that is not negative.", "Pick a preset or Other (Specify).", "Save. Admins can click Edit your fields."],
options="Currency rejects non-numeric and negative values.",
results="Activity records “Changed '{label}' to '{value}'.”",
errors="“The Buy Price is not valid!” “The Sell Price is not valid!” The product-name error string is not used unless a numeric check runs. Do not promise that sentence.",
limits=["Read-only editor is view only.", "Account type 1 hides prices."],
examples="Set Sell Price to 12.50 and a Supplier preset.",
screens=[("Product editor", "Open a product", "Name, prices, custom fields", "Number is not editable"),
         ("Add Products", "Add", "AUTO and description", "Create path")],
verify=["Other (Specify) accepts free text. A preset not in the list is rejected on multi-edit."],
do_not=["Renaming the product number."],
uncertain=["None."])

add(19,
audience="A user loading many products from a spreadsheet.",
objective="Import a CSV that creates products and stages quantities for check-in.",
concepts=["Under 250 KB, at most 100 columns, UTF-8, commas.", "The first row is the header.", "At least a product number must be mapped.", "Sample headers are examples."],
prereqs=["Signed in, not read-only."],
steps=["From Add Products, upload the file.", "Drag columns onto Product Number and any other fields.", "Fix row errors.", "Continue to check-in."],
options="Unmapped quantity stays 1, prices 0, location All Locations. Expiration imports only for new numbers, and only if expirations are on.",
results="New numbers are created. Existing numbers keep their fields. Their quantity is staged for check-in.",
errors="“This file is too large. Use a CSV smaller than 250 KB.” “You must select at least a Product Number to upload.” Duplicate numbers in the file are rejected. Quote the other file errors from the catalog entry PED-012.",
limits=["Presets are not enforced on import.", "Do not say an existing product’s description is updated."],
examples="A three-column file of number, name, and quantity.",
screens=[("Import", "After upload", "Column matching", "Product Number must be mapped")],
verify=["A semicolon file is rejected.", "An existing product number is not overwritten."],
do_not=["Semicolon CSV as supported."],
uncertain=["None for the parser."])

add(20,
audience="A user working in the product grid.",
objective="Choose columns, sort, page, select, and use the toolbar.",
concepts=["Page size is 50.", "Product Number cannot be unchecked.", "Select all means every product in the account, not the current location or search.", "Printable view does not call print by itself."],
prereqs=["Signed in. Some toolbar buttons are absent for read-only."],
steps=["Open Products.", "Click column headers to sort. Click again to reverse.", "Use SAVE COLUMNS after showing or hiding columns.", "Select the page, then Select all only if you mean the whole catalog.", "Use Add, export, print barcodes, or printable from the toolbar. Delete and multi-edit have their own articles."],
options="Default sort is product number ascending. Cost value is calculated.",
results="Column choices are per user.",
errors="“No products yet”. “No matches found!”",
limits=["The SQL page size grows on later pages, so a later page can show more than 50 rows. Mention this only if the live grid does it.", "A cell that is only a web address becomes a link and does not open the editor."],
examples="Hide Sell Price, sort by quantity, select this page only.",
screens=[("Products", "Open the grid", "Headers and toolbar", "Sort and toolbar"),
         ("Columns", "SAVE COLUMNS", "The checkbox list", "Product Number stays on")],
verify=["Select all count versus the rows on the page."],
do_not=["Select all as “this location only”."],
uncertain=["Read-only URL pills were not re-verified."])

add(21,
audience="A user finding products in the list.",
objective="Search the product list and understand what matches.",
concepts=["Header Enter stores the term and opens Products.", "Comma-separated terms are combined with AND.", "Each term matches product number, name, and every custom field, including hidden columns. Not price or quantity.", "Search forces All Locations and hides the pager."],
prereqs=["Signed in."],
steps=["Type in the header and press Enter.", "Read the chips.", "Remove a chip to widen the search."],
options="No AND/OR syntax beyond commas. % and _ act as wildcards.",
results="A filtered catalog view. No data change.",
errors="“No matches found!”",
limits=["Do not say search matches buy price, sell price, or quantity."],
examples="Search “gloves, large” to require both words.",
screens=[("Products", "After Enter", "Chips and results", "AND search")],
verify=["A price value does not match."],
do_not=["Search operators."],
uncertain=["None for the product-list search. Header suggestion fields are a different article."])

add(22,
audience="An editor changing many products at once.",
objective="Set one field on the selected products.",
concepts=["Quantity is available only when a real location is selected, and it overwrites. It does not add.", "Empty value is rejected.", "Presets are enforced unless the value is empty or Other (Specify).", "Select all edits the whole account."],
prereqs=["Signed in, not read-only. A selection."],
steps=["Select products. Avoid Select all unless you mean every product.", "Open For All Selected Items.", "Choose a field, enter a value, and set it."],
options="Fields: Product Name, Quantity at a real location, Buy Price, Sell Price, and each custom field.",
results="Those products change. Activity records a product edit with quantity 1 in the log, not the number you typed.",
errors="“Please enter a value”. “Value must be numeric!” “Value is not allowed for this field.”",
limits=["Do not say quantity is added to the current amount."],
examples="Set Supplier to Acme for the five selected gloves.",
screens=[("Products", "Select rows", "For All Selected Items", "One field for the selection")],
verify=["Quantity at a location replaces the old number."],
do_not=["Multi-edit as a way to add stock."],
uncertain=["None."])

add(23,
audience="A user correcting a quantity without a transfer.",
objective="Type a new quantity on the product list or the product map.",
concepts=["This is not a Transfer mode.", "The list editor works only on the editable page, at a real location, on an in-stock cell, and not during search.", "Down stops at 0.", "The on-screen number updates when the request is sent."],
prereqs=["Signed in, not read-only. A specific location."],
steps=["On the product map, click a location, type a whole number, and press Enter.", "Or on the product list, edit the quantity cell and confirm.", "Read the failure alert if it appears. The number may already have changed on screen."],
options="Arrow keys step the value on a fine pointer.",
results="An adjust request with source and destination equal to that location.",
errors="“There was a problem updating the quantity in this location...”",
limits=["Do not document an Adjust button on Transfer.", "Invalid map input becomes 0.", "Timeout is 3 seconds."],
examples="Change a bin from 4 to 6 without checking out and back in.",
screens=[("Product editor map", "Click a location", "Quantity being typed", "Enter saves"),
         ("Product list", "A location view", "An editable quantity", "Not available during search")],
verify=["Search hides list editing. All Locations hides it."],
do_not=["Transfer adjust mode."],
uncertain=["The remote API’s final stock write beyond the request the page sends."])

add(24,
audience="A user adding photos, files, and barcode labels.",
objective="Update a product image, attach a file, and print a label.",
concepts=["Product photos in the list depend on the display setting.", "There is no size or type check on the product photo upload.", "Label stocks are 30252 (default), 30336, 30334, and 30330.", "Location barcodes are edited in the location editor. Product labels are printed from the product."],
prereqs=["Signed in. Read-only can download attachments and cannot upload.", "List photos require the product-images setting."],
steps=["Open a product and click the image.", "Use the paperclip to attach or download a file. Confirm before delete.", "Select products and print barcodes. Choose a stock size. Preview.", "Turn on product images in Settings if the grid should show photos."],
options="Default stock 30252, 1-1/8 by 3-1/2 inches. Code 128. Missing name prints as UNTITLED.",
results="Image or file stored. Print does not write the database.",
errors="Attachment delete confirm: “Are you sure you want to delete this attachment?”",
limits=["A Lansweeper image disables product upload.", "Select-all print asks before printing every product.", "The printable list does not send the job to the printer by itself."],
examples="Print 30336 labels for five selected SKUs.",
screens=[("Product editor", "Click the photo", "Upload", "No type check to mention as a guarantee"),
         ("Print barcodes", "After a selection", "Stock sizes", "30252 is first")],
verify=["Read-only cannot upload.", "Unknown stock falls back to 30252."],
do_not=["Document Editor as the attachment tool."],
uncertain=["None."])

add(25,
audience="A user copying or removing a product.",
objective="Clone a product without its stock, or delete it from the catalog.",
concepts=["Clone copies fields, image when it can, and expiration if set. It does not copy stock, locations, or attachments.", "Delete says it also checks the product out of all locations.", "Select all before delete deletes every product in the account.", "The old clone popup and the quantity-only delete dialog are not the live path."],
prereqs=["Signed in, not read-only."],
steps=["Open a product, click Clone Product, leave Auto on or type a new number, and confirm.", "Or click Delete this product and confirm.", "From the list, select rows and delete. Read the cannot-be-undone warning."],
options="Auto number is CSN- plus nine digits.",
results="A new catalog row, or the product is removed. What else the deleter removes is Uncertain beyond the expiration call the page makes.",
errors="“You must enter a product number.” “That product number already exists!”",
limits=["Do not say clone copies quantities.", "Do not describe delete as a choice between one location and all locations. That dialog is unwired."],
examples="Clone a glove to a new color. Delete a discontinued SKU.",
screens=[("Clone", "Clone Product", "Auto checked", "Stock is not copied"),
         ("Delete", "Delete this product", "Check-out warning", "The live delete")],
verify=["Cloned product has no location quantity."],
do_not=["Popups/CloneProduct.aspx.", "The quantity-only delete dialog."],
uncertain=["productDeleter cascade."])

add(26,
audience="A user receiving stock.",
objective="Check products into a location.",
concepts=["Source is All Locations.", "Click moves 1. There is no check-in everything.", "Save adds the quantities.", "The Start page also adds, but the comment comes after the write.", "If a URL asks for both check-in and check-out, check-out wins."],
prereqs=["Signed in, not read-only. A real destination. Empty locations and All Locations as the destination are refused from the map."],
steps=["From the map, start check-in on a location.", "Or open Check In from Start or the phone menu.", "Search or scan. Click a product to take 1. Type a larger quantity when asked.", "Click Check In. Skip the comment or save one."],
options="New Products and import show only while the destination selection is empty, unless import is hidden.",
results="One check-in activity. Quantities increase at the destination.",
errors="“Please enter a quantity of at least 1.” “Product Number '{scan}' doesn't exist!” on desktop. A mobile miss can open Add Products.",
limits=["Do not describe this as subtracting from a source location. The source is the catalog."],
examples="Receive 12 boxes into Receiving.",
screens=[("Transfer check-in", "Open check-in", "Infinity list and destination", "Catalog on the left"),
         ("Save", "Check In", "Comment Skip or Save", "The save button label")],
verify=["There is no Check In Everything button."],
do_not=["Check-in everything.", "Adjust mode."],
uncertain=["None for the Transfer backend."])

add(27,
audience="A user issuing stock.",
objective="Check products out of a location.",
concepts=["Destination is All Locations.", "Click moves 1 up to on-hand. Drag moves the rest.", "Save sets the source to the quantity left behind. It does not subtract on this page.", "Start check-out does subtract and stops at 0.", "Activity stores the quantity that moved."],
prereqs=["Signed in, not read-only. Stock at the source."],
steps=["Drag a full location to Drag inventory here to check out, or open Check Out.", "Move quantities.", "Click Check Out.", "Use Check-Out Everything only when you want the whole location. It hides while a map filter is on."],
options="The add-quantity box still says Transfer. Describe the action as check-out anyway.",
results="Source quantity becomes what you did not move.",
errors="“Product '{term}' was not found at this location.” “Please enter a quantity up to {max}.”",
limits=["Do not say Transfer check-out subtracts. Say the source is set to the remaining quantity."],
examples="Check out 2 of 10 and leave 8.",
screens=[("Check-out", "Open check-out", "On-hand list", "Zero rows are omitted"),
         ("Everything", "Check-Out Everything", "The count", "Hidden during a map filter")],
verify=["Remaining quantity on the source after a partial check-out."],
do_not=["Merging this with Start’s subtract-and-floor behavior without naming both."],
uncertain=["None for Transfer."])

add(28,
audience="A user moving stock between two places.",
objective="Transfer a partial or full quantity, and know the one-unit map path clears the source.",
concepts=["Both locations must be real and different.", "Destination becomes its current quantity plus what you moved.", "Source becomes what you left behind on the Transfer page.", "A map drag of quantity 1 sets that product’s source quantity to 0. That is not move-1-and-keep-the-rest."],
prereqs=["Signed in, not read-only."],
steps=["Drop a location or a product row onto a different location.", "If the one-unit comment appears, Cancel to stop, or save knowing the source for that product becomes 0.", "Otherwise set partial quantities and click Transfer.", "On Start, pick source then destination. The same place is rejected."],
options="Transfer Everything moves all remaining, like check-out everything.",
results="One transfer activity.",
errors="“The Source can't be the Destination!”",
limits=["If loading the destination product throws, destination quantity is treated as 0 and then set to the moved amount only. Mention this as a failure case, not the normal add."],
examples="Move 4 from Shelf A to Shelf B and leave the rest on A. Separately, drag a single unit and expect the source to show 0.",
screens=[("Map drop", "Drop onto another location", "Transfer popup", "Partial quantities"),
         ("One unit", "Drag quantity 1", "Moving this item", "Source becomes 0")],
verify=["A quantity of 2 uses the Transfer page, not the one-unit clear.", "A quantity of 1 on the map clears the source."],
do_not=["Describing the one-unit path as a normal partial transfer."],
uncertain=["None for the in-repo backends."])

add(29,
audience="A user with a scanner.",
objective="Check in, check out, or transfer by scanning, without creating products.",
concepts=["Mode is derived. Source only checks out. Destination only checks in. Both transfer.", "Save posts to the inventory API. What that API does to stock is Uncertain.", "Quick Scan does not create a product."],
prereqs=["Signed in, not read-only."],
steps=["Open Quick Scan.", "Scan a location, then products, or scan products after a kiosk has locked the location.", "Save."],
options="Placeholder “ready to scan...”. Kiosk modes are the next article.",
results="“{N} Transactions completed successfully.” or, on mobile, “Transaction saved”.",
errors="“You have to select at least one location and one product!” “There was a problem saving the transaction!”",
limits=["Do not state the resulting on-hand numbers. Verify them live or omit them.", "No lot, expiration, or kit fields."],
examples="Scan a bin, scan three items, save a check-out.",
screens=[("Quick Scan", "Open it", "Ready to scan", "Location then products")],
verify=["A product-only scan cannot save.", "On-hand after save, in a test account, before documenting the math."],
do_not=["Create-on-scan.", "A specific stock formula."],
uncertain=["api/inventory stock math."])

add(30,
audience="A user setting a station at one location.",
objective="Open a check-in or check-out kiosk for one location.",
concepts=["Transfer is not a kiosk mode.", "Location scans are ignored in kiosk mode.", "Narrow screens use the mobile Quick Scan page."],
prereqs=["Signed in, not read-only. A saved location."],
steps=["Open the location editor.", "Click Checkin Kiosk or Checkout Kiosk.", "Scan products only.", "Save."],
options="The link carries mode and locationID.",
results="Same save as Quick Scan, with the location fixed.",
errors="Same as Quick Scan, plus “Kiosk mode is active…” when a location scan is attempted. Quote the catalog sentence from XFR-011.",
limits=["Do not offer a transfer kiosk."],
examples="A receiving desk uses Checkin Kiosk on the dock location.",
screens=[("Location editor", "Kiosk links", "Checkin Kiosk and Checkout Kiosk", "Two modes only")],
verify=["A location barcode does not change the kiosk location."],
do_not=["Transfer as a kiosk mode."],
uncertain=["API stock math, same as Quick Scan."])

add(31,
audience="A user moving many lines from a file.",
objective="Import a list into check-in, check-out, or transfer without creating products.",
concepts=["This mode does not insert products.", "Match by product number, description, or a custom field.", "More than one match is skipped.", "Check-in keeps the file quantity. Check-out and transfer cut it to on-hand.", "The page locks until save or cancel."],
prereqs=["Signed in, not read-only. Import before the destination selection is filled."],
steps=["Open check-in, check-out, or transfer.", "Click import.", "Map the columns. Transfer files use FROM and TO.", "Review skips and reductions.", "Save or cancel."],
options="Samples: Product Number and Quantity. With a location, add Location. Transfer adds FROM and TO.",
results="Save uses that mode’s activity. An unedited import tags the comment. Cancel writes nothing.",
errors="Quote the file and row errors from XFR-005, including “This value matched more than one product” and “This product was not found at the source location.”",
limits=["The Start page can consume a similar file and then add or subtract. Say so if you mention Start. Do not treat it as the Transfer overwrite."],
examples="A checkout file of SKU and quantity against one bin.",
screens=[("Transfer", "Import before locations are chosen", "Review list", "Skipped and reduced rows")],
verify=["Cancel does not change stock.", "An ambiguous name is skipped."],
do_not=["Creating products from this import."],
uncertain=["A few transfer-import skip strings were not fully quoted in the catalog. Do not invent them."])

add(32,
audience="A user on a phone.",
objective="Use the same map and the mobile check-in, check-out, and transfer flow.",
concepts=["The phone map is the same 2017 map, not a separate mobile map page.", "Opening mobile home clears an in-progress process.", "There is no footer Transfer. Transfer is in the menu when products exist.", "A return token of Map without .aspx lands on mobile home, not the map."],
prereqs=["Signed in. About 900px wide uses the phone layout."],
steps=["Open the menu: Home, Map, Products, Activity, Check In, Check Out, Transfer, Quick Scan, Help, Settings, Logout.", "Pick a location. Use the default badge to change the saved default.", "Finish the movement.", "On the map, use the bottom bar: Edit, Clone, Vertical, 3D, Delete, Close. The first tap selects."],
options="Tablet mode turns multi-select off. Pinch-zoom of the browser page is disabled so the map can zoom.",
results="The live mobile save uses the Transfer backend when the old product list cookie is empty.",
errors="Empty recent locations: “No recent locations.” Success banners: “Check-in completed successfully.” and the check-out and transfer equivalents.",
limits=["Do not document Mobile/Map.aspx. It redirects to unauthorized.", "Do not document Quick Add as the normal scan path."],
examples="Check in from the phone footer after tapping a location.",
screens=[("Phone map", "Narrow window", "Bottom bar", "First tap selects"),
         ("Mobile home", "Open home", "Menu and empty recent locations", "Home clears a process")],
verify=["Transfer in the menu, not the footer.", "Home clears an unfinished check-out."],
do_not=["The 2018 mobile map.", "Legacy Quick Add as the main flow."],
uncertain=["Cookie path on the mobile location selector."])

add(33,
audience="A user searching from the header.",
objective="Open a product or location from suggestions, or send the text to the product list.",
concepts=["Suggestions come from an outside search API, limit 10.", "A product opens the editor. A location opens the location editor.", "Enter stores the text and opens the product list.", "If nothing comes back and Add is allowed, one row offers Create New Product."],
prereqs=["Signed in. The create row is hidden for read-only."],
steps=["Click the header search.", "Click a product or location suggestion.", "Or press Enter to search the product list."],
options="No search operators.",
results="Navigation only, unless you then edit.",
errors="An HTTP error shows no create row.",
limits=["Do not say which fields the suggestion API matches."],
examples="Type a SKU, click the product, land in the editor.",
screens=[("Header", "Type three letters", "Suggestion list", "Product versus location")],
verify=["Read-only does not see Create New Product."],
do_not=["Invented match fields."],
uncertain=["API match fields."])

add(34,
audience="Any signed-in user, including read-only.",
objective="Read recent activity and open one row.",
concepts=["There is no undo.", "Default is all activity, all users, all locations, last 90 days, 15 rows.", "A comment in the code says 365. The product uses 90.", "Show More reloads a longer list from the top and can stay visible when everything is shown."],
prereqs=["Signed in."],
steps=["Open Activity.", "Read a row. Click it for details.", "Click a product or location name in the row to open that editor instead of the details.", "Use the header icon for up to five recent inventory rows, then View Activity History."],
options="Empty text is “No Activity...”. Your own name shows as You when it matches.",
results="A record. Nothing is reversed.",
errors="Missing detail: “Activity not found”.",
limits=["With a user filter, timestamps may not use the account time zone. Mention this only as a limitation.", "The header popup’s other-user suffix is a user index, not a name. Do not describe it as the person’s name."],
examples="Find yesterday’s check-in and open the product from the row.",
screens=[("Activity", "Open history", "Default filters and 15 rows", "90 days, not 365"),
         ("Details", "Click a row", "Quantity and locations", "No undo and no comment edit")],
verify=["Default date range is 90 days."],
do_not=["Undo.", "A 365-day default."],
uncertain=["None for the list."])

add(35,
audience="A user narrowing history.",
objective="Filter by type, date, person, place, and keyword.",
concepts=["Check In and Check Out are not pure type filters. They keep adjusts that moved the matching way, and transfers only when one end is inside the location filter.", "With no location selected, transfers are removed from both.", "Users match the stored first name, not the user id.", "Keyword matches comment, product number, product name, and every custom field."],
prereqs=["Signed in. Read-only people are omitted from the user chips. Their old rows can still appear."],
steps=["Choose a type.", "Choose a date preset or a range.", "Choose a person and a location.", "Type a keyword. There is no AND or OR syntax."],
options="Date presets: All Time, Today, Yesterday, Last 7 Days, Last 30 Days, This Month. All Time starts at 1 Jan 2011. The picker max is today.",
results="A filtered list. Changing filters does not reset the start index.",
errors="A bad date falls back to the last 90 days.",
limits=["Two people with the same first name cannot be separated. A renamed person no longer matches old rows.", "% and _ stay wildcards.", "Location includes descendants."],
examples="Check In, Last 7 Days, one room, keyword gloves.",
screens=[("Activity filters", "Open filters", "Type, date, user, location, keyword", "Check In is not only check-ins")],
verify=["A transfer with no location filter does not appear under Check In."],
do_not=["Check In as “activity type check-in only”."],
uncertain=["None."])

add(36,
audience="A user exporting history.",
objective="Download activity as a CSV and know which columns are empty.",
concepts=["Readable Format is on by default.", "The download ignores the 15-row cap.", "The last four headers, old quantity, new quantity, difference, and cost difference, are never filled.", "Commas in some fields become underscores."],
prereqs=["Signed in, including read-only."],
steps=["Set the filters first.", "Click the CSV download.", "Leave Readable Format checked unless you want the uniform file described in the tooltip."],
options="Tooltip: “If you need to manipulate your data more easily you can uncheck this box for a more uniform file.”",
results="A CSV of the filtered history.",
errors="None specific beyond an empty filter result.",
limits=["Do not tell readers the difference columns contain numbers.", "Hover shows at most 11 product lines. Deleted products show [DELETED]."],
examples="Export last 30 days of check-outs.",
screens=[("Activity", "Download", "Readable Format checked", "Empty trailing columns")],
verify=["Open the CSV and confirm the last four columns are blank."],
do_not=["Filled old and new quantity columns."],
uncertain=["None."])

add(37,
audience="A user downloading current stock.",
objective="Download a product report or a map quantity report.",
concepts=["The product report does not include the current search.", "Every product-report download rewrites location paths in the account before the query. Do not publish that as a feature. Do not claim the download is side-effect free if you are verifying data.", "Map report is hidden until some visible location has quantity above 0.", "Group by Location includes empty locations. Group by Product sums."],
prereqs=["Signed in. The map button also requires a visible quantity. Read-only is not separately blocked on the product export page."],
steps=["On Products, click the download icon. Choose columns. Download.", "On the map, click Download Quantity Report. Choose Group by Location or Group by Product."],
options="Product report defaults: skip zero quantity, skip sub-locations on a specific location, include description, quantity, breakdown, buy, cost, sell, and custom fields. Image off.",
results="A CSV. Cost is quantity times buy price, rounded half away from zero.",
errors="Map export while signed out is unauthorized. Empty map search: “No results to download”.",
limits=["Do not say the product report respects the search chips."],
examples="Download All Locations with cost. Download the map grouped by product.",
screens=[("Export report", "From Products", "The checkboxes", "Search is not applied"),
         ("Map report", "Download Quantity Report", "Two group modes", "Hidden until there is quantity")],
verify=["A searched product list still exports the unsearched location.", "Confirm with engineering before mentioning the location-path rewrite to customers."],
do_not=["The path rewrite as a customer-facing feature."],
uncertain=["None for the columns."])

add(38,
audience="A user reading prices and cost.",
objective="Understand buy, sell, and cost value in the list and the report.",
concepts=["Cost value is quantity times buy price. It is not stored.", "The currency symbol is account-wide free text, default $.", "The subscription card does not use this symbol.", "Buy and sell can be hidden per user."],
prereqs=["Signed in. Prices hidden for records accounts."],
steps=["Set the currency symbol in Settings if you are an admin.", "Show Buy Price and Sell Price. That Settings control appears only while personalized sort is on.", "Read Cost Value in the grid and in the report."],
options="Image URL is an optional report column, off by default.",
results="Display and a calculated column.",
errors="“Please enter a currency symbol”.",
limits=["Do not say cost is a stored field.", "Do not say the currency symbol changes billing."],
examples="Buy 2, quantity 10, cost value 20.",
screens=[("Products", "Cost Value column", "A calculated number", "Not an editable field"),
         ("Settings", "Currency symbol", "The text box", "Account-wide")],
verify=["Hiding buy price hides it in the editor as well."],
do_not=["Currency codes as a dropdown. Any non-empty symbol is accepted."],
uncertain=["None."])

add(39,
audience="A person signing in or changing a password.",
objective="Sign in with email or Google, reset a password, and update a password.",
concepts=["Forgot-password reset has no minimum length. The link host is www.cyberstockroom.com.", "Settings password change requires 6 characters and is hidden for Google-linked users.", "Linking Google does not change the CyberStockroom email."],
prereqs=["Public for login. Signed in for password change and linking."],
steps=["Enter email and password, or click Google.", "Use forgot password, open the email, and set a new password.", "In Settings, click Update Your Password, enter old, new, and repeat.", "If Google is not linked, use the link button."],
options="Login placeholders me@email.com and a masked password.",
results="A session. Password change returns to Settings.",
errors="“The email or password is not correct...” Password change: incorrect, don’t match, too short, or must be different. Quote those sentences.",
limits=["Do not invent a Google error sentence for a normal login. It was not fully traced.", "Invitation acceptance is the team article."],
examples="Reset a forgotten password from the login page.",
screens=[("Login", "Open Login", "Email, password, Google", "Both methods"),
         ("Settings", "Update Your Password", "Old, new, repeat", "Hidden when Google is linked")],
verify=["A Google-linked user does not see the password form."],
do_not=["A 6-character rule on the forgot-password page."],
uncertain=["Ordinary Google login failure text."])

add(40,
audience="A signed-in user updating their own profile.",
objective="Set a name, photo, and email, and read the role badge.",
concepts=["A blank name blocks the app with a required-name popup, except on Settings and printable view.", "Name max is 50 and must be unique on the account.", "Email uniqueness is real, but the same-as-old check compares to the first name, not the current email. Do not document that bug as intended behavior. Do not promise a no-op when re-saving the same email.", "Presets 1 through 15, or an upload under 3 MB."],
prereqs=["Signed in."],
steps=["If asked, enter a name and pick an icon.", "In Settings, change the name and press Enter, or Escape to cancel.", "Change the email the same way.", "Click Apply on a preset or an upload."],
options="Accepted images: png, jpeg, gif, webp. Default preset is 1.",
results="Name, email, or picture saved. The badge is display only.",
errors="“Please enter your name.” “Please use 50 characters or fewer.” “Someone sharing this account is using this name already...” Email title: “That email is invalid or already exists.” Image: “Please choose an image file.” “Please choose an image under 3 MB.”",
limits=["The Mobile badge in markup is never shown. A stored Mobile user appears as User."],
examples="Replace the default avatar and correct a last name.",
screens=[("Required name", "Blank profile", "Name and icons", "The blocking popup"),
         ("Settings profile", "Open profile", "Name, email, badge", "Badge is not editable")],
verify=["Escape on the name field does not save."],
do_not=["The same-as-old email check as a working feature."],
uncertain=["None for name and photo."])

add(41,
audience="An admin managing people. A User can see the form but cannot send the invite.",
objective="Invite someone, accept the invite, change a role, or remove a person.",
concepts=["The unmarked invite role is Admin.", "An email that already belongs to this account does not change role.", "There is no last-admin protection.", "Accepting an invite does not show the role."],
prereqs=["Admin for invite, role change, and delete. Admin and User can see the list. Read-only cannot."],
steps=["Open Profile & Team.", "Search if there are more than 12 people.", "Invite with an email and a role.", "The person opens the link and creates a password.", "Change a role from another person’s card, or DELETE them."],
options="Roles ADMIN, USER, and READ-ONLY. Page size 12.",
results="A new user, a role change, or a deleted user. The invite copies the inviter’s expiration flag and map coordinates without the share marker.",
errors="“Please enter an email address.” “Please enter a valid email address.” “Unable to Invite - Try Again?” “Please create a password to accept your invitation.” Delete confirm names the user.",
limits=["A User sees Invite and gets the unable-to-invite error. Say the action is for admins."],
examples="Invite a read-only auditor. Later change them to User.",
screens=[("Team", "Profile & Team", "Cards and invite", "Default role Admin"),
         ("Accept", "Invitation link", "Create your password", "Role is not on this page")],
verify=["A non-admin invite fails.", "Re-inviting an existing teammate does not change their role."],
do_not=["Last-admin protection.", "Role choice on the accept page."],
uncertain=["None."])

add(42,
audience="An admin deciding who can change data.",
objective="See what Admin, User, and Read-only can do.",
concepts=["Read-only users are sent to the read-only map, product list, and product editor.", "They cannot transfer, import, or create.", "They can read activity and download some files.", "User can see team and invite UI. The invite API is admin-only.", "There is no last-admin guard."],
prereqs=["Signed in as each role if you are capturing screenshots. Use test users."],
steps=["Compare the Map menu, Products toolbar, and Settings sections for each role.", "As read-only, open a product and confirm fields are disabled.", "As admin, change another user’s role."],
options="Effective roles are Admin, User, and Read-only. A legacy Mobile type is treated as User.",
results="Permissions, not a data change, except the role change itself.",
errors="Read-only direct links to Transfer, import, or the default-location picker go to unauthorized or the read-only page.",
limits=["Do not say a read-only user cannot drag the map. That was not proven.", "SUPER_USER sees an empty Settings page. Whether any customer has that role was not checked. Do not document it as a choice."],
examples="A read-only user can look up a quantity and cannot check it out.",
screens=[("Read-only map", "Sign in as read-only", "Hover without the add button", "View, not create"),
         ("Settings", "Each role", "Which sections exist", "User lacks subscription and share")],
verify=["Read-only Products toolbar has no Add.", "User invite returns unable to invite."],
do_not=["A Mobile role in the role dropdown."],
uncertain=["Read-only map drag."])

add(43,
audience="An admin defining fields. Any user can reorder when personalized sort is on.",
objective="Add, rename, delete, preset, and reorder custom fields, and show or hide prices.",
concepts=["Fields are text. There is no date, number, or dropdown type.", "Names and presets are account-wide. Order and price visibility are per user.", "Price cards appear in Settings only while personalized sort is on.", "Create has no duplicate-name check.", "Delete warns that data is erased. The full cascade was not read."],
prereqs=["Admin for create, rename, delete, and presets."],
steps=["Open Custom Fields.", "Turn personalized sort on to show Buy and Sell and the arrows.", "Create a field.", "Rename it.", "Open Presets, enter values, optionally allow other.", "Delete only after exporting, and only if you accept the warning."],
options="Other (Specify). Allow other. Commas in presets become underscores.",
results="A new text field, a renamed label, presets, or a deleted definition.",
errors="“Unable to save the personalized sort preference right now.” “Unable to save the field visibility right now.” Delete confirm includes “Existing data for this field will be erased!”",
limits=["Closing the preset popup does not refresh Settings.", "Do not say duplicate names are blocked.", "Do not say every related row was verified as deleted."],
examples="Add Supplier with three presets and Other.",
screens=[("Custom fields", "Personalized sort off", "No price cards", "Turn sort on first"),
         ("Presets", "Presets on a field", "Values and allow other", "Account-wide")],
verify=["A second field with the same name can be created.", "Buy Price cannot be deleted."],
do_not=["Date or dropdown field types."],
uncertain=["Delete cascade beyond the warning."])

add(44,
audience="Any signed-in user setting how the map and list look. Share is admin-only.",
objective="Set images, zero quantities, expirations, low and high colors, popup fields, and sharing.",
concepts=["These are per user except where the catalog says otherwise.", "A failed toggle reverts after about 1.5 seconds.", "Expiring soon uses 7, 30, and 365 for week, month, and year.", "Zero quantity locations stay white. That sentence belongs to the threshold, not the product-list toggle.", "Kitting is not in this list."],
prereqs=["Signed in. Admin for Share Map Layout."],
steps=["Open Settings, Options.", "Turn product images, zero-quantity products, and expirations on or off.", "Set expiring soon only after expirations are on.", "Set quantity threshold, then max highlight above it.", "Open the map gear for popup details. The field list is per account. Do not invent field names."],
options="Expiring soon default 60 days. Threshold on starts at 1. Max highlight off shows 10.",
results="This user’s display. Sharing is covered in the share-layout article.",
errors="“Enable Expirations before using Expiring Soon.” “Expiring soon window must be a valid duration greater than 0.” “The threshold must be a valid number bigger than 0.” “Max highlight must be greater than the quantity threshold.”",
limits=["Do not publish the hidden kitting checkbox."],
examples="Highlight locations at or below 5 and at or above 100.",
screens=[("Settings Options", "Scroll the toggles", "Images, zero, expirations, threshold", "No kitting switch"),
         ("Popup details", "Map gear", "The account’s field list", "Do not invent names")],
verify=["Month stores 30, not a calendar month.", "Kitting row is not visible."],
do_not=["DSP-008 as a customer switch.", "White-zero sentence on the product toggle."],
uncertain=["None for these toggles."])

add(45,
audience="An admin setting account defaults, and any user setting their own locations.",
objective="Set default check-in and check-out locations, the time zone, and the currency symbol.",
concepts=["Default locations are per user. Clear means none, stored as All Locations.", "Time zone and currency are account-wide and admin-only.", "Time zone offsets are whole hours from -12 through 13. Two labels share +5. There are no half-hour zones.", "Currency is any non-empty symbol, default $."],
prereqs=["Admin or User for locations. Read-only is unauthorized. Admin for time zone and currency."],
steps=["Open Default Check-In Location, pick a place, Save, or CLEAR Selection.", "Repeat for check-out.", "Choose a time zone. It saves on change.", "Type a currency symbol and press Enter."],
options="Fallback time zone -5. Fallback currency $.",
results="Later check-ins and check-outs can start at those locations. Activity timestamps use the time zone. Product headers use the symbol.",
errors="“Error saving timezone. Please try again.” “Please enter a currency symbol”. “Error saving currency symbol. Please try again.”",
limits=["The currency symbol does not change the subscription card.", "Do not offer half-hour zones."],
examples="Default check-in to Receiving. Currency €. Time zone the warehouse’s GMT offset.",
screens=[("Default location", "Click the row", "Save and CLEAR Selection", "Clear shows none"),
         ("Time zone", "The dropdown", "GMT list", "Two labels share +5")],
verify=["After clear, the label shows none.", "A non-admin does not see time zone."],
do_not=["Half-hour time zones.", "Currency as a billing control."],
uncertain=["None."])

add(46,
audience="An admin on a Stripe subscription, and anyone whose trial or payment blocks the app.",
objective="Read the plan, change a Stripe plan or card, cancel, and understand the trial redirect.",
concepts=["Self-serve buttons appear only when the payment method contains Stripe.", "Online Invoice does not get those buttons.", "Do not publish dollar amounts. They are images.", "The enterprise image has no click.", "Unpaid trial is 14 days. After that, other pages redirect to Settings.", "The trial, upgrade, and payment banners stay hidden. Do not tell users to look for them.", "There is no documented plan-capacity limit."],
prereqs=["Admin for cancel and billing history. Update Account blocks read-only only, not non-admin."],
steps=["Open Subscription and read the summary.", "If the buttons are there, use Update Plan, Change Card, or Cancel.", "Cancel asks “Are you sure you want to cancel your subscription?” Choose Cancel Subscription or Keep Subscription.", "Open Billing History for the charges table."],
options="Monthly and annual images. Live price ids may be named only if you need them internally. Do not print prices.",
results="A plan or card change, or a cancel that sets confirmed payment back to 0 and applies the trial rule again.",
errors="“Please contact admin@cyberstockroom.com to change your subscription or payment method”. Billing exception: “No billing history to show...” Empty plan: “No Active Subscription”.",
limits=["PayPal and Stripe-invoice customers do not get the self-serve buttons.", "An invoice table is built and not shown. Do not describe it.", "People sent to Settings are not automatically shown the plan popup."],
examples="Update a card. Read the next payment date. A lapsed trial can open Settings and not the map.",
screens=[("Subscription", "Open Subscription", "Plan and Stripe buttons", "Buttons only for Stripe"),
         ("Billing history", "Billing History", "Charges table", "No invoice table")],
verify=["A non-Stripe method shows the contact sentence.", "Hidden banners are not visible."],
do_not=["Dollar amounts.", "Capacity banner.", "Visible trial banner."],
uncertain=["_cvr success-page sentence. Do not quote it."])

add(47,
audience="A user whose account has expirations turned on.",
objective="See what is expired or expiring, set a date on a product, and know the limits of replace or clone.",
concepts=["The feature is off until Expirations is on in Settings.", "The window defaults to 60 days.", "The list shows the first 100 rows. Counts can be larger.", "Replace or clone has five radios. What they do to stock is Uncertain.", "A past date warns and does not block save."],
prereqs=["SHOW_EXPIRATIONS. Read-only can view the list and cannot manage."],
steps=["Turn Expirations on. Set Expiring Soon if you want a window.", "Open Expirations.", "Click a row to edit that product’s date. Dates run from 2018-01-01 through 2050-01-01.", "On the editable list, click manage, leave Replace and Delete or pick another radio, and save only if you accept that the stock effect is not documented here."],
options="Radios: Replace and Delete, Replace only, Clone and Delete, Clone and Check-out, Clone only. Default is Replace and Delete.",
results="The list and the product date are confirmed. The replacement API’s stock result is not.",
errors="“You must select an expiration date.” “This date has already passed!” “You must select a product number.” “That product number already exists!” Editor API errors may only appear in the browser console.",
limits=["A product expiring later today can be counted differently from how it is listed.", "Do not document each radio’s inventory effect."],
examples="Filter to expired gloves and open the product to set a new date. Stop before replace-or-clone unless the stock effect has been verified live.",
screens=[("Expirations", "Open the list", "Red and yellow rows", "Expired versus soon"),
         ("Manage", "manage", "Five radios", "Do not claim stock results")],
verify=["Read-only has no manage.", "Window 0 hides the yellow state."],
do_not=["Stock results of api/expirationReplacement."],
uncertain=["Replacement stock actions. List API match rules."])

add(48,
audience="An account on the API beta list, and anyone who needs the docs link.",
objective="Create a key, copy it once, and open the API docs.",
concepts=["The manager appears only for beta accounts.", "The plaintext key is shown once.", "The docs link is visible even when you cannot create a key.", "OAuth consent is a different mechanism. Do not mix them. Do not list OAuth scopes."],
prereqs=["Signed in. Beta list for create and delete."],
steps=["Open API & Integrations.", "If you see the request sentence, email support. The docs link still works.", "If you see keys, enter a name and click + Create New API Key.", "Copy the prompt text.", "Delete a key only if you mean to revoke it immediately."],
options="Names longer than 30 characters display with an ellipsis.",
results="A key or a revocation.",
errors="“Please enter a valid key name”. “Error creating API key. Please try again.” Non-beta text tells you to email support@cyberstockroom.com.",
limits=["Do not document a direct CreateNewKey call as a customer path for non-beta accounts."],
examples="Create a key named Warehouse iPad and store it in a password manager.",
screens=[("API keys", "Beta account", "Name and create", "One-time prompt"),
         ("Non-beta", "A normal account", "Request sentence and docs link", "No create button")],
verify=["Reload and confirm the full key is gone."],
do_not=["OAuth scope names.", "Showing the key again later."],
uncertain=["OAuth scope text."])

add(49,
audience="An admin who wants Lansweeper.",
objective="Request the integration. Do not document the unlinked sync screens.",
concepts=["The live Settings text asks you to email support. It contains the typo “conenct”.", "Connect, sync, and disconnect on Settings are commented out.", "A product can still show a Lansweeper link when an asset URL exists."],
prereqs=["Admin for the Settings heading. Users do not see it."],
steps=["Open API & Integrations.", "Read the Lansweeper sentence.", "Email support@cyberstockroom.com.", "On a product, use the Lansweeper link only if it is shown."],
options="None on the live page.",
results="No sync from this screen.",
errors="None on the live page.",
limits=["Do not document site selection, field matching, or a sync progress button."],
examples="Email support to ask for a call. Later, open a product that shows an asset link.",
screens=[("Settings", "Lansweeper heading", "The request sentence", "No connect button"),
         ("Product", "A linked asset", "The Lansweeper link", "Only when a URL exists")],
verify=["Synchronize is not visible."],
do_not=["LSW-002 through LSW-005 as Settings steps."],
uncertain=["Stored field pairing. Duplicate class binding."])

add(50,
audience="A user who cannot find something.",
objective="Check view, search, zero quantities, and empty states before assuming data is missing.",
concepts=["All Locations and one location show different rows.", "Zero-quantity products can be hidden.", "Map search with no API match falls back to titles.", "A location can look empty while its children have stock.", "Read-only users see a different map and product page, not a missing account."],
prereqs=["Signed in."],
steps=["Clear the product search.", "Switch between All Locations and the location you expect.", "Turn on zero-quantity products if the row might be zero.", "On the map, clear Search Map.", "If you are read-only, confirm you are on the read-only pages."],
options="Product images off hides photos, not rows.",
results="The item is visible or the empty-state sentence explains why.",
errors="“No matches found!” “No products yet”. “Location is empty...” “This location is empty but its sub-locations are not”.",
limits=["Do not claim the header search and the product-list search match the same fields."],
examples="A zero-quantity SKU reappears after the display setting is turned on.",
screens=[("Products", "No matches", "The empty search state", "Clear chips"),
         ("Map", "Empty search", "No highlight", "Clear the filter")],
verify=["Zero-quantity toggle with a known zero product."],
do_not=["None."],
uncertain=["Header and map API match fields."])

add(51,
audience="A user whose count looks wrong after a move.",
objective="Tell the Transfer overwrite, the Start subtract, and the one-unit map clear apart.",
concepts=["Transfer check-out sets the source to the remaining quantity.", "Start check-out subtracts and stops at 0.", "A one-unit drag on the map sets that product’s source to 0 even if you thought you moved one of many.", "Check-in on Transfer adds. Check-in on Start also adds.", "Direct quantity edit overwrites the typed number."],
prereqs=["A test quantity you can afford to change, or a written example from the catalog."],
steps=["Identify which screen you used: Transfer, Start, map one-unit, or the quantity cell.", "For Transfer, compare the quantity you left in the selection with the source.", "For a one-unit map drag, expect 0 at the source for that product.", "For a typed quantity, expect the typed number, not an addition."],
options="None.",
results="The reader can name which rule applied.",
errors="“There was a problem updating the quantity in this location...” The on-screen number may already have changed.",
limits=["Do not publish Quick Scan’s resulting quantity. It is Uncertain.", "If the destination product fails to load during a transfer, the destination can be set to the moved amount only."],
examples="Drag the only unit of a SKU and find 0 left behind. Move 1 of 5 on the Transfer page and find 4 left behind.",
screens=[("Transfer partial", "Move 1 of 5", "Source shows 4", "Remaining quantity"),
         ("Map one-unit", "Drag quantity 1", "Source shows 0", "Different rule")],
verify=["Both paths in a test account before publishing the numbers."],
do_not=["One stock formula for every screen.", "Quick Scan math."],
uncertain=["Quick Scan and other external inventory APIs."])

add(52,
audience="A user who cannot edit, import, or move.",
objective="Check role, map lock, trial redirect, and admin-only actions.",
concepts=["Read-only cannot create, import, or transfer.", "The map is locked until it is unlocked.", "An expired unpaid trial or a delinquent Stripe payment sends every page except Settings to Settings.", "Those banners are hidden.", "Invite, custom fields, and API keys are admin or beta gated even if a control is visible."],
prereqs=["The affected user."],
steps=["Confirm the role badge.", "If a location snaps back, unlock the map.", "If every page opens Settings, read the subscription section. Do not look for a hidden banner.", "If import is missing, confirm you are not read-only and the transfer destination is not already chosen."],
options="None.",
results="The reader knows which gate applies.",
errors="“Unable to Invite - Try Again?” Unauthorized pages for read-only. “Could not move location”.",
limits=["Do not say the last admin cannot be removed or demoted.", "Do not say a capacity limit caused the redirect."],
examples="A read-only user cannot see Add. A locked map refuses an overlapping drop.",
screens=[("Locked map", "Try to overlap", "Snap back", "Unlock"),
         ("Settings redirect", "Open Map on an expired trial", "Settings", "No banner required")],
verify=["Expired trial in a test account lands on Settings.", "Banners stay hidden."],
do_not=["Capacity upgrade banner.", "Visible trial banner."],
uncertain=["Whether any live user is SUPER_USER."])

add(53,
audience="A user whose CSV failed or imported only some rows.",
objective="Fix file format, mapping, duplicates, and skipped movement rows.",
concepts=["Create import and movement import are different.", "Create import rejects duplicate numbers in the file and does not update existing products.", "Movement import skips ambiguous matches and missing stock. It does not create products.", "Limits: under 250 KB, 100 columns, UTF-8, commas, header row."],
prereqs=["The file and the mode you used."],
steps=["Read the error title: Success, Import Failed, or No items imported.", "If the file was rejected, fix size, encoding, semicolons, or quotes.", "Map a product number.", "For a movement, open the skipped rows and fix duplicates or quantities."],
options="Movement match can be product number, description, or a custom field.",
results="A corrected file can be imported again. Cancel on the review screen writes nothing.",
errors="Use the exact strings in PED-012 and XFR-005. Do not paraphrase a sentence you cannot see.",
limits=["Do not invent skip reasons that were not quoted.", "Existing products are not updated by a create import. Say that when the user expected an update."],
examples="A semicolon export from another tool is rejected. A name that matches two products is skipped.",
screens=[("Import error", "Upload a bad file", "The error sentence", "Quote it"),
         ("Movement review", "After a partial import", "Skipped rows", "Save has not happened yet")],
verify=["Each quoted error against a fixture file."],
do_not=["Unquoted skip strings."],
uncertain=["Some transfer-import skip strings inside AppendTransferImportRow."])

add(54,
audience="A user who moved a tile and expected the stock to move.",
objective="See that dragging and reparenting change layout only.",
concepts=["Drag moves the tile in this user’s layout.", "Reparent changes the parent id. Nested locations stay with it. Quantities stay on the same location ids.", "Copying stock is Ctrl+drop, a different gesture.", "Deleting a location does check stock out. That is not a move."],
prereqs=["A location with stock."],
steps=["Note the quantity.", "Unlock if needed and drag the tile.", "Confirm the quantity is unchanged.", "Reparent it and confirm again.", "If you needed the stock in the other place, use transfer or Ctrl+drop instead."],
options="None.",
results="Layout changes. Inventory does not.",
errors="“Could not move location” on a failed reparent.",
limits=["Ctrl+drop clears the destination first. Do not recommend it as a simple move."],
examples="Slide a shelf two squares right. The same products remain in that shelf.",
screens=[("Map", "Before and after a drag", "Same quantity label", "Layout only")],
verify=["Quantity before and after a drag."],
do_not=["Drag as a transfer."],
uncertain=["None."])

add(55,
audience="A user with duplicate numbers, a missing rename, or a deleted product.",
objective="Work within product-number rules.",
concepts=["Product numbers cannot be renamed.", "AUTO numbers are CSN- plus nine digits.", "Create skips existing numbers. It does not update them.", "Duplicate numbers in one import file are rejected.", "Clone can keep Auto on to avoid a clash.", "Delete is the catalog delete, not a one-location quantity delete.", "The old dialogs are not the live path."],
prereqs=["Signed in, not read-only, for changes."],
steps=["To change an identity, clone to a new number and delete the old one if you mean to retire it.", "To fix an import, remove duplicate numbers from the file.", "After delete, do not expect the old editor to keep working. A missing product shows Product Error."],
options="Clone Auto on by default.",
results="A new number, or the old product removed.",
errors="“Product number already exists”. “That product number already exists!” “No Poduct Number!” when a manual number is blank.",
limits=["Do not promise that delete only removes one location’s quantity.", "Do not describe what productDeleter removes beyond the warning and the expiration call."],
examples="Clone SKU-1 to SKU-2, then delete SKU-1.",
screens=[("Editor", "Product number", "A label, not a box", "Cannot rename"),
         ("Clone", "Auto on", "New number", "No stock copied")],
verify=["Existing number in a create import is skipped and its name stays."],
do_not=["The unwired delete dialog.", "The old clone popup."],
uncertain=["productDeleter cascade."])

assert set(BODY) == set(range(1, 56))

CAT_URL = {
"Getting Started": "https://cyberstockroom.helpscoutdocs.com/category/153-getting-started",
"Map & Locations": "https://cyberstockroom.helpscoutdocs.com/category/161-map-locations",
"Products & Inventory": "https://cyberstockroom.helpscoutdocs.com/category/172-products-inventory",
"Inventory Operations": "https://cyberstockroom.helpscoutdocs.com/category/182-inventory-operations",
"Search, Activity & Reports": "https://cyberstockroom.helpscoutdocs.com/category/190-search-activity-reports",
"Team & Account Settings": "https://cyberstockroom.helpscoutdocs.com/category/197-team-account-settings",
"Advanced Features & Integrations": "https://cyberstockroom.helpscoutdocs.com/category/206-advanced-features-integrations",
"Troubleshooting & FAQs": "https://cyberstockroom.helpscoutdocs.com/category/210-troubleshooting-faqs",
}
CAT_DESC = {
"Getting Started": "Retrieved from the live category page: Learn how CyberStockroom works, set up your first locations and products, and begin tracking inventory.",
"Products & Inventory": "Retrieved from the live category page: Create and maintain the product catalog, manage product information, import products, and work with inventory quantities.",
"Inventory Operations": "Retrieved from the live category page: Perform everyday inventory activities, including receiving, issuing, transferring, scanning, and importing inventory movements.",
}

def ids(n, key):
    if key == "primary":
        return PRIMARY[n]
    return SUPPORTING[n]

def feat_line(fid):
    return f"{fid} {names[fid]}"

for n in list(SUPPORTING):
    SUPPORTING[n] = [fid for fid in SUPPORTING[n] if fid not in PRIMARY.get(n, [])]

# feature -> articles
primary_of = {fid: [] for fid in names}
support_of = {fid: [] for fid in names}
for n in range(1, 56):
    for fid in PRIMARY[n]:
        primary_of[fid].append(kb(n))
    for fid in SUPPORTING[n]:
        if fid in names and kb(n) not in primary_of[fid]:
            support_of[fid].append(kb(n))

for fid in list(support_of):
    support_of[fid] = [x for x in support_of[fid] if x not in primary_of[fid]]

def disposition(fid):
    if fid in INTERNAL:
        return "INTERNAL ONLY"
    if fid in GAPS and fid in NEEDS:
        return "COVERAGE GAP"
    if fid in GAPS:
        return "COVERAGE GAP"
    if fid in NEEDS and not primary_of[fid]:
        return "NEEDS INVESTIGATION"
    if primary_of[fid]:
        return "PRIMARY"
    if support_of[fid]:
        return "SUPPORTING"
    return "UNMAPPED"

missing_names = [fid for n in range(1, 56) for fid in PRIMARY[n] + SUPPORTING[n] if fid not in names]
if missing_names:
    raise SystemExit("unknown ids " + ",".join(missing_names))

unmapped = [fid for fid in names if disposition(fid) == "UNMAPPED"]
if unmapped:
    raise SystemExit("unmapped " + ",".join(unmapped))

def render_article(n):
    cat, title, url = KB[n]
    b = BODY[n]
    rel = [kb(i) for i, nums in WF.items() if False]
    wf = [w for w, nums in WF.items() if n in nums]
    lines = []
    lines.append(f"# {kb(n)} — {title}")
    lines.append("")
    lines.append("Handoff for the documentation agent. This is not the customer article.")
    lines.append("")
    lines.append("## Article identity")
    lines.append("")
    lines.append(f"- Permanent KB ID: {kb(n)}")
    lines.append(f"- Exact Help Scout title: {title}")
    lines.append(f"- Category: {cat}")
    lines.append(f"- Category URL: {CAT_URL[cat]}")
    lines.append(f"- Existing article URL: {url}")
    lines.append("- Existing article summary: not retrieved. The live article body was not read. Read it before editing so unique customer wording is not destroyed.")
    lines.append(f"- Intended audience: {b['audience']}")
    lines.append(f"- Customer objective: {b['objective']}")
    lines.append("")
    lines.append("## Feature references")
    lines.append("")
    lines.append("Primary feature IDs:")
    for fid in PRIMARY[n]:
        lines.append(f"- {feat_line(fid)}")
    lines.append("")
    lines.append("Supporting feature IDs:")
    sup = [fid for fid in SUPPORTING[n] if fid in names]
    if sup:
        for fid in sup:
            lines.append(f"- {feat_line(fid)}")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("Related workflows: " + (", ".join(wf) if wf else "None"))
    lines.append("")
    lines.append("Source-code references, for the agent, not for the article: " + CODE[n])
    lines.append("")
    lines.append("Walkthrough source: `QA_FeatureCatalog/FEATURE_CATALOG.md` for each ID above. Do not invent a step that is not in that entry.")
    lines.append("")
    lines.append("## Content requirements")
    lines.append("")
    lines.append("Concepts:")
    for x in b["concepts"]:
        lines.append(f"- {x}")
    lines.append("")
    lines.append("Prerequisites and permissions:")
    for x in b["prereqs"]:
        lines.append(f"- {x}")
    lines.append("")
    lines.append("Customer actions:")
    for i, x in enumerate(b["steps"], 1):
        lines.append(f"{i}. {x}")
    lines.append("")
    lines.append("Options and settings: " + b["options"])
    lines.append("")
    lines.append("Expected results: " + b["results"])
    lines.append("")
    lines.append("Errors and troubleshooting: " + b["errors"])
    lines.append("")
    lines.append("Limitations:")
    for x in b["limits"]:
        lines.append(f"- {x}")
    lines.append("")
    lines.append("Example: " + b["examples"])
    lines.append("")
    lines.append("Related articles:")
    related = []
    for fid in PRIMARY[n] + sup:
        for other in primary_of.get(fid, []):
            if other != kb(n) and other not in related:
                related.append(other)
    if related:
        for other in related:
            num = int(other[3:])
            lines.append(f"- {other} {KB[num][1]}")
    else:
        lines.append("- None beyond the workflows above.")
    lines.append("")
    lines.append("## Visual walkthrough")
    lines.append("")
    lines.append("Capture these from the running app. Do not draw stand-in screenshots.")
    lines.append("")
    for i, (screen, action, state, shows) in enumerate(b["screens"], 1):
        lines.append(f"### Stage {i}")
        lines.append(f"- Screen: {screen}")
        lines.append(f"- Action: {action}")
        lines.append(f"- UI state to capture: {state}")
        lines.append(f"- What it must demonstrate: {shows}")
        lines.append("- Sample data: a test account. Do not use a customer account. Use read-only and admin users only where this article compares roles.")
        lines.append("")
    lines.append("## Validation requirements")
    lines.append("")
    lines.append("Feature IDs that must be covered:")
    for fid in PRIMARY[n]:
        lines.append(f"- {fid}")
    lines.append("")
    lines.append("Live verification:")
    for x in b["verify"]:
        lines.append(f"- {x}")
    lines.append("")
    lines.append("Do not publish:")
    for x in b["do_not"]:
        lines.append(f"- {x}")
    lines.append("")
    lines.append("Uncertainties:")
    for x in b["uncertain"]:
        lines.append(f"- {x}")
    for fid in PRIMARY[n] + sup:
        if fid in NEEDS:
            lines.append(f"- {fid}: {NEEDS[fid]}")
        if fid in INTERNAL:
            lines.append(f"- {fid}: {INTERNAL[fid]}")
    lines.append("")
    return "\n".join(lines)

for n in range(1, 56):
    (ART / f"{kb(n)}.md").write_text(render_article(n), encoding="utf-8")

# KB_ARTICLE_MAP
map_lines = ["# Knowledge base article map", "",
"Article titles, categories, and URLs come from `CyberStockroom_KB_Article_URLs.csv` and were checked against the live sitemap at https://cyberstockroom.helpscoutdocs.com/sitemap.xml on 6 Nov 2026. Every article URL in that CSV was present in the sitemap.",
"",
"Article body text was not retrieved. Existing summaries are therefore not recorded. Category descriptions were retrieved only for Getting Started, Products & Inventory, and Inventory Operations.",
"",
"Coverage status is Ready for the documentation agent. It is not a claim that the live article already covers the features.",
""]
order = []
for cat in ["Getting Started", "Map & Locations", "Products & Inventory", "Inventory Operations", "Search, Activity & Reports", "Team & Account Settings", "Advanced Features & Integrations", "Troubleshooting & FAQs"]:
    map_lines.append(f"## {cat}")
    map_lines.append("")
    map_lines.append(f"Category URL: {CAT_URL[cat]}")
    map_lines.append("")
    map_lines.append(CAT_DESC.get(cat, "Category description: not retrieved. The category page was not read. The name and URL are from the article list and the sitemap."))
    map_lines.append("")
    map_lines.append("| KB ID | Title | URL | Primary features | Supporting features |")
    map_lines.append("| --- | --- | --- | --- | --- |")
    for n, (c, title, url) in enumerate(ARTICLES, 1):
        if c != cat:
            continue
        p = ", ".join(PRIMARY[n])
        s = ", ".join(fid for fid in SUPPORTING[n] if fid in names) or "None"
        map_lines.append(f"| {kb(n)} | {title} | {url} | {p} | {s} |")
    map_lines.append("")
(ROOT / "KB_ARTICLE_MAP.md").write_text("\n".join(map_lines), encoding="utf-8")

# coverage
cov = ["# Feature coverage", "",
"Every ID in `QA_FeatureCatalog/SUMMARY.md` is listed once. PRIMARY means an existing article should substantially document it. SUPPORTING means an article should mention it. INTERNAL ONLY must not be written as a working customer feature. COVERAGE GAP means no current article is a fit. NEEDS INVESTIGATION means a customer article would have to omit or flag an untraced behavior.",
"",
"| Feature ID | Name | Disposition | Primary articles | Supporting articles | Publication restrictions | Unresolved questions |",
"| --- | --- | --- | --- | --- | --- | --- |"]
for fid in names:
    disp = disposition(fid)
    if fid in GAPS and fid in NEEDS:
        disp = "COVERAGE GAP"
    restr = INTERNAL.get(fid, "None")
    if fid in NEEDS and fid not in INTERNAL:
        question = NEEDS[fid]
    else:
        question = "None" if fid not in NEEDS else NEEDS[fid]
    if fid in GAPS and "no help article" not in question:
        question = (question + " " if question != "None" else "") + "No existing article."
    cov.append("| {fid} | {name} | {disp} | {p} | {s} | {r} | {q} |".format(
        fid=fid,
        name=names[fid].replace("|", "/"),
        disp=disp,
        p=", ".join(primary_of[fid]) or "None",
        s=", ".join(support_of[fid]) or "None",
        r=restr.replace("|", "/"),
        q=question.replace("|", "/"),
    ))
(ROOT / "KB_FEATURE_COVERAGE.md").write_text("\n".join(cov) + "\n", encoding="utf-8")

# audit
from collections import Counter
c = Counter(disposition(fid) if not (fid in GAPS) else "COVERAGE GAP" for fid in names)
# fix disposition function for gaps that also have needs: KIT and RPT
# recompute consistently
counts = Counter()
for fid in names:
    d = "COVERAGE GAP" if fid in GAPS else disposition(fid)
    counts[d] += 1

audit = f"""# Knowledge base mapping audit

## What was retrieved

- Live sitemap: https://cyberstockroom.helpscoutdocs.com/sitemap.xml on 6 Nov 2026.
- Article titles, categories, and URLs: `CyberStockroom_KB_Article_URLs.csv`. All 55 URLs were also in the sitemap.
- Category descriptions retrieved from the live category pages: Getting Started, Products & Inventory, Inventory Operations.
- Category descriptions not retrieved: Map & Locations, Search, Activity & Reports, Team & Account Settings, Advanced Features & Integrations, Troubleshooting & FAQs. Names and URLs for those categories are from the sitemap and the CSV. Their descriptions were not invented.
- Individual article bodies and summaries: not retrieved. Every article file says so.

## Counts

- Categories: 8
- Articles: 55
- Feature IDs examined: {len(names)}
- Primary coverage: {counts['PRIMARY']}
- Supporting coverage only: {counts['SUPPORTING']}
- Internal only: {counts['INTERNAL ONLY']}
- Coverage gaps: {counts['COVERAGE GAP']}
- Needs investigation as the disposition: {counts['NEEDS INVESTIGATION']}
- Unmapped: {counts['UNMAPPED'] if 'UNMAPPED' in counts else 0}

## Internal-only features

{chr(10).join('- ' + fid + ' — ' + INTERNAL[fid] for fid in INTERNAL)}

## Coverage gaps

- KIT-001 and KIT-002. Kitting has no article. Workflow WF-012 has no article either. The Settings switch that might have been expected is hidden and unwired. The component editor has confirmed defects. Do not write a tutorial that says quantity edit and remove work.
- RPT-002. The AI insights page has no menu link and its generator was not in the website files that were read.

## Needs investigation inside articles that do exist

- ACC-015 OAuth scope text, on the API article only as a do-not-write.
- EXP-002 stock effect of each replace or clone radio.
- XFR-011 and the kiosk article: Quick Scan stock math.
- MAP-013 whether a structure clone copies quantities.
- SRCH-001 and MAP-018 match fields.
- productDeleter cascade on delete articles.
- Read-only map drag.
- Some transfer-import skip sentences.

## Suggested new articles

Do not create these in Help Scout until the behavior is safe to document.

1. Kits. Cover KIT-001 only, and say KIT-002 quantity edit and same-quantity delete are not reliable. Do not mention KIT-003 or the Settings kitting checkbox.
2. AI inventory insights. Cover RPT-002 only after the page is linked from the product and the generator can be described. Until then, leave it out.

## Structure notes

- Getting Started overlaps the dedicated map, product, import, and check-in articles. Keep the first-15-minutes article short and link out.
- Understanding Inventory Actions overlaps the three how-to articles. Use it for the Start page and for the difference between Start and Transfer.
- Searching and Finding Products and Finding Products and Locations with Search are different searches. Do not merge them.
- Understanding Products and Quantities, Changing Inventory Quantities Directly, and Understanding Inventory Values overlap. Keep quantities, direct edits, and cost columns in those three articles.
- No article should absorb kitting, the AI report, or the unlinked Lansweeper sync screens.

## Ready for the documentation agent

Yes, for the 55 existing articles, with the publication restrictions in each handoff file. Not ready to document kits, the AI report, OAuth scopes, or external API stock math as confirmed behavior.

No website code and no Help Scout article was edited.
"""
(ROOT / "KB_MAPPING_AUDIT.md").write_text(audit, encoding="utf-8")
print("articles", len(list(ART.glob('KB-*.md'))))
print("features", len(names))
print(dict(counts))
