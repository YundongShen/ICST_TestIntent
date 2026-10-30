# Survey instrument

This is the final wording used by `module-spec-v3`. The three [HTML copies](Survey_HTML/) are the participant-facing record. In this survey, **material** means the code in A, the code and baseline summary in B, or the code and Intent Onboarding Document in C.

## Background

### BG01: roles

**Which roles describe you?** Select all that apply.

- Software developer / engineer
- Software test / QA engineer
- Researcher / academic
- Other

Specify the role when Other is selected.

### BG02: software testing experience

**Which option best describes your experience with software testing (e.g., reading, writing, or maintaining tests)?** Select one.

- I am still learning about testing as part of my education
- Less than 1 year
- 1 to less than 3 years
- 3 to less than 6 years
- 6 to less than 9 years
- 9 years or more

### BG03: technology familiarity

**Before this study, how familiar were you with these technologies used in this test suite?** Rate each item.

- JavaScript / TypeScript
- Playwright tests and assertions
- HTML elements and DOM attributes
- CSS styling and Bootstrap

| Value | Familiarity |
| --- | --- |
| 1 | Not familiar at all |
| 2 | Slightly familiar |
| 3 | Somewhat familiar |
| 4 | Moderately familiar |
| 5 | Very familiar |

## Part 1: test suite comprehension

Select one answer for each question. Explanations are optional.

### CQ01

How many test cases does this test suite contain?

- 2
- 5
- 6
- 7
- Can't tell from the material

### CQ02

According to this test suite, what should happen to the page content (the body element) after the page loads?

- It is visible immediately and stays visible
- It is hidden at first and then becomes visible
- It is visible at first and then becomes hidden
- Can't tell from the material

### CQ03

Suppose clicking the "Launch demo modal" button stopped opening the modal. Would this test suite detect it?

- Yes, at least one test would fail
- No, all tests would still pass
- Can't tell from the material

**Optional explanation:** Briefly, what made you choose this answer?

## Agreement scale for Parts 2 and 3

| Value | Response |
| --- | --- |
| 1 | Strongly disagree |
| 2 | Disagree |
| 3 | Neither agree nor disagree |
| 4 | Agree |
| 5 | Strongly agree |

The overall statement also offers **Cannot judge from the material**. A reason is required for this choice. The four specific statements require a rating from 1 to 5.

## Part 2: comprehension support

**Overall statement:** The material helps me understand this test suite.

More specifically, the material makes clear...

1. ...what behavior the test suite checks.
2. ...what each test case is meant to check.
3. ...how each test's steps and assertions check the intended behavior.
4. ...how the test cases relate to each other.

**Optional open questions:**

1. Which part of the material helped you most to understand the test suite, and why?
2. What is still unclear about the test suite, and why?

## Part 3: extension support

**Overall statement:** The material would help me plan a new test case for this suite.

More specifically, the material would help me...

1. ...check whether a new test case would duplicate an existing one.
2. ...find an existing test case to build on.
3. ...decide which behavior or condition to test next.
4. ...choose inputs and expected results for a new test case.

**Optional open questions:**

1. What in the material would you use to design a new test case, and why?
2. What information is missing that you would need to design a new test case?

## Researcher scoring key

| Question | Correct answer | Basis in the code |
| --- | --- | --- |
| CQ01 | 6 | The file contains six `test(...)` cases. |
| CQ02 | It is hidden at first and then becomes visible | The first two tests use `toBeHidden()` and `toBeVisible()` on `body`. |
| CQ03 | No, all tests would still pass | The launch test reads `aria-hidden` before the click and calls `expect(...)` without a matcher. |

CQ03 assumes that locating and clicking the button still succeeds, while the click no longer opens the modal. Each correct answer earns 1 point. Other answers, including **Can't tell from the material**, earn 0. The total score is 0 to 3. This score is an outcome, not a participant exclusion rule.
