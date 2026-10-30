## Test Suite Overview

**Suite ID:** csp.spec.ts

**Test cases:** 4

This suite verifies the server's security posture by checking Content Security Policy and other protective headers, ensuring no browser-level violations occur during page load, and confirming the absence of inline styles in the served HTML. All tests are independent and run in any order, as each explicitly navigates to the homepage or fetches the page content without relying on shared state or fixtures. Note that the inline style check only scans the `<body>` content, so inline styles elsewhere in the served HTML are not checked despite the test name; within the body, any `style="` attribute fails the test, including one inside an SVG.

- **CSP and Security Header Verification**
  - **Unique Dependencies:** `@playwright/test`
  - **Verify CSP Header Directives** (dependencies: `@playwright/test`)
  - **Verify Other Security Headers** (dependencies: `@playwright/test`)
  - **Verify No Console Violations** (dependencies: `@playwright/test`)
  - **Verify No Inline Styles** (dependencies: `@playwright/test`)

---

## Group 1: Verify CSP Header Directives, Verify Other Security Headers, Verify No Console Violations, Verify No Inline Styles

**Shared testing question:** Does the server correctly configure and enforce Content-Security-Policy and related security headers?

### Verify CSP Header Directives
<sub>[csp.spec.ts:4-17](csp.spec.ts#L4-L17)</sub>

**Test Objects**

Server's Content-Security-Policy response header

**Test Goals**

Verify that the CSP header returned by the homepage contains all necessary security directives.

**Test Activities**

- Step 1: Access the homepage `/` and retrieve the response object.
- Step 2: Extract the value of `content-security-policy` from the response header.
- Step 3: Assert that this header exists and contains, in order: `default-src 'none'`, `script-src 'self'`, `style-src 'self'`, `img-src 'self' data:`, `frame-src blob:`, `object-src blob:`, `form-action 'none'`.

### Verify Other Security Headers
<sub>[csp.spec.ts:19-27](csp.spec.ts#L19-L27)</sub>

**Test Objects**

Other security response headers from the server

**Test Goals**

Confirm that the response contains the correct fields.

**Test Activities**

- Step 1: Access `/` and retrieve the response header.
- Step 2: Assert `x-content-type-options` as `nosniff`.
- Step 3: Assert `x-frame-options` as `DENY`.
- Step 4: Assert `referrer-policy` as `strict-origin-when-cross-origin`.
- Step 5: Assert `permissions-policy` as containing `camera=()`.

### Verify No Console Violations
<sub>[csp.spec.ts:29-46](csp.spec.ts#L29-L46)</sub>

**Test Objects**

Browser console and error events during page load.

**Test Goals**

Verify that no CSP violations or related errors occur after the page has fully loaded.

**Test Activities**

- Step 1: Listen for page console messages; if `Content-Security-Policy` or `CSP` is present, add it to the violations array.
- Step 2: Listen for uncaught errors on the page and add them to the violations list.
- Step 3: Access `/` and wait for the `[data-testid="items-container"]` element to appear.
- Step 4: Wait an additional 500ms to allow asynchronous violations a chance to trigger.
- Step 5: Assert the length of violations to 0.

### Verify No Inline Styles
<sub>[csp.spec.ts:48-58](csp.spec.ts#L48-L58)</sub>

**Test Objects**

The HTML page returned by the server

**Test Goals**

Confirm that the `style=` inline style attribute does not exist in the HTML.

**Test Activities**

- Step 1: Retrieve the homepage HTML text using an API request.
- Step 2: Extract the content of the `<body>` section.
- Step 3: Search for matches of `style="` in the body content.
- Step 4: Assert the result as null (not found).
