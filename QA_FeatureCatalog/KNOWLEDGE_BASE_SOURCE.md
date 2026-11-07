# CyberStockroom support knowledge source

This file is retrieval material for a customer-support assistant. It is not a published help article. Answer from these entries. Never present an **Uncertain** statement, or an entry marked **Not verified**, as a confirmed fact. If an entry does not cover the question, say that it is not covered. Do not invent prices, error text, stock math, or steps.

Roles:

- **Admin** can open every Settings section: profile, team, custom fields, default locations, API, the Lansweeper request, display settings including Share Map Layout, time zone, currency, and subscription.
- **User** can open profile, team, custom fields, default locations, API, and display settings. A User does not get Share Map Layout, Lansweeper, time zone, currency, or subscription.
- **Read-only** can open profile, custom fields, API, and display settings. A Read-only user does not get team or default locations, and cannot use the editable map, product list, product editor, Transfer, Start, import, or create pages.
- A legacy Mobile role is treated as User.

Someone who is not signed in is sent to the login page.

**All Locations** means the whole catalog. It is not a room or a building. Clearing a personal default location shows **(none)**.

A **records account** uses different activity labels (Assignments, Assign, Deallocate, Records) and turns price fields off. Do not describe that account’s stock movement with the add, subtract, or overwrite rules in this file. Those rules are for a standard inventory account.

When an unpaid trial has passed 14 days from account creation, or a confirmed subscription’s payment is delinquent, every signed-in page except Settings sends the person to Settings. Settings does not show a trial-expired banner, a plan-capacity banner, or a payment banner.

## SET — Settings shell

### SET-001 — Settings sections
- **Availability:** Current
- **Access:** Signed in. The menu hides sections the role cannot open.
- **Purpose:** Move around the Settings page.
- **Open:** Account menu, or the mobile **Settings** link.
- **Steps:**
  1. Open Settings.
  2. Click **PROFILE & TEAM**, **CUSTOM FIELDS**, **DEFAULT LOCATIONS**, **API & INTEGRATIONS**, **OPTIONS**, or **SUBSCRIPTION**.
  3. The page scrolls to that section. **OPTIONS** is the display settings. Time zone and currency are further down the same page and have no menu item of their own.
- **Options and limits:** Which items appear depends on the role list at the top of this file.
- **Result:** Scroll position only. Nothing is saved.
- **Troubleshooting:** None.
- **Related:** SET-002, SET-003
- **Confidence:** Confirmed

### SET-002 — Text fields save on change
- **Availability:** Current
- **Access:** Whoever can see the field.
- **Purpose:** Save a Settings text value without a separate Save button on that field.
- **Open:** Name, email, custom-field names, currency, and the create-field box. Quantity threshold, max highlight, expiring soon, and currency also save when you press Enter.
- **Steps:**
  1. Click the field. The current value is remembered.
  2. Type the new value.
  3. Press Enter to save.
  4. Press Escape instead to put the remembered value back. That does not save.
- **Options and limits:** Display toggles save when they are switched. They do not use this Enter behavior.
- **Result:** That field’s own save runs. Escape leaves the stored value unchanged.
- **Troubleshooting:** The field’s own error, not a shared message.
- **Related:** SET-003, ACC-009, ACC-010, ACCSET-002, CFL-004
- **Confidence:** Confirmed

### SET-003 — One settings write at a time
- **Availability:** Current
- **Access:** Whoever can start the action.
- **Purpose:** Stop a second invite, custom-field change, or API-key change while the first one is still running.
- **Open:** Invite, custom-field create, delete, reorder, visibility, personalized sort, and API key create or delete.
- **Steps:**
  1. Start one of those actions.
  2. Wait until it finishes before starting another. Those controls are disabled while it runs.
- **Options and limits:** Profile name, email, password, and the display toggles are not part of this wait.
- **Result:** One of those writes at a time.
- **Troubleshooting:** “Another action is currently in progress. Please wait for it to complete.”
- **Related:** SET-002, TEAM-004, CFL-001, API-001
- **Confidence:** Confirmed

## ACC — Sign-in and profile

### ACC-001 — Log in with email
- **Availability:** Current
- **Access:** Public. An existing session goes to the map.
- **Purpose:** Sign in with an email and password.
- **Open:** The login page.
- **Steps:**
  1. Enter the email. The placeholder is `me@email.com`.
  2. Enter the password.
  3. Submit.
- **Options and limits:** None.
- **Result:** The person is signed in.
- **Troubleshooting:** “The email or password is not correct...”
- **Related:** ACC-002, ACC-003, ACC-004, WF-009
- **Confidence:** Confirmed

### ACC-002 — Log in with Google
- **Availability:** Current
- **Access:** Public. On an invitation that is Google-only, the email, password, login, and forgot-password controls are hidden. The Google button stays.
- **Purpose:** Sign in with Google.
- **Open:** The Google button on the login page.
- **Steps:**
  1. Click the Google button.
  2. Complete the Google prompt.
- **Options and limits:** None.
- **Result:** The person is signed in when Google accepts the sign-in. This is confirmed for an invitation. The ordinary login button is expected to use the same sign-in.
- **Troubleshooting:** A failed invitation check leaves the page without an on-page message. Do not invent an error sentence for a normal Google login. That sentence was not traced.
- **Related:** ACC-004, ACC-012
- **Confidence:** Confirmed for the invitation path. Inferred for a normal Google login. The failure sentence for a normal login is Uncertain.

### ACC-003 — Forgot password
- **Availability:** Current
- **Access:** Public, from the login page.
- **Purpose:** Email a reset link and choose a new password.
- **Open:** Forgot password on the login page. The reset page is titled “Reset your password”.
- **Steps:**
  1. Enter the email and request a reset.
  2. Open the link in the mail. The mail is from `support@cyberstockroom.com` and the link goes to `https://www.cyberstockroom.com/Login?PasswordReset=` plus a code.
  3. On “Reset your password”, the email box is locked. The label is “Pick a New Password”.
  4. Submit. The person is signed in.
- **Options and limits:** This page does not show the 6-character rule used when changing a password in Settings. Use a real password. Invitation links use the site the person is on. Reset links use www.cyberstockroom.com.
- **Result:** The password is replaced and the person is signed in.
- **Troubleshooting:** Unknown email: “That Email is not in our records...”. Known email: “An Email has been sent”.
- **Related:** ACC-001, ACC-011
- **Confidence:** Confirmed

### ACC-004 — Accept an invitation
- **Availability:** Current
- **Access:** The person who received the invite email.
- **Purpose:** Join the account with the role the inviter already chose.
- **Open:** The invitation link from TEAM-004. The title is “Accept your Invitation”. The password label is “Create your password”.
- **Steps:**
  1. Open the link. The role is not shown and cannot be chosen here.
  2. Enter a password and submit.
  3. If the invitation is Google-only, use the Google button instead. Email and password are hidden.
- **Options and limits:** The password cannot be blank. This page does not require 6 characters. A bad link shows the normal login form.
- **Result:** The person joins the account and is signed in. If they still have no name, the name prompt opens on the next page other than Settings (ACC-007).
- **Troubleshooting:** “Please create a password to accept your invitation.”
- **Related:** TEAM-004, ACC-002, ACC-007, WF-009
- **Confidence:** Confirmed

### ACC-005 — Choose a plan during signup
- **Availability:** Current
- **Access:** During signup, inside the registration page.
- **Purpose:** Pick a monthly or annual plan while signing up.
- **Open:** The signup page shows the same plan images as a later plan change (SUB-002).
- **Steps:**
  1. Choose the monthly or annual image.
  2. Finish checkout.
- **Options and limits:** The enterprise image does not start checkout. Dollar amounts are drawn in the images. Do not quote a price. There is no company-name or seat-count field on this page. Without a session, the frame goes to the login page.
- **Result:** The same checkout as a plan change.
- **Troubleshooting:** None beyond the login redirect when there is no session.
- **Related:** SUB-002
- **Confidence:** Confirmed

### ACC-007 — Required name
- **Availability:** Current
- **Access:** Signed in, when the name is still blank. Not opened on Settings or on a printable view.
- **Purpose:** Require a name and a profile icon before the rest of the app is used.
- **Open:** A profile prompt opened by the app.
- **Steps:**
  1. Type a name and pick a profile icon.
  2. Save.
- **Options and limits:** Maximum 50 characters. The name must be unique on the account. Icons match ACC-008: png, jpeg, gif, or webp, under 3 MB, or a preset from 1 through 15.
- **Result:** The name is saved and the prompt stops. The parent page reloads, or the browser goes to the map if there is no parent.
- **Troubleshooting:** “Please enter your name.” “Please use 50 characters or fewer.” “Someone sharing this account is using this name already...”
- **Related:** ACC-008, ACC-009
- **Confidence:** Confirmed

### ACC-008 — Profile picture
- **Availability:** Current
- **Access:** Signed in, on Settings and on the required-name prompt.
- **Purpose:** Choose a preset avatar or upload a picture.
- **Open:** The profile icon picker.
- **Steps:**
  1. Choose a preset from 1 through 15, or upload a file.
  2. Click Apply.
- **Options and limits:** The default preset is 1. Accepted uploads are png, jpeg, gif, and webp, under 3 MB. On Settings the picker’s own name box is hidden. Change the name with ACC-009.
- **Result:** The profile picture updates.
- **Troubleshooting:** “Please choose an image file.” “Please choose an image under 3 MB.”
- **Related:** ACC-007, ACC-009
- **Confidence:** Confirmed

### ACC-009 — Your name
- **Availability:** Current
- **Access:** Signed in, on Settings.
- **Purpose:** Change the name shown on the team card, the menu, and activity.
- **Open:** The name field on Settings.
- **Steps:**
  1. Change the name.
  2. Leave the field or press Enter. Escape restores the value from when the field was focused and does not save.
- **Options and limits:** Maximum 50 characters. The name must be unique on the account.
- **Result:** The name is saved. The current user’s team card updates without a full reload.
- **Troubleshooting:** “Please enter your name.” “Please use 50 characters or fewer.” “Someone sharing this account is using this name already...”
- **Related:** SET-002, ACC-007, ACT-003
- **Confidence:** Confirmed

### ACC-010 — Your email
- **Availability:** Current
- **Access:** Signed in, on Settings, including a user who has linked Google.
- **Purpose:** Change the email on this user.
- **Open:** The email field on Settings.
- **Steps:**
  1. Change the email.
  2. Leave the field or press Enter.
- **Options and limits:** The address is checked for format, for uniqueness on this account, for uniqueness on any account, and against pending invitations.
- **Result:** The email is updated when those checks pass.
- **Troubleshooting:** The field title becomes “That email is invalid or already exists.”
- **Related:** SET-002, ACC-011
- **Confidence:** Confirmed for the title the user sees. Do not describe any extra same-value check. That comparison was not a reliable match against the current email.

### ACC-011 — Update your password
- **Availability:** Current
- **Access:** Settings profile. Hidden when the user signs in with Google.
- **Purpose:** Replace the password.
- **Open:** **Update Your Password** on Settings.
- **Steps:**
  1. Click **Update Your Password**.
  2. Enter the old password, the new password, and the repeat.
  3. Save. Cancel only hides the form.
- **Options and limits:** Minimum 6 characters. The page colors the field as you type (under 6 red, under 9 yellow, 9 or more green) and still sends the form. The server enforces the 6-character minimum. The new password must differ from the old one.
- **Result:** The password is changed and the browser returns to Settings.
- **Troubleshooting:** “The password is incorrect. Try Again?” “The passwords don't match. Try Again?” “That password is too short. Please use at least 6 characters. Try Again?” “The new password must be different! Try Again?”
- **Related:** ACC-003, ACC-012
- **Confidence:** Confirmed

### ACC-012 — Link Google on an existing user
- **Availability:** Current
- **Access:** Settings profile, only when Google is not already linked.
- **Purpose:** Attach Google to an email user.
- **Open:** The Google link button on Settings.
- **Steps:**
  1. Click the Google link button and finish the Google prompt.
  2. The browser returns to the profile section of Settings. On the next load, **Update Your Password** is gone.
- **Options and limits:** Linking does not change the CyberStockroom email.
- **Result:** The user is linked to Google.
- **Troubleshooting:** A rejected Google sign-in leaves no on-page message.
- **Related:** ACC-002, ACC-011
- **Confidence:** Confirmed

### ACC-013 — Role badge
- **Availability:** Current
- **Access:** The profile card, for a role that can see the profile section.
- **Purpose:** Show whether this user is Admin, User, or Read-only.
- **Open:** Settings, profile card.
- **Steps:**
  1. Open Settings.
  2. Read the badge: Admin, User, or Read-Only.
- **Options and limits:** Display only. A stored Mobile role is shown as User.
- **Result:** Nothing is saved.
- **Troubleshooting:** None.
- **Related:** TEAM-002
- **Confidence:** Confirmed

### ACC-014 — Subscription update confirmation
- **Availability:** Current
- **Access:** After a subscription update that lands on the success page.
- **Purpose:** Confirm that a plan change finished.
- **Open:** The success page after a subscription update.
- **Steps:**
  1. Finish a plan change that opens this page.
  2. Read “Success!” and “Thank you for Updating your subscription.”
- **Options and limits:** No plan name is printed. Some update paths use a different confirmation address. Do not quote that other page as the same two sentences. Its text was not compared.
- **Result:** A confirmation page only.
- **Troubleshooting:** None.
- **Related:** SUB-002
- **Confidence:** Confirmed for the main success page. Uncertain for the other confirmation address.

### ACC-015 — Allow or deny an OAuth connection
- **Availability:** Current
- **Access:** A signed-in user who was sent here by an application asking to connect. A missing sign-in goes to the login page.
- **Purpose:** Allow or refuse a connection. This is not an API key.
- **Open:** The consent screen.
- **Steps:**
  1. Read the screen. The exact permission wording is rendered outside this product’s pages and was not verified here.
  2. Click **Allow** or **Cancel**.
- **Options and limits:** Those two buttons only. Do not list permission names.
- **Result:** The requesting application receives an allow or a denial.
- **Troubleshooting:** None on the buttons. A missing sign-in goes to the login page.
- **Related:** API-001
- **Confidence:** Confirmed for the buttons. Uncertain for the permission wording.

## TEAM — Team members

### TEAM-001 — Team list
- **Availability:** Current
- **Access:** Settings, **PROFILE & TEAM**. Admin and User. Read-only does not get this section.
- **Purpose:** Find people on the account.
- **Open:** Settings, team section.
- **Steps:**
  1. Open the team section. Cards sort Admin, then User, then Read-only.
  2. If there are more than 12 people, a search box and role pills appear.
  3. Search matches name or email. Placeholder: “Search by name or email...”. Pills filter ADMIN, USER, and READ-ONLY. Each page shows 12 people.
- **Options and limits:** Search and pills stay hidden until there are more than 12 people. Seeing the list does not allow managing it. A legacy Mobile person is labeled USER.
- **Result:** A filtered view.
- **Troubleshooting:** “No users found”.
- **Related:** TEAM-002, TEAM-003, TEAM-004, WF-009
- **Confidence:** Confirmed

### TEAM-002 — Change a teammate’s role
- **Availability:** Current
- **Access:** Admin only. The role list is disabled for anyone else. Your own card has no role list.
- **Purpose:** Change another person’s role.
- **Open:** The role list on another user’s card.
- **Steps:**
  1. Choose ADMIN, USER, or READ-ONLY.
  2. Confirm. Cancel does not save.
- **Options and limits:** Those three roles. There is no Mobile choice.
- **Result:** That person’s role changes.
- **Troubleshooting:** A failed save reloads the cards from the last successful list.
- **Related:** TEAM-001, ACC-013, WF-009
- **Confidence:** Confirmed

### TEAM-003 — Remove a teammate
- **Availability:** Current
- **Access:** **DELETE** on another user’s card. Shown only when the viewer is Admin and the card is not themselves.
- **Purpose:** Remove a person from the account.
- **Open:** **DELETE** on that card.
- **Steps:**
  1. Click **DELETE**.
  2. Confirm “Are you sure you want to delete the user …”.
- **Options and limits:** You cannot delete your own card from this list.
- **Result:** That person is removed. If it was the last card on a page, the list moves to the previous page.
- **Troubleshooting:** Cancelling the confirm leaves the person in place.
- **Related:** TEAM-001, WF-009
- **Confidence:** Confirmed

### TEAM-004 — Invite a teammate
- **Availability:** Current
- **Access:** An Admin can send the invitation. The form can also be visible to a User. A User who sends it is rejected.
- **Purpose:** Email an invitation and choose the role the person will have.
- **Open:** Settings, **Invite a Team Member**.
- **Steps:**
  1. Enter an email. Placeholder `example@company.com`.
  2. Choose a role. The first option, and the unmarked default, is ADMIN. Choices are ADMIN, USER, and READ-ONLY.
  3. Send.
- **Options and limits:** The mail is from `admin@cyberstockroom.com`. The subject is “{inviter name} is inviting you to CyberStockroom. Details Inside.” The link opens the accept page (ACC-004). The invited person has no name until they accept. An email that already belongs to this account is not given a new role by another invitation. A new invite copies the inviter’s map position without turning on Share Map Layout, and it copies whether expirations are on.
- **Result:** An invitation is sent when the sender is an Admin and the email checks pass.
- **Troubleshooting:** “Please enter an email address.” “Please enter a valid email address.” A User who sends the form sees “Unable to Invite - Try Again?”
- **Related:** ACC-004, DSP-001, WF-009
- **Confidence:** Confirmed

## CFL — Custom fields

A custom field is a named text field, optionally with a preset list. There is no date, number, or dropdown field type. Names and presets are account-wide. Order, price visibility, and personalized sort belong to the current user. Create, rename, delete, and presets require Admin. Reorder and price visibility allow Admin, User, and Read-only.

### CFL-001 — Personalized sort
- **Availability:** Current
- **Access:** Settings custom fields, and the custom-field window on product pages. Admin, User, and Read-only.
- **Purpose:** Let this user order fields independently.
- **Open:** The personalized-sort switch.
- **Steps:**
  1. Turn personalized sort on.
  2. Use the up and down buttons, including on Buy Price and Sell Price.
  3. Turn it off to return the Settings list to the default order.
- **Options and limits:** Default is off. Turning it off does not erase the saved order. A new field is added at the end the next time a personal list is cleaned up.
- **Result:** This user’s field order. When the switch is off, the Settings list hides the Buy Price and Sell Price cards.
- **Troubleshooting:** “Unable to save the personalized sort preference right now.” The switch reverts.
- **Related:** CFL-002, CFL-003
- **Confidence:** Confirmed

### CFL-002 — Show or hide Buy Price and Sell Price
- **Availability:** Current
- **Access:** Admin, User, and Read-only, after personalized sort is on. On a records account the price fields are not offered in the product editor.
- **Purpose:** Hide or show Buy Price and Sell Price for this user.
- **Open:** The Buy Price and Sell Price cards. They are omitted from Settings until personalized sort is on. In the product window, a hidden price is a compact row with Show.
- **Steps:**
  1. Turn personalized sort on so the cards appear in Settings.
  2. Use Show on Buy Price or Sell Price.
- **Options and limits:** Default is visible. The cards say “DEFAULT”. Their names cannot be edited and they cannot be deleted.
- **Result:** This user sees or hides those prices on the map and in editors.
- **Troubleshooting:** “Unable to save the field visibility right now.”
- **Related:** CFL-001, PED-001, MAP-025
- **Confidence:** Confirmed

### CFL-003 — Add a custom field
- **Availability:** Current
- **Access:** Admin. **Create New Field...** on Settings and in the product-page field window.
- **Purpose:** Add an account-wide text field with no presets.
- **Open:** **Create New Field...**
- **Steps:**
  1. Type a name.
  2. Create the field.
- **Options and limits:** The new field starts without presets. The page does not show an empty-name error or a duplicate-name error.
- **Result:** An account-wide text field.
- **Troubleshooting:** None is shown for an empty or duplicate name.
- **Related:** CFL-004, CFL-006, SET-003
- **Confidence:** Confirmed

### CFL-004 — Rename a custom field
- **Availability:** Current
- **Access:** Admin. Buy Price and Sell Price cannot be renamed.
- **Purpose:** Change the account-wide label.
- **Open:** The name on a custom-field card.
- **Steps:**
  1. Change the name.
  2. Leave the field or press Enter.
- **Options and limits:** No length or uniqueness message is shown.
- **Result:** The label changes for the account.
- **Troubleshooting:** None.
- **Related:** CFL-003, SET-002
- **Confidence:** Confirmed

### CFL-005 — Delete a custom field
- **Availability:** Current
- **Access:** Admin. Buy Price and Sell Price cannot be deleted here.
- **Purpose:** Remove a custom field.
- **Open:** Delete on a custom-field card.
- **Steps:**
  1. Click delete.
  2. Confirm the warning. It says existing data for the field will be erased and recommends exporting inventory first.
- **Options and limits:** Cancel leaves the field. Which stored rows are removed beyond that warning was not fully traced.
- **Result:** The field definition is deleted. Treat the warning as the customer-visible promise. Do not add a list of records that was not verified.
- **Troubleshooting:** Cancel leaves the field.
- **Related:** CFL-003, RPT-001
- **Confidence:** Confirmed for the button and the warning. Uncertain for every related row that is removed.

### CFL-006 — Preset choices
- **Availability:** Current
- **Access:** Admin, from **Presets** on a Settings custom-field card. The product-page field window does not show Presets.
- **Purpose:** Limit a custom field to a list of text choices.
- **Open:** **Presets** on the Settings card.
- **Steps:**
  1. Click **Presets**.
  2. Enter the allowed values. Blank values are stripped.
  3. Optional: check “allow other”. That adds **Other (Specify)** only when at least one real preset remains.
  4. Save. An empty save leaves the field as a normal text field.
- **Options and limits:** Commas in stored presets become underscores. Closing the window does not refresh the Settings list. Reopen Settings to see the saved presets.
- **Result:** The field offers those choices where presets are used, including the product editor (PED-001).
- **Troubleshooting:** None is shown on this window for a rejected preset.
- **Related:** CFL-003, PED-001
- **Confidence:** Confirmed

## DEF — Default locations

Each user has their own defaults. Admin and User. A Read-only user cannot open the picker.

### DEF-001 — Default check-in location
- **Availability:** Current
- **Access:** Admin and User. Settings, **Default Check-In Location**.
- **Purpose:** Suggest this user’s check-in location on later check-in screens.
- **Open:** **Default Check-In Location**. The header is “Select Default Check-In Location”.
- **Steps:**
  1. Click **Default Check-In Location**.
  2. Pick a location and click Save, or click **CLEAR Selection**.
