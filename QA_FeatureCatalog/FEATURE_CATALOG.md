# CyberStockroom feature catalog

Primary reference for knowledge-base coverage. Identifiers are stable. Add new features with the next free number in that prefix. Do not renumber.

| Field | Meaning |
| --- | --- |
| Confidence | **Confirmed** means the behavior was read in this repository. **Inferred** means a nearby caller makes the behavior likely. **Uncertain** means the implementation was not fully traced. |
| KB Status | Starts as `Not audited`. |
| KB Article URL | Starts blank. |

Knowledge-base comparison target: https://cyberstockroom.helpscoutdocs.com/

Adequate coverage means the article explains what the feature does, how to open it, its options, and the constraints below. A mention is not coverage.

Modules in this file: Settings and account (above), then map, movement, products, activity, expirations, kitting, search, and reports (appended). A second-pass control-by-control traceability check is not finished. Do not treat this file as absolute 100% coverage. Full research notes stay in `_research/`.

## ID index (this revision)

| Prefix | Module |
| --- | --- |
| SET | Settings shell |
| ACC | Sign-in, profile requirement, signup billing landing |
| TEAM | Team members |
| CFL | Custom fields |
| DEF | Default check-in and check-out locations |
| API | API keys |
| LSW | Lansweeper |
| DSP | Display settings |
| ACCSET | Account-wide time zone and currency |
| SUB | Subscription and billing |
| MAP | Map and locations |
| XFR | Check-in, check-out, transfer, Quick Scan, mobile movement |
| PRD | Product list |
| PED | Product editor, create, import, barcodes |
| ACT | Activity history |
| EXP | Expirations |
| KIT | Kitting |
| SRCH | Header search |
| RPT | Reports |

## Roles used below

Effective role comes from `User_Legacy.GetEffectiveUserType`. A stored `MOBILE` user is treated as User. `SUPER_USER` matches no Settings section, so that account sees an empty Settings page. Whether any customer still has `SUPER_USER` was not checked in data.

| Effective role | Settings sections |
| --- | --- |
| Admin | Profile, team, custom fields, default locations, API, Lansweeper request, display settings including Share Map Layout, time zone, currency, subscription |
| User | Profile, team, custom fields, default locations, API, display settings. No Share Map Layout, Lansweeper, time zone, currency, or subscription |
| Read-only | Profile, custom fields, API, display settings |

`webAPI_Utilities.isAllowed` also checks the `csToken` cookie. Several screens are stricter than the API, or the reverse. Each feature says which one applies.

---

## SET — Settings shell

### SET-001 — Settings sections

- **Module:** Settings. **Page:** `Settings.aspx`. **Parent:** none.
- **What it does:** Left menu scrolls to Profile & Team, Custom Fields, Default Locations, API & Integrations, Options, or Subscription. Hidden menus are skipped. Options is the label for display settings. Admins also reach time zone and currency further down that same scroll; those two have no menu item of their own.
- **Why:** Move between settings without leaving the page.
- **Access:** Header account menu or the mobile Settings link. Signed in.
- **Options:** Menu labels are PROFILE & TEAM, CUSTOM FIELDS, DEFAULT LOCATIONS, API & INTEGRATIONS, OPTIONS, SUBSCRIPTION. Anchors: `profile`, `fields`, `DefaultLocations`, `integrations`, `generalSettings`, `subscription`.
- **Permissions:** See the role table. `ShowAllowedMenu` / `ShowAllowedSections` in `Settings.aspx.vb`.
- **Result:** Scroll position only.
- **Code:** `Settings.aspx` 51–87; `js/components/menu.js`; `js/pages/settings.js`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Settings page sections

### SET-002 — Text fields save on change

- **Module:** Settings. **Pages:** name, email, custom-field names, currency, create-field box.
- **What it does:** Focus remembers the value. Typing marks the field unsaved. Enter blurs and fires the field’s change handler. Escape restores the remembered value and does not save.
- **Access:** Those inputs.
- **Related:** SET-003. Threshold, max highlight, expiring soon, and currency also save from Enter through `toggle.js`.
- **Code:** `js/components/text-input.js`; `js/components/toggle.js`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** How Settings text fields save

### SET-003 — One settings write at a time

- **Module:** Settings. **Pages:** invite, custom-field create/delete/reorder/visibility/personalized sort, API key create/delete.
- **What it does:** While one of those requests runs, the same controls are disabled.
- **Failure:** “Another action is currently in progress. Please wait for it to complete.”
- **Edge:** Profile name, email, password, and the display toggles are not in this lock.
- **Code:** `js/business/action-blocking.js`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Why Settings asks you to wait

---

## ACC — Sign-in and profile

### ACC-001 — Log in with email

- **Page:** `Login.aspx`.
- **What it does:** Checks email and password. On success writes the session and `csToken` and logs the account in. An existing session redirects to `Map`.
- **Options:** Email placeholder `me@email.com`. Password placeholder `***********`.
- **Failure:** “The email or password is not correct...” HTTPS is forced.
- **Code:** `Login.aspx` 169–186; `Login.aspx.vb` `btn_login_Click`, `Page_Init`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Log in to CyberStockroom

### ACC-002 — Log in with Google

