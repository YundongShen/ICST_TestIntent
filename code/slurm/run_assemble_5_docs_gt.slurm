#!/bin/bash
#SBATCH --partition=berzelius
#SBATCH --gres=gpu:A100-SXM4-80GB:1
#SBATCH --time=00:30:00
#SBATCH --mem=64GB
#SBATCH --cpus-per-task=16
#SBATCH --job-name=assemble_onboarding_gt
#SBATCH --output=assemble_onboarding_gt_%j.out
#SBATCH --exclude=node061

# Onboarding template or test-version job.
TASK_ROOT="${PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}"
if [[ -f "$TASK_ROOT/code/main.py" ]]; then
    TASK_ROOT="$TASK_ROOT/code"
fi
source "$TASK_ROOT/slurm/job_env.sh"

exec "$PYTHON_BIN" "$PROJECT_ROOT/scripts/assemble_5_onboarding_docs_gt_test_generation.py" --groundtruth-dir "${GROUNDTRUTH_DIR:-$PROJECT_ROOT/../Data/Groundtruth}"