- **Options and limits:** Clear shows **(none)**.
- **Result:** That user’s default check-in location is updated and the Settings label reloads.
- **Troubleshooting:** None beyond the read-only block.
- **Related:** DEF-002, XFR-007, XFR-009, WF-001
- **Confidence:** Confirmed

### DEF-002 — Default check-out location
- **Availability:** Current
- **Access:** Admin and User. Settings, **Default Check-Out Location**.
- **Purpose:** Suggest this user’s check-out location, and the transfer source on Start.
- **Open:** **Default Check-Out Location**.
- **Steps:**
  1. Click **Default Check-Out Location**.
  2. Pick a location and Save, or clear the selection.
- **Options and limits:** Clear shows **(none)**.
- **Result:** That user’s default check-out location is updated and the Settings label reloads.
- **Troubleshooting:** None beyond the read-only block.
- **Related:** DEF-001, XFR-002, WF-003
- **Confidence:** Confirmed

## API — API keys

### API-001 — Create and delete an API key
- **Availability:** Restricted
- **Access:** The API section is visible to Admin, User, and Read-only. The key manager appears only for accounts that have been given API access. Everyone else is told to email support.
- **Purpose:** Create a named API key, or revoke one.
- **Open:** Settings, **API Keys**.
- **Steps:**
  1. If the account does not have API access, the page says to email support@cyberstockroom.com. Stop there.
  2. Enter a key name and click **+ Create New API Key**.
  3. Copy the key from the prompt. It is shown once: “This is the only time this API key will be shown. Please copy and store it safely:”.
  4. Later loads show a shortened key and an issued date such as `MMM d, yyyy`.
  5. Delete asks you to confirm. Access is revoked immediately.
- **Options and limits:** Names longer than 30 characters display with `...`. The full name is the tooltip. The exact customer sentence when access is off is: “The CyberStockroom API is currently available to select users only. You can request access by emailing us at support@cyberstockroom.com”.
- **Result:** A key is created or revoked. On an enabled account, a person who can open the manager can create a key and can delete a key from their own list.
- **Troubleshooting:** “Please enter a valid key name”. “Error creating API key. Please try again.”
- **Related:** API-002, SET-003, ACC-015
- **Confidence:** Confirmed

### API-002 — API documentation link
- **Availability:** Current
- **Access:** Under the API key area, including accounts that do not have API access.
- **Purpose:** Open the public API documentation.
- **Open:** **Read API Documentation**.
- **Steps:**
  1. Click **Read API Documentation**.
  2. A new tab opens `https://documenter.getpostman.com/view/1256102/2sB34ZqPYv`.
- **Options and limits:** None.
- **Result:** The documentation site. Nothing is saved.
- **Troubleshooting:** None.
- **Related:** API-001
- **Confidence:** Confirmed

## LSW — Lansweeper

### LSW-001 — Request the integration
- **Availability:** Restricted
- **Access:** Admin only. The live Settings block has no Connect button.
- **Purpose:** Ask support to connect Lansweeper.
- **Open:** The Lansweeper heading on Settings.
- **Steps:**
  1. Read “The Lansweeper Integration is available by request. If you'd like to conenct your Lansweeper account please email us at support@cyberstockroom.com to schedule a call.”
  2. Email support. Quote the sentence as it appears, including “conenct”.
- **Options and limits:** There is no Synchronize or Disconnect button on the live page.
- **Result:** No Lansweeper data changes from this block.
- **Troubleshooting:** None.
- **Related:** PED-004
- **Confidence:** Confirmed

## DSP — Display settings

These settings belong to the current user unless the entry says otherwise. Admin, User, and Read-only can use them. Share Map Layout is Admin only. A failed toggle reverts after about 1.5 seconds.

### DSP-001 — Share Map Layout
- **Availability:** Current
- **Access:** Admin. Settings, **OPTIONS**, **Share Map Layout**.
- **Purpose:** Let teammates copy this admin’s map layout. They cannot edit the shared original.
- **Open:** **Share Map Layout**.
- **Steps:**
  1. Turn **Share Map Layout** on.
  2. Teammates copy it from the map gear, **Shared Maps** (MAP-016).
- **Options and limits:** Default is off. Products and quantities are not shared. An invitation copies the inviter’s map position without turning sharing on for the new person.
- **Result:** This admin’s layout can be copied. Inventory is not copied.
- **Troubleshooting:** The toggle reverts after about 1.5 seconds if the save fails.
- **Related:** MAP-016, TEAM-004, WF-010
- **Confidence:** Confirmed

### DSP-002 — Product Images
- **Availability:** Current
- **Access:** Admin, User, and Read-only. Settings, **OPTIONS**.
- **Purpose:** Show or hide photos in the product list.
- **Open:** The product images toggle.
- **Steps:**
  1. Turn product images on or off.
  2. Open the product list. Image cells appear only when the switch is on.
- **Options and limits:** There is no camera button on the product-list toolbar.
- **Result:** This user sees or hides product photos in the list.
- **Troubleshooting:** The toggle reverts after about 1.5 seconds if the save fails.
- **Related:** PRD-009
- **Confidence:** Confirmed

### DSP-003 — Zero Quantity Products
- **Availability:** Current
- **Access:** Admin, User, and Read-only. Settings, **OPTIONS**.
- **Purpose:** Include or hide products whose quantity is 0 on the product list at All Locations.
- **Open:** The zero-quantity toggle.
- **Steps:**
  1. Turn the toggle off to hide products whose quantity is 0.
  2. Turn it on to include them.
- **Options and limits:** This switch does not paint locations white. Locations with quantity 0 staying white belongs to the quantity threshold (DSP-006).
- **Result:** This user’s product grid includes or skips zero-quantity rows.
- **Troubleshooting:** The toggle reverts after about 1.5 seconds if the save fails.
- **Related:** PRD-001, DSP-006
- **Confidence:** Confirmed

### DSP-004 — Expirations
- **Availability:** Current
- **Access:** Admin, User, and Read-only. Settings, **OPTIONS**.
- **Purpose:** Show or hide expiration tools for this user.
- **Open:** The expirations toggle.
- **Steps:**
  1. Turn expirations on. The Expirations menu appears, and a map popup can include expiration.
  2. Turn it off. The Expiring Soon block hides.
- **Options and limits:** Per user. A new invitation copies the inviter’s setting. Turning it off does not by itself write the expiring-soon window to 0.
- **Result:** This user sees or hides expiration tools.
- **Troubleshooting:** The toggle reverts after about 1.5 seconds if the save fails.
- **Related:** DSP-005, EXP-001, PED-005, WF-011
- **Confidence:** Confirmed

### DSP-005 — Expiring Soon
- **Availability:** Current
- **Access:** Settings, under Options, only while expirations are on.
- **Purpose:** Choose how far ahead a product counts as expiring soon.
- **Open:** The expiring-soon control. Helper: “Highlight products expiring within this period”.
- **Steps:**
  1. Turn the expiring-soon toggle on. An empty value saves 60 days.
  2. Enter a number of at least 1 and choose days, weeks, months, or years.
  3. Save.
- **Options and limits:** The markup default is 60 days. Off stores no highlight window. Weeks are stored as 7 days, months as 30 days, and years as 365 days. A month is not a calendar month. Exact multiples display as the larger unit (14 days shows as 2 weeks, 30 days as 1 month).
- **Result:** The expiration list and map highlights use that window.
- **Troubleshooting:** “Enable Expirations before using Expiring Soon.” “Expiring soon window must be a valid duration greater than 0.” “Error saving expiring soon window. Please try again.”
- **Related:** DSP-004, EXP-001, MAP-019, WF-011
- **Confidence:** Confirmed

### DSP-006 — Quantity Threshold
- **Availability:** Current
- **Access:** Admin, User, and Read-only. Settings, **OPTIONS**.
- **Purpose:** Mark low quantities on the map.
- **Open:** Quantity threshold. Copy: “Highlight locations with quantity at or below:”.
- **Steps:**
  1. Turn the toggle on. It saves 1 immediately.
  2. Enter a number bigger than 0.
- **Options and limits:** Off stores 0. If a value greater than 0 is already stored, the box shows it and is enabled. Otherwise the toggle is off and the box shows `1` disabled. Locations with quantity 0 stay white. Do not attach that white-location sentence to the zero-quantity product toggle.
- **Result:** This user’s low-quantity highlight (MAP-019).
- **Troubleshooting:** “The threshold must be a valid number bigger than 0.” “Error saving threshold value. Please try again.”
- **Related:** DSP-007, MAP-019
- **Confidence:** Confirmed

### DSP-007 — Max Highlight
- **Availability:** Current
- **Access:** Inside the quantity-threshold details, only while Quantity Threshold is on.
- **Purpose:** Mark high quantities on the map.
- **Open:** Max highlight. Copy: “Highlight locations with quantity at or above:”.
- **Steps:**
  1. Turn Quantity Threshold on.
  2. Turn max highlight on and enter a number greater than the threshold.
- **Options and limits:** When nothing is stored, the toggle is off and the box shows `10`. Off stores 0. That `10` is the empty-box placeholder, not a live threshold until you turn the switch on and save.
- **Result:** Locations at or above this number use the max color during a map search highlight (MAP-019).
- **Troubleshooting:** “Enable Quantity Threshold before using Max Highlight.” “Max highlight must be a valid number greater than 0.” “Max highlight must be greater than the quantity threshold.” “Error saving max highlight. Ensure it is greater than the quantity threshold.” If validation fails after the toggle was disabled, the control can stay disabled until reload.
- **Related:** DSP-006, MAP-019
- **Confidence:** Confirmed

## ACCSET — Account settings

Admin only. Both values apply to the whole account. If the account row cannot be read, currency falls back to `$` and time zone falls back to GMT−5.

### ACCSET-001 — Time zone
- **Availability:** Current
- **Access:** Admin. Settings, below Options. No menu item of its own.
- **Purpose:** Set the offset used for activity timestamps when no single user is filtered.
- **Open:** The time zone dropdown.
- **Steps:**
  1. Open the time zone dropdown.
  2. Choose an offset. It saves on change. “Saved ✓” shows for about 2 seconds.
- **Options and limits:** Whole-hour offsets from GMT−12 through GMT+13. Two labels share GMT+05:00: “(GMT+05:00) Yekaterinburg” and “(GMT+05:00) Islamabad, Karachi, Tashkent”. There is no half-hour zone. Do not invent the other city names. They come from that dropdown.
- **Result:** Activity timestamps use this offset when the history is not filtered to one user (ACT-001).
- **Troubleshooting:** “Error saving timezone. Please try again.”
- **Related:** ACT-001, SET-001
- **Confidence:** Confirmed

### ACCSET-002 — Currency symbol
- **Availability:** Current
- **Access:** Admin.
- **Purpose:** Set the symbol used on product prices.
- **Open:** The currency box on Settings.
- **Steps:**
  1. Type a symbol. The box shows `$` until the stored value loads.
  2. Save or press Enter.
- **Options and limits:** Any non-empty text. This is not a list of currency codes. It does not change how the subscription card formats its amount.
- **Result:** Product headers use the symbol.
- **Troubleshooting:** “Please enter a currency symbol”. “Error saving currency symbol. Please try again.”
- **Related:** PRD-003, SUB-001, SET-002
- **Confidence:** Confirmed

## SUB — Subscription and billing

Admin section. Plan labels: a standard plan shows the plan name with no badge. Custom shows “Custom Plan” and the badge “Custom”. Enterprise shows “Enterprise Plan”. Legacy shows “Legacy Plan”. Payment method labels: Cheque shows “Bank Cheque”. Coupa shows “Coupa (Payment Platform)”. Direct bank transfer shows “Direct Bank Transfer”. A PayPal card, PayPal invoice, or Stripe invoice shows “Online Invoice”. A Stripe card shows “Credit Card (Stripe)”. Anything else shows “(None)”. Annual shows “Annually”. Monthly shows “Monthly”.

### SUB-001 — Subscription summary
- **Availability:** Current
- **Access:** Admin. Settings, **SUBSCRIPTION**.
- **Purpose:** Read the current plan, amount, frequency, and payment method.
- **Open:** **SUBSCRIPTION**.
- **Steps:**
  1. Open Subscription.
  2. Read the plan name, billing amount, frequency, payment method, and card or contact details.
- **Options and limits:** USD and CAD amounts show `$` plus the currency code. Other currencies show the code, then the amount. A missing amount omits that row. This view is not a price table. Do not quote a price from it unless you are reading the customer’s own screen.
- **Result:** A display only. Nothing is changed.
- **Troubleshooting:** Empty state: “No Active Subscription”, “You don't have an active subscription. Subscribe to a plan to get started.”, and **Subscribe to a Plan**.
- **Related:** SUB-002, ACCSET-002
- **Confidence:** Confirmed

### SUB-002 — Change a Stripe subscription
- **Availability:** Current
- **Access:** Admin subscription section. **Update Plan**, **Change Card**, **Cancel Subscription**, and **Billing History** appear only when the payment method is a Stripe card (“Credit Card (Stripe)”). “Online Invoice” does not get these buttons. Cancel and billing history require Admin.
- **Purpose:** Change the plan, change the card, or cancel a Stripe-card subscription.
- **Open:** Those buttons on Subscription.
- **Steps:**
  1. Click **Update Plan**. Choose the monthly or annual image. The enterprise image does nothing. Do not quote a dollar amount. The prices are in the images.
  2. If a card is already on file, the plan can update without a new checkout. Otherwise Stripe checkout runs.
  3. **Change Card** opens the payment update.
  4. **Cancel Subscription** asks “Are you sure you want to cancel your subscription?” with **Cancel Subscription** and **Keep Subscription**.
- **Options and limits:** Monthly or annual. Other payment methods show “Please contact admin@cyberstockroom.com to change your subscription or payment method”. Stripe footnote: “For any billing questions please contact admin@cyberstockroom.com”.
- **Result:** Cancel turns the subscription off. The 14-day trial rule applies again. An account older than 14 days is sent back to Settings. A successful plan change can show ACC-014.
- **Troubleshooting:** Use the contact sentence above for a non-Stripe-card method.
- **Related:** SUB-001, SUB-003, SUB-004, ACC-005, ACC-014
- **Confidence:** Confirmed

### SUB-003 — Billing history
- **Availability:** Current
- **Access:** Admin, from **Billing History** on a Stripe-card subscription. Other roles cannot open it.
- **Purpose:** Read charges and the next payment.
- **Open:** **Billing History**.
- **Steps:**
  1. Open billing history.
  2. Read Date (such as `MMM dd, yyyy`), Amount, Subscription (invoice plan name plus description, cut off at `@`), and Status Successful or Failed.
  3. Next payment uses the first subscription’s period end and plan amount.
- **Options and limits:** There is no invoice table on the page.
- **Result:** A list of charges.
- **Troubleshooting:** Any failure replaces the table with “No billing history to show...” and hides next payment.
- **Related:** SUB-002
- **Confidence:** Confirmed

### SUB-004 — Trial end and failed payment
- **Availability:** Current
- **Access:** Automatic. There is no button.
- **Purpose:** Send an expired unpaid trial, or a delinquent confirmed payment, to Settings.
- **Open:** Any signed-in page other than Settings, when the condition is met.
- **Steps:**
  1. An unpaid trial lasts 14 days from the day the account was created.
  2. After that, pages other than Settings go to Settings.
  3. The same redirect happens when a confirmed subscription’s payment is delinquent.
- **Options and limits:** The person can still open Settings. They are not automatically shown a plan popup. Settings does not display “Your free trial has expired. Please select a plan to continue..”, “You have exceeded the capacity of your current plan. Please upgrade to continue.”, or “Your payment method needs to be updated!” Do not describe a plan-capacity limit.
- **Result:** The person stays on Settings until the billing condition changes.
- **Troubleshooting:** None. The redirect is the behavior.
- **Related:** SUB-002, SET-001
- **Confidence:** Confirmed

## MAP — Map and locations

The live map is the inventory map, including on a phone. There is no right-click menu and no free resize. The map starts locked. A Read-only user is sent to the read-only map. A non-read-only user who opens the read-only address is sent back to the editable map.

### MAP-001 — Open the inventory map
- **Availability:** Current
- **Access:** Signed in, and not read-only. A Read-only user gets MAP-002.
- **Purpose:** Open this user’s visual layout of every location.
- **Open:** Main menu **Map**.
- **Steps:**
  1. Click **Map**.
  2. Wait until the layout finishes and the map is revealed.
- **Options and limits:** Primary locations are children of All Locations and use this user’s saved positions. Nested locations are drawn inside their parent. There is no right-click menu and no resize handle. Compact tile sizes are not available.
- **Result:** This user’s layout only. Inventory is unchanged.
- **Troubleshooting:** If layout setup fails, the map still tries to reveal. There is no customer sentence for that failure.
- **Related:** MAP-002, MAP-008, MAP-009, MAP-044, WF-006
- **Confidence:** Confirmed

### MAP-002 — Read-only map
- **Availability:** Current
- **Access:** Automatic for a Read-only user. Anyone else is sent to the editable map.
- **Purpose:** View the map without the create control.
- **Open:** **Map**, as a Read-only user.
- **Steps:**
  1. Open the map. The floating **+** (“Create a new location...”) is hidden.
  2. Hover a location. The strip shows View (“View the products in this location...”), then **More actions**. Inside more: **V** and **3D** when those controls are drawn, and “View Location Details...”.
  3. Click the location to open the product peek (MAP-024).
  4. Click View to open the read-only product list for that location.
- **Options and limits:** Do not tell a customer that Read-only users cannot drag tiles, and do not tell them that they can rearrange the map. Whether the move handle still drags was not settled.
- **Result:** The same canvas and this user’s coordinates. Viewing does not change inventory.
- **Troubleshooting:** None.
- **Related:** MAP-001, MAP-024, MAP-027, MAP-028, MAP-029, MAP-038
- **Confidence:** Confirmed for the redirect and the hover. Uncertain for dragging.

### MAP-003 — Location types
- **Availability:** Current
- **Access:** Chosen when a location is created. No control was found that changes the type later.
- **Purpose:** Pick the icon for a new location.
- **Open:** Create on the map (MAP-005) or on mobile home (MAP-043).
- **Steps:**
  1. Start a new location.
  2. On the map, choose **BUILDING**, **WAREHOUSE**, **STORE**, **FLOOR**, **ROOM**, **CLOSET**, **SHELF**, **BIN**, or **VEHICLE**.
  3. On mobile home the same nine choices are **Building**, **Warehouse**, **Store**, **Floor**, **Room**, **Closet**, **Shelf**, **Bin**, and **Vehicle**.
- **Options and limits:** Anything outside those nine is named “Location” if it is stored. A missing type on the editor’s create path defaults to Building. Do not publish a step that changes the type after the location exists.
- **Result:** The type is stored and picks the location image. Inventory is unchanged.
- **Troubleshooting:** Mobile create: “Invalid location type.”
- **Related:** MAP-005, MAP-007, MAP-043, WF-006
- **Confidence:** Confirmed

### MAP-004 — Quantity labels on tiles
- **Availability:** Current
- **Access:** Every map, when it loads. No button.
- **Purpose:** Show how much stock is on a tile.
- **Open:** The map.
- **Steps:**
  1. A location with its own quantity greater than 0 is drawn full.
  2. A location with zero of its own and quantity only in children is ghosted. A 3D parent is the exception: it is drawn full, including when its own quantity is 0, and it gets a sloped bottom edge. That slope has no text. The word **3D** is a control, not a badge on the tile.
  3. On a primary tile the count reads `own (children)` when both are greater than 0, the own number when only the location itself has quantity, `(children)` when only children have quantity, and nothing when both are 0.
  4. A nested tile shows its own quantity only. A nested 3D parent with no quantity of its own and quantity in children shows `(children)`.
- **Options and limits:** Dragging a tile for check-out, transfer, or copy requires its own quantity greater than 0. Child stock alone does not make it draggable, including a 3D parent that only looks full because of children.
- **Result:** Display only.
- **Troubleshooting:** None.
- **Related:** MAP-014, MAP-019, MAP-021, MAP-022, MAP-029
- **Confidence:** Confirmed

### MAP-005 — Create a location
- **Availability:** Current
- **Access:** Editable map, not Read-only. A Read-only user cannot open the new-location page.
- **Purpose:** Add a location under All Locations, under a tile, or inside a 3D stack.
- **Open:** Floating **+** (“Create a new location...”) creates a child of All Locations. A **+** on a tile creates a child of that tile. Inside an open 3D stack, **Add** (“Add a location to this stack”) creates a child. The hover **+** is hidden on a 3D parent and on locations inside a 3D stack.
- **Steps:**
  1. If the map has no primary location, the prompt **Pick your first location** already shows the type list. The floating **+** does nothing while that prompt is up. Pick a type from the prompt.
  2. Otherwise click the floating **+**, the tile **+**, or **Add**.
  3. Click a type from MAP-003.
  4. The name box starts empty. The placeholder is “Type New {type} Name...”. The instruction is “Press Enter to Save...”.
  5. Type a name and press Enter.
- **Options and limits:** The box is not prefilled with a default name. A new primary location is highlighted on the next map load. A nested location is not highlighted that way. This page does not copy inventory onto the new location.
- **Result:** The location is created and a location-created activity is recorded.
- **Troubleshooting:** “That location name is already in use!”
- **Related:** MAP-003, MAP-007, MAP-036, MAP-037, MAP-043, WF-006
- **Confidence:** Confirmed

### MAP-006 — Rename a location
- **Availability:** Current
- **Access:** Location editor, not Read-only. **All Locations** is text only and cannot be renamed.
- **Purpose:** Change a location’s name.
- **Open:** The name field at the top of the location editor.
- **Steps:**
  1. Open the editor for a real location.
  2. Change the name. The current name is already in the field.
  3. Press Enter.
- **Options and limits:** None.
- **Result:** The name is updated and a location-edited activity is recorded with the comment `Changed location name to '{name}'`. Rename does not highlight the location on the map.
- **Troubleshooting:** “That location name is already in use!”
- **Related:** MAP-007, MAP-013, WF-006
- **Confidence:** Confirmed

### MAP-007 — Location editor
- **Availability:** Current
- **Access:** Editable map, **More actions**, then Edit (“Edit this location...”), or the phone footer **Edit**. Read-only goes away from this page. An unknown location shows a location error page.
- **Purpose:** Rename, add a child, open products, attach a file, set a barcode, or open a kiosk.
- **Open:** Edit on a location.
- **Steps:**
  1. Open the editor. You see the type image, the name, the breadcrumb (MAP-042), the children, **ADD NEW**, the paperclip (MAP-039), **Barcode # (scan to change)** (MAP-040), **Print Barcodes**, **View Products**, **Checkin Kiosk**, and **Checkout Kiosk**.
  2. Under **ADD NEW**, click or drag a type onto the page. That opens the same name page as MAP-005, as a child of this location.
  3. Click a child row to open that child.
  4. Click **View Products** to open the product list for this location.
