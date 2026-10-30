# Onboarding Guide: End-to-End Test Suite

## Overview
This document outlines the structure and behavior of the `teste2e.cy.js` file. This file contains End-to-End (E2E) tests written using Cypress. The suite validates user interactions on a web application hosted at `http://localhost:3000`. The tests primarily focus on the authentication flow, error handling, and a specific administrative workflow for creating new roles.

## Test Structure
The suite is organized under a single `describe` block titled "Test suite - conjunto de pruebas". It currently contains four test cases (`it` blocks):

1.  **Validar pagina de inicio**: Validates the initial state of the login page.
2.  **Prueba E2E- HappyPath**: Currently empty; intended for successful login scenarios.
3.  **Prueba E2E- UnhappyPath**: Validates error handling when invalid credentials are provided.
4.  **Prueba E2E- Golden Path-Recorrido nuevo rol**: A complex workflow test for creating a new user role after logging in.

## Key Behaviors and Selectors
Before modifying or writing new tests, familiarize yourself with the following patterns used in the existing code:

### Base URL and Navigation
All tests begin by visiting `http://localhost:3000`. Ensure the application is running locally on this port before executing the suite.

### Authentication Flow
The login process follows a consistent pattern across tests:
1.  Click the navigation element: `.ml-auto.items-center > .flex`.
2.  Interact with input fields using IDs: `#user` and `#password`.
3.  Submit the form by clicking the button with class `.z-0`.

### Error Handling
The "UnhappyPath" test demonstrates how the application handles invalid input.
*   **Input**: User types `9999999` and password `9999`.
*   **Verification**: The test asserts that an error message container (`[data-content=""] > div`) becomes visible after submission.

### Role Management Workflow
The "Golden Path" test is the most complex scenario. It simulates a user logging in with specific credentials (`99999999` / `99999999`) and navigating to a management dashboard.
*   **Navigation**: The test clicks a link with the href `/finos/v1/11/management`.
*   **Form Interaction**: It fills out a form with specific Spanish text:
    *   Role Name: "Administrador"
    *   Description: "Se encarga de dar permisos"
*   **Submission**: The form is submitted via a button inside a flex row (`.flex-row > .z-0`).

## Critical Implementation Notes

### Hardcoded Delays
The "Golden Path" test relies heavily on `cy.wait(3000)` between almost every action. This indicates the application may have slow rendering times or asynchronous processes that are not yet handled by Cypress's built-in waiting mechanisms (like `cy.get` with `should` assertions).
*   **Action**: When refactoring, consider replacing these fixed waits with explicit assertions to improve test reliability and speed.

### Fragile Selectors
The test suite uses a mix of IDs (stable) and complex CSS selectors (fragile).
*   **Stable**: `#user`, `#password`, `[href="/finos/v1/11/management"]`.
*   **Fragile**: `.ml-auto.items-center > .flex`, `:nth-child(2) > .h-auto`.
*   **Risk**: Changes to the UI layout or class names (e.g., Tailwind CSS updates) will likely break the fragile selectors. Prioritize adding `data-testid` attributes to the application code to stabilize these selectors.

### Incomplete Test
The "HappyPath" test is currently empty. This is a known gap in the suite. A new developer should implement the logic for a successful login scenario here, likely mirroring the "UnhappyPath" structure but with valid credentials and a different assertion (e.g., checking for a dashboard element).

## Getting Started
1.  Start the application on `http://localhost:3000`.
2.  Run the suite to observe the current behavior, noting the long execution time caused by the hardcoded waits.
3.  Begin by implementing the missing "HappyPath" test.
4.  Gradually refactor the "Golden Path" test to remove `cy.wait` calls in favor of robust assertions.
