# CyberStockroom feature catalog

Primary reference for knowledge-base coverage. Identifiers are stable. Add new features with the next free number in that prefix. Do not renumber.

| Field | Meaning |
| --- | --- |
| Confidence | **Confirmed** means the behavior was read in this repository. **Inferred** means a nearby caller makes the behavior likely. **Uncertain** means the implementation was not fully traced. |
| KB Status | Starts as `Not audited`. |
| KB Article URL | Starts blank. |

Knowledge-base comparison target: https://cyberstockroom.helpscoutdocs.com/

Adequate coverage means the article explains what the feature does, how to open it, its options, and the constraints below. A mention is not coverage.

This file is the knowledge-base source for every ID in `SUMMARY.md`. Each feature has a walkthrough: Open, Steps, Options, Result, If it fails, and Do not write. `ALL_FEATURES.md` stays the short index. A control-by-control pass over `_extract/` is still not done. External APIs called out as Uncertain are outside this repo.

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

- **Open:** The account menu in the header, or the mobile **Settings** link. Signed in. Hidden menu items are skipped for that role.
- **Steps:**
  1. Open Settings.
  2. Click **PROFILE & TEAM**, **CUSTOM FIELDS**, **DEFAULT LOCATIONS**, **API & INTEGRATIONS**, **OPTIONS**, or **SUBSCRIPTION**.
  3. The page scrolls to that section. **OPTIONS** is the display settings. Time zone and currency sit further down the same scroll and have no menu item of their own.
- **Options:** Anchors are `profile`, `fields`, `DefaultLocations`, `integrations`, `generalSettings`, and `subscription`. Which items exist depends on the role table at the top of this file.
- **Result:** Scroll position only. Nothing is saved.
- **If it fails:** None.
- **Do not write:** Do not tell a User they can open Subscription, time zone, currency, Share Map Layout, or Lansweeper. Read-only does not get the team section or default locations.
- **Related:** SET-002, SET-003.
- **Code:** `Settings.aspx` 51–87; `js/components/menu.js`; `js/pages/settings.js`; `Settings.aspx.vb` `ShowAllowedMenu` / `ShowAllowedSections`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Settings page sections

### SET-002 — Text fields save on change

- **Open:** Name, email, custom-field names, currency, and the create-field box on Settings.
- **Steps:**
  1. Click the field. The current value is remembered.
  2. Type the new value. The field is marked unsaved.
  3. Press Enter. The field blurs and its change handler saves.
  4. Press Escape instead to put the remembered value back. That does not save.
- **Options:** None. Quantity threshold, max highlight, expiring soon, and currency also save from Enter through `toggle.js`.
- **Result:** The field’s own save runs. Escape leaves the stored value unchanged.
- **If it fails:** The field’s own error, not a shared message.
- **Do not write:** Do not say every Settings control saves on Enter. Display toggles save when they are switched.
- **Related:** SET-003, ACC-009, ACC-010, ACCSET-002, CFL-004.
- **Code:** `js/components/text-input.js`; `js/components/toggle.js`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** How Settings text fields save

### SET-003 — One settings write at a time

- **Open:** Invite, custom-field create, delete, reorder, visibility, personalized sort, and API key create or delete.
- **Steps:**
  1. Start one of those actions.
  2. While it is running, those same controls are disabled.
  3. Wait until it finishes before starting another.
- **Options:** None.
- **Result:** One of those writes at a time.
- **If it fails:** “Another action is currently in progress. Please wait for it to complete.”
- **Do not write:** Profile name, email, password, and the display toggles are not in this lock.
- **Related:** SET-002, TEAM-004, CFL-001, API-001.
- **Code:** `js/business/action-blocking.js`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Why Settings asks you to wait

## ACC — Sign-in and profile

### ACC-001 — Log in with email

- **Open:** `Login.aspx`. Public. An existing session goes to the map.
- **Steps:**
  1. Enter the email. Placeholder `me@email.com`.
  2. Enter the password. Placeholder `***********`.
  3. Submit. On success the session and `csToken` are written and the account is logged in.
- **Options:** None.
- **Result:** The user is signed in. HTTPS is forced.
- **If it fails:** “The email or password is not correct...”
- **Do not write:** None.
- **Related:** ACC-002, ACC-003, ACC-004. WF-009.
- **Code:** `Login.aspx` 169–186; `Login.aspx.vb` `btn_login_Click`, `Page_Init`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Log in to CyberStockroom

### ACC-002 — Log in with Google

- **Open:** The Google button on `Login.aspx`. On an invitation, if the account is `googleOnly`, email, password, login, and forgot-password are hidden. The Google button stays.
- **Steps:**
  1. Click the Google button. It stores the ID token and clicks the hidden Google login button.
  2. On an invitation, a valid token calls `signIn_google` and `Account.LogIn_Google`.
- **Options:** None.
- **Result:** The person is signed in when the token is accepted.
- **If it fails:** A failed token check on the invitation path exits without an on-page message. The ordinary failure sentence was not fully traced past `VerfiyGoogleToken`.
- **Do not write:** Do not invent a Google error sentence for a normal login.
- **Related:** ACC-004, ACC-012.
- **Code:** `Login.aspx` 206–242; `Login.aspx.vb` 185–213, 289.
- **Confidence:** Confirmed for the invitation path. Inferred that the main button posts the same handler.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Log in with Google

### ACC-003 — Forgot password

- **Open:** Forgot password on `Login.aspx`. The reset page is `Login.aspx?PasswordReset={guid}`.
- **Steps:**
  1. Enter the email and request a reset.
  2. The mail comes from `support@cyberstockroom.com` and links to `https://www.cyberstockroom.com/Login?PasswordReset=` plus the GUID.
  3. On the reset page, titled “Reset your password”, the email box is locked. The label is “Pick a New Password”.
  4. Submit. A new salted hash is stored and the person is logged in.
- **Options:** None. This path does not check a minimum length.
- **Result:** The password is replaced and the person is signed in.
- **If it fails:** Unknown email runs an Intercom message “That Email is not in our records...”. A known email runs “An Email has been sent”. An empty new password is not rejected here.
- **Do not write:** Do not say the reset link uses the current website host. That host is hard-coded. Invitation links use the request host.
- **Related:** ACC-001, ACC-011.
- **Code:** `Login.aspx.vb` 122–138, 216–278.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Reset a forgotten password

### ACC-004 — Accept an invitation

- **Open:** `Login.aspx?Invitation={guid}` from the invite email (TEAM-004).
- **Steps:**
  1. Open the link. The title is “Accept your Invitation” and the password label is “Create your password”. The role was chosen by the inviter and is not shown.
  2. Enter a non-blank password and submit. A new-user notification is sent and the person is logged in.
  3. Google acceptance writes email, Google id, name, and Google photo URL.
- **Options:** If `googleOnly` is 1, email and password are hidden.
- **Result:** The person joins the account. The invitation id is not cleared by the SQL that was read. A blank name then opens ACC-007 on the next page other than Settings.
- **If it fails:** Blank password: “Please create a password to accept your invitation.” There is no 6-character minimum on this path. A bad GUID leaves the normal login form.
- **Do not write:** Do not say accepting an invite lets the person pick a role.
- **Related:** TEAM-004, ACC-002, ACC-007. WF-009.
- **Code:** `Login.aspx.vb` 86–213.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Accept a team invitation

### ACC-005 — Choose a plan during signup

- **Open:** `SecureRegistration.aspx` iframes `UpdateAccount.aspx` with no query. `UpdateAccount` redirects to Login when there is no session.
- **Steps:**
  1. During signup, the iframe shows the same monthly and annual checkout as SUB-002.
  2. Choose the monthly or annual image. The enterprise image has no click.
- **Options:** Live price ids are under SUB-002. Dollar amounts are in images, not text.
- **Result:** The same checkout as a plan change.
- **If it fails:** No session sends the iframe to Login.
- **Do not write:** Do not publish a dollar amount. No company-name or seat-count field was found on this page.
- **Related:** SUB-002.
- **Code:** `SecureRegistration.aspx`; `UpdateAccount.aspx.vb` `LoginReplacement`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Choose a plan during signup

### ACC-006 — Welcome page (not a customer step)

- **Open:** `Welcome.aspx`. `Page_Init` redirects to `/Map` and returns.
- **Result:** The map. Profile and demo-data code below the redirect does not run.
- **If it fails:** None.
- **Do not write:** Do not publish Welcome as a setup wizard. There are no steps.
- **Related:** MAP-001.
- **Code:** `Welcome.aspx.vb` 16–28.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Welcome is not a setup wizard

### ACC-007 — Required name

- **Open:** `ProfileRequired.aspx` from the master page when `FirstName` is blank. Not opened on Settings or `?printable=true`.
- **Steps:**
  1. Type a name and pick a profile icon.
  2. Save. The name is validated, then the icon is applied.
  3. The parent reloads, or the browser goes to `/Map` if there is no parent.
- **Options:** Icon rules match ACC-008: png, jpeg, gif, webp, under 3 MB. Presets 1 through 15.
- **Result:** `Users.FirstName` is set and the popup stops appearing.
- **If it fails:** Empty: “Please enter your name.” Over 50 characters: “Please use 50 characters or fewer.” Duplicate on the account: “Someone sharing this account is using this name already...”
- **Do not write:** None.
- **Related:** ACC-008, ACC-009.
- **Code:** `UserPage.master.vb` `OpenProfilePopupIfNameBlank`; `ProfileRequired.aspx.vb` `btn_save_Click`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Enter your name when the app asks

### ACC-008 — Profile picture

- **Open:** The profile icon picker on Settings and on Profile Required.
- **Steps:**
  1. Choose a preset from 1 through 15, or upload a file.
  2. Click Apply.
- **Options:** Default preset is `1`. Accepted types are png, jpeg, gif, and webp. On Settings the picker’s own name box is hidden. The name is ACC-009.
- **Result:** A preset copies `Images/Avatars/{n}.png`. An upload is stored by `ProfileIcons.SaveUpload`.
- **If it fails:** “Please choose an image file.” “Please choose an image under 3 MB.”
- **Do not write:** None.
- **Related:** ACC-007, ACC-009.
- **Code:** `ProfileIconPicker.ascx.vb` `btn_apply_Click`; `ProfileIcons.vb`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Choose a profile picture

### ACC-009 — Your name

- **Open:** Settings profile field `txt_profile_user_name`. Also ACC-007.
- **Steps:**
  1. Change the name.
  2. Leave the field or press Enter (SET-002). Escape restores the focused value and does not save.
- **Options:** Maximum 50 characters. The name must be unique on the account.
- **Result:** `Users.FirstName` is saved. The team card for the current user updates without a full reload. Activity rows and the collapsed menu use this name.
- **If it fails:** “Please enter your name.” “Please use 50 characters or fewer.” “Someone sharing this account is using this name already...”
- **Do not write:** None.
- **Related:** SET-002, ACC-007, ACT-003.
- **Code:** `js/business/profile.js` `updateUserName`; `webAPI/users.aspx.vb` `UpdateUserName`; `User_Legacy.DisplayNameError`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Change your name in Settings

### ACC-010 — Your email

- **Open:** Settings `txt_profile_email`. Google-linked users can still edit email.
- **Steps:**
  1. Change the email and leave the field or press Enter.
  2. The server checks format, uniqueness in this account, uniqueness in any account, and pending invitations.
- **Options:** None.
- **Result:** The user’s email is updated when the checks pass.
- **If it fails:** The input title becomes “That email is invalid or already exists.” The server throws an empty `ArgumentException`.
- **Do not write:** Do not describe the “same as old” check as comparing to the current email. The code compares the new email to `FirstName`. A no-op only happens when the typed email equals the person’s name.
- **Related:** SET-002, ACC-011.
- **Code:** `js/business/profile.js` `updateUserEmail`; `webAPI/users.aspx.vb` `UpdateUserEmail`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Change the email on your user

### ACC-011 — Update your password

- **Open:** Settings profile, **Update Your Password**. Hidden when `GoogleID` is set.
- **Steps:**
  1. Click **Update Your Password**.
  2. Enter the old password, the new password, and the repeat.
  3. Save. Cancel only hides the form.
- **Options:** Minimum 6 characters. The client colors the field (under 6 red, under 9 yellow, 9 or more green) and does not block the postback.
- **Result:** A salted SHA-256 hash is stored. Success returns to `Settings.aspx`. An old unsalted hash is still accepted as the old password.
- **If it fails:** “The password is incorrect. Try Again?” “The passwords don't match. Try Again?” “That password is too short. Please use at least 6 characters. Try Again?” “The new password must be different! Try Again?”
- **Do not write:** Do not tell a Google-linked user to change a password on this page. The form is hidden.
- **Related:** ACC-003, ACC-012.
- **Code:** `Settings.aspx.vb` `btn_password_reset_click`; `SignInApplicationService.ChangePassword`; `js/business/profile.js` `validatePassword`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Update your password

### ACC-012 — Link Google on an existing user

- **Open:** Settings profile, only when `GoogleID` is empty.
- **Steps:**
  1. Click the Google link button.
  2. The token audience is verified and the Google id is stored.
  3. The browser goes to `Settings#profile`. On the next load the password form is gone.
- **Options:** None. The Google email from the token is not written by this click.
- **Result:** The user is linked to Google.
- **If it fails:** A bad token exits with no on-page message. `settings.js` signs the Google JS client out on load.
- **Do not write:** Do not say linking Google changes the CyberStockroom email.
- **Related:** ACC-002, ACC-011.
- **Code:** `Settings.aspx.vb` `btn_google_login_click`; `SignInApplicationService.VerifyGoogleToken`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Link Google to an existing user

### ACC-013 — Role badge

- **Open:** The profile card on Settings, for a role that can see the profile section.
- **Steps:**
  1. Open Settings.
  2. Read the badge: Admin, User, or Read-Only, from the effective type.
- **Options:** None. Display only.
- **Result:** Nothing is saved.
- **If it fails:** None.
- **Do not write:** A Mobile badge exists in markup and is never turned on. Stored Mobile is shown as User. `SUPER_USER` matches no badge and gets no profile section.
- **Related:** TEAM-002.
- **Code:** `Settings.aspx.vb` `_displayGoogleAndAdminBadge`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** What the role badge on your profile means

### ACC-014 — Subscription update confirmation

- **Open:** `SuccessSignup.aspx` after a subscription update. Some `UpdateAccount` branches redirect to `_cvr/SuccessSignup` instead.
- **Steps:**
  1. Finish a plan change that redirects here.
  2. Read “Success!” and “Thank you for Updating your subscription.”
- **Options:** None. No plan name is printed.
- **Result:** A confirmation page only.
- **If it fails:** None.
- **Do not write:** The `_cvr` copy’s exact sentence was not compared. Do not quote it as the same sentence.
- **Related:** SUB-002.
- **Code:** `SuccessSignup.aspx`; `UpdateAccount.aspx.vb` redirect branches.
- **Confidence:** Confirmed for `SuccessSignup.aspx`.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Subscription update confirmation

### ACC-015 — Allow or deny an OAuth connection

- **Open:** `OAuth2/consent.aspx` after a valid OAuth request. A missing user index sends the browser to Login.
- **Steps:**
  1. Read the consent screen. Scope wording is rendered outside this website project.
  2. Click **Allow** to return the user id to the client, or **Cancel** to deny and redirect with an error.
- **Options:** Buttons **Cancel** and **Allow** only.
- **Result:** The client receives an allow or an error. This is not an API key.
- **If it fails:** None on the buttons themselves. A missing user goes to Login.
- **Do not write:** Do not list OAuth scope names. They are not in this repo.
- **Related:** API-001.
- **Code:** `OAuth2/consent.aspx.vb` `consent_allow_Click`, `consent_cancel_Click`.
- **Confidence:** Confirmed for the buttons. Uncertain for scope text.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Allow or deny an OAuth connection

## TEAM — Team members

### TEAM-001 — Team list

- **Open:** Settings, **PROFILE & TEAM**. Admin and User. Read-only does not get this section.
- **Steps:**
  1. Open the team section. Cards sort Admin, then User, then Read-only.
  2. If the unfiltered list is longer than 12, a search box and role pills appear.
  3. Search matches name or email. Placeholder “Search by name or email...”. Pills filter ADMIN, USER, and READ-ONLY. Page size is 12.
- **Options:** Search and pills stay hidden until there are more than 12 people.
- **Result:** A filtered view. Seeing the list does not allow managing it.
- **If it fails:** No matches: “No users found”.
- **Do not write:** A legacy Mobile row is labeled USER. Pending invites with a blank first name still appear if the query returns them.
- **Related:** TEAM-002, TEAM-003, TEAM-004. WF-009.
- **Code:** `Settings.aspx.vb` `InitUsers`; `js/components/user-card.js`; `js/components/filters.js`; `js/components/pagination.js`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Find a teammate in Settings

### TEAM-002 — Change a teammate’s role

- **Open:** The role select on another user’s card. Disabled unless the viewer is Admin. Your own card has no select.
- **Steps:**
  1. Choose `ADMIN`, `USER`, or `READ-ONLY`.
  2. Confirm. `SetUserType` writes `TypeOfUser`.
  3. Cancel does not post.
- **Options:** Those three roles. There is no Mobile option.
- **Result:** The person’s role changes. Nothing in this method keeps at least one admin.
- **If it fails:** The server rejects `MOBILE` with “MOBILE role is no longer supported.” A failed post reloads the cards from the last JSON.
- **Do not write:** Do not say the last admin is protected. The method that was read does not compare the target account id to the caller’s account.
- **Related:** TEAM-001, ACC-013. WF-009.
- **Code:** `js/business/users.js`; `webAPI/users.aspx.vb` `SetUserType`; `js/components/user-card.js`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Change a teammate’s role

### TEAM-003 — Remove a teammate

- **Open:** **DELETE** on another user’s card. Shown only when the viewer is Admin and the card is not themselves.
- **Steps:**
  1. Click **DELETE**.
  2. Confirm “Are you sure you want to delete the user …”.
- **Options:** None.
- **Result:** That user row is deleted. If it was the last card on a page, the list moves to the previous page.
- **If it fails:** None beyond cancelling the confirm.
- **Do not write:** Do not say the last admin cannot be removed.
- **Related:** TEAM-001. WF-009.
- **Code:** `js/business/users.js` `deleteUser`; `webAPI/users.aspx.vb` `DeleteUser`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Remove a teammate

### TEAM-004 — Invite a teammate

- **Open:** Settings, **Invite a Team Member**. The form is visible to Admin and User. The API allows admins only.
- **Steps:**
  1. Enter an email. Placeholder `example@company.com`.
  2. Choose a role. The first option, and the unmarked default, is `ADMIN`. Choices are `ADMIN`, `USER`, and `READ-ONLY`.
  3. Send. The mail is from `admin@cyberstockroom.com`, subject “{inviter name} is inviting you to CyberStockroom. Details Inside.”, and links to `Login.aspx?Invitation={guid}`.
- **Options:** The stored invited name is an empty string until they accept.
- **Result:** A new invitation GUID is stored. Map coordinates are copied from the inviter with the share-map marker stripped. `SHOW_EXPIRATIONS` is copied. Onboarding flags are set to finished.
- **If it fails:** Empty: “Please enter an email address.” Bad pattern: “Please enter a valid email address.” A User who clicks gets “Unable to Invite - Try Again?”
- **Do not write:** If this account already has that email, the update does not change `TypeOfUser`. If the email exists only on another account, the create function returns without inserting, but the send function can still run and the button can say “Send Another Invitation”. Do not promise a role change for an existing teammate.
- **Related:** ACC-004, DSP-001. WF-009.
- **Code:** `js/business/invitations.js`; `webAPI/invitations.aspx.vb` `SendInvitation`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Invite a teammate and choose their role

## CFL — Custom fields

A custom field is a named text field, optionally with a preset list. There is no date, number, or dropdown field type. Names and presets are account-wide. Order, price visibility, and personalized sort are stored on the current user. Create, rename, delete, and presets require Admin. Reorder and price visibility allow Admin, User, and Read-only.

### CFL-001 — Personalized sort

- **Open:** Settings custom fields, and the custom-field modal on product pages.
- **Steps:**
  1. Turn personalized sort on.
  2. Up and down buttons appear, including on Buy Price and Sell Price.
  3. Move the fields. The order is saved for this user.
  4. Turn it off to return the Settings list to the default order. The saved order is not deleted.
- **Options:** Default is off when the coordinate token is absent.
- **Result:** This user’s field order. When off, the Settings list hides the Buy Price and Sell Price cards.
- **If it fails:** “Unable to save the personalized sort preference right now.” The toggle reverts.
- **Do not write:** Do not say turning it off erases the saved order. A new field is appended the next time a personalized list is normalized.
- **Related:** CFL-002, CFL-003.
- **Code:** `js/business/custom-fields.js` `handlePersonalizedSortToggle`; `webAPI/settings.aspx.vb` `SaveCustomFieldOrder`; `Gridster_Utilities.NormalizeCustomFieldOrder`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Turn on a personal custom-field order

### CFL-002 — Show or hide Buy Price and Sell Price

- **Open:** The Buy Price and Sell Price cards. They are omitted from the Settings list until personalized sort is on (CFL-001). In the product modal, a hidden price field is a compact row with Show.
- **Steps:**
  1. Turn personalized sort on so the cards appear in Settings.
  2. Use Show on Buy Price or Sell Price.
- **Options:** Default is visible when the hide token is absent. Card subtitle is “DEFAULT”. Names are not editable. There is no delete button.
- **Result:** `showBuyPrice` / `showSellPrice` for this user. The map and editors read the same flags.
- **If it fails:** “Unable to save the field visibility right now.”
- **Do not write:** Do not tell someone to hide prices from Settings while personalized sort is off. The cards are not there.
- **Related:** CFL-001, PED-001, MAP-025.
- **Code:** `js/business/custom-fields.js` `toggleSpecialFieldVisibility`; `Gridster_Utilities.GetShowBuyPriceFromRaw`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Show or hide Buy Price and Sell Price

### CFL-003 — Add a custom field

- **Open:** **Create New Field...** under the list, on Settings and in the product-page modal. Admin only.
- **Steps:**
  1. Type a name.
  2. Create the field. It is inserted and a new `CF_Index` is returned.
- **Options:** The new card starts with `validValues: [""]`, which is not a preset.
- **Result:** An account-wide text field with no presets.
- **If it fails:** None. There is no empty-name or duplicate-name check in `CreateNewCustomField`.
- **Do not write:** Do not say duplicate names are rejected.
- **Related:** CFL-004, CFL-006, SET-003.
- **Code:** `js/business/custom-fields.js` `createNewCustomField`; `webAPI/customFields.aspx.vb` `CreateNewCustomField`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Add a custom field

### CFL-004 — Rename a custom field

- **Open:** The name on a custom-field card. Admin. Buy Price and Sell Price inputs are read-only for everyone.
- **Steps:**
  1. Change the name.
  2. Leave the field or press Enter. `RenameCustomField` runs.
- **Options:** None.
- **Result:** The account-wide label changes.
- **If it fails:** None. There is no length or uniqueness check in the web method.
- **Do not write:** Do not say Buy Price or Sell Price can be renamed here.
- **Related:** CFL-003, SET-002.
- **Code:** `webAPI/customFields.aspx.vb` `RenameCustomField`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Rename a custom field

### CFL-005 — Delete a custom field

- **Open:** Delete on a custom-field card. Admin. Buy Price and Sell Price cannot be deleted here.
- **Steps:**
  1. Click delete.
  2. Confirm the warning, which says existing data for the field will be erased and recommends exporting inventory first.
- **Options:** None.
- **Result:** The field definition is deleted.
- **If it fails:** Cancel leaves the field.
- **Do not write:** The warning says values are erased. The repository cascade was not read. Do not describe which tables are cleared beyond that warning.
- **Related:** CFL-003, RPT-001.
- **Code:** `webAPI/customFields.aspx.vb` `DeleteCustomField`.
- **Confidence:** Confirmed for the button and the warning. Uncertain for the cascade.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Delete a custom field

### CFL-006 — Preset choices

- **Open:** **Presets** on a Settings custom-field card. Admin. Opens `Popups/FixedMultiFields.aspx?id={CF_Index}`. The product-page modal does not show Presets.
- **Steps:**
  1. Click **Presets**.
  2. Enter the allowed values. Blank values are stripped.
  3. Optional: check “allow other”. That appends `Other (Specify)` only when at least one real preset remains.
  4. Save. An empty save leaves the field as a normal text field.
- **Options:** “allow other”. Commas in stored presets become underscores.
- **Result:** Saved non-blank values become `validValues`. A field counts as having presets when any value is non-blank and is not `Other (Specify)`.
- **If it fails:** None shown for a rejected preset on this popup.
- **Do not write:** Closing the popup does not refresh Settings (`afterClose` is empty). `SavePresets` itself was not given a role check in the application service that was read. Do not say the product modal can edit presets.
- **Related:** CFL-003, PED-001.
- **Code:** `Popups/FixedMultiFields.aspx.vb` `SavePresets`; `CustomFieldApplicationService.SavePresets`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Add preset choices to a custom field

## DEF — Default locations

Per user. Admin and User. Read-only is redirected to `/_admin/_unauthorized` if they open the picker directly. Clear stores location id `-2`, displayed as `(none)`.

### DEF-001 — Default check-in location

- **Open:** Settings, **Default Check-In Location**. Opens `_locationSelectorToggle.aspx?type=defaultcheckin`.
- **Steps:**
  1. Click **Default Check-In Location**. The header is “Select Default Check-In Location”.
  2. Pick a location and click Save, or click `CLEAR Selection`.
- **Options:** Clear stores `-2`, shown as `(none)`.
- **Result:** `CheckInLocationDefault` is updated. The popup sets `cookie_refresh_settings=TRUE`, and Settings reloads the label.
- **If it fails:** None beyond the read-only redirect.
- **Do not write:** None.
- **Related:** DEF-002, XFR-007, XFR-009. WF-001.
- **Code:** `_locationSelectorToggle.aspx.vb` `save_defaultCheckin`; `Settings.aspx.vb` `InitDefaultLocations`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Set your default check-in location

### DEF-002 — Default check-out location

- **Open:** Settings, **Default Check-Out Location**. Query `type=defaultcheckout`.
- **Steps:**
  1. Click **Default Check-Out Location**.
  2. Pick a location and Save, or clear the selection.
- **Options:** Clear stores `-2`, shown as `(none)`.
- **Result:** `CheckOutLocationDefault` is updated, and Settings reloads the same way as DEF-001.
- **If it fails:** None beyond the read-only redirect.
- **Do not write:** None.
- **Related:** DEF-001, XFR-002. WF-003.
- **Code:** `_locationSelectorToggle.aspx.vb` checkout save.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Set your default check-out location

## API — API keys

### API-001 — Create and delete an API key

- **Open:** Settings, **API Keys**. The section is visible to Admin, User, and Read-only. The manager appears only when the account is on `CS_API_v0._betaList`.
- **Steps:**
  1. If the account is not on the beta list, the page says to email support@cyberstockroom.com. Stop there.
  2. Enter a key name and click **+ Create New API Key**.
  3. Copy the plaintext from the prompt. It is shown once: “This is the only time this API key will be shown. Please copy and store it safely:”.
  4. Later loads show a truncated display and an issued date (`MMM d, yyyy`).
  5. Delete revokes that key after a confirm that access is revoked immediately.
- **Options:** Name. Names longer than 30 characters display with `...`. The full name is the tooltip.
- **Result:** A key is created or revoked. Create and delete allow every role at the API. Delete also requires the key to belong to the caller’s own key list.
- **If it fails:** Empty name: “Please enter a valid key name”. Create failure: “Error creating API key. Please try again.”
- **Do not write:** A non-beta caller who posted `CreateNewKey` directly is not stopped by `_isBetaUser`. Do not document that as a customer path. Non-beta text: “The CyberStockroom API is currently available to select users only. You can request access by emailing us at support@cyberstockroom.com”.
- **Related:** API-002, SET-003, ACC-015.
- **Code:** `ApiKeyApplicationService.vb`; `js/business/api-keys.js`; `webAPI/apiKeys.aspx.vb`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Create and delete an API key

### API-002 — API documentation link

- **Open:** Under the API key area, including accounts that are not on the beta list.
- **Steps:**
  1. Click **Read API Documentation**.
  2. A new tab opens `https://documenter.getpostman.com/view/1256102/2sB34ZqPYv`.
- **Options:** None.
- **Result:** The documentation site. Nothing is saved.
- **If it fails:** None.
- **Do not write:** None.
- **Related:** API-001.
- **Code:** `Settings.aspx` 373.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Open the CyberStockroom API documentation

## LSW — Lansweeper

### LSW-001 — Request the integration

