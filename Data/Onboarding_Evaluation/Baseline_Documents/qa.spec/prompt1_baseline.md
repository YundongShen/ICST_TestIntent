## Prompt

```text
Below is one test file from the project's test suite. Generate a natural language summary of each test case. 

Use only what the test file shows. Do not invent behavior that is not in the code. Write in English and use no emoji. Each summary should be no more than one paragraph long.

Test file: {file_name}

{source}
```

## Generated Document

The first test case verifies that the QA view loads correctly by confirming the browser navigates to the `/qa` URL and that the main body element of the page becomes visible.

The second test case checks for the presence of QA-related visual components by searching for elements with class names containing keywords like "qa", "metric", "card", or "quality" and asserts that at least one such element exists on the page.

The third test case ensures that test result or status indicators are displayed by locating elements with class names including "test", "result", "status", or "gate" and verifying that the count of these elements is greater than or equal to zero.

The fourth test case validates the rendering of coverage data or visualizations by finding SVG, canvas, or elements with class names related to "chart", "coverage", or "progress", asserting that at least one of these elements is present.