- **Options and limits:** The map’s Edit link always opens an existing location. Do not use a different address as the way to create a location.
- **Result:** Creating a child inserts a location. The editor itself does not move stock.
- **Troubleshooting:** Name, barcode, and attachment failures are MAP-006, MAP-040, and MAP-039.
- **Related:** MAP-005, MAP-006, MAP-027, MAP-039, MAP-040, MAP-041, MAP-042, WF-005, WF-006
- **Confidence:** Confirmed

### MAP-008 — Move primary locations
- **Availability:** Current
- **Access:** Editable map. Drag the diamond on the location header. Nested locations have no header of their own. They move with the parent, or by MAP-010. The map starts locked (MAP-009).
- **Purpose:** Change where a top-level location sits on this user’s map.
- **Open:** The diamond move handle.
- **Steps:**
  1. If the lock title is “unlock map to move locations freely”, click the lock first.
  2. Drag the diamond header of a primary location and release it.
- **Options and limits:** There is no resize handle and no right-click move. While locked, an overlapping drop snaps back. While unlocked, overlaps are removed and the position saves. The grid allows up to 100 rows. The minimum primary width is 2 grid cells.
- **Result:** This user’s layout only. Nested locations stay inside the parent. Inventory stays on the same locations.
- **Troubleshooting:** A locked overlap is cancelled and is not reported in a sentence.
- **Related:** MAP-009, MAP-010, MAP-011, MAP-030, WF-006
- **Confidence:** Confirmed

### MAP-009 — Map lock
- **Availability:** Current
- **Access:** Editable map toolbar. Hidden on the bare designer frame. The saved preference is still read there.
- **Purpose:** Stop accidental moves.
- **Open:** The lock button.
- **Steps:**
  1. Open the map. The lock starts on. The button title is “unlock map to move locations freely”.
  2. Click the lock to unlock. The title becomes “lock map to prevent locations from being moved accidentally”. Positions save without a full reload.
  3. Click it again to lock. An in-progress reparent is cancelled.
- **Options and limits:** Locked is the default. Do not say the map starts unlocked.
- **Result:** The preference is stored for this user. Inventory is unchanged. While locked, an overlapping move snaps back.
- **Troubleshooting:** None on the button.
- **Related:** MAP-008, MAP-010, WF-006
- **Confidence:** Confirmed

### MAP-010 — Move a location under a different parent
- **Availability:** Current
- **Access:** Editable map. The clasp tooltip is “Snap off location and move to a different parent.” Hidden on the bare designer frame when the address contains a welcome flag.
- **Purpose:** Change a location’s parent without moving its stock to another location.
- **Open:** The clasp.
- **Steps:**
  1. Click the clasp.
  2. The banner says “Click a new parent or empty space on the map to move this location.” **Cancel** is on the banner. Escape cancels. Turning the lock on also cancels.
  3. Click a location tile, or click empty canvas. Empty canvas makes the location a primary location under All Locations.
  4. The dialog title is “Move location?” The message is “Move this location? Nested locations stay with it.” Click **Cancel** or **Move**.
- **Options and limits:** This is not a stock transfer.
- **Result:** The parent changes. Nested locations stay with it. Quantities stay on the same locations.
- **Troubleshooting:** Title “Could not move location”. Message “Could not move this location.” Button **OK**.
- **Related:** MAP-008, MAP-009, WF-006
- **Confidence:** Confirmed

### MAP-011 — Tile size follows children
- **Availability:** Current
- **Access:** Automatic. There is no resize handle.
- **Purpose:** Resize a primary tile to fit its children.
- **Open:** After adding or removing children, or turning **V** or **3D** on or off, reload the map.
- **Steps:**
  1. Add or remove children, or change vertical or 3D stacking.
  2. After the map reloads, the primary tile’s width and height follow the children.
- **Options and limits:** The minimum primary width is 2 grid cells. The grid allows up to 100 rows. Compact cell sizes are not used. There is no free resize.
- **Result:** Layout only.
- **Troubleshooting:** None.
- **Related:** MAP-005, MAP-008, MAP-028, MAP-029, WF-006
- **Confidence:** Confirmed

### MAP-012 — Delete a location
- **Availability:** Current
- **Access:** Editable map, **More actions**, then Delete (“Delete this location...”), or the phone footer **Delete**. Read-only cannot open the dialog.
- **Purpose:** Delete a location and its sub-locations, and check out stock that is still there.
- **Open:** Delete.
- **Steps:**
  1. Click Delete.
  2. The dialog shows the location name, path, and type image.
  3. The message is “Are your sure you want to DELETE this location?” and “All sub-locations will be deleted. Existing products will be checked out automatically.”
  4. Click **YES**. There is no No button. Closing the popup cancels.
- **Options and limits:** Sub-locations are always included. There is no choice to keep them. If the location and its children still have quantity, a check-out activity is recorded with the comment `Items cleared before deleting location '{name}' ({id})`, and those quantity rows are removed. Then the locations are deleted and a delete activity is recorded with `Deleted location '{name}' ({id})`. This is not the Transfer page.
- **Result:** The location and its sub-locations are gone. A primary location is removed from this user’s layout.
- **Troubleshooting:** If the location no longer exists when the dialog opens, the popup closes with no sentence. Closing the popup cancels.
- **Related:** MAP-021, WF-006. WF-003 is a different check-out.
- **Confidence:** Confirmed

### MAP-013 — Clone a location’s structure
- **Availability:** Current
- **Access:** Editable map, **More actions**, then Clone (“Clone this location...”), or the phone footer **Clone**. Not on the read-only strip.
- **Purpose:** Copy a location’s structure under a new name.
- **Open:** Clone.
- **Steps:**
  1. Click Clone.
  2. The title is “Name the New Location”. The name box allows 255 characters. The suggested name is the source plus ` (Copy)`, then ` (Copy 2)`, and so on up to 999, shortened so the whole name is at most 255 characters.
  3. **Auto-Rename Sub-Locations** is off by default. **Keyword** and **Replace with** start disabled. The tip is “Replaces a whole word or hyphen-separated part in sub-location names. For example, A32 to B45 renames A32-1 to B45-1. The new location itself keeps the name you entered.”
  4. Click **Clone** or **Cancel**. Enter in the name or keyword fields confirms. Escape closes the window.
- **Options and limits:** Keyword and replacement, each max 255, only when the switch is on. Keyword rename skips a blank result or a name that collides with a sibling.
- **Result:** The new root keeps the typed name. The map reloads and can highlight the new location. Whether quantities are copied is **Uncertain**. Do not say the clone copies stock, and do not say it leaves quantities at zero. Copying stock on the map is MAP-014.
- **Troubleshooting:** “Please enter a name for the new location.” “A clone cannot use the same name as the original location.” “That name is already used by another location next to the original.” A service error leaves the user on the map. No fixed error sentence was found for that failure.
- **Related:** MAP-014, MAP-037, WF-006
- **Confidence:** Confirmed for the page. Uncertain for whether quantities are copied.

### MAP-014 — Copy stock with Ctrl+drop
- **Availability:** Current
- **Access:** Editable map. Hold Ctrl, drag a full location (its own quantity greater than 0), and drop it on a different location. Not available while several locations are selected (MAP-030). A product chip from the peek is a transfer (MAP-022), not this copy.
- **Purpose:** Copy a location’s stock onto another location.
- **Open:** Ctrl+drag of a full location.
- **Steps:**
  1. Hold Ctrl.
  2. Drag a full location onto a different location. The same location, and All Locations as source or destination, are ignored.
  3. Confirm “Are you sure you want to copy the contents to this location? Any existing items will be cleared first.”
  4. Cancel does not copy.
- **Options and limits:** The confirm text says existing items at the destination are cleared first. What the copy does to each quantity is **Uncertain**. Do not publish a per-product formula. This is not the structure clone (MAP-013).
- **Result:** On confirm the map reloads when the copy succeeds.
- **Troubleshooting:** A failure leaves the user on the map. There is no fixed sentence.
- **Related:** MAP-013, MAP-022, MAP-030, WF-006
- **Confidence:** Confirmed for the prompt. Uncertain for the stock math.

### MAP-015 — ABC sort
- **Availability:** Current
- **Access:** Gear, **Map settings**, row **ABC Sort**. The row title is “When on, child locations are shown in alphabetical order.” Hidden when the bare designer frame turns mobile controls off. The saved flag still affects any map that reads it.
- **Purpose:** Sort a location’s direct children by name.
- **Open:** **Map settings**, **ABC Sort**.
- **Steps:**
  1. Open **Map settings**.
  2. Turn **ABC Sort** on or off. The default is off.
  3. The page saves and reloads.
- **Options and limits:** Direct children are sorted by name, then by id. Fewer than 2 children skips the sort. Primary canvas positions are a separate list.
- **Result:** Display order of direct children only. Inventory is unchanged.
- **Troubleshooting:** If the setting cannot be saved, the page does not reload. There is no customer sentence.
- **Related:** MAP-016, MAP-028, MAP-029
- **Confidence:** Confirmed

### MAP-016 — Use a shared map layout
- **Availability:** Current
- **Access:** **Map settings**, **Shared Maps**. An admin turns sharing on in Settings (DSP-001). Any signed-in user can sync to a shared layout.
- **Purpose:** Replace this user’s layout with a teammate’s layout.
- **Open:** **Shared Maps**.
- **Steps:**
  1. Open **Shared Maps**. While it loads, the row says “Loading…”.
  2. If the list is empty: “No shared maps. Admins can share their maps in the Settings page.”
  3. Choose a person. The dialog title is “Sync your Map Layout” and it shows that person’s name and email.
  4. The warning is “If you sync to this layout, you will lose your existing layout. Are you sure you want to continue?”
  5. Click **Keep my layout** or **Sync**. Escape or the backdrop cancels unless a sync is already running. While it runs the button says “Syncing…”.
- **Options and limits:** The copy includes positions, both zoom levels, vertical stacks, and 3D stacks. Inventory, products, and locations are not copied.
- **Result:** This user’s layout is replaced, then the map reloads.
- **Troubleshooting:** “Could not load shared maps.” “Sync is not available. Please refresh the page.” “Could not save the synced layout. Please try again.” “Could not sync this layout. Please try again.”
- **Related:** DSP-001, MAP-009, MAP-015, MAP-017, MAP-028, MAP-029, WF-010
- **Confidence:** Confirmed

### MAP-017 — Zoom
- **Availability:** Current
- **Access:** Zoom buttons on the editable and read-only maps. Each button’s title is “Type +/- to zoom”. Pinch works on touch. **+** and **−** work when the user is not typing.
- **Purpose:** Zoom the map.
- **Open:** The zoom buttons, pinch, or the keys.
- **Steps:**
  1. Click **+** or **−**, press those keys, or pinch.
  2. **+** multiplies the zoom by 1.1. **−** multiplies it by 0.9.
- **Options and limits:** Desktop zoom stays between 0.1 and 1. Touch zoom stays between 0.15 and 2.2. The first zoom is 1 on desktop and 0.74 on a narrow layout (about 900px wide) unless this user has saved a zoom. Keys are ignored while typing, during the one-location coach, or while a window is open. Ctrl+wheel does not zoom the browser page.
- **Result:** Zoom is saved for this user. Inventory is unchanged.
- **Troubleshooting:** None.
- **Related:** MAP-031, MAP-034, MAP-044
- **Confidence:** Confirmed

### MAP-018 — Search the map
- **Availability:** Current
- **Access:** The box placeholder is “Search Map...”. Clear is **×** (“Clear filter”). On narrow chrome a **>** button applies the filter (“Search”, “Apply filter”).
- **Purpose:** Highlight locations that match the text.
- **Open:** **Search Map...**
- **Steps:**
  1. Type in **Search Map...**.
  2. Matching tiles highlight and the view moves to them.
  3. Press Enter to cycle to the next match. The form does not submit.
  4. Press Escape, or click **×**, to clear the search and restore the previous scroll position.
- **Options and limits:** The same text can be passed along when a transfer opens from the map. Which fields the search service matches is **Uncertain**. If that search cannot be reached, the page matches location titles on the map instead.
- **Result:** Display only, until a later transfer uses the same text as a filter.
- **Troubleshooting:** An empty result disables the quantity download and sets its title to “No results to download”. There is no sentence for a search-service error.
- **Related:** MAP-019, MAP-020, MAP-032, MAP-034
- **Confidence:** Confirmed for the page. Uncertain for which fields are matched.

### MAP-019 — Low and high quantity colors
- **Availability:** Current
- **Access:** Automatic during a map search highlight. The numbers come from DSP-006 and DSP-007. This screen does not edit them.
- **Purpose:** Color searched locations by quantity.
- **Open:** Search the map (MAP-018).
- **Steps:**
  1. Search the map.
  2. A quantity of 0 or below is a plain location highlight, with no low, mid, or max color.
  3. If both the threshold and the max highlight are off, a quantity above 0 is the middle color only.
  4. Otherwise, quantity at or above the max highlight uses the max color and the tooltip starts with `MAX level`. Quantity at or below the threshold uses the low color. Anything else above 0 is the middle color.
- **Options and limits:** Do not publish a default threshold such as 10 as the live map rule. Locations with quantity 0 stay white even outside this search coloring (DSP-006). A non-numeric value is treated as off.
- **Result:** Color and tooltip only.
- **Troubleshooting:** None.
- **Related:** DSP-006, DSP-007, MAP-018
- **Confidence:** Confirmed

### MAP-020 — Check in from the map
- **Availability:** Current
- **Access:** Editable map hover, “Check IN products to this location...”. Not on the read-only strip. An empty location can be the destination. All Locations does not open the page.
- **Purpose:** Open Transfer in check-in mode for one location.
- **Open:** Check IN on a location.
- **Steps:**
  1. Hover the location and click Check IN.
  2. Transfer opens with the catalog as the source and this location as the destination. The current search text is passed as a filter.
  3. A wide layout opens Transfer in a popup. A narrow layout (about 900px) opens the mobile transfer page and stores a return path.
  4. During onboarding the import button can be hidden.
  5. Finish on that page (WF-002, XFR-001). The map click itself does not change quantities.
- **Options and limits:** Do not say an empty location cannot be a check-in destination.
- **Result:** The transfer page is opened. Stock changes happen there.
- **Troubleshooting:** All Locations returns without opening the page and without a sentence.
- **Related:** MAP-021, MAP-022, XFR-001, WF-002
- **Confidence:** Confirmed

### MAP-021 — Check out from the map
- **Availability:** Current
- **Access:** Editable map hover, “Check OUT products from this location...”, or drag a full location onto the strip. The strip’s visible label is **Check out**. Its accessible name is “Drag inventory here to check out”. The strip is hidden during onboarding. An empty location, or a location whose quantity is only in children, cannot start the drag and cannot open check-out. All Locations does not open it.
- **Purpose:** Open Transfer in check-out mode.
- **Open:** Check OUT, or the **Check out** strip.
- **Steps:**
  1. Hover a full location and click Check OUT, or drag that location onto **Check out**.
  2. Transfer opens with this location as the source and All Locations as the destination.
  3. Wide layout uses a popup. Narrow layout uses the mobile transfer page. Onboarding can hide import.
  4. Finish on that page (WF-003, XFR-002). The map click does not itself subtract stock.
- **Options and limits:** Delete’s automatic check-out (MAP-012) is not this transfer.
- **Result:** The transfer page is opened.
- **Troubleshooting:** An empty source returns without a sentence.
- **Related:** MAP-004, MAP-012, MAP-020, XFR-002, WF-003
- **Confidence:** Confirmed

### MAP-022 — Drag stock between locations
- **Availability:** Current
- **Access:** Editable map. Drag a full location, or a product row from the peek, onto a different location. The same location, and All Locations, are ignored. Ctrl+drop is MAP-014, unless a product chip is the drag.
- **Purpose:** Open a transfer between two locations, or the one-unit comment when the drag is exactly one unit.
- **Open:** A drop onto another location.
- **Steps:**
  1. Drag a full location, or a peek row, onto another location. A 3D parent opens its stack while you drag over it.
  2. If the drag is exactly one unit and onboarding is off, the single-unit dialog opens (MAP-023).
  3. Otherwise Transfer opens. A wide layout uses a popup. A narrow layout opens the mobile transfer page.
  4. Finish that page (WF-004).
- **Options and limits:** A drop on All Locations is not a transfer. Check-in and check-out are MAP-020 and MAP-021.
- **Result:** Inventory changes on the transfer page, not at the moment of the drop, except the single-unit commit in MAP-023.
- **Troubleshooting:** A same-location drop is ignored.
- **Related:** MAP-014, MAP-020, MAP-021, MAP-023, MAP-024, WF-004
- **Confidence:** Confirmed

### MAP-023 — Move one unit and comment
- **Availability:** Current
- **Access:** Automatic on an editable-map drop when onboarding is off, and either the dragged product quantity is exactly 1, or the location’s own quantity is exactly 1 and the lookup finds one product with quantity 1. The lookup asks for 25 products. If the lookup fails, or the location has more than one product with quantity, the full transfer page opens instead. Onboarding always opens the full transfer page.
- **Purpose:** Move that single unit and optionally add a comment, without the full Transfer page.
- **Open:** The drop described above.
- **Steps:**
  1. Drop that single unit on another location.
  2. The title is “Moving this item.” The hint is “Any comments about this transaction?”
  3. Leave the box empty and the button stays **Skip Comment**. Type a comment and the button becomes **Save**.
  4. Click **Skip Comment** or **Save**, or press Enter. **Cancel**, Escape, or the backdrop aborts and does not save.
- **Options and limits:** This sets that product’s quantity at the source to 0 and puts 1 at the destination. It is not “move 1 and leave the rest.” A one-unit click on the Transfer page does leave the rest (XFR-003).
- **Result:** That product’s source stock is set to 0. The destination receives 1. A transfer is recorded.
- **Troubleshooting:** A failed lookup opens the transfer page with no sentence.
- **Related:** MAP-022, XFR-003, WF-004
- **Confidence:** Confirmed

### MAP-024 — See products inside a location
- **Availability:** Current
- **Access:** Click a location on the editable or read-only map. The product-editor map uses the quantity box instead (MAP-026). A 3D stack also has **View contents** for the parent.
- **Purpose:** Peek at up to 25 products in a location.
- **Open:** Click the location.
- **Steps:**
  1. Click the location. The peek shows “loading...”.
  2. Up to 25 products load. While the map search has text, and the click is not in the “highlight location” state, the search is included. A highlight-location click clears that filter so the products in the location show without the search.
  3. Rows are draggable (MAP-022). A field chip can filter the rows (MAP-025).
  4. Press Escape to close the peek.
- **Options and limits:** Products past the first 25 are not requested. Do not say the peek lists every product when the location has more than 25.
- **Result:** A list on the map. No inventory change unless the user then drags a row or edits a quantity on the product map.
- **Troubleshooting:** A failed expiration lookup stores an empty date for that product. There is no sentence.
- **Related:** MAP-022, MAP-025, MAP-027
- **Confidence:** Confirmed

### MAP-025 — Popup details
- **Availability:** Current
- **Access:** **Map settings**, **Popup details**. The row title is “Choose which product fields show in the location popup.” Hidden when the bare designer frame turns mobile controls off.
- **Purpose:** Choose which product fields appear as chips in the location peek.
- **Open:** **Popup details**. The hint is “Select which product details to show in the popup.”
- **Steps:**
  1. Open **Popup details**.
  2. Turn fields on or off. The list is built for this account. Do not invent field names.
  3. An expiration switch appears only when the account has expiration data.
  4. Click **Done**.
- **Options and limits:** When nothing has been saved, description only is shown. Description stays on. Expiration is off until it is turned on. Buy Price, Sell Price, and personalized sort are edited in Settings, not in this popup.
- **Result:** The peek chips follow the saved fields. Inventory is unchanged.
- **Troubleshooting:** A bad field list becomes an empty list. Save is skipped if the map layout is not ready. There is no sentence.
- **Related:** MAP-024, CFL-001, CFL-002
- **Confidence:** Confirmed

### MAP-026 — Change quantity on the product map
- **Availability:** Current
- **Access:** The map inside the product editor. Read-only on that map is blocked. Helper text: “STEP 1 Select a product.” and “STEP 2 Click a location. Type new quantity. Press Enter.”
- **Purpose:** Set a product’s quantity at one location. This is an adjust. It is not a Transfer mode.
- **Open:** Click a location on the product’s map.
- **Steps:**
  1. Click a location. A quantity box opens for the product you are editing.
  2. Type the new quantity.
  3. Press Enter to save. Up and Down step the value when the pointer can hover.
  4. Press Escape to close the box without saving.
- **Options and limits:** Invalid input is replaced with 0 and is not sent. The on-screen number can change when the request is sent, not only after it succeeds. The comment stored is `Quantity for '{product number}' was adjusted from {old} to {new}`. The update waits about 3 seconds.
- **Result:** The quantity at that location is set to the number you typed when the update is accepted. What is stored after the service accepts the request is that new quantity. Do not add a second stock formula.
- **Troubleshooting:** “There was a problem updating the quantity in this location...” The on-screen number is not put back.
- **Related:** MAP-024, PRD-010, PED-006, WF-013. Not a Transfer mode (XFR-004).
- **Confidence:** Confirmed

### MAP-027 — Open the product list for a location
- **Availability:** Current
- **Access:** Hover View, “View the products in this location...”, on the editable and read-only maps. Location editor **View Products** does the same.
- **Purpose:** Open the product list filtered to that location.
- **Open:** View, or **View Products**.
- **Steps:**
  1. Click View, or **View Products**.
  2. The editable map opens the product list. The read-only map opens the read-only product list.
- **Options and limits:** “View Location Details...” is MAP-038, not this list.
- **Result:** The product list opens on that location. Quantity is unchanged by this click.
- **Troubleshooting:** None.
- **Related:** MAP-002, MAP-007, MAP-024
- **Confidence:** Confirmed

### MAP-028 — Vertical stack
- **Availability:** Current
- **Access:** Editable map, **More actions**, then **V**, or the phone footer **Vertical**. Hidden inside a 3D stack. Needs at least two direct children. A child that has its own children must already be 3D.
- **Purpose:** Stack child locations in a column.
- **Open:** **V** or **Vertical**.
- **Steps:**
  1. Open **More actions** and click **V**, or select the location and click **Vertical**.
  2. If it is allowed, the map reloads and children stack in a column. The default is off until you turn it on.
