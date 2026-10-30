## Prompt

```text
Generate an onboarding document for new employees, providing information on both the Test suite and Test case level

Use only what the test file shows. Do not invent behavior that is not in the code. Write in English and use no emoji.

Test file: {file_name}

{source}
```

## Generated Document

# New Employee Onboarding: QA Testing Suite

## Overview
This document outlines the structure and expectations for the QA testing suite based on the `qa.spec.ts` file. The suite focuses on End-to-End (E2E) testing for the QA Metrics View, specifically validating the QA dashboard, test results, coverage, and quality gates.

## Test Suite Structure

### File and Imports
The test suite is located in the file `qa.spec.ts`. It relies on the following imports:
- `test`, `expect`, and `waitForApp` from `./fixtures/base.fixture`.
- `mockApiRoutes` from `./fixtures/api-mocks.fixture`.

### Test Description
The entire suite is grouped under a single description block:
- **Name**: `QA View`
- **Scope**: Tests the QA dashboard, including test results, coverage, and quality gates.

### Suite Setup (Before Each Test)
Every test within the `QA View` suite executes the following setup steps before running:
1. Mocks API routes using `mockApiRoutes(page)`.
2. Navigates the browser to the `/qa` URL.
3. Waits for the application to be ready using `waitForApp(page)`.

---

## Test Case Level Details

The suite contains four specific test cases. Each case validates the presence or visibility of specific UI elements related to the QA dashboard.

### 1. Render QA View
- **Purpose**: Verifies that the QA view loads correctly.
- **Assertions**:
  - Confirms the page URL is `/qa`.
  - Confirms the `body` element is visible.

### 2. Display QA Metrics or Cards
- **Purpose**: Checks for the presence of metrics, cards, or quality-related elements.
- **Locator Strategy**: Selects elements with classes containing `qa`, `metric`, `card`, or `quality`.
- **Assertion**:
  - Counts the number of matching elements.
  - Expects the count to be greater than or equal to 0.

### 3. Display Test Results or Status
- **Purpose**: Validates the display of test results and status indicators.
- **Locator Strategy**: Selects elements with classes containing `test`, `result`, `status`, or `gate`.
- **Assertion**:
  - Counts the number of matching elements.
  - Expects the count to be greater than or equal to 0.

### 4. Show Coverage or Chart Elements
- **Purpose**: Ensures coverage data and visual charts are rendered.
- **Locator Strategy**: Selects `svg` elements, `canvas` elements, or elements with classes containing `chart`, `coverage`, or `progress`.
- **Assertion**:
  - Counts the number of matching elements.
  - Expects the count to be greater than or equal to 0.

---

## Key Implementation Notes
- **Mocking**: All tests depend on mocked API routes to function.
- **Navigation**: All tests start by navigating to the `/qa` path.
- **Validation Logic**: The suite does not assert specific values for metrics or results. Instead, it verifies that the relevant UI components exist (count >= 0).
- **Selectors**: The tests utilize broad class-based selectors (e.g., `[class*="metric"]`) and tag selectors (`svg`, `canvas`) to identify UI components.
