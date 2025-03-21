#!/bin/bash
#SBATCH --gpus 4
#SBATCH -t 6:00:00
#SBATCH -A Berzelius-2025-50
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=olivewry@gmail.com
#SBATCH -o /proj/cloudrobotics-nest/users/x_ruiwa/nppc_logs/slurm-%A.out
#SBATCH -e /proj/cloudrobotics-nest/users/x_ruiwa/nppc_logs/slurm-%A.err

module load Anaconda/2023.09-0-hpc1-bdist

cd /home/x_ruiwa/nppc
conda activate nppc

# Define arguments
SEEDS=(42 53 64)
MODEL="deepseek-r1-32"
N_SHOTS=1
N_TRIALS=2
BATCH_SIZE=2
RESULT_FOLDER="results"
DEBUG=""
PROBLEM_IDX=1

# Get the problem name using Python
PROBLEM_NAME=$(python -c "
from npgym.configs import PROBLEM2PATH
print(list(PROBLEM2PATH.keys())[$PROBLEM_IDX])
")

echo "Running NPPC for problem: $PROBLEM_NAME"

# Check if the problem name is valid
if [ -z "$PROBLEM_NAME" ]; then
    echo "Error: No problem name found for index $PROBLEM_IDX."
    exit 1
fi

# Get the available levels for the selected problem
LEVELS=$(python -c "
import sys
from npgym.configs import PROBLEM_LEVELS
problem_name = sys.argv[1]
if problem_name in PROBLEM_LEVELS:
    print(' '.join(map(str, PROBLEM_LEVELS[problem_name].keys())))
else:
    sys.exit(1)
" "$PROBLEM_NAME")

# LEVELS=(2, 3, 4, 5, 6, 7, 8, 9, 10, 11)

# Check if levels were found
if [ $? -ne 0 ] || [ -z "$LEVELS" ]; then
    echo "Error: Invalid problem name or failed to retrieve levels."
    exit 1
fi

# Run evaluation for each seed and level
for SEED in "${SEEDS[@]}"; do
    for LEVEL in $LEVELS; do
        echo "Running NPPC Evaluation for $PROBLEM_NAME | Level $LEVEL | Seed $SEED | Model $MODEL | N-Shots $N_SHOTS | N-Trials $N_TRIALS"
        python main_nppc_final.py \
            --seed "$SEED" \
            --model "$MODEL" \
            --problem "$PROBLEM_IDX" \
            --level "$LEVEL" \
            --n_shots "$N_SHOTS" \
            --n_trials "$N_TRIALS" \
            --batch_size "$BATCH_SIZE" \
            --result_folder "$RESULT_FOLDER" \
            $DEBUG
    done
done

echo "Finished evaluating all levels for $PROBLEM_NAME"