- **Options and limits:** Tooltips when it is not allowed: “Stack children vertically”, “Turn off vertical stack”, “Needs at least two children”, “A child has its own locations. Turn that child to 3D first”, “Turn off 3D first”, “Turn off 3D on a child first”, or “Vertical isn't available here.”
- **Result:** Layout only. Children keep their quantities.
- **Troubleshooting:** If the layout cannot be saved, the page does not reload. There is no customer sentence.
- **Related:** MAP-011, MAP-015, MAP-029, WF-006
- **Confidence:** Confirmed

### MAP-029 — 3D stack
- **Availability:** Current
- **Access:** Editable map hover **3D**, or the phone footer **3D**. The open stack is also used on the read-only map. Hidden for a location that is already inside a 3D stack. Empty parents can become 3D. Not allowed when a child is already 3D or a child has children.
- **Purpose:** Hide children in an overlay stack.
- **Open:** **3D**.
- **Steps:**
  1. Click **3D**. If it is allowed, the map reloads and children are hidden in an overlay.
  2. Click the parent to open or close the stack. Click outside to close it.
  3. **Add** on the stack creates a child (MAP-005). **View contents** peeks the parent.
  4. Search and drag can open the stack.
- **Options and limits:** Tooltips when it is not allowed: “Show children in a 3D stack”, “Turn off 3D stack”, “Already inside a 3D stack”, “A child is already 3D”, “A child has its own locations”, “Remove child locations before turning off 3D”, or “3D isn't available here.” A 3D parent with only child quantity is drawn full but still cannot be dragged unless its own quantity is greater than 0.
- **Result:** Layout only.
- **Troubleshooting:** If the layout cannot be saved, there is no customer sentence.
- **Related:** MAP-004, MAP-005, MAP-011, MAP-028, WF-006
- **Confidence:** Confirmed

### MAP-030 — Move several locations
- **Availability:** Current
- **Access:** Editable map on desktop. Off while touch controls are on, including tablet mode and the phone layout. Primary tiles only.
- **Purpose:** Move several top-level locations together.
- **Open:** Ctrl-click, Cmd-click, or Ctrl-drag on empty map.
- **Steps:**
  1. Ctrl-click or Cmd-click primary tiles, or Ctrl-drag a rectangle on empty map. The move starts after 5 pixels. The right mouse button does not select.
  2. Drag the group.
  3. Release to save. An invalid drop (collision or off the grid) is not saved.
  4. Press Escape to cancel the drag or clear the selection.
- **Options and limits:** Inventory is unchanged. Ctrl+drop inventory copy is suppressed while a selection is active. There is no right-click selection menu. Do not publish multi-select on a phone or while tablet mode is on.
- **Result:** This user’s positions for the group.
- **Troubleshooting:** An invalid drop is not saved and has no sentence.
- **Related:** MAP-008, MAP-014, MAP-033, MAP-034, WF-006
- **Confidence:** Confirmed

### MAP-031 — Minimap
- **Availability:** Current
- **Access:** The toggle title is “Minimap (picture-in-picture)”. The canvas label is “Map overview. Click to scroll the map.” It can open by itself on a large map when no open or closed choice is saved.
- **Purpose:** Jump the map by clicking a small overview.
- **Open:** The minimap toggle.
- **Steps:**
  1. Open the minimap.
  2. Click the picture. The big map scrolls to that spot.
  3. A drag that passes over the minimap can drop at the center of the current view.
- **Options and limits:** Open or closed. No saved state can auto-open. The canvas is 240 by 160.
- **Result:** Scroll position. Inventory changes only if that drop is a transfer or a Ctrl+copy.
- **Troubleshooting:** None.
- **Related:** MAP-008, MAP-017, MAP-018, MAP-022, MAP-030
- **Confidence:** Confirmed

### MAP-032 — Download a quantity report
- **Availability:** Current
- **Access:** Button title “Download Quantity Report”. It stays hidden until some visible location has quantity greater than 0. An empty search disables it and sets the title to “No results to download”. Signed in. The export itself has no separate read-only ban.
- **Purpose:** Download quantities from the map as a CSV.
- **Open:** **Download Quantity Report**.
- **Steps:**
  1. Click **Download Quantity Report**.
  2. The hint is “You are about to download the product quantities across your map.” If a search is active, the dialog shows “filtering by” and the term.
  3. Leave **Group by Location** selected (it starts checked), or choose **Group by Product**.
  4. Click **Download** or **Cancel**. Escape closes the dialog.
- **Options and limits:** **Group by Location** columns are Location ID, Location, Product Number, Description, Quantity, and empty locations are included. **Group by Product** columns are Product Number, Description, Quantity, summed. The file name starts `CyberStockroom - Group by Location` or `CyberStockroom - Group by Product`, then the date such as `MMM d yyyy`. A search term is inserted into the name. The name is cut at 200 characters, then `.csv`. Only quantities greater than 0 are included.
- **Result:** A file download. Inventory quantities are unchanged.
- **Troubleshooting:** “The map data could not be downloaded.” A signed-out request does not download and shows no sentence.
- **Related:** MAP-018
- **Confidence:** Confirmed

### MAP-033 — Tablet mode
- **Availability:** Current
- **Access:** **Map settings** row **Tablet mode**, or the tablet button. The row stays hidden until the device allows a user toggle. Hidden entirely when the bare designer frame turns mobile controls off.
- **Purpose:** Use touch controls and a selection footer.
- **Open:** **Tablet mode**.
- **Steps:**
  1. Turn **Tablet mode** on or off. If the user is not allowed to toggle, nothing happens and there is no sentence.
  2. The page saves and reloads. Touch UI, the selection footer, and edge scroll turn on. Multi-select turns off.
  3. On a narrow editable map, the first tap selects the location. The bottom bar shows **Edit**, **Clone**, **Vertical**, **3D**, **Delete**, and **Close**. **Vertical** and **3D** are left off when they do not apply. **Close** is “Return to standard footer”.
- **Options and limits:** Do not say every device shows the Tablet mode switch.
- **Result:** This user’s tablet-mode choice, and the touch layout. Inventory is unchanged.
- **Troubleshooting:** A disallowed toggle returns without a sentence.
- **Related:** MAP-030, MAP-034, MAP-044
- **Confidence:** Confirmed

### MAP-034 — Map keyboard shortcuts
- **Availability:** Current
- **Access:** The keyboard, when the condition in the step is true. Shortcuts do the same thing as the matching buttons.
- **Purpose:** Run map actions from the keyboard.
- **Open:** The keyboard.
- **Steps:**
  1. Press **+** or **=** to zoom in by 1.1, or **−** to zoom out by 0.9, when you are not typing, not in the one-location coach, and no window is open.
  2. Ctrl+wheel does not zoom the browser page.
  3. Enter in **Search Map...** cycles matches. Escape in that box clears the search.
  4. Escape closes clone, sync, export, reparent, the reparent error, the single-unit dialog, the peek, and the check-in lesson, and it clears multi-select.
  5. Hold Ctrl and drop a location to copy inventory (MAP-014), unless a multi-select is active.
  6. Ctrl or Cmd-click, and Ctrl-drag on empty map, select primary tiles. Touch controls turn this off.
  7. Enter in the product-map quantity box saves. Escape closes it without saving. Up and Down step that quantity on a fine pointer.
  8. Enter confirms clone and the single-unit dialog.
- **Options and limits:** There is no right-click shortcut. Do not publish multi-select keys while touch controls are on.
- **Result:** The same result as the matching feature. Inventory changes only for the quantity save, the single-unit commit, or Ctrl+drop.
- **Troubleshooting:** The matching feature’s errors.
- **Related:** MAP-013, MAP-014, MAP-017, MAP-018, MAP-023, MAP-026, MAP-030
- **Confidence:** Confirmed

### MAP-035 — Pan and scroll to origin
- **Availability:** Current
- **Access:** Drag empty canvas on the editable map. The origin button title is “Scroll to map origin (top-left)”. It starts hidden and appears when the user is scrolled away. The read-only page does not include that same grab-pan script. The map control’s own drag-scroll still loads with the control.
- **Purpose:** Pan the map and jump back to the top-left.
- **Open:** Empty canvas, or the origin button.
- **Steps:**
  1. Press empty canvas and drag. The cursor is grab, then grabbing. A drag that starts on a location, a move handle, the hover strip, the add tab, the check-out strip, the peek, the toolbox, the minimap, or the getting-started card does not pan.
  2. When you are scrolled away, click **Scroll to map origin (top-left)**.
- **Options and limits:** Do not say the read-only page includes the editable map’s grab-pan script.
- **Result:** Scroll position only.
- **Troubleshooting:** None.
- **Related:** MAP-002, MAP-017, MAP-031
- **Confidence:** Confirmed

### MAP-036 — Empty-map coaching
- **Availability:** Current
- **Access:** Editable map only, after layout. Not during onboarding for the getting-started card.
- **Purpose:** Show a first-location prompt, one-location tips, or a progress card.
- **Open:** Automatic.
- **Steps:**
  1. If there is no primary location, the prompt says **Pick your first location** and the type list is pinned there. The floating **+** does nothing until that prompt is gone.
  2. If there is exactly one location tile, the tips are **Create Sub-Locations** on the tile and **Create New Location** near the floating **+**. Zoom keys are blocked during this coach.
  3. If there is more than one location tile and the account has zero products, the card title **My Progress** is shown. The steps are “You started your map”, “Add your first product”, and “Check-in your products”.
  4. If there is more than one location tile, the account has products, and the sum of the tiles’ own quantities is 0, the lesson button’s accessible name is “Play 2 min lesson about checking in your products”. The lesson title is “2 min lesson about checking in your products”. Escape or **Close** closes the lesson.
- **Options and limits:** Do not say one card covers every mix. The bare designer frame has its own separate tips.
- **Result:** Coaching only, until the user creates a location or checks products in.
- **Troubleshooting:** None.
- **Related:** MAP-005, MAP-017, MAP-020
- **Confidence:** Confirmed

### MAP-037 — Highlight a new location
- **Availability:** Current
- **Access:** Automatic on the next map load after a primary create or a clone. No button.
- **Purpose:** Scroll to a location you just added as a primary location, or just cloned.
- **Open:** The next map load.
- **Steps:**
  1. Create a primary location or clone a location.
  2. After the reload, the map scrolls to the new location.
  3. A keyword rename on a clone can also show a notice.
- **Options and limits:** A nested create does not use this highlight. Do not say every new nested location is scrolled into view.
- **Result:** Highlight only.
- **Troubleshooting:** None.
- **Related:** MAP-005, MAP-013
- **Confidence:** Confirmed

### MAP-038 — View barcode and attachments (read-only)
- **Availability:** Current
- **Access:** Read-only hover, **More actions**, then “View Location Details...”. An unknown location goes to a location error page.
- **Purpose:** Download a location’s files and print its barcode without editing them.
- **Open:** “View Location Details...”.
- **Steps:**
  1. Click “View Location Details...”.
  2. Click a file name to download it. A stored name longer than 30 characters is shown as the first 20 characters plus `...`, then the extension.
  3. The barcode box is disabled. Click **Print Barcodes** to open the print page.
- **Options and limits:** Upload is not available here. The paperclip does not upload. Upload and delete are MAP-039.
- **Result:** Download or print. The barcode cannot be edited here.
- **Troubleshooting:** A missing location leaves the page with no sentence on this screen.
- **Related:** MAP-002, MAP-039, MAP-040
- **Confidence:** Confirmed

### MAP-039 — Attach a file to a location
- **Availability:** Current
- **Access:** Location editor. The paperclip title is “Click to attach file...”. Not Read-only. The read-only details popup shows a paperclip and does not upload.
- **Purpose:** Store or delete a file on a location.
- **Open:** The paperclip in the location editor.
- **Steps:**
  1. Click the paperclip.
  2. Choose a file. The editor reloads.
  3. To delete, confirm “Are you sure you want to delete this attachment?”
- **Options and limits:** A cancel on the confirm does not delete. Choosing no file does not upload. No type or size limit is shown.
- **Result:** The file is stored for that location, or it is deleted. Inventory is unchanged.
- **Troubleshooting:** None beyond the confirm.
- **Related:** MAP-007, MAP-038, WF-006
- **Confidence:** Confirmed

### MAP-040 — Location barcode
- **Availability:** Current
- **Access:** Location editor, “Barcode # (scan to change)”. Print tooltip “Print Barcodes”. The read-only peek barcode cannot be edited.
- **Purpose:** Set or print a location barcode.
- **Open:** The barcode box in the location editor.
- **Steps:**
  1. Click the barcode box. It selects the current value.
  2. Type a new value and press Enter. Enter does nothing if the text equals the saved barcode.
  3. If the barcode is free, it saves and the editor reloads.
  4. If it is already used, the box turns red with white text. There is no alert.
  5. Click **Print Barcodes** to open the print page. Print does not change the barcode.
- **Options and limits:** Do not say the peek barcode can be scanned to change.
- **Result:** The barcode is saved only when it is not already used.
- **Troubleshooting:** A taken barcode is the color change, not a sentence.
- **Related:** MAP-007, MAP-038
- **Confidence:** Confirmed

### MAP-041 — Location kiosk
- **Availability:** Current
- **Access:** Location editor, **Checkin Kiosk** (“Open Checkin Kiosk”) and **Checkout Kiosk** (“Open Checkout Kiosk”). They open a new tab. Not available to Read-only, because the editor is blocked.
- **Purpose:** Open Quick Scan locked to this location.
- **Open:** **Checkin Kiosk** or **Checkout Kiosk**.
- **Steps:**
  1. Open the editor.
  2. Click **Checkin Kiosk** or **Checkout Kiosk**.
  3. On a screen wider than 900px, Quick Scan opens in a popup-style page. At 900px or narrower it opens the mobile Quick Scan page. The location is locked to check-in or check-out.
- **Options and limits:** There is no kiosk transfer mode. Inventory changes happen in Quick Scan (XFR-011). What that save does to stock is **Uncertain**.
- **Result:** Navigation only, until Quick Scan is saved.
- **Troubleshooting:** If there is no location, the link does nothing useful.
- **Related:** XFR-011, WF-005
- **Confidence:** Confirmed for the links. Uncertain for Quick Scan’s stock math.

### MAP-042 — Location breadcrumb
- **Availability:** Current
- **Access:** The location trail in the location editor and in the transfer UI.
- **Purpose:** Jump to a parent or a child location.
- **Open:** Hover the breadcrumb.
- **Steps:**
  1. The trail starts with **ALL LOCATIONS**.
  2. Hover the breadcrumb. A menu of child locations opens.
  3. Click a location. The page reloads on that location. In the editor, that opens the existing location.
  4. On a transfer popup, the first click uses the pointer’s horizontal position. Left of 350 pixels is FROM. Otherwise it is TO.
- **Options and limits:** The breadcrumb itself does not move stock.
- **Result:** The page shows the chosen location.
- **Troubleshooting:** None.
- **Related:** MAP-007, MAP-020, MAP-022, WF-002, WF-004
- **Confidence:** Confirmed

### MAP-043 — Create a top-level location from mobile
- **Availability:** Current
- **Access:** Mobile home, the **+** tile (“Add location”). Not the map page. Signed in, and not read-only. The new location is always under All Locations.
- **Purpose:** Create one top-level location from the phone home screen.
- **Open:** **+** on mobile home.
- **Steps:**
  1. Tap **+**.
  2. The title is “Select a location Type”. Tap **Building**, **Warehouse**, **Store**, **Floor**, **Room**, **Closet**, **Shelf**, **Bin**, or **Vehicle**.
  3. The next title is “New location”. The name box is filled with “New ” plus that type name (for example “New Building”) and the text is selected. Maximum length is 200.
  4. Click **Create** or **Cancel**. Enter clicks **Create**.
- **Options and limits:** This screen cannot parent the new location under another tile. Nested create is MAP-005.
- **Result:** One top-level location is created and a location-created activity is recorded.
- **Troubleshooting:** “Please enter a name.” “Not signed in.” “Read-only users cannot create locations.” “Invalid location type.” “Invalid parent.” “That location name is already in use.” “Could not verify location name.” “Could not create location.” “Invalid request.” “Method not allowed.”
- **Related:** MAP-003, MAP-005, WF-006
- **Confidence:** Confirmed

### MAP-044 — Map on a phone
- **Availability:** Current
- **Access:** The inventory map at about 900px or narrower, or with tablet mode on. Read-only users still use the read-only map. Do not open a separate mobile map address. That address is not available.
- **Purpose:** Use the same map on a phone, with touch layout and the mobile transfer page.
- **Open:** **Map** on a phone.
- **Steps:**
  1. Open **Map**.
  2. The zoom starts at 0.74 unless this user has saved a mobile zoom.
  3. When the narrow touch chrome is on, the first tap selects a location and the bottom bar is **Edit**, **Clone**, **Vertical**, **3D**, **Delete**, and **Close**.
  4. Search shows the **>** button. Multi-select is off. Hover tooltips are off.
  5. A transfer, check-in, or check-out from a location opens the mobile transfer page as a full page.
- **Options and limits:** Browser pinch is turned off so it does not fight the map pinch. The same locations and the same inventory rules as the desktop map apply. The bare designer frame removes the lock, settings, zoom toolbar, ABC sort, shared maps, export, and tablet button from that embedded map.
- **Result:** Layout and which transfer page opens can change. Inventory rules do not.
- **Troubleshooting:** None beyond the feature being used.
- **Related:** MAP-001, MAP-017, MAP-020, MAP-021, MAP-022, MAP-030, MAP-033
- **Confidence:** Confirmed

## XFR — Check-in, check-out, transfer, Quick Scan, and mobile movement

These screens have no Adjust button. Batch, lot, expiration, and kitting are not fields on them. A Read-only user cannot open Transfer, the check-in page for new products, or Quick Scan, and is sent to the read-only map from Start and from the mobile menu.

When a Transfer address asks for both check-in and check-out, check-out wins.

Transfer and Start do not change stock the same way.

- **Transfer check-in** adds the chosen quantity at the destination. The catalog is not a stock location, so nothing is overwritten there.
- **Transfer check-out** sets the source quantity to the amount you left on the source side. It does not subtract from a freshly read balance, and it does not stop at zero by a floor. Nothing is added at a destination.
- **Transfer between two locations** sets the source to the amount you left behind and adds the moved amount to whatever is already at the destination.
- **Start check-in** adds. **Start check-out** subtracts and does not go below 0. **Start transfer** subtracts from the source and adds that quantity at the destination.
- On Transfer, the comment is collected before the stock write. On Start, the stock is already written when the comment box appears.

The map’s one-unit move (MAP-023) sets that product’s source quantity to 0. A one-unit click on Transfer leaves the rest at the source.

### XFR-001 — Check in
- **Availability:** Current
- **Access:** Signed in, not Read-only. From the map (MAP-020), from mobile after a location is chosen (XFR-008), or from the check-in page itself. The source header reads **CHECK-IN**. The source is the catalog. The destination is a real location. If the saved destination is also All Locations, the page picks another location.
- **Purpose:** Add catalog quantity at a location.
- **Open:** A check-in Transfer page.
- **Steps:**
  1. Use **search or scan**, or scan a barcode into it. The left list is the catalog, up to 250 rows. Each row shows an infinity mark instead of an on-hand count.
  2. Click a product. One unit moves to the destination.
  3. Click the infinity mark to open **Check-in quantity**. The prompt is “How many of '{name}' would you like to check in?” The quantity must be at least 1. There is no maximum. **Check In** applies it. **Cancel** closes the box. Enter confirms. Escape cancels.
  4. Drag a catalog row onto the destination. That also moves 1, not the whole catalog.
  5. Drag a destination row back to the source to clear that line. **Clear All (N items)** clears every selected line.
  6. While the destination is still empty, **import file** and **New Products** are available, unless import was hidden. A search with no catalog match shows **Create New Product**.
  7. Click **Check In**. The title is “Any comments about this transaction?” An empty box shows **Skip Comment**. Typed text changes the button to **Save**. Enter, Escape, and a click on the backdrop all confirm and continue the save.
- **Options and limits:** There is no **Check-In Everything** button. Lines with a moved quantity of 0 are skipped. If the address also asks for check-out, this check-in path does not run. Do not describe this save as a subtract, an overwrite of source stock, or a floor at 0. Do not describe the map’s one-unit move as this check-in.
- **Result:** The chosen quantity is added to whatever is already at the destination. One check-in activity is stored, including the comment. The comment is collected before the stock write.
- **Troubleshooting:** “Please enter a quantity of at least 1.” On the update box: “Please enter a quantity of 0 or greater.” A desktop scan or search that misses: “Product Number '{scan}' doesn't exist!” A mobile check-in miss opens Add Products instead of that alert.
- **Related:** WF-002, WF-001, WF-008, XFR-006, XFR-007, XFR-008, DEF-001
- **Confidence:** Confirmed

### XFR-002 — Check out
- **Availability:** Current
- **Access:** Signed in, not Read-only. From the map strip (MAP-021). The destination header reads **CHECKOUT**. The destination is All Locations. The left list is stock at the source.
- **Purpose:** Remove stock from a location by setting the source to what you leave behind.
- **Open:** A check-out Transfer page.
- **Steps:**
  1. Search or scan in **search or scan**. The list loads stock at the source, 250 rows at a time. A product with quantity 0 is left off the list unless that product is already selected.
  2. Click a product. One unit moves, and only up to the on-hand amount.
  3. Click the quantity. In check-out the add box still says **Transfer quantity** and “How many of '{name}' would you like to transfer? (Max: {max})”, and its button still says **Transfer**. The update box says **Update quantity** and “Enter the updated quantity for '{name}' to check out. (Max: {max})”, and its button says **Update**.
  4. Drag a row onto the destination to move all of the remaining quantity. Drag it back, or use **Clear All (N items)**, to return it.
  5. **Check-Out Everything** loads the location in pages of 500 and moves every remaining unit. Its tooltip is “Check out all the products in this location”. The label includes “(N shown)” when rows are on screen. The control is hidden while a map-filter badge is on.
  6. Click **Check Out**, then confirm “Any comments about this transaction?” **Skip Comment** or **Save** works the same way as check-in: Enter, Escape, and the backdrop confirm.