- **Page:** `Login.aspx`.
- **What it does:** The Google button stores the ID token and clicks the hidden Google login button. On an invitation, a valid token calls `signIn_google` and `Account.LogIn_Google`.
- **Visibility:** Public login form. If the account is `googleOnly`, the invitation form hides email, password, login, and forgot-password. The Google button stays.
- **Failure:** A failed token check on the invitation path exits without an on-page message. The ordinary (non-invitation) failure sentence was not fully traced past `VerfiyGoogleToken`.
- **Code:** `Login.aspx` 206–242; `Login.aspx.vb` 185–213, 289.
- **Confidence:** Confirmed for the invitation path. Inferred that the main button posts the same handler. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Log in with Google

### ACC-003 — Forgot password

- **Page:** `Login.aspx`, then `Login.aspx?PasswordReset={guid}`.
- **What it does:** Looks up the email, stores `PasswordResetID`, and emails `https://www.cyberstockroom.com/Login?PasswordReset=` plus the GUID from `support@cyberstockroom.com`. The reset page title is “Reset your password” and the label is “Pick a New Password”. The email box is locked. Submit stores a new salted hash and logs in. This path does not check a minimum length.
- **Failure:** Unknown email runs an Intercom message “That Email is not in our records...”. A known email runs “An Email has been sent”. Empty new password is not rejected here.
- **Edge:** The reset host is hard-coded to `www.cyberstockroom.com`. Invitation links use the current request host.
- **Code:** `Login.aspx.vb` 122–138, 216–278.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Reset a forgotten password

### ACC-004 — Accept an invitation

- **Page:** `Login.aspx?Invitation={guid}`. **Parent:** TEAM-004.
- **What it does:** Loads the account and email from `InvitationID`. Title becomes “Accept your Invitation” and the password label “Create your password”. A non-blank password is stored, a new-user notification is sent, and the person is logged in. Google acceptance writes email, Google id, name, and Google photo URL.
- **Options:** Role was chosen by the inviter and is not shown here.
- **Failure:** Blank password: “Please create a password to accept your invitation.” No 6-character minimum on this path. A bad GUID leaves the normal login form. `googleOnly = 1` hides email and password.
- **Result:** The invitation id is not cleared by the SQL that was read. A blank invited name then opens ACC-007 on the next page other than Settings.
- **Code:** `Login.aspx.vb` 86–213.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Accept a team invitation

### ACC-005 — Choose a plan during signup

- **Page:** `SecureRegistration.aspx` iframes `UpdateAccount.aspx` with no query.
- **What it does:** The iframe is the same monthly and annual checkout as SUB-002. `UpdateAccount` redirects to Login when there is no session.
- **Edge:** No company-name or seat-count field was found on `SecureRegistration.aspx`. Prices are drawn on images, not stored as text. Do not publish a price from this catalog. Live price ids are recorded under SUB-002.
- **Code:** `SecureRegistration.aspx`; `UpdateAccount.aspx.vb` `LoginReplacement`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Choose a plan during signup

### ACC-006 — Welcome page (not a customer step)

- **Page:** `Welcome.aspx`.
- **What it does:** `Page_Init` redirects to `/Map` and returns. Profile and demo-data code below that line does not run.
- **Documentation note:** Do not publish Welcome as a setup wizard.
- **Code:** `Welcome.aspx.vb` 16–28.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

### ACC-007 — Required name

- **Page:** `ProfileRequired.aspx`, opened from `UserPage.master` when `FirstName` is blank. Not opened on Settings or `?printable=true`.
- **What it does:** Name plus the profile icon picker. Save validates the name, writes it, then applies the icon. The parent reloads, or the browser goes to `/Map` if there is no parent.
- **Validation:** Same name rules as SET-004’s sibling ACC name rules: empty, longer than 50, or duplicate on the account. Image rules match ACC-008’s picker: png, jpeg, gif, webp, under 3 MB.
- **Code:** `UserPage.master.vb` `OpenProfilePopupIfNameBlank`; `ProfileRequired.aspx.vb` `btn_save_Click`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Enter your name when the app asks

### ACC-008 — Profile picture

- **Pages:** `Controls/ProfileIconPicker.ascx` on Settings and on Profile Required.
- **What it does:** Choose preset `1` through `15` or upload, then Apply. Upload uses `ProfileIcons.SaveUpload`. A preset copies `Images/Avatars/{n}.png`.
- **Defaults:** `DefaultKey` is `"1"`. Accept `image/png,image/jpeg,image/gif,image/webp`.
- **Failure:** “Please choose an image file.” “Please choose an image under 3 MB.”
- **Edge:** On Settings the picker’s own name box is hidden. The name is ACC-009.
- **Code:** `ProfileIconPicker.ascx.vb` `btn_apply_Click`; `ProfileIcons.vb`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Choose a profile picture

### ACC-009 — Your name

- **Page:** Settings profile `txt_profile_user_name`. Also ACC-007.
- **What it does:** On change, posts `UpdateUserName`, trims, checks `DisplayNameError`, and saves `Users.FirstName`. The team card for the current user updates without a full reload.
- **Who:** Any role that can see the profile section.
- **Validation:** Empty: “Please enter your name.” Over 50: “Please use 50 characters or fewer.” Duplicate: “Someone sharing this account is using this name already...” Escape restores the focused value.
- **Result:** Activity rows and the collapsed menu use this name.
- **Code:** `js/business/profile.js` `updateUserName`; `webAPI/users.aspx.vb` `UpdateUserName`; `User_Legacy.DisplayNameError`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Change your name in Settings

