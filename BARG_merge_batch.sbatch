#!/bin/bash
#SBATCH --job-name=create_BARG_disdrometer_merged_product
#SBATCH --partition=slurm
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=7-00:00:00
#SBATCH --output=/rcfs/projects/oracle/gold396/logs/create_BARG_merge_%j.out
#SBATCH --error=/rcfs/projects/oracle/gold396/logs/create_BARG_merge_%j.err

set -euo pipefail

SCRIPT_DIR="/rcfs/projects/oracle/gold396"
PYTHON="/rcfs/projects/oracle/.venv/bin/python"

mkdir -p "${SCRIPT_DIR}/logs"

"${PYTHON}" "${SCRIPT_DIR}/BARG_merge_file_create.py"

"${PYTHON}" "${SCRIPT_DIR}/tokay_correction.py" "/rcfs/projects/oracle/gold396/BARG" "/rcfs/projects/oracle/gold396/BARG_filtered"


echo "All Done."


# print out job info
scontrol show job $SLURM_JOB_ID