- **Options and limits:** When the address asks for both check-in and check-out, this check-out path is the one that runs. A partial line is marked on the source row while some quantity remains there and some is selected. Do not say this page subtracts and stops at 0. That rule belongs to Start (XFR-006). Do not describe a one-unit click here as the map’s one-unit move. The map’s one-unit move sets that product’s source stock to 0.
- **Result:** Save sets the source stock of each moved product to the quantity you left on the source side. The check-out activity stores the moved quantities, not the remaining quantity. The comment is collected before that write. Nothing is added at a destination.
- **Troubleshooting:** “Product '{term}' was not found at this location.” “Please enter a quantity of 0 or greater.” “Please enter a quantity up to {max}.” An import that asks for more than is on hand shows “Only {available} items were available at this location. Quantity adjusted from {requested} to {available}”.
- **Related:** WF-003, MAP-021, XFR-003, XFR-005, XFR-006, XFR-008, DEF-002
- **Confidence:** Confirmed

### XFR-003 — Transfer between two locations
- **Availability:** Current
- **Access:** Signed in, not Read-only. Drop a location or a product row onto a different location, or open **Transfer** on mobile after both locations are chosen. Both locations are real. The same location, or All Locations as the destination, is not this transfer.
- **Purpose:** Move quantity from one location to another.
- **Open:** Transfer with two different locations.
- **Steps:**
  1. Confirm the two location selectors name different places. Picking the same place on this page does nothing: the selectors keep the previous pair and show no message. The Start page, which is a different screen, shows “The Source can't be the Destination!”
  2. Search or scan the source list. It is on-hand stock, 250 at a time. Quantity 0 stays hidden unless that product is already selected.
  3. Click a product to move 1, up to on-hand. Click the quantity for **Transfer quantity** / “How many of '{name}' would you like to transfer? (Max: {max})” and **Transfer**. A later edit says **Update quantity**, “Enter the updated quantity for '{name}' to transfer. (Max: {max})”, and **Update**.
  4. Drag a row to move all remaining. Drag back or **Clear All (N items)** to undo.
  5. **Transfer Everything** follows the same all-remaining behavior as **Check-Out Everything**, including the 500-row pages, and hides while the map-filter badge is on. Tooltip: “Transfer all the products in this location”.
  6. Click **Transfer**. There is no **New Products** button on this mode. Then confirm “Any comments about this transaction?” with **Skip Comment** or **Save**.
- **Options and limits:** A one-unit click on this page keeps the rest at the source. The map’s one-unit move does not. Do not say this page subtracts from the source and then adds. The source becomes the quantity you left on the source side. The destination becomes its current quantity plus the amount moved.
- **Result:** One transfer activity stores the moved quantities. The comment is collected before that write.
- **Troubleshooting:** “Product '{term}' was not found at this location.” “Please enter a quantity of at least 1.” “Please enter a quantity of 0 or greater.” “Please enter a quantity up to {max}.” The import tooltip is the same on-hand sentence as check-out.
- **Related:** WF-004, MAP-022, MAP-023, XFR-002, XFR-005, XFR-006, XFR-008, XFR-009, DEF-001, DEF-002
- **Confidence:** Confirmed

### XFR-004 — Quantity adjust is not a Transfer mode
- **Availability:** Current
- **Access:** Transfer, Start, and the mobile movement screens.
- **Purpose:** Explain that these screens do not set a location’s quantity to an arbitrary number.
- **Open:** Check-in, check-out, or transfer on Transfer, Start, or mobile.
- **Steps:**
  1. Open one of those screens.
  2. Use **Check In**, **Check Out**, or **Transfer**. There is no Adjust button.
- **Options and limits:** The word “adjusted” on Transfer is only the import warning that a requested quantity was cut to on-hand: “Only {available} items were available at this location. Quantity adjusted from {requested} to {available}”. That is not an adjust activity.
- **Result:** A completed save is a check-in, a check-out, or a transfer, using XFR-001, XFR-002, XFR-003, or XFR-006. To set a quantity directly, use the product map (MAP-026) or the product list at a real location (PRD-010).
- **Troubleshooting:** None. There is no adjust action on these screens to fail.
- **Related:** MAP-026, PRD-010, XFR-001, XFR-002, XFR-003, XFR-005, WF-004
- **Confidence:** Confirmed

### XFR-005 — Import a file into a movement
- **Availability:** Current
- **Access:** On check-in, check-out, or transfer, before any quantity is in the destination list. The button label is **import file** (“Import from file”). It is hidden once the destination selection is not empty, and it is hidden when import was turned off for onboarding. Signed in, not Read-only.
- **Purpose:** Fill a movement from a file. This does not create products.
- **Open:** **import file**.
- **Steps:**
  1. Click **import file** and match the columns (PED-014).
  2. Return to the movement. The page locks into review. Search, drag, and the source list stay locked until you save or cancel. The status title is **Success!**, **Import Failed**, or **No items imported**.
  3. On **Success!** with at least one row, click **Check In**, **Check Out**, or **Transfer**. Then confirm the comment. If you did not edit the selection, the comment gains a file-import marker.
  4. **Cancel** closes the page and does not commit the movement.
- **Options and limits:** Check-in keeps the requested quantity and does not warn that a product is missing at the location. Check-out and transfer require on-hand stock and cut the line down when the file asks for more. A cut line shows “Only {available} items were available at this location. Quantity adjusted from {requested} to {available}”. More than one match is skipped. The save uses the host mode’s stock rule. A file sent into Start then uses Start’s add or subtract, not the Transfer overwrite.
- **Result:** A successful save writes the same stock change as the host mode. Cancel writes nothing. The review box can show “{n} rows imported”, “{n} adjusted quantities”, and “{n} rows skipped”.
- **Troubleshooting:** “The file could not be read. Please upload it again.” “The file did not contain any products.” “The file could not be checked. Please try the import again.” “No quantity was provided for this product.” “Quantity is missing.” “Quantity must be a whole number.” “Quantity must be greater than 0.” “This value matched more than one product in {field}.” “This product number was not found in your catalog.” “This value was not found in {field}.” “This product was not found at the source location.” “None of this product is available at the source location.” “The requested quantity is not available at the source location.” **Import Failed** adds “Please retry importing your file.” and **Retry Import**. Warnings offer **Upload Corrected File**. Check-in does not show the “not found at the source location” warning.
- **Related:** WF-008, WF-002, WF-003, WF-004, XFR-001, XFR-002, XFR-003, XFR-006, PED-014
- **Confidence:** Confirmed

### XFR-006 — Start page
- **Availability:** Current
- **Access:** Start. Signed in, not Read-only. Read-only goes to the read-only map. With no products, the menu is hidden and the page shows “You have not added any products yet” and **Click to create**. With products, the pictures are Create, Check In, Transfer, Check Out, and Quick Scan. Check-in, check-out, and transfer are hidden from the mobile menu when the account has no products. Quick Scan stays.
- **Purpose:** Check in, check out, or transfer with Start’s add and subtract rules, which are not the Transfer-page rules.
- **Open:** Start, or a Start address that already names the action and a location.
- **Steps:**
  1. Click **Check In**. The selector title is **Check In**, subtitle “Add Products to a Location”, then “Please select a Check In Location.” The default is the user’s check-in location (DEF-001).
  2. Click **Check Out**. Title **Check Out**, “Remove Products from a Location”, “Please select a Check Out Location.” Default is the check-out location (DEF-002).
  3. Click **Transfer**. Title **Transfer**, “Move Products between Location”, “Please select a Source Location for the Transfer.” Then pick a destination.
  4. Click **Create** to open Add Products (WF-001). Click Quick Scan for XFR-011.
  5. Choose products and finish.
  6. After the quantity is written, the page shows “Success!” and “You can leave a brief comment if you like.” The box placeholder is “Any comments about this transaction?” Click **Save Comment** to store the comment and open the map.
- **Options and limits:** Check-in adds the chosen quantity. Check-out subtracts and does not go below 0. Transfer subtracts from the source and adds that quantity at the destination. A file import that already named locations uses those locations. Do not use these add and subtract sentences for a records account. The comment is collected after the stock write. Leaving the comment box does not undo the stock change. The same source and destination shows “The Source can't be the Destination!” and “Please select a Destination.”
- **Result:** One check-in, check-out, or transfer activity for a standard inventory account. **Save Comment** only appends the comment and then opens the map.
- **Troubleshooting:** Check-in and check-out exit without saving when the chosen location cannot be read. There is no extra sentence for that miss.
- **Related:** WF-002, WF-003, WF-004, WF-001, WF-005, XFR-001, XFR-002, XFR-003, XFR-007, XFR-011, DEF-001, DEF-002
- **Confidence:** Confirmed

### XFR-007 — Check in products just created
- **Availability:** Current
- **Access:** After products are created (WF-001). Signed in, not Read-only. The catalog rows already exist. This page adds stock or sends the lines back to an open check-in. It does not create the products.
- **Purpose:** Place just-created products, skip placement, or return quantities to an open transfer.
- **Open:** The check-in page after create.
- **Steps:**
  1. Standalone, with no imported location on every line: the title is “1 Product created.” or “{n} Products created.” The map prompt is “Click a location to Check it in.” or “Click a location to Check them in.” The selected location starts from the address when that location exists, otherwise the user’s check-in default.
  2. Set each quantity to a whole number, 0 or greater, and at least one line to 1 or more. The quantity title is “This quantity will be checked in to the selected location.”
  3. Click **Check in**. The comment box is “Any comments about this transaction?” **Cancel** closes it without saving. An empty box uses **Skip Comment**. Typed text switches the button to **Save**.
  4. **Skip check-in** closes the page and does not add stock. The products stay in the catalog.
  5. When every imported line already has a real location, the map is hidden. Each line shows its location path, and the quantity title is “This quantity will be checked in to this location.” **Check in** saves each line to its own location.
  6. When this page was opened from an open transfer, there is no map. The title is “1 Product was created. Set the quantity, then continue.” or “{n} Products were created. Set quantities, then continue.” **Skip ››** drops the batch and returns to Transfer. **Continue** returns the quantities to Transfer and does not change stock on this page.
- **Options and limits:** A generated product number shows “1 product number was generated.” or “{n} product numbers were generated.” Lines with quantity 0 are omitted from the save. **Continue** does not check the products in. **Skip check-in** does not delete the new catalog rows. All Locations is not a valid destination for the save.
- **Result:** Standalone save adds the quantities at the one chosen location and writes one check-in activity. Imported-location save adds each line at its own location and writes one check-in activity. The done page reloads the parent window, or goes to the product list when there is no parent. Stock from **Continue** changes on the later Transfer save (XFR-001).
- **Troubleshooting:** “No products are waiting to be checked in.” “Each quantity must be a whole number, 0 or greater.” “Select a location on the map before checking in.” “Enter a quantity of at least 1 for one product.” “A location in this import could not be found.” One unusable imported location aborts the whole save.
- **Related:** WF-001, XFR-001, XFR-005, PED-010, PED-013, DEF-001
- **Confidence:** Confirmed

### XFR-008 — Mobile check-in, check-out, and transfer
- **Availability:** Current
- **Access:** Mobile menu **Check In**, **Check Out**, or **Transfer**. Signed in, not Read-only. These three items are hidden when the account has no products.
- **Purpose:** Run the Transfer stock rules from the phone.
- **Open:** Those menu items, then the location picker (XFR-009).
- **Steps:**
  1. Pick the location or locations. Check-in needs a destination. Check-out needs a source. Transfer needs both. The page says “Click to change” or, for transfer, “Click to change Source” and “Click to change Destination”.
  2. When no product list has been filled yet, the page opens the mobile transfer page in the matching mode. Choose products with the same clicks, drags, and labels as XFR-001, XFR-002, and XFR-003.
  3. Confirm “Any comments about this transaction?”
  4. **Save location** alerts “The location(s) will be saved for next time” and stores a check-in or check-out default. It does nothing when both a source and a destination are already set, so a transfer does not replace a saved default.
- **Options and limits:** Opening mobile home clears an in-progress movement (XFR-012). Do not use the older product-list path as the way a new mobile check-in works. That older path runs only when a product list is already filled. It adds on check-in, subtracts and stops at 0 on check-out, and subtracts then adds on transfer, and its comment box (“Add a comment?”, **Skip**, **Save**) is confirmed before that write. The current menu path uses the Transfer rules instead.
- **Result:** Check-in adds at the destination. Check-out sets the source to the quantity left behind. Transfer sets the source to the quantity left behind and adds that amount at the destination. Mobile home then shows “Check-in completed successfully.”, “Check-out completed successfully.”, or “Transfer completed successfully.”
- **Troubleshooting:** The Transfer page failures in XFR-001, XFR-002, and XFR-003.
- **Related:** WF-002, WF-003, WF-004, XFR-001, XFR-002, XFR-003, XFR-009, XFR-010, XFR-012, DEF-001, DEF-002
- **Confidence:** Confirmed

### XFR-009 — Mobile location picker
- **Availability:** Current
- **Access:** While a mobile process still needs a location. Source for check-out and for the transfer source. Destination for check-in and for the transfer destination. A contents list is view-only.
- **Purpose:** Choose the location for the mobile movement, or view what is in a location.
- **Open:** The mobile location list.
- **Steps:**
  1. The list is the location tree starting at All Locations. Expand a row with **+** (“Show or hide sub-locations”).
  2. For a source or contents list, the check-out default is pre-selected when that location still exists. For a destination list, the check-in default is pre-selected.
  3. Tap a location. The page returns to the process.
  4. The badge **default** switches to **change**. **change** opens the Settings location picker. If that window cannot open, the page goes to the default-locations section of Settings.
- **Options and limits:** Contents is view-only. **Save location** is hidden, and the header becomes the location name. A stored default that no longer exists is ignored. Tapping a location in Contents does not check stock in or out. The **default** badge is not the same control as **Save location** on the process page.
- **Result:** The chosen location is the source or destination for the movement that follows. Changing the default badge updates the user’s default through Settings, not through the movement save.
- **Troubleshooting:** A missing location sends the process page back to this picker.
- **Related:** WF-004, XFR-008, XFR-012, DEF-001, DEF-002
- **Confidence:** Confirmed

### XFR-010 — Older mobile product list and Quick Add
- **Availability:** Restricted
- **Access:** Not the list that **Check In**, **Check Out**, or **Transfer** open when the product list is empty. Those menu items open the mobile transfer page. This list is still reached from Back on the older progress steps, and Quick Add returns here. The search box says “Scan or Search...”
- **Purpose:** Increase a listed quantity by scanning, or create a catalog product that is not placed in a location.
- **Open:** The older product list, only from those return paths.
- **Steps:**
  1. Press Enter on a row that is already on the list. That row’s quantity increases by 1.
  2. Scan a value the list does not know. If the search result is a miss, Quick Add opens with that product number.
  3. On Quick Add, the description placeholder is “Description...”. Click **CREATE** or **CANCEL**.
- **Options and limits:** **CREATE** saves even when the description is empty. The new product is created in the catalog and is not placed at a location. The activity is a product create with quantity 1. **CANCEL** goes back without creating. Do not say Quick Add checks the product in. Do not tell someone to start Check In and expect this list.
- **Result:** **CREATE** adds a catalog product and returns to the product selector. A later save from a filled product list uses the older add, subtract-and-stop-at-0, or subtract-then-add behavior, not the Transfer rules.
- **Troubleshooting:** A scan that the search recognizes is added to the list. A miss opens Quick Add. No separate error sentence is shown for that miss.
- **Related:** WF-005, XFR-008, XFR-011, PED-010
- **Confidence:** Confirmed

### XFR-011 — Quick Scan
- **Availability:** Current
- **Access:** Start menu Quick Scan, the mobile menu **QuickScan**, or a location kiosk (MAP-041). Signed in, not Read-only. Quick Scan stays available when the account has no products.
- **Purpose:** Scan products and locations, then save a check-in, check-out, or transfer.
- **Open:** Quick Scan.
- **Steps:**
  1. The instruction is “Scan a product or location”. The field placeholder is “ready to scan...”.
  2. Scan a product. The first scan adds it with a count of 1. Scanning it again adds 1. The columns are **Source**, **Products**, and **Destination**.
  3. Scan a location. The first location fills **Source**. The next fills **Destination**. Scanning a location that is already source or destination swaps the two. Scanning another location when both are filled shifts the previous source into the destination.
  4. Source only shows **Check Out**. Destination only shows **Check In**. Both show **Transfer**. Otherwise the save button stays hidden.
  5. Optional text uses “Optional comment...”. Enter in that box saves. Click **Check In**, **Check Out**, or **Transfer**. On the mobile frame the button says **Save**.
  6. Kiosk: the instruction becomes “Scan products to check in” or “Scan products to check out”. The location is already filled, its delete control is hidden, and location scans are ignored. A transfer kiosk query is ignored and the page stays in normal Quick Scan.
- **Options and limits:** What the save does to stock, and which activity it writes, is **Uncertain**. Do not state that Quick Scan adds, subtracts, overwrites, or stops at zero. A missing barcode does not create a product. The page does not show an on-hand balance before the save.
- **Result:** Desktop success shows “{N} Transactions completed successfully.” The mobile frame shows “Transaction saved”. The list then clears, except a kiosk, which reloads the same locked location.
- **Troubleshooting:** “You have to select at least one location and one product!” “Kiosk mode is active; location and mode are fixed.” “There was a problem saving the transaction!” A scan request that fails shows no message and leaves the field unchanged.
- **Related:** WF-005, XFR-006, XFR-010, XFR-012, MAP-041
- **Confidence:** Confirmed for the page. Uncertain for the stock math and the activity it writes.

### XFR-012 — Mobile home
- **Availability:** Current
- **Access:** Mobile **Home**. Every load clears an in-progress movement. A Read-only user is sent to the read-only map before this menu is shown.
- **Purpose:** Start a movement from the phone, or clear one by opening Home.
- **Open:** Mobile **Home**.
- **Steps:**
  1. Open the menu. The links are **Home**, **Map**, **Products**, **Activity**, then **Check In**, **Check Out**, and **Transfer** when the account has at least one product, then **QuickScan**, **Help**, **Settings**, and **Logout**.
  2. After a location is primed, the footer shows **Check In**, the product-list icon (“View products in selected location”), and **Check Out**.
  3. **Check In** and **Check Out** open the process page (XFR-008). The list icon opens Products for that location.
- **Options and limits:** **Check In**, **Check Out**, and **Transfer** are omitted when the product count is 0. **QuickScan** remains. There is no footer **Transfer**. An empty recent-location list says “No recent locations.” Do not resume a half-finished mobile transfer by opening Home. That load clears it.
- **Result:** A later Check In, Check Out, or Transfer starts at the location picker again. The footer check-in and check-out use the primed location as the destination or source.
- **Troubleshooting:** None.
- **Related:** WF-002, XFR-008, XFR-009, XFR-011
- **Confidence:** Confirmed

## PRD — Product list

The list shows 50 products on a page request. All Locations is the whole catalog. A Read-only user does not stay on the editable list. They use the read-only list.

### PRD-001 — Product list
- **Availability:** Current
- **Access:** Products, from the inventory menu, for a signed-in user who is not Read-only. A Read-only user is sent to the read-only list.
- **Purpose:** Browse products at All Locations or at one location.
- **Open:** Products.
- **Steps:**
  1. Open Products.
  2. Leave the location on ALL LOCATIONS, or choose one location. On a narrow screen (900px and under) the location is shown as a path.
  3. A chosen location lists products whose quantity at that location is greater than 0. If that list is empty and a child location has stock, the page shows the child rows and “This location is empty but its sub-locations are not”.
  4. On ALL LOCATIONS, products with quantity 0 are appended after the in-stock rows when Zero Quantity Products (DSP-003) is on. When that setting is off, rows whose quantity is 0 are left out.
- **Options and limits:** The first visit sorts by product number, ascending. A later visit restores the page, sort direction, and sort column. Cost value in a row is that row’s quantity times its buy price and is calculated for display. Quantity cells in the sub-location summary are not the quick-edit cells in PRD-010. Do not assume every later page is a strict window of exactly 50 rows. The pager is offered when the count is above 50 (PRD-005).
- **Result:** The grid for the current page.
- **Troubleshooting:** A Read-only user never sees the editable page.
- **Related:** PRD-002, PRD-004, PRD-005, DSP-003, WF-013
- **Confidence:** Confirmed

### PRD-002 — Empty list
- **Availability:** Current
- **Access:** Products, or the read-only product list, when the grid has no rows.
- **Purpose:** Explain an empty catalog, an empty location, or a search with no hits.
- **Open:** The empty product list.
- **Steps:**
  1. With no products and the location on ALL LOCATIONS, the page shows “No products yet” and “Click to create”. That opens Add Products.
  2. A real location with no stock in it or in its children shows “Location is empty...” and “Click to Check in”. That opens check-in for that location on Start.
  3. A search with no rows shows “No matches found!” and hides “No products yet”.
- **Options and limits:** Do not use “Click to create” for a single empty location. That action is “Click to Check in”. When children have stock, the sub-location banner is used and this empty-location message stays hidden.
- **Result:** Create, check-in, or a no-matches message.
- **Troubleshooting:** Those sentences are the empty states.
- **Related:** PRD-001, PRD-006, PRD-011, PED-010, WF-001
- **Confidence:** Confirmed

### PRD-003 — Columns
- **Availability:** Current
- **Access:** Products. The same menu exists for a Read-only user. **EDIT COLUMNS** is visible only for an Admin.
- **Purpose:** Choose and order the product-list columns.
- **Open:** Hover the columns icon, “Select the columns to display in your inventory”.
- **Steps:**
  1. Hover the columns icon.
  2. Check or uncheck a column. Product Number stays checked. Its checkbox cannot be cleared.
  3. Drag a checked column name to change the order. Product Number stays at the front of the default set.
  4. Click **SAVE COLUMNS**. The list reloads, keeping the current page and sort.
  5. An Admin can click **EDIT COLUMNS**. That opens the custom-field editor.
- **Options and limits:** Columns: Product Number (always on), Quantity, Description (stored as Product Name), Buy Price, Sell Price, each custom field, and Cost Value. Buy Price, Sell Price, and Cost Value show the account currency in the header, for example “Buy Price (USD)”. Default when nothing valid is stored: Product Number, Quantity, Product Name, Buy Price, Sell Price, Cost Value, then every custom field. Cost Value is quantity times buy price, calculated when the row is drawn. It is not a stored product column. An empty description displays `UNTITLED (Product Number : {number})`. There is no camera button on this toolbar. Hiding photos is DSP-002.
- **Result:** This user’s column order. A missing or broken stored order is replaced by the default and the page reloads.
- **Troubleshooting:** A stale column name causes the page to restore the default set. There is no alert.
- **Related:** PRD-001, PRD-004, PRD-009, DSP-002, CFL-002
- **Confidence:** Confirmed

### PRD-004 — Sort
- **Availability:** Current
- **Access:** Products, on any visible column header.
- **Purpose:** Sort the list.
- **Open:** A column header: Product Number, Quantity, Description, Buy Price, Sell Price, a custom field, or Cost Value, for columns that are on.
- **Steps:**
  1. Click a column header. The list sorts ascending and returns to the first page.
  2. Click the same header again. The direction flips and the list returns to the first page.
  3. Open Products again later. The previous column and direction are restored.