### ACC-010 — Your email

- **Page:** Settings `txt_profile_email`.
- **What it does:** Posts `UpdateUserEmail`. The server checks format, uniqueness in this account, uniqueness in any account, and pending invitations.
- **Failure:** The input title becomes “That email is invalid or already exists.” The server throws an empty `ArgumentException`.
- **Edge:** The “same as old” short-circuit compares the new email to `FirstName`, not to the current email. A no-op only happens when the typed email equals the person’s name. Google-linked users can still edit email. Password is what gets hidden.
- **Code:** `js/business/profile.js` `updateUserEmail`; `webAPI/users.aspx.vb` `UpdateUserEmail`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Change the email on your user

### ACC-011 — Update your password

- **Page:** Settings profile.
- **What it does:** “Update Your Password” reveals old, new, and repeat. Save calls `SignInApplicationService.ChangePassword`.
- **Visibility:** Hidden when `GoogleID` is set.
- **Validation:** “The password is incorrect. Try Again?” “The passwords don't match. Try Again?” “That password is too short. Please use at least 6 characters. Try Again?” “The new password must be different! Try Again?” Client color (under 6 red, under 9 yellow, 9 or more green) does not block the postback. Success returns to `Settings.aspx`. Cancel only hides the form.
- **Result:** Salted SHA-256. An old unsalted hash is still accepted as the old password.
- **Code:** `Settings.aspx.vb` `btn_password_reset_click`; `SignInApplicationService.ChangePassword`; `js/business/profile.js` `validatePassword`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Update your password

### ACC-012 — Link Google on an existing user

- **Page:** Settings profile.
- **What it does:** Shown only when `GoogleID` is empty. The button verifies the token audience and stores the Google id. Redirects to `Settings#profile`. The password form disappears on the next load. The Google email from the token is not written by this click.
- **Failure:** A bad token exits with no on-page message. `settings.js` signs the Google JS client out on load.
- **Code:** `Settings.aspx.vb` `btn_google_login_click`; `SignInApplicationService.VerifyGoogleToken`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Link Google to an existing user

### ACC-013 — Role badge

- **Page:** Settings profile.
- **What it does:** Shows Admin, User, or Read-Only from the effective type. Display only.
- **Edge:** A Mobile badge exists in markup and is never turned on. Stored Mobile is shown as User. `SUPER_USER` matches no badge and also gets no profile section.
- **Code:** `Settings.aspx.vb` `_displayGoogleAndAdminBadge`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** What the role badge on your profile means

### ACC-014 — Subscription update confirmation

- **Pages:** `SuccessSignup.aspx`. Some `UpdateAccount` branches redirect to `_cvr/SuccessSignup` instead.
- **What it does:** Static “Success!” and “Thank you for Updating your subscription.” No plan name is printed.
- **Uncertain:** The `_cvr` copy’s exact sentence was not compared.
- **Code:** `SuccessSignup.aspx`; `UpdateAccount.aspx.vb` redirect branches.
- **Confidence:** Confirmed for `SuccessSignup.aspx`. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Subscription update confirmation

### ACC-015 — Allow or deny an OAuth connection

- **Pages:** `OAuth2/auth.aspx`, `OAuth2/consent.aspx`.
- **What it does:** After a valid OAuth request, Cancel denies and redirects to the client with an error. Allow returns the user id to the client. A missing user index sends the browser to Login.
- **Options:** Buttons “Cancel” and “Allow”. Scope wording is rendered by `consentScreen`, which is not in this website project. Do not list scope names.
- **Related:** API-001 is a separate mechanism.
- **Code:** `OAuth2/consent.aspx.vb` `consent_allow_Click`, `consent_cancel_Click`.
- **Confidence:** Confirmed for the buttons. Uncertain for scope text. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Allow or deny an OAuth connection

---

## TEAM — Team members

### TEAM-001 — Team list

- **Page:** Settings team section. **Parent:** SET-001.
- **What it does:** Loads every user returned for the account. Cards sort Admin, then User, then Read-only. Search matches name or email. Role pills filter ADMIN, USER, READ-ONLY. Page size is 12.
- **Who sees it:** Admin and User. Read-only does not get the section.
- **Options:** Search and pills stay hidden until the unfiltered list is longer than 12. Placeholder “Search by name or email...”. No matches: “No users found”.
- **Edge:** A legacy Mobile row is labeled USER. Pending invites with a blank first name still appear if the query returns them. Seeing the list does not allow managing it.
- **Code:** `Settings.aspx.vb` `InitUsers`; `js/components/user-card.js`; `js/components/filters.js`; `js/components/pagination.js`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Find a teammate in Settings

### TEAM-002 — Change a teammate’s role

- **Page:** Role select on another user’s card. **Parent:** TEAM-001.
- **What it does:** Confirm, then `SetUserType` writes `TypeOfUser`.
- **Options:** `ADMIN`, `USER`, `READ-ONLY`. No Mobile option. The server rejects `MOBILE` with “MOBILE role is no longer supported.”
- **Who:** The select is disabled unless the viewer is Admin. Your own card has no select. The API allows admins only.
- **Failure:** Cancel does not post. A failed post reloads the cards from the last JSON.
- **Edge:** Nothing in this method keeps at least one admin. The method that was read does not compare the target account id to the caller’s account.
- **Code:** `js/business/users.js`; `webAPI/users.aspx.vb` `SetUserType`; `js/components/user-card.js`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Change a teammate’s role

