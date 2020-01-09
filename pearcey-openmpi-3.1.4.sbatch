#!/bin/bash -l
## This file is automatically created by master.py
#SBATCH --ntasks=20
#SBATCH --time=00:10:00

module load singularity/3.5.0
module load openmpi/3.1.4-ofed45-gcc

mpirun -n 20 -oversubscribe singularity exec testopenmpi-3.1.4_latest.sif /home/testmpi/mpi_check
