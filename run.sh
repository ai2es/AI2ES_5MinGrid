#!/usr/bin/bash

#SBATCH --job-name=lightning
#SBATCH --ntasks=1
#SBATCH --mail-type=ALL
#SBATCH -p normal
#SBATCH --mem=28G
<<<<<<< HEAD
#SBATCH -t 12:00:00
=======
#SBATCH -t 00:30:00
>>>>>>> 44484fee9563840a465c0080309888fbbf906562
#SBATCH --mail-user=wrmf@ou.edu
#SBATCH --output=logs/lightning_%A_stdout.txt
#SBATCH --error=logs/lightning_%A_sderr.txt

# cd to directory where job was submitted from
cd $SLURM_SUBMIT_DIR
pwd

# echo the job id to the slurm file
# echo $SLURM_ARRAY_TASK_ID

source activate maps

python -u grid.py