- **Options and limits:** Quantity sorts by the sum of quantity. Cost Value sorts by that sum times buy price. Product number is the default when the sort is still the initial sort. Every header click returns to the first page.
- **Result:** The grid reloads in the new order. The sorted header shows an ascending or descending indicator.
- **Troubleshooting:** None.
- **Related:** PRD-001, PRD-003, PRD-005
- **Confidence:** Confirmed

### PRD-005 — Pages and select all
- **Availability:** Current
- **Access:** Products, when the list is not in search. The pager is hidden while a search is active and when the count is 50 or less.
- **Purpose:** Move between pages and select the current page or the whole catalog.
- **Open:** The pager and the header checkbox.
- **Steps:**
  1. When the count is above 50, use the page numbers, First Page, or Last Page.
  2. Click the checkbox in the header row. Every checkbox on this page is selected. When the pager is showing, the line reads “The {n} Products on this page are selected” and offers “Select all {full count} products.”
  3. Click “Select all {full count} products.” The line changes to “All {full count} Products in your inventory are selected” and offers “Clear selection.”
  4. Click “Clear selection” to return to the current page only, or clear the header checkbox to drop the selection.
- **Options and limits:** “Select all {full count} products” selects every product in the account. It is not limited to the current location or to a search. During search the pager is hidden, so that account-wide link is not offered. Do not promise that every later page shows only 50 rows.
- **Result:** The account-wide flag is what delete, multi-edit, and barcode print use when it is on.
- **Troubleshooting:** None on the pager.
- **Related:** PRD-001, PRD-006, PRD-011, PED-015
- **Confidence:** Confirmed

### PRD-006 — Search the product list
- **Availability:** Current
- **Access:** The header search, on any signed-in page, or a search link that opens Products. Read-only users can search. They land on the read-only list.
- **Purpose:** Find products across the catalog. Terms are combined with AND.
- **Open:** The header search, then Enter (SRCH-001).
- **Steps:**
  1. Type a term and press Enter. Products opens.
  2. Read the chips under the header. Each term is its own chip. When more than one chip is showing, an ALL chip is added.
  3. Separate words with commas to require every term. Each term matches product number, description, and every custom field, including custom fields that are hidden from the grid.
  4. Click a term chip to remove that term. Click ALL to clear every term.
- **Options and limits:** Buy price, sell price, and quantity are not searched. Search uses ALL LOCATIONS and hides the pager. Leaving Products and leaving Product Editor clears the search. A search does not stay inside the current location.
- **Result:** Matching products from the whole catalog. No matches shows “No matches found!”
- **Troubleshooting:** “No matches found!” There is no error for a blank search.
- **Related:** PRD-001, PRD-002, PRD-005, SRCH-001, WF-013
- **Confidence:** Confirmed

### PRD-007 — Open a product
- **Availability:** Current
- **Access:** A row on the product list. The same click on the read-only list opens the read-only editor.
- **Purpose:** Open the product editor.
- **Open:** A data cell in the row.
- **Steps:**
  1. Click a data cell (description, quantity, price, or another visible field).
  2. The product editor opens. On the read-only list, the read-only editor opens.
  3. The checkbox column selects the row. It does not open the editor.
- **Options and limits:** A web-address pill follows PRD-008 and does not open the editor. A product number the editor cannot find goes to a product error page.
- **Result:** The editor opens on that product.
- **Troubleshooting:** None on the click.
- **Related:** PRD-008, PED-001, PED-009, WF-013
- **Confidence:** Confirmed

### PRD-008 — Web addresses in the grid
- **Availability:** Current
- **Access:** Products and the read-only product list. A cell qualifies only when its entire text is a web address.
- **Purpose:** Open a web address stored as the whole cell.
- **Open:** A cell whose whole text is an `http://` or `https://` address, a protocol-relative address, a `www.` host, or a bare domain such as `example.com`.
- **Steps:**
  1. Click the pill. It opens in a new tab.
  2. A cell that has extra words around an address stays plain text and still opens the product editor.
- **Options and limits:** The pill text is the host, without a leading `www.`, plus a non-default port when one is present. `www.` hosts, bare domains, and protocol-relative addresses open as `https`.
- **Result:** The address opens in a new tab. The product editor stays closed for that click.
- **Troubleshooting:** A value that is not a whole-cell address is left as text. There is no error message.
- **Related:** PRD-007
- **Confidence:** Confirmed

### PRD-009 — Photos in the list
- **Availability:** Current
- **Access:** Products and the read-only list, when product images are on for this user (DSP-002). There is no camera button on the toolbar.
- **Purpose:** Show a 40 by 40 thumbnail above the product number.
- **Open:** The product list after product images are on.
- **Steps:**
  1. Turn on product images in Settings if the product-number column shows numbers only.
  2. Return to Products.
- **Options and limits:** When a photo is missing, a demo product whose number contains `CS_DEMO_` uses a demo image. Any other product uses a small camera placeholder.
- **Result:** The product number column shows the thumbnail and the number. Turning images off removes the thumbnails on the next load.
- **Troubleshooting:** A missing file is replaced by the fallback image. There is no alert.
- **Related:** DSP-002, PED-002, PRD-003
- **Confidence:** Confirmed

### PRD-010 — Change quantity in the list
- **Availability:** Current
- **Access:** The editable Products page only, with a real location selected (not ALL LOCATIONS), on a quantity cell that is in stock. Not during search, not on the sub-location summary, and not on the read-only list. This is separate from multi-edit.
- **Purpose:** Set the in-stock quantity at the current location.
- **Open:** Click an in-stock quantity.
- **Steps:**
  1. Select one location. ALL LOCATIONS leaves the quantity cell as a normal cell.
  2. Click an in-stock quantity. A small editor opens with the current number, up and down arrows, and a blue OK mark.
  3. Type a new whole number, or use the arrows. The down arrow stops at 0.
  4. Press Enter or click OK.
  5. Press Escape to close the editor and leave the quantity unchanged.
- **Options and limits:** Up adds 1. Down subtracts 1 and stops at 0. Arrow keys step the value only for a desktop pointer that can hover. A narrow or touch layout still has the on-screen arrows. The update waits about 3 seconds. The stock math inside the inventory service, beyond setting this location to the number you submit, was not read in this website.
- **Result:** On success the list reloads and keeps the current page and sort. The quantity shown is whatever was stored.
- **Troubleshooting:** “There was a problem updating the quantity in this location...” A non-numeric entry stays in the editor and is not submitted.
- **Related:** PED-006, MAP-026, PRD-011, WF-013
- **Confidence:** Confirmed for the request. Uncertain for any stock rule beyond the submitted quantity.

### PRD-011 — Add, delete, multi-edit, recent, export, print, printable
- **Availability:** Current
- **Access:** The Products toolbar. Add, delete, and multi-edit are on the editable page. Recent, export, print barcodes, and the printable image are also on the read-only list. Delete, multi-edit, and print barcodes stay inactive until a checkbox is selected. Export is always available. Add’s tooltip is “Add one or more products to your inventory”.
- **Purpose:** Start create, delete products, edit many products, see recent creates, export, print barcodes, or open a printable view.
- **Open:** The toolbar.
- **Steps:**
  1. Add: click the add image. Add Products opens (PED-010).
  2. Delete: check one or more products. Tooltip: “Delete selected products from your inventory.” Confirm “Are you sure you want to delete the selected products from your inventory? This action cannot be undone!” The checked rows are deleted, or every product in the account when select-all is on.
  3. Multi-edit: tooltip “Multi-Edit: Change all of the selected items at once”. In “For All Selected Items”, choose a field after SET, type a value after TO, and click Update. Cancel closes the panel.
  4. Recent: hover the recent-products image. The panel title is “Recently Created”. Click a row to open that product. The panel lists up to 50 creates.
  5. Export: tooltip “Download Product Report”. The product report opens for the current location (RPT-001). The current search is not included.
  6. Print barcodes: tooltip “Print barcodes for selected products”. If select-all is on, confirm “You are about to print barcodes for all {count} products. This may take a moment. Continue?”
  7. Printable: the image tooltip is the misspelled “pritnable version”. A new tab opens the product list in a printable view. The menu and the clickable controls are hidden. The browser print dialog is not opened.
- **Options and limits:** Multi-edit fields: Product Name; Quantity only at a real location; Buy Price; Sell Price; each custom field. Quantity overwrites the quantity at the current location. A custom field that lists “Other (Specify)” accepts any typed text. A preset list without that choice accepts only a listed value. On a standard inventory account, multi-edit records an edit with quantity 1 in the activity, not the number typed, and the comment `Changed '{field}' to '{value}'`. Do not describe that write for a records account. The live delete removes the product. The dialog says the action cannot be undone. Removal of images, attachments, and quantities inside the delete service is **Uncertain**. Do not describe an older quantity-only delete dialog as the live path. A Read-only user who opens the printable address is sent to the read-only list and the printable view is not kept.
- **Result:** Add opens create. Delete records a product-deleted activity and returns to the list. Recent rows are creates, newest first, up to 50. Export opens RPT-001. Barcodes open PED-015.
- **Troubleshooting:** Delete cancel leaves the list unchanged. Multi-edit: “Please enter a value”; “Value must be numeric!”; “Value is not allowed for this field.”; “Invalid field selected.” Recent, when there are no creates: “No recent new products...”. Print-barcode cancel on select-all stays on the list.
- **Related:** PED-008, PED-010, PED-015, RPT-001, PRD-005, WF-001, WF-013
- **Confidence:** Confirmed, with the delete cascade Uncertain

## PED — Product editor, create, import, barcodes

### PED-001 — Edit name, price, and custom fields
- **Availability:** Current
- **Access:** Product editor. The product number is the label “PRODUCT NUMBER:” and cannot be renamed. Read-only users are sent to PED-009. An Admin also sees “Edit your fields”.
- **Purpose:** Change the name, prices, and custom fields.
- **Open:** A product row or search.
- **Steps:**
  1. Fields follow the account’s field order: Product Name, then buy price, sell price, and custom fields where those are visible.
  2. Click a text field, change it, and press Enter. The hint “Press Enter to Save...” appears while the field is active.
  3. For a custom field with presets, open the dropdown. Choose “(none)”, a preset, the current value when it is outside the list, or “Other (Specify)”.
  4. “Other (Specify)” opens a box titled “Other (Specify):”. Type a value and click Save, or Cancel to keep the previous value.
  5. An Admin can click “Edit your fields”.
- **Options and limits:** Buy Price and Sell Price appear only on a standard inventory account and only when CFL-002 says to show them. Their labels include the account currency. “(none)” stores an empty value. Currency fields reject a non-numeric value and a negative value. Do not tell users they will see “The Product Name is not valid!” for a normal name edit. That sentence is not shown for a normal name.
- **Result:** The field is saved and an edit activity is recorded with `Changed '{label}' to '{value}'`. The editor reloads. The product list is marked to reload when the user returns to it.
- **Troubleshooting:** “The Buy Price is not valid!” or “The Sell Price is not valid!” when the value is not numeric or is negative. A custom-field text error uses “The field {name} is not valid!” only when a numeric check on that field fails.
- **Related:** PRD-007, PED-009, CFL-002, WF-013
- **Confidence:** Confirmed

### PED-002 — Product photo
- **Availability:** Current
- **Access:** Product editor, the image under PRODUCT NUMBER. Tooltip: “Click to update image...”. Read-only users can see the image and cannot upload. A Lansweeper image removes the click and the tooltip (PED-004).
- **Purpose:** Replace the product photo.
- **Open:** Click the product image.
- **Steps:**
  1. Click the product image and choose a file. The editor uploads it and reloads.
  2. If the image came from Lansweeper, the picture is not clickable. Use the Lansweeper link.
- **Options and limits:** The upload does not show a file-type or size error. Do not invent a size limit or an allowed-type list. A missing image falls back to a camera placeholder, or to a demo image when the product number contains `CS_DEMO_`.
- **Result:** The new image is shown on the editor. The product list is marked to reload.
- **Troubleshooting:** Choosing no file leaves the current image.
- **Related:** PED-004, PED-009, PED-011, PRD-009
- **Confidence:** Confirmed

### PED-003 — Product attachments
- **Availability:** Current
- **Access:** Product editor, tooltip “Click to attach file...”. Existing files appear as chips named `{filename}.{extension}`. Read-only users can download a chip and do not see upload or delete. This is not a purchase order, sales order, or kit document.
- **Purpose:** Attach, download, or delete a file on a product.
- **Open:** The attachment image.
- **Steps:**
  1. Click the attachment image and choose a file. The editor reloads and shows a chip.
  2. Click the chip to download the file.
  3. Click the X on that chip. Confirm “Are you sure you want to delete this attachment?”
- **Options and limits:** The upload does not show an extension list or a size check. There is no message for a rejected type or an oversized file.
- **Result:** The file can be downloaded from the chip. Delete removes that attachment and reloads the editor. Other products are unchanged.
- **Troubleshooting:** Cancel on the confirm leaves the attachment.
- **Related:** PED-009
- **Confidence:** Confirmed

### PED-004 — Lansweeper link on a product
- **Availability:** Current
- **Access:** Product editor and the read-only editor. The Lansweeper image is hidden until an asset lookup returns a link.
- **Purpose:** Open the linked Lansweeper asset.
- **Open:** The Lansweeper image on a linked product.
- **Steps:**
  1. Open a product that is linked to a Lansweeper asset.
  2. Click the Lansweeper image. The asset opens in a new window.
  3. When the asset type has a Lansweeper image, that image replaces the product photo and the photo click is removed.
- **Options and limits:** Do not expect the button on every product. If the lookup fails, the link stays hidden and there is no error sentence.
- **Result:** The user is looking at the Lansweeper asset. The product row is unchanged.
- **Troubleshooting:** None on the page.
- **Related:** PED-002, PED-009
- **Confidence:** Confirmed

### PED-005 — Expiration on the product
- **Availability:** Current
- **Access:** Product editor, the EXPIRATION date, only when expirations are on for this user. The same date is shown disabled on the read-only editor.
- **Purpose:** Set or clear one product’s expiration date.
- **Open:** The expiration field.
- **Steps:**
  1. Open the product.
  2. Pick a date. The field allows `2018-01-01` through `2050-01-01`.
  3. Read the color: green when more than 60 days remain, gold when 60 or fewer days remain and the date is still in the future, red when the date is today or earlier.
  4. Clear the date to remove it.
- **Options and limits:** The color window on this field is 60 days. It is separate from the account expiring-soon window (DSP-005). A failed save is not shown as an alert. Import of a date is PED-013. An existing product in a create-import does not receive the file’s expiration.
- **Result:** A chosen date is saved for this product. A cleared date is removed. The other catalog fields are unchanged.
- **Troubleshooting:** No on-screen error when the expiration save fails. Import, on a bad date: “Row {n}: Expiration must be a date such as 2026-12-31.”
- **Related:** EXP-001, PED-007, PED-013, WF-011
- **Confidence:** Confirmed

### PED-006 — Product editor map
- **Availability:** Current
- **Access:** The right side of the product editor. Quantity behavior is MAP-026. Read-only users can still see their map and cannot edit quantity there the same way.
- **Purpose:** Change this product’s quantity by clicking a location.
- **Open:** The map on the product editor. The instruction reads “Click a location. Type new quantity. Press Enter.”
- **Steps:**
  1. Click a location, type the new quantity, and press Enter.
  2. After a quantity change, the editor reloads so the map and the fields match.
- **Options and limits:** The first load of the editor uses zoom 0.9. Clone does not copy location quantities onto the new product.
- **Result:** The quantity change follows MAP-026.
- **Troubleshooting:** Map errors belong to MAP-026.
- **Related:** MAP-026, PED-007, PED-009, PRD-010, WF-013
- **Confidence:** Confirmed

### PED-007 — Clone a product
- **Availability:** Current
- **Access:** Product editor, tooltip “clone this product”. Read-only users do not get the button. This modal is the live clone.
- **Purpose:** Create a new product from the current fields, without copying stock or attachments.
- **Open:** The clone image.
- **Steps:**
  1. Click the clone image. The dialog title is “Clone Product”.
  2. Leave Auto checked to accept the next number. The number box shows “[Automatic Product Number]” and stays disabled.
  3. Or uncheck Auto and type a product number.
  4. Adjust the copied fields. When expirations are on, an Expiration date is included.
  5. Click Clone. Cancel closes the dialog.
- **Options and limits:** Auto is checked by default and assigns `CSN-` plus nine digits. Empty name is saved as the new product number. A price that does not parse is saved as 0. The date is copied only when expirations are on and a date was entered. Quantities, locations, and attachments are not copied. The image is copied when that copy succeeds.
- **Result:** The new product is created. A create activity is recorded. The new editor opens with a “new” badge once.
- **Troubleshooting:** “You must enter a product number.” “That product number already exists!”
- **Related:** PED-001, PED-005, PED-006, WF-013
- **Confidence:** Confirmed

### PED-008 — Delete one product
- **Availability:** Current
- **Access:** Product editor, tooltip “Delete this product”. Read-only users do not get the button. This uses the same delete as the product list.
- **Purpose:** Delete the open product.
- **Open:** The trash button.
- **Steps:**
  1. Click the trash button.
  2. Read “Delete this product?” and “Deleting this product will also check it out of all locations on the map.”
  3. Click Delete, or Cancel.
- **Options and limits:** The dialog states that the product is checked out of all locations. Whether images, attachments, and every quantity row are removed is **Uncertain**. Do not promise a result the delete service was not verified to complete. Cancel leaves the product. A missing product goes to a product error page.
- **Result:** The product delete runs and a product-deleted activity is recorded. The editor then asks for that same product number, which is no longer there.
- **Troubleshooting:** Cancel closes the dialog.
- **Related:** PRD-011, WF-013
- **Confidence:** Confirmed for the click. Uncertain for images, attachments, and quantities.

### PED-009 — Read-only product editor
- **Availability:** Current
- **Access:** A Read-only user opening a product. A user who is not Read-only and opens the read-only editor is sent to the editable editor.
- **Purpose:** Read a product, print a label, download an attachment, open Lansweeper, and view the map.
- **Open:** A product, as a Read-only user.
- **Steps:**
  1. Open a product.
  2. Read the fields. They are disabled.
  3. Use Print Barcodes, an attachment chip, the Lansweeper image when it is present, and the map.
- **Options and limits:** Clone, delete, photo upload, and attachment upload are not on this page. The expiration date is visible and disabled.
- **Result:** No catalog field is saved from this page.
- **Troubleshooting:** A missing product number goes to a product error page.
- **Related:** PRD-007, PED-001, PED-002, PED-003, PED-004, PED-006
- **Confidence:** Confirmed

### PED-010 — Create products by typing
- **Availability:** Current
- **Access:** Add Products, from the product-list add button, from “+ New Products” on the selector, or from header “Create New Product”. The page title is “Create New Products”. A single add from a mobile transfer uses the title “Add Product” and does not open check-in. Read-only users are not given this page from the product toolbar. A records account disables prices.
- **Purpose:** Type one or more new products, then check them in unless this was the single mobile add.
- **Open:** Add Products.
- **Steps:**
  1. Leave AUTO checked, or uncheck it and type a product number. AUTO’s placeholder is “CSN-XXXXXXXXX [AUTO]”.
  2. Type a DESCRIPTION. Add BUY PRICE and SELL PRICE when they are shown, then the visible custom fields. Prices show a `0.00` placeholder while focused.
  3. Press Enter to add the row to the list on the right. The button hint is “Press Enter to create...”.
  4. Repeat for more products. Click Save Products.
  5. Check-in opens next (WF-001), unless this was the single mobile-transfer add.
- **Options and limits:** AUTO assigns `CSN-` plus nine digits. An empty description is saved as the product number. Empty prices stay 0. A non-numeric or negative price highlights the box and stops the add. A blank manual number shows the placeholder “No Poduct Number!” (spelled that way). Staged quantity for the following check-in is 1. Existing numbers are skipped and are not updated.
- **Result:** New numbers are created. Unless this is the mobile single add, the next page is check-in, or the open transfer when the user came from one. The mobile single add returns the new product to the parent and does not open check-in. A create activity is recorded.
- **Troubleshooting:** “No Poduct Number!” on a blank manual number. “Product number already exists” or “Could not verify product number”. If every typed number already exists, Save Products does not open check-in.
- **Related:** PRD-011, PED-011, PED-013, WF-001, WF-013
- **Confidence:** Confirmed

### PED-011 — Photo while creating
- **Availability:** Current
- **Access:** Add Products, on the thumbnail for the product being typed. A new add session clears temporary images.
- **Purpose:** Attach a photo that is copied onto the new product numbers.
- **Open:** The thumbnail on Add Products.
- **Steps:**
  1. Click the thumbnail and choose a file.
  2. The thumbnail updates. Its title becomes “Change image”.
  3. Add the product row and click Save Products.
- **Options and limits:** The upload does not show a file type or size message. Products that were skipped because the number already exists do not get this photo from this step.
- **Result:** The photo is copied onto each new product number when save succeeds.
- **Troubleshooting:** Choosing no file leaves the placeholder.
- **Related:** PED-010, PED-002, WF-001
- **Confidence:** Confirmed

### PED-012 — Import a CSV (shared rules)
- **Availability:** Current
- **Access:** Import from file, from Add Products (“import file”) or from the product selector. Read-only users cannot open it. These rules apply before create-import and before a movement import.
- **Purpose:** Upload a CSV and match its columns.
- **Open:** Import from file.
- **Steps:**
  1. Choose a CSV and upload it.
  2. When the file is accepted, the instruction changes to “Drag from left to right to Match the fields.”
  3. Drag each file column onto a field on the right. Click a field to clear that match.
  4. Continue with PED-013 or PED-014.
- **Options and limits:** The file must be under 250 KB, UTF-8, comma-separated, with at most 100 columns. The first non-blank row is the header and is never a product. Quoted commas are supported. At least a Product Number must be matched before a create upload can continue. The sample link on a create import is a products sample file. A semicolon file is rejected.
- **Result:** A valid file is held for column matching. Nothing is written to the catalog until the matching step is confirmed.
- **Troubleshooting:** “This file is empty.” “This file is too large. Use a CSV smaller than 250 KB.” “This file is not a CSV. Save it as a comma-separated CSV and try again.” “This file is not valid UTF-8. Save it as CSV UTF-8 and try again.” “This file uses semicolons between columns. Save it as a comma-separated CSV and try again.” “This file has more than 100 columns. Remove the extra columns and try again.” “Row {n} could not be read. Check the quotes and try again.” “This file has no products.” “You must select at least a Product Number to upload.” “This file could not be read. Save it as CSV UTF-8 and try again.” “The column matching could not be read. Match the fields again.”
- **Related:** PED-013, PED-014, WF-007, WF-008
- **Confidence:** Confirmed

