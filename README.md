# Testing MPI implementations inside Docker container

This package tests various implementations of MPI inside Docker container.
Two major implementations are tested here: MPICH and OpenMPI.
Package contents:
* Source code (`mpi_check.c`) and `Makefile`
* Dockerfiles for building Docker images of various MPI implementations (`Dockerfile-*`)
* Samples of job scheduling batch files for a number of HPC systems (`*.sbatch`)

## MPICH
It has ABI (Application Binary Interface) compatibility across multiple versions and vendors.
More information can be found here: [https://www.mpich.org/abi/]

## OpenMPI
Compatibility is guaranteed within a major version number, where a version number is given as: `major.minor.release`.
There are a number of versions:
* Current at the time of writing (December 2019): 4.x
* Still supported by OpenMPI: 3.x
* No longer supported: 2.x and 1.x
More information on this can be found here: [https://www.open-mpi.org/software/ompi/versions/]

## How to use
### Use a pre-built Docker image
This is the simplest way.
1. Pull a suitable pre-built image from DockerHub using Singularity:
```
singularity pull docker://lahur/testmpich
singularity pull docker://lahur/openmpi-3.1.4
```
2. Run the command within the container

### Build Docker image
There are cases where you need to modify something, such as checking OpenMPI version not available in pre-built images. To build your own Docker image, you might need to modify Dockerfile.
```
docker build -t my_docker_image -f my_dockerfile .
```
If you wish to use the image on another machine, push the Docker image to your account in DockerHub. Then pull it from the target machine.

## TO DO
* More detailed steps

## Miscellaneous
* This package can be extended to testing IO load from within container.
