#!/bin/bash
#SBATCH --partition=berzelius
#SBATCH --gres=gpu:A100-SXM4-80GB:1
#SBATCH --time=01:30:00
#SBATCH --mem=128GB
#SBATCH --cpus-per-task=32
#SBATCH --job-name=combined_missing
#SBATCH --output=combined_missing_%A_%a.out
#SBATCH --exclude=node061

# Dataset jobs: submit with python slurm/submit_dataset_jobs.py dataset_combined_missing.slurm.
# Arrays address source files; each source is split into case-level records.

TASK_ROOT="${PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}"
if [[ -f "$TASK_ROOT/code/main.py" ]]; then
    TASK_ROOT="$TASK_ROOT/code"
fi
source "$TASK_ROOT/slurm/job_env.sh"

export MODEL_TYPE=qwen
export EXTRACT_MODE=combined
export INFERENCE_BACKEND=local
export RUN_KIND="${RUN_KIND:-retry}"
export RETRY_REASON="${RETRY_REASON:-missing_output}"
# Reruns preserve first-run outputs and write into a separate run directory.
source "$PROJECT_ROOT/slurm/dataset_job.sh"

