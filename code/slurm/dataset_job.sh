#!/bin/bash
set -euo pipefail

if [[ "${RUN_KIND:-primary}" != "primary" && -z "${MANIFEST_PATH:-}" ]]; then
    echo "Retry jobs require a selection manifest from submit_dataset_jobs.py." >&2
    exit 2
fi

MANIFEST_PATH="${MANIFEST_PATH:-$PROJECT_ROOT/slurm/test_suite_manifest.json}"
DATASET_STAGE="${DATASET_STAGE:-validated}"
RUN_KIND="${RUN_KIND:-primary}"
RETRY_REASON="${RETRY_REASON:-}"

if [[ "$RUN_KIND" != "primary" && -z "$RETRY_REASON" ]]; then
    echo "Retry jobs require a recorded reason; use slurm/submit_dataset_jobs.py." >&2
    exit 2
fi

exec "$PYTHON_BIN" "$PROJECT_ROOT/run_dataset.py" \
    --manifest "$MANIFEST_PATH" \
    --task-index "${SLURM_ARRAY_TASK_ID:?Submit this job as an array}" \
    --mode "${EXTRACT_MODE:?}" \
    --stage "$DATASET_STAGE" \
    --run-kind "$RUN_KIND" \
    --retry-reason "$RETRY_REASON" \
    --output-root "${OUTPUT_ROOT:-$PROJECT_ROOT/Result/dataset}"

