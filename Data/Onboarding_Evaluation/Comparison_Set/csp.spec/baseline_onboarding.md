# Onboarding Guide: Content Security Policy Test Suite

## Overview
This document outlines the purpose and structure of `csp.spec.ts`, a Playwright test file dedicated to verifying the application's security posture. As a new team member, your primary focus when working with this file is ensuring the server enforces strict Content Security Policy (CSP) rules and related security headers without breaking functionality.

## Test Framework and Setup
The suite uses **Playwright** (`@playwright/test`). Tests are organized under the `test.describe('Content Security Policy')` block. Most tests utilize the `page` fixture to simulate browser interactions, while one test uses the `request` fixture for direct HTTP inspection.

## What This Suite Tests

### 1. Strict CSP Header Enforcement
The first test verifies that the root URL (`/`) returns a `content-security-policy` header with a highly restrictive configuration. The expected policy includes:
- `default-src 'none'`: Blocks all resources by default.
- `script-src 'self'`: Allows scripts only from the same origin.
- `style-src 'self'`: Allows styles only from the same origin.
- `img-src 'self' data:`: Allows images from the same origin and data URIs.
- `frame-src blob:` and `object-src blob:`: Restricts frames and objects to blob URLs only.
- `form-action 'none'`: Disables form submissions entirely.

### 2. Additional Security Headers
The second test confirms the presence of four critical security headers on the root response:
- `x-content-type-options`: Must be `nosniff`.
- `x-frame-options`: Must be `DENY`.
- `referrer-policy`: Must be `strict-origin-when-cross-origin`.
- `permissions-policy`: Must explicitly disable camera access (`camera=()`).

### 3. Runtime CSP Compliance
The third test ensures the page loads without triggering CSP violations. It monitors:
- Console logs for messages containing "Content-Security-Policy" or "CSP".
- Page errors via the `pageerror` event.
The test navigates to the root, waits for the `[data-testid="items-container"]` selector to appear, and waits an additional 500ms to capture async violations before asserting that the violation list is empty.

### 4. Absence of Inline Styles
The final test performs a static analysis of the HTML response body. It extracts the `<body>` content and asserts that there are **no** `style=` attributes present. This ensures compliance with the strict `style-src 'self'` policy, which would otherwise block inline styles.

## Key Guidelines for Contributors

1.  **Do Not Weaken the Policy**: Any changes to the application that require new script sources, styles, or form actions will cause these tests to fail. You must update the server configuration to explicitly allow the new source (e.g., adding a specific domain to `script-src`) rather than relaxing the policy to `*` or `'unsafe-inline'`.
2.  **Inline Styles are Forbidden**: The test explicitly checks the HTML body for `style=` attributes. If your feature requires styling, use external CSS files or CSS-in-JS solutions that do not render inline style attributes in the DOM.
3.  **Form Submissions**: The current policy sets `form-action 'none'`. If your feature requires form submissions, you must modify the CSP header to allow the specific action URL, as the current configuration blocks all forms.
4.  **Timing Considerations**: The runtime violation test includes a 500ms timeout to catch async errors. If you introduce heavy async loading logic, ensure it does not generate CSP errors within this window.
5.  **Selector Reliance**: The runtime test waits for `[data-testid="items-container"]`. Ensure this test ID remains present on the root page for the test to proceed correctly.

By adhering to these constraints, you ensure the application maintains its high security baseline while developing new features.
