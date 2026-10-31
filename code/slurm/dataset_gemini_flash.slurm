#!/bin/bash
#SBATCH --partition=berzelius
#SBATCH --gres=gpu:A100-SXM4-80GB:1
#SBATCH --time=02:00:00
#SBATCH --mem=32GB
#SBATCH --cpus-per-task=8
#SBATCH --job-name=dataset_gemini_flash
#SBATCH --output=dataset_gemini_flash_%A_%a.out
#SBATCH --array=0-97%10


TASK_ROOT="${PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}"
if [[ -f "$TASK_ROOT/code/main.py" ]]; then
    TASK_ROOT="$TASK_ROOT/code"
fi
source "$TASK_ROOT/slurm/job_env.sh"

export MODEL_TYPE=qwen
export EXTRACT_MODE=independent
export INFERENCE_BACKEND=api
export GEMINI_MODEL=gemini-2.5-flash
export RUN_KIND="${RUN_KIND:-primary}"
export RETRY_REASON="${RETRY_REASON:-}"
source "$PROJECT_ROOT/slurm/dataset_job.sh"

