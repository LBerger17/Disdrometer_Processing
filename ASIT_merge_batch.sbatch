#!/bin/bash
#SBATCH --job-name=create_ASIT_disdrometer_merged_product
#SBATCH --partition=slurm
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=7-00:00:00
#SBATCH --output=/rcfs/projects/oracle/gold396/logs/create_ASIT_202508_%j.out
#SBATCH --error=/rcfs/projects/oracle/gold396/logs/create_ASIT_202508_%j.err

set -euo pipefail

SCRIPT_DIR="/rcfs/projects/oracle/gold396"
PYTHON="/rcfs/projects/oracle/.venv/bin/python"

mkdir -p "${SCRIPT_DIR}/logs"

for year_month in 2024-{07..12} 2025-{01..08}; do
    year=${year_month%-*}
    month=${year_month#*-}

    "${PYTHON}" "${SCRIPT_DIR}/ASIT_merge_file_create.py" \
        --year "$year" --month "$month"
done


"${PYTHON}" "${SCRIPT_DIR}/tokay_correction.py" "/rcfs/projects/oracle/gold396/ASIT" "/rcfs/projects/oracle/gold396/ASIT_filtered"

echo "All Done."


# print out job info
scontrol show job $SLURM_JOB_ID
