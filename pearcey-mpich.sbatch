#!/bin/bash -l
## This file is automatically created by master.py
#SBATCH --ntasks=20
#SBATCH --time=00:10:00

module load singularity/3.5.0
module load mpich/3.3.0

mpirun -n 20 singularity exec testmpich_latest.sif /home/testmpi/mpi_check