### TEAM-003 — Remove a teammate

- **Page:** DELETE on another user’s card. **Parent:** TEAM-001.
- **What it does:** Confirm “Are you sure you want to delete the user …”, then deletes that user row.
- **Who:** Rendered only when the viewer is Admin and the card is not themselves. API is admin-only.
- **Edge:** No last-admin guard. If that was the last card on a page, the list moves to the previous page.
- **Code:** `js/business/users.js` `deleteUser`; `webAPI/users.aspx.vb` `DeleteUser`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Remove a teammate

### TEAM-004 — Invite a teammate

- **Page:** Settings “Invite a Team Member”. **Parent:** TEAM-001.
- **What it does:** Checks a simple email pattern, then inserts or updates `CS_ADMIN.Users` with a new invitation GUID and emails `Login.aspx?Invitation={guid}`. Subject: “{inviter name} is inviting you to CyberStockroom. Details Inside.” From `admin@cyberstockroom.com`.
- **Options:** Role `ADMIN`, `USER`, or `READ-ONLY`. The first option, and so the unmarked default, is `ADMIN`. Placeholder `example@company.com`. The stored name is an empty string.
- **Who sees the form:** Admin and User, because both see the team section. The API allows admins only. A User who clicks gets “Unable to Invite - Try Again?”
- **Validation:** Empty: “Please enter an email address.” Bad pattern: “Please enter a valid email address.”
- **Result:** `TypeOfUser` is the selected role. `_onboardingPlaybook` 1, `_onboardingCompleted` 1, `_onboardingStatus` `finalize`. Map coordinates are copied from the inviter with the share-map marker stripped. `SHOW_EXPIRATIONS` is copied from the inviter.
- **Edge:** If this account already has that email, the update changes invitation id, name, onboarding flags, coordinates, and expirations. It does not change `TypeOfUser`. If the email exists on another account and not this one, the create function returns without inserting, but the send function still runs and the button can say “Send Another Invitation”.
- **Related:** ACC-004.
- **Code:** `js/business/invitations.js`; `webAPI/invitations.aspx.vb` `SendInvitation`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Invite a teammate and choose their role

---

## CFL — Custom fields

A custom field is a named text field, optionally with a preset list. The editor does not offer date, number, or dropdown types. `CS_FIELDS.FieldType` is only `PRODUCT_PROPERTY` and `CUSTOM_FIELD`.

Buy Price and Sell Price are built-in cards, not custom fields. Default order tokens: Buy Price `1000000001`, Sell Price `1000000002`, then each `CF_Index`.

Names and presets are account-wide. Order, price visibility, and personalized sort are stored on the current user’s `GridsterCoordinates2017`.

Create, rename, delete, and presets require raw type Admin (`hidden_custom_fields_can_edit = 1`). A stored Mobile user is a User for the menu and cannot edit fields. Reorder and price visibility allow Admin, User, and Read-only.

### CFL-001 — Personalized sort

- **Pages:** Settings custom fields, and `Controls/CustomFieldEditorModal.ascx` on product pages.
- **What it does:** Saves a per-user flag. When on, fields come back in that user’s order and up/down buttons appear, including on Buy Price and Sell Price. When off, the Settings list hides the Buy Price and Sell Price cards and uses the default order. Turning it off does not delete the saved order.
- **Default:** Off when the coordinate token is absent.
- **Failure:** “Unable to save the personalized sort preference right now.” The toggle reverts.
- **Edge:** A new field is appended the next time a personalized list is normalized.
- **Code:** `js/business/custom-fields.js` `handlePersonalizedSortToggle`; `webAPI/settings.aspx.vb` `SaveCustomFieldOrder`; `Gridster_Utilities.NormalizeCustomFieldOrder`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Turn on a personal custom-field order

### CFL-002 — Show or hide Buy Price and Sell Price

- **Parent:** CFL-001.
- **What it does:** Show toggles on those two cards save `showBuyPrice` / `showSellPrice` for the current user. The map and editors read the same flags.
- **Visibility:** The cards are omitted from the Settings list until personalized sort is on. So price visibility cannot be changed from Settings until that toggle is on. In the product modal, a hidden price field is a compact row with Show.
- **Default:** Visible when the hide token is absent. Card subtitle is “DEFAULT”. Names are not editable. There is no delete button.
- **Failure:** “Unable to save the field visibility right now.”
- **Code:** `js/business/custom-fields.js` `toggleSpecialFieldVisibility`; `Gridster_Utilities.GetShowBuyPriceFromRaw`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Show or hide Buy Price and Sell Price

### CFL-003 — Add a custom field

- **Page:** “Create New Field...” under the list, on Settings and in the product-page modal.
- **What it does:** Inserts `fieldName` and returns the new `CF_Index`. The new card starts with `validValues: [""]`, which is not a preset.
- **Who:** Admin only.
- **Validation:** No empty-name or duplicate-name check in `CreateNewCustomField`.
- **Code:** `js/business/custom-fields.js` `createNewCustomField`; `webAPI/customFields.aspx.vb` `CreateNewCustomField`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Add a custom field

### CFL-004 — Rename a custom field

