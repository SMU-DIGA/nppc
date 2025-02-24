#!/bin/bash
#SBATCH --gpus 4
#SBATCH -t 3:00:00
#SBATCH -A berzelius-2024-286
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user olivewry@gmail.com
#SBATCH -o /proj/cloudrobotics-nest/users/x_ruiwa/corl/pusht/diffusion_cnn/r3m_finetune/slurm-%A.out
#SBATCH -e /proj/cloudrobotics-nest/users/x_ruiwa/corl/pusht/diffusion_cnn/r3m_finetune/slurm-%A.err

module load Anaconda/2023.09-0-hpc1-bdist

cd /home/x_ruiwa/nppc

conda activate nppc

python main_offline.py 