- **Open:** The Lansweeper heading on Settings. Admin only. Users see the API section from the same menu icon and do not see this heading.
- **Steps:**
  1. Read “The Lansweeper Integration is available by request. If you'd like to conenct your Lansweeper account please email us at support@cyberstockroom.com to schedule a call.”
  2. Email support. There is no Connect button on the live page.
- **Options:** None.
- **Result:** No Lansweeper data changes from this block.
- **If it fails:** None.
- **Do not write:** Do not correct the typo “conenct” as if the product said “connect”, and do not document Synchronize or Disconnect. `InitLansweeper` is commented out and those buttons are inside a server comment.
- **Related:** LSW-002, PED-004.
- **Code:** `Settings.aspx` 386–407; `Settings.aspx.vb` line 53.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Request the Lansweeper integration

### LSW-002 — Choose sites (not linked from current Settings)

- **Open:** Direct URL `pages/settings/popups/lansweeperSiteSelector.aspx` only. No live Settings link.
- **Steps:**
  1. Check the sites to include.
  2. Click Connect. Checked site uid and name are saved and the success popup opens. Zero checked sites goes to `/Settings`.
- **Options:** “Only sites that contain assets will be synchronized. Some demo sites may not be permitted.”
- **Result:** The selected sites are stored, then the success popup.
- **If it fails:** A load exception goes to `lansweeperConnectionFailure?source=siteSelector`. Text: “There was a problem connecting your Lansweeper Account.”
- **Do not write:** Do not publish this as a step in Settings. It is not linked.
- **Related:** LSW-001, LSW-005.
- **Code:** `lansweeperSiteSelector.aspx.vb` `btn_connect_Click`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Choose which Lansweeper sites to sync

### LSW-003 — Match a Lansweeper field (not linked)

- **Open:** Direct URL `lansweeperFieldToggle.aspx`. Not linked from Settings.
- **Steps:**
  1. The header is “Select a Field to Match: '{name}'”.
  2. Pick one of this account’s custom fields (`CF_Index` / `fieldName`).
  3. The selection sets `cookie_refresh_settings` and closes the fancybox.
- **Options:** The account’s custom fields. Do not invent field names.
- **Result:** The popup closes. How the pairing is stored was not opened.
- **If it fails:** None traced.
- **Do not write:** Do not publish the stored mapping. It is Uncertain, and the page is not linked from Settings.
- **Related:** CFL-003, LSW-001.
- **Code:** `lansweeperFieldToggle.aspx.vb`.
- **Confidence:** Confirmed for the option list. Uncertain for the stored mapping.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Match a Lansweeper field to a custom field

### LSW-004 — Match a category to a location (not linked)

- **Open:** `_locationSelectorToggle.aspx?type=lansweeper` only. Live Settings hrefs are `defaultcheckin` and `defaultcheckout`. Read-only is redirected.
- **Steps:**
  1. The header is “Select a Location to Match: '{name}'”.
  2. Save replaces a tag on the location. Clear calls the same save with the clear flag.
- **Options:** The account’s locations.
- **Result:** A location tag is replaced.
- **If it fails:** None traced beyond the read-only redirect.
- **Do not write:** Do not publish this as the default-location picker (DEF-001, DEF-002).
- **Related:** DEF-001, LSW-001.
- **Code:** `_locationSelectorToggle.aspx.vb` `save_lansweeper`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Match a Lansweeper category to a location

### LSW-005 — Link, sync, and progress (not linked from current Settings)

- **Open:** Direct URLs for link-and-sync, connection success, and connection failure. Not linked from the live Settings page.
- **Steps:**
  1. If progress is 0, link-and-sync sets “Preparing to Synchronize...” at 1%, calls link and synchronize, and writes `ColumnOrder`.
  2. The success popup shows progress and status.
  3. At 100% it waits 1.5 seconds and goes to `/Map`. A second synchronize is skipped when progress is already not 0.
- **Options:** None on the live Settings page.
- **Result:** Worker rows can be inserted by `SyncAllSites`, which the commented Settings button would call. The live page does not call it.
- **If it fails:** Failure popup text is on LSW-002’s failure page.
- **Do not write:** Two code-behind files declare the class `pages_settings_popups_lansweeperConnectionSuccess`. Which file the compiler binds was not verified. Do not publish this as a Settings button.
- **Related:** LSW-001, LSW-002.
- **Code:** `lansweeperLinkAndSync.aspx`, `lansweeperConnectionSuccess.aspx`, `lansweeperConnectionFailure.aspx`; `LansweeperApplicationService.SyncAllSites`.
- **Confidence:** Confirmed for the methods read. Uncertain for the duplicate class.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Lansweeper sync progress is not on Settings

## DSP — Display settings

Per user unless noted. Admin, User, and Read-only. A failed toggle reverts after 1.5 seconds. Share Map Layout is the admin-only row.

### DSP-001 — Share Map Layout

- **Open:** Settings, **OPTIONS**, **Share Map Layout**. Admin only.
- **Steps:**
  1. Turn **Share Map Layout** on.
  2. Teammates can then list this layout and copy it (MAP-016). They cannot change the shared original.
- **Options:** Default is off when the marker is absent. The stored marker is `-16,CS_MAP_SHAREABLE_ON`.
- **Result:** This admin’s layout can be copied. Inventory is not shared. An invite copies coordinates with the marker stripped (TEAM-004).
- **If it fails:** The toggle reverts after 1.5 seconds on a failed save.
- **Do not write:** Do not say sharing copies products or quantities.
- **Related:** MAP-016, TEAM-004. WF-010.
- **Code:** `webAPI/settings.aspx.vb` `SaveShareMapLayout`, `GetSharedMaps`; `Settings.aspx` 444–446.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Share your map layout with the team

### DSP-002 — Product Images

- **Open:** Settings, **OPTIONS**, product images toggle.
- **Steps:**
  1. Turn product images on or off.
  2. Open the product list. Image cells appear only when the flag is on.
- **Options:** The stored property is spelled `SHOW_PRORDUCT_IMAGES`.
- **Result:** `SHOW_PRODUCT_IMAGES` for this user.
- **If it fails:** The toggle reverts after 1.5 seconds.
- **Do not write:** None.
- **Related:** PRD-009.
- **Code:** `webAPI/settings.aspx.vb` `ShowProductImages`; `Products.aspx.vb` `StylingRefresh`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Show product images in the product list

### DSP-003 — Zero Quantity Products

- **Open:** Settings, **OPTIONS**, zero-quantity toggle.
- **Steps:**
  1. Turn the toggle off to hide products whose quantity is 0.
  2. Turn it on to include them in the product grid.
- **Options:** None.
- **Result:** `SHOW_ZERO_QUANTITY` for this user. The products grid skips zero rows when it is off.
- **If it fails:** The toggle reverts after 1.5 seconds.
- **Do not write:** The sentence “Locations with 0 quantity will appear in white on the map” belongs to DSP-006, not this toggle.
- **Related:** PRD-001, DSP-006.
- **Code:** `webAPI/settings.aspx.vb` `ShowZeroQuantityProducts`; `Products.aspx.vb` around 1846.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Include products with zero quantity

### DSP-004 — Expirations

- **Open:** Settings, **OPTIONS**, expirations toggle.
- **Steps:**
  1. Turn expirations on. The Expirations menu appears, and the map popup can include expiration.
  2. Turn it off. The Expiring Soon block in Settings hides. The window is not by itself written to 0.
- **Options:** Per user, `SHOW_EXPIRATIONS`. New invites copy the inviter’s flag (TEAM-004).
- **Result:** This user sees or hides expiration tools.
- **If it fails:** The toggle reverts after 1.5 seconds.
- **Do not write:** None.
- **Related:** DSP-005, EXP-001, PED-005. WF-011.
- **Code:** `webAPI/settings.aspx.vb` `ShowExpirations`; `UserPage.master.vb` 66–68.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Turn expiration dates on or off

### DSP-005 — Expiring Soon

- **Open:** Settings, under Options, only while expirations are on (DSP-004).
- **Steps:**
  1. Turn the expiring-soon toggle on. An empty value saves 60 days.
  2. Enter a number of at least 1 and choose days, weeks, months, or years.
  3. Save. Weeks are stored as ×7, months as ×30, years as ×365.
- **Options:** Markup default is 60 days. Stored `-1` is on at 60. Stored `0` is off. Exact multiples display as the larger unit (14 days shows as 2 weeks, 30 days as 1 month). Helper: “Highlight products expiring within this period”.
- **Result:** Coordinate token `-18` and `hidden_EXPIRING_SOON_DAYS` on the map.
- **If it fails:** “Enable Expirations before using Expiring Soon.” “Expiring soon window must be a valid duration greater than 0.” “Error saving expiring soon window. Please try again.”
- **Do not write:** Do not say a month is a calendar month. It is 30 days. A year is 365 days.
- **Related:** DSP-004, EXP-001, MAP-019. WF-011.
- **Code:** `js/business/general-settings.js`; `webAPI/settings.aspx.vb` `SaveExpiringSoonWindow`; `Gridster_Utilities.vb`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Set the expiring-soon highlight window

### DSP-006 — Quantity Threshold

- **Open:** Settings, **OPTIONS**, quantity threshold.
- **Steps:**
  1. Turn the toggle on. It saves 1 immediately.
  2. Enter a number bigger than 0. Copy: “Highlight locations with quantity at or below:”.
- **Options:** Off stores 0. If a value greater than 0 is stored, the box shows it and is enabled. Otherwise the toggle is off and the box shows `1` disabled. Locations with quantity 0 stay white.
- **Result:** `_generalThreshold` for this user. The map uses it for low-quantity color (MAP-019).
- **If it fails:** “The threshold must be a valid number bigger than 0.” “Error saving threshold value. Please try again.”
- **Do not write:** Do not attach the white-location sentence to the zero-quantity product toggle (DSP-003).
- **Related:** DSP-007, MAP-019.
- **Code:** `webAPI/settings.aspx.vb` `ShowGeneralThreshold`; `Map_CONTROL_2017.ascx.vb` around 141–150.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Highlight low quantities on the map

### DSP-007 — Max Highlight

- **Open:** Inside the quantity-threshold details. Available only while Quantity Threshold is on.
- **Steps:**
  1. Turn Quantity Threshold on.
  2. Turn max highlight on and enter a number greater than the threshold. Copy: “Highlight locations with quantity at or above:”.
- **Options:** When nothing is stored, the toggle is off and the box shows `10`. Off stores 0.
- **Result:** Locations at or above this number use the max color (MAP-019).
- **If it fails:** “Enable Quantity Threshold before using Max Highlight.” “Max highlight must be a valid number greater than 0.” “Max highlight must be greater than the quantity threshold.” “Error saving max highlight. Ensure it is greater than the quantity threshold.” If validation fails after the toggle was disabled, the control can stay disabled until reload.
- **Do not write:** None.
- **Related:** DSP-006, MAP-019.
- **Code:** `webAPI/settings.aspx.vb` `SaveMaxHighlight`; `js/business/general-settings.js` `handleMaxHighlightToggle`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Highlight high quantities on the map

### DSP-008 — Kitting toggle (not a feature)

- **Open:** The row exists in Settings markup and is `display: none`. Nothing initializes it.
- **Result:** Nothing is saved from this row.
- **If it fails:** None.
- **Do not write:** Do not publish Kitting as a Settings option. There are no steps. `SHOW_KITTING` can still show the Products-menu Kitting icon. How that flag is turned on was not found in Settings.
- **Related:** KIT-001. WF-012.
- **Code:** `Settings.aspx` 526–536; `UserPage.master.vb` 70–72.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Kitting is not a Settings switch

## ACCSET — Account settings

Admin only. Both values are account-wide. Fallback when the account row cannot be read: currency `$`, time zone `-5`.

### ACCSET-001 — Time zone

- **Open:** Settings, below Options. Admin only. No menu item of its own (SET-001).
- **Steps:**
  1. Open the time zone dropdown.
  2. Choose an offset. It saves on change. “Saved ✓” shows for about 2 seconds.
- **Options:** Integer offsets from `-12` through `13`. Two labels share value `5`: “(GMT+05:00) Yekaterinburg” and “(GMT+05:00) Islamabad, Karachi, Tashkent”. There is no half-hour offset.
- **Result:** `Accounts.TimeZone`. Activity timestamps use this offset.
- **If it fails:** “Error saving timezone. Please try again.”
- **Do not write:** Do not offer half-hour zones.
- **Related:** ACT-001, SET-001.
- **Code:** `webAPI/settings.aspx.vb` `SetTimeZone`; `js/business/general-settings.js` `handleTimezoneSave`; `Settings.aspx` 631–657.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Set the account time zone

### ACCSET-002 — Currency symbol

- **Open:** The currency box on Settings. Admin only.
- **Steps:**
  1. Type any symbol. The markup default is `$`, replaced on load by the stored value.
  2. Save or press Enter.
- **Options:** Any non-empty string. This is not a currency-code list. Fallback `$`.
- **Result:** `Accounts.Currency`. Product headers use it. The subscription card does not.
- **If it fails:** “Please enter a currency symbol”. “Error saving currency symbol. Please try again.”
- **Do not write:** Do not say this changes the subscription amount format. That uses the subscription record.
- **Related:** PRD-003, SUB-001, SET-002.
- **Code:** `webAPI/settings.aspx.vb` `SetCurrencySymbol`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Set the currency symbol

## SUB — Subscription and billing

Admin section. Plan labels: `STANDARD` shows the plan name with no badge. `CUSTOM` shows “Custom Plan” and badge “Custom”. `ENTERPRISE` shows “Enterprise Plan”. `LEGACY` shows “Legacy Plan”. Payment method labels: Cheque → “Bank Cheque”. Coupa → “Coupa (Payment Platform)”. Direct bank transfer → “Direct Bank Transfer”. PayPal card, PayPal invoice, or Stripe invoice → “Online Invoice”. Stripe card → “Credit Card (Stripe)”. Anything else → “(None)”. `IsAnnual` true is “Annually”. False is “Monthly”.

### SUB-001 — Subscription summary

- **Open:** Settings, **SUBSCRIPTION**. Admin.
- **Steps:**
  1. Open Subscription.
  2. Read the plan name, billing amount, frequency, payment method, and card or contact details.
- **Options:** Amount uses `$` plus the code for USD or CAD, and the code then the amount for other currencies. A missing amount omits the row.
- **Result:** A display of the stored subscription. Nothing is changed.
- **If it fails:** Empty state: “No Active Subscription”, “You don't have an active subscription. Subscribe to a plan to get started.”, and **Subscribe to a Plan** linking to `UpdateAccount?Update=Plan`.
- **Do not write:** Do not publish a price table. This view does not contain one.
- **Related:** SUB-002, ACCSET-002.
- **Code:** `js/business/subscription.js` `loadSubscription`; `SubscriptionApplicationService.vb`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Read your subscription on the Settings page

### SUB-002 — Change a Stripe subscription

- **Open:** **Update Plan**, **Change Card**, **Cancel Subscription**, and **Billing History** appear only when the payment-method string contains “Stripe”. That includes “Credit Card (Stripe)”. “Online Invoice” does not.
- **Steps:**
  1. Click **Update Plan**. `UpdateAccount?Update=Plan` opens. Monthly uses price id `price_1O6zRX4D3SV7Y45Utyewx37h`. Annual uses `price_1O6zS34D3SV7Y45UCZ8p3YaG`. `test_ON` is false. The enterprise image has no click.
  2. If a card is already on file and `stripe_payment_skip` is `1`, the plan updates without a new checkout. Otherwise Stripe checkout runs.
  3. **Change Card** opens `UpdateAccount?Update=Payment`, which calls `updatePayment()` on first load.
  4. **Cancel Subscription** asks “Are you sure you want to cancel your subscription?” with **Cancel Subscription** and **Keep Subscription**.
- **Options:** Monthly or annual image. Do not publish a dollar amount. The prices are in the images.
- **Result:** Cancel sets `ConfirmedPayment` to 0, deletes the `StripeAccounts` row, and calls `stripeRegistrar.deleteSubscription`. The 14-day trial rule applies again. An account older than 14 days is sent back to Settings.
- **If it fails:** Other payment methods show “Please contact admin@cyberstockroom.com to change your subscription or payment method”. Stripe footnote: “For any billing questions please contact admin@cyberstockroom.com”.
- **Do not write:** Do not say PayPal or Stripe-invoice subscriptions get these buttons. `UpdateAccount` blocks read-only only. It does not require Admin. Cancel and billing history do require Admin.
- **Related:** SUB-001, SUB-003, SUB-004, ACC-005, ACC-014.
- **Code:** `js/business/subscription.js`; `webAPI/subscription.aspx.vb` `CancelSubscription`; `UpdateAccount.aspx` 101–139 and 414–449.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Change, cancel, or review a Stripe subscription

### SUB-003 — Billing history

- **Open:** **Billing History** from a Stripe subscription (SUB-002), or `BillingHistory.aspx`. Admin. Other roles go to `/_admin/_unauthorized`.
- **Steps:**
  1. Open billing history.
  2. Read the charges table: Date (`MMM dd, yyyy`), Amount (charge amount / 100), Subscription (invoice plan name plus description, cut off at `@`), Status Successful or Failed.
  3. Next payment uses the first subscription’s period end and plan amount / 100.
- **Options:** None.
- **Result:** A list of charges. An invoice table is built and not added to the page.
- **If it fails:** Any exception replaces the table with “No billing history to show...” and hides next payment.
- **Do not write:** Do not describe an invoice table. It is not shown.
- **Related:** SUB-002.
- **Code:** `BillingHistory.aspx.vb`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Read billing history

### SUB-004 — Trial end and failed payment

- **Open:** Automatic. There is no button.
- **Steps:**
  1. An unpaid trial lasts 14 days from `Accounts.DateCreated` while `ConfirmedPayment` is 0.
  2. When that trial is expired and `SuppressUpgradeAlert` is false, every signed-in page except Settings redirects to `/Settings`.
  3. When `ConfirmedPayment` is 1, the Stripe customer is delinquent, and `SuppressPaymentAlert` is false, the same redirect happens.
- **Options:** The suppress flags are account columns. No Settings control edits them.
- **Result:** The person can still open Settings. They are not automatically shown the plan popup.
- **If it fails:** None. The redirect is the behavior.
- **Do not write:** Settings contains “Your free trial has expired. Please select a plan to continue..”, “You have exceeded the capacity of your current plan. Please upgrade to continue.”, and “Your payment method needs to be updated!” CSS hides all three. `ToggleExpiry`, `ToggleUpgrade`, and `TogglePayment` are not called. Do not document a plan-capacity limit or a banner the user can see. In `UpdateAlert.aspx`, the trial sentence is unreachable because the branch assigns `UpdateType = "CC_Error"`.
- **Related:** SUB-002, SET-001.
- **Code:** `BillingAccessGate.vb`; `Account.vb` 889–901; `css/pages/settings.css` 113–118; `js/business/subscription.js` 5–38; `UpdateAlert.aspx`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** What happens when a trial ends

## MAP — Map and locations

Layout is per user in `GridsterCoordinates2017`. The live map is `Map_CONTROL_2017` on `Map.aspx`. There is no right-click menu and no free resize. The map is locked by default. Location `-2` is All Locations. Location types are 0–8. `Mobile/Map.aspx`, `Mobile/ProductEditorMap.aspx`, `mapDashboardTest.aspx`, `Map_CONTROL_MOBILE_2018`, `CS_Map.vb`, and `GridsterFunctions.vb` are not reachable customer UI. A phone still uses the 2017 control. Compact tile sizes are compiled and skipped (`_setGridsterSize(0)`, comment “Compact Features Not yet released”).

Read-only users are redirected from `Map.aspx` to `Map_read_only.aspx`. A non-read-only user who opens the read-only page is sent back to `/Map`.

### MAP-001 — Open the inventory map

- **Open:** Main menu **Map** (`simpleRedirect('Map')`). Signed in, and not read-only. A read-only user is sent to the read-only map (MAP-002). A signed-out user is sent to Login.
- **Steps:**
  1. Sign in as a user who is not read-only.
  2. Click **Map**.
  3. The page loads every location. Primary locations (children of All Locations, id `-2`) are placed from this user’s saved coordinates. Nested locations are drawn inside their parent. The map type is 1 (designer). The stage stays covered until layout finishes, then it is revealed.
- **Options:** None. There is no right-click menu and no resize handle.
- **Result:** This user’s layout only. Inventory is unchanged.
- **If it fails:** `[Map] Gridster init failed` is logged, and the stage still tries to reveal.
- **Do not write:** `Mobile/Map.aspx` is not the map. Its code-behind always redirects to `/_admin/_unauthorized`. The 2018 control, `mapDashboardTest.aspx`, `CS_Map.vb`, and `GridsterFunctions.vb` are not customer UI. Compact sizes 40, 25, and 15 are not selected.
- **Related:** MAP-002, MAP-008, MAP-009, MAP-044. WF-006.
- **Code:** `UserPage.master` menu **Map**; `Map.aspx.vb` `Page_Init` lines 8–16; `Map_CONTROL_2017.ascx.vb` `Page_Load` login redirect and `_setGridsterSize(0)` lines 119–136 and 230; Gridster init log `Map_CONTROL_2017.ascx` line 7973.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Open the inventory map

### MAP-002 — Read-only map

- **Open:** Automatic when a read-only user opens Map. Anyone else who opens `Map_read_only.aspx` is sent to `/Map`. Map type is 4.
- **Steps:**
  1. Sign in as read-only. The app opens the read-only map instead of the designer map.
  2. Hover a location. The strip shows View (tooltip “View the products in this location...”), then **More actions** (›). Inside more: **V** and **3D** when those controls are drawn, and “View Location Details...”.
  3. Click the location. The product peek still opens (MAP-024).
  4. Click View. The page stores `LocationID_VIEW` and opens Products_read_only.
- **Options:** None. The floating **+** (title “Create a new location...”) is hidden.
- **Result:** The same canvas and this user’s coordinates. No inventory change from viewing.
- **If it fails:** None.
- **Do not write:** A diamond move handle is still rendered for the read-only map. Drag is not separately cancelled. Do not publish “read-only users cannot drag” or “read-only users can rearrange the map” as a settled rule.
- **Related:** MAP-001, MAP-024, MAP-027, MAP-028, MAP-029, MAP-038.
- **Code:** `Map_read_only.aspx.vb` lines 11–20; `Map_Styling.vb` `GetLocationHoverDiv` lines 169–210; floating add hidden for map types 2, 4, and 5 in `Map_CONTROL_2017.ascx.vb`; move handle `Gridster_Utilities.OpenGridsterItem` lines 101–104.
- **Confidence:** Confirmed for the redirect and the hover. Inferred for whether the move handle still drags.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Use the read-only inventory map

### MAP-003 — Location types

- **Open:** The type is chosen when a location is created (MAP-005 or MAP-043). The editor shows the type image. No control was found that changes the type after create.
- **Steps:**
  1. Start a new location.
  2. On the designer map the choices are **BUILDING**, **WAREHOUSE**, **STORE**, **FLOOR**, **ROOM**, **CLOSET**, **SHELF**, **BIN**, and **VEHICLE**.
  3. On the mobile home the same nine choices are labeled **Building**, **Warehouse**, **Store**, **Floor**, **Room**, **Closet**, **Shelf**, **Bin**, and **Vehicle**.
  4. The stored type is 0 Building, 1 Warehouse, 2 Store, 3 Floor, 4 Room, 5 Closet, 6 Shelf, 7 Bin, 8 Vehicle. Anything else is named “Location”.
- **Options:** 0 Building, 1 Warehouse, 2 Store, 3 Floor, 4 Room, 5 Closet, 6 Shelf, 7 Bin, 8 Vehicle. A missing type on the editor’s create path defaults to 0. A missing parent defaults to `-2` (All Locations).
- **Result:** The integer is stored on the location and picks the location image. Inventory is unchanged.
- **If it fails:** Mobile create rejects a type outside 0–8 with “Invalid location type.”
- **Do not write:** Do not publish a step that changes a location’s type after it exists.
- **Related:** MAP-005, MAP-007, MAP-043. WF-006.
- **Code:** `Location.GetLocationTypeName` lines 521–543; toolbox `Map_CONTROL_2017.ascx` lines 15905–15958; `mobile_main.aspx` lines 2913–2923; `MobileCreateLocationHandler.vb` lines 64.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Location icons and types

### MAP-004 — Quantity labels on tiles

- **Open:** Every map type draws this when the map loads. No button.
- **Steps:**
  1. Open the map.
  2. A location with its own quantity greater than 0 is drawn full.
  3. A location with zero of its own and quantity only in children is ghosted. A 3D parent is the exception: it is drawn full, including when its own quantity is 0, and it gets a sloped bottom edge. That slope has no text. The word **3D** is the hover and footer control (MAP-029), not a badge printed on the tile.
  4. On a primary tile the count reads `own (children)` when both are greater than 0, the own number when only the location itself has quantity, `(children)` when only children have quantity, and nothing when both are 0.
  5. A nested tile shows its own quantity only. A nested 3D parent with no quantity of its own and quantity in children shows `(children)`.
  6. Dragging that tile for check-out, transfer, or Ctrl+drop requires its own quantity greater than 0. Child stock alone does not make it draggable, including a 3D parent that only looks full because of children.
- **Options:** None.
- **Result:** Display only. Inventory is unchanged.
- **If it fails:** None.
- **Do not write:** Do not call the slope a “3D” label. Do not say a ghosted tile, or a 3D parent with only child stock, can be dragged.
- **Related:** MAP-014, MAP-019, MAP-021, MAP-022, MAP-029.
- **Code:** `Map_Styling.vb` `GetLocationCountLabel` lines 224–261 and full/ghosted classes lines 327–345; `AppendThreeDBadge` lines 484–491; `mapLocationElIsFull` `Map_CONTROL_2017.ascx` lines 9152–9160.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** How location tiles show quantity

### MAP-005 — Create a location

- **Open:** Designer map, not read-only. Floating **+** (title “Create a new location...”) creates a child of All Locations (`-2`). A **+** on a designer tile creates a child of that tile. Inside an open 3D stack, **Add** (aria-label “Add a location to this stack”) creates a child, because the hover **+** is hidden on a 3D parent and on locations inside a 3D stack. Read-only users cannot open `NewLocation.aspx`.
- **Steps:**
  1. If the designer map has no primary location, the prompt **Pick your first location** already shows the type list. Clicking the floating **+** does nothing while that prompt is up. Pick a type from the prompt.
  2. Otherwise click the floating **+**, the tile **+**, or **Add**.
  3. Click **BUILDING**, **WAREHOUSE**, **STORE**, **FLOOR**, **ROOM**, **CLOSET**, **SHELF**, **BIN**, or **VEHICLE**.
  4. The name page opens. The box starts empty. The placeholder is “Type New {type} Name...” (for example “Type New Building Name...”). The instruction is “Press Enter to Save...”.
  5. Type a name and press Enter.
- **Options:** The nine types in MAP-003. The placeholder is built from “New ” plus the type name. The box is not prefilled.
- **Result:** The location is inserted with that name, type, parent, and path. Activity `LOCATION__CREATE`. A new primary location (parent `-2`) is highlighted on the next map load. A nested location does not get that highlight cookie. Inventory quantities are not copied onto the new location by this page.
- **If it fails:** “That location name is already in use!”
- **Do not write:** `CreateLocation_FASTER_DEBUG` is not called. Do not describe a name prompt that says “Please enter a name for the new location” with the default “New Location Name”; that prompt is not the live path.
- **Related:** MAP-003, MAP-007, MAP-036, MAP-037, MAP-043. WF-006.
- **Code:** `HoverAddClick` lines 4949–4953; toolbox lines 15905–15958; `NewLocation.aspx.vb` lines 30–48; `EDITABLE_FIELD.ascx.vb` `NEW_LOCATION_NAME` lines 289–294 and 470–499.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Add a location on the map

### MAP-006 — Rename a location

- **Open:** Location Editor (MAP-007), name field at the top. Not read-only. “All Locations” (id `-2`) is shown as the text “All Locations” and is not editable.
- **Steps:**
  1. Open the editor for a real location.
  2. Change the name. The current name is already in the field.
  3. Press Enter to save.
- **Options:** None.
- **Result:** The name is updated. Activity `LOCATION__EDIT` with comment `Changed location name to '{name}'`. The map highlight cookie is not set by a rename.
- **If it fails:** “That location name is already in use!”
- **Do not write:** Do not publish a rename of All Locations.
- **Related:** MAP-007, MAP-013. WF-006.
- **Code:** `LocationEditor.aspx.vb` `LoadNameField` lines 266–268; `EDITABLE_FIELD.ascx.vb` `LOCATION_NAME` lines 441–466.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Rename a location

### MAP-007 — Location editor

