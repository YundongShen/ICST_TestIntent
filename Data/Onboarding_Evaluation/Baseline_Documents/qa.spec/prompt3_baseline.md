## Prompt

```text
Below is one test file from the project's test suite. Generate a natural language summary of each test case and the overall test suite. 

Use only what the test file shows. Do not invent behavior that is not in the code. Write in English and use no emoji.

Test file: {file_name}

{source}
```

## Generated Document

### Overall Test Suite Summary
The test suite validates the "QA View" of the application, specifically focusing on the QA dashboard that displays test results, code coverage, and quality gates. Before each test runs, the suite sets up the environment by mocking API routes, navigating to the `/qa` URL, and waiting for the application to fully load. The tests verify that the page loads correctly and that key visual components related to metrics, test results, and coverage charts are present on the screen.

### Individual Test Case Summaries

*   **should render QA view**: Verifies that the browser successfully navigates to the `/qa` URL and that the main page body is visible, confirming the basic rendering of the view.
*   **should display QA metrics or cards**: Checks for the presence of UI elements that likely represent metrics or cards by searching for classes containing keywords like "qa", "metric", "card", or "quality". It asserts that at least zero such elements exist (effectively checking that the query does not fail, though the assertion is permissive).
*   **should display test results or status**: Validates that the page contains elements related to test outcomes by locating classes with keywords such as "test", "result", "status", or "gate". Similar to the previous test, it asserts that the count of these elements is non-negative.
*   **should show coverage or chart elements**: Ensures that visual data representations, such as charts or coverage indicators, are rendered. It looks for SVG elements, canvas elements, or classes containing "chart", "coverage", or "progress", asserting that the count of these elements is at least zero.
