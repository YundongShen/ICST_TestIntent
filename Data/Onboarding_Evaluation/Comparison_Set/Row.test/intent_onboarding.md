## Test Suite Overview

**Suite ID:** Row.test.tsx

**Test cases:** 4

This suite verifies the Row component's ability to calculate and update ingredient weights based on user input, unit selection, ingredient changes, and the scale prop. Each test renders the component independently with a default scale of 1, except the final case which explicitly sets scale to 2. The tests rely on specific hardcoded ingredient densities and unit conversion factors, such as Pizza Flour at 116.0g and Agave syrup at 336.0g, meaning the assertions are tightly coupled to these specific data values rather than generic calculation logic. No shared state or execution order dependencies exist between cases, as cleanup runs after every test.

- **Row Conversion Logic**
  - **Unique Dependencies:** `@testing-library/react`, `@testing-library/user-event`, `bun:test`, `./Row`
  - **Verify Value Entry** (dependencies: `@testing-library/react`, `@testing-library/user-event`, `bun:test`, `./Row`)
  - **Verify Unit Change** (dependencies: `@testing-library/react`, `@testing-library/user-event`, `bun:test`, `./Row`)
  - **Verify Ingredient Change** (dependencies: `@testing-library/react`, `@testing-library/user-event`, `bun:test`, `./Row`)
  - **Verify Scale Property** (dependencies: `@testing-library/react`, `@testing-library/user-event`, `bun:test`, `./Row`)

---

## Group 1: Verify Value Entry, Verify Unit Change, Verify Ingredient Change, Verify Scale Property

**Shared testing question:** Does the Row component correctly calculate and update conversion results based on changes to input values, units, ingredients, or scaling factors?

### Verify Value Entry
<sub>[Row.test.tsx:9-17](Row.test.tsx#L9-L17)</sub>

**Test Objects**

`Row` Component

**Test Goals**

Verify that entering a value displays the correct conversion result.

**Test Activities**

- Step 1: Render the `Row` component with `scale={1}`.
- Step 2: Locate the number input box and enter `2`.
- Step 3: Wait and confirm that the result text `232.0 g` appears on the page.

### Verify Unit Change
<sub>[Row.test.tsx:19-34](Row.test.tsx#L19-L34)</sub>

**Test Objects**

`Row` Component

**Test Goals**

Verify that changing the unit recalculates the result correctly.

**Test Activities**

- Step 1: Render the `Row` component with `scale={1}`.
- Step 2: Enter `1` in the input box and confirm that the initial result displays `116.0 g`.
- Step 3: Open the first dropdown menu (unit selection) and select `Ounce`.
- Step 4: Confirm that the result is updated to `14.5 g`.

### Verify Ingredient Change
<sub>[Row.test.tsx:36-51](Row.test.tsx#L36-L51)</sub>

**Test Objects**

`Row` Component

**Test Goals**

Verify that changing the ingredient recalculates the result based on the new ingredient's density.

**Test Activities**

- Step 1: Render the `Row` component with `scale={1}`.
- Step 2: Enter `1` in the input box and confirm the initial result displays `116.0 g`.
- Step 3: Open the second dropdown (ingredient selection) and select `Agave syrup`.
- Step 4: Confirm the result is updated to `336.0 g`.

### Verify Scale Property
<sub>[Row.test.tsx:53-60](Row.test.tsx#L53-L60)</sub>

**Test Objects**

`Row` Component

**Test Goals**

Confirm that the `scale` property affects the final calculation result.

**Test Activities**

- Step 1: Render the `Row` component with `scale={2}`.
- Step 2: Enter `1` in the input box.
- Step 3: Confirm the result displays `232.0 g` (twice the base value).