- **Parent:** CFL-003.
- **What it does:** Changing the name on a real custom-field card posts `RenameCustomField`. Account-wide.
- **Who:** Admin. Buy Price and Sell Price inputs are read-only for everyone.
- **Validation:** No length or uniqueness check in the web method.
- **Code:** `webAPI/customFields.aspx.vb` `RenameCustomField`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Rename a custom field

### CFL-005 — Delete a custom field

- **Parent:** CFL-003.
- **What it does:** Confirm, then deletes the field definition.
- **Confirm:** “Are you sure you want to delete the field … Warning: Existing data for this field will be erased! It is recommended that you export your inventory first before deleting custom fields.”
- **Who:** Admin. Buy Price and Sell Price cannot be deleted here.
- **Uncertain:** The UI states that existing values are erased. The repository cascade was not read.
- **Code:** `webAPI/customFields.aspx.vb` `DeleteCustomField`.
- **Confidence:** Confirmed for the button and the warning. Uncertain for the cascade. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Delete a custom field

### CFL-006 — Preset choices

- **Page:** Presets on a Settings custom-field card opens `Popups/FixedMultiFields.aspx?id={CF_Index}`. The product-page modal does not show Presets.
- **What it does:** Saved non-blank values become `validValues`. A field counts as having presets when any value is non-blank and is not `Other (Specify)`.
- **Options:** Checkbox “allow other”. It appends `Other (Specify)` only when at least one real preset remains. An empty save leaves the field as a normal text field. Blank values are stripped.
- **Who:** The Settings button is admin-only. `SavePresets` itself was not given a role check in the application service that was read.
- **Edge:** Closing the popup does not refresh Settings (`afterClose` is empty).
- **Code:** `Popups/FixedMultiFields.aspx.vb` `SavePresets`; `CustomFieldApplicationService.SavePresets`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Add preset choices to a custom field

---

## DEF — Default locations

Per user. Admin and User. Read-only is redirected to `/_admin/_unauthorized` if they open the picker directly. Clear stores location id `-2`, displayed as `(none)`.

### DEF-001 — Default check-in location

- **Page:** Settings “Default Check-In Location” opens `_locationSelectorToggle.aspx?type=defaultcheckin`.
- **What it does:** Save updates `CS_ADMIN.Users.CheckInLocationDefault`. Clear sets `-2`.
- **Popup:** Header “Select Default Check-In Location”. Buttons Save and `CLEAR Selection`.
- **Used by:** Check-in flows that read `CheckInLocationDefault`, including product selector and check-in of created products.
- **Result:** The popup sets `cookie_refresh_settings=TRUE` before it closes (`_locationSelectorToggle.aspx.vb`). Settings reloads when that cookie is `TRUE`.
- **Code:** `_locationSelectorToggle.aspx.vb` `save_defaultCheckin`; `Settings.aspx.vb` `InitDefaultLocations`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Set your default check-in location

### DEF-002 — Default check-out location

- **Page:** “Default Check-Out Location”, `?type=defaultcheckout`.
- **What it does:** Updates `CheckOutLocationDefault`. Clear sets `-2`. Same picker and the same refresh uncertainty as DEF-001.
- **Code:** `_locationSelectorToggle.aspx.vb` checkout save.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Set your default check-out location

---

## API — API keys

### API-001 — Create and delete an API key

- **Page:** Settings “API Keys”.
- **What it does:** If the account id is on `CS_API_v0._betaList`, the request sentence is replaced by key cards, a name box, and “+ Create New API Key”. Create returns the plaintext once in a prompt: “This is the only time this API key will be shown. Please copy and store it safely:”. Later loads show a truncated display and an issued date (`MMM d, yyyy`). Delete revokes that key.
- **Who sees the section:** Admin, User, and Read-only. The manager UI appears only for beta accounts. Create and delete allow every role at the API, and delete also requires the key to belong to the caller’s own key list.
- **Non-beta text:** “The CyberStockroom API is currently available to select users only. You can request access by emailing us at support@cyberstockroom.com”.
- **Validation:** Empty name: “Please enter a valid key name”. Create failure: “Error creating API key. Please try again.” Delete confirm warns that access is revoked immediately. Names longer than 30 characters display with `...`; the full name is the tooltip.
- **Edge:** A non-beta caller who posted `CreateNewKey` directly is not stopped by `_isBetaUser`. The UI is the gate.
- **Code:** `ApiKeyApplicationService.vb`; `js/business/api-keys.js`; `webAPI/apiKeys.aspx.vb`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Create and delete an API key

### API-002 — API documentation link

- **Page:** Under the API key area, including non-beta accounts.
- **What it does:** Opens `https://documenter.getpostman.com/view/1256102/2sB34ZqPYv` in a new tab. Link text “Read API Documentation”.
- **Code:** `Settings.aspx` 373.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Open the CyberStockroom API documentation

---

## LSW — Lansweeper

### LSW-001 — Request the integration

- **Page:** Settings Lansweeper heading. Admin only. Users see the API section from the same menu icon and do not see this heading.
- **What it does:** Shows “The Lansweeper Integration is available by request. If you'd like to conenct your Lansweeper account please email us at support@cyberstockroom.com to schedule a call.” The typo “conenct” is in the markup. `InitLansweeper` is commented out. Synchronize and Disconnect are inside a server comment.
- **Result:** No Lansweeper data changes from this block.
- **Code:** `Settings.aspx` 386–407; `Settings.aspx.vb` line 53.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Request the Lansweeper integration

