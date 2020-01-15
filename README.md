# Testing MPI implementations inside Docker / Singularity container
This package tests various implementations of MPI inside Singularity containers derived directly from Docker images.
Two major implementations are tested here: MPICH and OpenMPI.
Package contents:
* Source code `mpi_check.c` and `Makefile`
* Python script `master.py` to automatically create Docker images of various MPI implementations, 
  as well as samples of job scheduling batch files for an HPC system (`*.sbatch`).

## MPICH
It has ABI (Application Binary Interface) compatibility across multiple versions and vendors.
More information can be found here: https://www.mpich.org/abi/

## OpenMPI
Compatibility is guaranteed within a major version number, where a version number is given as: `major.minor.release`.
There are a number of versions:
* Current at the time of writing (December 2019): `4.x`
* Still supported by OpenMPI: `3.x`
* No longer supported: `2.x` and `1.x`
More information on this can be found here: https://www.open-mpi.org/software/ompi/versions/

## How to use
### Using a pre-built Docker image
This is the simplest way.
1. Pull one of these pre-built Docker images from DockerHub and turn it into Singularity container:
```
singularity pull docker://lahur/testmpich
singularity pull docker://lahur/testopenmpi-4.0.2
singularity pull docker://lahur/testopenmpi-3.1.4
singularity pull docker://lahur/testopenmpi-2.1.6
```
2. Run the command within the container
For example, on Pearcey, depending on the MPI implmentation, run one of these batch files.
```
sbatch pearcey-mpich.sbatch
sbatch pearcey-openmpi-4.0.2.sbatch
sbatch pearcey-openmpi-3.1.4.sbatch
sbatch pearcey-openmpi-2.1.6.sbatch
```

### Building Docker images automatically
The Python script `master.py` can build a number of Docker images automatically.
Inside the file, at the top, there's a section for user settings:
```
mpi_targets = ["mpich", "openmpi-4.0.2", "openmpi-3.1.4", "openmpi-2.1.6"]

target_prepend = "lahur/test"
target_append = ":latest"

dry_run = True

HPC = "pearcey"
```

Note
- `mpi_targets` is a list of MPI targets. Modify this to build different target.
- The name of Docker image created will be in this format:
`target_prepend` `target` `target_append`. 
For example: `lahur/testopenmpi-4.0.2:latest`.
- Set `dry_run` to `False` if you want to actually build the image. Otherwise only Dockerfiles and sample batch files are produced.
- `HPC` is the name of HPC that will be prepended to sample batch files.

Executing the script is simple.
```
python master.py
```
The script will create the necessary Dockerfiles, build the images, and make samples of SLURM batch files.

### Building Docker image manually
To build Docker image manually, you can modify the existing Dockerfiles. Then run the build command.
```
docker build -t my_dockerHub_account/my_docker_image:image_tag -f my_dockerfile .
```

### Sharing Docker image
If you wish to use the image on another machine, push the Docker image to your account in DockerHub. 
```
docker push my_dockerHub_account/my_docker_image:image_tag
```
Then pull it from the target machine as a singularity object.
```
singularity pull docker://my_dockerHub_account/my_docker_image:image_tag
```

## Links
- Website for this project: <https://prlahur.github.io/testmpi/>
- CSIRO <https://www.csiro.au/>