### PED-013 — Import to create products
- **Availability:** Current
- **Access:** Import from file in create mode, from Add Products. Sample header names are examples: Product Number, Product Name, Buy Price, Sell Price, Manufacturer, Supplier. The importer uses the columns you drop, not those header names.
- **Purpose:** Create new products from a CSV and stage quantities for check-in. Existing products are not updated.
- **Open:** Import from Add Products.
- **Steps:**
  1. Upload a CSV that passes PED-012.
  2. Drag columns onto Product Number, Description, Buy Price and Sell Price when those are shown, each custom field, Quantity, Expiration when expirations are on, and Location number or Location name unless you are returning to a transfer.
  3. Quantity’s tip is “You can include a quantity column to use during Check In”. Location’s tip is “You can include a location column to check these products into those locations.” Expiration’s tip is “A date like 2026-12-31 (year-month-day).”
  4. Click Next. If some numbers already exist, review the notice and click Continue.
  5. Check-in opens (WF-001), or the open transfer when you came from one.
- **Options and limits:** Unmapped product number becomes `CSN-` plus nine digits. Unmapped description becomes the product number. Unmapped prices stay 0. Unmapped quantity stays 1. Unmapped location stays All Locations. Length limit is 255 for product number, description, and each custom field. Manufacturer and Supplier import only when those file columns are dropped onto custom fields. Presets are not enforced. Buy and sell slots appear on a standard inventory account when prices are shown. Existing products keep their description, price, and custom fields. Their quantity is staged for check-in. Expirations are saved only for new numbers.
- **Result:** New product numbers are created. The notice says “Existing products keep their description, price, and custom fields. Their quantity is staged for check-in. New products are created from this file.” The summary line is “1 product already exists” or “{count} products already exist”.
- **Troubleshooting:** “Row {n}: Buy Price must be a number such as 12.50.” The sell-price sentence uses the same pattern. “Row {n}: Quantity must be a whole number such as 1 or 1.00.” “Row {n}: Expiration must be a date such as 2026-12-31.” “Product number "{n}" is used on {count} rows.” “Row {n}: Product number is longer than 255 characters.” The description and custom-field length sentences use the same 255-character pattern. “Row {n} has {found} columns and the header has {expected}.” “The file or column matching changed. Review the import and try again.”
- **Related:** PED-012, PED-005, PED-010, WF-001, WF-007
- **Confidence:** Confirmed

### PED-014 — Import a list into check-in, check-out, or transfer
- **Availability:** Current
- **Access:** Import from file with create turned off, from “Import From File” or “OR Import from File with Locations”, before the movement’s destination selection is finished. This mode does not insert products.
- **Purpose:** Stage rows for a movement. Stock changes later, on the host page.
- **Open:** Import from check-in, check-out, or transfer.
- **Steps:**
  1. Upload a CSV that passes PED-012. Sample shapes are product number and quantity; product number, quantity, and location when a location column is required; and product number, quantity, FROM, and TO for a transfer.
  2. Match the identifier. On a transfer, open “Choose the field that identifies each product” and pick Product Number, Description, or a custom field. Match Quantity. Match Location number, or FROM and TO, when those slots are showing. Location name can be chosen with “Choose how locations are identified”.
  3. Click Next.
- **Options and limits:** Quantity is required. A non-transfer row whose column count does not match the header fails the file. A transfer row with a different column count is skipped. A repeated identifier on a transfer keeps the later quantity. No product rows are inserted. Stock is changed later by the host page, and those paths are not the same (WF-008).
- **Result:** The movement receives the imported lines. A transfer returns to Transfer, or to the mobile transfer page on a phone.
- **Troubleshooting:** “The selected field must be numeric!” when a non-transfer quantity column is not numeric. Transfer skips: “Row {n}: {field} is blank.” “Row {n}: Quantity must be a whole number such as 1 or 1.00.” “Row {n}: Quantity must be a whole number greater than 0.” “Row {n}: this row has {found} columns and the header has {expected}, so it was skipped.” “Row {n}: {field} "{value}" was already on {earlier}. The quantity from row {n} was used.” Location names that do not match show the location error from the lookup.
- **Related:** PED-012, PED-016, XFR-005, WF-008
- **Confidence:** Confirmed

### PED-015 — Print barcode labels
- **Availability:** Current
- **Access:** Print Barcode Labels, from the product editor, from the product-list barcode image, or after select-all. The header title is “Print Barcode Labels”.
- **Purpose:** Preview Code 128 labels and print them from the browser.
- **Open:** Print Barcodes.
- **Steps:**
  1. Open the page for one product or for the selected list.
  2. Choose a label stock. The first choice is already selected: `30252 (1-1/8" × 3-1/2")`.
  3. Click **PREVIEW & PRINT**. The page builds a Code 128 barcode for each product.
  4. Use the browser print dialog on the preview. The page recommends a DYMO LabelWriter 450.
- **Options and limits:** Stocks: `30252 (1-1/8" × 3-1/2")`, `30336 (1" × 2-1/8")`, `30334 (2-1/4" × 1-1/4")`, `30330 (3/4" × 2")`. An unknown stock falls back to 30252. There is no custom layout. A missing name is printed as “UNTITLED”. A comma in a product number clears the shared name, and each name is then looked up.
- **Result:** One label per product number, with a Code 128 symbol and the product name or “UNTITLED”.
- **Troubleshooting:** An empty product list returns without drawing labels. There is no extra alert.
- **Related:** PRD-011, PED-001, PED-009
- **Confidence:** Confirmed

### PED-016 — Product selector
- **Availability:** Current
- **Access:** The selector used by Start for check-in, check-out, and transfer. Read-only users cannot open it. Scanning and the inventory write after you continue were not fully traced on this page. That write is XFR-006.
- **Purpose:** Pick a location, then search, add products, or import a list.
- **Open:** Check In, Check Out, or Transfer from Start.
- **Steps:**
  1. Check In: title “Check In”, subtitle “Add Products to a Location”, instruction “Please select a Check In Location.” The location starts at the default check-in location.
  2. Check Out: title “Check Out”, subtitle “Remove Products from a Location”, starting at the default check-out location.
  3. Transfer: title “Transfer”, subtitle “Move Products between Location”. First “Please select a Source Location for the Transfer.” Then “Please select a Destination Location for the Transfer.”
  4. After the location is set, use “Search or scan...”, “+ New Products”, “Import From File”, or “OR Import from File with Locations”.
- **Options and limits:** “+ New Products” opens the create path. “Import From File” opens import without creating products. “OR Import from File with Locations” requires a location column. The same source and destination on a transfer is refused. Do not treat the scan matcher on this page as confirmed. Those steps belong to XFR-006 and are Uncertain here.
- **Result:** The chosen location is stored for the movement. New Products and Import leave this page.
- **Troubleshooting:** “The Source can't be the Destination!” The page asks for a destination again.
- **Related:** PED-010, PED-014, DEF-001, XFR-006, WF-002, WF-003, WF-004, WF-008
- **Confidence:** Confirmed for titles and location rules. Uncertain for the scan script and the write after continue.

## ACT — Activity history

There is no undo on activity history or activity details. Account and user administration events are not included in this list.

On a records account, Inventory is labeled **Assignments**, Check In is **Assign**, Check Out is **Deallocate**, and Products is **Records**. Transfer stays **Transfer**. Create, Edit, Delete, and Adjust are not renamed. Location phrases stay the same.

Standard inventory phrases: created new products, deleted products, edited products, checked in products, checked out products, transferred products, adjusted a product quantity, created a new location, deleted a location, renamed a location.

Records phrases: created new records, deleted records, edited records, assigned records, deallocated records, transferred records, adjusted a record.

### ACT-001 — Activity history
- **Availability:** Current
- **Access:** Any signed-in user, including Read-only. The header activity icon, the menu link **Activity**, and **View Activity History**.
- **Purpose:** Read the newest inventory, product, and location activity.
- **Open:** Activity History.
- **Steps:**
  1. Open Activity History.
  2. The first load uses **All Activity**, user **All**, location **All Locations**, the last **90** days through today, an empty keyword box, and **15** rows. Do not say the default range is 365 days.
  3. Read each row: avatar, comment, “{You|name} {description}”, time, product count, and location icons. Your stored first name is shown as **You**.
  4. Click the row background to open one activity (ACT-005). Click a product name or a location name to open that editor. Those clicks do not open details.
  5. Click **Show More...** to add 15 to the window. The page reloads a longer list from the newest row. It does not page forward.
- **Options and limits:** Changing user, date, location, or category does not reset the 15-row window. With a user filter on, timestamps are the stored time and are not shifted by the account time zone. With no user filter, timestamps are shifted by the account time zone. A product activity with no content lines is skipped. When at least one row is drawn, **Show More...** stays even if every matching row is already visible. There is no undo.
- **Result:** Newest first. Empty list shows **No Activity...** and **details will appear here**, and hides **Show More...**.
- **Troubleshooting:** A missing profile image uses a generic avatar. If the name lookup for a user filter fails, the list loads with no user filter.
- **Related:** ACT-002, ACT-003, ACT-004, ACT-005, ACT-006, ACT-007, WF-011
- **Confidence:** Confirmed

### ACT-002 — Filter by type
- **Availability:** Current
- **Access:** The left rail on Activity History.
- **Purpose:** Limit the list by activity group. Check In and Check Out are not pure type filters.
- **Open:** A group or a child button. The active button turns green.
- **Steps:**
  1. Click a group or a child button. The list reloads.
  2. Use **Check In** or **Check Out** together with a location when you need transfers. With **All Locations**, transfers are removed from both of those buttons.
- **Options and limits:**
  - **All Activity** includes creates, check-ins, deletes, check-outs, transfers, edits, location create, location delete, location rename, and quantity adjusts.
  - **Inventory** includes check-in, check-out, transfer, and adjust.
  - **Check In** keeps a native check-in. It keeps an adjust when the quantity did not go down, when the quantities are equal, or when the comment does not parse as a decrease. It keeps a transfer only when a location is selected, a destination is inside that location or its children, and the source is not.
  - **Check Out** keeps a native check-out. It keeps an adjust only when the old quantity is greater than the new quantity. The comment must match `Quantity for '…' was adjusted from {old} to {new}.` If it does not parse and the first content quantity is greater than 0, the adjust is treated as a check-in. It keeps a transfer only when a location is selected, the source is in that location or its children, and the destination is not. A move that stays inside the filtered tree is excluded.
  - **Transfer**, **Adjust**, **Products** (Create, Edit, Delete), and **Location** (Create, Edit, Delete) filter those types.
  - Under Check In or Check Out, matching transfer rows are drawn with check-in or check-out icons, and the comment can show a transfer badge. Adjust rows that map onto check-in or check-out can show a quantity-adjust badge. The quantity shown is the absolute change. The badges are display-only. The stored comment is unchanged. Activity details does not add these badges.
- **Result:** The list follows those rules. Default is **All Activity**.
- **Troubleshooting:** None on screen.
- **Related:** ACT-001, ACT-003, ACT-004, ACT-007
- **Confidence:** Confirmed

### ACT-003 — Date, user, location, and keyword
- **Availability:** Current
- **Access:** The top of Activity History. Date control at the top right. User chips at the top left. Location selector beside them. Keyword placeholder “search by keyword...”.
- **Purpose:** Narrow activity by date, person, location, and keyword.
- **Open:** Those controls.
- **Steps:**
  1. Open the date control and pick a preset or two dates. Apply posts the range. The label looks like `MMMM D, YYYY - MMMM D, YYYY`.
  2. Click **All**, **Me**, or another person. The selected chip is full opacity with a green border.
  3. Pick a location, or leave **All Locations**.
  4. Type a keyword and press Enter, or click the search image. The search image does not have its own action. The reload still uses the text box.
- **Options and limits:**
  - Date presets: All Time (1 Jan 2011 through tomorrow), Today, Yesterday, Last 7 Days (today minus 6 days through today), Last 30 Days (today minus 29 days through today), This Month. The picker does not allow a date after today, so All Time’s tomorrow and a future day in This Month can be clamped. The end day is included. If the saved dates are missing, or a date cannot be read, the range is the last 90 days. Do not say the default is 365 days.
  - Users: **All** does not filter by person. **Me** is the signed-in user. Other chips are people who have logged in and are not Read-only. The match is the stored first name, not a separate user identity. Two people with the same first name cannot be separated. A renamed person no longer matches older rows. Read-only people are omitted from the chips. Their older rows can still appear under the name that was stored.
  - Location: All Locations, or one location and its children. Location create, edit, and delete match that location. The destination is not used for those three types.
  - Keyword: empty skips the keyword. A term matches comment, product number, product name, and every custom field. There are no AND or OR operators. A percent sign or underscore in the keyword acts as a wildcard, not as a literal character.
- **Result:** The four filters combine with the type filter. The download header repeats the date range, the selected person’s first name, and `Comment : {term}` when the keyword is not blank. The keyword does not reset the Show More window.
- **Troubleshooting:** A keyword that matches nothing uses the empty state in ACT-001. If the user-name lookup fails, the page loads with no user filter.
- **Related:** ACT-001, ACT-002, ACT-004
- **Confidence:** Confirmed

### ACT-004 — Activity row hover and CSV
- **Availability:** Current
- **Access:** The product count on a row, and the download image to the left of the date range. Tooltip: “Download spreadsheet file (.csv)”.
- **Purpose:** See products on a row, or download the filtered activities.
- **Open:** Hover the count, or click the download image.
- **Steps:**
  1. Hover the product count. The panel lists product name, number, and quantity.
  2. Click a product name in the hover to open Product Editor. Click a location in the hover to open Location Editor. Those clicks do not open Activity Details.
  3. Leave **Readable Format** checked, or clear it. Click the download image. The file uses the current filters and ignores the 15-row cap.
- **Options and limits:** Count text is `{n} Product` or `{n} Products`. When the row has quantities, it adds `({qty} Item)` or `({qty} Items)`. Create and edit omit the quantity. Check-in can say “to {location}”. Check-out can say “from {location}”. Transfer says “from {a} to {b}”. Adjust says “at {location}”. The hover lists at most 11 product lines. Further products are still counted. **Readable Format** is checked by default. Tooltip: “If you need to manipulate your data more easily you can uncheck this box for a more uniform file.” Checked writes one summary line per activity, then product lines whose first columns are blank. Unchecked repeats date, user, activity, source, destination, and comment on every product line. Columns, exactly: Date, User, Activity, Source, Destination, Comments, Product Number, Description, Quantity, FROM, TO, Buy Price, Sell Price, Old Quantity, New Quantity, Qty. Diff., Cost Diff. The last four headers are present and are not filled. Commas in user, description, comment, product number, and product name become underscores. Location paths in FROM and TO are not changed that way. The filename is `CyberStockroom - {category label} Report`, plus ` at {location name}` when a location is selected and the name is not `[DELETED]`, cut at 200 characters, then `.csv`.
- **Result:** A CSV of the filtered activities, including rows past the 15 on screen. If product details cannot be read, the chip reads `{n} Product(s) [DELETED]` and the hover lists the product numbers. An empty product name in the CSV is `[DELETED]`.
- **Troubleshooting:** None is shown for a download error. The file is still offered when the page can build it.
- **Related:** ACT-001, ACT-002, ACT-003, ACT-005
- **Confidence:** Confirmed

### ACT-005 — One activity
- **Availability:** Current
- **Access:** Click a history row. It opens in a window. It is not in the main menu.
- **Purpose:** Read every product on one activity and download that activity.
- **Open:** The row background, not a product or location name inside it.
- **Steps:**
  1. Click the row.
  2. Read the user (**You** when the stored first name matches), the description, the time, the comment, the locations, and the product table.
  3. Click a product name to open Product Editor in the parent window. Click a location row to open Location Editor the same way.
  4. Click the download image to download this activity.
- **Options and limits:** Product table columns are Product, Number, and Qty, except create and edit, which omit Qty. Qty is the larger of quantity in and quantity out. Extra columns appear only when both header locations are All Locations: check-in **To**, check-out **From**, adjust **Location**, transfer **From** and **To**. The details file always uses grouped rows and All Activity. There is no comment edit and no undo. The check-in and check-out badges from the list are not added here. The filename is `CyberStockroom - {description} - {MMM d yyyy}`, cut at 200 characters, plus `.csv`.
- **Result:** The full product list, with no 11-line cap.
- **Troubleshooting:** Missing or unknown id shows **Activity not found** and **This activity may have been removed or is not available on this account.** A download of a missing id does not return a file. A blank product name displays `[DELETED]`.
- **Related:** ACT-001, ACT-004, ACT-007
- **Confidence:** Confirmed

### ACT-006 — Header activity popup
- **Availability:** Current
- **Access:** The activity icon in the header, including on Activity History, Expirations, Kitting, and the insights report. Any signed-in user.
- **Purpose:** Show up to five recent inventory rows.
- **Open:** The activity icon.
- **Steps:**
  1. Open the activity icon.
  2. Read up to 5 rows. Click **View Activity History**, or the icon itself, to open Activity History.
- **Options and limits:** The popup prefers recent check-ins, check-outs, transfers, and adjusts. If that list is empty, a backup list is used and does not apply the Check In / Check Out direction rules. Rows that are not those four types are skipped. A row does not open the activity. Your own comment is suffixed ` - You`. Another person’s comment is not labeled with their name.
- **Result:** Avatar, description, comment, and time.
- **Troubleshooting:** A missing profile image uses a generic avatar. There is no sentence.
- **Related:** ACT-001, ACT-002, ACT-007
- **Confidence:** Confirmed

### ACT-007 — What is stored
- **Availability:** Current
- **Access:** There is no control on Activity History that writes these rows. They are created by checking in, checking out, transferring, adjusting a quantity, or creating, renaming, or deleting a location. The expiration replacement page sends a comment and then opens Activity History. What that service writes is **Uncertain** (EXP-002).
- **Purpose:** Say which phrases appear, and that zero-quantity lines are not stored.
- **Open:** Finish one of those actions, then open Activity History.
- **Steps:**
  1. Finish the action on its own page.
  2. Open Activity History. The new row uses the phrase for the account kind listed at the top of this section.
- **Options and limits:** A content line is stored only when the product number is not empty and the quantity is greater than 0. Zero-quantity lines are dropped. There is no undo and no way to delete an activity from this screen. An unrecognized account can show a short activity label that includes a number, or the text `[ERROR-ACC1 - unkown account type]`. Do not describe administration events as rows in this list.
- **Result:** A new activity the history page can show when the type is one of the product, inventory, location, or adjust types and the row has the content lines that type uses.
- **Troubleshooting:** A line that fails while the activity is recorded is skipped. There is no sentence.
- **Related:** ACT-001, ACT-002, ACT-005, WF-011
- **Confidence:** Confirmed for the phrases and the content-line rule. Uncertain for rows written by expiration replacement.

## EXP — Expirations

Expirations must be on for this user (DSP-004). Opening Expirations while they are off goes to the expirations area of Settings. A Read-only user gets the list without **manage**. The yellow window is DSP-005.

### EXP-001 — Expiration list
- **Availability:** Current
- **Access:** The Expirations icon or the menu link **Expirations**, when expirations are on. Page heading **Product Expirations**.
- **Purpose:** See products that are expired or coming due, and open the product.
- **Open:** Expirations.
- **Steps:**
  1. Open Expirations.
  2. Read the chips **{n} Expiring Soon** and **{n} Expired**.
  3. Read the list. Each row is `{product number} - {description}` plus a status. Click the row to open Product Editor.
  4. Type in the box (placeholder “search...”). Each keystroke reloads the first page, up to 100 rows. On the editable page, **manage** opens EXP-002.
- **Options and limits:** Colors use the date only, with the time set to midnight. A date before today is red with white text: `expired ({yyyy-mm-dd})`. If the window is greater than 0 and the date is on or before today plus that many days, the row is yellow: `will expire in {n} days ({date})`. Otherwise the row is grey: `will expire on {date}`. Stored window 0 hides the yellow treatment and no row is yellow. The chips use the current clock, so a product expiring later today can be counted one way and listed another. The chips can count more products than the list shows. The list shows the first 100 rows. Products past those 100 are counted and not listed. Which fields the search matches is **Uncertain**.
- **Result:** A row opens the product editor.
- **Troubleshooting:** A failed list request does not show a sentence. Duplicate product numbers in one response are skipped.
- **Related:** EXP-002, DSP-004, DSP-005, PED-005, WF-011
- **Confidence:** Confirmed for the page. Uncertain for which fields search matches.

### EXP-002 — Replace or clone an expiring product
- **Availability:** Current
- **Access:** **manage** on a row of the editable Expirations page. Read-only users do not get this button. Modal title **Manage this product's expirations**.
- **Purpose:** Start a replace or clone with a new date and a new product number. What each choice does to stock is **Uncertain**.
- **Open:** **manage**.
- **Steps:**
  1. Click **manage**. The title shows the description, product number, and date.
  2. Pick **New Expiration Date**. Pick **New Product Number**, or check **Auto**.
  3. Leave **Replace and Delete** selected, or choose **Replace only**, **Clone and Delete**, **Clone and Check-out**, or **Clone only**.
  4. Click the green button. **Cancel** closes the window.
- **Options and limits:** The default is **Replace and Delete**. The button label starts as **Replace** and updates after you click a radio. The checkboxes under the radios are a legend. They are not choices you can toggle. **Auto** fills `[Automatic Product Number]`. A past date shows “This date has already passed!” and turns the box red, but save does not repeat that check. Save stops only when the date box is empty or the product number is empty or already used. Do not state what each radio does to quantities, locations, or the old product.
- **Result:** On success the browser goes to Activity History. The stock effect is **Uncertain**.
- **Troubleshooting:** “You must select an expiration date.” “This date has already passed!” “You must select a product number.” “That product number already exists!” A failed existence check is treated as “does not exist,” and save continues. A failed replacement does not show a sentence. The window has already faded out.
- **Related:** EXP-001, ACT-001, DSP-004, DSP-005, WF-011
- **Confidence:** Confirmed for the wizard. Uncertain for what each action does to stock.

## KIT — Kitting

Kitting appears in the Products menu only when it is already enabled for this user. Settings does not include a control that turns it on. Opening Kitting while it is off goes to the kitting area of Settings. How the flag is turned on was not found in Settings. There is no build and no break. There is no Kitting link in the collapsed menu. A Read-only kitting page is not in this product as a working screen. Do not use a **manage** button on a kit. It does not open a working action.