### LSW-002 — Choose sites (not linked from current Settings)

- **Page:** `pages/settings/popups/lansweeperSiteSelector.aspx`.
- **What it does:** Checkboxes of sites. Connect saves checked site uid and name and redirects to the success popup. Zero checked sites goes to `/Settings`.
- **Copy:** “Only sites that contain assets will be synchronized. Some demo sites may not be permitted.”
- **Failure:** A load exception goes to `lansweeperConnectionFailure?source=siteSelector`. Failure text: “There was a problem connecting your Lansweeper Account.”
- **Reachability:** No live Settings link. Recorded so it is not mistaken for a current click path.
- **Code:** `lansweeperSiteSelector.aspx.vb` `btn_connect_Click`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Choose which Lansweeper sites to sync

### LSW-003 — Match a Lansweeper field (not linked)

- **Page:** `lansweeperFieldToggle.aspx`.
- **What it does:** Options are this account’s custom fields (`CF_Index` / `fieldName`). A selection sets `cookie_refresh_settings` and closes the fancybox. Header: “Select a Field to Match: '{name}'”.
- **Uncertain:** The UI class `lansweeperFieldToggle` that stores the pairing was not opened.
- **Code:** `lansweeperFieldToggle.aspx.vb`.
- **Confidence:** Confirmed for the option list. Uncertain for the stored mapping. **KB Status:** Not audited. **KB Article URL:**

### LSW-004 — Match a category to a location (not linked)

- **Page:** `_locationSelectorToggle.aspx?type=lansweeper`.
- **What it does:** Header “Select a Location to Match: '{name}'”. Save replaces a tag on the location. Clear calls the same save with the clear flag. Read-only is redirected.
- **Reachability:** Live Settings hrefs are only `defaultcheckin` and `defaultcheckout`.
- **Code:** `_locationSelectorToggle.aspx.vb` `save_lansweeper`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Match a Lansweeper category to a location

### LSW-005 — Link, sync, and progress (not linked from current Settings)

- **Pages:** `lansweeperLinkAndSync.aspx`, `lansweeperConnectionSuccess.aspx`, `lansweeperConnectionFailure.aspx`.
- **What it does:** If progress is 0, link-and-sync sets “Preparing to Synchronize...” at 1%, calls link and synchronize, and writes `ColumnOrder`. The success popup shows progress and status and, at 100%, waits 1.5 seconds and goes to `/Map`. A second synchronize is skipped when progress is already not 0.
- **Uncertain:** `lansweeperLinkAndSync.aspx.vb` and `lansweeperConnectionSuccess.aspx.vb` both declare the class `pages_settings_popups_lansweeperConnectionSuccess`. Which file the compiler binds was not verified. `CALLBACK_TYPE` in the file that was read is `callBackType.test`.
- **Code:** those three popups; `LansweeperApplicationService.SyncAllSites` (inserts worker rows; called by the commented Settings button, not by the live page).
- **Confidence:** Confirmed for the methods read. Uncertain for the duplicate class. **KB Status:** Not audited. **KB Article URL:**

---

## DSP — Display settings

Per user unless noted. Admin, User, and Read-only. A failed toggle reverts after 1.5 seconds. Share Map Layout is the admin-only row.

### DSP-001 — Share Map Layout

- **What it does:** Writes coordinate marker `-16,CS_MAP_SHAREABLE_ON` on the current admin. Other users can list shared maps and copy that layout. The page says teammates can sync to the layout and cannot change it. Invited users receive a copy of the inviter’s coordinates with the marker stripped.
- **Default:** Off when the marker is absent.
- **Who:** Admin row and admin API.
- **Code:** `webAPI/settings.aspx.vb` `SaveShareMapLayout`, `GetSharedMaps`; `Settings.aspx` 444–446.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Share your map layout with the team

### DSP-002 — Product Images

- **What it does:** Sets `SHOW_PRODUCT_IMAGES` for this user. The products grid adds image cells only when the flag is true. The code property is spelled `SHOW_PRORDUCT_IMAGES`.
- **Code:** `webAPI/settings.aspx.vb` `ShowProductImages`; `Products.aspx.vb` `StylingRefresh`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Show product images in the product list

### DSP-003 — Zero Quantity Products

- **What it does:** Sets `SHOW_ZERO_QUANTITY`. When off, the products grid skips rows whose quantity is 0.
- **Edge:** The sentence “Locations with 0 quantity will appear in white on the map” belongs to DSP-006, not to this toggle.
- **Code:** `webAPI/settings.aspx.vb` `ShowZeroQuantityProducts`; `Products.aspx.vb` around 1846.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Include products with zero quantity

### DSP-004 — Expirations

- **What it does:** Sets `SHOW_EXPIRATIONS` for this user. The master page then shows the Expirations menu. The map popup can include expiration. Turning the toggle off hides the Expiring Soon block in Settings. It does not by itself write the window to 0.
- **Related:** New invites copy the inviter’s flag (TEAM-004).
- **Code:** `webAPI/settings.aspx.vb` `ShowExpirations`; `UserPage.master.vb` 66–68.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Turn expiration dates on or off

### DSP-005 — Expiring Soon