- **Open:** Designer hover **More actions**, then Edit (tooltip “Edit this location...”), or the phone footer **Edit**. URL `LocationEditor.aspx?LoadType=EXISTING&LocationID=`. Read-only goes to unauthorized. An unknown id goes to `Location Error.html`.
- **Steps:**
  1. Open the editor. You see the type image, the name, the breadcrumb (MAP-042), the children, **ADD NEW**, the paperclip (MAP-039), **Barcode # (scan to change)** (MAP-040), **Print Barcodes**, **View Products**, **Checkin Kiosk**, and **Checkout Kiosk**.
  2. Under **ADD NEW**, click or drag a type onto the page. That opens the same name page as MAP-005, as a child of this location.
  3. Click a child row to open that child.
  4. Click **View Products** to open the product list for this location (MAP-027).
- **Options:** **ADD NEW** uses the same nine types as MAP-003.
- **Result:** The editor sets `LocationID_VIEW` to this location. Creating a child inserts a location. The editor itself does not move stock.
- **If it fails:** None on this page. Name, barcode, and attachment failures are MAP-006, MAP-040, and MAP-039.
- **Do not write:** A `LoadType` other than `EXISTING` calls `InitializeNewLocation` and creates “New {type}” immediately. The map’s Edit link always sends `EXISTING`. Do not publish a non-EXISTING URL as the way to create a location.
- **Related:** MAP-005, MAP-006, MAP-027, MAP-039, MAP-040, MAP-041, MAP-042. WF-005, WF-006.
- **Code:** `MapProcessEvent_JS` case `EDIT` lines 9252–9255; `LocationEditor.aspx.vb` `Page_Init` and `LoadCorrectMode` lines 175–184; `LocationEditor.aspx` **ADD NEW** line 162, **View Products** line 393, kiosk lines 410–415.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Edit a location

### MAP-008 — Move primary locations

- **Open:** Designer map. Drag the diamond on the location header (`gridster-move-handle`). Nested locations have no header of their own. They move with the parent, or by reparent (MAP-010). The map is locked by default (MAP-009).
- **Steps:**
  1. If the lock title is “unlock map to move locations freely”, click the lock first. That is the default.
  2. Drag the diamond header of a primary location.
  3. Release it.
  4. While locked, an overlapping drop snaps back. While unlocked, overlaps are removed and the coordinates save.
- **Options:** None. There is no resize handle. `max_rows` is 100. Minimum primary width is 2 grid cells (MAP-011).
- **Result:** This user’s `GridsterCoordinates2017` only. Nested locations stay inside the parent. Inventory stays on the same location ids.
- **If it fails:** None. A locked overlap is cancelled, not reported in a sentence.
- **Do not write:** Do not publish a corner drag that resizes a tile. Do not publish a right-click move command.
- **Related:** MAP-009, MAP-010, MAP-011, MAP-030. WF-006.
- **Code:** `mapGetGridsterOptions` lines 2988–3004; `mapHookGridsterMapLock`; `Gridster_Utilities.OpenGridsterItem` lines 93–105.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Move locations on the map

### MAP-009 — Map lock

- **Open:** Designer map toolbar, lock button. Hidden on `MapDesignerNaked` (`DisableMobileView`). The saved preference is still read there.
- **Steps:**
  1. Open the map. The lock starts on. The button title is “unlock map to move locations freely”. A missing token is locked. Token `-19` is locked. Token `-21` is unlocked.
  2. Click the lock to unlock. The title becomes “lock map to prevent locations from being moved accidentally”. Coordinates save without a full reload.
  3. Click it again to lock. An in-progress reparent is cancelled.
- **Options:** Locked (default) or unlocked.
- **Result:** The token is stored on this user’s coordinate string. Inventory is unchanged. While locked, an overlapping move snaps back (MAP-008).
- **If it fails:** None. A failed coordinate save has no separate sentence on this button.
- **Do not write:** Do not say the map starts unlocked.
- **Related:** MAP-008, MAP-010. WF-006.
- **Code:** `Map_CONTROL_2017.ascx` lock button lines 10637–10648; `mapMapLockToggle` lines 2540–2550; `mapRefreshMapLockMenuUi` lines 2475–2479; `Gridster_Utilities.vb` lines 57–62.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Lock or unlock the map layout

### MAP-010 — Move a location under a different parent

- **Open:** Designer map. The clasp tooltip is “Snap off location and move to a different parent.” Hidden on `MapDesignerNaked` when the query contains `welcome=1`.
- **Steps:**
  1. Click the clasp.
  2. The banner says “Click a new parent or empty space on the map to move this location.” **Cancel** is on the banner. Escape cancels. Turning the lock on also cancels.
  3. Click a location tile, or click empty canvas. Empty canvas sets the parent to `-2` and makes the location primary.
  4. The dialog title is “Move location?” The message is “Move this location? Nested locations stay with it.” Click **Cancel** or **Move**.
- **Options:** None. Column and row default to 1 if the posted values are below 1.
- **Result:** The parent id changes. Nested locations stay with it. Quantities stay on the same location ids. Inventory is not moved between locations.
- **If it fails:** Title “Could not move location”. Message “Could not move this location.” Button **OK**.
- **Do not write:** Do not describe this as a stock transfer.
- **Related:** MAP-008, MAP-009. WF-006.
- **Code:** `GetLocationReparentClasp` lines 215–221; banner line 5097; confirm modal lines 10801–10816; error modal lines 10847–10854; `btn_hidden_reparent_coordinates_Click`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Move a location under a different parent

### MAP-011 — Tile size follows children

- **Open:** Automatic. There is no resize handle.
- **Steps:**
  1. Add or remove children, or turn **V** or **3D** on or off.
  2. After the map reloads, the primary tile’s width and height follow the children. The minimum primary width is 2 grid cells. `max_rows` is 100.
- **Options:** None.
- **Result:** Layout only. Inventory is unchanged.
- **If it fails:** None.
- **Do not write:** Do not publish a free resize. Compact cell sizes are compiled and skipped.
- **Related:** MAP-005, MAP-008, MAP-028, MAP-029. WF-006.
- **Code:** `Gridster_Utilities.OpenGridsterItem` lines 93–96; `mapGetGridsterOptions` has no `resize` key; `Map_CONTROL_2017.ascx.vb` `_setGridsterSize(0)` lines 135–136.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Why a location tile is wider or taller

### MAP-012 — Delete a location

- **Open:** Designer hover **More actions**, then Delete (tooltip “Delete this location...”), or the phone footer **Delete**. Read-only cannot open the dialog.
- **Steps:**
  1. Click Delete.
  2. The dialog shows the location name, path, and type image.
  3. The message is “Are your sure you want to DELETE this location?” and “All sub-locations will be deleted. Existing products will be checked out automatically.”
  4. Click **YES**. There is no No button. Closing the popup cancels.
- **Options:** None. The checkbox “Include Any Sub-Locations” is in the markup, set checked, then `Visible = False` before the dialog is shown. The click handler never reads it.
- **Result:** Descendants are always included. If the quantity in this location and its children is greater than 0, activity `INVENTORY__CHECK_OUT` is recorded with comment `Items cleared before deleting location '{name}' ({id})`, and those quantity rows are deleted. Then the location rows are deleted and activity `LOCATION__DELETE` is recorded with comment `Deleted location '{name}' ({id})`. A primary location is removed from this user’s coordinates. This is not the Transfer page.
- **If it fails:** None. If the `LocationToDelete` cookie is missing, **YES** does nothing. If the location no longer exists when the dialog opens, the popup closes with no sentence.
- **Do not write:** Do not say the user can choose to keep sub-locations. Do not say delete only removes the parent.
- **Related:** MAP-021, WF-003 is a different check-out. WF-006.
- **Code:** `ConfirmationDialog.aspx` lines 36–48; `ConfirmationDialog.aspx.vb` `ClearLabelsAndButtons` line 230, `btn_yes_delete_Click` lines 87–109, `CheckoutProductsBeforeDeletingLocation` lines 113–153, `DeleteLocationFunction` lines 185–221.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Delete a location

### MAP-013 — Clone a location’s structure

- **Open:** Designer hover **More actions**, then Clone (tooltip “Clone this location...”), or the phone footer **Clone**. Not on the read-only strip.
- **Steps:**
  1. Click Clone.
  2. The title is “Name the New Location”. The name box allows 255 characters. The suggested name is the source plus ` (Copy)`, then ` (Copy 2)`, and so on up to 999, shortened so the whole name is at most 255 characters.
  3. **Auto-Rename Sub-Locations** is off by default. **Keyword** and **Replace with** start disabled. The info control is “About auto-rename”. The tip is “Replaces a whole word or hyphen-separated part in sub-location names. For example, A32 to B45 renames A32-1 to B45-1. The new location itself keeps the name you entered.”
  4. Click **Clone** or **Cancel**. Enter in the name or keyword fields confirms. Escape closes the modal.
- **Options:** **Auto-Rename Sub-Locations** off by default. Keyword and replacement, each max 255, only when the switch is on.
- **Result:** The page POSTs `https://code.cyberstockroom.com/api/LocationClone` with the new name and the source id, then reloads and can highlight the new location. The new root keeps the typed name. Keyword rename, when used, changes sub-location names and skips a blank result or a sibling-name collision. What the API copies, including whether quantities are copied, is Uncertain. Inventory copy on the map is MAP-014.
- **If it fails:** “Please enter a name for the new location.” “A clone cannot use the same name as the original location.” “That name is already used by another location next to the original.” An API error hides the tarp and leaves the user on the map. No fixed API-error sentence was found.
- **Do not write:** Do not say the clone copies stock, and do not say it leaves quantities at zero. That API effect is Uncertain.
- **Related:** MAP-014, MAP-037. WF-006.
- **Code:** Modal lines 10756–10798; `mapCloneSuggestedName` lines 9863–9878; `mapCloneModalRefreshNameGate` lines 9891–9903; `cloneLocation`; `LocationApplicationService.ApplyKeywordRenameViaIdMap`.
- **Confidence:** Confirmed for the page. Uncertain for the API copy rules.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Clone a location’s structure

### MAP-014 — Copy stock with Ctrl+drop

- **Open:** Designer map. Hold Ctrl, drag a full location (own quantity greater than 0), and drop it on a different location. Not available while multi-select is active (MAP-030). Skipped when the drag is a product chip from the peek; that drop is a transfer (MAP-022).
- **Steps:**
  1. Hold Ctrl.
  2. Drag a full location onto a different location. The same location, source `-2`, and destination `-2` are ignored.
  3. Confirm “Are you sure you want to copy the contents to this location? Any existing items will be cleared first.”
  4. Cancel does not call the API.
- **Options:** None.
- **Result:** On confirm, the page POSTs `https://code.cyberstockroom.com/api/inventory?action=clone` with the source and destination ids, then reloads on success. This is the stock copy. It is not the structure clone (MAP-013). The confirm text says existing items at the destination are cleared first. What that API does to quantities is Uncertain.
- **If it fails:** None. An API error hides the tarp and logs `xhr.message`. There is no fixed sentence.
- **Do not write:** Do not publish a cleared-first stock formula, a quantity total, or a per-SKU rule. Those are outside this repo. Do not say Ctrl+drop runs during a multi-select.
- **Related:** MAP-013, MAP-022, MAP-030. WF-006.
- **Code:** `MapProcessEvent_JS` case `DROP` lines 9378–9388; keydown lines 9164–9171; `_cloneContents` lines 9712–9732.
- **Confidence:** Confirmed for the prompt and the request. Uncertain for the API’s stock math.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Copy stock from one location to another

### MAP-015 — ABC sort

- **Open:** Gear, aria-label **Map settings**, row **ABC Sort**. The row title is “When on, child locations are shown in alphabetical order.” Hidden when `DisableMobileView` is set. The saved flag still affects any map that reads it.
- **Steps:**
  1. Open **Map settings**.
  2. Turn **ABC Sort** on or off. The default is off. Token `-20` means on. A missing token leaves children in location-id order.
  3. The page saves and reloads.
  4. Direct children are sorted by name, then by id. Fewer than 2 children skips the sort.
- **Options:** Off (default) or on.
- **Result:** Display order of direct children only. Primary canvas positions are a separate coordinate list. Inventory is unchanged.
- **If it fails:** `[Map] ABC_SORT_TOGGLE: could not save coordinates.` The page does not reload.
- **Do not write:** None.
- **Related:** MAP-016, MAP-028, MAP-029.
- **Code:** Settings row lines 10673–10685; `mapAbcSortToggle` lines 2514–2537; `CS_Map_Reusable.GetChildLocationsForRender` lines 128–136.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Sort child locations alphabetically

### MAP-016 — Use a shared map layout

- **Open:** **Map settings** → **Shared Maps**. Sharing is turned on in Settings by an admin (DSP-001), not by a switch in this menu.
- **Steps:**
  1. Open **Shared Maps**. While it loads, the row says “Loading…”.
  2. If the list is empty, it says “No shared maps. Admins can share their maps in the Settings page.”
  3. Choose a person. The dialog title is “Sync your Map Layout” and it shows that person’s name and email.
  4. The warning is “If you sync to this layout, you will lose your existing layout. Are you sure you want to continue?”
  5. Click **Keep my layout** or **Sync**. Escape or the backdrop cancels unless a sync is already running. While it runs the button says “Syncing…”.
- **Options:** None. The copy is the other user’s coordinates, both zooms, vertical parents, 3D parents, and the vertical-migrated flag.
- **Result:** This user’s layout is replaced by that layout, then the map reloads. Inventory, products, and locations are not copied.
- **If it fails:** “Could not load shared maps.” “Sync is not available. Please refresh the page.” “Could not save the synced layout. Please try again.” “Could not sync this layout. Please try again.”
- **Do not write:** Do not say sync copies stock.
- **Related:** DSP-001, MAP-009, MAP-015, MAP-017, MAP-028, MAP-029. WF-010.
- **Code:** Menu row lines 10707–10712; `mapLoadSharedMapsSubmenu` lines 2095–2111; modal lines 10858–10877; `mapSyncLayoutModalConfirm` lines 2344–2417.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Use a teammate’s map layout

### MAP-017 — Zoom

- **Open:** Zoom buttons on `Map.aspx` and `Map_read_only.aspx`. Each button’s title is “Type +/- to zoom”. Pinch works on touch. Keys **+** and **−** work when the user is not typing.
- **Steps:**
  1. Click **+** or **−**, press those keys, or pinch.
  2. **+** multiplies the zoom by 1.1. **−** multiplies it by 0.9.
  3. Desktop zoom stays between 0.1 and 1. Touch zoom stays between 0.15 and 2.2.
  4. The first zoom is 1 on desktop and 0.74 on the mobile track. A narrow layout (about 900px) uses the mobile number. Saved values are tokens `-6` (standard) and `-7` (mobile).
- **Options:** None beyond the two saved zoom numbers.
- **Result:** Zoom is saved on this user’s coordinate string. Inventory is unchanged. Ctrl+wheel does not zoom the browser page.
- **If it fails:** None.
- **Do not write:** Keys are ignored while typing, during the one-location coach, or while a modal is open. Do not publish those moments as zoom shortcuts.
- **Related:** MAP-031, MAP-034, MAP-044.
- **Code:** `Map.aspx` lines 145–151; `mapZoomStepIn` and `mapZoomStepOut` lines 7880–7885; `getMapZoomMin` and `getMapZoomMax` lines 6131–6136; `Gridster_Utilities.DefaultMobileZoom` line 83.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Zoom the map

### MAP-018 — Search the map

- **Open:** The box placeholder is “Search Map...”. The clear control is **×** (title “Clear filter”). On narrow chrome a **>** button applies the filter (title “Search”, aria-label “Apply filter”).
- **Steps:**
  1. Type in **Search Map...**.
  2. The page requests `GET https://code.cyberstockroom.com/api/map?mapFilter=`. Matching tiles highlight and the view moves to them.
  3. Press Enter to cycle to the next match. The form does not submit.
  4. Press Escape, or click **×**, to clear the search and restore the previous scroll position.
- **Options:** None. The same text is passed as `MAP_FILTER` when a transfer opens from the map.
- **Result:** Display only, until a later transfer uses the same text as a filter. Which fields the API matches is Uncertain. If the API call fails, the page matches location titles on the map instead.
- **If it fails:** None as a sentence for the API error. An empty result disables the quantity download and sets its title to “No results to download”.
- **Do not write:** Do not name the API’s match fields. They are not in this repo.
- **Related:** MAP-019, MAP-020, MAP-032, MAP-034.
- **Code:** Input line 10622; submit button line 10629; `mapFilterStartSearch` lines 13617–13670; `mapFilterTitleMatches` lines 13854–13863.
- **Confidence:** Confirmed for the client. Uncertain for the API match fields.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Search the map

### MAP-019 — Low and high quantity colors

- **Open:** Automatic during a map search highlight. The two numbers are DSP-006 (quantity threshold) and DSP-007 (max highlight). This map screen does not edit them. Do not invent the numbers; they come from that user’s settings and coordinate string. A missing or negative max highlight is treated as 0.
- **Steps:**
  1. Search the map (MAP-018).
  2. A quantity of 0 or below is a plain location highlight, with no low, mid, or max color.
  3. If both the threshold and the max highlight are 0, a quantity above 0 is mid only.
  4. Otherwise, quantity at or above the max highlight uses the max color and the tooltip prefix `MAX level`. Quantity at or below the threshold uses the low color. Anything else that is still above 0 is mid.
- **Options:** The threshold and max highlight saved for this user. Both 0 is the “no special ends” case.
- **Result:** Color and tooltip only. Inventory is unchanged.
- **If it fails:** None. A non-numeric value is treated as 0.
- **Do not write:** Do not publish a default threshold such as 10. That number is on the unreachable dashboard prototype, not this map.
- **Related:** DSP-006, DSP-007, MAP-018.
- **Code:** `mapResolveQuantityTier` lines 13555–13561; `mapApplyQuantityThresholdToLocation` lines 13564–13579; `MAP_MAX_TOOLTIP_PREFIX` line 13522.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Low-stock and max-level colors on the map

### MAP-020 — Check in from the map

- **Open:** Designer hover, tooltip “Check IN products to this location...”. Not on the read-only strip. An empty location can be the destination. Destination `-2` (All Locations) does not open the page.
- **Steps:**
  1. Hover the location and click Check IN.
  2. Transfer opens with source `-2` and this location as the destination. The URL includes `isCheckin=true`. The current search text is passed as `MAP_FILTER`.
  3. A wide layout opens `Transfer.aspx` in a popup. A narrow layout (about 900px) opens `MOBILE_Transfer.aspx` as a full page and stores a return path.
  4. During onboarding the URL also includes `HideImportFile=true`.
  5. Finish the transfer on that page (WF-002, XFR-001). The map click itself does not change quantities.
- **Options:** None.
- **Result:** The transfer page is opened. Stock changes happen there, not in the map click. Do not copy the Transfer page’s stock math into this step.
- **If it fails:** None. Destination `-2` returns without opening the page and without a sentence.
- **Do not write:** Do not say an empty location cannot be a check-in destination. `Map.aspx` defines `checkin(id)`, which on tablet mode primes `MOBILE_Process` CHECK_IN, but the map control never calls `checkin(id)`. Do not publish that function as the hover button.
- **Related:** MAP-021, MAP-022, XFR-001. WF-002.
- **Code:** `MapProcessEvent_JS` case `CHECKIN` lines 9227–9230; `_dragToCheckin` lines 9685–9709; `Map.aspx` `checkin` lines 47–51 is not called by the control.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Check products in from the map

### MAP-021 — Check out from the map

- **Open:** Designer hover, tooltip “Check OUT products from this location...”. Or drag a full location and drop it on the strip. The strip’s visible label is **Check out**. Its accessible name is “Drag inventory here to check out”. The strip is hidden during onboarding. An empty location, or a location whose quantity is only in children, cannot start the drag and cannot open check-out. Source `-2` does not open it.
- **Steps:**
  1. Hover a full location and click Check OUT, or drag that location onto **Check out**.
  2. Transfer opens with this location as the source and destination `-2`. The URL includes `isCheckout=true`.
  3. Wide layout uses a popup. Narrow layout uses `MOBILE_Transfer.aspx`. Onboarding adds `HideImportFile=true`.
  4. Finish the transfer on that page (WF-003, XFR-002).
- **Options:** None.
- **Result:** The transfer page is opened. The map click does not itself subtract stock.
- **If it fails:** None. An empty source returns without a sentence.
- **Do not write:** `Map.aspx` `checkout(id)` is not called by the map control. Do not publish it as the hover or the strip. Do not treat delete’s check-out activity (MAP-012) as this transfer.
- **Related:** MAP-004, MAP-012, MAP-020, XFR-002. WF-003.
- **Code:** `_dragToCheckout` lines 9656–9682; `DRAG_START` full check lines 9270–9276 and strip lines 9316–9320; strip markup lines 14962–14964.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Check products out from the map

### MAP-022 — Drag stock between locations

- **Open:** Designer map. Drag a full location, or a product row from the peek, onto a different location. Same id, source `-2`, and destination `-2` are ignored. Ctrl+drop is MAP-014 instead, unless a product chip is the drag.
- **Steps:**
  1. Drag a full location, or a peek row, onto another location. A 3D parent opens its stack while you drag over it.
  2. If the drag is exactly one unit and onboarding is off, the single-unit dialog opens (MAP-023).
  3. Otherwise Transfer opens. A wide layout uses a popup. A narrow layout opens `MOBILE_Transfer.aspx`.
  4. Finish that page (WF-004). Closing the popup runs the transfer backend only when the refresh cookie says to.
- **Options:** None.
- **Result:** Source and destination cookies are set to the two location ids. Inventory changes on the transfer page, not at the moment of the drop, except the single-unit commit in MAP-023.
- **If it fails:** None. A same-location drop is ignored.
- **Do not write:** Do not describe a drop on All Locations as a transfer. Check-in and check-out are MAP-020 and MAP-021.
- **Related:** MAP-014, MAP-020, MAP-021, MAP-023, MAP-024. WF-004.
- **Code:** `DROP` lines 9370–9396; `mapOpenInventoryTransferPage` lines 9417–9436.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Drag stock to another location

### MAP-023 — Move one unit and comment

- **Open:** Automatic on a designer drop when onboarding is off, and either the dragged product quantity is exactly 1, or the location’s own quantity is exactly 1 and the product lookup finds one product with quantity 1. The lookup asks for 25 products. If the lookup fails, or the location has more than one product with quantity, the full transfer page opens instead. Onboarding always opens the full transfer page.
- **Steps:**
  1. Drop that single unit on another location.
  2. The title is “Moving this item.” The hint is “Any comments about this transaction?”
  3. Leave the box empty and the button stays **Skip Comment**. Type a comment and the button becomes **Save**.
  4. Click **Skip Comment** or **Save**, or press Enter. **Cancel**, Escape, or the backdrop aborts and does not post.
- **Options:** A comment, or none.
- **Result:** The commit writes that product number, sets the source cookie quantity of that SKU to 0, and sets the destination cookie quantity to 1, then posts the transfer backend. The source stock of that SKU is set to 0. This is not the Transfer page’s “move 1, keep the rest” rule.
- **If it fails:** None. A failed lookup opens the transfer page with no sentence.
- **Do not write:** Do not publish this as moving 1 and leaving the rest at the source.
- **Related:** MAP-022, XFR-003. WF-004.
- **Code:** `mapBeginSingleUnitTransfer` lines 9442–9458; `mapLookupSingleUnitLocationTransfer` lines 9461–9508; `mapCommitSingleUnitTransfer` lines 9629–9653; modal lines 10734–10739.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Move one item from the map and add a comment

### MAP-024 — See products inside a location

- **Open:** Click a location on the designer or read-only map. The product-editor map uses the quantity box instead (MAP-026). A 3D stack also has **View contents** for the parent.
- **Steps:**
  1. Click the location. The peek shows “loading...”.
  2. Up to 25 products load from `api/products` for that location. While the map search has text, and the click is not in the “highlight location” state, `SearchTerms` is included. A highlight-location click clears that filter so all products in the location show.
  3. Rows are draggable (MAP-022). A custom-field chip can filter the rows. Which chips appear is MAP-025.
  4. Press Escape to close the peek.
- **Options:** None. Expiration lookups are capped at 25 product ids. Products past the first 25 are not requested.
- **Result:** A list on the map. No inventory change unless the user then drags a row or edits a quantity on the product map.
- **If it fails:** None. A failed expiration lookup stores an empty date for that product.
- **Do not write:** Do not say the peek lists every product when the location has more than 25.
- **Related:** MAP-022, MAP-025, MAP-027.
- **Code:** `peekAtProducts` lines 3509–3527; expiration cap line 3483; “loading...” line 3241.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** See products inside a location

### MAP-025 — Popup details

- **Open:** **Map settings** → **Popup details**. The row title is “Choose which product fields show in the location popup.” Hidden when `DisableMobileView` is set.
- **Steps:**
  1. Open **Popup details**. The hint is “Select which product details to show in the popup.”
  2. Turn fields on or off. The list is built for this account. Do not invent field names.
  3. An expiration switch appears only when the account has expiration data.
  4. Click **Done**.
- **Options:** The account’s popup-detail catalog. Token `-23` stores the selected custom-field indexes. When that token is absent, description only is shown. The save path that was read keeps description on. Expiration is off when its token is absent.
- **Result:** The peek chips follow the saved indexes. Inventory is unchanged.
- **If it fails:** None. A bad catalog becomes an empty list. Save is skipped if the map layout is not ready.
- **Do not write:** CFL-001 and CFL-002 are stored in the same coordinate string and are edited in Settings, not in this popup. Do not list Buy Price, Sell Price, or a personalized-sort switch as rows here.
- **Related:** MAP-024, CFL-001, CFL-002.
- **Code:** Row lines 10687–10691; modal lines 10744–10752; `mapPopupDetailCatalog`; `Gridster_Utilities` token `-23` lines 68–69.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Choose product fields in the location popup

### MAP-026 — Change quantity on the product map

- **Open:** Product editor map, type 2 (`MapProductEditorNaked.aspx` with `ProductNumber`). Read-only on a product-editor map goes to unauthorized. Helper text: “STEP 1 Select a product.” and “STEP 2 Click a location. Type new quantity. Press Enter.”
- **Steps:**
  1. Click a location. A quantity box opens for the product in the query string.
  2. Type the new quantity.
  3. Press Enter to save. Up and Down step the value when the pointer is fine (`hover: hover` and `pointer: fine`).
  4. Press Escape to close the box without saving.
- **Options:** None. The request uses `action=adjust` with source and destination both equal to that location, and the quantity set to the new value. The comment sent is `Quantity for '{uid}' was adjusted from {old} to {new}`. Timeout is 3 seconds.
- **Result:** The on-screen number and the full or ghosted style update when the request is sent, not only after success. What the API writes after it accepts the request is the adjust call above. Do not add a second stock formula.
- **If it fails:** Invalid input is replaced with 0 and reselected, and it is not sent. A request error logs “There was a problem updating the quantity in this location...” and does not roll the on-screen number back.
- **Do not write:** Do not say the number changes only after the API succeeds. Map type 5 exists in the enum and no page in this scope sets it.
- **Related:** MAP-024, PRD-010. Not a Transfer mode (WF-004).
- **Code:** `MapProductEditorNaked.aspx` helpers lines 163–174; `UpdateCount` lines 5932–5964; `updateQuantity` lines 5984–6022 and the label update that follows the request.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Change a product’s quantity on the map

### MAP-027 — Open the product list for a location

- **Open:** Hover View, tooltip “View the products in this location...”, on the designer map and the read-only map. Location Editor **View Products** does the same.
- **Steps:**
  1. Click View, or click **View Products** in the editor.
  2. The app stores `LocationID_VIEW`.
  3. The designer map opens Products. The read-only map opens Products_read_only.
- **Options:** None.
- **Result:** The product list opens on that location. Quantity is unchanged by this click.
- **If it fails:** None. `ProcessHover` catches a parse error and does not show a sentence.
- **Do not write:** “View Location Details...” is MAP-038, not this list.
- **Related:** MAP-002, MAP-007, MAP-024.
- **Code:** `MapProcessEvent_JS` case `VIEW` lines 9237–9239; `Map.aspx.vb` lines 20–22; `Map_read_only.aspx.vb` lines 18–20; `LocationEditor.aspx` line 393.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Open the product list for a location

### MAP-028 — Vertical stack

- **Open:** Designer hover **More actions**, then **V**, or the phone footer **Vertical**. Hidden inside a 3D stack. Needs at least two direct children. A child that has its own children must already be 3D.
- **Steps:**
  1. Open **More actions** and click **V**, or select the location and click **Vertical**.
  2. If it is allowed, the parent id is saved (token `-8`) and the map reloads. Children stack in a column. The default is off until the user turns it on.
  3. If it is not allowed, the control shows one of these tooltips: “Stack children vertically”, “Turn off vertical stack”, “Needs at least two children”, “A child has its own locations. Turn that child to 3D first”, “Turn off 3D first”, “Turn off 3D on a child first”, or “Vertical isn't available here.”
