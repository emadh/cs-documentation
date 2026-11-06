# Settings and account — code catalog

Audit date: 2026-11-05. Source of truth is the application code under `cs-website`. No runtime click-through was performed. Plan prices, Stripe product marketing names, and Lansweeper scope wording that are not string literals in this repo are not invented.

`Company.vb` is an empty `CompanySettings` structure. It does not drive any settings screen.

`CS_FIELDS.FieldType` is only `PRODUCT_PROPERTY` and `CUSTOM_FIELD`. The Settings custom-field editor does not offer date, number, or dropdown field types. A custom field is a named text field, optionally with a preset list.

`webAPI/products.aspx` (`GetPopularProducts`, `SearchProducts`, `CreateProducts`) and `webAPI/locations.aspx` (`UpdateParent`) are not called by the Settings page. Default locations are saved by `_locationSelectorToggle.aspx.vb`, not by `webAPI/locations.aspx`.

---

## Page inventory

| Page | What a signed-in person sees | Who reaches it |
| --- | --- | --- |
| `Settings.aspx` | Left menu plus the sections `ShowAllowedSections` turns on. Master page is `UserPage.master`, which requires a login. | All signed-in roles. Section set depends on effective user type. |
| `Controls/ProfileIconPicker.ascx` | Avatar preview, upload, presets 1–15, Apply. On Settings the name box inside the picker is hidden (`showName=False`). | Settings profile; also `ProfileRequired.aspx`. `Welcome.aspx` configures it but redirects away before that runs. |
| `Controls/CustomFieldEditorModal.ascx` | Same custom-field cards as Settings, including Personalized Sort. Presets button is omitted when the list sits inside `#custom_field_editor_modal`. | Registered on `Products.aspx`, `ProductEditor.aspx`, `AddProducts.aspx`, `ImportFromFile.aspx`. Not registered on `Settings.aspx`. |
| `Popups/FixedMultiFields.aspx` | Preset values plus “allow other”. Opened from a Settings custom-field Presets button. | Admin custom-field edit path. |
| `pages/settings/popups/lansweeperSiteSelector.aspx` | Checkboxes of Lansweeper sites, Connect. | Not linked from the live Settings markup. `InitLansweeper` is commented out. |
| `pages/settings/popups/lansweeperFieldToggle.aspx` | Picker of this account’s custom-field names to match a Lansweeper field. | Same: popup exists, Settings connect UI is commented out. |
| `_locationSelectorToggle.aspx` | Map picker used by Settings. `CodeFile` is `_locationSelectorToggle.aspx.vb`. Header and save target depend on `?type=`. | Default check-in, default check-out, and `type=lansweeper`. Read-only users are redirected to `/_admin/_unauthorized`. |
| `pages/settings/popups/lansweeperCategoryLocationToggle.aspx` | Separate page. Its code-behind `Page_Init` is empty. It declares the same class name as `_locationSelectorToggle.aspx.vb`. | Not the href used by Settings. |
| `pages/settings/popups/lansweeperLinkAndSync.aspx` | Empty body. On first load it links and starts a sync if `progress = 0`, and writes `ColumnOrder`. | Not linked from live Settings markup. |
| `pages/settings/popups/lansweeperConnectionSuccess.aspx` | Progress percent and status text. At 100% waits 1.5s and redirects to `/Map`. | Redirect target of the site selector. |
| `pages/settings/popups/lansweeperConnectionFailure.aspx` | Static failure message. Code-behind is empty. | Redirect target when the site selector throws. |
| `UpdateAccount.aspx` | “Monthly and Annual Plans” images, a non-clickable enterprise image, and Stripe checkout. `?Update=Payment` calls `updatePayment()`. | Opened from the subscription card. Page blocks `READ_ONLY` only. It does not require `ADMIN`. |
| `UpdateAlert.aspx` | Banner plus an iframe of `UpdateAccount.aspx`. | Linked by hidden anchors on Settings. Those anchors are not auto-opened by `settings.js`. |
| `BillingHistory.aspx` | Next payment date and amount when Stripe returns a subscription, then a charges table: Date, Amount, Subscription, Status (`Successful` / `Failed`). | Admin only. Non-admins go to `/_admin/_unauthorized`. |
| `Login.aspx` | Email, password, Google sign-in, Forgot Password. Invitation and password-reset query strings change the labels. | Public. |
| `SecureRegistration.aspx` | Iframe of `UpdateAccount.aspx` (no `Update` query). | Public signup shell. |
| `Welcome.aspx` | `Page_Init` redirects to `/Map` and returns. The profile and demo-data code below that line does not run. | Any request to Welcome. |
| `ProfileRequired.aspx` | Name plus profile icon. Save reloads the parent, or goes to `/Map` if there is no parent. | Opened by `UserPage.master` when `FirstName` is blank, except on Settings and printable views. |
| `SuccessSignup.aspx` | “Success! Thank you for Updating your subscription.” Code-behind is empty. | Redirect after Stripe plan or card update in `UpdateAccount.aspx.vb`. |
| `_cvr/SuccessSignup.aspx` | Separate copy. `UpdateAccount` redirects to `_cvr/SuccessSignup` from some payment paths and to `SuccessSignup` from others. | See Update Account feature. |
| `OAuth2/auth.aspx` | Hosts panels filled by `New auth(...)`. | OAuth entry. |
| `OAuth2/consent.aspx` | Cancel and Allow. Body is `New consentScreen(clientId, scopes).Panel`. That class is not defined in this website project. | After OAuth request validation. |

Commented-out Settings markup (not rendered): Lansweeper Synchronize button, Disconnect button, and the connect panel inside `section_lansweeper`.

Hidden from the layout, still in the DOM: the Kitting row (`style="display: none;"`). No `CheckedChanged` handler exists in `Settings.aspx.vb`.

---

## Permission model

Roles are `User_Legacy.TypeOfUserAccount`: `ADMIN`, `USER`, `SUPER_USER`, `MOBILE`, `READ_ONLY` (`User_Legacy.vb` 441–447).

`GetEffectiveUserType` maps `MOBILE` to `USER` and leaves every other value unchanged (`User_Legacy.vb` 449–451). `GetDisplayUserType` shows `MOBILE` as `USER` (`User_Legacy.vb` 454–456).

Settings menu and sections use `GetEffectiveUserType` (`Settings.aspx.vb` 70–144):

| Effective type | Menu | Sections |
| --- | --- | --- |
| `ADMIN` | Profile & Team, Custom Fields, Default Locations, API & Integrations, Options, Subscription | Profile, team, custom fields, default locations, API, Lansweeper block, display settings, Share Map Layout row, account settings (time zone and currency), subscription |
| `USER` (includes stored `MOBILE`) | Same except Subscription | Profile, team, custom fields, default locations, API, display settings. Lansweeper, account settings, subscription, and the Share Map Layout row stay `Visible=False` |
| `READ_ONLY` | Profile & Team, Custom Fields, API & Integrations, Options. Default Locations and Subscription menus stay off | Profile, custom fields, API, display settings. Team, default locations, Lansweeper, account settings, subscription stay off |
| `SUPER_USER` | No `Case` matches. Every section starts `visible="false"`, so the page shell renders with no sections | Same |

`webAPI_Utilities.isAllowed` (`webAPI_Utilities.vb` 19–76):

- Cookie `csToken` must equal the token posted by the page.
- A login session cookie must exist.
- `ADMIN` is allowed only when `allowAdmins` is true.
- `USER` and `MOBILE` are allowed only when `allowUsers` is true.
- `READ-ONLY` is allowed only when `allowReadOnly` is true.
- Anything else, including `SUPER_USER`, is denied.
- Defaults are all four flags true.

Calls that pass `False` and therefore block that role:

| Action | Admins | Users / MOBILE | Read-only |
| --- | --- | --- | --- |
| Display toggles, threshold, max highlight, expiring soon, API key create/delete | yes | yes | yes |
| Share map layout | yes | no | no |
| Custom-field order, price visibility, personalized sort | yes | yes | yes |
| Time zone, currency, invite, set role, delete user, cancel subscription | yes | no | no |
| Create, rename, delete custom field | yes | no | no |
| Rename self, change own email | yes | yes | yes |

UI gates that are stricter or looser than the API are called out on each feature. The important ones: a `USER` still sees the invite form; API keys appear only when the account is on `CS_API_v0._betaList`; custom-field create/rename/delete/presets render only when `hidden_custom_fields_can_edit` is `1`, which Settings sets only for raw `TypeOfUser = ADMIN` (`Settings.aspx.vb` 262–265). A stored `MOBILE` user is treated as `USER` for the menu, and `canEdit` is false because the raw type is not `ADMIN`.

`UserPage.master.vb` 61–63 hides Start, add-products, and tools for `READ_ONLY`. `BillingAccessGate.Enforce` (`BillingAccessGate.vb` 10–22) redirects to `/Settings` when:

- trial is expired and `SuppressUpgradeAlert` is false, or
- `ConfirmedPayment = 1`, the Stripe customer is delinquent, and `SuppressPaymentAlert` is false.

It does not redirect again when the current page name is `Settings`. Trial expiry is computed as 14 days from `Accounts.DateCreated` when `ConfirmedPayment` is 0 (`Account.vb` 889–901). `ConfirmedPayment > 0` means the trial is not expired.

`AccountSettings.AccountType` is an integer copied into `hidden_AccountType` (`UserPage.master.vb` 65, `Account.vb` 984). This catalog did not find a settings-section branch on that integer.

---

## Profile

### Profile name

- Pages: `Settings.aspx` `txt_profile_user_name`; `ProfileRequired.aspx`; `Welcome.aspx` (unreachable).
- What it does: On change, `updateUserName` posts `webAPI/users.aspx/UpdateUserName`. The server trims the name and calls `User_Legacy.DisplayNameError`, then `userModifier.set_name` (`users.aspx.vb` 66–82, `User_Legacy.vb` 104–119). Settings also rewrites the current user’s team card via `refreshCurrentUserCardName` (`profile.js` 22–47, `user-card.js` 171–196).
- Why: The name is `Users.FirstName`. Activity rows and the collapsed menu use it (`UserPage.master.vb` 115).
- How to access + visibility: Settings profile section. Menu `section_menu_profileAndTeam`. Visible for Admin, User, and Read-only.
- Options and defaults: Placeholder `Enter Name...`. Loaded from `MO.UserCredentials.FirstName` when length > 0 (`Settings.aspx.vb` 158–164).
- Permissions: Any authenticated role. `isAllowed` is called with defaults (`users.aspx.vb` 67).
- Validation/failures: Empty after trim: “Please enter your name.” Longer than 50: “Please use 50 characters or fewer.” Duplicate on the account: “Someone sharing this account is using this name already...” The input gets an error state and that message as `title` (`profile.js` 33–35). Escape restores the focused value (`text-input.js` 12–26).
- Result: `CS_ADMIN.Users.FirstName` for the current user. Team card and, after reload, the menu name.
- Edge cases: Uniqueness ignores the user’s current name (`DisplayNameError` passes `FirstName` as `currentName`). Blank names on other pages open `ProfileRequired` (`UserPage.master.vb` 355–360). Settings itself does not open that popup.
- Code evidence: `Settings.aspx` 133; `Settings.aspx.vb` 158–164; `js/business/profile.js` 22–47; `webAPI/users.aspx.vb` 66–82; `User_Legacy.vb` 104–119.
- Confidence: Confirmed
- Suggested KB title: Change your name in Settings

### Profile email

- Pages: `Settings.aspx` `txt_profile_email`.
- What it does: `updateUserEmail` posts `UpdateUserEmail`. Server uses `emailValidator`: format, not already in this account, not in any account, and not a pending invitation (`users.aspx.vb` 95–120).
- Why: Login and invitations key off `Users.Email`.
- How to access + visibility: Profile section, all three effective roles that see profile.
- Options and defaults: Current `MO.UserCredentials.Email` (`Settings.aspx.vb` 166–168). Input type `email`.
- Permissions: Any authenticated role.
- Validation/failures: Failure sets the input title to “That email is invalid or already exists.” (`profile.js` 58–60). The server throws `ArgumentException` with no message (`users.aspx.vb` 119).
- Result: `userModifier.set_email` commits the new email.
- Edge cases: The “same as old” short-circuit compares `new_email` to `MO.UserCredentials.FirstName`, not to the current email (`users.aspx.vb` 102–105). A no-op only happens when the typed email string equals the person’s name. Google-linked users can still edit this field; only the password block is hidden.
- Code evidence: `Settings.aspx` 139; `js/business/profile.js` 50–61; `webAPI/users.aspx.vb` 95–120.
- Confidence: Confirmed
- Suggested KB title: Change the email on your user

