## Prompt

```text
Generate an Onboarding document, firstly, an overview of the Test Intent, and secondly, information for each Test Case.

Use only what the test file shows. Do not invent behavior that is not in the code. Write in English and use no emoji.

Test file: {file_name}

{source}
```

## Generated Document

# Onboarding Document: Bootstrap 4 Test Suite

## 1. Test Intent Overview

The purpose of this test suite is to verify the behavior of a web application utilizing Bootstrap 4, specifically focusing on initial page rendering, CSS styling application, and modal interaction. The tests are executed using Playwright and target a root path (`/`).

The primary objectives include:
*   Verifying that the page body is initially hidden and becomes visible after loading.
*   Confirming that alert messages receive specific styling (background color changes) once the Bootstrap 4 CSS file is loaded from the CDN.
*   Validating the presence and state of a modal dialog, ensuring it is initially hidden and can be triggered by a specific button click.

All tests assume the page loads successfully at the root URL before execution.

---

## 2. Test Case Details

### Test Case 1: Initial Page Visibility
*   **Description**: Verifies the state of the page body immediately upon navigation.
*   **Target Element**: `body`
*   **Expected Behavior**: The `body` element must be hidden.
*   **Assertion**: `page.locator('body')` is hidden.

### Test Case 2: Page Content Display
*   **Description**: Verifies that the page content becomes visible after the initial load phase.
*   **Target Element**: `body`
*   **Expected Behavior**: The `body` element must eventually become visible.
*   **Assertion**: `page.locator('body')` is visible.

### Test Case 3: Alert Message Styling
*   **Description**: Verifies that the background color of an alert element changes after the Bootstrap CSS is loaded.
*   **Target Element**: First element with class `.alert-primary`.
*   **Process**:
    1.  Capture the initial computed background color of the alert.
    2.  Wait for the response from `https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css`.
    3.  Capture the new computed background color.
*   **Expected Behavior**: The background color must change after the CSS response is received.
*   **Assertion**: The styled color is not equal to the initial color.

### Test Case 4: Modal Presence and Initial State
*   **Description**: Verifies the existence and initial hidden state of the modal dialog.
*   **Target Element**: Element with attribute `[role="dialog"]`.
*   **Expected Behavior**:
    1.  Exactly one modal element exists on the page.
    2.  The modal's `aria-hidden` attribute is set to `'true'`.
*   **Assertion**:
    *   Count of `[role="dialog"]` equals 1.
    *   `aria-hidden` attribute value equals `'true'`.

### Test Case 5: Modal Launch Button Existence
*   **Description**: Verifies the presence of the button used to trigger the modal.
*   **Target Element**: Button containing the text "Launch demo modal".
*   **Expected Behavior**: The button locator is defined.
*   **Assertion**: The locator for `text=Launch demo modal` is defined.

### Test Case 6: Modal Launch Interaction
*   **Description**: Verifies that clicking the launch button changes the modal's visibility state.
*   **Target Elements**:
    *   Button: `text=Launch demo modal`
    *   Modal: `[role="dialog"]`
*   **Process**:
    1.  Locate the modal and capture its initial `aria-hidden` attribute (expected to be `'true'` based on previous test logic, though this test captures it locally).
    2.  Locate the launch button.
    3.  Click the launch button.
*   **Expected Behavior**: The `aria-hidden` attribute of the modal changes to `'false'`.
*   **Assertion**: The `aria-hidden` attribute value equals `'false'`.