- **Options:** Off until turned on. On is stored as that parent’s id under token `-8`.
- **Result:** Layout only. Children keep their ids and quantities.
- **If it fails:** `[Map] VERTICAL_CHILDREN_TOGGLE: could not save coordinates.` The page does not reload. A locked-on toggle logs `[Map] VERTICAL_CHILDREN_TOGGLE: not allowed (locked on).`
- **Do not write:** Do not say **V** works inside a 3D stack or with a single child.
- **Related:** MAP-011, MAP-015, MAP-029. WF-006.
- **Code:** `LocationEligibleForVerticalStack` lines 328–336; `LocationVerticalToggleTooltip` lines 414–430; footer label **Vertical** line 5662; save log line 739.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Stack child locations vertically

### MAP-029 — 3D stack

- **Open:** Designer hover **3D**, or the phone footer **3D**. The open stack is also used on the read-only map. Hidden for a location that is already inside a 3D stack. Empty parents can become 3D. Not allowed when a child is already 3D or a child has children.
- **Steps:**
  1. Click **3D**. If it is allowed, token `-22` is saved and the map reloads. Children are hidden in an overlay.
  2. Click the parent to open or close the stack. Click outside to close it.
  3. **Add** on the stack creates a child (MAP-005). **View contents** peeks the parent.
  4. Search and drag can open the stack.
  5. If it is not allowed, the tooltip is one of: “Show children in a 3D stack”, “Turn off 3D stack”, “Already inside a 3D stack”, “A child is already 3D”, “A child has its own locations”, “Remove child locations before turning off 3D”, or “3D isn't available here.”
- **Options:** Off until turned on.
- **Result:** Layout only. A 3D parent with only child quantity is drawn full (MAP-004) but still cannot be dragged unless its own quantity is greater than 0.
- **If it fails:** `[Map] THREE_D_CHILDREN_TOGGLE: could not save coordinates.` A locked-on toggle logs `[Map] THREE_D_CHILDREN_TOGGLE: not allowed (locked on).`
- **Do not write:** Do not say 3D is available when a child already has children or is itself 3D.
- **Related:** MAP-004, MAP-005, MAP-011, MAP-028. WF-006.
- **Code:** `LocationEligibleForThreeDStack` lines 301–311; tooltips lines 436–455; `map3dToggleStack`; **Add** line 1135.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Show child locations in a 3D stack

### MAP-030 — Move several locations

- **Open:** Designer map on desktop. Off while touch controls are on, including tablet mode and the phone layout. Primary tiles only.
- **Steps:**
  1. Ctrl-click or Cmd-click primary tiles, or Ctrl-drag a rectangle on empty map. The move starts after 5 pixels. The right mouse button does not select.
  2. Drag the group.
  3. Release to save. An invalid drop (collision or off the grid) is not saved.
  4. Press Escape to cancel the drag or clear the selection.
- **Options:** None.
- **Result:** This user’s coordinates for the group. Inventory is unchanged. Ctrl+drop inventory copy is suppressed while a selection is active.
- **If it fails:** None. An invalid drop is not saved and has no sentence.
- **Do not write:** Do not publish multi-select on a phone or while tablet mode is on. There is no right-click selection menu.
- **Related:** MAP-008, MAP-014, MAP-033, MAP-034. WF-006.
- **Code:** `mapMultiSelectOnPointerDown` lines 8925–8954; `MAP_MULTI_SELECT_MOVE_THRESHOLD_PX` line 8211; `mapMultiSelectIsDesktopEnabled` lines 8221–8222.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Select and move several locations

### MAP-031 — Minimap

- **Open:** The toggle title is “Minimap (picture-in-picture)”. The canvas is 240×160 and its label is “Map overview. Click to scroll the map.” It can auto-open on a large map when no open or closed state is saved.
- **Steps:**
  1. Open the minimap. Open is token `-10`. Closed is token `-11`.
  2. Click the picture. The big map scrolls to that spot.
  3. A drag that passes over the minimap can drop at the center of the current view.
- **Options:** Open or closed. No saved state can auto-open.
- **Result:** Scroll position, plus the same drop result as a normal drop. Inventory changes only if that drop is a transfer or a Ctrl+copy.
- **If it fails:** None.
- **Do not write:** None.
- **Related:** MAP-008, MAP-017, MAP-018, MAP-022, MAP-030.
- **Code:** Toggle lines 14967–14978; `mapViewFinderInit` line 7786; tokens `-10` and `-11` in `Gridster_Utilities.vb`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Use the map minimap

### MAP-032 — Download a quantity report

- **Open:** Button title “Download Quantity Report”. It stays hidden until some visible location has quantity greater than 0. An empty search disables it and sets the title to “No results to download”. Signed in. A signed-out export request returns HTTP 401 with no sentence. The export method has no separate read-only ban.
- **Steps:**
  1. Click **Download Quantity Report**.
  2. The title is “Download Quantity Report”. The hint is “You are about to download the product quantities across your map.” If a search is active, the dialog shows “filtering by” and the term.
  3. Leave **Group by Location** selected (it starts checked), or choose **Group by Product**.
  4. Click **Download** or **Cancel**. Escape closes the dialog.
- **Options:** **Group by Location** (default, value `byLocation`) or **Group by Product** (value `summed`). By location the columns are Location ID, Location, Product Number, Description, Quantity, and empty locations are included. By product the columns are Product Number, Description, Quantity, summed. The file name starts `CyberStockroom - Group by Location` or `CyberStockroom - Group by Product`, then the date `MMM d yyyy`. A search term is inserted into the name. The name is cut at 200 characters, then `.csv`. The SQL starts from `Quantity > 0`.
- **Result:** A file download. Inventory is unchanged.
- **If it fails:** “The map data could not be downloaded.”
- **Do not write:** Do not add columns that are not in those two headers.
- **Related:** MAP-018.
- **Code:** Button lines 10654–10655; modal lines 10820–10843; `BuildMapQuantityCsv` lines 661–713; `MapExportTitle` lines 640–643; error text line 14301.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Download a quantity report from the map

### MAP-033 — Tablet mode

- **Open:** **Map settings** row **Tablet mode**, or the tablet button. The row stays hidden until the device allows a user toggle. Hidden entirely when `DisableMobileView` is set. Token `-5` means on.
- **Steps:**
  1. Turn **Tablet mode** on or off. If the user is not allowed to toggle, nothing happens.
  2. The page saves and reloads. Touch UI, the selection footer, and edge scroll turn on. Multi-select turns off.
  3. On a narrow designer map, the first tap selects the location. The bottom bar shows **Edit**, **Clone**, **Vertical**, **3D**, **Delete**, and **Close**. **Vertical** and **3D** are left off when they do not apply. **Close** is “Return to standard footer”.
- **Options:** Off until the user or the device turns it on.
- **Result:** This user’s tablet-mode token, and the touch layout. Inventory is unchanged.
- **If it fails:** None. A disallowed toggle returns without a sentence.
- **Do not write:** Do not say every device shows the Tablet mode switch.
- **Related:** MAP-030, MAP-034, MAP-044.
- **Code:** `mapTabletModeToggle` lines 2573–2588; footer actions lines 5659–5683; token `-5` in `Gridster_Utilities.vb` lines 29–31.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Turn on tablet mode for the map

### MAP-034 — Map keyboard shortcuts

- **Open:** The keyboard, when the condition in the step is true. Shortcuts do the same thing as the matching buttons.
- **Steps:**
  1. Press **+** or **=** to zoom in by 1.1, or **−** to zoom out by 0.9, when you are not typing, not in the one-location coach, and no modal is open.
  2. Ctrl+wheel does not zoom the browser page.
  3. Enter in **Search Map...** cycles matches. Escape in that box clears the search.
  4. Escape closes clone, sync, export, reparent, the reparent error, the single-unit dialog, the peek, and the check-in lesson, and it clears multi-select.
  5. Hold Ctrl and drop a location to copy inventory (MAP-014), unless a multi-select is active.
  6. Ctrl or Cmd-click, and Ctrl-drag on empty map, select primary tiles. Touch controls turn this off.
  7. Enter in the product-map quantity box saves. Escape closes it without saving. Up and Down step that quantity on a fine pointer.
  8. Enter confirms clone and the single-unit dialog.
- **Options:** None.
- **Result:** The same result as the matching feature. Inventory changes only when the shortcut is the quantity save, the single-unit commit, or Ctrl+drop.
- **If it fails:** None beyond the feature that shortcut runs.
- **Do not write:** Do not publish a right-click shortcut. Do not publish multi-select keys while touch controls are on.
- **Related:** MAP-013, MAP-014, MAP-017, MAP-018, MAP-023, MAP-026, MAP-030.
- **Code:** `document.onkeydown` zoom around lines 7910–7930; `mapFilterKeydown`; multi-select key handler; `UpdateCount` lines 5937–5964; clone and unit-transfer Enter handlers.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Map keyboard shortcuts

### MAP-035 — Pan and scroll to origin

- **Open:** Drag empty canvas on `Map.aspx`. The origin button title is “Scroll to map origin (top-left)”. It starts hidden and appears when the user is scrolled away. The grab-pan script is on `Map.aspx` and is not copied onto the read-only page. The control’s own drag-scroll still loads with the control.
- **Steps:**
  1. Press empty canvas and drag. The cursor is grab, then grabbing. A drag that starts on a location, a move handle, the hover strip, the add tab, the check-out strip, the peek, the toolbox, the minimap, or the getting-started card does not pan.
  2. When you are scrolled away, click **Scroll to map origin (top-left)**. The map jumps to the top-left.
- **Options:** None.
- **Result:** Scroll position only.
- **If it fails:** None.
- **Do not write:** Do not say the read-only page includes the `Map.aspx` grab-pan script.
- **Related:** MAP-002, MAP-017, MAP-031.
- **Code:** `Map.aspx` pan script lines 62–142; origin button lines 10724–10728; `mapInitScrollToOriginControl`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Pan the map and return to the top-left

### MAP-036 — Empty-map coaching

- **Open:** Designer map only, after layout. Product count is queried only for the designer map. Not during onboarding for the getting-started card.
- **Steps:**
  1. If the designer map has no primary location, the prompt says **Pick your first location** and the type toolbox is pinned there. The floating **+** does nothing until that prompt is gone (MAP-005).
  2. If there is exactly one location tile, the tips are **Create Sub-Locations** on the tile and **Create New Location** near the floating **+**. Zoom keys are blocked during this coach (MAP-017).
  3. If there is more than one location tile and the account has zero products, the card title **My Progress** is shown. The steps are “You started your map”, “Add your first product”, and “Check-in your products”.
  4. If there is more than one location tile, the account has products, and the sum of the tiles’ own quantities is 0, the card is in the check-in state. The lesson button’s accessible name is “Play 2 min lesson about checking in your products”. The lesson title is “2 min lesson about checking in your products”. Escape or **Close** closes the lesson.
- **Options:** None.
- **Result:** Coaching only. Inventory changes only if the user then creates a location or checks products in.
- **If it fails:** None.
- **Do not write:** Do not say one card covers every mix. Zero locations uses the empty prompt. One location uses the two tips. The progress card requires more than one location tile. `MapDesignerNaked` has its own “Create Sub-Locations” and “Create New Location” helpers in `localStorage`. Those are separate from these tips.
- **Related:** MAP-005, MAP-017, MAP-020.
- **Code:** `mapRevealAfterLayout` lines 1472–1483; `mapShowEmptyLocationPrompt` lines 4603–4620; empty prompt text line 15817; `mapShowSingleLocationCoach` lines 4842–4865; `mapShowGettingStartedCard` lines 4880–4899; lesson title line 15902.
- **Confidence:** Confirmed for these gates.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** First-time hints on an empty map

### MAP-037 — Highlight a new location

- **Open:** Automatic on the next map load after a primary create or a clone. No button.
- **Steps:**
  1. Create a primary location or clone a location.
  2. After the reload, the map scrolls to the new id and then clears the cookie.
  3. A keyword rename on a clone can also show a notice.
- **Options:** None.
- **Result:** Highlight only. A nested create (parent other than `-2`) does not set this cookie in the name-field save.
- **If it fails:** None. An empty cookie does not highlight.
- **Do not write:** Do not say every new nested location is scrolled into view by this cookie.
- **Related:** MAP-005, MAP-013.
- **Code:** `EDITABLE_FIELD.ascx.vb` lines 497–498; `mapApplyPendingNewLocationHighlight`; `mapShowCloneRenameNotice` called from `mapRevealAfterLayout` lines 1476–1477.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Find a location you just added

### MAP-038 — View barcode and attachments (read-only)

- **Open:** Read-only hover **More actions**, then “View Location Details...”. Page `Popups/PeekLocationDetails.aspx?LocationID=`. Signed in. This file has no extra read-only check. An unknown location goes to `Location Error.html`.
- **Steps:**
  1. Click “View Location Details...”.
  2. Click a file name to download it. A stored name longer than 30 characters is shown as the first 20 characters plus `...`, then the extension.
  3. The barcode box is disabled. Click **Print Barcodes** to open `PrintBarcode`.
- **Options:** None.
- **Result:** Download or print. The barcode cannot be edited here. Upload is not wired: the paperclip’s click returns false, and the file input is hidden.
- **If it fails:** None. A missing location redirects with no sentence on this page.
- **Do not write:** Do not say this popup uploads or deletes attachments. Upload and delete are MAP-039.
- **Related:** MAP-002, MAP-039, MAP-040.
- **Code:** `MapProcessEvent_JS` case `READ_ONLY` lines 9241–9244; `PeekLocationDetails.aspx` lines 28–46; `PeekLocationDetails.aspx.vb` `_showAttachments` lines 46–62.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** View a location’s barcode and attachments

### MAP-039 — Attach a file to a location

- **Open:** Location Editor. The paperclip title is “Click to attach file...”. Not read-only.
- **Steps:**
  1. Click the paperclip.
  2. Choose a file. The page posts when a file is present, then reloads the editor.
  3. To delete, confirm “Are you sure you want to delete this attachment?”
- **Options:** None.
- **Result:** The file is stored for that location id, or it is deleted after the confirm. Inventory is unchanged.
- **If it fails:** None. A cancel on the confirm does not delete. A post with no file does not upload.
- **Do not write:** The read-only details popup shows the same paperclip title and does not upload.
- **Related:** MAP-007, MAP-038. WF-006.
- **Code:** `LocationEditor.aspx` line 331 and the confirm at line 311; `LocationEditor.aspx.vb` `_upload_attachment` lines 642–647.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Attach a file to a location

### MAP-040 — Location barcode

- **Open:** Location Editor label “Barcode # (scan to change)”. Print tooltip “Print Barcodes”. The peek barcode (MAP-038) cannot be edited.
- **Steps:**
  1. Click the barcode box. It selects the current value.
  2. Type a new value and press Enter. Enter does nothing if the text equals the saved barcode.
  3. If the barcode is free, it saves and the editor reloads.
  4. If it is already used, the box turns `#AF5756` with white text. There is no alert.
  5. Click **Print Barcodes** to open the print page.
- **Options:** None. The box starts from the barcode stored for this location.
- **Result:** `set_barcode` runs only when `_barcodeExists` is false. Print does not change the barcode.
- **If it fails:** None. A taken barcode is the color change, not a sentence.
- **Do not write:** Do not say the peek barcode can be scanned to change.
- **Related:** MAP-007, MAP-038.
- **Code:** `LocationEditor.aspx` lines 396–405; `LocationEditor.aspx.vb` `hidden_barcode_btn_Click` lines 620–638.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Set or print a location barcode

### MAP-041 — Location kiosk

- **Open:** Location Editor links **Checkin Kiosk** (title “Open Checkin Kiosk”) and **Checkout Kiosk** (title “Open Checkout Kiosk”). They open a new tab. Not available to read-only, because the editor is blocked. If there is no location id, the link stays `#`.
- **Steps:**
  1. Open the editor.
  2. Click **Checkin Kiosk** or **Checkout Kiosk**.
  3. At a viewport wider than 900px the page is `/Popups/QuickScan.aspx`. At max-width 900px it is `/MOBILE_QuickScan.aspx`. The query is `mode=checkin` or `mode=checkout`, plus `locationID`.
- **Options:** Check-in or check-out, locked to this location.
- **Result:** Navigation only. Inventory changes happen in Quick Scan (XFR-011), not on the editor. What Quick Scan’s inventory API does to stock is Uncertain.
- **If it fails:** None.
- **Do not write:** Do not describe the editor links as the Transfer page.
- **Related:** XFR-011. WF-005.
- **Code:** `LocationEditor.aspx` lines 410–415 and `wireKioskLinks` lines 605–620.
- **Confidence:** Confirmed for the links. Uncertain for the Quick Scan API’s stock math.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Open a kiosk for one location

### MAP-042 — Location breadcrumb

- **Open:** `LocationSelector_CONTROL` in the location editor and in the transfer UI. Hover the breadcrumb.
- **Steps:**
  1. The trail starts with **ALL LOCATIONS**. That item relocates to id `-2`.
  2. Hover the breadcrumb. A menu of child locations opens.
  3. Click a location. The host reloads on that id. In the editor, that opens `LocationEditor.aspx?LoadType=EXISTING&LocationID=`.
  4. On a transfer popup, the first click uses the pointer’s x. Left of x=350 is FROM. Otherwise it is TO.
- **Options:** None. A parent filter other than `-2` limits the tree to that parent’s path.
- **Result:** The page moves to the chosen location. Inventory is unchanged by the breadcrumb itself.
- **If it fails:** None.
- **Do not write:** None.
- **Related:** MAP-007, MAP-020, MAP-022. WF-002, WF-004.
- **Code:** `LocationSelector_CONTROL.ascx.vb` breadcrumb line 61; `SetZone` lines 40–49; `LocationEditor.aspx.vb` `CS_LocationSelector1_LocationChanged`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Pick a location from the breadcrumb

### MAP-043 — Create a top-level location from mobile

- **Open:** Mobile home, the **+** tile (aria-label “Add location”). Not the map page. Signed in, and not read-only. The new location’s parent is always `-2` (All Locations).
- **Steps:**
  1. Tap **+**.
  2. The title is “Select a location Type”. Tap **Building**, **Warehouse**, **Store**, **Floor**, **Room**, **Closet**, **Shelf**, **Bin**, or **Vehicle**.
  3. The next title is “New location”. The name box is filled with “New ” plus that type name (for example “New Building”) and the text is selected. Max length is 200.
  4. Click **Create** or **Cancel**. Enter clicks **Create**.
- **Options:** Types 0–8, same meanings as MAP-003. `parentId` sent by this screen is `-2`.
- **Result:** One root location is inserted. Activity `LOCATION__CREATE`. The response is `{ok:true}` or `{ok:false, message}`. This handler does not create a child of another location.
- **If it fails:** “Please enter a name.” “Not signed in.” “Read-only users cannot create locations.” “Invalid location type.” “Invalid parent.” “That location name is already in use.” “Could not verify location name.” “Could not create location.” “Invalid request.” “Method not allowed.”
- **Do not write:** Do not say this screen can parent the new location under a tile. Nested create is MAP-005.
- **Related:** MAP-003, MAP-005. WF-006.
- **Code:** `mobile_main.aspx.vb` `BuildRecentLocationNewTile` lines 581–590; `mobile_main.aspx` titles lines 2913 and 2934, default name lines 2732–2736, post lines 2791–2804; `MobileCreateLocationHandler.vb` lines 27–125.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Create a top-level location from mobile

### MAP-044 — Map on a phone

- **Open:** `Map.aspx` at about 900px or narrower, or with tablet mode on. The control is `Map_CONTROL_2017`. Read-only users still go to `Map_read_only.aspx`. `user-scalable=no` is set so the browser pinch does not fight the map pinch.
- **Steps:**
  1. Open **Map** on a phone. Do not open `Mobile/Map.aspx`.
  2. The zoom track defaults to 0.74 unless this user has saved a mobile zoom (token `-7`).
  3. When the narrow designer touch chrome is on, the first tap selects a location and the bottom bar is **Edit**, **Clone**, **Vertical**, **3D**, **Delete**, and **Close**.
  4. Search shows the **>** button. Multi-select is off. Hover tooltips are off.
  5. A transfer, check-in, or check-out from a location drag or hover opens `MOBILE_Transfer.aspx` as a full page.
- **Options:** None beyond the mobile zoom and tablet mode (MAP-033).
- **Result:** The same locations and the same inventory rules as the desktop map. The layout and the transfer page change. `MapDesignerNaked` sets `DisableMobileView`, which removes the lock, settings, zoom toolbar, ABC sort, shared maps, export, and tablet button from that iframe.
- **If it fails:** None beyond the feature being used.
- **Do not write:** `Mobile/Map.aspx` always redirects to `/_admin/_unauthorized`. `Mobile/ProductEditorMap.aspx` does the same. The 2018 control is not the phone map.
- **Related:** MAP-001, MAP-017, MAP-020, MAP-021, MAP-022, MAP-030, MAP-033.
- **Code:** `Map.aspx` viewport line 9; `Mobile/Map.aspx.vb` lines 4–6; `mapIsMobileFooterSelectionMode` lines 5534–5544; `mapCoordsViewportIsNarrow` lines 2600–2605; `mapOpenInventoryTransferPage` narrow branch.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Use the map on a phone

# XFR — Inventory movement

Walkthroughs for XFR-001 through XFR-012. IDs are unchanged.

These screens have no Adjust control. Batch, lot, expiration, and kitting are not fields on them. A read-only user is sent to `/_admin/_unauthorized` from `Transfer.aspx`, `CheckInCreatedProducts.aspx`, and Quick Scan, and to `/Map_read_only` from Start and from the mobile master.

When a Transfer address contains both `isCheckin=true` and `isCheckout=true`, check-out wins.

Transfer save and Start save do not use the same stock rule. Transfer sets the source to the remaining cookie quantity and adds the moved amount at the destination. Start check-in adds. Start check-out subtracts and stops at 0. The Start comment appears after that stock write.

---

### XFR-001 — Check in

- **Open:** Signed in, not read-only. From the map, drop inventory onto a location to open `Transfer.aspx?isCheckin=true` (a narrow layout opens `MOBILE_Transfer.aspx?isCheckin=true`). The mobile menu **Check In** uses the same page after a location is chosen (XFR-008). The source header reads **CHECK-IN**. The source id is forced to `-2` (the catalog). The destination is a real location. If the saved destination is also `-2`, the page picks another location.
- **Steps:**
  1. Use the box labeled **search or scan**, or scan a barcode into it. The left list is the catalog from `api/search` (`SearchType=1`, limit 250). Each row shows an infinity glyph instead of an on-hand count.
  2. Click a product. One unit moves to the destination.
  3. Click the infinity glyph to open **Check-in quantity**. The prompt is “How many of '{name}' would you like to check in?” The quantity must be at least 1. There is no maximum. **Check In** applies it. **Cancel** closes the box. Enter confirms. Escape cancels.
  4. Drag a catalog row onto the destination. That also moves 1, not the whole catalog.
  5. Drag a destination row back to the source to clear that line. **Clear All (N items)** clears every selected line.
  6. While the destination is still empty, **import file** and **New Products** are available, unless the address has `HideImportFile=true`. A search with no catalog match shows **Create New Product**.
  7. Click **Check In**. The title is “Any comments about this transaction?” An empty box shows **Skip Comment**. Typed text changes the button to **Save**. Enter, Escape, and a click on the backdrop all confirm and continue the save.
- **Options:** The destination is the location selector. The quantity on each line is the amount to add. There is no **Check-In Everything** control. Onboarding can hide the import button with `HideImportFile=true`. Account type 1 is not this quantity path; see **Do not write**.
- **Result:** Save adds the chosen quantity to whatever is already at the destination. The catalog source is not a stock row, so nothing is overwritten there. One check-in activity is stored (`INVENTORY__CHECK_IN`) for the moved quantities, including the comment collected in the previous step. Lines with a moved quantity of 0 are skipped. The comment is collected before the stock write. That is different from Start (XFR-006), where the comment appears after the stock write.
- **If it fails:** “Please enter a quantity of at least 1.” On the update box: “Please enter a quantity of 0 or greater.” A desktop scan or search that misses: “Product Number '{scan}' doesn't exist!” A mobile check-in miss opens Add Products instead of that alert. A read-only user never sees the page.
- **Do not write:** Do not describe this save as a subtract, an overwrite of source stock, or a floor at 0. Do not tell the reader to check in everything from one button. If the address also has `isCheckout=true`, this check-in path does not run; check-out wins (XFR-002). Do not describe MAP-023 as this check-in. Batch, lot, expiration, and kitting are not on this screen.
- **Related:** WF-002. Also WF-001 when new products return here (XFR-007), WF-008 (XFR-005), XFR-006, XFR-008, DEF-001.
- **Code:** `Transfer.aspx` `isTransferCheckinMode`, `TransferOneItem`, `drop`, `showTransferQtyModal`; `Transfer.aspx.vb` `Page_Init` (check-out wins, then source forced to `-2`); `TransferFunctions.TransferProductsBackend` (source `-2` adds `QuantityDest` to the existing destination quantity).
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Check products in from the catalog

### XFR-002 — Check out

- **Open:** Signed in, not read-only. From the map, drag a location toward **Check out** (“Drag inventory here to check out”). That opens `Transfer.aspx?isCheckout=true`, or `MOBILE_Transfer.aspx?isCheckout=true` on a narrow layout. The destination header reads **CHECKOUT** and the destination id is forced to `-2`. The left list is stock at the source.
- **Steps:**
  1. Search or scan in **search or scan**. The list loads stock at the source, 250 rows at a time. A product with quantity 0 is left off the list unless that product is already in the destination selection.
  2. Click a product. One unit moves, and only up to the on-hand amount.
  3. Click the quantity to open the quantity box. In check-out the add box still says **Transfer quantity** and “How many of '{name}' would you like to transfer? (Max: {max})”, and its button still says **Transfer**. The update box says **Update quantity** and “Enter the updated quantity for '{name}' to check out. (Max: {max})”, and its button says **Update**.
  4. Drag a row onto the destination to move all of the remaining quantity. Drag it back, or use **Clear All (N items)**, to return it.
  5. **Check-Out Everything** loads the location in pages of 500 and moves every remaining unit. Its tooltip is “Check out all the products in this location”. The label includes “(N shown)” when rows are on screen. The control is hidden while the map-filter badge is on.
  6. Click **Check Out**, then confirm “Any comments about this transaction?” **Skip Comment** or **Save** works the same way as check-in: Enter, Escape, and the backdrop confirm.
- **Options:** When the address has both `isCheckin=true` and `isCheckout=true`, this check-out path is the one that runs. The destination stays `-2`. A partial line is marked on the source row while some quantity remains there and some is selected.
- **Result:** Save sets the source stock of each moved product to the remaining cookie quantity. That is an overwrite of the source row, not a subtract from the current database quantity. The destination is not a location, so nothing is added. The check-out activity (`INVENTORY__CHECK_OUT`) stores the moved quantities, not the remaining quantity. The comment is collected before that write.
- **If it fails:** “Product '{term}' was not found at this location.” “Please enter a quantity of 0 or greater.” “Please enter a quantity up to {max}.” An import that asks for more than is on hand shows the tooltip “Only {available} items were available at this location. Quantity adjusted from {requested} to {available}”.
- **Do not write:** Do not say this page subtracts and floors at 0. That rule belongs to Start check-out (XFR-006) and to the legacy mobile handlers (XFR-008). Do not describe a one-unit click here as MAP-023. MAP-023 sets that SKU’s source stock to 0.
- **Related:** WF-003. MAP-021, XFR-003, XFR-005, XFR-006, XFR-008, DEF-002.
- **Code:** `Transfer.aspx` `TransferEverything`, `refreshTransferEverythingLabel`, `transferFetchAllLocationProducts` (page size 500); `Transfer.aspx.vb` `Page_Init` checkout branch; `TransferFunctions.TransferProductsBackend` (destination `-2` writes `QuantitySrc` onto the source).
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Check products out of a location

### XFR-003 — Transfer between two locations

- **Open:** Signed in, not read-only. Drop a location, or a product row, onto a different location on the map. Desktop opens `Transfer.aspx` in a popup. A narrow layout opens `MOBILE_Transfer.aspx`. Both locations are real. The same location, or a destination of `-2`, is not this transfer. The mobile menu **Transfer** is the same page after both locations are chosen (XFR-008).
- **Steps:**
  1. Confirm the two location selectors name different places. Picking the same place on this page does nothing: the selectors keep the previous pair and show no message.
  2. Search or scan the source list. It is on-hand stock at the source, 250 at a time. Quantity 0 stays hidden unless that product is already selected.
  3. Click a product to move 1, up to on-hand. Click the quantity for **Transfer quantity** / “How many of '{name}' would you like to transfer? (Max: {max})” and **Transfer**. A later edit says **Update quantity**, “Enter the updated quantity for '{name}' to transfer. (Max: {max})”, and **Update**.
  4. Drag a row to move all remaining. A line that is only partly moved uses the partial-count style on the source row. Drag back or **Clear All (N items)** to undo.
  5. **Transfer Everything** follows the same all-remaining behavior as **Check-Out Everything**, including the 500-row pages, and hides while the map-filter badge is on. Tooltip: “Transfer all the products in this location”.
  6. Click **Transfer**. There is no **New Products** button on this mode. Then confirm “Any comments about this transaction?” with **Skip Comment** or **Save**.