### Password update

- Pages: Settings profile; `Login.aspx` for reset and invitation acceptance.
- What it does: “Update Your Password” shows old, new, and repeat boxes. Save posts back `btn_password_reset_click`, which calls `SignInApplicationService.ChangePassword` (`Settings.aspx.vb` 180–193, `SignInApplicationService.vb` 11–43).
- Why: Replaces `passwordHash` and `passwordSalt` for the current user (`SignInApplicationService.vb` 71–84).
- How to access + visibility: Profile section, unless `GoogleID` length is greater than 0. Then the instruction and key icon are hidden (`Settings.aspx.vb` 209–243).
- Options and defaults: Placeholders Old Password, New Password, Repeat Password. Fields start empty. The block is `display: none` until `ShowPasswordField`.
- Permissions: The signed-in user only. This is a page postback, not the web API role matrix.
- Validation/failures: Server messages, written into the “Update Your Password” label in red: “The password is incorrect. Try Again?”; “The passwords don't match. Try Again?”; “That password is too short. Please use at least 6 characters. Try Again?”; “The new password must be different! Try Again?” Client coloring on new and repeat only: empty stays white; length under 6 is red; under 9 is yellow; 9 or more is green (`profile.js` 65–87). Client color does not block the postback. Success redirects to `Settings.aspx`. Cancel only hides the div (`Settings.aspx` 163).
- Result: Salted SHA-256 password. Old unsalted hashes are still accepted for the old-password check (`SignInApplicationService.vb` 54–67).
- Edge cases: No maximum length in this method. Google-linked users have no password form on Settings.
- Code evidence: `Settings.aspx` 149–164; `Settings.aspx.vb` 150–152, 180–193, 209–243; `SignInApplicationService.vb` 11–84; `js/business/profile.js` 65–96.
- Confidence: Confirmed
- Suggested KB title: Update your password

### Link a Google account

- Pages: Settings profile; also `Login.aspx`.
- What it does: The Google button’s `onSignIn` stores the Google ID token and clicks the hidden `btnGoogleLogin`. The server calls `VerifyGoogleToken` against Google’s tokeninfo endpoint and requires `aud` equal to the app client id in `Settings.aspx` line 25. It then `updateGoogleID` (`Settings.aspx.vb` 195–204, `SignInApplicationService.vb` 88–137, `UserApplicationService.vb` 29–36).
- Why: A stored `GoogleID` is what later hides the password form and shows “Signed in with Google”.
- How to access + visibility: Panel starts `display: none` and is set to `display: block` only when `GoogleID` is empty (`Settings.aspx.vb` 209–211).
- Options and defaults: One Google button (`g-signin2`, long title, dark theme).
- Permissions: Current user. Failed token verification exits without a message (`Settings.aspx.vb` 199–201).
- Validation/failures: Audience mismatch returns false. No on-page error string.
- Result: `Users` Google ID is set. Redirect to `Settings#profile`. Password controls disappear on the next load. The Google email is read from the token but is not written by `btn_google_login_click`.
- Edge cases: `settings.js` calls `ResetGoogleAuth` on load, which signs the Google JS client out (`profile.js` 98–101, `settings.js` 8–10).
- Code evidence: `Settings.aspx` 184–189; `Settings.aspx.vb` 195–243; `js/business/profile.js` 98–117; `SignInApplicationService.vb` 88–137.
- Confidence: Confirmed
- Suggested KB title: Link Google to an existing user

### Profile picture

- Pages: `Controls/ProfileIconPicker.ascx` on Settings and `ProfileRequired.aspx`.
- What it does: Choose preset `1`–`15` or upload. Apply posts `btn_apply_Click`. Upload goes through `ProfileIcons.SaveUpload`. A preset copies `Images/Avatars/{n}.png` via `saveProfileImage` (`ProfileIconPicker.ascx.vb` 69–86, `ProfileIcons.vb` 72–103).
- Why: `imageProcessor.getProfileImage` is what the menu and team cards show.
- How to access + visibility: Left of the name on Settings. `Configure(..., showName:=False, immediate:=True, returnUrl:="Settings.aspx#profile")` (`Settings.aspx.vb` 171–173).
- Options and defaults: Preset keys `1` through `15` (`ProfileIconPicker.ascx` 17–31). `DefaultKey` is `"1"` (`ProfileIcons.vb` 10). Accept `image/png,image/jpeg,image/gif,image/webp`.
- Permissions: Current user. No role check in the picker.
- Validation/failures: “Please choose an image file.” when empty, wrong extension, or zero length. “Please choose an image under 3 MB.” when `ContentLength > 3 * 1024 * 1024` (`ProfileIcons.vb` 81–90). Error is `lbl_error`.
- Result: Profile image bytes for that user index, and the icon key (`custom` or `1`–`15`).
- Edge cases: Settings does not show the picker’s own name box. Name is the separate profile field.
- Code evidence: `Controls/ProfileIconPicker.ascx` 16–38; `Controls/ProfileIconPicker.ascx.vb` 28–86; `ProfileIcons.vb` 9–10, 72–103; `Settings.aspx.vb` 171–173.
- Confidence: Confirmed
- Suggested KB title: Choose a profile picture

### Role badge on your own profile

- Pages: Settings profile.
- What it does: Shows one badge from the effective type: Admin, User, or Read-Only (`Settings.aspx.vb` 247–254).
- Why: Display only. It does not change permissions.
- How to access + visibility: Right side of the profile block.
- Options and defaults: Markup also has a Mobile badge (`Settings.aspx` 177). Nothing sets `badge_mobile.Visible = True`. Stored `MOBILE` is shown as User.
- Permissions: Whoever can see profile.
- Validation/failures: None.
- Result: No data change.
- Edge cases: `SUPER_USER` matches none of the badge cases, and that user also gets no profile section.
- Code evidence: `Settings.aspx` 175–178; `Settings.aspx.vb` 247–254; `User_Legacy.vb` 449–456.
- Confidence: Confirmed
- Suggested KB title: What the role badge on your profile means

---

## Team

### Team list, search, role filters, paging

- Pages: `Settings.aspx` `section_team`, `div_users`.
- What it does: `InitUsers` serializes `UserApplicationService.getAllUsersInAccount_Basic` and calls `loadUsers` (`Settings.aspx.vb` 175–178). Cards sort Admin, then User, then Read-only (`user-card.js` 16–17). Search matches name or email. Role pills filter `ADMIN`, `USER`, `READ-ONLY`. Page size is 12 (`user-card.js` 7, `filters.js` 12–21, `pagination.js` 4–35).
- Why: Shows everyone returned for the account id, including the image URL stored on the user.
- How to access + visibility: Profile & Team menu. Section is on for Admin and User. Off for Read-only (`Settings.aspx.vb` 108, 120, 136).
- Options and defaults: Search and pills stay `display: none` until the unfiltered list length is greater than 12 (`filters.js` 14–21). Placeholder “Search by name or email...”.
- Permissions: Seeing the list does not allow managing it. `canManage` is true only when the current card’s type is `ADMIN` and the card is not yourself (`user-card.js` 24, 56–67).
- Validation/failures: No matches shows “No users found”.
- Result: Display only.
- Edge cases: A legacy `MOBILE` row is labeled `USER`, so it sorts and filters as User. Names that are still blank (pending invites are inserted with an empty `FirstName`) still appear if `getAllBySchema` returns them.
- Code evidence: `Settings.aspx` 204–233; `Settings.aspx.vb` 175–178; `js/components/user-card.js` 11–144; `js/components/filters.js` 6–37; `js/components/pagination.js` 4–35; `UserApplicationService.vb` 11–21.
- Confidence: Confirmed
- Suggested KB title: Find a teammate in Settings

### Change a teammate’s role

- Pages: Role `<select>` on each team card except your own.
- What it does: Confirm dialog, then `set_user_type` → `webAPI/users.aspx/SetUserType`, which writes `userParams.userType = newUserType` (`users.js` 5–27, `users.aspx.vb` 38–52).
- Why: That string is what `isAllowed` and `GetEffectiveUserType` read later.
- How to access + visibility: Team section. Non-admins see the select disabled (`user-card.js` 66–81). Your own card has no select.
- Options and defaults: Option text `ADMIN`, `USER`, `READ-ONLY`. There is no Mobile option. Current value comes from `GetDisplayUserType`.
- Permissions: API allows admins only (`isAllowed` with users, mobile, and read-only false) (`users.aspx.vb` 39).
- Validation/failures: `MOBILE` throws “MOBILE role is no longer supported.” The UI cannot send that value. Cancel closes the confirm and does not post. A failed post reloads the cards from the last hidden JSON (`users.js` 29–33).
- Result: `TypeOfUser` for that user index. The page does not check that the index belongs to the same account, and it does not keep at least one admin.
- Edge cases: You cannot change your own role from this control. A disabled select is still visible to Users.
- Code evidence: `js/components/user-card.js` 66–117; `js/business/users.js` 5–34; `webAPI/users.aspx.vb` 38–57.
- Confidence: Confirmed
- Suggested KB title: Change a teammate’s role

### Delete a teammate

- Pages: DELETE on another user’s card.
- What it does: Confirm, then `delete_user` → `DeleteUser` → `repo.deleteByID` (`users.js` 37–66, `users.aspx.vb` 18–26).
- Why: Removes that user row.
- How to access + visibility: DELETE is rendered only when the viewer is Admin and the card is not themselves (`user-card.js` 65–70).
- Options and defaults: None.
- Permissions: Admin API only (`users.aspx.vb` 20).
- Validation/failures: Confirm copy is “Are you sure you want to delete the user …”. Cancel does nothing. Failure reloads cards.
- Result: User row deleted. If that was the last card on a page, the list moves to the previous page (`users.js` 58–65). Page size 12.
- Edge cases: No “last admin” guard in `DeleteUser`. The method does not compare the target account id to the caller’s account.
- Code evidence: `js/components/user-card.js` 65–127; `js/business/users.js` 37–73; `webAPI/users.aspx.vb` 18–30.
- Confidence: Confirmed
- Suggested KB title: Remove a teammate

### Invite a teammate

- Pages: Settings “Invite a Team Member”.
- What it does: `sendInvitation` checks a simple email pattern, then `send_invitation` → `SendInvitation` (`invitations.js` 5–49, `invitations.aspx.vb` 18–34). The server inserts or updates `CS_ADMIN.Users` with a new invitation GUID and emails `Login.aspx?Invitation={guid}` (`invitations.aspx.vb` 37–102).
- Why: Creates a user row the person can finish on the login page.
- How to access + visibility: The form is inside `section_team`, so Admin and User see it. Read-only does not. The API allows admins only (`invitations.aspx.vb` 19).
- Options and defaults: Role select values `ADMIN`, `USER`, `READ-ONLY` (`Settings.aspx` 252–256). The select has no explicit default attribute; the first option is `ADMIN`. Email placeholder `example@company.com`. Name stored on the row is an empty string (`invitations.aspx.vb` 28, 41).
- Permissions: Admin API. A User can click the button; the request is unauthorized and the button becomes “Unable to Invite - Try Again?” (`invitations.js` 46–48).
- Validation/failures: Empty email: “Please enter an email address.” Pattern failure: “Please enter a valid email address.” Role `MOBILE` is rejected server-side; the select cannot send it. While the request runs, `blockAllActions` disables invite, custom-field controls, and API-key controls (`action-blocking.js` 14–64).
- Result: New row: `TypeOfUser` = selected role, `InvitationID` = GUID, `_onboardingPlaybook` = 1, `_onboardingCompleted` = 1, `_onboardingStatus` = `finalize`. `GridsterCoordinates2017` is copied from the inviter with the share-map marker stripped. `SHOW_EXPIRATIONS` is copied from the inviter (`invitations.aspx.vb` 50–76). Email subject is “{inviter name} is inviting you to CyberStockroom. Details Inside.” From address `admin@cyberstockroom.com`.
- Edge cases: If this account already has that email, the update changes invitation id, name, onboarding flags, map coordinates, and expirations. It does not change `TypeOfUser` (`invitations.aspx.vb` 67–69). If the email exists on any account and there is no row on this account, `LEGACY_CREATE_INVITATION` returns without inserting, but `SendInvitation` still calls `LEGACY_SEND_INVITATION` and returns success (`invitations.aspx.vb` 28–31, 71–74). The button then says “Send Another Invitation”.
- Code evidence: `Settings.aspx` 244–259; `js/business/invitations.js` 5–57; `webAPI/invitations.aspx.vb` 18–102; `js/business/action-blocking.js` 14–64.
- Confidence: Confirmed
- Suggested KB title: Invite a teammate and choose their role

