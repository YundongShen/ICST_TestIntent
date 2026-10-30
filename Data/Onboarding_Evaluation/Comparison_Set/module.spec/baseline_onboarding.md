# Onboarding Guide: Test Suite Overview

## Introduction
Welcome to the team. This document outlines the structure, scope, and expectations for the `module.spec.ts` test file. This file is part of the project's end-to-end (E2E) testing suite, utilizing **Playwright** to validate the behavior of the application's user interface.

## Test Framework and Setup
The tests are written using the Playwright test runner. Each test case follows a standard lifecycle:

1.  **Framework Imports**: The file imports `test` and `expect` from `@playwright/test`.
2.  **Global Setup**: A `test.beforeEach` hook is defined to ensure a clean state for every test. This hook navigates the browser to the root path (`/`) before executing any specific test case.
3.  **Test Organization**: Tests are grouped logically using `test.describe` blocks. The primary suite is labeled "Bootstrap 4," with a nested suite for "Modal" functionality.

## Scope of Tests
The current test suite focuses on the integration of **Bootstrap 4** components and the initial loading state of the application. It does not test backend logic, API responses (other than CSS loading), or complex data flows.

### 1. Page Loading and Visibility
The suite verifies the application's loading sequence:
*   **Initial State**: The `body` element must be hidden immediately upon page load.
*   **Final State**: The `body` element must eventually become visible, confirming that the application loads content successfully.

### 2. CSS Styling and Asset Loading
A specific test validates that external stylesheets are applied correctly:
*   It targets an element with the class `.alert-primary`.
*   It captures the computed background color before the Bootstrap CSS is loaded.
*   It waits for the specific network response from the CDN (`https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css`).
*   It asserts that the background color changes after the CSS is applied, confirming the stylesheet is active.

### 3. Modal Component Behavior
A nested suite validates the functionality of a demo modal:
*   **Existence and State**: The page must contain exactly one modal element (`[role="dialog"]`). Initially, this modal must have the attribute `aria-hidden` set to `true`.
*   **Trigger Element**: The page must contain a button with the visible text "Launch demo modal".
*   **Interaction**: Clicking the launch button must change the modal's `aria-hidden` attribute from `true` to `false`, indicating the modal is now open.

## Key Technical Considerations
Before modifying or adding tests, be aware of the following patterns used in this file:

*   **Locator Strategy**: The tests rely heavily on CSS selectors (e.g., `.alert-primary`, `[role="dialog"]`) and text content (e.g., `text=Launch demo modal`). Ensure any new tests use stable selectors.
*   **Network Assertions**: The styling test explicitly waits for a specific URL response. This is a critical pattern for verifying that external dependencies are loaded before checking visual styles.
*   **Attribute Inspection**: Modal state is verified by reading the `aria-hidden` attribute directly rather than checking visibility classes. This is the preferred method for accessibility-compliant state checking in this suite.
*   **Asynchronous Evaluation**: The test uses `page.evaluate` to inspect computed styles within the browser context. This is necessary for validating dynamic CSS changes.

## Guidelines for New Contributions
*   **Do not invent behavior**: Only test what is currently rendered or interacted with on the page.
*   **Respect the setup**: Do not alter the `beforeEach` hook unless there is a specific need to change the starting URL for a new feature.
*   **Maintain isolation**: Ensure new tests do not rely on the state left by previous tests. The `beforeEach` hook resets the page for every run.
*   **Use descriptive names**: Follow the existing convention of `should [action] [subject]` for test descriptions.

By adhering to these patterns, you will ensure consistency across the test suite and maintain reliable coverage for the Bootstrap 4 integration.
