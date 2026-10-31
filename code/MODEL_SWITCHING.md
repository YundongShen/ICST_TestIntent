# Model Switching

Run the commands below from the repository's `code/` directory:

```bash
cd code
python -m pip install -r requirements.txt
```

The extraction framework uses pretrained models without task-specific training.
The default local model is Qwen 3.5-27B. The default prompting workflow is Independent Extraction.

## Models used in the study

| Model | Backend | Configuration |
|---|---|---|
| DeepSeek 7B | Local, FP16 | `MODEL_TYPE=7b` |
| Qwen 3.5-27B | Local, BF16 | `MODEL_TYPE=qwen` |
| Gemini 2.5 Flash | Gemini API | `GEMINI_MODEL=gemini-2.5-flash` |
| Gemini 3.1 Pro | Gemini API | `GEMINI_MODEL=gemini-3.1-pro-preview` |

The local checkpoint IDs are `deepseek-ai/deepseek-llm-7b-chat` and
`Qwen/Qwen3.5-27B`. The API model IDs above identify the requested API models;
the Pro configuration uses the preview model ID.

## Local inference

Qwen 3.5-27B:

```bash
INFERENCE_BACKEND=local MODEL_TYPE=qwen python main.py \
  --test-file ../Data/Test_Suite/playwright/module.spec.ts --mode independent
```

DeepSeek 7B:

```bash
INFERENCE_BACKEND=local MODEL_TYPE=7b python main.py \
  --test-file ../Data/Test_Suite/playwright/module.spec.ts --mode independent
```

Local models are loaded on the first inference request. Their configuration files
specify the checkpoint and local model directory. Qwen's local directory can also
be set with `MODEL_PATH`.

## Gemini API inference

Set `GOOGLE_API_KEY` or `VERTEX_API_KEY` in the environment before running an API
command. The service uses the Vertex client when `VERTEX_API_KEY` is set.

Gemini 2.5 Flash:

```bash
INFERENCE_BACKEND=api GEMINI_MODEL=gemini-2.5-flash python main.py \
  --test-file ../Data/Test_Suite/playwright/module.spec.ts --mode independent
```

Gemini 3.1 Pro:

```bash
GOOGLE_CLOUD_LOCATION=global INFERENCE_BACKEND=api \
GEMINI_MODEL=gemini-3.1-pro-preview python main.py \
  --test-file ../Data/Test_Suite/playwright/module.spec.ts --mode independent
```

## Prompting workflows

Set `--mode` to `independent`, `combined`, or `chain`.

- Independent extracts each element from the complete test artifact in a separate call.
- Combined extracts the three elements in one call.
- Chained extracts Objects, then Goal with Objects as context, then Activities with
  Objects and Goal as context.

All three workflows use the same definitions and extraction rules in
`layers/extract/prompts.py`. The workflow comparison uses Qwen 3.5-27B.
The model comparison uses Independent Extraction.

## Entry points and processing stages

`main.py` splits the source into cases, extracts Test Intent, performs semantic
validation and granularity adjustment, and generates an onboarding report.
A failed semantic check triggers re-extraction up to the configured limit.
A result that still fails validation does not reach report generation.
Granularity adjustment changes the level of description while checking that
verification meaning is preserved.

The main command also supports:

- `--extract-only`: run Input and Extract without semantic processing or report generation.
- `--no-adjust`: validate the extracted intent without changing granularity.
- `--object-level`, `--goal-level`, and `--activity-level`: request granularity
  for selected elements, from 0 (specific) to 1 (general).
- `--merge-activities`: permit adjacent related activities to be grouped during adjustment.
- `--max-reextract`: set the semantic validation retry limit; the default is 2.

`run_dataset.py` processes one source entry from the versioned dataset manifest.
`extract_for_dataset.py` provides the same command as an alternate entry point:

```bash
INFERENCE_BACKEND=local MODEL_TYPE=qwen python extract_for_dataset.py \
  --task-index 0 --mode independent --stage validated
```

The dataset runner always retains the initial raw extraction.
With `--stage validated`, it also saves the semantic processing result and records
each extraction attempt. With `--stage raw`, it saves the initial extraction only.
These stages are identified in the output metadata. The raw and validated results
must be interpreted according to their recorded stage.

## SLURM jobs

The source manifest contains 98 test files that split into 210 test cases.
The submission helper derives array bounds from the selected source files:

```bash
python slurm/submit_dataset_jobs.py submit_dataset_extraction.slurm --dry-run
```

Remove `--dry-run` to submit the job on a configured SLURM system.
Retry jobs require an explicit file list and record their reason.
Reruns use new output directories. Empty-output reruns are recorded as diagnostic runs.

## Environment variables

| Variable | Purpose |
|---|---|
| `INFERENCE_BACKEND` | Select `local` or `api`; the default is `local`. |
| `MODEL_TYPE` | Select local `qwen`, `7b`, or its alias `deepseek`. |
| `GEMINI_MODEL` | Select the API model; set it explicitly for the model being evaluated. |
| `GOOGLE_API_KEY` | Credential for the standard Gemini API client. |
| `VERTEX_API_KEY` | Credential for the Vertex API client. |
| `GOOGLE_CLOUD_LOCATION` | Location configuration supplied to the API environment. |
| `MODEL_PATH` | Override Qwen's local model directory. |
| `EXTRACT_MODE` | Default workflow for `main.py`; `--mode` sets it explicitly. |
| `PROJECT_ROOT` | Path to `code/` when submitting SLURM jobs. |
| `VENV_PATH` | Optional virtual environment used by SLURM jobs. |