---

## Custom fields

There is no separate “field type” control. Cards are either a real custom field (`cardType` `CUSTOM_FIELD`) or the built-in Buy Price / Sell Price tokens.

Default order tokens: Buy Price `1000000001`, Sell Price `1000000002`, then each `CF_Index` (`CustomFieldApplicationService.vb` 167–179, `Gridster_Utilities.vb` 79–80).

Buy and Sell visibility default on, because a missing hide-token means show (`Gridster_Utilities.vb` 732–739). Personalized sort defaults off (`Gridster_Utilities.vb` 742–744).

Order, visibility, and the personalized-sort flag are stored in the current user’s `GridsterCoordinates2017`, not as account-wide field metadata (`webAPI/settings.aspx.vb` 263–289). Field names and preset lists are account-wide (`customFields.aspx.vb`).

### Personalized sort

- Pages: Settings custom-fields section and `CustomFieldEditorModal.ascx`.
- What it does: `handlePersonalizedSortToggle` sets the hidden flag and calls `save_custom_field_order` (`custom-fields.js` 344–389, `webAPI.js` 215–227). The server writes order, buy/sell visibility, and the personalized-sort flag (`settings.aspx.vb` 263–295).
- Why: When the flag is on, `getCustomFields` returns fields in that user’s saved order (`CustomFieldApplicationService.vb` 16–42). When it is off, the settings list hides Buy Price and Sell Price cards (`custom-field-card.js` 82–93).
- How to access + visibility: Custom Fields menu. Admin, User, and Read-only.
- Options and defaults: Checkbox. Server value `hidden_personalized_sort_enabled` is `1` or `0`. Default `0` in markup and when the coordinate token is absent.
- Permissions: `SaveCustomFieldOrder` allows admin, user, and read-only (`settings.aspx.vb` 264).
- Validation/failures: Failure alert “Unable to save the personalized sort preference right now.” and the toggle reverts (`custom-fields.js` 364–385).
- Result: Up/down buttons appear on every card, including Buy and Sell, only while the toggle is on (`custom-field-card.js` 259–264). Moving a card persists that user’s order (`custom-fields.js` 277–309).
- Edge cases: `NormalizeCustomFieldOrder` drops tokens that are not in the available list and appends missing ids (`Gridster_Utilities.vb` 816–834). A new field therefore shows up at the end of a personalized list after the next normalize. Turning sort off does not delete the saved order; the active list switches back to the default card JSON (`CustomFieldApplicationService.vb` 114).
- Code evidence: `Settings.aspx` 291–296; `Settings.aspx.vb` 261–270; `js/business/custom-fields.js` 277–389; `js/components/custom-field-card.js` 82–93, 259–264; `webAPI/settings.aspx.vb` 263–295; `Gridster_Utilities.vb` 742–744, 816–834.
- Confidence: Confirmed
- Suggested KB title: Turn on a personal custom-field order

### Buy Price and Sell Price visibility

- Pages: Those two cards, only while personalized sort is on. In the modal, a hidden price field is a compact row with a Show toggle (`custom-field-card.js` 120–124, 274–304).
- What it does: The Show toggle calls `toggleSpecialFieldVisibility`, which saves `showBuyPrice` / `showSellPrice` (`custom-fields.js` 107–125, 312–341).
- Why: Map and editors read `GetShowBuyPriceFromRaw` / `GetShowSellPriceFromRaw` (`Map_CONTROL_2017.ascx.vb` 158, `Account.vb` 469).
- How to access + visibility: Custom-field section, any role that can open it, but the cards are filtered out of the Settings list when personalized sort is off. So a person cannot change price visibility from Settings until they turn personalized sort on.
- Options and defaults: Show checked when `isVisible !== false`. Account default is visible.
- Permissions: Same as save order: admin, user, and read-only. Names are not editable (`allowNameEditing = False`). There is no delete button.
- Validation/failures: “Unable to save the field visibility right now.”
- Result: Per-user hide tokens in coordinates. Hidden cards get class `custom-field-card-hidden` but stay on the Settings list so Show can be turned back on.
- Edge cases: The word on the card is the literal “Buy Price” or “Sell Price”, subtitle “DEFAULT” (`CustomFieldApplicationService.vb` 123–143, `custom-field-card.js` 169–173).
- Code evidence: `CustomFieldApplicationService.vb` 118–144; `js/components/custom-field-card.js` 82–93, 181–209; `js/business/custom-fields.js` 312–341; `Gridster_Utilities.vb` 732–739.
- Confidence: Confirmed
- Suggested KB title: Show or hide Buy Price and Sell Price

### Create a custom field

- Pages: “Create New Field...” input under the list, Settings and the modal.
- What it does: Change event calls `createNewCustomField` → `CreateNewCustomField`, which inserts `fieldName` and returns the new `CF_Index` (`custom-fields.js` 187–229, `customFields.aspx.vb` 41–53).
- Why: Adds an account custom field that product screens can store values in.
- How to access + visibility: The input is appended only when `hidden_custom_fields_can_edit` is `1` (`custom-field-card.js` 115–117). Settings sets that only for raw type `ADMIN` (`Settings.aspx.vb` 262–265).
- Options and defaults: Empty text. Placeholder “Create New Field...”. New card is `CUSTOM_FIELD`, `validValues: [""]`, visible, name editable (`webAPI.js` 462–473).
- Permissions: API admin only (`customFields.aspx.vb` 43).
- Validation/failures: No empty-name or duplicate-name check in `CreateNewCustomField`. HTTP failure marks the input as error. Concurrent actions alert “Another action is currently in progress...”
- Result: New custom-field row. Both the default and personalized in-memory lists get a copy (`custom-fields.js` 209–214). Other users see it after reload, appended by normalize if they have a saved order.
- Edge cases: A User or Read-only person can reorder and toggle price visibility but cannot create.
- Code evidence: `js/components/custom-field-card.js` 349–384; `js/business/custom-fields.js` 187–229; `webAPI/customFields.aspx.vb` 41–57; `webAPI/webAPI.js` 442–477.
- Confidence: Confirmed
- Suggested KB title: Add a custom field

### Rename a custom field

- Pages: The name input on a `CUSTOM_FIELD` card.
- What it does: Change posts `RenameCustomField`, which sets `cf.fieldName` (`custom-fields.js` 171–184, `customFields.aspx.vb` 17–29).
- Why: The name is the label on product and map surfaces.
- How to access + visibility: Admin cards only (`allowNameEditing` and `canEdit`). Buy and Sell inputs are read-only for everyone.
- Options and defaults: Current `fieldName`.
- Permissions: Admin API.
- Validation/failures: No length or uniqueness check in the web method. Failure uses the text-input error state. No alert string.
- Result: Account-wide rename. Both local collections update (`custom-fields.js` 64–76).
- Edge cases: Enter blurs and fires change (`text-input.js` 16–19). Escape restores the previous text and does not save.
- Code evidence: `js/components/custom-field-card.js` 145–162; `js/business/custom-fields.js` 171–184; `webAPI/customFields.aspx.vb` 17–33.
- Confidence: Confirmed
- Suggested KB title: Rename a custom field

### Delete a custom field

- Pages: DELETE on an admin custom-field card.
- What it does: Confirm, then `DeleteCustomField` → `repo.deleteByID` (`custom-fields.js` 232–274, `customFields.aspx.vb` 66–74).
- Why: Removes the field definition.
- How to access + visibility: Admin cards. Not shown for Buy Price or Sell Price.
- Options and defaults: None.
- Permissions: Admin API.
- Validation/failures: Confirm text: “Are you sure you want to delete the field … Warning: Existing data for this field will be erased! It is recommended that you export your inventory first before deleting custom fields.” Cancel stops. Failure sets the input error state.
- Result: Field row deleted and removed from both local lists. The warning is the code’s statement that existing values are erased; this catalog did not trace the repository’s cascade.
- Edge cases: Buy and Sell cannot be deleted from this UI.
- Code evidence: `js/components/custom-field-card.js` 212–227; `js/business/custom-fields.js` 232–274; `webAPI/customFields.aspx.vb` 66–79.
- Confidence: Confirmed
- Suggested KB title: Delete a custom field

### Custom-field presets

- Pages: Presets button on Settings cards only. `ShowFixedMultiField` opens `Popups/FixedMultiFields.aspx?id={CF_Index}` (`custom-fields.js` 392–406). The modal sets `showPresets` false (`custom-field-card.js` 109–110).
- What it does: Save calls `CustomFieldApplicationService.SavePresets` (`FixedMultiFields.aspx.vb` 66–75).
- Why: `validValues` become the allowed choices. `CustomFieldHasPresets` is true when any value is non-blank and not `Other (Specify)` (`CustomFieldApplicationService.vb` 49–60).
- How to access + visibility: Admin, Settings page, real custom fields. Button class `has-values` when a real preset exists, otherwise `empty` (`custom-field-card.js` 237–244).
- Options and defaults: Checkbox `chk_allow_other`. New fields start with `validValues: [""]`, which is not a preset. If the saved list is empty, the field stays a normal text field (`CustomFieldApplicationService.vb` 85–89).
- Permissions: The Settings button is admin-only. `SavePresets` itself has no role check in the application service; the popup page’s own gate was not re-read for this catalog beyond the save call.
- Validation/failures: Blank values and the literal `Other (Specify)` are stripped from the posted list. “Allow other” appends `Other (Specify)` only when at least one real preset remains (`CustomFieldApplicationService.vb` 70–89).
- Result: `customField.validValues` replaced and committed.
- Edge cases: Presets are not available from the product-page modal. Fancybox close for this popup does not refresh Settings (`settings.js` 276–291 `afterClose` is empty).
- Code evidence: `js/components/custom-field-card.js` 229–253; `js/business/custom-fields.js` 392–406; `Popups/FixedMultiFields.aspx.vb` 41–75; `CustomFieldApplicationService.vb` 49–95.
- Confidence: Confirmed
- Suggested KB title: Add preset choices to a custom field

---

## Default locations

Both links use fancybox class `fancybox-lansweeper-map` and href `_locationSelectorToggle` (`Settings.aspx` 330–341). Read-only users never see the section, and the popup redirects them if opened directly (`_locationSelectorToggle.aspx.vb` 24–26).

Clear writes location id `-2` (`_locationSelectorToggle.aspx.vb` 102–104, 120–122). `getReadablePath` returns `"ALL"` on failure, and Settings displays that as `(none)` (`LocationApplicationService.vb` 14–23, `Settings.aspx.vb` 280–288).

The popup buttons are Save (`btn_save_location`) and `CLEAR Selection` (`_locationSelectorToggle.aspx` 75).

### Default check-in location

- Pages: Settings “Default Check-In Location”; popup `?type=defaultcheckin`.
- What it does: Save runs `UPDATE CS_ADMIN.Users SET CheckInLocationDefault`. Clear sets `-2` (`_locationSelectorToggle.aspx.vb` 38–39, 96–111).
- Why: Check-in flows read `UserCredentials.CheckInLocationDefault` (for example `ProductSelector.aspx.vb` 38 and `CheckInCreatedProducts.aspx.vb` 253).
- How to access + visibility: Menu `section_menu_defaultLocations`. Admin and User. Not Read-only.
- Options and defaults: Whatever location the picker posts. Display is the uppercase readable path, or `(none)` when the path is `ALL`.
- Permissions: Popup blocks read-only. No extra admin check. The column is per user (`UserIndex` in the update).
- Validation/failures: Closing the fancybox reloads Settings only when cookie `cookie_refresh_settings` is `TRUE` (`settings.js` 256–270). This catalog did not find that cookie write inside `save_defaultCheckin`. If the popup does not set the cookie, the label stays stale until a manual reload.
- Result: `CheckInLocationDefault` for the current user.
- Edge cases: Header text is “Select Default Check-In Location”.
- Code evidence: `Settings.aspx` 330–333; `Settings.aspx.vb` 276–283; `_locationSelectorToggle.aspx.vb` 34–39, 56–57, 96–111.
- Confidence: Confirmed for the save. Inferred for whether the fancybox always refreshes.
- Suggested KB title: Set your default check-in location

### Default check-out location

