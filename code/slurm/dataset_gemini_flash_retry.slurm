#!/bin/bash
#SBATCH --gres=gpu:A100-SXM4-80GB:1
#SBATCH --time=02:00:00
#SBATCH --mem=32GB
#SBATCH --cpus-per-task=8
#SBATCH --job-name=gemini_flash_retry
#SBATCH --output=gemini_flash_retry_%A_%a.out


TASK_ROOT="${PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}"
if [[ -f "$TASK_ROOT/code/main.py" ]]; then
    TASK_ROOT="$TASK_ROOT/code"
fi
source "$TASK_ROOT/slurm/job_env.sh"

export MODEL_TYPE=qwen
export EXTRACT_MODE=independent
export INFERENCE_BACKEND=api
export GEMINI_MODEL=gemini-2.5-flash
export RUN_KIND="${RUN_KIND:-retry}"
export RETRY_REASON="${RETRY_REASON:-}"
source "$PROJECT_ROOT/slurm/dataset_job.sh"

