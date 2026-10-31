#!/bin/bash
#SBATCH --partition=berzelius
#SBATCH --gpus=1
#SBATCH --time=02:00:00
#SBATCH --mem=32GB
#SBATCH --cpus-per-task=8
#SBATCH --job-name=download_qwen
#SBATCH --output=download_qwen_%j.out

TASK_ROOT="${PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}"
if [[ -f "$TASK_ROOT/code/main.py" ]]; then
    TASK_ROOT="$TASK_ROOT/code"
fi
source "$TASK_ROOT/slurm/job_env.sh"

exec "$PYTHON_BIN" "$PROJECT_ROOT/slurm/download_model.py"