- Pages: Settings “Default Check-Out Location”; popup `?type=defaultcheckout`.
- What it does: Same picker. Save updates `CheckOutLocationDefault`. Clear sets `-2` (`_locationSelectorToggle.aspx.vb` 41–43, 114–127).
- Why: Check-out flows read `CheckOutLocationDefault` (`ProductSelector.aspx.vb` 46).
- How to access + visibility: Same section as check-in.
- Options and defaults: Same `(none)` display rule (`Settings.aspx.vb` 285–288).
- Permissions: Same as check-in. Per user.
- Validation/failures: Same refresh-cookie uncertainty.
- Result: `CheckOutLocationDefault` for the current user.
- Edge cases: The save method comment still says “Update Check In Location” (`_locationSelectorToggle.aspx.vb` 115). The SQL column is `CheckOutLocationDefault`.
- Code evidence: `Settings.aspx` 337–341; `Settings.aspx.vb` 278–288; `_locationSelectorToggle.aspx.vb` 41–43, 58–59, 114–127.
- Confidence: Confirmed
- Suggested KB title: Set your default check-out location

---

## API keys

### API access message, create, and delete

- Pages: Settings “API Keys”, `api_key_dynamic_div`.
- What it does: `InitApiKeys` loads keys only when the account id is in `CS_API_v0._betaList` joined to `CS_ADMIN.Accounts` (`ApiKeyApplicationService.vb` 8–45). Otherwise it leaves the static sentence. `loadApiKeys` replaces that div with cards, a name box, and “+ Create New API Key” (`api-key-card.js` 27–137). Create posts `CreateNewKey`. Delete posts `DeleteKey`.
- Why: Keys are `userKey` rows for the current `UserIndex` (`apiKeys.aspx.vb` 31–34, 67).
- How to access + visibility: Menu API & Integrations. The section is visible to Admin, User, and Read-only (`Settings.aspx.vb` 111, 123, 133). The management UI replaces the div only when the hidden JSON is non-empty, which happens only for beta accounts.
- Options and defaults: Non-beta text: “The CyberStockroom API is currently available to select users only. You can request access by emailing us at support@cyberstockroom.com”. Name placeholder “Name your key...”. Names longer than 30 characters display with `...`; the full name is the tooltip (`api-key-card.js` 59–69).
- Permissions: Create and delete call `isAllowed` with all roles allowed (`apiKeys.aspx.vb` 24, 62). The beta list is what hides the form. Delete also requires the key id to be in the caller’s own key list (`apiKeys.aspx.vb` 69–81).
- Validation/failures: Empty name: “Please enter a valid key name”. Create failure: “Error creating API key. Please try again.” Delete confirm: “Are you sure you want to delete the api key … Warning: This will immediately revoke all access using this key and may disrupt any connected systems or integrations.” Delete failure: “Error deleting API key. Please try again.”
- Result: Create returns plaintext once. The page shows `prompt` with “This is the only time this API key will be shown. Please copy and store it safely:” (`api-keys.js` 112–116). Later loads show `truncatedDisplay` and issued date formatted `MMM d, yyyy`. Delete removes the row.
- Edge cases: The beta check compares schema with hyphens normalized to underscores (`ApiKeyApplicationService.vb` 39). A non-beta caller who posted `CreateNewKey` directly would not be stopped by `_isBetaUser`; the UI is the gate. The documentation link under the div is not removed when cards render.
- Code evidence: `Settings.aspx` 361–373; `Settings.aspx.vb` 295–303; `ApiKeyApplicationService.vb` 8–45; `js/components/api-key-card.js` 27–137; `js/business/api-keys.js` 5–141; `webAPI/apiKeys.aspx.vb` 23–90.
- Confidence: Confirmed
- Suggested KB title: Create and delete an API key

### API documentation link

- Pages: Settings, under the API key div.
- What it does: Static link to `https://documenter.getpostman.com/view/1256102/2sB34ZqPYv` in a new tab (`Settings.aspx` 373).
- Why: No in-app docs page. The href is the documentation.
- How to access + visibility: Same section as API keys, including non-beta accounts.
- Options and defaults: Link text “Read API Documentation”.
- Permissions: Whoever can see the API section.
- Validation/failures: None in app code.
- Result: Leaves the app.
- Edge cases: None in this repo.
- Code evidence: `Settings.aspx` 371–373.
- Confidence: Confirmed
- Suggested KB title: Open the CyberStockroom API documentation

---

## Lansweeper

### Lansweeper request block on Settings

- Pages: `section_lansweeper`.
- What it does: Renders the request sentence. `InitLansweeper` is commented out, so connect, progress, synchronize, and disconnect do not render (`Settings.aspx.vb` 53, 307–356). `lansweeper.js` only defines `disconnectConfirmation`, and the button that called it is inside the comment (`Settings.aspx` 399–407, `lansweeper.js` 5–11).
- Why: The live page tells the customer to email support. The service methods `GetLansweeperConnection`, `SyncAllSites`, and `Disconnect` still exist (`LansweeperApplicationService.vb` 6–52) and are not called from `Page_Init`.
- How to access + visibility: Admin only (`Settings.aspx.vb` 112, 126, 138). The menu item is the shared “API & Integrations” icon, which Users and Read-only also see because they see the API section. They do not see this Lansweeper heading.
- Options and defaults: Text: “The Lansweeper Integration is available by request. If you'd like to conenct your Lansweeper account please email us at support@cyberstockroom.com to schedule a call.” Typo “conenct” is in the markup.
- Permissions: Admin section visibility.
- Validation/failures: None. There is no in-page connect button.
- Result: No Lansweeper data changes from this block.
- Edge cases: Commented authorize URL in `InitLansweeper` is `https://app.lansweeper.com/authorize-app/985f4e62409cea0e1c6e7b37fcdb7af3` (`Settings.aspx.vb` 317). It is not active.
- Code evidence: `Settings.aspx` 386–407; `Settings.aspx.vb` 53, 112, 307–356; `LansweeperApplicationService.vb` 6–52; `js/business/lansweeper.js` 5–11.
- Confidence: Confirmed
- Suggested KB title: Request the Lansweeper integration

### Lansweeper site selection (popup, not linked from current Settings)

- Pages: `lansweeperSiteSelector.aspx`.
- What it does: Lists sites as checkboxes. Connect saves checked sites (`uid` = checkbox id, `name` = checkbox text) and redirects to `lansweeperConnectionSuccess` (`lansweeperSiteSelector.aspx.vb` 47–74). Zero checked sites redirects to `/Settings`.
- Why: Those sites are what a later sync iterates (`LansweeperApplicationService.SyncAllSites` 28–43).
- How to access + visibility: No live Settings link. Admin would have to open the URL.
- Options and defaults: One checkbox per site the page succeeded in loading. Label under the button: “Only sites that contain assets will be synchronized. Some demo sites may not be permitted.” (`lansweeperSiteSelector.aspx` 68).
- Permissions: Uses `UserPageNoMenu.master`. This catalog did not find an extra role check in the popup code-behind.
- Validation/failures: Load exception redirects to `lansweeperConnectionFailure?source=siteSelector` (`lansweeperSiteSelector.aspx.vb` 40–42).
- Result: Connection `sites` updated and committed. Display settings get a default column-order string from `getDefaultColumnOrderCookieString(sites.Count)`.
- Edge cases: Not part of the current Settings click path.
- Code evidence: `pages/settings/popups/lansweeperSiteSelector.aspx` 64–68; `pages/settings/popups/lansweeperSiteSelector.aspx.vb` 47–74.
- Confidence: Confirmed for the popup. Confirmed it is not mounted by current Settings.
- Suggested KB title: Choose which Lansweeper sites to sync

### Lansweeper field match (popup, not linked)

- Pages: `lansweeperFieldToggle.aspx`.
- What it does: Builds a toggle list whose options are this account’s custom fields (`key` = `CF_Index`, `name` = `fieldName`) (`lansweeperFieldToggle.aspx.vb` 26–55). A selection sets `cookie_refresh_settings` to `TRUE` and closes the fancybox.
- Why: The control class `lansweeperFieldToggle` performs the match. That class body was not in the files read for this catalog.
- How to access + visibility: Query `id` and `name`. Not linked from live Settings.
- Options and defaults: One option per custom field. No Buy Price or Sell Price entries in `_getOptions`.
- Permissions: Logged-in master page. No extra role check in this file.
- Validation/failures: Not visible in this file.
- Result: Cookie refresh plus whatever `lansweeperFieldToggle` saves. Uncertain beyond the custom-field option list.
- Edge cases: Header is “Select a Field to Match: '{name}'”.
- Code evidence: `pages/settings/popups/lansweeperFieldToggle.aspx.vb` 18–55.
- Confidence: Confirmed for the option source. Uncertain for the stored mapping, because `lansweeperFieldToggle` was not opened.
- Suggested KB title: Match a Lansweeper field to a custom field

### Lansweeper location match

- Pages: `_locationSelectorToggle.aspx?type=lansweeper` (and `name` query). Same popup as default locations.
- What it does: Header “Select a Location to Match: '{name}'”. Save calls `save_lansweeper`, which replaces a tag on the location (`_locationSelectorToggle.aspx.vb` 35–37, 54–55, 80–93). Clear calls `save_lansweeper(True)`.
- Why: Ties a Lansweeper category to a map location.
- How to access + visibility: Not linked from the live Lansweeper section. Read-only is redirected.
- Options and defaults: Pick a location or CLEAR Selection.
- Permissions: Not read-only.
- Validation/failures: Not enumerated in `save_lansweeper` beyond the repository call.
- Result: Location tag replaced, unit of work committed.
- Edge cases: Fancybox class on Settings is shared with default locations, but the live hrefs are only `defaultcheckin` and `defaultcheckout`.
- Code evidence: `_locationSelectorToggle.aspx.vb` 15–19, 34–37, 54–55, 68–70, 80–93.
- Confidence: Confirmed
- Suggested KB title: Match a Lansweeper category to a location

### Lansweeper link-and-sync and progress popups

- Pages: `lansweeperLinkAndSync.aspx`, `lansweeperConnectionSuccess.aspx`, `lansweeperConnectionFailure.aspx`.
- What it does: Link-and-sync, if `progress` is 0, sets status “Preparing to Synchronize...” at 1%, calls `accountLinker.link` and `AccountSynchronizer.synchronize`, then writes `ColumnOrder` (`lansweeperLinkAndSync.aspx.vb` 30–56). Success popup shows `progress` and `status` on a timer and redirects to `/Map` when progress is 100 (`lansweeperConnectionSuccess.aspx.vb` 26–38). Failure page text: “There was a problem connecting your Lansweeper Account.”
- Why: This is the sync pipeline. `SyncAllSites` on the application service instead inserts `CS_ADMIN.CS_WORKER` rows with task `lansweeper` when none exist for that site uid (`LansweeperApplicationService.vb` 22–44). The commented Settings button called `SyncAllSites`. The link-and-sync popup calls the SDK synchronizer directly.
- How to access + visibility: Not linked from current Settings. Site selector redirects to the success popup.
- Options and defaults: No customer toggles on these three pages. `CALLBACK_TYPE` is `callBackType.test` (`lansweeperLinkAndSync.aspx.vb` 15).
- Permissions: Login via master or `GetMasterAccountObject`. No role check in these files.
- Validation/failures: Existing `progress <> 0` skips a second synchronize (`lansweeperLinkAndSync.aspx.vb` 34–42).
- Result: Connection status/progress, and the user’s `ColumnOrder`.
- Edge cases: `lansweeperLinkAndSync.aspx` and `lansweeperConnectionSuccess.aspx.vb` both declare `Inherits pages_settings_popups_lansweeperConnectionSuccess`. That is a duplicate class name in source. Which file the site actually compiles was not verified.
- Code evidence: `pages/settings/popups/lansweeperLinkAndSync.aspx.vb` 15–56; `pages/settings/popups/lansweeperConnectionSuccess.aspx.vb` 17–38; `pages/settings/popups/lansweeperConnectionFailure.aspx` 21–30; `LansweeperApplicationService.vb` 22–52.
- Confidence: Confirmed for the methods that were read. Uncertain which duplicate class the compiler binds.
- Suggested KB title: What happens after Lansweeper connects

---

## Display settings

These are per user unless noted. Toggles call `handleToggleSetting` or a dedicated handler (`toggle.js` 9–29). A failed toggle reverts after 1.5s (`general-settings.js` 40–50).

Section `section_display_settings` is on for Admin, User, and Read-only. Share Map Layout’s row is admin-only.

### Share Map Layout

