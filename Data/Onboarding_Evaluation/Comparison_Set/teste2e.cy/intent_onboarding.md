## Test Suite Overview

**Suite ID:** teste2e.cy.js

**Test cases:** 3

This suite validates the end-to-end user journey from the homepage login to role management, covering form visibility, invalid credential handling, and successful role creation. All tests independently visit the application root and navigate to the login form, meaning no shared fixtures or state dependencies exist between cases. However, the "Golden Path" test relies heavily on hardcoded `cy.wait` commands for stability rather than explicit element readiness checks, which may cause flakiness if the application loads faster or slower than expected. Additionally, the "HappyPath" test case is currently empty and provides no verification despite its name.

- **Login Interface and Role Management**
  - **Unique Dependencies:** None
  - **Login Interface Rendering** (dependencies: None)
  - **Invalid Credential Rejection** (dependencies: None)
  - **Successful Login and Role Creation** (dependencies: None)

---

## Group 1: Login Interface Rendering

**Shared testing question:** Does the login interface render correctly with all required input fields and controls visible?

### Login Interface Rendering
<sub>[teste2e.cy.js:2-8](teste2e.cy.js#L2-L8)</sub>

**Test Objects**

Login Page (Homepage Login Entry and Form Elements)

**Test Goals**

Verify that after opening the homepage and clicking the login entry, the username, password input fields, and login button in the login form are all present and visible.

**Test Activities**

- Step 1: Access `http://localhost:3000`.
- Step 2: Click the login entry element.
- Step 3: Assert that the username input field `#user` exists.
- Step 4: Assert that the password input field `#password` exists.
- Step 5: Assert that the login button `.z-0` is visible.

---

## Group 2: Invalid Credential Rejection

**Shared testing question:** Does the system correctly reject invalid credentials and provide appropriate feedback?

### Invalid Credential Rejection
<sub>[teste2e.cy.js:13-20](teste2e.cy.js#L13-L20)</sub>

**Test Objects**

Login Functionality (Incorrect Credential Handling)

**Test Goals**

Verify that after entering an invalid username and password, login fails and an error message is displayed.

**Test Activities**

- Step 1: Access `http://localhost:3000`.
- Step 2: Click the login entry.
- Step 3: Enter `9999999` in the username input box.
- Step 4: Enter `9999` in the password input box.
- Step 5: Click the login button.
- Step 6: Assert the error message element `[data-content=""] > div` to be visible.

---

## Group 3: Successful Login and Role Creation

**Shared testing question:** Does the system grant access to protected management features after successful authentication?

### Successful Login and Role Creation
<sub>[teste2e.cy.js:21-39](teste2e.cy.js#L21-L39)</sub>

**Test Objects**

Login and Role Management Functionality

**Test Goals**

Verify that after logging in with valid credentials, you can access the management interface and successfully create a new role.

**Test Activities**

- Step 1: Access `http://localhost:3000`.
- Step 2: Click the login entry.
- Step 3: Enter the username.
- Step 4: Enter the password.
- Step 5: Click the login button and wait 3 seconds.
- Step 6: Click the management menu link and wait 3 seconds.
- Step 7: Click the second sub-menu item and wait 3 seconds.
- Step 8: Click the "New" button and wait 3 seconds.
- Step 9: Enter the character name in the first input box.
- Step 10: Enter the description in the second input box and wait 3 seconds.
- Step 11: Click the "Save" button and wait 3 seconds.
