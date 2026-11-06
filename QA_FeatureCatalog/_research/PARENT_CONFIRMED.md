# Confirmed while building the page inventory

These notes are already reflected in PAGE_INVENTORY.md where they describe pages. Extra behavior that belongs in the feature catalog:

## Activity descriptions

`Activity.GetActivityDescription` (`App_Code/Classes/Business Objects/Activity.vb` around line 116).

Account type 0 (standard):

| Code name | User-facing phrase |
| --- | --- |
| PRODUCT__CREATE | created new products |
| PRODUCT__DELETE | deleted products |
| PRODUCT__EDIT | edited products |
| INVENTORY__CHECK_IN | checked in products |
| INVENTORY__CHECK_OUT | checked out products |
| INVENTORY__TRANSFER | transferred products |
| INVENTORY__ADJUST | adjusted a product quantity |
| LOCATION__CREATE | created a new location |
| LOCATION__DELETE | deleted a location |
| LOCATION__EDIT | renamed a location |

Account type 1 (Records / Arvig) uses record wording: created/deleted/edited records, assigned records, deallocated records, transferred records, adjusted a record. Location phrases stay the same.

Numeric filters in `GetActivitiesList` Category argument:

| Category | Meaning in comments | Activity codes |
| --- | --- | --- |
| 0 | All inventory | 1, 3, 4, 25 |
| 1 | Check in | 1, 4, 25 |
| 2 | Check out | 3, 4, 25 |
| 3 | Transfer | 4 |
| 13 | Adjust | 25 |
| 4 | All product | 0, 2, 5 |
| 5 | Create products | 0 |
| 6 | Delete products | 2 |
| 7 | Edit products | 5 |
| 8 | All location | 6, 7, 8 |
| 9 | Create locations | 6 |
| 10 | Delete locations | 7 |
| 11 | Edit locations | 8 |
| 12 | All | 0, 1, 2, 3, 4, 5, 6, 7, 8, 25 |

The enum values themselves live with `ActivityCodeIndex`. The names are used throughout the site. The integer mapping above is what the history query filters on. Confirm the enum numeric values against the compiled Activity type if the source enum is not in this repo.

History UI buttons in `ActivityHistory.aspx.vb` match these groups: inventory, check in, check out, transfer, adjust, products create/delete/edit, locations create/delete/edit, all. Also load more, location filter, user filter, date filter, download report.

## Transfer page modes

`Transfer.aspx` script distinguishes check-in mode (`isTransferCheckinMode`) from a normal transfer. Quantity modal title is "Check-in quantity" or "Transfer quantity". Dragging a product row calls `TransferFunction`. Dragging the whole list calls `TransferEverything`. Check-in uses an infinite quantity sentinel so stock is not capped by a source location. Same-location and All Locations (`-2`) drops are rejected on the map before this page opens.

## Map single-unit move

`mapBeginSingleUnitTransfer` opens the in-map comment dialog only when the dragged location contains exactly one unit, or when a specific product row being dragged has quantity 1. Otherwise `mapOpenInventoryTransferPage` opens Transfer (desktop Fancybox) or MOBILE_Transfer (narrow).

## Records application

Account type 1 changes activity language only in `GetActivityDescription`. Whether the rest of the UI swaps "product" for "record" still needs a dedicated pass (`App_Code/Classes/Customizations/RecordsApp.vb`).