- Pages: Settings display settings, first row.
- What it does: `SaveShareMapLayout` writes coordinate marker `-16,CS_MAP_SHAREABLE_ON` (`webAPI/settings.aspx.vb` 173–183, `Gridster_Utilities.vb` 76–78, 747–755). `GetSharedMaps` returns other users on the account whose coordinates contain that marker (`settings.aspx.vb` 194–221).
- Why: Another user can request `GetSharedMapLayoutParts` and copy the layout. The helper text on the page says teammates can sync to the layout and cannot change it (`Settings.aspx` 444–446). `GetShareableMapCoordinatesForAccountUser` is what the parts method uses (`settings.aspx.vb` 248–251).
- How to access + visibility: `row_share_map_layout` admin only (`Settings.aspx.vb` 114, 368–370).
- Options and defaults: Off when the marker is absent (`GetShareMapLayoutEnabledFromRaw` returns false for blank).
- Permissions: API requires admin twice: `isAllowed(..., True, False, False, False)` and `TypeOfUser = ADMIN` (`settings.aspx.vb` 174–177).
- Validation/failures: Failure reverts the toggle. No alert string.
- Result: The current admin’s map coordinates gain or lose the share marker. Invited users receive a copy of the inviter’s coordinates with that marker stripped (`invitations.aspx.vb` 58–59).
- Edge cases: Users can call `GetSharedMaps` (`isAllowed` defaults). They cannot turn the flag on.
- Code evidence: `Settings.aspx` 435–447; `Settings.aspx.vb` 368–373; `js/business/general-settings.js` 249–275; `webAPI/settings.aspx.vb` 169–255; `Gridster_Utilities.vb` 76–78, 747–755.
- Confidence: Confirmed
- Suggested KB title: Share your map layout with the team

### Product Images

- Pages: Settings toggle “Product Images”.
- What it does: `ShowProductImages` sets `set_showProductImages` (`settings.aspx.vb` 27–36).
- Why: `Products.aspx.vb` `StylingRefresh` calls `GridviewImagesAdd` only when `SHOW_PRORDUCT_IMAGES` is true (`Products.aspx.vb` 275–277). The same flag is checked on `Products_read_only.aspx.vb` 234.
- How to access + visibility: Options / display settings. Admin, User, Read-only.
- Options and defaults: Checked state loaded from `MO.UserCredentials.SHOW_PRORDUCT_IMAGES` (`Settings.aspx.vb` 364). The database default for a brand-new user was not read from a schema script in this pass.
- Permissions: Any authenticated role.
- Validation/failures: HTTP failure reverts the checkbox.
- Result: Per-user `SHOW_PRODUCT_IMAGES`.
- Edge cases: The property name in code is spelled `SHOW_PRORDUCT_IMAGES`.
- Code evidence: `Settings.aspx` 454–459; `Settings.aspx.vb` 363–366; `js/business/general-settings.js` 17–18; `webAPI/settings.aspx.vb` 27–36; `Products.aspx.vb` 275–277.
- Confidence: Confirmed
- Suggested KB title: Show product images in the product list

### Zero Quantity Products

- Pages: Settings toggle “Zero Quantity Products”.
- What it does: `ShowZeroQuantityProducts` sets `set_showZeroQuantity` (`settings.aspx.vb` 47–56).
- Why: On the products grid, when the flag is false, rows with quantity 0 are skipped (`Products.aspx.vb` 1846–1850). Same check on the read-only products page at line 1468.
- How to access + visibility: Display settings. All three roles.
- Options and defaults: Loaded from `SHOW_ZERO_QUANTITY` (`Settings.aspx.vb` 365).
- Permissions: Any authenticated role.
- Validation/failures: Toggle reverts on HTTP failure.
- Result: Per-user flag.
- Edge cases: The threshold note separately says locations with 0 quantity stay white on the map. That sentence is about map color, not this product-list toggle (`Settings.aspx` 564–566).
- Code evidence: `Settings.aspx` 471–476; `Settings.aspx.vb` 365; `webAPI/settings.aspx.vb` 47–56; `Products.aspx.vb` 1846–1850.
- Confidence: Confirmed
- Suggested KB title: Include products with zero quantity

### Expirations

- Pages: Settings toggle “Expirations”.
- What it does: `ShowExpirations` sets `set_showExpirations` (`settings.aspx.vb` 67–76). The master page sets `hidden_expiration_on` to 1 when the flag is true (`UserPage.master.vb` 66–68). The map sets `hidden_POPUP_DETAIL_EXPIRATION_AVAILABLE` from the same flag (`Map_CONTROL_2017.ascx.vb` 821, 837).
- Why: Turns expiration display on for that user. Turning it off also hides the Expiring Soon block in the settings UI (`general-settings.js` 448–454).
- How to access + visibility: Display settings. All three roles.
- Options and defaults: Loaded from `SHOW_EXPIRATIONS` (`Settings.aspx.vb` 366). New invites copy the inviter’s value (`invitations.aspx.vb` 55, 76).
- Permissions: Any authenticated role.
- Validation/failures: Toggle reverts on failure. The Expiring Soon server method rejects enable when this flag is false.
- Result: Per-user `SHOW_EXPIRATIONS`.
- Edge cases: Hiding the Expiring Soon block does not by itself write the expiring-soon window to 0. The stored window remains until that toggle is saved.
- Code evidence: `Settings.aspx` 489–494; `Settings.aspx.vb` 366; `webAPI/settings.aspx.vb` 67–76; `UserPage.master.vb` 66–68; `Map_CONTROL_2017.ascx.vb` 806–837; `js/business/general-settings.js` 23–27, 448–454.
- Confidence: Confirmed
- Suggested KB title: Turn expiration dates on or off

### Expiring Soon

- Pages: Nested under Expirations. Number, unit, save.
- What it does: `SaveExpiringSoonWindow` stores a day count on coordinate token `-18` (`settings.aspx.vb` 144–162). The client converts weeks × 7, months × 30, years × 365 (`general-settings.js` 408–416).
- Why: `GetExpiringSoonWindowFromRaw` is written to `hidden_EXPIRING_SOON_DAYS` for the map (`Map_CONTROL_2017.ascx.vb` 845). Helper text: “Highlight products expiring within this period”.
- How to access + visibility: Display settings. The block is hidden while the Expirations toggle is off. Enabling Expiring Soon while Expirations is off alerts “Enable Expirations before using Expiring Soon.” and does not save (`general-settings.js` 516–519). The server throws the same sentence (`settings.aspx.vb` 150–151).
- Options and defaults: Units `days`, `weeks`, `months`, `years`. Markup default value `60` and unit days, inputs disabled (`Settings.aspx` 509–514). `DefaultExpiringSoonWindowDays` is 60 (`Gridster_Utilities.vb` 74). Stored `-1` (`ExpiringSoonWindowAbsentMarker`) means the settings toggle is treated as on and the box shows 60 (`Settings.aspx.vb` 409, `general-settings.js` 494–503). Effective map window when the token is absent is also 60 (`Gridster_Utilities.vb` 702–706). Stored `0` means disabled. Turning the toggle on with an empty or non-positive value saves 60 (`general-settings.js` 527–530).
- Permissions: Any authenticated role.
- Validation/failures: “Expiring soon window must be a valid duration greater than 0.” Save failure: “Error saving expiring soon window. Please try again.”
- Result: Per-user day count. Display converts exact multiples back to years, then months, then weeks (`general-settings.js` 419–427). 14 days displays as 2 weeks. 30 days displays as 1 month.
- Edge cases: A month is 30 days and a year is 365 days in this converter, not calendar months. `min="1"` is on the number input.
- Code evidence: `Settings.aspx` 496–517; `Settings.aspx.vb` 406–418; `js/business/general-settings.js` 406–592; `webAPI/settings.aspx.vb` 144–162; `Gridster_Utilities.vb` 74–75, 688–706; `Map_CONTROL_2017.ascx.vb` 845.
- Confidence: Confirmed
- Suggested KB title: Set the expiring-soon highlight window

### Quantity Threshold

- Pages: Settings “Quantity Threshold” plus a number and save.
- What it does: `ShowGeneralThreshold` stores `value` when the toggle is on and the value is greater than 0, otherwise stores 0 (`settings.aspx.vb` 87–100).
- Why: The map builder receives `_generalThreshold` (`Map_CONTROL_2017.ascx.vb` 141–150). The settings copy says “Highlight locations with quantity at or below:” and “Locations with 0 quantity will appear in white on the map.”
- How to access + visibility: Display settings. All three roles. Details stay hidden until the toggle is on.
- Options and defaults: If the stored threshold is greater than 0, the box is enabled and shows that number. Otherwise the toggle is off and the box shows `1` disabled (`Settings.aspx.vb` 376–388). Turning the toggle on saves `1` immediately (`general-settings.js` 66–73).
- Permissions: Any authenticated role.
- Validation/failures: Save is ignored in `thresholdConfirmation` unless the value is numeric and greater than 0. Alert: “The threshold must be a valid number bigger than 0.” HTTP failure: “Error saving threshold value. Please try again.”
- Result: Per-user `_generalThreshold`. Off is 0. Max Highlight cannot be enabled unless this is on.
- Edge cases: The client does not require an upper bound.
- Code evidence: `Settings.aspx` 547–566; `Settings.aspx.vb` 376–388; `js/business/general-settings.js` 54–142, 239–246; `webAPI/settings.aspx.vb` 87–100; `Map_CONTROL_2017.ascx.vb` 141–150.
- Confidence: Confirmed
- Suggested KB title: Highlight low quantities on the map

### Max Highlight

- Pages: Inside the threshold details, “Max Highlight”.
- What it does: `SaveMaxHighlight` stores a positive integer above the threshold, or 0 when off (`settings.aspx.vb` 111–132). The map reads `GetMaxHighlightFromRaw` (`Map_CONTROL_2017.ascx.vb` 148).
- Why: Settings copy: “Highlight locations with quantity at or above:”.
- How to access + visibility: Only after Quantity Threshold is on, because `max_highlight_details` is inside `threshold_details`. All three roles.
- Options and defaults: When no stored max exists, the toggle is off and the box shows `10` disabled (`Settings.aspx.vb` 399–402). Markup default is also `10` (`Settings.aspx` 582). Turning it on uses the box, or 10 if the box does not parse (`general-settings.js` 296). If the box is empty or not greater than 0 after a successful save call is skipped, the UI then shows threshold + 1 (`general-settings.js` 305–310).
- Permissions: Any authenticated role.
- Validation/failures: Alerts: “Enable Quantity Threshold before using Max Highlight.”; “Enable Quantity Threshold before setting Max Highlight.”; “Max highlight must be a valid number greater than 0.”; “Max highlight must be greater than the quantity threshold.” Server throws the threshold-required and must-be-greater sentences (`settings.aspx.vb` 122–126). Save failure alert: “Error saving max highlight. Ensure it is greater than the quantity threshold.”
- Result: Per-user coordinate metadata. 0 removes the highlight.
- Edge cases: If validation fails after the toggle was disabled, `handleMaxHighlightToggle` returns without clearing `disabled` or `toggle-saving` (`general-settings.js` 291–300). The control can stay disabled until reload.
- Code evidence: `Settings.aspx` 568–585; `Settings.aspx.vb` 390–403; `js/business/general-settings.js` 278–399; `webAPI/settings.aspx.vb` 111–132; `Map_CONTROL_2017.ascx.vb` 148.
- Confidence: Confirmed
- Suggested KB title: Highlight high quantities on the map

### Kitting toggle (not shown)

- Pages: Settings markup `toggle_show_kitting`.
- What it does: The row is `display: none` (`Settings.aspx` 526). `InitDisplaySettings` does not set this checkbox. No click handler in `toggle.js`. No postback handler in `Settings.aspx.vb`.
- Why: `SHOW_KITTING` is still loaded onto the user and copied to `hidden_kitting_on` when it equals 1 (`Account.vb` 879–885, `UserPage.master.vb` 70–72). This Settings control does not write it.
- How to access + visibility: Not visible.
- Options and defaults: Not initialized by the settings page.
- Permissions: Not reachable from the visible UI.
- Validation/failures: None.
- Result: No change from this control.
- Edge cases: Do not document Kitting as a Settings option.
- Code evidence: `Settings.aspx` 526–536; `Account.vb` 879–885; `UserPage.master.vb` 70–72.
- Confidence: Confirmed
- Suggested KB title: Do not publish. The control is hidden and unwired.

---

## Account settings

Section `section_account_settings` is admin-only (`Settings.aspx.vb` 115, 127, 139). Time zone and currency APIs pass `allowUsers`, `allowMobile`, and `allowReadOnly` as false (`settings.aspx.vb` 312, 332).

