# Internal validation — do not ingest

Run date: 2026-11-07. This note is not retrieval material for the customer assistant. `KNOWLEDGE_BASE_SOURCE.md` is the only support source.

Website HEAD: `a4f1fc6b686294b7c00c692b744565efd5dc447d` on `mobile-responsive`. Working tree clean. Product behavior is unchanged from `e8172b5c35b4e32a77ea28569ae82ad28ed83f8e`. The only commit in range updates the catalog command and an IDE user file.

## Coverage

151 catalog IDs. 141 included in `KNOWLEDGE_BASE_SOURCE.md`. 10 excluded. No ID is in both lists. No support-source ID is missing from the catalog. No duplicate headings. Every included feature has Availability, Access, Purpose, Open, Steps, Result, and Confidence. The CSV parses and has 151 rows.

## Excluded

| ID | Reason |
| --- | --- |
| ACC-006 | Not live. Welcome redirects to the map before any wizard. |
| LSW-002 | Not live. Site picker is not linked from Settings. |
| LSW-003 | Not live. Field matcher is not linked. Stored pairing was not verified. |
| LSW-004 | Not live. Category-to-location matcher is not linked from Settings. |
| LSW-005 | Not live. Link, sync, and progress are not linked from Settings. |
| DSP-008 | Not live. The Settings kitting checkbox is hidden and unwired. |
| PED-017 | Not live. The document editor does not print, save, or continue. |
| PED-018 | Not live. Old clone, quantity-only delete, and success screens are not linked. |
| KIT-003 | Not live. Kit **manage** throws before any action. |
| RPT-002 | No menu path. Opening it requires a direct address. How a report is generated is outside this repo. |

## Kept internal (not copied into the support source)

- Changing or removing a teammate does not protect the last Admin. The role update that was read does not compare the target account with the caller’s account.
- The invite form can be visible to a User. Only an Admin can complete it. An email that exists only on another account can still reach the send step after the create returns without inserting. The support source says an email already on this account does not change that person’s role, and that a User sees “Unable to Invite - Try Again?”
- A direct API-key create is not stopped by the beta check. The support source only describes the request-access sentence and the manager on an enabled account.
- The email “same as old” check compares the typed email with the person’s name, not the current email. The support source only quotes “That email is invalid or already exists.”
- The password-reset page does not reject an empty password. The support source says that page does not show the 6-character rule used in Settings.
- An old unsalted password hash is still accepted as the current password when changing it in Settings.
- Preset save was not given a role check in the service that was read. The support source describes Presets as an Admin control on Settings.
- The plan-change page blocks Read-only users and does not require Admin. Cancel and billing history do require Admin.
- Trial and payment suppress flags have no Settings control. The three Settings banners stay hidden.
- The insights report assigns text as HTML and is not encoded. The page is excluded.
- Whether any live user still has the unused super-user role was not checked.

## Uncertain customer effects, stated as Uncertain in the support source

Location-clone quantities, Ctrl+drop stock math, Quick Scan stock math, expiration-replacement stock actions, kit storage and search matching, header and map search match fields, product-delete images and attachments and quantities, Google login failure text for a normal login, and whether a Read-only user can still drag the map.
