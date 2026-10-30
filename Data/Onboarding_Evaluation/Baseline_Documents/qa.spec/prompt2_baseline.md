## Prompt

```text
Below is one test file from the project's test suite. Generate a natural language summary of each test case and the overall test suite. 

Use only what the test file shows. Do not invent behavior that is not in the code. Write in English and use no emoji. Each test case summary should be no more than one paragraph long.

Test file: {file_name}

{source}
```

## Generated Document

Overall Test Suite Summary
This test suite validates the end-to-end functionality of the QA Metrics View, specifically focusing on the dashboard that displays test results, code coverage, and quality gates. Before each test runs, the suite mocks API routes, navigates to the `/qa` URL, and waits for the application to fully load. The tests collectively verify that the page loads correctly, the URL is accurate, and the interface contains expected elements related to metrics, test statuses, and visual charts, ensuring the core components of the QA dashboard are present and visible.

Test Case Summaries

The first test case verifies that the QA view renders successfully by checking that the browser's current URL is `/qa` and confirming that the main body of the page is visible to the user.

The second test case ensures that the page displays elements associated with QA metrics by searching for DOM nodes with class names containing keywords like "qa," "metric," "card," or "quality," and asserting that at least one such element exists.

The third test case validates the presence of test results or status indicators by locating elements with class names including "test," "result," "status," or "gate," and confirming that the count of these elements is greater than or equal to zero.

The fourth test case checks for the existence of coverage or chart visualizations by searching for SVG elements, canvas elements, or nodes with class names containing "chart," "coverage," or "progress," and asserting that at least one such element is found on the page.