- **Options:** Source and destination must differ. The Start page selector, which is a different screen (XFR-006), shows “The Source can't be the Destination!” and “Please select a Destination.” when the same place is picked twice.
- **Result:** Save sets source stock to the remaining cookie quantity (overwrite) and sets destination stock to the quantity already there plus the amount moved. One transfer activity (`INVENTORY__TRANSFER`) stores the moved quantities. The comment is collected before that write. A one-unit click on this page keeps the rest at the source. That is a different action from the map’s one-unit move.
- **If it fails:** “Product '{term}' was not found at this location.” “Please enter a quantity of at least 1.” “Please enter a quantity of 0 or greater.” “Please enter a quantity up to {max}.” The import tooltip is the same on-hand sentence as check-out.
- **Do not write:** Do not describe MAP-023 as this partial move. MAP-023, when the dragged quantity is exactly 1, sets that SKU’s source stock to 0. Do not say this page subtracts from the source and then adds. The source write is the remaining cookie quantity.
- **Related:** WF-004. MAP-022. MAP-023 is related only as the one-unit map move that zeros source stock. XFR-002, XFR-005, XFR-006, XFR-008, XFR-009, DEF-001, DEF-002.
- **Code:** `Transfer.aspx` `TransferFunction`, `TransferEverything`; `Transfer.aspx.vb` `LocationSelector_Source_LocationChanged`, `LocationSelector_Destination_LocationChanged` (same id exits without a redirect); `ProductSelector.aspx.vb` for the Start sentence; `TransferFunctions.TransferProductsBackend`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Transfer products between two locations

### XFR-004 — Quantity adjust is not a Transfer mode

- **Open:** Transfer (`Transfer.aspx`), Start (`Start.aspx`), and the mobile process (`MOBILE_Process.aspx` / `MOBILE_Transfer.aspx`). Signed-in movement screens. There is no query flag that turns any of them into an adjust mode.
- **Steps:**
  1. Open check-in, check-out, or transfer on Transfer, Start, or mobile.
  2. There is no Adjust button and no `isAdjust` mode. The save buttons are **Check In**, **Check Out**, or **Transfer**.
- **Options:** None. These handlers never register activity 25 (`INVENTORY__ADJUST`).
- **Result:** A completed save is a check-in, a check-out, or a transfer. The source and destination quantities follow XFR-001, XFR-002, XFR-003, or XFR-006. No adjust activity is written from these pages.
- **If it fails:** None. There is no adjust action on these screens to fail.
- **Do not write:** Do not write an adjust walkthrough for Transfer, Start, or mobile movement. The word “adjusted” on Transfer is only the import warning that a requested quantity was cut to on-hand (XFR-005): “Only {available} items were available at this location. Quantity adjusted from {requested} to {available}”. Quantity adjust that does exist is MAP-026 and PRD-010.
- **Related:** WF-004 (this is not that workflow). MAP-026, PRD-010, XFR-001, XFR-002, XFR-003, XFR-005.
- **Code:** `Transfer.aspx.vb` `Page_Init` (only `isCheckout` and `isCheckin`); `Activity.vb` `INVENTORY__ADJUST = 25` is registered from the map and the product list, not from `TransferFunctions`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Quantity adjust is not a transfer mode

### XFR-005 — Import a file into a movement

- **Open:** On check-in, check-out, or transfer, before any quantity is in the destination list. The button label is **import file** (tooltip “Import from file”). It is hidden once the destination selection is not empty, and it is hidden entirely when `HideImportFile=true`. Signed in, not read-only.
- **Steps:**
  1. Click **import file**. The page goes to import with the current source, destination, and mode.
  2. Match rows by product number when the match field is blank or `PN`, by product name when it is `DESC`, or by custom field `CF_{index}`.
  3. Return with `ApplyImportedTransfer=1`. The page locks into review. Search, drag, and the source list stay locked until you save or cancel. The status title is **Success!**, **Import Failed**, or **No items imported**.
  4. On **Success!** with at least one row, click the mode button: **Check In**, **Check Out**, or **Transfer**. Then confirm the comment. If you did not edit the selection, the comment gains `{{cs-file-import}}`.
  5. **Cancel** closes the page and does not commit the movement.
- **Options:** Check-in keeps the requested quantity and does not warn that a product is missing at the location. Check-out and transfer require on-hand stock and cut the line down when the file asks for more. A cut line shows “Only {available} items were available at this location. Quantity adjusted from {requested} to {available}”. More than one match is skipped. The save activity is still the host mode’s activity (check-in, check-out, or transfer), with that mode’s stock rule.
- **Result:** A successful save writes the same stock change as the host mode: check-in adds at the destination (XFR-001), check-out overwrites the source to the remaining quantity (XFR-002), transfer overwrites the source to the remaining quantity and adds at the destination (XFR-003). Cancel writes nothing. The review box can show “{n} rows imported”, “{n} adjusted quantities”, and “{n} rows skipped”.
- **If it fails:** “The file could not be read. Please upload it again.” “The file did not contain any products.” “The file could not be checked. Please try the import again.” “No quantity was provided for this product.” “Quantity is missing.” “Quantity must be a whole number.” “Quantity must be greater than 0.” “This value matched more than one product in {field}.” “This product number was not found in your catalog.” “This value was not found in {field}.” “This product was not found at the source location.” “None of this product is available at the source location.” “The requested quantity is not available at the source location.” **Import Failed** adds “Please retry importing your file.” and **Retry Import**. Warnings offer **Upload Corrected File**. Check-in does not show the “not found at the source location” warning.
- **Do not write:** Do not say this import creates products. Creating products is a different import (WF-007). Do not say the word “adjusted” here is an adjust activity. Do not apply the Transfer overwrite rule to a file that was sent into Start; Start then uses its own add or subtract (XFR-006).
- **Related:** WF-008. WF-002, WF-003, WF-004. XFR-001, XFR-002, XFR-003, XFR-006, PED-014.
- **Code:** `Transfer.aspx.vb` `BuildImportedTransferSelectionString`, `ReadImportMatchField`; `Transfer.aspx` `renderImportStatusBox`, `isTransferInteractionLocked`, `buildTransferCommentWithImportTag`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Import a file into a check-in, check-out, or transfer

### XFR-006 — Start page

- **Open:** `Start.aspx`. Signed in, not read-only. Read-only goes to `Map_read_only`. The greeting is “Hello {first name}! What would you like to do?” With no products, the menu is hidden and the page shows “You have not added any products yet” and **Click to create**. With products, the menu pictures are Create, Check In, Transfer, Check Out, and Quick Scan. An address with `checkin`, `checkout`, `transfer`, or `add`, plus `id`, opens that action. Check-in, check-out, and transfer are hidden from the mobile menu when the account has no products; Quick Scan stays (XFR-012). This Start menu is the desktop page.
- **Steps:**
  1. Click **Check In**. The selector title is **Check In**, subtitle “Add Products to a Location”, then “Please select a Check In Location.” The default is the user’s check-in location (DEF-001). `ProcessName` is `ADD`.
  2. Click **Check Out**. Title **Check Out**, “Remove Products from a Location”, “Please select a Check Out Location.” Default is the check-out location (DEF-002). `ProcessName` is `CHECKOUT`.
  3. Click **Transfer**. Title **Transfer**, “Move Products between Location”, “Please select a Source Location for the Transfer.” Then pick a destination. If the same place is picked twice: “The Source can't be the Destination!” and “Please select a Destination.”
  4. Click **Create** to open Add Products with `LastPage=Start` (WF-001). Click Quick Scan for XFR-011.
  5. Choose products and finish. The hidden finish button is labeled **Finish**.
  6. After the quantity is written, the page shows “Success!” and “You can leave a brief comment if you like.” The box placeholder is “Any comments about this transaction?” Click **Save Comment** to store the comment and open the Map.
- **Options:** Check-in adds the chosen quantity at the location. Check-out subtracts the chosen quantity and does not go below 0. Transfer subtracts from the source and adds that quantity at the destination. A file import that already named locations uses those locations instead of the single selector. Account type 1 does not use these quantity updates; it uses the records assignment.
- **Result:** Standard accounts (account type 0) write one activity: check-in, check-out, or transfer. The stock change is already stored when “Success!” appears. **Save Comment** only appends the comment onto that activity and then opens the Map. Leaving the comment box does not undo the stock change. This is not the Transfer-page overwrite. Transfer sets the source to the remaining cookie quantity; Start check-out subtracts, and Start check-in adds.
- **If it fails:** Check-in and check-out exit without saving when the location cookie cannot be read. The same-location transfer selector shows “The Source can't be the Destination!” A read-only user is sent to `Map_read_only`.
- **Do not write:** Do not say the Start comment is collected before the stock write. Do not copy the Transfer overwrite rule onto this page. Do not document account type 1 as add, subtract, or overwrite. Product-selector field details stay under PED-016.
- **Related:** WF-002, WF-003, WF-004, WF-001, WF-005. XFR-001, XFR-002, XFR-003, XFR-007, XFR-011, DEF-001, DEF-002, PED-016.
- **Code:** `Start.aspx` menu images and `ShowComments`; `Start.aspx.vb` `FinishAddHandler` (`OverwriteQuantity` false, so add), `FinishCheckoutHandler` (`CHECKOUT` true, so subtract with a floor of 0), `btn_transfer_complete_Click` (subtract, then add), `btn_comment_save_Click` (`WriteComment`, then redirect to Map). `Product.UpdateProductLocationQuantity`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Check in, check out, or transfer from Start

### XFR-007 — Check in products just created

- **Open:** `CheckInCreatedProducts.aspx` after products are created (WF-001). Signed in, not read-only. Read-only goes to `/_admin/_unauthorized`. The catalog rows already exist. This page either adds stock or sends the lines back to an open check-in. It does not create the products.
- **Steps:**
  1. Standalone, with no imported location on every line: the title is “1 Product created.” or “{n} Products created.” The map prompt is “Click a location to Check it in.” or “Click a location to Check them in.” The selected location starts as the query `loc` when that location exists, otherwise the user’s check-in default (DEF-001).
  2. Set each quantity to a whole number, 0 or greater, and at least one line to 1 or more. The quantity title is “This quantity will be checked in to the selected location.”
  3. Click **Check in**. The comment box is “Any comments about this transaction?” **Cancel** closes it without saving. An empty box uses **Skip Comment**. Typed text switches the button to **Save**. Confirming writes the check-in.
  4. **Skip check-in** closes the page and does not call the save. The products stay in the catalog with no stock added here.
  5. When every imported line already has a real location, the map is hidden. Each line shows its location path, and the quantity title is “This quantity will be checked in to this location.” **Check in** saves each line to its own location.
  6. When this page was opened from an open transfer, there is no map. The title is “1 Product was created. Set the quantity, then continue.” or “{n} Products were created. Set quantities, then continue.” **Skip ››** drops the batch and returns to Transfer. **Continue** rewrites the quantities and returns with `ApplyCreatedCheckIn=1`.
- **Options:** A generated product number shows “1 product number was generated.” or “{n} product numbers were generated.” Lines with quantity 0 are omitted from the save. A file-origin batch can append `{{cs-file-import}}` to the comment.
- **Result:** Standalone save adds the quantities at the one chosen location and writes one check-in activity. Imported-location save adds each line at its own location and writes one check-in activity with a location per line. The done page reloads the parent window, or goes to `/Products.aspx` when there is no parent. **Continue** from an open transfer does not change stock on this page. Stock changes on the later Transfer save (XFR-001). **Skip check-in** and **Skip ››** do not check anything in.
- **If it fails:** “No products are waiting to be checked in.” “Each quantity must be a whole number, 0 or greater.” “Select a location on the map before checking in.” “Enter a quantity of at least 1 for one product.” “A location in this import could not be found.” One unusable imported location aborts the whole save. A destination of `-2` does not save.
- **Do not write:** Do not say **Continue** checks the new products in. Do not say **Skip check-in** deletes the new catalog rows. Do not describe this page as the Transfer overwrite.
- **Related:** WF-001. XFR-001, XFR-005, PED-010, PED-013, DEF-001.
- **Code:** `CheckInCreatedProducts.aspx.vb` `Page_Init`, `btn_checkin_Click`, `btn_continue_transfer_Click`, `SaveImportedLocationCheckIn`, `ShowQueryError`; `CreatedProductCheckIn.vb` `SaveCheckIn`, `SaveCheckInAtLineLocations` (both add, `OverwriteQuantity` false); `CheckInCreatedProductsDone.aspx`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Check in products you just created

### XFR-008 — Mobile check-in, check-out, and transfer

- **Open:** Mobile menu **Check In**, **Check Out**, or **Transfer** (XFR-012). Signed in, not read-only; the mobile master sends a read-only user to `/Map_read_only`. The cookie `MOBILE_Process` is `CHECK_IN`, `CHECK_OUT`, `TRANSFER`, or `LOCATIONS` (view only, XFR-009). These three movement items are hidden when the account has no products.
- **Steps:**
  1. Pick the location or locations (XFR-009). Check-in needs a destination. Check-out needs a source. Transfer needs both. The page says “Click to change” or, for transfer, “Click to change Source” and “Click to change Destination”.
  2. When `MOBILE_ListOfProducts` is empty, the page sends you to `MOBILE_Transfer.aspx` with `isCheckin=true`, `isCheckout=true`, or neither. Choose products with the same clicks, drags, and **Check In** / **Check Out** / **Transfer** labels as XFR-001, XFR-002, and XFR-003.
  3. Confirm “Any comments about this transaction?” Save goes to `MOBILE_Process.aspx?CommitTransfer=1`.
  4. **Save location** on the older process chrome alerts “The location(s) will be saved for next time” and stores a check-in or check-out default. It does nothing when both a source and a destination are already set, so a transfer does not replace a saved default.
- **Options:** A return path that contains `.aspx` and does not contain `..` is where the page goes after a committed transfer. The token `Map`, with no `.aspx`, falls through to mobile home. Opening mobile home clears the in-progress process cookies (XFR-012).
- **Result:** The live path uses `TransferProductsBackend`. Check-in adds at the destination. Check-out overwrites the source to the remaining cookie quantity. Transfer overwrites the source to the remaining quantity and adds that amount at the destination. Mobile home then shows “Check-in completed successfully.”, “Check-out completed successfully.”, or “Transfer completed successfully.”
- **If it fails:** The Transfer page failures in XFR-001, XFR-002, and XFR-003. A return path that contains `..` is not used.
- **Do not write:** Do not document the legacy product-list handlers as the path a new mobile check-in follows. Those handlers run only when `MOBILE_ListOfProducts` is already filled. They add on check-in, subtract and floor at 0 on check-out, and subtract-then-add on transfer, and their comment box (“Add a comment?”, **Skip**, **Save**) is confirmed before that write. The current process page does not open that product list by itself (XFR-010). Do not say **Save location** updates defaults during a transfer.
- **Related:** WF-002, WF-003, WF-004. XFR-001, XFR-002, XFR-003, XFR-009, XFR-010, XFR-012, DEF-001, DEF-002.
- **Code:** `MOBILE_Process.aspx.vb` `CompleteMobileTransferFlow`, `RedirectToMobileTransferIfNeeded`, `CheckIN_Handler`, `CheckOUT_Handler`, `TRANSFER_Handler`, `btn_setDefault_location_Click`; `Transfer.aspx` `finishSaveAndCloseAfterComment`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Check in, check out, and transfer on mobile

### XFR-009 — Mobile location picker

- **Open:** `MOBILE_LocationSelector.aspx` while a mobile process still needs a location (XFR-008). `LocationType=Source` for check-out and for the transfer source. `LocationType=Destination` for check-in and for the transfer destination. `LocationType=Contents` for view-only contents. Signed in through the mobile master.
- **Steps:**
  1. The list is the location tree starting at parent `-2`. Expand a row with **+** (“Show or hide sub-locations”).
  2. For a source or contents list, the check-out default is pre-selected when that location still exists. For a destination list, the check-in default is pre-selected.
  3. Tap a location. Source and contents write `MOBILE_SourceID`. Destination writes `MOBILE_DestinationID`. The page returns to `MOBILE_Process.aspx`.
  4. The badge **default** switches to **change**. **change** opens the Settings location picker. If that popup cannot open, the page goes to `Settings#DefaultLocations`.
- **Options:** Contents (`MOBILE_Process` = `LOCATIONS`) is view-only. **Save location** is hidden, and the header becomes the location name. A stored default that no longer exists is ignored and the list starts at `-2`.
- **Result:** The chosen id is the source or destination for the movement that follows. Contents shows what is in the location and does not start a check-in, check-out, or transfer. Changing the default badge updates the user’s default location through Settings, not through the movement save.
- **If it fails:** None on the picker itself. A missing location sends the process page back to this picker.
- **Do not write:** Do not say tapping a location in Contents checks stock in or out. Do not say the **default** badge is the same control as **Save location** on the process page.
- **Related:** WF-004. XFR-008, XFR-012, DEF-001, DEF-002.
- **Code:** `MOBILE_LocationSelector.aspx.vb` `LoadLocations`, `DisplayChildren` (`-2`), `SetLocation` via `MOBILE_LocationSelector.aspx`; `MOBILE_Process.aspx.vb` `LOCATIONS` branch.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Pick a mobile check-in or check-out location

### XFR-010 — Legacy mobile product list and Quick Add

- **Open:** `MOBILE_ProductSelector.aspx` writes product cookies and returns to the process page, which then uses the legacy handlers (XFR-008). The current process page does not open this list by itself when the product cookie is empty; it opens `MOBILE_Transfer.aspx` instead. Progress **back** and Quick Add’s return URL still land here. The search box says “Scan or Search...”
- **Steps:**
  1. Press Enter on a row that is already on the list. That row’s quantity increases by 1.
  2. Scan a value the list does not know. If the search result category is `FALSE`, the page opens `MOBILE_QuickAdd.aspx` with that product number.
  3. On Quick Add, the description box placeholder is “Description...”. Click **CREATE** or **CANCEL**.
- **Options:** **CREATE** saves even when the description is empty. The new product is created at location `-2` (not placed). The activity is `PRODUCT__CREATE` with quantity 1. **CANCEL** goes back without creating.
- **Result:** **CREATE** adds a catalog product and returns to the product selector. It does not check the product in and does not place it at a location. A later save from the filled product-list cookie uses the legacy add, subtract-and-floor, or subtract-then-add handlers, not `TransferProductsBackend`.
- **If it fails:** An unknown scan whose category is not `FALSE` is added to the list from the search result. A category of `FALSE` leaves the list and opens Quick Add. No separate error sentence is shown for that miss.
- **Do not write:** Do not tell a mobile user to start Check In, Check Out, or Transfer and expect this list. That path opens the Transfer page. Do not say Quick Add checks the new product in. Quick Scan does not create products either (XFR-011).
- **Related:** WF-005. XFR-008, XFR-011, PED-010.
- **Code:** `MOBILE_ProductSelector.aspx` `Try2Scan`; `MOBILE_QuickAdd.aspx` **CREATE** / **CANCEL**; `MOBILE_QuickAdd.aspx.vb` `btn_create_product_Click`; `Controls/MOBILE_ProcessProgress.ascx.vb` back step to `MOBILE_ProductSelector.aspx`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Legacy mobile product list and Quick Add

### XFR-011 — Quick Scan

- **Open:** Start menu Quick Scan opens `Popups/QuickScan.aspx`. The mobile menu **QuickScan** opens `MOBILE_QuickScan.aspx`, which frames the same page. The location editor can open it as a kiosk with `mode=checkin` or `mode=checkout` and a positive `locationID` (MAP-041). Signed in, not read-only. Read-only goes to `/_admin/_unauthorized`. Quick Scan stays available when the account has no products.
- **Steps:**
  1. The instruction is “Scan a product or location”. The field placeholder is “ready to scan...”.
  2. Scan a product. The first scan adds it with a count of 1. Scanning it again adds 1 to that count. The columns are labeled **Source**, **Products**, and **Destination**.
  3. Scan a location. The first location fills **Source**. The next fills **Destination**. Scanning a location that is already source or destination swaps the two. Scanning another location when both are filled shifts the previous source into the destination.
  4. The mode is derived on the page. Source only shows **Check Out**. Destination only shows **Check In**. Both show **Transfer**. Otherwise the save button stays hidden.
  5. Optional text uses the placeholder “Optional comment...”. Enter in that box saves. Click **Check In**, **Check Out**, or **Transfer**. On the mobile frame the button says **Save**.
  6. Kiosk: the instruction becomes “Scan products to check in” or “Scan products to check out”. The location is already filled, its delete control is hidden, and location scans are ignored. `transfer` is not a kiosk mode. A query that is not `checkin` or `checkout` with a positive whole-number `locationID` stays on normal Quick Scan.
- **Options:** The save posts `api/inventory?action=checkin`, `checkout`, or `transfer`, with each line’s product, source, destination, and on-screen count. Check-in sends source `-2`. Check-out sends destination `-2`. The comment is sent with the post. What that API does to stock, and which activity it writes, is Uncertain. This page does not call `TransferFunctions`.
- **Result:** Desktop success shows “{N} Transactions completed successfully.” The mobile frame shows “Transaction saved”. The list then clears, except a kiosk, which reloads the same locked location. The page does not show an on-hand balance before the post.
- **If it fails:** “You have to select at least one location and one product!” “Kiosk mode is active; location and mode are fixed.” “There was a problem saving the transaction!” A scan request that fails shows no message and leaves the field unchanged. There is no create-on-scan.
- **Do not write:** Do not state that Quick Scan adds, subtracts, overwrites, or floors stock. The API stock math is Uncertain. Do not say a missing barcode creates a product. Do not describe kiosk transfer; that query is ignored and the page stays in normal Quick Scan.
- **Related:** WF-005. XFR-006, XFR-010, XFR-012, MAP-041.
- **Code:** `Popups/QuickScan.aspx` `getTransactionType`, `apiPostTransaction`, `processScan`, `parseFixedModeFromQuery`, `applyKioskInstructionText`; `Scripts/Popups/QuickScan/QuickScan.js` `showCheckin`, `showCheckout`, `showTransfer`; `Popups/QuickScan.aspx.vb` `Page_Init`.
- **Confidence:** Confirmed for the page. Uncertain for the API stock math and the activity it writes.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Use Quick Scan and the location kiosk

### XFR-012 — Mobile home

- **Open:** Mobile **Home** (`MOBILE_main` / `mobile_main.aspx`). Every load clears the movement cookies: process, source, destination, product list, and return path. A read-only user is redirected by the mobile master to `/Map_read_only` before this menu is shown.
- **Steps:**
  1. Open the menu. The links are **Home**, **Map**, **Products**, **Activity**, then **Check In**, **Check Out**, and **Transfer** when the account has at least one product, then **QuickScan**, **Help**, **Settings**, and **Logout**.
  2. After a location is primed, the footer shows **Check In**, the product-list icon (“View products in selected location”), and **Check Out**.
  3. **Check In** and **Check Out** set `MOBILE_Process` and open the process page (XFR-008). The list icon opens Products for that location.
- **Options:** **Check In**, **Check Out**, and **Transfer** are omitted from the menu when the product count is 0. **QuickScan** remains. There is no footer **Transfer**. An empty recent-location list says “No recent locations.”
- **Result:** Opening Home clears an in-progress mobile movement, so a later Check In, Check Out, or Transfer starts at the location picker again. The footer check-in and check-out use the primed location as the destination or source.
- **If it fails:** None. A read-only user does not get this menu.
- **Do not write:** Do not tell the reader to resume a half-finished mobile transfer by opening Home. That load clears it. Do not add a footer Transfer step.
- **Related:** WF-002. XFR-008, XFR-009, XFR-011.
- **Code:** `mobile_main.aspx` `Process`, footer **Check In** / **Check Out**; `MOBILE_main.aspx.vb` `ResetCookies`; `MOBILE_MasterPage.master` menu links and `HideInventoryActionsWhenAccountHasNoProducts`.
- **Confidence:** Confirmed.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Mobile home movement menu

# Products walkthroughs

Tutorial steps for the product list and the product editor, create, import, and label screens. IDs match `FEATURE_CATALOG.md` and are not renumbered. Page size is 50. Location `-2` is ALL LOCATIONS. Read-only users do not stay on `Products.aspx`; they use `Products_read_only.aspx`.

29 entries: PRD-001 through PRD-011, PED-001 through PED-018.

## PRD — Product list

### PRD-001 — Product list

**Open:** Products, from the inventory menu, for a signed-in user who is not read-only. A read-only user who opens Products is sent to `Products_read_only`. The location selector (desktop) or the location path (narrow screens, 900px and under) shows the current location. `-2` is ALL LOCATIONS.

**Steps:**
1. Open Products.
2. Leave the location on ALL LOCATIONS, or choose one location.
3. Read the grid. A chosen location lists products whose quantity at that location is greater than 0. If that list is empty and a child location has stock, the page shows the child rows and the sentence “This location is empty but its sub-locations are not”.
4. On ALL LOCATIONS, products with quantity 0 are appended after the in-stock rows when Zero Quantity Products (DSP-003) is on. When that setting is off, rows whose quantity is 0 are left out.
5. The first visit sorts by product number, ascending. A later visit restores the page, sort direction, and sort column from the keep-view cookie.

**Options:** Location: ALL LOCATIONS (`-2`) or one real location. DSP-003, Zero Quantity Products, controls whether zero-quantity rows stay on ALL LOCATIONS. Default sort is product number ascending (direction `0`). The keep-view cookie stores `page|direction|column`.

**Result:** The grid shows up to 50 products for the current page. Cost value in a row is that row’s quantity times its buy price and is calculated for display. The keep-view cookie is rewritten with the page, direction, and column.

**If it fails:** None on the list itself. A read-only user never sees this page.

**Do not write:** A quantity of 0 at ALL LOCATIONS is still subject to DSP-003. The sub-location sentence is a summary banner; quantity cells in that summary are not the quick-edit cells in PRD-010.

**Related:** PRD-002, PRD-004, PRD-005, DSP-003, WF-013

**Code:** `Products.aspx.vb` `Page_Init` (read-only redirect, lines 50–52), `GRIDVIEW_INIT` (page size 50 and keep-view cookie, lines 90–123), `InventoryGetAndDisplay` (lines 1557–1707), `InventoryExtractFromRawSimplified` (`SHOW_ZERO_QUANTITY`, lines 1846–1850). `PageSize` is 50 at line 39.

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** View the product list

### PRD-002 — Empty list

**Open:** Products, or the read-only product list, when the grid has no rows to show. The message depends on ALL LOCATIONS, a single location, or a search.

**Steps:**
1. Open Products with no products in the account and the location on ALL LOCATIONS. The page shows “No products yet” and “Click to create”.
2. Click that message. It opens Add Products (`AddProducts.aspx?LastPage=Products`).
3. Choose a real location that has no stock in it or in its children. The page shows “Location is empty...” and “Click to Check in”.
4. Click that message. It opens check-in for that location (`Start.aspx?checkin=true&id=` plus the location id).
5. Search and get no rows. The page shows “No matches found!” and hides “No products yet”.

**Options:** None. The three messages are chosen by the page.

**Result:** ALL LOCATIONS with an empty catalog offers create. An empty location offers check-in. A search with no hits stays on the list and shows the no-matches sentence. When children have stock, PRD-001’s sub-location banner is used and this empty-location message stays hidden.

**If it fails:** The sentences above are the empty states. There is no separate error alert.

**Do not write:** “Click to create” on a single empty location. That location’s action is “Click to Check in”.

**Related:** PRD-001, PRD-006, PRD-011, PED-010, WF-001

**Code:** `Products.aspx` empty blocks (lines 737–754). `Products.aspx.vb` `MessageNoProductsShow` (lines 243–256) and the search assignment `lbl_no_result_A.Text = "No matches found!"` (lines 1644–1646).

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** What an empty product list means

### PRD-003 — Columns

**Open:** Products. Hover the columns icon, tooltip “Select the columns to display in your inventory”. The same menu exists for a read-only user. EDIT COLUMNS is visible only for an Admin.

**Steps:**
1. Hover the columns icon.
2. Check or uncheck a column. Product Number stays checked; its checkbox cannot be cleared.
3. Drag a checked column name in that menu to change the order. Product Number is fixed at the front of the default set.
4. Click SAVE COLUMNS. The order is stored on this user and the list reloads, keeping the current page and sort.
5. An Admin can click EDIT COLUMNS. That closes the menu and opens the custom-field editor.

