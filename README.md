# ICST_TestIntent

This repository contains the code, data, and examples for the Test Intent study. Test Intent describes the verification expressed by a test artifact through **Test Objects**, **Test Goal**, and **Test Activities**.

## Data

The dataset contains **210 test cases from 98 source files**, covering unit, integration, API, browser automation, performance, and BDD testing.

| Directory | Contents |
|---|---|
| [Data/Test_Suite/](Data/Test_Suite/) | Test suite sources, organized by framework |
| [Data/Test_Case/](Data/Test_Case/) | Individual test cases with their source context, organized by framework |
| [Data/Groundtruth/](Data/Groundtruth/) | Reference Test Objects, Test Goal, and Test Activities, stored per test case |
| [Data/LLM_Extraction/](Data/LLM_Extraction/) | Case-level Test Intent results for workflow and model comparisons, organized by model and prompting workflow |
| [Data/Comparison_Results/](Data/Comparison_Results/) | Case-level alignment judgments and summary statistics in `manual_review.xlsx` |
| [Data/Peer_Review/](Data/Peer_Review/) | Researcher review records, labels, and revision information in `peer_review.xlsx` |
| [Data/RQ2_Samples/](Data/RQ2_Samples/) | Samples organized by workflow, model, and testing category, with pattern judgments in `Case_Judgments.xlsx` |
| [Data/Onboarding_Evaluation/](Data/Onboarding_Evaluation/) | Baseline and intent-based documents, survey questions, study materials, online survey implementation, and participant responses |

The onboarding evaluation compares three conditions. Their questionnaires and materials are available in:

- [A: test code only](Data/Onboarding_Evaluation/Survey_HTML/survey_module.spec_A.html)
- [B: test code and a baseline summary](Data/Onboarding_Evaluation/Survey_HTML/survey_module.spec_B.html)
- [C: test code and an Intent Onboarding Document](Data/Onboarding_Evaluation/Survey_HTML/survey_module.spec_C.html)

## Code

The extraction framework uses five layers. Model backends, supporting scripts, batch jobs, and regression tests are stored alongside them.

| Directory | Purpose |
|---|---|
| [code/layers/input/](code/layers/input/) | Read test artifacts, split suites into cases, and retain their context |
| [code/layers/extract/](code/layers/extract/) | Extract Test Objects, Test Goal, and Test Activities using Independent, Combined, or Chained Extraction |
| [code/layers/intent/](code/layers/intent/) | Validate extracted intent, retry failed extractions, and adjust description granularity |
| [code/layers/business/](code/layers/business/) | Group test cases and generate onboarding documents from Test Intent |
| [code/layers/output/](code/layers/output/) | Render and save output documents |
| [code/model/](code/model/) | Local model loading and Gemini API inference |
| [code/scripts/](code/scripts/) | Candidate test-file collection and Markdown-to-Word conversion |
| [code/slurm/](code/slurm/) | SLURM submission scripts, the source manifest, and batch-run configuration |
| [code/tests/](code/tests/) | Regression checks for extraction, semantic processing, and batch jobs |

Main entry points:

- [`extract_for_comparison.py`](code/extract_for_comparison.py) runs the workflow and model comparisons using only the Input and Extract layers. Each case is extracted separately, and cases from the same source file are saved in one suite JSON. Semantic validation, re-extraction, granularity adjustment, and onboarding generation are excluded from this workflow.
- [`main.py`](code/main.py) processes a test file or suite and generates an onboarding report.

The published comparison files in `Data/LLM_Extraction/` contain suite metadata and a `test_cases` list with `objects`, `goals`, and `activities` for each case. New runs of `extract_for_comparison.py` also save raw model responses and the generation token limit.

## Run

Install the dependencies and run extraction for the comparisons using Qwen 3.5-27B with Independent Extraction:

```bash
cd code
python -m pip install -r requirements.txt

python extract_for_comparison.py \
  --test-file ../Data/Test_Suite/playwright/module.spec.ts \
  --mode independent --backend local --model qwen \
  --output Result/comparison/Qwen3.5-27B/Independent/playwright/module.specIntent.json
```

Use `--mode independent`, `--mode combined`, or `--mode chain` to select the prompting workflow.

For onboarding document generation, run the full pipeline:

```bash
INFERENCE_BACKEND=local MODEL_TYPE=qwen python main.py \
  --test-file ../Data/Test_Suite/playwright/module.spec.ts --mode independent
```

The evaluated models are DeepSeek 7B, Qwen 3.5-27B, Gemini 2.5 Flash, and Gemini 3.1 Pro. See [MODEL_SWITCHING.md](code/MODEL_SWITCHING.md) for model configuration, comparison commands, and optional manifest-based batch and SLURM commands.

## Examples

[Examples.md](Examples.md) presents five worked examples covering unit, integration, performance, manual, and BDD test artifacts.


