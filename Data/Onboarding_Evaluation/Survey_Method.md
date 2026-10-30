# Survey method

## Research question

To what extent can an onboarding document, based on extracted test intent, support a practitioner in comprehending and extending a test suite?

## Design and materials

The study uses a between-subjects design. Each participant reads one test suite, `module.spec.ts`, in one condition.

| Condition | Material |
| --- | --- |
| A | Test code only |
| B | The same code and a baseline summary generated from the code |
| C | The same code and an Intent Onboarding Document based on extracted Test Objects, Test Goals, and Test Activities |

The code, question content, and response scales are shared across conditions. Instructions refer to code alone in A and to code with supporting material in B and C. B and C use the same side-by-side layout and document heading. A shows the code in a single centered panel.

The exact material versions and their standalone HTML copies are linked in the [directory guide](README.md).

## Recruitment and allocation

The target population includes students and professionals with a software testing background. Recruitment used convenience and purposive sampling through personal contacts, LinkedIn, Bluesky, X, and Mastodon.

The survey records roles, software testing experience, and prior familiarity with the technologies used in the suite. These answers describe the sample and support background comparisons. They do not determine allocation.

After the background section and instructions, the server assigns a condition using shuffled blocks containing A, B, and C once each. An existing browser session keeps its assignment. This balances assignments; completed group sizes can differ when people leave before submission.

## Procedure

1. Read the participation note and complete the background questions.
2. Read the instructions and select **Ready to start**.
3. Read the assigned material and answer three comprehension questions.
4. Rate comprehension support: one overall statement and four specific statements.
5. Rate support for planning a new test: one overall statement and four specific statements.
6. Submit the answers and receive a receipt.

The material remains available during the three question sections. Ratings and open comments appear in separate columns. Open comments are optional.

## Measures

| Measure | Response |
| --- | --- |
| Roles | Multiple selection, with text for Other |
| Testing experience | One year-range category or still learning |
| Technology familiarity | Four self-ratings from 1 to 5 |
| Comprehension | Three multiple-choice questions, with an optional explanation for the third |
| Comprehension support | One overall statement and four specific statements, rated from Strongly disagree to Strongly agree |
| Extension support | One overall statement and four specific statements on planning a new test, using the same agreement scale |
| Explanations | Two optional open questions for each support section |

Each overall support statement also offers **Cannot judge from the material** and asks for a reason when selected. The four specific statements use the five-point agreement scale.

Comprehension questions provide a code-based outcome. Extension support measures perceived help with planning; participants do not implement a new test in this survey. The full wording and scoring key are in [Survey_Instrument.md](Survey_Instrument.md).

## Recording and analysis

Cloudflare Pages serves the HTML interface. Supabase stores allocation and response records. Drafts are saved before final submission. A response is complete when `submitted_at` is set. Test and live records are separate.

The main comparisons are C versus A and C versus B.

- Score each correct comprehension answer as 1 and each other answer as 0, giving a total from 0 to 3. Also report accuracy for each question.
- Analyze each overall support rating and its four specific ratings separately. Keep the five response levels and state the number of scored responses. **Cannot judge** is reported separately and is not scored as 0 or as a neutral rating.
- Summarize roles as multiple-response counts, experience as categories, and familiarity as ordinal ratings. Compare these backgrounds across groups before interpreting group differences.
- Use open comments to describe what helped, what remained unclear, and what information was missing.

Background comparisons provide context for interpreting the material comparisons.