**Options:** Columns: Product Number (always on), Quantity, Description (stored as Product Name), Buy Price, Sell Price, each custom field, and Cost Value. Buy Price, Sell Price, and Cost Value show the account currency in the header, for example “Buy Price (USD)”. Default when nothing valid is stored: Product Number, Quantity, Product Name, Buy Price, Sell Price, Cost Value, then every custom field. Cost Value is quantity times buy price, calculated when the row is drawn, and is not a stored product column. Prices use the account currency. An empty description displays `UNTITLED (Product Number : {number})`.

**Result:** SAVE COLUMNS writes this user’s `ColumnOrder` in `CS_ADMIN.Users` and in the ColumnOrder cookie. The grid headers follow that order. A missing or broken stored order is replaced by the default and the page reloads.

**If it fails:** None. A stale column name causes the page to restore the default set.

**Do not write:** A separate camera button on this toolbar. The image toggle markup is commented out. Hiding photos is DSP-002, not a products-toolbar control.

**Related:** PRD-001, PRD-004, PRD-009, DSP-002, CFL-002

**Code:** `Products.aspx` columns menu (lines 567–609) and `#ColumnsSortable` (lines 1269–1278). `Products.aspx.vb` `GetCheckboxMarkup`, `ColumnsDefaultDisplay` (lines 692–727), `btn_ColumnAdjust` (lines 730–734), header labels including “Description” (lines 891–923), untitled description (lines 991–998). Admin gate: `ph_edit_columns.Visible` (lines 54–56).

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Choose product list columns

### PRD-004 — Sort

**Open:** Products, on any visible column header. Headers are Product Number, Quantity, Description, Buy Price, Sell Price, each custom field name, and Cost Value, for the columns that are turned on.

**Steps:**
1. Click a column header. The list sorts ascending and returns to the first page.
2. Click the same header again. The direction flips and the list returns to the first page.
3. Open Products again later. The keep-view cookie restores that column and direction.

**Options:** Direction starts ascending. The same header toggles ascending and descending. Quantity sorts by the sum of quantity. Cost Value sorts by that sum times buy price. Product number is the default when the sort is still “DEFAULT”.

**Result:** The grid reloads on page 0 in the new order. The sorted header shows an ascending or descending indicator. Page, direction, and column are written to the keep-view cookie.

**If it fails:** None.

**Do not write:** A sort that keeps the current page. Every header click sets the page index to 0.

**Related:** PRD-001, PRD-003, PRD-005

**Code:** `Products.aspx.vb` `GridView1_Sorting` (lines 1085–1113), `GetColumnNameFromIndex` (lines 1034–1042), `HeaderTextWithSortIndicator` (lines 1056–1068).

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Sort the product list

### PRD-005 — Pages and select all

**Open:** Products, when the list is not in search. The pager is the numeric control with first and last, at the top and bottom of the grid. It is hidden while a search is active and when the count is 50 or less.

**Steps:**
1. When more than 50 products are in the count, use the page numbers, First Page, or Last Page. Each page shows 50 products.
2. Click the checkbox in the header row. Every checkbox on this page is selected. When the pager is showing, the line reads “The {n} Products on this page are selected” and offers “Select all {full count} products.”
3. Click “Select all {full count} products.” The line changes to “All {full count} Products in your inventory are selected” and offers “Clear selection.”
4. Click “Clear selection” to return to the current page only, or clear the header checkbox to drop the selection.

**Options:** Page size is 50. First click of the header checkbox selects the current page. “Select all {full count} products” selects every product in the account. That set is the whole product table. It is not limited to the current location or to a search. During search the pager is hidden, so the select-all-in-the-account link is not offered.

**Result:** Page changes reload the grid and store the page in the keep-view cookie. The account-wide flag is what delete, multi-edit, and barcode print use when it is on.

**If it fails:** None on the pager.

**Do not write:** Later pages as a strict window of 50 rows. The SQL limit string is `LIMIT {page*50}, {page*50+50}`, which MySQL reads as an offset plus a growing row count. Also do not write select-all as “everything in this location” or “everything in this search.”

**Related:** PRD-001, PRD-006, PRD-011, PED-015

**Code:** `Products.aspx` pager settings (line 834), `SelectAllCheckboxes1` and `select_all_complete` (lines 1206–1266). `Products.aspx.vb` `PageSize = 50` (line 39), `GridView1_PageIndexChanging` (lines 675–680), search pager suppression (`VirtualItemCount = 1`, `hidden_HasPagination = "0"`, lines 1637–1642), `CheckedProductsGelCompleteInventoryList` (lines 2040–2052).

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Page through products and select all

### PRD-006 — Search the product list

**Open:** The header search, on any signed-in page, or a `?Search=` link that opens Products. Read-only users can search; they land on the read-only list after the redirect.

**Steps:**
1. Type a term in the header search and press Enter. The term is appended to the product-search cookie and Products opens.
2. Read the chips under the header. Each term is its own chip. When more than one chip is showing, an ALL chip is added.
3. Separate words with commas to require every term (AND). Each term matches product number, description, and every custom field, including custom fields that are hidden from the grid.
4. Click a term chip to remove that term. Click ALL to clear every term.
5. To replace the cookie with one term, open Products with `?Search=` set to that term.

**Options:** Terms are comma-separated and combined with AND. Each term is a contains match on product number, product name, and every custom field. Buy price, sell price, and quantity are not searched. Search uses ALL LOCATIONS for that request and hides the pager. `?Search=` replaces the cookie with that one term. Leaving Products and leaving Product Editor clears the search cookie and the keep-view cookie.

**Result:** Matching products are listed from the whole catalog for that request. The location selector is set to ALL LOCATIONS. No matches shows “No matches found!”.

**If it fails:** “No matches found!” when nothing matches. There is no error for a blank search.

**Do not write:** A search that stays inside the current location, or a match on price or quantity.

**Related:** PRD-001, PRD-002, PRD-005, SRCH-001, WF-013

**Code:** `UserPage.master.vb` `CS_SEARCHBOX1_AC_QuerySearchRequested` (lines 339–344) and the cookie clear when the path is outside Products and Product Editor (lines 88–95). `Products.aspx.vb` `SearchIfRequested` (lines 519–547), `SearchFiltersShow` (lines 566–608), `SQLSearchClauseGet` (lines 1952–1984).

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Search the product list

### PRD-007 — Open a product

**Open:** Products, on a row that is already listed. The same click on the read-only list opens the read-only editor.

**Steps:**
1. Click a data cell in the row (description, quantity, price, or another visible field).
2. The product editor opens for that product number (`ProductEditor.aspx?ProductNumber=`).
3. On the read-only list, the same click opens `ProductEditor_read_only.aspx` for that product number.
4. Leave the checkbox column alone when the goal is to select the row. That column does not open the editor.

**Options:** None. The destination is the editable editor or the read-only editor, based on the page.

**Result:** The editor opens on that product. A product number the editor cannot find is sent to `Product Error.html` (PED-008). A web-address pill in the grid follows PRD-008 and does not open the editor.

**If it fails:** None on the click. A missing product is handled by the editor.

**Do not write:** Clicking the row checkbox as the way to open the product.

**Related:** PRD-008, PED-001, PED-009, WF-013

**Code:** `Products.aspx.vb` row click starting at cell 1 (lines 1005–1013). `Products_read_only.aspx.vb` the same click to `ProductEditor_read_only.aspx` (line 961). Checkbox column is cell 0 and is outside that loop.

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Open a product from the list

### PRD-008 — Web addresses in the grid

**Open:** Products and the read-only product list. The same script runs on both pages. A cell qualifies only when its entire text is a web address.

**Steps:**
1. Find a cell whose whole text is an `http://` or `https://` address, a protocol-relative address (`//host`), a `www.` host, or a bare domain such as `example.com`.
2. Click the pill. It opens in a new tab.
3. Leave a cell that has extra words around an address. That cell stays plain text and still opens the product editor (PRD-007).

**Options:** The pill text is the host, without a leading `www.`, plus a non-default port when one is present. The link target is the normalized `https` address for `www.`, bare domains, and protocol-relative URLs.

**Result:** The address opens in a new tab. The product editor stays closed for that click.

**If it fails:** A value that is not a whole-cell address is left as text. There is no error message.

**Do not write:** A pill for a sentence that merely contains a URL.

**Related:** PRD-007

**Code:** `Scripts/Pages/Products/ProductsGridUrlCells.js` `normalizeUrl` (lines 11–64). Included from `Products.aspx` (line 13) and `Products_read_only.aspx` (line 11).

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Open a web address in the product list

### PRD-009 — Photos in the list

**Open:** Products, and the read-only list, when product images are on for this user (DSP-002). The toolbar camera control is not on the page.

**Steps:**
1. Turn on product images in Settings (DSP-002) if the product-number column shows numbers only.
2. Return to Products. Each product number cell shows a 40×40 image above the product number.
3. When a photo is missing, a demo product whose number contains `CS_DEMO_` uses `Images/Pages/Products/{sku}.png`. Any other product uses `Images/icons/cam_small.png`.

**Options:** DSP-002 is the switch. Image size is 40×40. There is no hide-images button on the products toolbar.

**Result:** The product number column shows the thumbnail and the number. Turning DSP-002 off removes the thumbnails on the next load.

**If it fails:** A missing file is replaced by the fallback image. There is no alert.

**Do not write:** A camera button on the products toolbar. That control is commented out.

**Related:** DSP-002, PED-002, PRD-003

**Code:** `Products.aspx.vb` `CONST__THUMBNAIL_IMG_WIDTH = 40` (line 36), `StylingRefresh` (lines 273–277), `GridviewImagesAdd` (lines 1144–1177). The camera button is inside a comment in `Products.aspx` (lines 677–684).

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** See photos in the product list

### PRD-010 — Change quantity in the list

**Open:** The editable Products page only, with a real location selected (not ALL LOCATIONS), on a quantity cell that is in stock. The cell is not editable during search or on the sub-location summary. Read-only lists do not offer this editor. This is separate from multi-edit (PRD-011).

**Steps:**
1. Select one location in the location control. ALL LOCATIONS leaves the quantity cell as a normal cell.
2. Click an in-stock quantity. A small editor opens with the current number, up and down arrows, and a blue OK mark.
3. Type a new whole number, or use the arrows. The down arrow stops at 0.
4. Press Enter or click OK. The page posts `api/inventory?action=adjust` with source and destination both set to that location, and the quantity set to the number typed.
5. Press Escape to close the editor and leave the quantity unchanged.

**Options:** Up adds 1. Down subtracts 1 and stops at 0. Arrow keys on the keyboard step the value only for a fine pointer (a desktop pointer that can hover). A narrow or touch layout still has the on-screen arrows. The request body is one transaction: product, source, destination, quantity. Timeout is 3 seconds.

**Result:** On success the list reloads and keeps the current page and sort. The quantity shown is whatever the inventory API stored. The same kind of change from the product map is MAP-026 and PED-006.

**If it fails:** Alert: “There was a problem updating the quantity in this location...” A non-numeric entry stays in the editor and is not submitted.

**Do not write:** This editor on ALL LOCATIONS, during search, on the sub-location summary, on the read-only list, or as the multi-edit quantity path. The stock math inside `api/inventory` is outside this page.

**Related:** PED-006, MAP-026, PRD-011, WF-013

**Code:** `Products.aspx` `submitQtyQuickAdjust` (lines 213–257), `QtyQuickAdjust` (lines 259–346), `productsPageAllowQtyArrowKeys` (lines 166–168). `Products.aspx.vb` attaches the click only when `LocationID_VIEW > -2` and the row is not a search or sub-location summary (lines 494–508).

**Confidence:** Confirmed for the request

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Change quantity from the product list

### PRD-011 — Add, delete, multi-edit, recent, export, print, printable

**Open:** The Products toolbar. Add, delete, and multi-edit are on the editable page. Recent, export, print barcodes, and the printable image are also on the read-only list. Delete, multi-edit, and print barcodes stay inactive until a checkbox is selected. Export is always available. Add is the image whose tooltip is “Add one or more products to your inventory”.

**Steps:**

Add
1. Click the add image. Add Products opens (`AddProducts.aspx?LastPage=Products`). Continue with PED-010.

Delete
1. Check one or more products. The delete image becomes clickable. Tooltip: “Delete selected products from your inventory.”
2. Click delete. Confirm “Are you sure you want to delete the selected products from your inventory? This action cannot be undone!”
3. The page calls `Product.DeleteProducts` for the checked rows, or for every product in the account when select-all is on (PRD-005). The list reloads.

Multi-edit
1. Check one or more products and click the edit image. Tooltip: “Multi-Edit: Change all of the selected items at once”.
2. In “For All Selected Items”, choose a field after SET, type a value after TO, and click Update. Cancel closes the panel.
3. The field list is Product Name, Buy Price, Sell Price, and each custom field. Quantity is included only when a real location is selected.

Recently created
1. Hover the recent-products image. The panel title is “Recently Created”.
2. Click a row. The product editor opens for that product number. The panel lists up to 50 creates.

Export
1. Click the download image. Tooltip: “Download Product Report”.
2. The product report opens (RPT-001) for the current location id. The current search is not passed.

Print barcodes
1. Check one or more products. The barcode image appears. Tooltip: “Print barcodes for selected products”.
2. Click it. The barcode page opens for those product numbers (PED-015).
3. If select-all is on, confirm “You are about to print barcodes for all {count} products. This may take a moment. Continue?” and the page opens `PrintBarcode?Batch=1`.

Printable
1. Click the printable image at the bottom of the list. Its tooltip is the misspelled “pritnable version”.
2. A new tab opens `/Products?printable=true`. The menu and the clickable controls are hidden. The browser print dialog is not opened.

**Options:** Multi-edit fields: Product Name; Quantity only at a real location; Buy Price (with currency); Sell Price (with currency); each custom field. Quantity overwrites the quantity at the current location. A custom field that lists “Other (Specify)” among its presets accepts any typed text. A preset list without that choice accepts only a listed value. Empty description on a recent row still opens the editor. Export always sends the location id and does not send the search cookie.

**Result:** Add opens the create page (WF-001). Delete registers activity `PRODUCT__DELETE` and calls `ProductExpirations.Delete`, then returns to the list. Multi-edit on a standard account (account type 0) writes the field and records `PRODUCT__EDIT` with quantity `"1"` per product, not the number typed, and the comment `Changed '{field}' to '{value}'`. Account type 1 calls `RecordsApp.AdjustRecord` and skips that SQL update. Recent rows are activity-code 0, newest first, up to 50. Export opens RPT-001. Barcodes open PED-015. Printable view hides the navbar and `.clickable` controls.

**If it fails:** Delete cancel leaves the list unchanged. Multi-edit: “Please enter a value”; “Value must be numeric!”; “Value is not allowed for this field.”; “Invalid field selected.” Recent, when there are no creates: “No recent new products...”. Print-barcode cancel on select-all stays on the list.

**Do not write:** The quantity-only dialog `Dialogs/ProductDeleteConfirmation.aspx` as the delete path. Nothing sets `Session("ProductsToDelete")`. Its buttons would remove quantity rows only (“DELETE FROM ALL LOCATIONS” or “DELETE FROM LOCATION [ALL …]”). The live delete is `Product.DeleteProducts`. The older `_DeleteProduct` does delete the product row, quantity rows, and image files, and the toolbar button does not call it. What `productDeleter` removes for images, attachments, and quantities is Uncertain: that class is not in this repo. A read-only user who opens `/Products?printable=true` is redirected to the read-only list and the printable flag is not kept. Do not write the export as including the current search.

**Related:** PED-008, PED-010, PED-015, RPT-001, PRD-005, WF-001, WF-013

**Code:** `Products.aspx` toolbar (lines 501–674), printable image (line 891), `DeleteConfirmation` (lines 137–143), `ForceExport` (lines 145–150), `ConfirmAndPrintBarcodesBatch` (lines 158–162). `Products.aspx.vb` `btn_delete_Click` (lines 2136–2142), `CheckedProductsMultiEdit` (lines 1235–1393), `RecentProductsPopulate` (lines 186–227), `btn_export_report_Click` (lines 2144–2148), `btn_print_barcodes_Click` (lines 2150–2168). `Product.vb` `DeleteProducts` (lines 58–84). `UserPage.master` `makePrintable` (lines 99–103).

**Confidence:** Confirmed, with the deleter cascade Uncertain

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Add, delete, edit, export, and print from the product list

## PED — Product editor, create, import, labels

### PED-001 — Edit name, price, and custom fields

**Open:** Product editor, from a product row (PRD-007) or from search. The product number is the label “PRODUCT NUMBER:” and cannot be renamed. Read-only users are sent to PED-009. An Admin also sees “Edit your fields”.

**Steps:**
1. Open the product. Fields follow the account’s field order: Product Name, then buy price, sell price, and custom fields where those are visible.
2. Click a text field, change it, and press Enter. The hint “Press Enter to Save...” appears while the field is active.
3. For a custom field that has presets, open the dropdown. Choose “(none)”, a preset, the current value when it is outside the list, or “Other (Specify)”.
4. “Other (Specify)” opens a box titled “Other (Specify):”. Type a value and click Save, or Cancel to keep the previous value.
5. An Admin can click “Edit your fields” to open the custom-field editor.

**Options:** Buy Price and Sell Price appear only for account type 0 and only when CFL-002 says to show them. Their labels include the account currency. “(none)” stores an empty value. “Other (Specify)” stores the text entered in the modal. Currency fields reject a non-numeric value and a negative value. The product number is display-only.

**Result:** Save writes that column and records activity `PRODUCT__EDIT` with the comment `Changed '{label}' to '{value}'`. The editor reloads. The product list is marked to reload when the user returns to it.

**If it fails:** “The Buy Price is not valid!” or “The Sell Price is not valid!” when the value is not numeric or is negative. A custom-field text error uses “The field {name} is not valid!” only when a numeric check on that field fails. “The Product Name is not valid!” is stored on the name field and is shown only if a numeric check runs; the name field does not run that check.

**Do not write:** Renaming the product number from this screen. Do not tell users they will see “The Product Name is not valid!” for a normal name edit.

**Related:** PRD-007, PED-009, CFL-002, WF-013

**Code:** `ProductEditor.aspx.vb` `LoadFieldControls` (lines 232–375), `GetVisibleProductFieldOrderTokens` (lines 377–396), `_dropDownChanged` (lines 559–623). `ProductEditor.aspx` “Other (Specify):” modal (lines 415–425) and “Edit your fields” (lines 795–798). `Controls/EDITABLE_FIELD.ascx.vb` `SaveField` (lines 375–438) and the numeric check (lines 338–356).

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Edit a product’s name, prices, and custom fields

### PED-002 — Product photo

**Open:** Product editor, the image under PRODUCT NUMBER. Tooltip: “Click to update image...”. Read-only users can see the image and cannot upload. A Lansweeper image removes the click and the tooltip (PED-004).

**Steps:**
1. Click the product image.
2. Choose a file. The editor uploads it and reloads.
3. If the image came from Lansweeper, the picture is not clickable. Use the Lansweeper link in PED-004.

**Options:** None. The upload handler does not check file size or file type before it saves.

**Result:** The new image is stored for this product number and shown on the editor. The product list is marked to reload. A missing image falls back to `Images/icons/cam_small.png`, or to `Images/Pages/Products/{sku}.png` when the product number contains `CS_DEMO_`.

**If it fails:** Choosing no file leaves the current image. There is no on-screen type or size error.

**Do not write:** A size limit or an allowed-type list for this upload. Those checks are not in the handler.

**Related:** PED-004, PED-009, PED-011, PRD-009

**Code:** `ProductEditor.aspx` image control (line 487). `ProductEditor.aspx.vb` `_upload_image` (lines 668–687), `_getImage` (lines 157–170), Lansweeper clearing the click (lines 54–60). Read-only image uses `onclick="return false"` in `ProductEditor_read_only.aspx` (line 72).

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Change a product photo

### PED-003 — Product attachments

**Open:** Product editor, the attachment image, tooltip “Click to attach file...”. Existing files appear as chips named `{filename}.{extension}`. Read-only users can download a chip and do not see upload or delete. This is not Document Editor (PED-017).

**Steps:**
1. Click the attachment image and choose a file. The editor reloads and shows a chip.
2. Click the chip to download the file.
3. Click the X on that chip. Confirm “Are you sure you want to delete this attachment?”

**Options:** None. The upload does not use an extension allow-list or a size check.

**Result:** The file is stored against this product and can be downloaded from the chip. Delete removes that attachment and reloads the editor. Other products are unchanged.

**If it fails:** Cancel on the confirm leaves the attachment. There is no message for a rejected type or an oversized file.

**Do not write:** This screen as Document Editor, a purchase order, a sales order, or a kit document.

**Related:** PED-009, PED-017

**Code:** `ProductEditor.aspx` attachment control (line 522) and `DeleteAttachmentConfirmation` (lines 118–119). `ProductEditor.aspx.vb` `_upload_attachment` (lines 690–730), `_showAttachments` (lines 70–113), `_deleteAttachment` (lines 139–156). Read-only `_showAttachments` adds the download chip and no delete button (`ProductEditor_read_only.aspx.vb` lines 106–137).

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Attach a file to a product

### PED-004 — Lansweeper link on a product

**Open:** Product editor, and the read-only editor. The Lansweeper image is hidden until an asset lookup returns a URL.

**Steps:**
1. Open a product that is linked to a Lansweeper asset.
2. Click the Lansweeper image. The asset URL opens in a new window.
3. When the asset-type custom field (tag `LS_CF_ASSET_TYPE_NAME`) has a Lansweeper image, that image replaces the product photo and the photo click is removed (PED-002).

**Options:** None. The link is shown only when the stored asset URL has text.

**Result:** The user is looking at the Lansweeper asset. The product row is unchanged. If the lookup fails, the link stays hidden.

**If it fails:** Failures are swallowed and the link stays hidden. There is no error sentence.

**Do not write:** A Lansweeper button on every product. It appears only after a successful asset lookup.

**Related:** PED-002, PED-009

**Code:** `ProductEditor.aspx.vb` `_linkToLansweeper` (lines 38–68), called from `Page_Init` (line 211). `ProductEditor_read_only.aspx.vb` `_linkToLansweeper` (line 74), called from `Page_Init` (line 57).

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Open a product in Lansweeper

### PED-005 — Expiration on the product

**Open:** Product editor, the EXPIRATION date, only when expirations are on for this user (`SHOW_EXPIRATIONS`). The same date is shown disabled on the read-only editor. The list of upcoming dates is EXP-001.

**Steps:**
1. Open the product. The date loads from the expiration API when the flag is on.
2. Pick a date. The field allows `2018-01-01` through `2050-01-01`.
3. Read the color: green when more than 60 days remain, gold when 60 or fewer days remain and the date is still in the future, red when the day difference is 0 or less.
4. Clear the date to remove it. Clearing sends DELETE to the expiration API.

**Options:** The window is 60 days. Colors use the day difference, including a +1 day adjustment in the script. Import of a date is PED-013: a non-`yyyy-MM-dd` value fails that row, and an existing product in a create-import does not receive the file’s expiration.

**Result:** A chosen date is posted to `api/expiration` for this product. A cleared date is deleted there. The catalog product fields are unchanged.

**If it fails:** API errors are written with `console.log` only. The page does not show an alert. Import, on a bad date: “Row {n}: Expiration must be a date such as 2026-12-31.”

**Do not write:** An on-screen error when the expiration API fails. Also do not write an expiration update for a product number that already existed in a create-import.

**Related:** EXP-001, PED-007, PED-013, WF-011

**Code:** `ProductEditor.aspx` expiration script and the date input `min="2018-01-01"` `max="2050-01-01"` (lines 664–782). `ProductEditor.aspx.vb` shows the block when `SHOW_EXPIRATIONS` (lines 368–374). `ImportFromFile.aspx.vb` date check (line 1870).

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Set a product expiration date

### PED-006 — Product editor map

**Open:** The right side of the product editor. The editable editor hosts map type 2. The read-only editor hosts map type 5. Quantity behavior on the map is MAP-026.

**Steps:**
1. Open the product. The instruction reads “Click a location. Type new quantity. Press Enter.”
2. Click a location, type the new quantity, and press Enter.
3. After a quantity change, the editor reloads so the map and the fields match.

**Options:** The first load of the editor writes map zoom cookie `0.9`. Read-only users get map type 5 and can still see the map. Clone (PED-007) does not copy location quantities onto the new product.

**Result:** The quantity change follows MAP-026. The editor reloads on that product. The initial zoom for a fresh editor open is 0.9.

**If it fails:** None in the editor host. Map errors belong to MAP-026.

**Do not write:** Clone as a way to copy stock on this map. The clone insert does not write location quantities.

**Related:** MAP-026, PED-007, PED-009, PRD-010, WF-013

**Code:** `ProductEditor.aspx` instruction (line 820) and map host `data--type-of-map="2"` (line 841). `ProductEditor.aspx.vb` zoom cookie (lines 187–189) and `MAP_CONTROL_1_RefreshRequired` (lines 630–635). `ProductEditor_read_only.aspx` map type 5 (lines 303–304).

**Confidence:** Confirmed for the host

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Change quantity on the product map

### PED-007 — Clone a product

**Open:** Product editor, the clone image, tooltip “clone this product”. The live clone is this modal. Read-only users do not get the button.

**Steps:**
1. Click the clone image. The dialog title is “Clone Product”.
2. Leave Auto checked to accept the next number. The number box shows the placeholder “[Automatic Product Number]” and stays disabled.
3. Or uncheck Auto and type a product number.
4. Adjust the copied fields. When expirations are on, an Expiration date is included.
5. Click Clone. Cancel closes the dialog.

**Options:** Auto is checked by default. Auto assigns `CSN-` plus nine digits. Unchecking Auto requires a typed number. Empty name is saved as the new product number. A price that does not parse is saved as 0. The date is copied only when expirations are on and a date was entered.

**Result:** The new product is inserted with `INSERT IGNORE`. Activity `PRODUCT__CREATE` is recorded. The image is copied when that copy succeeds. The expiration is posted when one was entered. The new editor opens with a “new” badge once. Quantities, locations, and attachments are not copied.

**If it fails:** “You must enter a product number.” “That product number already exists!” A number that already exists stops the save on the server as well.

**Do not write:** `Popups/CloneProduct.aspx` as the clone screen. That popup has locked fields and no save, and it is not linked. Live clone is this editor modal.

**Related:** PED-001, PED-005, PED-006, PED-018, WF-013

**Code:** `ProductEditor.aspx` clone modal (lines 427–455). `Scripts/Pages/ProductEditor/ProductEditorClone.js` placeholder (line 7). `ProductEditor.aspx.vb` `btn_clone_product_Click` (lines 466–535) and `InsertProductOnly` in `Product.vb` (lines 191–220). `GetNextAutoSKU` (lines 246–255) formats nine digits.

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Clone a product

### PED-008 — Delete one product

**Open:** Product editor, the trash button, tooltip “Delete this product”. Read-only users do not get the button. This uses the same `Product.DeleteProducts` path as the grid (PRD-011).

**Steps:**
1. Click the trash button.
2. Read the dialog “Delete this product?” and “Deleting this product will also check it out of all locations on the map.”
3. Click Delete, or Cancel.

**Options:** None.

**Result:** Delete calls `Product.DeleteProducts` for this product number, registers `PRODUCT__DELETE`, and calls `ProductExpirations.Delete`. The editor then redirects to that same product number. A missing product is sent to `Product Error.html`.

**If it fails:** Cancel closes the dialog and leaves the product.

**Do not write:** A guaranteed checkout of every quantity as something this repo completes. The modal says that. The class that performs the delete, `productDeleter`, is outside this repo, so image, attachment, and quantity removal inside that class is Uncertain. Do not send readers to `Dialogs/ProductDeleteConfirmation.aspx`.

**Related:** PRD-011, PED-018, WF-013

**Code:** `ProductEditor.aspx` delete modal (lines 402–412) and `btn_delete2` (line 801). `ProductEditor.aspx.vb` `btn_delete2_Click` (lines 732–737) and the missing-product redirect (lines 196–198). `Product.vb` `DeleteProducts` (lines 58–84).

**Confidence:** Confirmed for the click. Uncertain for the deleter cascade

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Delete one product

### PED-009 — Read-only product editor

**Open:** A read-only user opening a product, from the read-only list or from a direct editor link. A user who is not read-only and opens the read-only editor is sent to `/ProductEditor`.

**Steps:**
1. Open a product as a read-only user.
2. Read the fields. They are disabled.
3. Use Print Barcodes, an attachment chip, the Lansweeper image when it is present, and the map (type 5).
4. Leave clone, delete, image upload, and attachment upload. Those controls are not on this page.

