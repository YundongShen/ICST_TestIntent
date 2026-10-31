#!/bin/bash
#SBATCH --partition=berzelius
#SBATCH --gres=gpu:A100-SXM4-80GB:1
#SBATCH --time=00:30:00
#SBATCH --mem=64GB
#SBATCH --cpus-per-task=16
#SBATCH --job-name=onboarding_silermenu
#SBATCH --output=onboarding_silermenu_%j.out
#SBATCH --exclude=node061

# Onboarding template or test-version job.
TASK_ROOT="${PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}"
if [[ -f "$TASK_ROOT/code/main.py" ]]; then
    TASK_ROOT="$TASK_ROOT/code"
fi
source "$TASK_ROOT/slurm/job_env.sh"

exec "$PYTHON_BIN" "$PROJECT_ROOT/scripts/test_onboarding_silermenu.py"

