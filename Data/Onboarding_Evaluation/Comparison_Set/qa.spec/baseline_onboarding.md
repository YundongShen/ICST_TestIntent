# Onboarding: QA Metrics View Test Suite

## Overview
This document outlines the structure and expectations for the `qa.spec.ts` test file. This suite contains End-to-End (E2E) tests specifically for the **QA Dashboard** (accessible at `/qa`). The primary goal of these tests is to verify the rendering of the dashboard and the presence of key visual components related to test results, coverage, and quality gates.

## Test Architecture
The tests utilize a custom fixture setup defined in `./fixtures/base.fixture` and `./fixtures/api-mocks.fixture`.

*   **Test Runner**: The suite uses a `test` runner imported from the base fixture.
*   **Setup (`beforeEach`)**: Before every test case, the following steps are executed:
    1.  **API Mocking**: `mockApiRoutes(page)` is called to intercept and mock backend API responses. This ensures tests run against consistent, controlled data.
    2.  **Navigation**: The browser navigates to the `/qa` route.
    3.  **Stability Check**: `waitForApp(page)` is invoked to ensure the application has fully loaded and stabilized before assertions run.

## Test Cases and Assertions
The suite contains four specific tests within the `QA View` description block. Note that these tests currently verify the **presence** of elements rather than specific data values or complex interactions.

1.  **Render Verification**: Confirms the browser URL is `/qa` and the `body` element is visible.
2.  **Metrics Display**: Searches for elements with classes containing `qa`, `metric`, `card`, or `quality`. It asserts that the count of these elements is greater than or equal to 0.
3.  **Test Results Display**: Searches for elements with classes containing `test`, `result`, `status`, or `gate`. It asserts that the count is greater than or equal to 0.
4.  **Coverage Display**: Searches for `svg`, `canvas`, or elements with classes containing `chart`, `coverage`, or `progress`. It asserts that the count is greater than or equal to 0.

## Key Considerations for New Developers
*   **Locator Strategy**: The tests rely heavily on CSS class name patterns (e.g., `[class*="metric"]`). When modifying the UI, ensure that class names for metrics, results, and charts retain these keywords, or the tests will fail to locate the elements.
*   **Assertion Logic**: Be aware that the current assertions (`toBeGreaterThanOrEqual(0)`) pass even if zero elements are found. These tests verify that the selectors do not throw errors and that the page structure allows for these elements to exist, but they do not currently enforce that specific data is rendered.
*   **Dependencies**: Do not modify the `mockApiRoutes` or `waitForApp` functions unless you understand the broader fixture architecture. The tests depend on these utilities to isolate the QA view from external network dependencies.

When adding new tests, follow the existing pattern: mock the API, navigate to `/qa`, wait for the app, and then assert on the presence of relevant DOM elements using class-based selectors.