**Options:** Print still opens the barcode page for this product. Attachment chips download. The expiration date is visible and disabled. Map type is 5.

**Result:** The user can read the product, print a label, download an attachment, open Lansweeper, and view the map. No catalog field is saved from this page.

**If it fails:** A missing product number redirects to `Product Error.html`.

**Do not write:** Clone, delete, photo upload, or attachment upload on this page.

**Related:** PRD-007, PED-001, PED-002, PED-003, PED-004, PED-006

**Code:** `ProductEditor.aspx.vb` read-only redirect (lines 177–179). `ProductEditor_read_only.aspx.vb` redirect of non-read-only users (lines 31–32), disabled fields (`isEnabled` false, lines 199–243), download-only attachments (lines 106–137). `ProductEditor_read_only.aspx` image `onclick="return false"` (line 72) and map type 5 (line 304).

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** View a product as a read-only user

### PED-010 — Create products by typing

**Open:** Add Products (`AddProducts.aspx`), from the product-list add button (`?LastPage=Products`), from “+ New Products” on the selector (PED-016), or from the header “Create New Product” path. The page title is “Create New Products”. A single mobile-transfer add (`MobileTransferSingleAdd=1`) uses the title “Add Product” and does not open check-in. Read-only users are not given this page from the product toolbar. Account type 1 disables prices.

**Steps:**
1. Leave AUTO checked, or uncheck it and type a product number. AUTO’s placeholder is “CSN-XXXXXXXXX [AUTO]”.
2. Type a DESCRIPTION. Add BUY PRICE and SELL PRICE when they are shown, then the visible custom fields. Prices show a `0.00` placeholder while focused.
3. Press Enter to add the row to the list on the right. The button hint is “Press Enter to create...”.
4. Repeat for more products. Click Save Products.
5. Check-in opens next (WF-001), unless this was the single mobile-transfer add.

**Options:** AUTO is checked by default and assigns `CSN-` plus nine digits. An empty description is saved as the product number. Empty prices stay 0. A non-numeric or negative price highlights the box and stops the add. A blank manual number shows the placeholder “No Poduct Number!” (spelled that way). Account type 1 grays out and disables both prices. Staged quantity for the following check-in is 1. `ListProducts` also inserts a `Quantities` row at location `-2` with no quantity column.

**Result:** Save calls `CreateNewAndStage`. New numbers are created. Existing numbers are skipped and are not updated. Unless this is the mobile single add, the next page is check-in (`CheckInCreatedProducts.aspx`), or the open transfer when the user came from one. The mobile single add posts the new product back to the parent and does not open check-in. Activity for the create is `PRODUCT__CREATE`.

**If it fails:** Placeholder “No Poduct Number!” on a blank manual number. “Product number already exists” or “Could not verify product number”. A non-numeric or negative price keeps the row off the list. If every typed number already exists, Save Products does not open check-in.

**Do not write:** An update of an existing product’s name, price, or custom fields from this page. Those numbers are skipped.

**Related:** PRD-011, PED-011, PED-013, WF-001, WF-013

**Code:** `AddProducts.aspx` title (line 1505), Save Products (line 1748), mobile title script (line 586). `AddProducts.aspx.vb` `LoadDynamicInputs` (lines 46–113), AUTO checkbox (lines 222–229), `btn_save_Click` (lines 297–437). `Product.vb` `CreateProducts` / `ListProducts` (lines 139–234) and `GetNextAutoSKU` (lines 246–255).

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Create products by typing

### PED-011 — Photo while creating

**Open:** Add Products, on the thumbnail for the product being typed. A new add session clears temporary images.

**Steps:**
1. On Add Products, click the thumbnail and choose a file.
2. The thumbnail updates. Its title becomes “Change image”.
3. Add the product row and click Save Products. The temporary image is copied onto the new product numbers.

**Options:** None. The upload does not check file type or file size.

**Result:** The photo is stored as a temp image first and is copied onto each new product number when save succeeds. Products that were skipped because the number already exists do not get this photo from this step.

**If it fails:** Choosing no file leaves the placeholder. There is no type or size message.

**Do not write:** A size limit or an allowed-type list for this upload.

**Related:** PED-010, PED-002, WF-001

**Code:** `AddProducts.aspx.vb` `btn_upload_Click` (lines 531–560) and `SaveCachedImages` (lines 505–516), called from `btn_save_Click` (line 403).

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Add a photo while creating products

### PED-012 — Import a CSV (shared rules)

**Open:** Import from file, from Add Products (“import file”) or from the product selector (PED-016). Read-only users are sent to unauthorized. These rules apply before create-import (PED-013) and before a movement import (PED-014).

**Steps:**
1. Choose a CSV and upload it.
2. When the file is accepted, the instruction changes to “Drag from left to right to Match the fields.”
3. Drag each file column onto a field on the right. Click a field to clear that match.
4. Continue with PED-013 or PED-014, depending on which import was opened.

**Options:** The file must be under 250 KB, UTF-8, comma-separated, with at most 100 columns. The first non-blank row is the header and is never a product. Quoted commas are supported. At least a Product Number must be matched before a create upload can continue. The sample link on a create import is `Samples/Products.csv`.

**Result:** A valid file is held for column matching. Nothing is written to the catalog until the matching step is confirmed.

**If it fails:** “This file is empty.” “This file is too large. Use a CSV smaller than 250 KB.” “This file is not a CSV. Save it as a comma-separated CSV and try again.” “This file is not valid UTF-8. Save it as CSV UTF-8 and try again.” “This file uses semicolons between columns. Save it as a comma-separated CSV and try again.” “This file has more than 100 columns. Remove the extra columns and try again.” “Row {n} could not be read. Check the quotes and try again.” “This file has no products.” “You must select at least a Product Number to upload.” “This file could not be read. Save it as CSV UTF-8 and try again.” “The column matching could not be read. Match the fields again.”

**Do not write:** A semicolon file, a file at or over 250 KB, or a first row that is treated as a product.

**Related:** PED-013, PED-014, WF-007, WF-008

**Code:** `ImportFromFile.aspx.vb` `Page_Init` read-only redirect (lines 29–31), `UploadFile` size and type checks (lines 162–205). `CSV_Class.vb` `ParseUpload` messages (lines 40–100). `ImportFromFile.aspx` the product-number message (line 1083).

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Upload a product CSV

### PED-013 — Import to create products

**Open:** Import from file in create mode, from Add Products. Sample file header: `Product Number, Product Name, Buy Price, Sell Price, Manufacturer, Supplier`. Those names are examples. The importer uses the columns the user drops, not those header names.

**Steps:**
1. Upload a CSV that passes PED-012.
2. Drag columns onto Product Number, Description, Buy Price and Sell Price when those are shown, each custom field, Quantity, Expiration when the flag is on, and Location # or Location Name unless the user is returning to a transfer.
3. Quantity’s tip is “You can include a quantity column to use during Check In”. Location’s tip is “You can include a location column to check these products into those locations.” Expiration’s tip is “A date like 2026-12-31 (year-month-day).”
4. Click Next. If some numbers already exist, review the notice and click Continue.
5. Check-in opens (WF-001), or the open transfer when the user came from one.

**Options:** Unmapped product number becomes `CSN-` plus nine digits. Unmapped description becomes the product number. Unmapped prices stay 0. Unmapped quantity stays 1. Unmapped location stays `-2`. Length limit is 255 for product number, description, and each custom field. Manufacturer and Supplier import only when those file columns are dropped onto custom fields. Presets are not enforced. Buy and sell slots appear for account type 0 when CFL-002 shows them.

**Result:** New product numbers are created. Existing products keep their description, price, and custom fields. Their quantity is staged for check-in. Expirations are saved only for new numbers. The notice says “Existing products keep their description, price, and custom fields. Their quantity is staged for check-in. New products are created from this file.” The summary line is “1 product already exists” or “{count} products already exist”.

**If it fails:** “Row {n}: Buy Price must be a number such as 12.50.” The sell-price sentence uses the same pattern. “Row {n}: Quantity must be a whole number such as 1 or 1.00.” “Row {n}: Expiration must be a date such as 2026-12-31.” “Product number "{n}" is used on {count} rows.” “Row {n}: Product number is longer than 255 characters.” The description and custom-field length sentences use the same 255-character pattern. “Row {n} has {found} columns and the header has {expected}.” “The file or column matching changed. Review the import and try again.”

**Do not write:** A create-import that updates the description, prices, or custom fields of a product number that already exists. Do not write an expiration onto those existing numbers.

**Related:** PED-012, PED-005, PED-010, WF-001, WF-007

**Code:** `ImportFromFile.aspx.vb` `PopulateFieldsList` create slots (lines 230–259), `BuildCreateImport` (lines 1710–1870), duplicate summary (line 1962), `ShowExistingProductsNotice` (lines 1987–2008), `SaveCreateImport` redirect to `CheckInCreatedProducts.aspx` (lines 1696–1706). Sample header in `Samples/Products.csv`.

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Import a CSV to create products

### PED-014 — Import a list into check-in, check-out, or transfer

**Open:** Import from file with create turned off, from the product selector’s “Import From File” or “OR Import from File with Locations”, before the movement’s destination selection is finished (XFR-005). This mode does not insert products.

**Steps:**
1. From check-in, check-out, or transfer, open Import From File.
2. Upload a CSV that passes PED-012. Samples: `Product Number, Quantity` for check-in or check-out; `Product Number, Quantity, Location` when a location column is required; `Product Number, Quantity, FROM, TO` for a transfer.
3. Match the identifier. On a transfer, open “Choose the field that identifies each product” and pick Product Number, Description, or a custom field. Match Quantity. Match Location #, or FROM (Location #) and TO (Location #), when those slots are showing. Location name can be chosen with “Choose how locations are identified”.
4. Click Next. A transfer that was started from an open transfer returns with `ApplyImportedTransfer=1` (XFR-005). Other movement imports store the start-page cookies and return to the selector or the transfer.

**Options:** Identifier: Product Number, Description, or a custom field, on a transfer match. Quantity is required. A non-transfer row whose column count does not match the header fails the file: “Row {n} has {found} columns and the header has {expected}.” A transfer row with a different column count is skipped: “Row {n}: this row has {found} columns and the header has {expected}, so it was skipped.” A repeated identifier on a transfer keeps the later quantity: “Row {n}: {field} "{value}" was already on {earlier}. The quantity from row {n} was used.”

**Result:** No product rows are inserted. The page writes the start-page cookies for the host movement. A transfer return redirects to Transfer (or `MOBILE_Transfer.aspx` on a mobile browser) with `ApplyImportedTransfer=1`. Stock is changed later by that host page (WF-002, WF-003, WF-004, or the Start page in WF-008).

**If it fails:** “The selected field must be numeric!” when a non-transfer quantity column is not numeric. Transfer skips: “Row {n}: {field} is blank.” “Row {n}: Quantity must be a whole number such as 1 or 1.00.” “Row {n}: Quantity must be a whole number greater than 0.” Location names that do not match show the location error label from the lookup.

**Do not write:** This import as creating products. Do not write the stock change here. Check-in, check-out, and transfer do that math on their own pages, and those paths are not the same (WF-008).

**Related:** PED-012, PED-016, XFR-005, WF-008

**Code:** `ImportFromFile.aspx.vb` `IsTransferMatchImport`, `PopulateFieldsList` movement slots (lines 275–284), ragged handling (lines 483–490 and 553–556), `AppendTransferImportRow` (lines 829–884), `CreateStartPageCookies` (line 621), transfer redirect with `ApplyImportedTransfer=1` (line 598). Samples: `Samples/ProductList.csv`, `ProductListLocation.csv`, `ProductListLocationTransfer.csv`.

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Import a list into check-in, check-out, or transfer

### PED-015 — Print barcode labels

**Open:** Print Barcode Labels, from the product editor’s Print Barcodes image, from the product-list barcode image (PRD-011), or from `PrintBarcode?Batch=1` after select-all. The page title in the header is “Print Barcode Labels”.

**Steps:**
1. Open the page for one product or for the selected list.
2. Choose a label stock. The first choice is already selected: `30252 (1-1/8" × 3-1/2")`.
3. Click PREVIEW & PRINT. The page builds a Code 128 barcode for each product.
4. Use the browser print dialog on the preview. The page recommends a DYMO LabelWriter 450.

**Options:** Stock, default first: `30252 (1-1/8" × 3-1/2")`, `30336 (1" × 2-1/8")`, `30334 (2-1/4" × 1-1/4")`, `30330 (3/4" × 2")`. An unknown stock falls back to 30252. `?Batch=1` reads the product list from the select-all cookie and does not replace it from the query string. A comma in `SKU` clears the shared name, and each name is then looked up. A missing name is printed as “UNTITLED”.

**Result:** The preview shows one label per product number, with a Code 128 symbol and the product name or “UNTITLED”. Printing is the browser’s print of that preview.

**If it fails:** An empty product list returns without drawing labels. There is no extra alert.

**Do not write:** A stock size that is not one of the four choices as a custom layout. Unknown values use 30252.

**Related:** PRD-011, PED-001, PED-009

**Code:** `PrintBarcode.aspx` title and stock list (lines 189–210). `PrintBarcode.aspx.vb` `Page_Init` batch and comma-in-SKU behavior (lines 14–33), `ResolveProductName` (lines 177–190). `BarcodePngGenerator.vb` `GetLabelSpec` (lines 42–57) and Code 128 (lines 59–68).

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Print barcode labels

### PED-016 — Product selector

**Open:** The selector used by Start for check-in, check-out, and transfer (`ProductSelector.aspx?Type=`). Read-only users are sent to unauthorized. The scan-and-filter script, and the inventory write after `SignalNext`, were not fully traced; that write is XFR-006.

**Steps:**
1. Open Check In. The title is “Check In”, the subtitle is “Add Products to a Location”, and the instruction is “Please select a Check In Location.” The location starts at the user’s default check-in location (DEF-001).
2. Or open Check Out. The title is “Check Out”, the subtitle is “Remove Products from a Location”, and the instruction asks for a Check Out location, starting at the default check-out location.
3. Or open Transfer. The title is “Transfer” and the subtitle is “Move Products between Location”. First: “Please select a Source Location for the Transfer.” Then: “Please select a Destination Location for the Transfer.”
4. After the location is set, use “Search or scan...”, “+ New Products”, “Import From File”, or “OR Import from File with Locations”.

**Options:** Check-in default is `CheckInLocationDefault`. Check-out and the transfer source start at the check-out default. “+ New Products” opens `/Start?add=true` (PED-010). “Import From File” opens import with create off (PED-014). “OR Import from File with Locations” adds `LOCATION_REQUIRED=TRUE`. The same source and destination on a transfer is refused.

**Result:** The chosen location is stored for the movement. New Products and Import leave this page for those flows. The inventory write that follows `SignalNext` is the movement page, XFR-006, and is not specified here.

**If it fails:** “The Source can't be the Destination!” and the page asks for a destination again.

**Do not write:** The scan matcher or the stock write on this page as confirmed behavior. Those steps are Uncertain here and belong to XFR-006.

**Related:** PED-010, PED-014, DEF-001, XFR-006, WF-002, WF-003, WF-004, WF-008

**Code:** `ProductSelector.aspx.vb` `Page_Init` titles (lines 31–56) and the same-location message (line 160). `ProductSelector.aspx` “Search or scan...” (line 115), “+ New Products” (line 149), “Import From File” (line 152), “OR Import from File with Locations” (line 99). `BounceUnauthorizedUsers` (lines 105–110).

**Confidence:** Confirmed for titles and location rules. Uncertain for the scan script and the write after `SignalNext`

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Pick products for check-in, check-out, or transfer

### PED-017 — Document editor is not product attachments

**Open:** `DocumentEditor.aspx?ID=` only by a direct address. No product page links here. Type 0, 1, and 2 change a heading color and which placeholder panels are visible. Type 3, BOM, is defined on the document class and has no page case.

**Options:** Type 0 heading “Purchase Order”. Type 1 heading “Sales Order”. Type 2 heading “Kit”. Header text is the literal `[PRINT] [SAVE] [NEXT]`. Footer text is the literal `[Cancel] [Save]`. Placeholder panels read `[VENDOR]`, `[CUSTOMER]`, and `[PROCESS]`.

**Result:** The page shows a heading and those literal labels. The header and footer words have no click handlers, so they do not print, save, or move to a next document.

**If it fails:** None. The controls do not run.

**Do not write:** This page as editing a document, a purchase order, a sales order, or a kit. Product attachments are PED-003. Do not write steps that click `[PRINT]`, `[SAVE]`, `[NEXT]`, `[Cancel]`, or `[Save]`.

**Related:** PED-003

**Code:** `DocumentEditor.aspx` header literals (lines 55–57) and footer (line 83). `DocumentEditor.aspx.vb` `PopulateDocument` (lines 25–58). `CS_Document_Class.vb` BOM value with no matching page case.

**Confidence:** Confirmed

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Document editor is not a product screen

### PED-018 — Unwired product screens

**Open:** These addresses are not linked from the live product list, the live editor, or the live delete and clone buttons. Opening one directly is not the supported path.

**Options:** None of these screens are offered from the live product toolbar or the live editor.

**Result:** The live clone remains the editor modal (PED-007). The live delete remains `Product.DeleteProducts` (PRD-011 and PED-008). The live success page after creating products is the check-in page (WF-001). Products clears the `STOCKROOM_BATCH` cookie when the list loads.

**If it fails:** None. These screens are not in the live path, so there is no user-facing failure to document.

**Do not write:**
- `Popups/CloneProduct.aspx`: fields are locked and there is no save. It is not the live clone (PED-007).
- `Dialogs/ProductDeleteConfirmation.aspx`: it would delete quantity rows only, with “DELETE FROM ALL LOCATIONS” or “DELETE FROM LOCATION [ALL …]”. Nothing sets `Session("ProductsToDelete")`. It is not the live delete (PRD-011).
- `SuccessProducts.aspx`: it shows “Success!” and “You can now Check In these products to any location.” No caller in this repo opens it. Live success is the check-in page.
- `Batch_Class.vb`: no in-scope page calls it. Products clears cookie `STOCKROOM_BATCH` on load.

**Related:** PED-007, PED-008, PRD-011, WF-001

**Code:** `Popups/CloneProduct.aspx` (no save control). `Dialogs/ProductDeleteConfirmation.aspx.vb` `Page_Init` / `LoadProductsToDelete` (lines 14–31) and `ShowButtons` (lines 85–148). `SuccessProducts.aspx` (lines 33–38). `Products.aspx.vb` `CookiesInitialize` clears `STOCKROOM_BATCH` (lines 280–286). `Batch_Class.vb` has no in-scope page caller.

**Confidence:** Confirmed they are unwired

**KB Status:** Not audited. **KB Article URL:**

**Suggested title:** Product screens that are not live

# ACT, EXP, KIT, SRCH, RPT

Walkthroughs for the knowledge base. Page behavior below was read in `cs-website`. Stock math for `api/expirationReplacement`, persistence and match rules for `api/kit`, and match fields for `api/search` are outside this repo and stay Uncertain.

There is no undo on activity history or activity details.

---

## ACT — Activity

Account and user activity codes 10, 11, 12, and 15–24 are declared on `ActivityCodeIndex` and are not included in the history query. Records accounts (account type 1) use Assignments, Assign, Deallocate, and Records for the group labels. The stored description phrases are in ACT-007.

### ACT-001 — Activity history

- **Open:** Any signed-in user, including read-only. The header activity icon, the collapsed menu link **Activity**, and the popup button **View Activity History** open `/ActivityHistory`. There is no `SHOW_*` flag.
- **Steps:**
  1. Open Activity History.
  2. The first load uses **All Activity**, user **All**, location **All Locations**, the last **90** days through today, an empty keyword box, and **15** rows. A comment in `Page_LoadComplete` says the default calendar is the last year (365 days). The constant `DEFAULT_DAYS_TIMESPAN` is 90, and the date picker uses `moment().subtract(90, 'days')`.
  3. Read each row: avatar, comment, “{You|name} {description}”, time, product count, and location icons. The current user’s stored first name is shown as **You** and highlighted `#558DC6`.
  4. Click the row background to open Activity Details (ACT-005). Click a product name or a location name in the row to open that editor. Those clicks do not open details.
  5. Click **Show More...** to add 15 to the window. The page reloads a longer list from the newest row. It does not page forward.
- **Options:** Category starts at All Activity (12). User filter starts at All (`-1`). Location starts at All Locations (`-2`). Keyword starts empty, placeholder “search by keyword...”. Listing cap is 15. See ACT-002 and ACT-003 for each control.
- **Result:** Newest first. Empty list shows **No Activity...** and **details will appear here**, and hides **Show More...**. When at least one row is drawn, **Show More...** stays on the page even if every matching row is already visible. Changing user, date, location, or category does not reset the 15-row window. With a user filter on, timestamps are the stored `DateAndTime` and are not shifted by the account time zone. With no user filter, timestamps are shifted by `AccountSettings.TimeZone` hours. A product activity with no content lines is skipped. There is no undo.
- **If it fails:** A missing profile image falls back to `Images/Icons/avatar.png`. If the first-name lookup for a user filter throws, the list loads with no user filter.
- **Do not write:** Do not say the default range is 365 days. Do not describe an undo. Do not say account or user activity codes 10–12 or 15–24 appear in this list.
- **Related:** ACT-002, ACT-003, ACT-004, ACT-005, ACT-006, ACT-007. WF-011 ends on this page after a successful expiration replacement.
- **Code:** `ActivityHistory.aspx.vb` `Page_Init` 19–29, `Page_LoadComplete` 31–52, `GetFilters` 132–206, `DisplayHistory_FAST` 378–1115, `btn_load_more_Click` 1117–1122. `Activity.vb` `GetActivitiesList_COMPLETE` 656–793. `ActivityHistory.aspx` empty state 765–768, **Show More...** 772. `UserPage.master` menu **Activity** 1292, icon 1390, **View Activity History** 1396.
- **Confidence:** Confirmed
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** View activity history

### ACT-002 — Filter by type

- **Open:** Left rail on Activity History. Same people as ACT-001.
- **Steps:**
  1. Click a group or a child button. The page posts back and reloads the list.
  2. The active button turns green (`#00B050`).
  3. Use **Check In** or **Check Out** only after you also pick a location when you need transfers. With **All Locations**, transfers are removed from both of those buttons.
- **Options:** Button, category integer, and SQL `ActivityCode` list:

  | Button | Category | SQL codes |
  | --- | --- | --- |
  | All Activity | 12 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 25 |
  | Inventory | 0 | 1, 3, 4, 25 |
  | Check In | 1 | 1, 4, 25, then an in-memory filter |
  | Check Out | 2 | 3, 4, 25, then an in-memory filter |
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

  Default is **All Activity**. On a records account (type 1), `SetButtonText` renames Inventory to **Assignments**, Check In to **Assign**, Check Out to **Deallocate**, and Products to **Records**. Transfer stays **Transfer**. Create, Edit, Delete, and Adjust are not renamed.

  **Check In** and **Check Out** are not pure type filters.
  - A native check-in (code 1) stays on Check In. A native check-out (code 3) stays on Check Out.
  - An adjust (code 25) stays on Check In when the comment quantity did not go down (old is not greater than new, the quantities are equal, or the comment does not parse). It stays on Check Out only when old quantity is greater than new. The comment must match `Quantity for '…' was adjusted from {old} to {new}.` If it does not parse and the first content quantity is greater than 0, old is treated as 0 and new as that quantity, so the adjust is treated as a check-in.
  - A transfer (code 4) is removed from both Check In and Check Out when no location is selected. When a location is selected, Check In keeps the transfer only if a destination is inside that location plus its descendants and the source is not. Check Out keeps it only if the source is in that tree and the destination is not. A move that stays inside the filtered tree is excluded.
  - Under Check In or Check Out, those transfer rows are drawn with check-in or check-out icons, and the comment is shown with a `{{cs-transfer}}` badge if that tag is not already there. Adjust rows that map onto check-in or check-out get a `{{cs-quantity-adjust}}` badge. The quantity shown is the absolute change, not the stored content quantity. The badges are display-only. The stored comment is unchanged. Activity Details does not add these badges.
- **Result:** The list is the SQL type list, then the Check In / Check Out rules above. The active button is green.
- **If it fails:** None on screen. A category value outside the table leaves the SQL list at the function default `(1,3,4,25)`. The page only posts the categories in the table.
- **Do not write:** Do not describe Check In as “only check-ins” or Check Out as “only check-outs.” Do not say the transfer or quantity-adjust badge is saved on the activity.
- **Related:** ACT-001, ACT-003, ACT-004, ACT-007
- **Code:** `ActivityHistory.aspx` 670–702. `ActivityHistory.aspx.vb` `ApplyCategoryCSS` 54–130, `SetButtonText` 1173–1185, `UpdateCategoryDisplay` 1145–1167. `Activity.vb` `GetActivitiesList_COMPLETE` 698–743, `InventoryActivityMatchesCategoryFilter` 1293–1345, `GetInventoryIconDisplayType` 1115–1143, `GetCommentForInventoryDisplay` 1146–1156, `GetAdjustEquivalentInventoryType` 1193–1207.
- **Confidence:** Confirmed
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Filter activity by type

### ACT-003 — Date, user, location, and keyword

- **Open:** Top of Activity History. Same people as ACT-001. The date control is the calendar at the top right. User chips are at the top left. The location selector sits with them. The keyword box placeholder is “search by keyword...”.
- **Steps:**
  1. Open the date control and pick a preset or two dates. Apply posts the range back. The label is `MMMM D, YYYY - MMMM D, YYYY`.
  2. Click **All**, **Me**, or another person. The selected chip is full opacity with a green border.
  3. Pick a location, or leave **All Locations**.
  4. Type a keyword and press Enter, or click the search image. The search image has no server click handler of its own. The postback still reloads the list from the text box.
- **Options:**
  - **Date presets:** All Time (1 Jan 2011 through tomorrow), Today, Yesterday, Last 7 Days (today minus 6 days through today), Last 30 Days (today minus 29 days through today), This Month (start of month through end of month). The picker `maxDate` is today, so All Time’s tomorrow and a future day in This Month can be clamped by the picker. The server includes the end day by adding 24 hours. If the saved dates are missing, the range is the last 90 days through today. A parse failure falls back to the last 90 days through now.
  - **Users:** **All** is index `-1` (no user predicate). **Me** is the signed-in user. Other chips come from people who have logged in (`CHAR_LENGTH(FirstLoginDate) > 1`) and whose type is not `READ-ONLY`. The query matches the stored first name (`UserID=@P1`), not the user index. Two people with the same first name cannot be separated. A renamed person no longer matches old rows, because the name was stored at registration. Read-only people are omitted from the chips. Their old rows can still appear if that name was stored.
  - **Location:** `-2` is All Locations. Any other id includes that location and descendants (`LocationID` or `LocationPath` like `%/{id}` or `%/{id}/%`). Location create, edit, and delete match the source id or a content product number that parses as a location id. `LocationDestinationID` is not used for those three types, because create stores a location type there.
  - **Keyword:** Empty skips the predicate. A term matches comment, product number, product name, and every custom field (`CF_{fieldIndex}`). There is no AND/OR syntax. `%` and `_` stay SQL LIKE wildcards. The term is a bound parameter.
- **Result:** The list uses the four filters together with the type filter from ACT-002. The CSV pre-header repeats the date range, the selected user’s first name, and `Comment : {term}` when the keyword is not blank. The keyword does not reset the Show More window.
- **If it fails:** None on screen for a keyword that matches nothing (the empty state in ACT-001). If the user-name lookup throws, the page loads with no user filter.
- **Do not write:** Do not say the default range is 365 days. Do not say the user chip matches a user id. Do not document search operators.
- **Related:** ACT-001, ACT-002, ACT-004
- **Code:** `ActivityHistory.aspx` date picker 510–580, keyword box 611. `ActivityHistory.aspx.vb` `GetFilters` 167–201, `PopulateUserFilters` 243–298, `hidden_btn_date_filter_Click` 1137–1143, `hidden_btn_user_filter_Click` 1131–1135, `LocationSelector_control_LocationChanged` 1124–1128. `Activity.vb` `CommentSearchExpression` 683–696, `TimeRangeExpression` 681, user predicate 760–766, `BuildActivityCompleteLocationScopeWhereClause` 468–473, `FilterLocationAdminActivitiesByLocationScope` 1362–1380. `User_Legacy.vb` `GetUserTable` 136–155.
- **Confidence:** Confirmed
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Filter activity by date, user, location, and keyword

### ACT-004 — Activity row hover and CSV

