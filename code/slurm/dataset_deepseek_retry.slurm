#!/bin/bash
#SBATCH --gres=gpu:A100-SXM4-80GB:1
#SBATCH --time=01:30:00
#SBATCH --mem=128GB
#SBATCH --cpus-per-task=32
#SBATCH --job-name=deepseek_retry
#SBATCH --output=deepseek_retry_%A_%a.out


TASK_ROOT="${PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}"
if [[ -f "$TASK_ROOT/code/main.py" ]]; then
    TASK_ROOT="$TASK_ROOT/code"
fi
source "$TASK_ROOT/slurm/job_env.sh"

export MODEL_TYPE=7b
export EXTRACT_MODE=independent
export INFERENCE_BACKEND=local
export RUN_KIND="${RUN_KIND:-retry}"
export RETRY_REASON="${RETRY_REASON:-runtime_failure}"
source "$PROJECT_ROOT/slurm/dataset_job.sh"