Both values are account-wide (`accountModifier` on `thisAccount`), not per user. Fallback when the account row cannot be read: currency `$`, time zone `-5` (`Account.vb` 301–302 and 994–995).

### Time zone

- Pages: Settings account settings, `drp_down_timezone`.
- What it does: Change calls `handleTimezoneSave` → `SetTimeZone` → `set_timezone` (`general-settings.js` 145–165, `settings.aspx.vb` 311–320).
- Why: Activity queries pass `AccountSettings.TimeZone` (`UserPage.master.vb` 164).
- How to access + visibility: Admin account settings. Saves on change, no separate button.
- Options and defaults: Integer offsets. Labels and values from `Settings.aspx` 631–657:

  - `-12` (GMT-12:00) International Date Line West
  - `-11` (GMT-11:00) Midway Island, Samoa
  - `-10` (GMT-10:00) Hawaii
  - `-9` (GMT-09:00) Alaska
  - `-8` (GMT-08:00) Pacific Time (US & Canada)
  - `-7` (GMT-07:00) Mountain Time (US & Canada)
  - `-6` (GMT-06:00) Central Time (US & Canada)
  - `-5` (GMT-05:00) Eastern Time (US & Canada)
  - `-4` (GMT-04:00) Atlantic Time (Canada)
  - `-3` (GMT-03:00) Greenland
  - `-2` (GMT-02:00) Mid-Atlantic
  - `-1` (GMT-01:00) Cape Verde Is.
  - `0` (GMT+00:00) Greenwich Mean Time : Dublin, Edinburgh, Lisbon, London
  - `1` (GMT+01:00) Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna
  - `2` (GMT+02:00) Cairo
  - `3` (GMT+03:00) Moscow, St. Petersburg, Volgograd
  - `4` (GMT+04:00) Abu Dhabi, Muscat
  - `5` (GMT+05:00) Yekaterinburg
  - `5` (GMT+05:00) Islamabad, Karachi, Tashkent
  - `6` (GMT+06:00) Astana, Dhaka
  - `7` (GMT+07:00) Bangkok, Hanoi, Jakarta
  - `8` (GMT+08:00) Beijing, Chongqing, Hong Kong, Urumqi
  - `9` (GMT+09:00) Osaka, Sapporo, Tokyo
  - `10` (GMT+10:00) Canberra, Melbourne, Sydney
  - `11` (GMT+11:00) Magadan, Solomon Is., New Caledonia
  - `12` (GMT+12:00) Auckland, Wellington
  - `13` (GMT+13:00) Nuku'alofa

  Selected value is `MO.AccountSettings.TimeZone` (`Settings.aspx.vb` 423). There is no half-hour offset.
- Permissions: Admin.
- Validation/failures: Alert “Error saving timezone. Please try again.” No range check beyond the dropdown. Two options share value `5`, so a saved `5` cannot tell Yekaterinburg from Islamabad, Karachi, Tashkent.
- Result: `Accounts.TimeZone` integer. “Saved ✓” for about 2 seconds.
- Edge cases: Duplicate value `5`.
- Code evidence: `Settings.aspx` 620–658; `Settings.aspx.vb` 421–424; `js/business/general-settings.js` 145–193; `js/components/toggle.js` 27–28; `webAPI/settings.aspx.vb` 311–320; `Account.vb` 328–333, 994–995.
- Confidence: Confirmed
- Suggested KB title: Set the account time zone

### Currency symbol

- Pages: Settings “Currency Symbol”, anchor `currency`.
- What it does: Save or Enter calls `SetCurrencySymbol` → `set_currencySymbol` (`general-settings.js` 196–215, `settings.aspx.vb` 331–340).
- Why: Stored on the account as `Currency` (`Account.vb` 318–323). The subscription card’s own currency comes from the subscription record, not from this box (`subscription.js` 171–178).
- How to access + visibility: Admin account settings.
- Options and defaults: Markup text is `$` (`Settings.aspx` 674). `InitGeneralAccountSettings` replaces it with `MO.AccountSettings.Currency` (`Settings.aspx.vb` 422). Fallback `$`.
- Permissions: Admin.
- Validation/failures: Trimmed empty: “Please enter a currency symbol”. HTTP failure: “Error saving currency symbol. Please try again.” No maximum length in the handler.
- Result: Account currency string. Button shows “Saved!”.
- Edge cases: Any non-empty string is accepted, including multi-character text. This is not a currency-code dropdown.
- Code evidence: `Settings.aspx` 664–676; `Settings.aspx.vb` 421–423; `js/business/general-settings.js` 196–236; `webAPI/settings.aspx.vb` 331–340; `Account.vb` 301–302, 318–323.
- Confidence: Confirmed
- Suggested KB title: Set the currency symbol

---

## Subscription and billing

`SubscriptionApplicationService.getSubscrtiption` maps the stored subscription. It does not contain a price table.

Plan type strings (`SubscriptionApplicationService.vb` 22–31):

- `planType.STANDARD` → `Standard` (no badge in the UI)
- `planType.CUSTOM` → `Custom Plan` (badge “Custom”, tooltip “This plan was created specifically for your team”)
- `planType.ENTERPRISE` → `Enterprise Plan` (badge “Enterprise”, tooltip “This plan that includes more than the standard turnkey solution”)
- `planType.LEGACY` → `Legacy Plan` (badge “Legacy”, tooltip “This plan is no longer available, but will continue to be active for your team”)

Payment method strings (`SubscriptionApplicationService.vb` 33–46):

- Cheque → `Bank Cheque`
- Coupa → `Coupa (Payment Platform)`
- Direct bank transfer → `Direct Bank Transfer`
- PayPal card, PayPal invoice, or Stripe invoice → `Online Invoice`
- Stripe card → `Credit Card (Stripe)`
- Anything else → `(None)`

`IsAnnual` true displays “Annually”. False displays “Monthly” (`subscription.js` 182). No other frequency label exists.

Stripe card display is brand plus `xxxx-xxxx-xxxx-` and last 4, or `xxxx-xxxx-xxxx-xxxx` if Stripe lookup throws (`SubscriptionApplicationService.vb` 56–68).

The selectable checkout images on `UpdateAccount.aspx` are monthly and annual. `test_ON` is `false`, so clicks use live price ids `price_1O6zRX4D3SV7Y45Utyewx37h` (index 1) and `price_1O6zS34D3SV7Y45UCZ8p3YaG` (index 2) (`UpdateAccount.aspx` 101–139, 435–439). The enterprise image has no `onclick` (`UpdateAccount.aspx` 429). Commented code that disabled TEAM and BUSINESS plans is not active (`UpdateAccount.aspx.vb` 236–255). This catalog did not find a live user-count or location-count cap in that page.

### Subscription summary

- Pages: Settings `div_subscription_container`.
- What it does: `InitSubscription` serializes `getSubscrtiption`. On any exception it stores `{}` and still calls `loadSubscription` (`Settings.aspx.vb` 429–438). The script paints the card (`subscription.js` 64–395).
- Why: Shows the stored plan, amount, frequency, payment method, and Stripe-only actions.
- How to access + visibility: Menu Subscription and `section_subscription` are admin-only.
- Options and defaults: Rows that render when present: plan name (fallback heading “Subscription”), Billing Amount, Billing Frequency, Payment Method, Payment Details (non-Stripe notes only), Contact, Card, Activated. Amount uses `$` plus the code for `USD` or `CAD`, and the code then the amount for other currencies (`subscription.js` 171–178). Missing amount shows the row as omitted, not “N/A”, because the row is skipped when `Amount` is falsy. A present amount that fails `parseFloat` can still render `NaN`.
- Permissions: Viewing is admin because the section is hidden. The load itself has no extra role check; it uses the page’s account id.
- Validation/failures: JSON errors are `console.error` only (`subscription.js` 393–395).
- Result: Display. No write.
- Edge cases: Empty object or missing `PlanName` shows “No Active Subscription”, the sentence “You don't have an active subscription. Subscribe to a plan to get started.”, and a “Subscribe to a Plan” link to `UpdateAccount?Update=Plan`.
- Code evidence: `Settings.aspx` 694–703; `Settings.aspx.vb` 429–438; `js/business/subscription.js` 64–395; `SubscriptionApplicationService.vb` 7–68.
- Confidence: Confirmed
- Suggested KB title: Read your subscription on the Settings page

### Update plan, change card, cancel, billing history buttons

- Pages: Rendered only when `PaymentMethod` contains the substring `Stripe` (`subscription.js` 142, 325–371).
- What it does:
  - “Update Plan” opens `UpdateAccount?Update=Plan` in a fancybox.
  - “Change Card” opens `UpdateAccount?Update=Payment`.
  - “Cancel Subscription” confirms, then `cancel_subscription` → `CancelSubscription`.
  - “Billing History” opens `BillingHistory` in a fancybox.
- Why: Stripe-card subscriptions are the ones this UI can change. Other payment types get the footnote “Please contact admin@cyberstockroom.com to change your subscription or payment method” (`subscription.js` 386–387). Stripe footnote: “For any billing questions please contact admin@cyberstockroom.com”.
- How to access + visibility: Admin subscription section, and only for payment methods whose display string contains “Stripe”. That includes “Credit Card (Stripe)”. “Online Invoice” does not contain “Stripe”, so PayPal and Stripe-invoice subscriptions do not get these buttons.
- Options and defaults: Confirm title buttons “Cancel Subscription” and “Keep Subscription”. Message: “Are you sure you want to cancel your subscription?”
- Permissions: Cancel API is admin-only (`subscription.aspx.vb` 20). `BillingHistory.aspx.vb` 15–17 redirects non-admins. `UpdateAccount.aspx.vb` 20–22 redirects read-only users only. A non-admin who is not read-only is not redirected by that check.
- Validation/failures: Cancel does not show an error alert in `CancelSubscription` in `subscription.js`. It reloads the page after the call (`subscription.js` 50–61). If the HTTP call throws, the reload still is not wrapped in try/catch, so a failure skips the reload and leaves the confirm closed.
- Result of cancel: `Accounts.ConfirmedPayment` set to `0`, the `CS_ADMIN.StripeAccounts` row for the account is deleted, and `stripeRegistrar.deleteSubscription` is called (`subscription.aspx.vb` 28–56). Because confirmed payment is 0, the 14-day trial rule applies again. An account older than 14 days then has `TrialExpired` true (`Account.vb` 893–900) and `BillingAccessGate` sends them to Settings.
- Result of plan update: If a card is already on file and `stripe_payment_skip` is `1`, `UpdatePlan` calls `updateSubscription` and upserts `StripePlan` (`UpdateAccount.aspx` 176–186, `UpdateAccount.aspx.vb` 278–299). If payment is not set, Stripe checkout runs and `ProcessStripe` either updates the subscription or creates a customer (`UpdateAccount.aspx.vb` 147–223). Redirects: `_cvr/SuccessSignup` or `SuccessSignup` depending on the branch, or back to `UpdateAccount` on the failure path at lines 187 and 223.
- Result of card update: `?Update=Payment` runs `updatePayment()` on first load (`UpdateAccount.aspx.vb` 31–33), then `updatePaymentMethod` (`UpdateAccount.aspx.vb` 104–127).
- Edge cases: `settings.js` clears cookie `stripe_plan_name` on Settings load (`settings.js` 6). Fancybox close reloads Settings when `cookie_refresh_settings` is `TRUE`. Non-Stripe subscriptions have no self-serve cancel.
- Code evidence: `js/business/subscription.js` 50–62, 141–142, 320–388; `webAPI/subscription.aspx.vb` 19–56; `UpdateAccount.aspx` 101–186, 414–449; `UpdateAccount.aspx.vb` 15–33, 104–223, 278–299; `BillingHistory.aspx.vb` 12–17; `Account.vb` 889–901.
- Confidence: Confirmed
- Suggested KB title: Change, cancel, or review a Stripe subscription

### Billing history table

- Pages: `BillingHistory.aspx`.
- What it does: Lists Stripe charges for `MO.StripeAccount.StripeCustomerID`. Columns Date (`MMM dd, yyyy`), Amount (charge amount / 100, currency format), Subscription (invoice plan name plus charge description, cut off at `@` when present), Status Successful or Failed (`BillingHistory.aspx.vb` 111–157, 207–216). Next payment uses the first subscription’s `CurrentPeriodEnd` and plan amount / 100 (`BillingHistory.aspx.vb` 44–49). The invoice table is built and then not added; the charges table is what is shown (line 91 is commented, line 92 adds charges).
- Why: Receipt list for the Stripe customer.
- How to access + visibility: Billing History button, admin, Stripe payment method. Direct URL requires admin.
- Options and defaults: None.
- Permissions: Admin.
- Validation/failures: Any exception replaces the table with “No billing history to show...” and hides next payment (`BillingHistory.aspx.vb` 94–98).
- Result: Display only.
- Edge cases: `GetInvoiceRow` defaults the plan label to “Custom Plan” when the line item name cannot be read (`BillingHistory.aspx.vb` 167–173). That row is not the one added to the page.
- Code evidence: `BillingHistory.aspx` 71–78; `BillingHistory.aspx.vb` 25–98, 111–157, 207–216.
- Confidence: Confirmed
- Suggested KB title: Read billing history