- **Open:** On Activity History, the product count on a row, and the download image to the left of the date range. Tooltip on the image: “Download spreadsheet file (.csv)”. Same people as ACT-001.
- **Steps:**
  1. Hover the product count. The panel lists product name, number, and quantity.
  2. Click a product name in the hover to open Product Editor. Click a location in the hover to open Location Editor. Those clicks do not open Activity Details.
  3. Leave **Readable Format** checked, or clear it. Click the download image. The file uses the current filters and ignores the 15-row cap.
- **Options:**
  - Count text is `{n} Product` or `{n} Products`. When the row has quantities, it adds `({qty} Item)` or `({qty} Items)`. Create and edit omit the quantity.
  - Check-in can say “to {location}”. Check-out can say “from {location}”. Transfer says “from {a} to {b}”. Adjust says “at {location}”.
  - The hover adds a line only while the index is `<= 10`, so at most 11 product lines are listed. Further products are still counted.
  - **Readable Format** is checked by default. Tooltip: “If you need to manipulate your data more easily you can uncheck this box for a more uniform file.” Checked writes one summary line per activity, then product lines whose first columns are blank. Unchecked repeats date, user, activity, source, destination, and comment on every product line.
  - Columns, exactly: `Date, User, Activity, Source, Destination, Comments, Product Number, Description, Quantity, FROM, TO, Buy Price, Sell Price, Old Quantity, New Quantity, Qty. Diff., Cost Diff.`
  - The filename is `CyberStockroom - {category label} Report`, plus ` at {location name}` when a location is selected and the name is not `[DELETED]`, sanitized and cut at 200 characters, then `.csv`.
- **Result:** The browser downloads a CSV of the filtered activities, including rows past the 15 on screen. `WriteActivityCsv` never fills Old Quantity, New Quantity, Qty. Diff., or Cost Diff. Commas in user, description, comment, product number, and product name become `_`. Location paths in FROM and TO are not passed through that replacement. Buy and sell prices are the raw product values. If product details throw, the chip reads `{n} Product(s) [DELETED]` and the hover lists the product numbers. An empty product name in the CSV is written as `[DELETED]`.
- **If it fails:** None on screen for a download error path that the page shows. The temp file is written, streamed, and deleted.
- **Do not write:** Do not say the last four CSV headers contain old quantity, new quantity, quantity difference, or cost difference. Do not say the download is limited to the 15 rows on screen.
- **Related:** ACT-001, ACT-002, ACT-003, ACT-005
- **Code:** `ActivityHistory.aspx` **Readable Format** and download 497–498. `ActivityHistory.aspx.vb` hover block 523–760, `DownloadReport` 1255–1329, `GetDownloadReportCategoryLabel` 1187–1225, `WriteDownloadReportPreHeader` 1243–1253. `Activity.vb` `ActivityCsvColumnHeader` 878, `WriteActivityCsv` 968–1068, `CsvSanitize` 964–966.
- **Confidence:** Confirmed
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Read an activity row and download the activity CSV

### ACT-005 — One activity

- **Open:** Click a history row. The page is `ActivityDetails.aspx?ActivityID=` in a Fancybox iframe (`UserPageNoMenu.master`). It is not in the main menu. Same login as Activity History.
- **Steps:**
  1. Click the row (not a product or location name inside it).
  2. Read the user (**You** when the stored first name matches), the description, the time, the comment, the locations, and the product table.
  3. Click a product name to open Product Editor in the parent window. Click a location row to open Location Editor the same way.
  4. Click the download image to request the same URL with `download=1`.
- **Options:** Product table columns are Product, Number, and Qty, except create (0) and edit (5), which omit Qty. Qty is the larger of quantity in and quantity out. Extra columns appear only when both header location ids are `-2`: check-in **To**, check-out **From**, adjust **Location**, transfer **From** and **To**. The details CSV always uses grouped rows and category 12 (All Activity).
- **Result:** The full product list, with no 11-line hover cap. There is no comment edit and no undo. `WriteComment` exists on `Activity` and is not called here. A successful download is one activity CSV. The filename is `CyberStockroom - {description} - {MMM d yyyy}`, sanitized, max 200 characters, plus `.csv`.
- **If it fails:** Missing or unknown id shows **Activity not found** and **This activity may have been removed or is not available on this account.** Download of a missing id returns HTTP 404 and ends the response. A blank product name displays `[DELETED]`.
- **Do not write:** Do not describe an undo or a way to edit the comment on this page. Do not say the check-in and check-out badges from ACT-002 are added here.
- **Related:** ACT-001, ACT-004, ACT-007
- **Code:** `ActivityDetails.aspx` 253–254. `ActivityDetails.aspx.vb` `Page_Init` 17–42, `StreamCsv` 49–72, `RenderDetails` 74–114, `RenderProducts` 251–299. `Activity.vb` `GetActivityCompleteById` 880–927.
- **Confidence:** Confirmed
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** View one activity and download it

### ACT-006 — Header activity popup

- **Open:** The activity icon in the header on every `UserPage.master` page, including Activity History, Expirations, Kitting, and the AI report. Any signed-in user.
- **Steps:**
  1. Open the activity icon.
  2. Read up to 5 rows. Click **View Activity History**, or the icon itself, to open Activity History.
- **Options:** The first query is inventory category 0 (codes 1, 3, 4, 25), from two years ago through now, limit 10, displayable types only. If that returns nothing, a backup query uses category 2 (codes 3, 4, 25), which is the check-out SQL list, and that backup does not run the Check In / Check Out direction filter. The popup then keeps at most 5 rows and skips any type that is not check-in, check-out, transfer, or adjust.
- **Result:** Each row shows an avatar, a description, a comment, and a time. The current user’s comment is suffixed ` - You`. Another user’s comment is suffixed with the numeric user index, not the name. The rows do not open Activity Details.
- **If it fails:** None on screen. A missing profile image falls back to `Images/Icons/avatar.png`.
- **Do not write:** Do not say a popup row opens the activity. Do not say the other-user suffix is the person’s name. Do not say the backup list applies the Check In / Check Out direction rules.
- **Related:** ACT-001, ACT-002, ACT-007
- **Code:** `UserPage.master.vb` `CreateNotificationSummary` 156–198, `AppendNotificationActivityRow` 200–275. `UserPage.master` 1390–1396.
- **Confidence:** Confirmed
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** See recent activity in the header

### ACT-007 — What is stored

- **Open:** There is no control on Activity History that writes these rows. A signed-in user creates them by checking in, checking out, transferring, adjusting a quantity, or creating, renaming, or deleting a location. The expiration replacement page sends a comment and then opens Activity History. What that API writes is Uncertain (EXP-002).
- **Steps:**
  1. Finish one of those actions on its own page.
  2. Open Activity History (ACT-001). The new row uses the phrase for the account type.
- **Options:** Standard account (type 0) phrases from `GetActivityDescription`: created new products, deleted products, edited products, checked in products, checked out products, transferred products, adjusted a product quantity, created a new location, deleted a location, renamed a location. Records account (type 1): created new records, deleted records, edited records, assigned records, deallocated records, transferred records, adjusted a record. Location phrases stay the same. Any other type returns `activity [{code}]`. An unknown account type returns `[ERROR-ACC1 - unkown account type]`. A content row is stored only when the product number length is greater than 0 and the quantity is greater than 0. Header location ids default to `-2`.
- **Result:** A new activity id. The history page can show it when the type is one of 0, 1, 2, 3, 4, 5, 6, 7, 8, or 25 and the row has content lines where the type uses them. Zero-quantity lines are dropped. There is no undo and no delete-activity method on this class. `WriteComment` can update a comment later and is not called by Activity History or Activity Details.
- **If it fails:** Per-line exceptions in `RegisterActivity` are swallowed. The insert is `INSERT IGNORE`.
- **Do not write:** Do not describe an undo. Do not say account or user codes 10–12 or 15–24 are written by a screen in this repo or listed in history. Do not say a zero-quantity line is stored.
- **Related:** ACT-001, ACT-002, ACT-005. WF-011 can land on Activity History after the replacement request.
- **Code:** `Activity.vb` `GetActivityDescription` 116–174, `ActivityCodeIndex` 206–243, `RegisterActivity` 245–325 (content guard at 272), `RegisterActivityHelper` 330–409.
- **Confidence:** Confirmed for the phrases and the content-row rule. Uncertain for rows written by `api/expirationReplacement`.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** What is stored as an activity

---

## EXP — Expirations

`SHOW_EXPIRATIONS` must be on (DSP-004). Direct `/Expirations` without that flag goes to `Settings#expirationsAnchor`. Read-only users go to `Expirations_read_only.aspx`, which lists rows and opens the product editor and does not render **manage**. The yellow window is DSP-005.

### EXP-001 — Expiration list

- **Open:** Header image `#expiration_icon`, or the collapsed menu link **Expirations**, when expirations are on for this user. Page title “Expirations (CyberStockroom)”. Heading **Product Expirations**.
- **Steps:**
  1. Open Expirations.
  2. Read the chips **{n} Expiring Soon** and **{n} Expired**.
  3. Read the list. Each row is `{product number} - {description}` plus a status. Click the row to open Product Editor.
  4. Type in the box (placeholder “search...”). Each keyup reloads page 1 with page size 100. On the editable page, **manage** opens EXP-002.
- **Options:** The list colors use the date only (time set to midnight):
  - Date before today: red `#AF5756`, white text, `expired ({yyyy-mm-dd})`.
  - Window greater than 0 and date on or before today plus that many days: yellow `#FFD966`, text `#454545`, `will expire in {n} days ({date})`.
  - Otherwise grey `#EEEEEE`, text `#454545`, `will expire on {date}`.
  The window comes from DSP-005. Stored `0` hides the yellow chip and no row is yellow. The chip counts use the server clock (`expirationDate <= Now` is expired; otherwise, if the window is greater than 0 and the date is within `Now` plus the window, it is expiring soon). The list uses the date only, so a product expiring later today can be counted one way and listed another. The chips count products from the product repository (page size 10,000,000). The list shows the first 100 API rows. Products past those 100 are counted and not listed.
- **Result:** Rows in the list. A row opens the product editor. The search box sends `searchTerms` as typed.
- **If it fails:** The list request’s error handler does not show a sentence. Duplicate product numbers in one response are skipped.
- **Do not write:** Do not say every expired product is on the list when the count is higher than 100. Do not invent which fields `searchTerms` matches. That match rule is outside this repo.
- **Related:** EXP-002, DSP-004, DSP-005, PED-005. WF-011.
- **Code:** `Expirations.aspx` `getExpirations` 54–84, `addListing` 90–149, colors 201–217, chips 42–47 and 296–297, search 305. `Expirations.aspx.vb` `Page_Init` 14–23, `_getExpirationCounts` 47–70. `Expirations_read_only.aspx` `addListing` 88–136 (no manage). `UserPage.master` 1291, 1383.
- **Confidence:** Confirmed for the page. Uncertain for which fields `api/expiration` `searchTerms` matches.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** See which products are expired or expiring

### EXP-002 — Replace or clone an expiring product

- **Open:** **manage** on a row of the editable Expirations page only. Read-only users do not get this button. Modal title **Manage this product's expirations**.
- **Steps:**
  1. Click **manage**. The title shows the description, product number, and date.
  2. Pick **New Expiration Date**. Pick **New Product Number**, or check **Auto**.
  3. Leave **Replace and Delete** selected, or choose another radio.
  4. Click the green button. **Cancel** closes the modal.
- **Options:** Default radio is **Replace and Delete** (value 1, checked). The footer button’s first label is **Replace** while `data-action` is already `replace_delete`. The label updates after a radio click. The checkboxes are `disabled`. They are a legend, not inputs.

  | Radio | Button label after selection | `action` | Legend that stays checked |
  | --- | --- | --- | --- |
  | Replace and Delete | Replace and Delete | `replace_delete` | Check-out old product from all locations. Delete the old product. Create a new product. Check-in new product to the same locations. |
  | Replace only | Replace only | `replace` | Same, except “Delete the old product.” is greyed |
  | Clone and Delete | Clone and Delete | `clone_delete` | “Check-in new product to the same locations.” is greyed |
  | Clone and Check-out | Clone and Check-out | `clone_checkout` | Delete old and check-in new are greyed |
  | Clone only | Clone only | `clone` | Check-out old, delete old, and check-in new are greyed. “Create a new product.” stays checked |

  **Auto** fills the box with `[Automatic Product Number]` and save sends `auto_sku_identifier` from the product repository. The comment sent is `Replacing expired product -  [Replace and Delete]` (two spaces before the bracket) or the matching bracket text for the other four actions. The POST is `https://code.cyberstockroom.com/api/expirationReplacement?action={action}` with headers `X-CS-TOKEN`, `X-CS-EXPIRATION-OLD-UID`, `X-CS-EXPIRATION-NEW-UID`, `X-CS-EXPIRATION-NEW-DATE`, and `X-CS-COMMENT`.
- **Result:** On HTTP success the browser goes to Activity History. What each action does to stock is Uncertain. The replacement work is not in this website project.
- **If it fails:** Empty date: **You must select an expiration date.** Changing the date to one `checkDate` treats as already passed shows **This date has already passed!** and turns the input `#AF5756`. Save does not repeat that date check. It only stops when the date box is empty. Empty product number: **You must select a product number.** A product number the products API returns as existing: **That product number already exists!** An HTTP error from that existence check is treated as “does not exist,” and save continues. A failed replacement POST only writes to the console. The modal has already faded to opacity 0.
- **Do not write:** Do not state what `replace_delete`, `replace`, `clone_delete`, `clone_checkout`, or `clone` does to quantities, locations, or the old product. The checklist is a legend. Do not describe those checkboxes as choices the user can toggle.
- **Related:** EXP-001, ACT-001, DSP-004, DSP-005. WF-011.
- **Code:** `Expirations.aspx` `checkDate` 334–353, radios 444–590, legend 540–564, `save` 614–660, `_post` 662–706, `_uidExists` 708–732. `Expirations.aspx.vb` `auto_sku_identifier` 34–35.
- **Confidence:** Confirmed for the wizard. Uncertain for what each action does to stock.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Replace or clone an expiring product

---

## KIT — Kitting

`SHOW_KITTING` must already be on. Direct `/Kitting` without the flag goes to `Settings#kittingAnchor`. The Settings checkbox is DSP-008. It is hidden and unwired. It is not how you turn kitting on. Nothing else in this repo sets the flag. Read-only users are sent to `Kitting_read_only`, and that file is not in the repo. There is no build and no break. There is no collapsed-menu Kitting link. The header image `#kitting_icon` shows only when the flag is on.

### KIT-001 — Kit list, create, delete, search

- **Open:** Header kitting icon when `SHOW_KITTING` is already on. Page title “Kitting (CyberStockroom)”. Heading **Product Kits & Assemblies**.
- **Steps:**
  1. Open Kitting. Read the chip **{n} Kits**.
  2. Click a kit name to expand **{n} Products included**. Click again to collapse.
  3. Click **+ NEW KIT**. The prompt is **New Kit Name:**. Accept to post the name. Cancel still posts, and the name becomes the string `null`.
  4. Type in the box (placeholder “search...”). Each keyup reloads page 1 with page size 100.
  5. Click **Delete Kit**. There is no confirm.
- **Options:** Create posts `{"id":-1,"name":"...","content":[]}` to `https://code.cyberstockroom.com/api/kit`. There is no duplicate check and no trim. Delete sends `DELETE https://code.cyberstockroom.com/api/kit/{id}` with an empty body. The list request is `GET https://code.cyberstockroom.com/api/kit?pageIndex=1&pageSize=100&searchTerms=`. The chip count uses `kitRepository.getAll` with page size 10,000,000 and can be larger than the 100 rows on screen. Create and delete refresh the list with an empty search even if the box still has text.
- **Result:** The list refreshes after a successful create or delete. Whether `id` `-1` inserts a kit, and which fields search matches, are Uncertain. The API is not in this repo.
- **If it fails:** Create, delete, and list errors are swallowed. The page shows no sentence. A quote in the kit name breaks the hand-built JSON.
- **Do not write:** Do not say the Settings kitting checkbox (DSP-008) turns kitting on. Do not describe a build or a break. Do not state the insert rules for `id` `-1`, an empty name, or the name `null`. Do not state which kit fields `searchTerms` matches. Do not describe `Kitting_read_only` as a working page.
- **Related:** KIT-002, KIT-003, DSP-008. WF-012.
- **Code:** `Kitting.aspx` `getKits` 46–89, `addListing` 109–186, `createNewKit` 544–548, `deleteKit` 316–336, search box 511, **+ NEW KIT** 535. `Kitting.aspx.vb` `Page_Init` 13–35, `_getkitCounts` 37–46. `Settings.aspx` `toggle_show_kitting` 532 (row hidden). `UserPage.master` 1354–1384.
- **Confidence:** Confirmed for the requests. Uncertain for API persistence and search matching.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** View, create, search, and delete kits

### KIT-002 — Kit components

- **Open:** Inside an expanded kit on the Kitting page. Same gate as KIT-001.
- **Steps:**
  1. Expand a kit. Each line is `{qty} x {description} ({product number})`.
  2. Click **+ Add New**. The modal title is **Add Item to Kit :** plus the kit name. Search products. The request uses page size 10. Click a row, or press Enter to take the first hit. The quantity prompt is **Please enter the new quantity for Product : {uid} in Kit: {name}**.
  3. Click the green quantity to get the same prompt for a product already in the kit.
  4. Click **x**. The confirm is **Are you sure you want to remove this item from the kit?**
- **Options:** Cancel on the quantity prompt, or a value that is `<= 0`, returns without a POST. Both add and remove POST the whole kit JSON to `https://code.cyberstockroom.com/api/kit`.
- **Result:** The intended refresh is a reloaded kit list. The posted JSON is defective. Editing a product that is already in the kit keeps `kit.content[j].quantity` (the old quantity). `newQty` is appended only when that product number was not found. Remove keeps a line only when the product number is different and the quantity is different, so every other component with the same quantity as the targeted line is dropped, and the targeted line is dropped. Do not treat this as a reliable editor. There is no build-into-inventory action.
- **If it fails:** The confirm is the only delete check. POST errors are swallowed. Non-numeric text is not `<= 0` in JavaScript (`NaN <= 0` is false), so that text continues into the POST.
- **Do not write:** Do not document quantity edit as saving the number the user typed for a product already in the kit. Do not document remove as deleting only the line that was clicked when another line has the same quantity. Do not describe a build or a break.
- **Related:** KIT-001, KIT-003. WF-012.
- **Code:** `Kitting.aspx` component markup 128–154, `changeQty` 197–255 (old quantity at 224), `deleteItem` 257–291 (same-quantity drop at 271), `getProducts` 576–614, `selectProduct` 629–638, `sendKitContent` 293–314, modal title 648.
- **Confidence:** Confirmed
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Add or remove products in a kit

### KIT-003 — Kit “manage” is not a kit action

- **Open:** A **manage** button is drawn on each kit row when the Kitting page loads. It is not a working kit action.
- **Steps:**
  1. Do not use **manage** to edit, build, or break a kit.
  2. The click handler sets `modal_kit_content` by concatenating the kit name without quotes (`addListing` around line 165), so the script throws before the modal logic runs.
- **Options:** The hidden modal is a copy of the expiration wizard: **New Expiration Date**, **New Product Number**, Replace and Delete, Replace only, Clone and Delete, Clone and Check-out, Clone only, and `api/expirationReplacement`. `Kitting.aspx.vb` never assigns `auto_sku_identifier`.
- **Result:** The wizard does not run from this button. Nothing about the kit is saved by this control.
- **If it fails:** The click throws. There is no sentence on the page for that error.
- **Do not write:** Do not publish **manage** as a kitting feature. Do not describe it as build, break, replace, or clone. Do not state what `api/expirationReplacement` would do to stock if the modal were reached.
- **Related:** KIT-001, EXP-002. WF-012.
- **Code:** `Kitting.aspx` `addListing` 164–169, wizard copy through `api/expirationReplacement` around 676–1062 (POST at 1042).
- **Confidence:** Confirmed
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Do not document kit manage as a kit action

---

## SRCH — Header search

### SRCH-001 — Header search

- **Open:** The toolbar box on `UserPage.master` (`CS_SEARCHBOX1`), including Activity, Expirations, Kitting, and the AI report. Placeholder is empty. Signed-in users see it, including read-only users. The create-product row is hidden for read-only users because Add Products is hidden.
- **Steps:**
  1. Type in the header box. Suggestions start at minimum length 0. Each request is `GET https://developers.cyberstockroom.com/api/search?API_TOKEN_ADMIN={cookie}&LIMIT=10` with the raw `term`. There are no search operators.
  2. Click a row whose category is `Products` to open Product Editor for that product number. Click a row whose category is `Locations` to open Location Editor for that location id.
  3. Press Enter to store the raw text on the product search cookie and open Products (PRD-006). The server appends a comma and that string onto `COOKIE_PRODUCT_SEARCH_FILTER` and redirects to `/Products.aspx`.
  4. If the API returns an empty array, the term is not empty, and Add Products is on the page, one row reads **Create New Product {term}**. Choosing it opens Add Products with `PreloadDescription` set to the term.
- **Options:** Limit 10. A newer response, or a term that no longer matches the box, is discarded. Local product and location markup is off. The widget uses the API. Categories other than `Products` and `Locations` are Uncertain. Which fields the API matches is Uncertain.
- **Result:** Product editor, location editor, the Products page with the term appended to the product search cookie, or Add Products with the description preloaded. Closing the product editor reloads the page when `CookieRefreshRequired=1` or `COOKIE_PRODUCTS_PAGE_RELOAD=TRUE`.
- **If it fails:** An HTTP error returns an empty list and does not show **Create New Product**. An empty term does not show that row. If the autocomplete cookie is missing, Enter’s server handler does nothing and does not redirect.
- **Do not write:** Do not invent which fields `api/search` matches. Do not invent categories other than `Products` and `Locations`. Do not say the create-product row appears for a read-only user. Do not document search operators.
- **Related:** PRD-006, PRD-007. WF-013.
- **Code:** `Controls/CS_SearchBox.ascx` `RegisterUserControlIndex` 67–266, `custom_search` 270–276, `openAddProductsFromEmptySearch` 283–291, placeholder 19. `UserPage.master.vb` `CS_SEARCHBOX1_AC_QuerySearchRequested` 339–344, `HideSectionsForReadOnlyUsers` 26–28. `CreateAutoCompleteGlobal` 285–297.
- **Confidence:** Confirmed for the client. Uncertain for API match fields and for categories other than Products and Locations.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Search products and locations from the header

---

## RPT — Reports

### RPT-001 — Download a product report

- **Open:** On Products, the download image tooltip is **Download Product Report**. It opens `ExportReport.aspx` in a Fancybox, or `ExportReport?LocationID=` when a location is selected. Page heading **Download Product Report**. Button **Download File**. Any signed-in user. This page has no read-only check and no feature flag.
- **Steps:**
  1. On Products, click the download icon.
  2. Choose a location, or leave all locations.
  3. Set **Include Products with 0 Quantity** and **Include Products in Sub-Locations**, and the field checkboxes.
  4. Click **Download File**.
- **Options:**

  | Control | Default | What it does |
  | --- | --- | --- |
  | Location selector | query `LocationID`, or the selector’s own populate | `-2` is all locations. **Include Products in Sub-Locations** is hidden when that query id is `-2`. |
  | Include Products with 0 Quantity | unchecked | When checked, products that are not already in the positive-quantity result are appended with quantity 0. Also forced on when the positive-quantity query returns zero rows. |
  | Include Products in Sub-Locations | unchecked | When checked and the location is not all, the query is that location and its descendants. |
  | Product Number | checked and disabled | Always included. Header **Product Number**. |
  | Description | checked | Header **Description**. |
  | Quantity | checked | Sum, or per-location quantity. Unchecking it disables **breakdown by location** in the browser. |
  | breakdown by location | checked | Adds **Location Path** and **Location Name**. |
  | Buy Price | checked | Header `Buy Price ({currency})`. Currency is the account currency. |
  | Cost Value | checked | Header `Cost Value ({currency})`. Value is quantity times buy price, rounded half away from zero to 2 decimals (`MidpointRounding.AwayFromZero`), formatted `F2`. If Cost Value is on and Buy Price or Quantity is off, those columns are still queried and then removed after the cost column is filled. |
  | Sell Price | checked | Header `Sell Price ({currency})`. |
  | Each custom field | checked | Header is the field name with commas replaced by `_`. |
  | Product Image | unchecked | Adds **Image URL**. |

  The positive-quantity filter is `Quantity > 0`. `SQL_CLAUSE_SEARCH` is always empty. The products search box is not applied. The filename is the readable location path plus `  - [DATE : {Now.ToLongDateString}]`, sanitized, max 200 characters, or `ALL LOCATIONS  - [DATE : {long date}]` when the path is empty, then `.csv`.
- **Result:** A CSV download. Before the query, `sanitizeLocationPathAndReturnReadablePaths` rewrites `Locations.LocationPath` for every location in the account (`UPDATE ... SET LocationPath=@P1 WHERE LocationID=@P2`). That rewrite runs on every download.
- **If it fails:** Download exceptions are swallowed. The page shows no sentence.
- **Do not write:** Do not say the product-list search is included. Do not say the download leaves `Locations.LocationPath` unchanged.
- **Related:** PRD-006, WF-013. Location-path text is also what Activity History uses for descendant filters (ACT-003).
- **Code:** `Products.aspx` download icon 662, Fancybox 146 and 456. `ExportReport.aspx` 53–120. `ExportReport.aspx.vb` `Page_Init` 17–30, `ExportReport` 51–167, `sanitizeLocationPathAndReturnReadablePaths` 170–209, `AppendCostValueColumn` 317–351, `DownloadFile` 353–418.
- **Confidence:** Confirmed
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Download a product report

### RPT-002 — AI insights report

- **Open:** There is no menu link, no href, and no redirect to this page anywhere else in this repo. A signed-in user who already has an id opens `/ai-report.aspx?id=` (or `/ai-report?id=`). Page title **AI Insights Report**. No `SHOW_*` flag.
- **Steps:**
  1. Open the URL with an id the report loader can read.
  2. Read the header **Your Inventory Insights**, the date, and the badge **AI-GENERATED**.
  3. Read each card. The footer label is **RECOMMENDATION**.
- **Options:** Query key `id` only. Card types from `reportContentItemType`: General, Location, Product, User. Each card has a title, italic bullet paragraphs, and a recommendation. The badge image is a sibling before the card, not inside it. `userFeedback` is read and not displayed. There is no export and no print button on the page. How reports are generated, and which ids exist, live in `SDK.Reports.AI.InsightsReport`, which is outside the files that were read.
- **Result:** A stack of cards under the date. Empty contents show the header only. Report text is assigned as HTML and is not encoded.
- **If it fails:** Any exception, including a bad id, redirects to Map with no message.
- **Do not write:** Do not write a menu path or a button that opens this page. Do not describe how an insights report is generated.
- **Related:** None of WF-011, WF-012, or WF-013 link here. WF-013’s download step is RPT-001.
- **Code:** `ai-report.aspx` title line 1, badge 116–120. `ai-report.aspx.vb` `ai_report_init` 13–27, `displayHeader` 37–40, `displayInsight` 42–76, `displayRecommendation` 109–114, `cardTypes` 134–139. A repo search for `ai-report` hits only these two files.
- **Confidence:** Confirmed that it is a signed-in page and that it has no menu link. Uncertain for how reports are generated.
- **KB Status:** Not audited. **KB Article URL:**
- **Suggested title:** Open an AI inventory insights report

## Uncertain items still not safe to publish as tutorial steps

- OAuth scope labels (\consentScreen\ / \uth\ are outside this website tree). ACC-015.
- Stored pairing inside \lansweeperFieldToggle\. LSW-003.
- Which of the duplicate Lansweeper class files the compiler binds. LSW-005.
- Database defaults for product images, zero quantity, and expirations on a brand-new admin. The Settings page displays whatever is already stored. Invites copy expirations from the inviter.
- Whether any live user still has \SUPER_USER\.
- Custom-field delete cascade beyond the on-screen warning. CFL-005.
- Google login failure text for a normal login. ACC-002.
- Half-hour time zones are not in the dropdown. ACCSET-001.
- \pi/LocationClone\ quantity copy. MAP-013.
- \pi/inventory\ stock math for Quick Scan, and the bodies of adjust, check-in, check-out, transfer, and clone beyond the request the page sends. XFR-011, MAP-014, MAP-026, PRD-010.
- \pi/expirationReplacement\ stock actions. EXP-002.
- \pi/kit\ insert rules and which fields kit search matches. KIT-001.
- \pi/search\ and \pi/map\ match fields. SRCH-001, MAP-018.
- \productDeleter\ child rows. PRD-011, PED-008.
- Database default for \Quantities.Quantity\ on the location \-2\ insert during create. PED-010.
- Whether a read-only user can drag the map move handle. MAP-002.
- \_cvr/SuccessSignup.aspx\ body text. ACC-014.
