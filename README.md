# Testing MPI implementations inside Singularity container

This package tests various implementations of MPI inside Singularity containers derived directly from Docker images.
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
### Using a pre-built Docker image
This is the simplest way.
1. Pull one of these pre-built Docker images from DockerHub and turn it into Singularity container:
```
singularity pull docker://lahur/testmpich
singularity pull docker://lahur/openmpi-3.1.4
singularity pull docker://lahur/openmpi-4.0.2
```
2. Run the command within the container
For example, on Pearcey, depending on the MPI implmentation, run one of these batch files.
```
batch pearcey-mpich.sbatch
batch pearcey-openmpi-3.1.4.sbatch
batch pearcey-openmpi-4.0.2.sbatch
```

### Building Docker image
There are cases where you need to modify something, such as for checking OpenMPI version not available in pre-built images. To build your own Docker image, you might need to modify Dockerfile. Then run the build command.
```
docker build -t my_dockerHub_account/my_docker_image:image_tag -f my_dockerfile .
```
If you wish to use the image on another machine, push the Docker image to your account in DockerHub. 
```
docker push my_dockerHub_account/my_docker_image:image_tag
```
Then pull it from the target machine as a singularity object.
```
singularity pull docker://my_dockerHub_account/my_docker_image:image_tag
```

### Building Singularity image
This will be added later, if required.

## Extension
This package can be extended to testing other aspects of container on HPC, such as IO load from within container.
