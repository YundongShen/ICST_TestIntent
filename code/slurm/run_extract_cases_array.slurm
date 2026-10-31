#!/bin/bash
#SBATCH --partition=berzelius
#SBATCH --gres=gpu:A100-SXM4-80GB:1
#SBATCH --time=01:30:00
#SBATCH --mem=64GB
#SBATCH --cpus-per-task=16
#SBATCH --array=0-30%10
#SBATCH --job-name=extract_case_onboarding
#SBATCH --output=extract_case_onboarding_%A_%a.out
#SBATCH --exclude=node061

TASK_ROOT="${PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}"
if [[ -f "$TASK_ROOT/code/main.py" ]]; then
    TASK_ROOT="$TASK_ROOT/code"
fi
source "$TASK_ROOT/slurm/job_env.sh"

exec "$PYTHON_BIN" "$PROJECT_ROOT/scripts/extract_one_case_for_onboarding_test_version.py" --task-index "${SLURM_ARRAY_TASK_ID:?Submit as an array with indices 0-30}"