### KIT-001 — Kit list, create, delete, search
- **Availability:** Restricted
- **Access:** The kitting icon, only when kitting is already on. Heading **Product Kits & Assemblies**.
- **Purpose:** View kits, create one, search, or delete one. Whether the service stores the kit is **Uncertain**.
- **Open:** Kitting.
- **Steps:**
  1. Open Kitting. Read the chip **{n} Kits**.
  2. Click a kit name to expand **{n} Products included**. Click again to collapse.
  3. Click **+ NEW KIT**. The prompt is **New Kit Name:**. Accept to send the name.
  4. Type in the box (placeholder “search...”). Each keystroke reloads the first page, up to 100 kits.
  5. Click **Delete Kit**. There is no confirm.
- **Options and limits:** There is no duplicate check and no trimming of the name. Cancel on the name prompt still sends a request, and the name sent is the word `null`. Do not rely on that as a way to create a kit, and do not state that it inserts one. The chip count can be larger than the 100 rows on screen. Create and delete refresh the list with an empty search even if the box still has text. Which fields search matches is **Uncertain**. A quote in the kit name can break the request.
- **Result:** The list refreshes after a successful create or delete. Whether a new kit is stored is **Uncertain**.
- **Troubleshooting:** Create, delete, and list errors are not shown. There is no sentence.
- **Related:** KIT-002, WF-012
- **Confidence:** Confirmed for the page requests. Uncertain for whether a kit is stored and for search matching.

### KIT-002 — Kit components
- **Availability:** Restricted
- **Access:** Inside an expanded kit, same gate as KIT-001.
- **Purpose:** Try to add a product to a kit. Do not rely on editing a quantity that is already in the kit, or on remove deleting only the clicked line.
- **Open:** An expanded kit.
- **Steps:**
  1. Expand a kit. Each line is `{qty} x {description} ({product number})`.
  2. Click **+ Add New**. The title is **Add Item to Kit :** plus the kit name. Search products. The search shows 10 at a time. Click a row, or press Enter to take the first hit. The quantity prompt is **Please enter the new quantity for Product :** followed by the product number and **in Kit:** followed by the kit name.
  3. Do not use the green quantity on a product already in the kit as a working edit. The page sends the old quantity, not the number you typed.
  4. Do not use **x** as a reliable remove of only that line. The confirm is “Are you sure you want to remove this item from the kit?” The request drops the clicked line and also drops every other component with the same quantity.
- **Options and limits:** Cancel on the quantity prompt, or a value of 0 or less, sends nothing. Non-numeric text can still be sent. There is no build-into-inventory action. Persistence of the kit is **Uncertain**.
- **Result:** The page tries to reload the kit list. Do not treat quantity edit or remove as a reliable editor.
- **Troubleshooting:** The confirm is the only delete check. A failed save shows no sentence.
- **Related:** KIT-001, WF-012
- **Confidence:** Confirmed

## SRCH — Header search

### SRCH-001 — Header search
- **Availability:** Current
- **Access:** The toolbar box on signed-in pages, including Activity, Expirations, Kitting, and the insights report. Read-only users see it. The create-product row is hidden for Read-only users.
- **Purpose:** Jump to a product or a location, open the product list, or start a new product when nothing matches.
- **Open:** The header search. The placeholder is empty.
- **Steps:**
  1. Type in the header box. Suggestions can start immediately. There are no search operators.
  2. Click a **Products** row to open Product Editor for that product number. Click a **Locations** row to open Location Editor for that location.
  3. Press Enter to open Products with that text added to the product search (PRD-006).
  4. If the suggestion list is empty, the term is not empty, and Add Products is available, one row reads **Create New Product {term}**. Choosing it opens Add Products with the description set to the term.
- **Options and limits:** Up to 10 suggestions. A newer response, or a term that no longer matches the box, is discarded. Do not invent categories other than Products and Locations. Which fields are matched is **Uncertain**. An error returns an empty list and does not show **Create New Product**. An empty term does not show that row.
- **Result:** Product editor, location editor, the product list, or Add Products with the description filled in.
- **Troubleshooting:** If suggestions are unavailable, Enter does nothing and does not open Products.
- **Related:** PRD-006, PRD-007, WF-013
- **Confidence:** Confirmed for the page. Uncertain for match fields and for any category other than Products and Locations.

## RPT — Reports

### RPT-001 — Download a product report
- **Availability:** Current
- **Access:** On Products, the download image tooltip is **Download Product Report**. Any signed-in user. This page has no separate Read-only block. The map quantity file is a different download (MAP-032).
- **Purpose:** Download a product CSV for a location, with optional zero quantities, sub-locations, and columns.
- **Open:** The download icon on Products. Heading **Download Product Report**. Button **Download File**.
- **Steps:**
  1. On Products, click the download icon.
  2. Choose a location, or leave all locations.
  3. Set **Include Products with 0 Quantity** and **Include Products in Sub-Locations**, and the field checkboxes.
  4. Click **Download File**.
- **Options and limits:**
  - Location starts from the product list’s location. **Include Products in Sub-Locations** is hidden when the location is all locations.
  - **Include Products with 0 Quantity** starts unchecked. When checked, products that are not already in the positive-quantity result are appended with quantity 0. It is also forced on when the positive-quantity query returns zero rows.
  - **Include Products in Sub-Locations** starts unchecked. When checked and the location is not all locations, the file includes that location and its children.
  - **Product Number** is checked and cannot be cleared.
  - **Description** starts checked.
  - **Quantity** starts checked. Unchecking it disables **breakdown by location** in the browser.
  - **breakdown by location** starts checked and adds **Location Path** and **Location Name**.
  - **Buy Price**, **Cost Value**, and **Sell Price** start checked. Headers include the account currency. Cost value is quantity times buy price, rounded half away from zero to 2 decimals. If Cost Value is on and Buy Price or Quantity is off, those values are still used to fill the cost column and then those columns are removed.
  - Each custom field starts checked. A comma in the field name becomes an underscore in the header.
  - **Product Image** starts unchecked and adds **Image URL**.
  - The product-list search is not included. Only quantities greater than 0 are in the first pass.
  - The filename is the readable location path plus `  - [DATE : {long date}]`, cut at 200 characters, or `ALL LOCATIONS  - [DATE : {long date}]` when the path is empty, then `.csv`.
- **Result:** A CSV download. Every download also refreshes the readable location paths stored for the account. Do not say the download leaves those paths unchanged.
- **Troubleshooting:** A download failure shows no sentence.
- **Related:** PRD-006, WF-013, ACT-003
- **Confidence:** Confirmed

## Workflows

These are the cross-page sequences. Use the feature entries for the exact labels, limits, and errors. Where a service outside the website finishes the stock change, the outcome stays **Uncertain**.

### WF-001 — Create products and check them in
- **Availability:** Current
- **Access:** Signed in, not Read-only. Prices are disabled on a records account.
- **Purpose:** Add catalog products and optionally place them.
- **Open:** Product list **Add**, header **Create New Product** when search has no matches, or Start **Create**.
- **Steps:**
  1. On Add Products, leave **AUTO** on or type a product number. Type a description. An empty description becomes the product number. Optional: buy price, sell price, and custom fields. Optional: a photo (PED-011). Save (PED-010).
  2. Or upload a CSV and match at least a product number (PED-012, PED-013). Existing product numbers are not updated. Their quantity is only staged for check-in.
  3. The check-in page opens (XFR-007), unless this was the single add from a mobile transfer. That path does not check in.
  4. Click a location. The suggested location is the default check-in location (DEF-001). Enter whole-number quantities. At least one line must be 1 or more. Save. Stock is added and a check-in is recorded.
  5. Click **Skip** instead to leave the products in the catalog with no placed stock.
  6. If every imported line already names a location, the map stays hidden and each line checks into that location.
  7. If you came from an open transfer, **Continue** does not change stock yet. Save the transfer later (XFR-001).
- **Options and limits:** See PED-010, PED-012, PED-013, and XFR-007.
- **Result:** New catalog rows. Stock only if check-in was saved.
- **Troubleshooting:** The feature entries’ messages.
- **Related:** PRD-011, SRCH-001, XFR-006, PED-010, PED-011, PED-012, PED-013, XFR-007, DEF-001, XFR-001
- **Confidence:** Confirmed

### WF-002 — Check in
- **Availability:** Current
- **Access:** Signed in, not Read-only. The menu item is hidden when the account has no products. Quick Scan stays available.
- **Purpose:** Add quantity. Transfer and Start do not use the same math.
- **Open:** The map (MAP-020), Start (XFR-006), or the mobile menu (XFR-008, XFR-012).
- **Steps:**
  1. On Transfer, the left list is the catalog, with an infinity mark. The source is All Locations. Click a product to move 1. Type a quantity of at least 1 when the badge asks. There is no **Check In Everything** (XFR-001).
  2. Click **Check In**. The chosen quantities are added at the destination. One check-in activity is written. You can skip the comment. The comment is collected before the stock write.
  3. On Start, the same button adds quantity, but the comment box appears only after the stock is already written. If the location cannot be read, Start saves nothing.
  4. On a phone, finishing from mobile home clears the in-progress process (XFR-012).
- **Options and limits:** Do not merge Transfer and Start.
- **Result:** Transfer adds at the destination. Start adds at the location.
- **Troubleshooting:** XFR-001 and XFR-006.
- **Related:** MAP-020, XFR-006, XFR-008, XFR-012, XFR-001, DEF-001
- **Confidence:** Confirmed

### WF-003 — Check out
- **Availability:** Current
- **Access:** Signed in, not Read-only.
- **Purpose:** Remove stock. Transfer sets the source to what you leave behind. Start subtracts and stops at 0.
- **Open:** The map (MAP-021) or Start.
- **Steps:**
  1. On the map, drag a full location to **Check out**, or open check-out so the destination is All Locations.
  2. On Transfer, the left list is stock at the source. Click to move 1, up to what is on hand. Drag a row to move the rest. **Check-Out Everything** loads the location in pages of 500 and hides while a map-filter badge is on (XFR-002).
  3. Click **Check Out**. Source stock becomes the quantity you left behind. The activity stores the quantity that moved.
  4. On Start, check-out subtracts and stops at 0 (XFR-006).
- **Options and limits:** If both check-in and check-out are requested, check-out wins (XFR-001).
- **Result:** Transfer overwrites the source to the remainder. Start subtracts.
- **Troubleshooting:** XFR-002 and XFR-006.
- **Related:** MAP-021, XFR-002, XFR-006, DEF-002
- **Confidence:** Confirmed

### WF-004 — Transfer between two locations
- **Availability:** Current
- **Access:** Signed in, not Read-only. The two locations must be different.
- **Purpose:** Move stock between locations. There is no Adjust button on Transfer.
- **Open:** The map (MAP-022), Start, or the phone (XFR-009, XFR-008).
- **Steps:**
  1. On the map, drop a full location or a product row onto a different location. The same location, or All Locations, is ignored. A wide screen opens Transfer in a popup. A narrow screen opens the mobile transfer page.
  2. When the dragged quantity is exactly 1, a comment box says **Moving this item.** Saving that path sets the source quantity of that product to 0 (MAP-023). That is not “move 1 and keep the rest.”
  3. Otherwise, on Transfer, click to move 1 or drag to move what remains. Click **Transfer**. The destination becomes its current quantity plus the amount moved. The source becomes the quantity you left behind (XFR-003).
  4. On Start, pick a source and then a destination. The same place shows “The Source can't be the Destination!” Start subtracts from the source and adds to the destination (XFR-006).
  5. On a phone, pick source and destination. The **default** badge opens the Settings location picker (DEF-001, DEF-002). Save uses the Transfer rules (XFR-008).
- **Options and limits:** Change a quantity in place from the product map (MAP-026) or the product list (PRD-010). That is XFR-004.
- **Result:** Depends on the path above.
- **Troubleshooting:** XFR-003, XFR-006, and MAP-023.
- **Related:** MAP-022, MAP-023, XFR-003, XFR-006, XFR-009, XFR-008, XFR-004, DEF-001, DEF-002
- **Confidence:** Confirmed

### WF-005 — Quick Scan and the location kiosk
- **Availability:** Current
- **Access:** Signed in, not Read-only.
- **Purpose:** Scan into a check-in, check-out, or transfer, or lock one location as a kiosk.
- **Open:** **Quick Scan** (XFR-011), or **Checkin Kiosk** / **Checkout Kiosk** in the location editor (MAP-041).
- **Steps:**
  1. Scan products. Each scan adds the product or adds 1. The placeholder is “ready to scan...”.
  2. Outside a kiosk, the first location scan becomes the source and the next becomes the destination.
  3. Click save. Source only checks out. Destination only checks in. Both transfer.
- **Options and limits:** A kiosk locks one location. Transfer is not a kiosk mode. Quick Scan does not create a product. Quick Add (XFR-010) creates a catalog product and does not check it in. What the Quick Scan save does to stock is **Uncertain**.
- **Result:** “{N} Transactions completed successfully.” or, on mobile, “Transaction saved”.
- **Troubleshooting:** XFR-011.
- **Related:** XFR-011, MAP-041, XFR-010
- **Confidence:** Confirmed for the page. Uncertain for stock math.

### WF-006 — Move, reparent, delete, or clone a location
- **Availability:** Current
- **Access:** Signed in, not Read-only. The map is locked until you unlock it (MAP-009).
- **Purpose:** Change the map’s locations without using Transfer, except that delete checks stock out.
- **Open:** The map.
- **Steps:**
  1. Click the floating **+**, a **+** on a tile, or **Add** inside a 3D stack. Pick a type. Name it (MAP-005, MAP-003). A duplicate name shows “That location name is already in use!”
  2. To move a primary location, unlock the map, then drag the diamond header (MAP-008). Children move with it. Inventory stays on the same locations. There is no resize handle (MAP-011).
  3. To put it under another parent, click the clasp, then click the new parent or empty canvas. Confirm **Move location?** Children stay with it. Empty canvas makes it primary (MAP-010).
  4. To delete, confirm **YES** on “Are your sure you want to DELETE this location?” Stock is checked out, then the location and its sub-locations are deleted (MAP-012). Closing the popup cancels. There is no No button.
  5. To clone the structure, name the copy. **Auto-Rename Sub-Locations** is off unless you turn it on. Confirm. Whether quantities copy is **Uncertain** (MAP-013).
  6. To copy stock, hold Ctrl and drop a full location onto another. Confirm the message that existing items there are cleared first (MAP-014). This is blocked while several locations are selected (MAP-030). What each quantity becomes is **Uncertain**.
  7. Rename, attachments, barcode, and kiosk links are in the location editor (MAP-006, MAP-007, MAP-039, MAP-040, MAP-041).
- **Options and limits:** See those feature entries.
- **Result:** Layout changes are saved for this user. Delete removes the locations. Stock copy and structure-clone quantities are **Uncertain**.
- **Troubleshooting:** The feature entries’ messages.
- **Related:** MAP-003, MAP-005, MAP-006, MAP-007, MAP-008, MAP-009, MAP-010, MAP-011, MAP-012, MAP-013, MAP-014, MAP-030, MAP-039, MAP-040, MAP-041
- **Confidence:** Confirmed for the page. Uncertain for clone quantities and copy stock math.

### WF-007 — Import a CSV to create products
- **Availability:** Current
- **Access:** Signed in, not Read-only.
- **Purpose:** Create products from a CSV and continue to check-in.
- **Open:** Add Products, import file.
- **Steps:**
  1. Upload a CSV under 250 KB, UTF-8, comma-separated, at most 100 columns. The first row is the header (PED-012).
  2. Drag columns onto Product Number and any other fields (PED-013). You must map at least a product number. Sample headers are examples, not required names.
  3. Unmapped quantity stays 1, prices stay 0, and the location stays All Locations. Duplicate numbers in the file are rejected. Existing products keep their description, price, and custom fields.
  4. Continue into check-in (WF-001).
- **Options and limits:** PED-012 and PED-013.
- **Result:** New products, plus staged quantities for check-in.
- **Troubleshooting:** PED-012 and PED-013.
- **Related:** PED-012, PED-013, WF-001
- **Confidence:** Confirmed

### WF-008 — Import a list into a movement
- **Availability:** Current
- **Access:** Signed in, not Read-only. The import button is hidden once the destination selection is filled.
- **Purpose:** Fill check-in, check-out, or transfer from a file without creating products.
- **Open:** **import file** before choosing the destination side (XFR-005, PED-014).
- **Steps:**
  1. Match by product number, description, or a custom field. A value that matches more than one product is skipped.
  2. Check-in keeps the quantity in the file. Check-out and transfer reduce it to what is on hand.
  3. Review the lines. The page stays locked until you save or cancel.
  4. Save uses the host mode (WF-002, WF-003, or WF-004). Cancel writes nothing.
- **Options and limits:** The same file can fill Start. Start then adds or subtracts. That is not the Transfer overwrite (XFR-006).
- **Result:** Stock changes only when the host page is saved.
- **Troubleshooting:** XFR-005 and PED-014.
- **Related:** XFR-005, PED-014, WF-002, WF-003, WF-004, XFR-006
- **Confidence:** Confirmed

### WF-009 — Invite a teammate and accept
- **Availability:** Current
- **Access:** An Admin sends the invite. The form can also be visible to a User. The User is rejected with “Unable to Invite - Try Again?”
- **Purpose:** Add a person and let them set a password.
- **Open:** Settings, **Invite a Team Member**.
- **Steps:**
  1. Enter an email and a role. The unmarked default is ADMIN (TEAM-004).
  2. Send. The mail links to the accept page.
  3. The invited person opens the link, creates a password, and submits (ACC-004). The role is not chosen on that page.
  4. An Admin can later change the role (TEAM-002) or click **DELETE** (TEAM-003).
- **Options and limits:** Inviting an email that already belongs to this account does not change that person’s role.
- **Result:** The person joins with the role the inviter chose.
- **Troubleshooting:** TEAM-004 and ACC-004.
- **Related:** TEAM-004, ACC-004, TEAM-002, TEAM-003
- **Confidence:** Confirmed

### WF-010 — Share a map layout and sync to it
- **Availability:** Current
- **Access:** An Admin turns sharing on. Any signed-in user can sync to a shared layout.
- **Purpose:** Copy positions and stacks, not inventory.
- **Open:** Settings **OPTIONS**, **Share Map Layout** (DSP-001), then the other user’s map gear, **Shared Maps** (MAP-016).
- **Steps:**
  1. Turn **Share Map Layout** on. Products and quantities are not shared.
  2. The other user opens **Shared Maps**.
  3. If none are shared: “No shared maps. Admins can share their maps in the Settings page.”
  4. Pick a person. The warning says the current layout will be lost. Click **Sync**, or **Keep my layout**.
- **Options and limits:** Coordinates, zooms, and vertical or 3D stacks are copied. Inventory is not copied.
- **Result:** The receiving user’s layout is replaced.
- **Troubleshooting:** MAP-016.
- **Related:** DSP-001, MAP-016
- **Confidence:** Confirmed

### WF-011 — Review expirations and replace or clone
- **Availability:** Current
- **Access:** Expirations must be on (DSP-004). The window is DSP-005. Read-only users get the list without **manage**.
- **Purpose:** Review dates and start a replace or clone. Stock results of the radios are **Uncertain**.
- **Open:** **Expirations**.
- **Steps:**
  1. The list shows the first 100 rows. Expired rows are red. Rows inside the window are yellow (EXP-001).
  2. Click a row to open the product editor and change that product’s date (PED-005).
  3. On the editable list, click **manage** (EXP-002). Leave **Replace and Delete** selected, or choose **Replace only**, **Clone and Delete**, **Clone and Check-out**, or **Clone only**.
  4. Set a future date and a product number. A past date warns “This date has already passed!” and does not block save.
  5. Save. The browser goes to activity history (ACT-001).
- **Options and limits:** Do not state what each radio does to stock.
- **Result:** The browser opens Activity History after a successful request. The stock effect is **Uncertain**.
- **Troubleshooting:** EXP-001 and EXP-002.
- **Related:** DSP-004, DSP-005, EXP-001, EXP-002, PED-005, ACT-001
- **Confidence:** Confirmed for the wizard. Uncertain for stock.

### WF-012 — Create and edit a kit
- **Availability:** Restricted
- **Access:** Kitting must already be on. Settings does not turn it on.
- **Purpose:** Create a kit and try to add components. Quantity edit and remove are not reliable.
- **Open:** **Kitting**.
- **Steps:**
  1. Click **+ NEW KIT**, type a name, and confirm (KIT-001). Cancel still sends the name `null`.
  2. Expand the kit. Click **+ Add New**, search for a product, and enter a quantity (KIT-002).
  3. Do not rely on editing a quantity that is already in the kit. The page sends the old quantity. Removing a line also drops every other component with the same quantity.
  4. **Delete Kit** has no confirm.
- **Options and limits:** There is no build and no break. Do not use **manage**. It does not complete a kit action.
- **Result:** The list refreshes when the request succeeds. Whether the kit is stored is **Uncertain**.
- **Troubleshooting:** KIT-001 and KIT-002. Errors are not shown.
- **Related:** KIT-001, KIT-002
- **Confidence:** Confirmed for the page. Uncertain for storage.

### WF-013 — Find a product and change it
- **Availability:** Current
- **Access:** Signed in. Read-only users can search and open the view-only editor. They cannot add, edit, clone, or delete.
- **Purpose:** Find a product and change its fields or its quantity.
- **Open:** The header search.
- **Steps:**
  1. Type in the header search and press Enter (SRCH-001, PRD-006). The product list opens at All Locations. Terms are combined with AND.
  2. Click a product row. The checkbox column does not open the editor (PRD-007).
  3. Change the name, prices, or custom fields (PED-001). The product number cannot be renamed. Presets offer **(none)**, each preset, and **Other (Specify)**.
  4. To change a quantity, use the product map: click a location, type a whole number, press Enter (PED-006, MAP-026). Or, on the product list at a real location, edit the in-stock quantity cell (PRD-010).
  5. **Clone Product** copies fields, not stock (PED-007). **Delete this product** uses the same delete as the grid (PED-008, PRD-011).
  6. The download icon opens the product report (RPT-001). The current search is not included. Every download refreshes location paths for the account.
- **Options and limits:** See those feature entries.
- **Result:** Field edits are saved on the product. Quantity edits follow MAP-026 or PRD-010. Clone does not copy stock.
- **Troubleshooting:** The feature entries’ messages.
- **Related:** SRCH-001, PRD-006, PRD-007, PED-001, PED-006, MAP-026, PRD-010, PED-007, PED-008, PRD-011, RPT-001
- **Confidence:** Confirmed
