#!/bin/bash -l
#SBATCH --nodes=2
#SBATCH --ntasks=40
#SBATCH --time=00:10:00
#SBATCH --partition=workq
#SBATCH --export=NONE

module load singularity
module load cray-mpich

export OMP_NUM_THREADS=1
export SINGULARITY_CACHEDIR=/group/askap/lah00b/learn/singularity

srun --export=all --mpi=pmi2 -N 2 -n 40 singularity exec testmpi_latest.sif /home/testmpi/mpi_check

