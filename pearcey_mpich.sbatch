#!/bin/bash -l
#SBATCH --ntasks=40
#SBATCH --time=00:10:00

module load singularity
module load mpich/3.3.0

mpirun -n 40 singularity exec testmpi_latest.sif /home/testmpi/mpi_check