### Trial expiry and delinquent payment

- Pages: `BillingAccessGate`; Settings banners `#div-expired`, `#div-upgrade`, `#div-payment`; `UpdateAlert.aspx`.
- What it does: The gate redirects to `/Settings` for an expired unpaid trial or a delinquent Stripe customer, unless the matching suppress flag is set (`BillingAccessGate.vb` 15–21). Trial length is 14 days from `DateCreated` while `ConfirmedPayment` is 0 (`Account.vb` 889–901).
- Why: Keeps the person on Settings until billing is updated. The gate does not open a plan picker by itself.
- How to access + visibility: Any non-settings page, all roles that use `UserPage.master`.
- Options and defaults: Banners exist with text “Your free trial has expired. Please select a plan to continue..”, “You have exceeded the capacity of your current plan. Please upgrade to continue.”, and “Your payment method needs to be updated!” (`Settings.aspx` 100–108). CSS sets all three to `display: none` (`css/pages/settings.css` 113–118). `ToggleExpiry`, `ToggleUpgrade`, and `TogglePayment` are defined in `subscription.js` 5–38 and are not called anywhere else in the repo. Nothing in `Settings.aspx.vb` shows the banners or clicks `alert_plan_force` / `alert_payment_force`.
- Permissions: Gate uses account flags, not role. Suppress flags are account columns `SuppressUpgradeAlert` and `SuppressPaymentAlert` (`Account.vb` 963–982). This catalog did not find a Settings control that edits those flags.
- Validation/failures: `UpdateAlert.aspx` 43–60: if the query is `Payment`, it shows the payment banner and loads `UpdateAccount.aspx?Update=Payment`. The `else if` uses assignment `UpdateType = "CC_Error"`, which is always truthy, so every other value, including `Plan`, shows “There was a problem with the information you entered. Please try again.” and still loads the payment iframe. The final else that would show the trial sentence is unreachable. Cookie `force_update` is written and is not read anywhere else in this repo.
- Result: Redirect to Settings. The expired-trial and upgrade banners do not appear from the current Settings load path. “Exceeded the capacity” has no writer in the files read for this catalog. Do not describe a capacity limit.
- Edge cases: People sent to Settings by the gate can still use Settings. They are not automatically shown the plan fancybox.
- Code evidence: `BillingAccessGate.vb` 10–28; `Account.vb` 889–901, 963–982; `Settings.aspx` 99–109; `css/pages/settings.css` 113–118; `js/business/subscription.js` 5–38; `UpdateAlert.aspx` 42–60.
- Confidence: Confirmed
- Suggested KB title: What happens when a trial ends

---

## Sign-in, signup, and OAuth

### Log in with email

- Pages: `Login.aspx`.
- What it does: `AuthenticatedUser`. On success, writes `csToken` from `signIn_email` and calls `Account.LogIn` (`Login.aspx.vb` 26–38). If a session already exists, `Page_Init` redirects to `Map` (`Login.aspx.vb` 79).
- Why: Creates the session the rest of the app requires (`UserPage.master.vb` 75–77).
- How to access + visibility: Public. Title “Log in to CyberStockroom”.
- Options and defaults: Email placeholder `me@email.com`. Password placeholder `***********`.
- Permissions: Public.
- Validation/failures: Label, hidden until failure: “The email or password is not correct...” (`Login.aspx` 186, `Login.aspx.vb` 40–45).
- Result: Session and csToken cookies.
- Edge cases: HTTPS is forced (`Login.aspx.vb` 54).
- Code evidence: `Login.aspx` 169–186; `Login.aspx.vb` 14–50, 53–79.
- Confidence: Confirmed
- Suggested KB title: Log in to CyberStockroom

### Log in with Google

- Pages: `Login.aspx` `g-signin2`.
- What it does: `onSignIn` stores the ID token and access token and clicks hidden `btnGoogleLogin` (`Login.aspx` 216–242). The server path continues in `Login.aspx.vb` after the portion read here (`VerfiyGoogleToken` starts at line 289).
- Why: Google sign-in instead of the password box.
- How to access + visibility: The Google button is on the public login form. Invitation flow hides email, password, login, and forgot-password when `Accounts.googleOnly` is 1 (`Login.aspx.vb` 106–119). The Google button is not in that hide list.
- Options and defaults: One Google button.
- Permissions: Public, except the token must validate.
- Validation/failures: `VerfiyGoogleToken` returning false exits the invitation Google path without a message (`Login.aspx.vb` 189–191). The ordinary Google login failure text was not fully traced past line 289.
- Result: `signIn_google` and `Account.LogIn_Google` on the invitation path (`Login.aspx.vb` 209–213).
- Edge cases: Client id meta tag matches the audience check used on Settings.
- Code evidence: `Login.aspx` 206–242; `Login.aspx.vb` 185–213, 289.
- Confidence: Confirmed for the invitation Google path. Inferred that the main Google button posts the same hidden button.
- Suggested KB title: Log in with Google

### Forgot password and reset link

- Pages: Login “Forgot Password?” then `Login.aspx?PasswordReset={guid}`.
- What it does: Looks up the email. Writes `PasswordResetID` and emails `https://www.cyberstockroom.com/Login?PasswordReset=` plus the GUID from `support@cyberstockroom.com` (`Login.aspx.vb` 242–273). The reset page sets the title “Reset your password” and “Pick a New Password”, locks the email box, and on submit stores a new salted hash with no length check (`Login.aspx.vb` 122–138, 216–237).
- Why: Replaces the password without the old password.
- How to access + visibility: Login page. The reset email field starts in a hidden div (`Login.aspx` 196).
- Options and defaults: Reset email placeholder “Your Email”.
- Permissions: Public.
- Validation/failures: Unknown email runs `Intercom('That Email is not in our records...')` (`Login.aspx.vb` 276–278). A known email runs `Intercom('An Email has been sent')` (`Login.aspx.vb` 275). Empty new password is not rejected in `PasswordResetProcess`.
- Result: New password hash, then `Account.LogIn`.
- Edge cases: The reset link host is hard-coded to `www.cyberstockroom.com`, unlike invitations, which use the current request host (`invitations.aspx.vb` 98–99).
- Code evidence: `Login.aspx` 193–198; `Login.aspx.vb` 122–138, 216–278.
- Confidence: Confirmed
- Suggested KB title: Reset a forgotten password

### Accept an invitation

- Pages: `Login.aspx?Invitation={guid}`.
- What it does: Loads account and email from `InvitationID`. Title becomes “Accept your Invitation” and the password label “Create your password” (`Login.aspx.vb` 86–104). Submit requires a non-blank password, stores the salted hash, sends `Account.SendNewUserNotification`, and logs in (`Login.aspx.vb` 142–182). Google acceptance writes email, Google id, name, and Google photo URL (`Login.aspx.vb` 185–204).
- Why: Finishes the user row created by Settings → Invite.
- How to access + visibility: The email link. A bad GUID is ignored and the normal login form remains (`Login.aspx.vb` 60–65).
- Options and defaults: Email is filled from the invitation row. Password is chosen here. Role was chosen by the inviter and is not shown on this form.
- Permissions: Whoever has the GUID.
- Validation/failures: Blank password: “Please create a password to accept your invitation.” No 6-character check on this path. `googleOnly = 1` hides email and password so acceptance is the Google button.
- Result: Password or Google identity saved. Invitation id is not cleared in the SQL that was read (`Login.aspx.vb` 165, 204).
- Edge cases: Invited `FirstName` is often blank, so the next authenticated page other than Settings opens `ProfileRequired`.
- Code evidence: `Login.aspx.vb` 86–213; `webAPI/invitations.aspx.vb` 97–102; `UserPage.master.vb` 355–360.
- Confidence: Confirmed
- Suggested KB title: Accept a team invitation

### Secure registration

- Pages: `SecureRegistration.aspx`.
- What it does: The page body is an iframe of `UpdateAccount.aspx` with no query string (`SecureRegistration.aspx` 19). Plan choice is the Update Account UI.
- Why: Signup billing is the same Stripe page as a plan change.
- How to access + visibility: Public page. `UpdateAccount` still runs `LoginReplacement`, which redirects to `Login.aspx` when there is no session (`UpdateAccount.aspx.vb` 93–99).
- Options and defaults: Same monthly and annual images as Update Account.
- Permissions: A session is required once the iframe loads Update Account.
- Validation/failures: Same as Update Account.
- Result: Same Stripe customer and `StripePlan` writes.
- Edge cases: This catalog did not find a company-name or seat-count field on `SecureRegistration.aspx`.
- Code evidence: `SecureRegistration.aspx` 19; `UpdateAccount.aspx.vb` 93–99; `UpdateAccount.aspx` 414–449.
- Confidence: Confirmed
- Suggested KB title: Choose a plan during signup

### Welcome page

- Pages: `Welcome.aspx`.
- What it does: Redirects to `/Map` immediately (`Welcome.aspx.vb` 16–18).
- Why: The comment says the profile steps below were pre-2022 onboarding (`Welcome.aspx.vb` 27).
- How to access + visibility: Any request. The redirect does not check role.
- Options and defaults: None that run.
- Permissions: None that run.
- Validation/failures: None.
- Result: Browser goes to `/Map`. Demo products and the welcome profile form do not run.
- Edge cases: Do not document Welcome as a setup wizard.
- Code evidence: `Welcome.aspx.vb` 16–28.
- Confidence: Confirmed
- Suggested KB title: Do not publish Welcome as a customer step

### Required profile popup

- Pages: `ProfileRequired.aspx`, opened from `UserPage.master` `profile_setup_trigger` when the first name is blank (`UserPage.master` 1216, `UserPage.master.vb` 355–360). Not opened on Settings or `?printable=true`.
- What it does: Name plus icon picker (`showName` true, `immediate` false). Save validates with `DisplayNameError`, writes the name, then applies the icon (`ProfileRequired.aspx.vb` 19–38).
- Why: Blocks a blank display name on the main app pages.
- How to access + visibility: Automatic fancybox. All roles with a blank `FirstName`.
- Options and defaults: Same avatar rules as the picker. Name max length 50 on the picker text box (`ProfileIconPicker.ascx` 11).
- Permissions: The signed-in user.
- Validation/failures: Same name errors. Same image errors. A failed icon does not redirect.
- Result: `FirstName` saved. Parent page reloads, or `/Map` if there is no parent.
- Edge cases: Settings is excluded so a person can land on Settings with a blank name and type one there instead.
- Code evidence: `UserPage.master.vb` 346–360; `UserPage.master` 90, 1216; `ProfileRequired.aspx.vb` 8–38.
- Confidence: Confirmed
- Suggested KB title: Enter your name when the app asks

### Payment success page

- Pages: `SuccessSignup.aspx` and the redirect target `_cvr/SuccessSignup`.
- What it does: Static thank-you: “Success!” and “Thank you for Updating your subscription.” (`SuccessSignup.aspx` 24–29). No plan name is printed. Code-behind does nothing.
- Why: Landing page after Stripe checkout redirects.
- How to access + visibility: Redirect from `UpdateAccount.aspx.vb`.
- Options and defaults: None.
- Permissions: No role check in `SuccessSignup.aspx.vb`.
- Validation/failures: None.
- Result: Display only.
- Edge cases: Two success URLs are used by different branches. This catalog did not diff `_cvr/SuccessSignup.aspx` body text.
- Code evidence: `SuccessSignup.aspx` 24–29; `SuccessSignup.aspx.vb` 1–4; `UpdateAccount.aspx.vb` 122, 127, 180, 215.
- Confidence: Confirmed for `SuccessSignup.aspx`. Uncertain for the `_cvr` copy’s exact sentence.
- Suggested KB title: Subscription update confirmation

### OAuth consent

