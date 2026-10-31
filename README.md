# ICST_TestIntent

Code, data, and examples for the Test Intent study. Test Intent represents the verification expressed by a test artifact through **Test Objects**, **Test Goal**, and **Test Activities**.

## Contents

| Path | Contents |
|---|---|
| [code/](code/) | Extraction framework, model backends, scripts, and SLURM jobs |
| [Data/Test_Suite/](Data/Test_Suite/) | Test suite sources |
| [Data/Groundtruth/](Data/Groundtruth/) | Ground Truth for 210 test cases from 98 source files |
| [Data/LLM_Extraction/](Data/LLM_Extraction/) | Extraction outputs and case-level versions |
| [Data/Comparison_Results/](Data/Comparison_Results/) | Alignment judgments |
| [Data/Peer_Review/](Data/Peer_Review/) | Peer-review records |
| [Data/RQ2_Samples/](Data/RQ2_Samples/) | Qualitative samples and case judgments |
| [Data/Onboarding_Evaluation/](Data/Onboarding_Evaluation/) | Survey instruments, materials, implementation, and responses |
| [Examples.md](Examples.md) | Worked examples of Test Intent |

Onboarding survey materials: [A: code only](Data/Onboarding_Evaluation/Survey_HTML/survey_module.spec_A.html), [B: code and baseline summary](Data/Onboarding_Evaluation/Survey_HTML/survey_module.spec_B.html), and [C: code and Intent Onboarding Document](Data/Onboarding_Evaluation/Survey_HTML/survey_module.spec_C.html).

## Run

```bash
cd code
python -m pip install -r requirements.txt
INFERENCE_BACKEND=local MODEL_TYPE=qwen python main.py \
  --test-file ../Data/Test_Suite/playwright/module.spec.ts --mode independent
```

Models: DeepSeek 7B, Qwen 3.5-27B, Gemini 2.5 Flash, and Gemini 3.1 Pro. Workflows: Independent, Combined, and Chained Extraction.

See [model and batch-run options](code/MODEL_SWITCHING.md).

