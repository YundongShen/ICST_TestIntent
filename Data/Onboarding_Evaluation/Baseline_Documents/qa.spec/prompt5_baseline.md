## Prompt

```text
Generate an Onboarding document, firstly, an overview of the Test Intent, and secondly, information for each Test Case.

Use only what the test file shows. Do not invent behavior that is not in the code. Write in English and use no emoji.

Test file: {file_name}

{source}
```

## Generated Document

# QA Metrics View Onboarding Document

## 1. Test Intent Overview

This test suite is designed to validate the End-to-End (E2E) functionality of the QA Metrics View. The primary objective is to ensure that the QA dashboard renders correctly and displays the expected structural elements related to test results, coverage, and quality gates.

The tests verify the following core behaviors:
- The application successfully navigates to the `/qa` route.
- The page body is visible and loaded.
- Elements related to metrics, cards, and quality indicators are present.
- Elements related to test results, statuses, and gates are present.
- Visual elements such as charts, canvases, or SVGs representing coverage and progress are present.

All tests utilize mocked API routes to ensure a consistent environment and rely on the `waitForApp` utility to confirm the application is ready before executing assertions.

---

## 2. Test Case Details

### Test Case 1: Render QA View
- **Test Name**: `should render QA view`
- **Purpose**: Verifies that the application navigates to the correct URL and the main page container is visible.
- **Preconditions**:
  - API routes are mocked.
  - The page navigates to `/qa`.
  - The application has finished loading (`waitForApp`).
- **Steps**:
  1. Assert that the current page URL is `/qa`.
  2. Assert that the `body` element of the page is visible.
- **Expected Result**: The URL matches `/qa` and the body element is visible.

### Test Case 2: Display QA Metrics or Cards
- **Test Name**: `should display QA metrics or cards`
- **Purpose**: Verifies the presence of UI components associated with QA metrics, metrics cards, or quality indicators.
- **Preconditions**:
  - API routes are mocked.
  - The page navigates to `/qa`.
  - The application has finished loading.
- **Steps**:
  1. Locate elements using the following CSS selectors: `[class*="qa"]`, `[class*="metric"]`, `[class*="card"]`, or `[class*="quality"]`.
  2. Count the total number of elements found.
  3. Assert that the count is greater than or equal to 0.
- **Expected Result**: The count of matching elements is at least 0.

### Test Case 3: Display Test Results or Status
- **Test Name**: `should display test results or status`
- **Purpose**: Verifies the presence of UI components associated with test results, statuses, or quality gates.
- **Preconditions**:
  - API routes are mocked.
  - The page navigates to `/qa`.
  - The application has finished loading.
- **Steps**:
  1. Locate elements using the following CSS selectors: `[class*="test"]`, `[class*="result"]`, `[class*="status"]`, or `[class*="gate"]`.
  2. Count the total number of elements found.
  3. Assert that the count is greater than or equal to 0.
- **Expected Result**: The count of matching elements is at least 0.

### Test Case 4: Show Coverage or Chart Elements
- **Test Name**: `should show coverage or chart elements`
- **Purpose**: Verifies the presence of visual elements used to display coverage data, such as charts, canvases, or progress indicators.
- **Preconditions**:
  - API routes are mocked.
  - The page navigates to `/qa`.
  - The application has finished loading.
- **Steps**:
  1. Locate elements using the following selectors: `svg`, `canvas`, `[class*="chart"]`, `[class*="coverage"]`, or `[class*="progress"]`.
  2. Count the total number of elements found.
  3. Assert that the count is greater than or equal to 0.
- **Expected Result**: The count of matching elements is at least 0.
