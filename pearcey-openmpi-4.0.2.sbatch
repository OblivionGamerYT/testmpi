#!/bin/bash -l
#SBATCH --ntasks=20
#SBATCH --time=00:10:00

module load singularity/3.5.0
module load openmpi/4.0.2-ofed45-gcc

mpirun -n 20 -oversubscribe singularity exec testopenmpi-4.0.2_latest.sif /home/testmpi/mpi_check