- **Parent:** DSP-004.
- **What it does:** Stores a day count on coordinate token `-18`. The map reads `hidden_EXPIRING_SOON_DAYS`. Helper: “Highlight products expiring within this period”.
- **Options:** Number (min 1) and unit days, weeks, months, or years. Weeks are ×7, months ×30, years ×365. Exact multiples display back as the larger unit (14 days shows as 2 weeks, 30 days as 1 month).
- **Defaults:** Markup value 60 days. Stored `-1` is treated as on at 60. Stored `0` is off. Turning the toggle on with an empty value saves 60. `DefaultExpiringSoonWindowDays` is 60, including when the token is absent for the map.
- **Failure:** “Enable Expirations before using Expiring Soon.” “Expiring soon window must be a valid duration greater than 0.” “Error saving expiring soon window. Please try again.”
- **Code:** `js/business/general-settings.js`; `webAPI/settings.aspx.vb` `SaveExpiringSoonWindow`; `Gridster_Utilities.vb`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Set the expiring-soon highlight window

### DSP-006 — Quantity Threshold

- **What it does:** Stores `_generalThreshold` for this user. Copy: “Highlight locations with quantity at or below:” and “Locations with 0 quantity will appear in white on the map.” Off stores 0. Turning the toggle on saves 1 immediately. The map builder receives the value.
- **Default:** If the stored value is greater than 0, the box shows it and is enabled. Otherwise the toggle is off and the box shows `1` disabled.
- **Failure:** “The threshold must be a valid number bigger than 0.” “Error saving threshold value. Please try again.”
- **Code:** `webAPI/settings.aspx.vb` `ShowGeneralThreshold`; `Map_CONTROL_2017.ascx.vb` around 141–150.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Highlight low quantities on the map

### DSP-007 — Max Highlight

- **Parent:** DSP-006.
- **What it does:** Stores a positive integer above the threshold, or 0 when off. Copy: “Highlight locations with quantity at or above:”. The block is inside the threshold details, so it is available only while Quantity Threshold is on.
- **Default:** When nothing is stored, the toggle is off and the box shows `10`.
- **Failure:** “Enable Quantity Threshold before using Max Highlight.” “Max highlight must be a valid number greater than 0.” “Max highlight must be greater than the quantity threshold.” “Error saving max highlight. Ensure it is greater than the quantity threshold.”
- **Edge:** If validation fails after the toggle was disabled, the control can stay disabled until reload.
- **Code:** `webAPI/settings.aspx.vb` `SaveMaxHighlight`; `js/business/general-settings.js` `handleMaxHighlightToggle`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Highlight high quantities on the map

### DSP-008 — Kitting toggle (not a feature)

- **What it does:** The row is `display: none`. Settings does not initialize it and has no save handler.
- **Documentation note:** Do not publish Kitting as a Settings option. `SHOW_KITTING` is still loaded onto the user and can show the Products-menu Kitting icon. How that flag is turned on was not found in Settings.
- **Code:** `Settings.aspx` 526–536; `UserPage.master.vb` 70–72.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**

---

## ACCSET — Account settings

Admin only. Both values are account-wide, not per user. Fallback when the account row cannot be read: currency `$`, time zone `-5`.

### ACCSET-001 — Time zone

- **What it does:** The dropdown saves on change to `Accounts.TimeZone`. Activity timestamps use this offset. “Saved ✓” for about 2 seconds.
- **Options:** Integer offsets from `-12` through `13`. Labels are the GMT list in `Settings.aspx` 631–657. Two labels share value `5`: “(GMT+05:00) Yekaterinburg” and “(GMT+05:00) Islamabad, Karachi, Tashkent”. There is no half-hour offset.
- **Failure:** “Error saving timezone. Please try again.”
- **Code:** `webAPI/settings.aspx.vb` `SetTimeZone`; `js/business/general-settings.js` `handleTimezoneSave`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Set the account time zone

### ACCSET-002 — Currency symbol

- **What it does:** Save or Enter writes `Accounts.Currency`. Any non-empty string is accepted. This is not a currency-code list. The subscription card formats money from the subscription record, not from this box.
- **Default:** Markup `$`, replaced on load by the stored value. Fallback `$`.
- **Failure:** “Please enter a currency symbol”. “Error saving currency symbol. Please try again.”
- **Code:** `webAPI/settings.aspx.vb` `SetCurrencySymbol`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Set the currency symbol

---

## SUB — Subscription and billing

Admin section. `getSubscrtiption` maps the stored subscription. It does not contain a price table.

Plan labels: `STANDARD` shows the plan name with no badge. `CUSTOM` shows “Custom Plan” and badge “Custom” (“This plan was created specifically for your team”). `ENTERPRISE` shows “Enterprise Plan” (“This plan that includes more than the standard turnkey solution”). `LEGACY` shows “Legacy Plan” (“This plan is no longer available, but will continue to be active for your team”).

Payment method labels: Cheque → “Bank Cheque”. Coupa → “Coupa (Payment Platform)”. Direct bank transfer → “Direct Bank Transfer”. PayPal card, PayPal invoice, or Stripe invoice → “Online Invoice”. Stripe card → “Credit Card (Stripe)”. Anything else → “(None)”.

Frequency: `IsAnnual` true is “Annually”. False is “Monthly”.

### SUB-001 — Subscription summary

