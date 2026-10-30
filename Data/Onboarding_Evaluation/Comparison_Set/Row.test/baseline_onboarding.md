# Row Component Test Suite Onboarding

## Overview
This document outlines the testing strategy for the `Row` component based on the `Row.test.tsx` file. The tests verify the component's ability to dynamically calculate ingredient weights based on user input, unit selection, ingredient selection, and a scaling factor.

## Testing Framework and Tools
The test suite utilizes the following stack:
- **Runner**: `bun:test` (indicated by the import from `bun:test`).
- **React Testing Library**: Used for rendering components (`render`, `screen`, `cleanup`) and querying the DOM.
- **User Event**: Used to simulate realistic user interactions like typing and clicking.
- **Cleanup**: The `afterEach` hook ensures the DOM is cleaned up after every test to prevent state leakage.

## Component Behavior Under Test
The `Row` component accepts a `scale` prop and renders an interactive row containing:
1.  **Input Field**: Identified by the role `spinbutton`. Users enter a quantity here.
2.  **Unit Selector**: Identified as the first `combobox`. Changing this alters the conversion logic.
3.  **Ingredient Selector**: Identified as the second `combobox`. Changing this updates the base weight value.
4.  **Result Display**: A text element showing the final calculated weight in grams (e.g., "116.0 g").

## Key Test Scenarios
The suite covers four specific behaviors:

1.  **Input Calculation**: Verifies that typing a number into the spinbutton immediately updates the result. For example, entering `2` with a scale of `1` yields `232.0 g`.
2.  **Unit Conversion**: Confirms that changing the unit (e.g., from the default to "Ounce") triggers a recalculation. The test expects the result to divide by the unit factor (e.g., `116.0 / 8 = 14.5 g`).
3.  **Ingredient Switching**: Ensures that selecting a different ingredient updates the base weight. Switching from "00 Pizza Flour" (base 116.0) to "Agave syrup" (base 336.0) updates the result accordingly.
4.  **Scaling**: Validates that the `scale` prop multiplies the final result. A scale of `2` doubles the calculated weight.

## Implementation Notes for Developers
- **Asynchronous Assertions**: All tests use `await` with `userEvent` and `screen.findByText`. This indicates the component performs calculations asynchronously or relies on React's rendering cycle. Do not use `getByText` for the result; use `findByText` to wait for the update.
- **Querying Strategy**: The tests rely heavily on semantic roles (`spinbutton`, `combobox`) rather than class names or IDs. Ensure your component maintains these ARIA roles.
- **Hardcoded Values**: The tests assume specific base values for ingredients (e.g., 116.0 for "00 Pizza Flour") and conversion factors (e.g., 8 for Ounces). If you modify the data source, update these expected values in the tests.
- **Cleanup**: Always ensure your component does not hold global state that persists between tests, as `cleanup` is explicitly called after each run.