- Pages: `OAuth2/auth.aspx`, `OAuth2/consent.aspx`.
- What it does: `auth.aspx` constructs `New auth(Request, Response, authentication panel, consent panel, error label)` (`auth.aspx.vb` 10–11). `consent.aspx` validates the request, shows Cancel and Allow, and on allow calls `ReturnRequestWithUserID` (`consent.aspx.vb` 28, 155). Cancel calls `DenyRequest`, which redirects to the client redirect URI with an error code (`consent.aspx.vb` 32–35, 159). If the user index cannot be resolved, `RedirectToLogin` runs (`consent.aspx.vb` 128–149).
- Why: Lets an external client act as the signed-in user after consent.
- How to access + visibility: OAuth authorize URL, not a Settings menu item.
- Options and defaults: Buttons “Cancel” and “Allow” (`consent.aspx` 111–114). Scope text is rendered by `consentScreen`, which is not defined in this website project. Do not list scope names.
- Permissions: Must be logged in to get a user index. No Settings-role check in the consent file that was read.
- Validation/failures: Invalid request id, state, or redirect calls `DenyRequest` (`consent.aspx.vb` 70–128).
- Result: Redirect back to the client with the user id, or with an error.
- Edge cases: API keys on Settings are a separate mechanism from this consent screen.
- Code evidence: `OAuth2/auth.aspx.vb` 10–11; `OAuth2/consent.aspx` 103–114; `OAuth2/consent.aspx.vb` 28–38, 48–67, 128–159.
- Confidence: Confirmed for buttons and redirect behavior. Uncertain for scope wording.
- Suggested KB title: Allow or deny an OAuth connection

---

## Shared UI behavior

### Unsaved text and action lock

- Pages: Settings name, email, custom-field names, currency, and the create-field box use `text-input.js`.
- What it does: Focus remembers the value. Typing adds unsaved. Enter blurs (which fires change and saves). Escape restores the remembered value (`text-input.js` 5–26).
- Why: Avoids a separate save button on those fields.
- How to access + visibility: Those inputs.
- Options and defaults: None.
- Permissions: Same as the field.
- Validation/failures: Saving, saved, error, and deleting classes are visual only.
- Result: Depends on the field’s change handler.
- Edge cases: Threshold, max highlight, expiring soon, and currency also save on Enter through `toggle.js` 67–97, using their own buttons.
- Code evidence: `js/components/text-input.js` 5–29; `js/components/toggle.js` 32–97.
- Confidence: Confirmed
- Suggested KB title: How Settings text fields save

### One settings action at a time

- Pages: Invite, custom-field create/delete/reorder/visibility/personalized sort, API key create/delete.
- What it does: `setActionInProgress(true)` plus `blockAllActions` disables those controls until the request finishes (`action-blocking.js` 14–118).
- Why: Stops overlapping writes.
- How to access + visibility: Automatic.
- Options and defaults: None.
- Permissions: N/A.
- Validation/failures: “Another action is currently in progress. Please wait for it to complete.”
- Result: No data change by itself.
- Edge cases: Profile name, email, password, and display toggles are not in `blockAllActions`.
- Code evidence: `js/business/action-blocking.js` 6–118; `js/business/invitations.js` 6–9; `js/business/api-keys.js` 6–9; `js/business/custom-fields.js` 187–193.
- Confidence: Confirmed
- Suggested KB title: Why Settings asks you to wait

### Settings menu scroll

- Pages: Left menu on Settings.
- What it does: `initScrollSpy` highlights the menu item for the section in view. `goToAnchor` scrolls to `profile`, `fields`, `DefaultLocations`, `integrations`, `generalSettings`, or `subscription` (`menu.js` 4–16, 74). Hidden menus are skipped.
- Why: Navigation only.
- How to access + visibility: Same visibility as `ShowAllowedMenu`.
- Options and defaults: Menu labels: PROFILE & TEAM, CUSTOM FIELDS, DEFAULT LOCATIONS, API & INTEGRATIONS, OPTIONS, SUBSCRIPTION (`Settings.aspx` 54–86).
- Permissions: N/A.
- Validation/failures: None.
- Result: Scroll position.
- Edge cases: OPTIONS is the menu label for display settings plus, for admins, the account settings that follow on the page. Account settings have no separate menu item.
- Code evidence: `Settings.aspx` 51–87; `js/components/menu.js` 4–16; `js/pages/settings.js` 12–15.
- Confidence: Confirmed
- Suggested KB title: Settings page sections

---

## UNCERTAIN

- Stripe image pixels may show prices or marketing names. Those strings are not in `UpdateAccount.aspx`. The only selectable ids in code are the two live price ids above. Do not publish a price from this catalog.
- `consentScreen` and `auth` class source are not in this website tree. OAuth scope labels are unknown here.
- `lansweeperFieldToggle` (the UI class, not the page) was not opened. The page’s option list is the account’s custom fields. The saved pairing is uncertain.
- `lansweeperLinkAndSync.aspx.vb` and `lansweeperConnectionSuccess.aspx.vb` both use the class name `pages_settings_popups_lansweeperConnectionSuccess`. Which file is compiled was not verified.
- `_locationSelectorToggle.aspx.vb` and `pages/settings/popups/lansweeperCategoryLocationToggle.aspx.vb` both declare `pages_settings_popups_lansweeperCategoryLocationToggle`. The Settings href uses `_locationSelectorToggle.aspx`, whose code-behind contains the save SQL. The popup file’s own `Page_Init` is empty. Whether the site compiler merges those two files was not verified.
- Whether `_locationSelectorToggle` sets `cookie_refresh_settings` was not found in the save methods that were read. The Settings fancybox reloads only when that cookie is `TRUE`.
- Database column defaults for `SHOW_PRODUCT_IMAGES`, `SHOW_ZERO_QUANTITY`, and `SHOW_EXPIRATIONS` on a brand-new admin were not taken from a schema script. Invites copy expirations from the inviter. The settings page displays whatever is already stored.
- `AccountType` integer meanings were not mapped to a settings behavior.
- `_cvr/SuccessSignup.aspx` body text was not compared with `SuccessSignup.aspx`.
- No code path in this pass shows the “exceeded the capacity of your current plan” banner. Do not document a plan capacity.
- `SUPER_USER` has no Settings section. Whether any customer still has that `TypeOfUser` was not checked in data.
- Custom-field delete’s repository may or may not cascade product values. The UI warning says existing data will be erased. The repository method body was not read.
- Google login failure text for a normal (non-invitation) login was not traced past `VerfiyGoogleToken`.
- Half-hour time zones are not in the dropdown. Whether older accounts store other integers was not checked.

---

## CONTROLS CHECKLIST

Settings left menu

- [ ] PROFILE & TEAM — `section_menu_profileAndTeam` — Admin, User, Read-only
- [ ] CUSTOM FIELDS — `section_menu_customFields` — Admin, User, Read-only
- [ ] DEFAULT LOCATIONS — `section_menu_defaultLocations` — Admin, User
- [ ] API & INTEGRATIONS — `section_menu_apiAndIntegrations` — Admin, User, Read-only
- [ ] OPTIONS — `section_menu_generalSettings` — Admin, User, Read-only
- [ ] SUBSCRIPTION — `section_menu_subscriptions` — Admin

Profile

- [ ] Avatar presets 1–15 — `profile-icon-picker` `data-icon` — current user
- [ ] Upload — accept png, jpeg, gif, webp, max 3 MB
- [ ] Apply — `btn_apply`
- [ ] Name — `txt_profile_user_name` — required, max 50, unique on the account
- [ ] Email — `txt_profile_email`
- [ ] Update Your Password — hidden when Google ID is set
- [ ] Old Password — `txt_OldPassword`
- [ ] New Password — `txt_password_1` — server minimum 6
- [ ] Repeat Password — `txt_password_2` — must match
- [ ] Save password — `btn_password_reset`
- [ ] Cancel password — hides the div
- [ ] Link Google — `g-signin2` — only when Google ID is empty
- [ ] Badge Admin / User / Read-Only — one of these; Mobile badge is never shown

Team (Admin and User see the section; only Admin can change data)

- [ ] Search — `user-search` — appears when more than 12 users
- [ ] Pill Admin — `data-role=ADMIN`
- [ ] Pill User — `data-role=USER`
- [ ] Pill Read-Only — `data-role=READ-ONLY`
- [ ] Previous / Next — page size 12
- [ ] Role select ADMIN / USER / READ-ONLY — disabled unless the viewer is Admin; hidden on your own card
- [ ] DELETE user — Admin, other users only
- [ ] Invite email — `invite-email`
- [ ] Invite role ADMIN / USER / READ-ONLY — first option ADMIN
- [ ] Send Invitation — `btn_send_invite` — API admin only

Custom fields

- [ ] Personalized Sort — `toggle_personalized_sort` — default off — Admin, User, Read-only
- [ ] Buy Price Show — only while personalized sort is on — default shown
- [ ] Sell Price Show — only while personalized sort is on — default shown
- [ ] Move up / Move down — only while personalized sort is on
- [ ] Field name — Admin, real custom fields
- [ ] DELETE field — Admin
- [ ] Presets — Admin, Settings page only, not the product modal
- [ ] Allow other — `chk_allow_other` on `FixedMultiFields.aspx` — adds `Other (Specify)` only if another preset exists
- [ ] Create New Field... — Admin

Default locations (Admin and User)

- [ ] Default Check-In Location — `type=defaultcheckin` — clear stores `-2`, displayed as `(none)`
- [ ] Default Check-Out Location — `type=defaultcheckout`
- [ ] CLEAR Selection — popup `btn_clear`
- [ ] Save location — `btn_save_location`

API (section visible to all three roles; manager UI only if the account is on `_betaList`)

- [ ] Request-access sentence — non-beta
- [ ] Key name — `new_api_key_name_input`
- [ ] + Create New API Key
- [ ] DELETE key
- [ ] Read API Documentation — Postman link

Lansweeper (Admin section)

- [ ] Request-email sentence — this is the live control
- [ ] Connect / Synchronize / Disconnect — present only in comments, not live
- [ ] Site checkboxes and Connect — popup, not linked from Settings
- [ ] Custom-field match list — popup, not linked
- [ ] Location match — `type=lansweeper`, not linked from the live section

Display (Admin, User, Read-only unless noted)

- [ ] Share Map Layout — Admin only — default off
- [ ] Product Images — per user
- [ ] Zero Quantity Products — per user
- [ ] Expirations — per user
- [ ] Expiring Soon — default treated as on at 60 days when the stored token is absent; off stores 0
- [ ] Expiring soon number — `txt_expiring_soon_value` — min 1
- [ ] Unit days / weeks / months / years — `drp_expiring_soon_unit`
- [ ] save expiring soon — `btn_save_expiring_soon`
- [ ] Quantity Threshold — off stores 0; on starts at 1
- [ ] Threshold number — `txt_generalThreshold` — must be > 0
- [ ] save threshold — `btn_save_generalThreshold`
- [ ] Max Highlight — requires threshold on; value must be > threshold; off-state display 10
- [ ] Max number — `txt_maxHighlight`
- [ ] save max highlight — `btn_save_maxHighlight`
- [ ] Kitting — in the DOM, `display: none`, no save handler

Account (Admin, account-wide)

- [ ] Time zone dropdown — values -12 through 13, two labels share value 5 — fallback -5
- [ ] Currency symbol — `txt_currency` — fallback `$` — empty rejected
- [ ] save currency — `btn_currency`

Subscription (Admin)

- [ ] No Active Subscription / Subscribe to a Plan — when no plan name
- [ ] Plan name and optional Custom, Enterprise, or Legacy badge
- [ ] Billing Amount, Billing Frequency Annually or Monthly, Payment Method, Payment Details, Contact, Card, Activated
- [ ] Cancel Subscription — only if payment method string contains “Stripe”
- [ ] Update Plan — same
- [ ] Change Card — same
- [ ] Billing History — same
- [ ] Monthly image — price id `price_1O6zRX4D3SV7Y45Utyewx37h`
- [ ] Annual image — price id `price_1O6zS34D3SV7Y45UCZ8p3YaG`
- [ ] Enterprise image — no click handler
- [ ] Billing history columns Date, Amount, Subscription, Status
- [ ] Next payment date and amount
- [ ] Trial and payment banners — markup and CSS only; no Settings code shows them

Login and related pages

- [ ] Email — `txt_email`
- [ ] Password — `txt_password`
- [ ] Log in
- [ ] Google sign-in
- [ ] Forgot Password?
- [ ] Reset email — `txt_password_email_reset`
- [ ] Invitation: Create your password
- [ ] Reset: Pick a New Password
- [ ] Profile required name and icon
- [ ] OAuth Cancel
- [ ] OAuth Allow
