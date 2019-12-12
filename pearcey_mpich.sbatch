#!/bin/bash -l
#SBATCH --nodes=2
#SBATCH --ntasks=40
#SBATCH --time=00:10:00

module load singularity
module load mpich/3.3.0

mpirun -N 2 -n 40 singularity exec testmpi_latest.sif /home/testmpi/mpi_check

