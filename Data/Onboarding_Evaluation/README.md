# Onboarding evaluation

This directory contains the current `module.spec` study and earlier material preparation records.

## Current study

The research question is:

> To what extent can an onboarding document, based on extracted test intent, support a practitioner in comprehending and extending a test suite?

| Condition | Material |
| --- | --- |
| [A](Survey_HTML/survey_module.spec_A.html) | Test code only |
| [B](Survey_HTML/survey_module.spec_B.html) | The same code and a baseline summary |
| [C](Survey_HTML/survey_module.spec_C.html) | The same code and an Intent Onboarding Document |

Each participant receives one condition. The study version is `module-spec-v3`.

| File or folder | Contents |
| --- | --- |
| [Survey_Method.md](Survey_Method.md) | Design, allocation, procedure, and analysis approach |
| [Survey_Instrument.md](Survey_Instrument.md) | Final questions, scales, and researcher scoring key |
| [Survey_HTML](Survey_HTML/) | Three standalone HTML copies with fixed A, B, or C materials |
| [Online_Survey](Online_Survey/) | Online collection code, database setup, and deployment notes |
| [Onboarding_Document_Design.md](Onboarding_Document_Design.md) | Structure of the intent-based document |

### Material files used in the study

- Code: [module.spec.ts](Baseline_Documents/module.spec/module.spec.ts).
- B: the **Generated Document** section of [prompt3_baseline.md](Baseline_Documents/module.spec/prompt3_baseline.md).
- C: [intent_onboarding.md](Comparison_Set/module.spec/intent_onboarding.md).

The HTML files contain the material shown to participants. Both document conditions use the same neutral heading, **Supporting material**.

## Earlier preparation records

`Baseline_Documents` also contains other prompt variants. `Comparison_Set` contains other suites and earlier comparison documents. These files are retained as preparation records; they were not all used in the current survey.

[Baseline_Generation_Prompt.md](Baseline_Generation_Prompt.md) records the earlier onboarding-style baseline setup. It is distinct from the summary prompt selected for condition B.

Survey results are maintained separately in `Survey_Results`.
