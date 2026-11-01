#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --time=04:00:00
#SBATCH --mem=16GB
#SBATCH --cpus-per-task=4
#SBATCH --job-name=dataset_gemini_pro
#SBATCH --output=dataset_gemini_pro_%A_%a.out
#SBATCH --array=0-97%5


TASK_ROOT="${PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}"
if [[ -f "$TASK_ROOT/code/main.py" ]]; then
    TASK_ROOT="$TASK_ROOT/code"
fi
source "$TASK_ROOT/slurm/job_env.sh"

export MODEL_TYPE=qwen
export EXTRACT_MODE=independent
export INFERENCE_BACKEND=api
export GEMINI_MODEL=gemini-3.1-pro-preview
export GOOGLE_CLOUD_LOCATION=global
export RUN_KIND="${RUN_KIND:-primary}"
export RETRY_REASON="${RETRY_REASON:-}"
source "$PROJECT_ROOT/slurm/dataset_job.sh"