- **Page:** Settings `div_subscription_container`.
- **What it does:** Paints plan name, billing amount, frequency, payment method, payment details for non-Stripe notes, contact, card, and activated. Amount uses `$` plus the code for USD or CAD, and the code then the amount for other currencies. A missing amount omits the row.
- **Empty state:** “No Active Subscription”, “You don't have an active subscription. Subscribe to a plan to get started.”, and “Subscribe to a Plan” linking to `UpdateAccount?Update=Plan`.
- **Code:** `js/business/subscription.js` `loadSubscription`; `SubscriptionApplicationService.vb`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Read your subscription on the Settings page

### SUB-002 — Change a Stripe subscription

- **Parent:** SUB-001. **Pages:** Settings buttons, `UpdateAccount.aspx`, `BillingHistory.aspx`.
- **Visibility:** Update Plan, Change Card, Cancel Subscription, and Billing History render only when the payment-method string contains “Stripe”. That includes “Credit Card (Stripe)”. “Online Invoice” does not, so PayPal and Stripe-invoice subscriptions do not get these buttons. Other methods show “Please contact admin@cyberstockroom.com to change your subscription or payment method”. Stripe footnote: “For any billing questions please contact admin@cyberstockroom.com”.
- **Update Plan:** Opens `UpdateAccount?Update=Plan`. Monthly image uses live price id `price_1O6zRX4D3SV7Y45Utyewx37h`. Annual image uses `price_1O6zS34D3SV7Y45UCZ8p3YaG`. `test_ON` is false. The enterprise image has no click. Do not publish a dollar amount; the prices are in the images, not in text. If a card is already on file and `stripe_payment_skip` is `1`, the plan updates without a new checkout. Otherwise Stripe checkout runs.
- **Change Card:** Opens `UpdateAccount?Update=Payment`, which calls `updatePayment()` on first load.
- **Cancel:** Confirm “Are you sure you want to cancel your subscription?” with “Cancel Subscription” and “Keep Subscription”. The server sets `ConfirmedPayment` to 0, deletes the `StripeAccounts` row, and calls `stripeRegistrar.deleteSubscription`. Because confirmed payment is 0, the 14-day trial rule applies again. An account older than 14 days is then sent back to Settings by the billing gate.
- **Who:** Cancel and billing history require Admin. `UpdateAccount` blocks read-only only. It does not require Admin.
- **Code:** `js/business/subscription.js`; `webAPI/subscription.aspx.vb` `CancelSubscription`; `UpdateAccount.aspx` 101–139 and 414–449; `UpdateAccount.aspx.vb`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Change, cancel, or review a Stripe subscription

### SUB-003 — Billing history

- **Page:** `BillingHistory.aspx`. **Parent:** SUB-002.
- **What it does:** Lists Stripe charges. Columns Date (`MMM dd, yyyy`), Amount (charge amount / 100), Subscription (invoice plan name plus description, cut off at `@`), Status Successful or Failed. Next payment uses the first subscription’s period end and plan amount / 100. The invoice table is built and not added; the charges table is what is shown.
- **Who:** Admin. Direct URL redirects others to `/_admin/_unauthorized`.
- **Failure:** Any exception replaces the table with “No billing history to show...” and hides next payment.
- **Code:** `BillingHistory.aspx.vb`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Read billing history

### SUB-004 — Trial end and failed payment

- **What it does:** `BillingAccessGate` sends every signed-in page except Settings to `/Settings` when the unpaid trial is expired and `SuppressUpgradeAlert` is false, or when `ConfirmedPayment` is 1, the Stripe customer is delinquent, and `SuppressPaymentAlert` is false. Trial length is 14 days from `Accounts.DateCreated` while `ConfirmedPayment` is 0.
- **Banners that do not show:** Settings contains “Your free trial has expired. Please select a plan to continue..”, “You have exceeded the capacity of your current plan. Please upgrade to continue.”, and “Your payment method needs to be updated!” CSS hides all three. `ToggleExpiry`, `ToggleUpgrade`, and `TogglePayment` are not called. No writer for a capacity limit was found. Do not document a plan capacity. People sent to Settings are not automatically shown the plan popup.
- **UpdateAlert:** Hidden anchors exist. `settings.js` does not click them. In `UpdateAlert.aspx`, the `else if` assigns `UpdateType = "CC_Error"`, so the trial sentence is unreachable.
- **Suppress flags:** `SuppressUpgradeAlert` and `SuppressPaymentAlert` are account columns. No Settings control edits them.
- **Code:** `BillingAccessGate.vb`; `Account.vb` 889–901; `css/pages/settings.css` 113–118; `js/business/subscription.js` 5–38; `UpdateAlert.aspx`.
- **Confidence:** Confirmed. **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** What happens when a trial ends

---

## Uncertain items from this pass

- OAuth scope labels (`consentScreen` / `auth` are outside this website tree).
- Stored pairing inside the `lansweeperFieldToggle` class.
- Which of the duplicate Lansweeper class files the compiler binds.
- Default-location refresh cookie is set by `_locationSelectorToggle.aspx.vb`. Removed from this uncertain list.
- Database defaults for product images, zero quantity, and expirations on a brand-new admin. The Settings page displays whatever is already stored. Invites copy expirations from the inviter.
- `AccountType` integer was not mapped to a settings behavior.
- `_cvr/SuccessSignup.aspx` body text.
- Whether any live user still has `SUPER_USER`.
- Custom-field delete cascade beyond the on-screen warning.
- Google login failure text for a normal login.
- Half-hour time zones are not in the dropdown. Older stored integers were not checked.
