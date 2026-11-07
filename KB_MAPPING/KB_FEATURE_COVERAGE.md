# Feature coverage

Every ID in `QA_FeatureCatalog/SUMMARY.md` is listed once. PRIMARY means an existing article should substantially document it. SUPPORTING means an article should mention it. INTERNAL ONLY must not be written as a working customer feature. COVERAGE GAP means no current article is a fit. NEEDS INVESTIGATION means a customer article would have to omit or flag an untraced behavior.

| Feature ID | Name | Disposition | Primary articles | Supporting articles | Publication restrictions | Unresolved questions |
| --- | --- | --- | --- | --- | --- | --- |
| SET-001 | Settings sections | SUPPORTING | None | KB-001, KB-020, KB-046 | None | None |
| SET-002 | Text fields save on change | SUPPORTING | None | KB-039, KB-040, KB-043, KB-045 | None | None |
| SET-003 | One settings write at a time | SUPPORTING | None | KB-041, KB-043, KB-048 | None | None |
| ACC-001 | Log in with email | PRIMARY | KB-039 | None | None | None |
| ACC-002 | Log in with Google | PRIMARY | KB-039 | None | None | None |
| ACC-003 | Forgot password | PRIMARY | KB-039 | None | None | None |
| ACC-004 | Accept an invitation | PRIMARY | KB-041 | KB-039 | None | None |
| ACC-005 | Choose a plan during signup | PRIMARY | KB-046 | None | None | None |
| ACC-006 | Welcome page | INTERNAL ONLY | None | None | Welcome.aspx redirects to the map before any wizard runs. Do not publish a welcome wizard. | None |
| ACC-007 | Required name | PRIMARY | KB-040 | None | None | None |
| ACC-008 | Profile picture | PRIMARY | KB-040 | None | None | None |
| ACC-009 | Your name | PRIMARY | KB-040 | None | None | None |
| ACC-010 | Your email | PRIMARY | KB-040 | None | None | None |
| ACC-011 | Update your password | PRIMARY | KB-039 | KB-040 | None | None |
| ACC-012 | Link Google | PRIMARY | KB-039 | KB-040 | None | None |
| ACC-013 | Role badge | PRIMARY | KB-040, KB-042 | KB-041 | None | None |
| ACC-014 | Subscription update confirmation | PRIMARY | KB-046 | None | None | None |
| ACC-015 | Allow or deny an OAuth connection | NEEDS INVESTIGATION | None | KB-048 | None | OAuth Allow and Cancel are real, but scope labels are outside this website repo. Do not list scope names. |
| TEAM-001 | Team list | PRIMARY | KB-041 | KB-042 | None | None |
| TEAM-002 | Change a teammate’s role | PRIMARY | KB-041, KB-042 | KB-052 | None | None |
| TEAM-003 | Remove a teammate | PRIMARY | KB-041 | None | None | None |
| TEAM-004 | Invite a teammate | PRIMARY | KB-041 | KB-014, KB-042 | None | None |
| CFL-001 | Personalized sort | PRIMARY | KB-043 | None | None | None |
| CFL-002 | Show or hide Buy Price and Sell Price | PRIMARY | KB-043 | KB-018, KB-038, KB-044 | None | None |
| CFL-003 | Add a custom field | PRIMARY | KB-043 | KB-052, KB-055 | None | None |
| CFL-004 | Rename a custom field | PRIMARY | KB-043 | None | None | None |
| CFL-005 | Delete a custom field | PRIMARY | KB-043 | None | None | None |
| CFL-006 | Preset choices | PRIMARY | KB-018, KB-043 | KB-022 | None | None |
| DEF-001 | Default check-in location | PRIMARY | KB-045 | KB-005, KB-026 | None | None |
| DEF-002 | Default check-out location | PRIMARY | KB-045 | KB-027 | None | None |
| API-001 | Create and delete an API key | PRIMARY | KB-048 | None | None | None |
| API-002 | API documentation link | PRIMARY | KB-048 | None | None | None |
| LSW-001 | Request the integration | PRIMARY | KB-049 | None | None | None |
| LSW-002 | Choose sites | INTERNAL ONLY | None | KB-049 | Site picker exists but is not linked from current Settings. | None |
| LSW-003 | Match a Lansweeper field | INTERNAL ONLY | None | KB-049 | Field-match popup is not linked from current Settings. Stored pairing was not fully traced. | None |
| LSW-004 | Match a category to a location | INTERNAL ONLY | None | KB-049 | Category-to-location match is not linked from current Settings. | None |
| LSW-005 | Link, sync, and progress | INTERNAL ONLY | None | KB-049 | Link, sync, and progress popups are not linked from current Settings. Duplicate class binding is unverified. | None |
| DSP-001 | Share Map Layout | PRIMARY | KB-014, KB-044 | None | None | None |
| DSP-002 | Product Images | PRIMARY | KB-024, KB-044 | KB-020, KB-050 | None | None |
| DSP-003 | Zero Quantity Products | PRIMARY | KB-044, KB-050 | KB-017, KB-020 | None | None |
| DSP-004 | Expirations | PRIMARY | KB-044, KB-047 | None | None | None |
| DSP-005 | Expiring Soon | PRIMARY | KB-044, KB-047 | None | None | None |
| DSP-006 | Quantity Threshold | PRIMARY | KB-044 | KB-015 | None | None |
| DSP-007 | Max Highlight | PRIMARY | KB-044 | KB-015 | None | None |
| DSP-008 | Kitting toggle | INTERNAL ONLY | None | None | The Settings kitting checkbox is hidden and unwired. Do not publish it as the way to turn kitting on. | None |
| ACCSET-001 | Time zone | PRIMARY | KB-045 | KB-034 | None | None |
| ACCSET-002 | Currency symbol | PRIMARY | KB-038, KB-045 | None | None | None |
| SUB-001 | Subscription summary | PRIMARY | KB-046 | None | None | None |
| SUB-002 | Change a Stripe subscription | PRIMARY | KB-046 | None | None | None |
| SUB-003 | Billing history | PRIMARY | KB-046 | None | None | None |
| SUB-004 | Trial end and failed payment | PRIMARY | KB-046, KB-052 | None | None | None |
| MAP-001 | Open the inventory map | PRIMARY | KB-001, KB-007 | KB-002, KB-003, KB-011 | None | None |
| MAP-002 | Read-only map | PRIMARY | KB-042, KB-052 | KB-050 | None | None |
| MAP-003 | Location types | PRIMARY | KB-003, KB-008 | None | None | None |
| MAP-004 | Quantity labels on tiles | PRIMARY | KB-007 | KB-010, KB-012, KB-017, KB-027, KB-050 | None | None |
| MAP-005 | Create a location | PRIMARY | KB-003, KB-008 | KB-002, KB-013 | None | None |
| MAP-006 | Rename a location | PRIMARY | KB-008 | KB-016 | None | None |
| MAP-007 | Location editor | PRIMARY | KB-016 | KB-008 | None | None |
| MAP-008 | Move primary locations | PRIMARY | KB-009, KB-054 | KB-052 | None | None |
| MAP-009 | Map lock | PRIMARY | KB-009, KB-052 | KB-003, KB-007 | None | None |
| MAP-010 | Move under a different parent | PRIMARY | KB-009, KB-054 | None | None | None |
| MAP-011 | Tile size follows children | PRIMARY | KB-009 | KB-012, KB-054 | None | None |
| MAP-012 | Delete a location | PRIMARY | KB-008 | None | None | None |
| MAP-013 | Clone a location’s structure | PRIMARY | KB-013 | None | None | Location clone posts api/LocationClone. Whether quantities copy was not in this repo. |
| MAP-014 | Copy stock with Ctrl+drop | PRIMARY | KB-013 | KB-054 | None | None |
| MAP-015 | ABC sort | PRIMARY | KB-011 | KB-009, KB-044 | None | None |
| MAP-016 | Use a shared map layout | PRIMARY | KB-014 | KB-044 | None | None |
| MAP-017 | Zoom | PRIMARY | KB-011 | KB-032 | None | None |
| MAP-018 | Search the map | PRIMARY | KB-015, KB-033, KB-050 | None | None | Map search calls api/map. Which fields match is outside this repo. Local title fallback is confirmed. |
| MAP-019 | Low and high quantity colors | PRIMARY | KB-015, KB-044 | None | None | None |
| MAP-020 | Check in from the map | PRIMARY | KB-026 | KB-005, KB-010 | None | None |
| MAP-021 | Check out from the map | PRIMARY | KB-027 | None | None | None |
| MAP-022 | Drag stock between locations | PRIMARY | KB-028 | None | None | None |
| MAP-023 | Move one unit and comment | PRIMARY | KB-028, KB-051 | None | None | None |
| MAP-024 | See products inside a location | PRIMARY | KB-010 | None | None | None |
| MAP-025 | Popup details | PRIMARY | KB-044 | KB-015, KB-047 | None | None |
| MAP-026 | Change quantity on the product map | PRIMARY | KB-023 | KB-051 | None | None |
| MAP-027 | Open the product list for a location | PRIMARY | KB-010 | None | None | None |
| MAP-028 | Vertical stack | PRIMARY | KB-012 | None | None | None |
| MAP-029 | 3D stack | PRIMARY | KB-012 | None | None | None |
| MAP-030 | Move several locations | PRIMARY | KB-009 | None | None | None |
| MAP-031 | Minimap | PRIMARY | KB-011 | None | None | None |
| MAP-032 | Download a quantity report | PRIMARY | KB-037 | None | None | None |
| MAP-033 | Tablet mode | PRIMARY | KB-032 | None | None | None |
| MAP-034 | Map keyboard shortcuts | PRIMARY | KB-011 | None | None | None |
| MAP-035 | Pan and scroll to origin | PRIMARY | KB-011 | None | None | None |
| MAP-036 | Empty-map coaching | PRIMARY | KB-002, KB-003 | None | None | None |
| MAP-037 | Highlight a new location | PRIMARY | KB-008 | None | None | None |
| MAP-038 | View barcode and attachments (read-only) | PRIMARY | KB-016 | None | None | None |
| MAP-039 | Attach a file to a location | PRIMARY | KB-016 | KB-024 | None | None |
| MAP-040 | Location barcode | PRIMARY | KB-016, KB-024 | None | None | None |
| MAP-041 | Location kiosk | PRIMARY | KB-030 | KB-016, KB-029 | None | None |
| MAP-042 | Location breadcrumb | PRIMARY | KB-011 | KB-016, KB-028, KB-035 | None | None |
| MAP-043 | Create a top-level location from mobile | PRIMARY | KB-032 | KB-008 | None | None |
| MAP-044 | Map on a phone | PRIMARY | KB-032 | KB-007, KB-011 | None | None |
| XFR-001 | Check in | PRIMARY | KB-001, KB-026, KB-051 | KB-005, KB-006, KB-032, KB-042 | None | None |
| XFR-002 | Check out | PRIMARY | KB-001, KB-027, KB-051 | KB-006, KB-032 | None | None |
| XFR-003 | Transfer between two locations | PRIMARY | KB-001, KB-028 | KB-006, KB-032, KB-051 | None | None |
| XFR-004 | Quantity adjust is not a Transfer mode | PRIMARY | KB-023 | KB-006, KB-028 | None | None |
| XFR-005 | Import a file into a movement | PRIMARY | KB-031, KB-053 | None | None | None |
| XFR-006 | Start page | PRIMARY | KB-006, KB-051 | KB-026, KB-027, KB-028, KB-031, KB-053 | None | None |
| XFR-007 | Check in products just created | PRIMARY | KB-005 | KB-002, KB-004, KB-019, KB-026, KB-045 | None | None |
| XFR-008 | Mobile check-in, check-out, and transfer | PRIMARY | KB-032 | KB-026, KB-027, KB-028 | None | None |
| XFR-009 | Mobile location picker | PRIMARY | KB-032 | KB-028, KB-045 | None | None |
| XFR-010 | Legacy mobile product list and Quick Add | INTERNAL ONLY | None | KB-032 | Legacy mobile product list and Quick Add are not the live auto path. Quick Add creates a catalog row and does not check it in. | None |
| XFR-011 | Quick Scan | PRIMARY | KB-029, KB-030 | None | None | Quick Scan posts api/inventory. The stock math of that API was not in this repo. |
| XFR-012 | Mobile home | PRIMARY | KB-032 | KB-030 | None | None |
| PRD-001 | Product list | PRIMARY | KB-001, KB-017, KB-020 | KB-010, KB-042, KB-050 | None | None |
| PRD-002 | Empty list | PRIMARY | KB-020, KB-050 | KB-004 | None | None |
| PRD-003 | Columns | PRIMARY | KB-020, KB-038 | KB-043 | None | None |
| PRD-004 | Sort | PRIMARY | KB-020 | None | None | None |
| PRD-005 | Pages and select all | PRIMARY | KB-020 | KB-022, KB-025 | None | None |
| PRD-006 | Search the product list | PRIMARY | KB-021, KB-033, KB-050 | KB-020, KB-037 | None | None |
| PRD-007 | Open a product | PRIMARY | KB-020 | KB-018, KB-033 | None | None |
| PRD-008 | Web addresses in the grid | PRIMARY | KB-020 | None | None | None |
| PRD-009 | Photos in the list | PRIMARY | KB-020 | KB-024 | None | None |
| PRD-010 | Change quantity in the list | PRIMARY | KB-023 | KB-017, KB-051 | None | None |
| PRD-011 | Toolbar actions | PRIMARY | KB-020, KB-022, KB-025, KB-055 | KB-018, KB-024, KB-037 | None | None |
| PED-001 | Edit name, price, and custom fields | PRIMARY | KB-018, KB-055 | KB-022, KB-043, KB-047 | None | None |
| PED-002 | Product photo | PRIMARY | KB-024 | KB-049 | None | None |
| PED-003 | Product attachments | PRIMARY | KB-024 | None | None | None |
| PED-004 | Lansweeper link on a product | PRIMARY | KB-049 | None | None | None |
| PED-005 | Expiration on the product | PRIMARY | KB-047 | None | None | None |
| PED-006 | Product editor map | PRIMARY | KB-023 | None | None | None |
| PED-007 | Clone a product | PRIMARY | KB-025, KB-055 | None | None | None |
| PED-008 | Delete one product | PRIMARY | KB-025, KB-055 | None | None | None |
| PED-009 | Read-only product editor | PRIMARY | KB-042, KB-052 | KB-018 | None | None |
| PED-010 | Create products by typing | PRIMARY | KB-004, KB-018, KB-055 | KB-002, KB-005, KB-019 | None | None |
| PED-011 | Photo while creating | PRIMARY | KB-004, KB-018 | None | None | None |
| PED-012 | Import a CSV (shared rules) | PRIMARY | KB-019, KB-053 | KB-004, KB-031, KB-052 | None | None |
| PED-013 | Import to create products | PRIMARY | KB-004, KB-019, KB-053 | None | None | None |
| PED-014 | Import a list into a movement | PRIMARY | KB-031 | KB-053 | None | None |
| PED-015 | Print barcode labels | PRIMARY | KB-024 | None | None | None |
| PED-016 | Product selector | PRIMARY | KB-006 | KB-026 | None | None |
| PED-017 | Document editor is not attachments | INTERNAL ONLY | None | None | Document Editor buttons are literal text with no handlers. Not product attachments. | None |
| PED-018 | Unwired product screens | INTERNAL ONLY | None | KB-055 | Old clone popup, quantity-only delete dialog, SuccessProducts, and batches are not on the live click path. | None |
| ACT-001 | Activity history | PRIMARY | KB-034 | KB-001, KB-035, KB-036, KB-045 | None | None |
| ACT-002 | Filter by type | PRIMARY | KB-035 | KB-036 | None | None |
| ACT-003 | Date, user, location, and keyword | PRIMARY | KB-035 | None | None | None |
| ACT-004 | Activity row hover and CSV | PRIMARY | KB-036 | KB-034 | None | None |
| ACT-005 | One activity | PRIMARY | KB-034 | None | None | None |
| ACT-006 | Header activity popup | PRIMARY | KB-034 | None | None | None |
| ACT-007 | What is stored | PRIMARY | KB-034 | None | None | None |
| EXP-001 | Expiration list | PRIMARY | KB-047 | KB-044 | None | None |
| EXP-002 | Replace or clone an expiring product | PRIMARY | KB-047 | None | None | The replace-or-clone wizard is real. What each radio does to stock is an API outside this repo. |
| KIT-001 | Kit list, create, delete, search | COVERAGE GAP | None | None | None | Kit create posts api/kit. Insert rules are outside this repo, and there is no help article. |
| KIT-002 | Kit components | COVERAGE GAP | None | None | None | Kit component edit has confirmed page defects. Persistence is outside this repo, and there is no help article. |
| KIT-003 | Kit “manage” is not a kit action | INTERNAL ONLY | None | None | The kit Manage button builds invalid JavaScript and is a copy of the expiration wizard. Do not publish it. | None |
| SRCH-001 | Header search | PRIMARY | KB-033 | KB-021 | None | Header search calls developers.cyberstockroom.com. Which fields match is outside this repo. |
| RPT-001 | Download a product report | PRIMARY | KB-037, KB-038 | None | None | None |
| RPT-002 | AI insights report | COVERAGE GAP | None | None | None | AI insights page exists at /ai-report.aspx?id= and has no menu link. Report generation is outside the files that were read. No existing article. |
