# Refinement Layer Process Test

This directory contains a separate process test of the Refinement Layer using Gemini 2.5 Flash. These runs are not part of the experiments or evaluation reported in the paper.

## Observed Changes

The run processed 20 intent records. Two passed the initial checks. Of the 18 initially rejected records, 15 passed after re-extraction, giving 17/20 recorded final passes. The run filled one empty Goal and revised several missing targets, unsupported claims, and overly broad descriptions. Three cases remained flagged after five re-extractions each.

| Case | Before processing | Saved output or remaining issue | Recorded final check |
|---|---|---|---|
| [cypress/kalkulator.cy_2](Records/cypress__kalkulator.cy_2.json) | Goal was empty. | Added the multiplication Goal; retained the input sequence and expected result of 42 in Activities. | Pass |
| [cypress/spec.cy_2](Records/cypress__spec.cy_2.json) | Objects omitted the error message checked by Activities. | Added the `.flash.error` target and specified the error-message check. | Pass |
| [jest_spec/server.spec_1_3](Records/jest_spec__server.spec_1_3.json) | Goal claimed HTTP 200 and `text/html` checks absent from the code. | Restricted the Goal to the returned `Hello City` text. | Pass |
| [pytest_unit/ADD_test__3](Records/pytest_unit__ADD_test__3.json) | Goal included Scalar inputs, which this case did not test. | Restricted the Goal to addition with an OrderedPair and a Vector. | Pass |
| [playwright/e2e.spec_1](Records/playwright__e2e.spec_1.json) | Objects listed `page` and locator calls. | Described the inspected post content, links, avatar, and heading as targets. | Pass |
| [playwright/module.spec_5](Records/playwright__module.spec_5.json) | Activities described asserting that a button exists. | Described the actual check that the button's Locator object is defined. | Pass |
| [pytest_api/REMOTE_FILE_test__2](Records/pytest_api__REMOTE_FILE_test__2.json) | Input already passed the checks. | Output was unchanged; no re-extraction was needed. | Pass |
| [playwright/top.spec_1](Records/playwright__top.spec_1.json), [supertest/app.test_1](Records/supertest__app.test_1.json), [supertest/app.test_2](Records/supertest__app.test_2.json) | The checker flagged `page`, locator calls, or `app` in Objects. | The checker continued to flag setup-to-object consistency or the `app` object despite revisions. | Fail (3 cases) |

Pass/fail follows `final_check_passed` in the process records; it is not an independent accuracy judgment. Full case histories are in [refinement_results.md](Records/refinement_results.md).

## Files

- `Before_Validation/`: input intent records.
- `After_Validation/`: saved outputs, including cases still flagged by the checker.
- `Records/`: checks, feedback, re-extraction attempts, and model responses.
