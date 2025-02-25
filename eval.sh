#!/bin/bash
#SBATCH --gpus 4
#SBATCH -t 6:00:00
#SBATCH -A berzelius-2024-286
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user olivewry@gmail.com
#SBATCH -o /proj/cloudrobotics-nest/users/x_ruiwa/corl/pusht/diffusion_cnn/r3m_finetune/slurm-%A.out
#SBATCH -e /proj/cloudrobotics-nest/users/x_ruiwa/corl/pusht/diffusion_cnn/r3m_finetune/slurm-%A.err

module load Anaconda/2023.09-0-hpc1-bdist

cd /home/x_ruiwa/nppc

conda activate nppc

# usage: ./eval.sh change the problem idx to run different problems

# Define arguments
SEED=42
MODEL="deepseek"
N_SHOTS=3
N_TRIALS=100
ASY_BATCH_SIZE=8
RESULT_FOLDER="results"
OFFLINE_EVAL="--offline_eval"
DEBUG=""
PROBLEM_IDX=2

PROBLEM_NAME=$(python -c "
from nppc_problem import problem2path
print(list(problem2path)[$PROBLEM_IDX])
")
echo "Running NPPC for problem: $PROBLEM_NAME"

# Check if the problem name is provided
if [ -z "$PROBLEM_NAME" ]; then
    echo "Error: No problem name provided."
    echo "Usage: ./run_nppc.sh \"3-Satisfiability (3-SAT)\""
    exit 1
fi

# Get levels dynamically from nppc_problem.py
LEVELS=$(python -c "
import sys
from nppc_problem import problem_levels

problem_name = sys.argv[1]
if problem_name in problem_levels:
    print(' '.join(map(str, problem_levels[problem_name].keys())))
else:
    sys.exit(1)
" "$PROBLEM_NAME")

# Check if levels were retrieved successfully
if [ $? -ne 0 ] || [ -z "$LEVELS" ]; then
    echo "Error: Invalid problem name or failed to retrieve levels from nppc_problem.py."
    exit 1
fi

# Loop through levels and run main_nppc_batch_offline.py
for LEVEL in $LEVELS; do
    echo "Running NPPC Evaluation for $PROBLEM_NAME at Level $LEVEL..."
    python main_nppc_batch_offline.py \
        --seed $SEED \
        --model $MODEL \
        --problem "$PROBLEM_IDX" \
        --level $LEVEL \
        --n_shots $N_SHOTS \
        --n_trials $N_TRIALS \
        --asy_batch_size $ASY_BATCH_SIZE \
        --result_folder $RESULT_FOLDER \
        $OFFLINE_EVAL \
        $DEBUG
done

echo "All levels for $PROBLEM_NAME have been evaluated."