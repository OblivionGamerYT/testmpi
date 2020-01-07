# Make multiple Docker images with different target MPI implementations.
# Author: Paulus Lahur
#
#------------------------------------------------------------------------------
# SETTINGS
#
# Set target MPI implementations here.
# How to write the target:
# - MPICH must be written this way: "mpich".
# - OpenMPI must be in this format: "openmpi-X.Y.Z", where X, Y and Z are
#   version's major, minor and revision number, respectively
# Note that the targets are set internally rather than externally 
# (ie. as arguments) for these reasons:
# - Minimise error checking
# - The target will be passed on as argument in shell commands.
#   Bad target might be mistaken as another command.

mpi_targets = ["mpich", "openmpi-4.0.2", "openmpi-3.1.4", "openmpi-2.1.6"]

# Docker image name is in this format: 
# target_prepend + mpi_target + target_append

target_prepend = "lahur/test"
target_append = ":latest"

# Set True if this is just a dry run. No Docker image will be created.

dry_run = True

#------------------------------------------------------------------------------
# CODE

import subprocess

print("There are", len(mpi_targets), "MPI targets")

print("Making Dockerfiles for all targets ...")

dockerfiles = []

common_top_part = (
"# This file is automatically created by " + __file__ + "\n"
"FROM ubuntu:latest\n"
"RUN apt-get update\n"
"RUN apt-get upgrade -y\n"
"RUN apt-get autoremove -y\n"
"RUN apt-get install -y git\n"
"RUN apt-get install -y make\n")

common_bottom_part = (
"WORKDIR /home\n"
"RUN git clone https://github.com/prlahur/testmpi.git\n"
"WORKDIR /home/testmpi\n"
"RUN make\n")

for mpi_target in mpi_targets:
    dockerfile = "Dockerfile-" + mpi_target
    dockerfiles.append(dockerfile)
    print("Making Dockerfile:", dockerfile)

    if (mpi_target == "mpich"):
        mpi_part = "RUN apt-get install -y mpich\n"

    elif (mpi_target[0:8] == "openmpi-"):
        # Note that OpenMPI is more complicated than MPICH, because:
        # - There are multiple versions
        # - OpenMPI must be built from the source code
        # - The source code must be downloaded from OpenMPI website first
        # - The version dictates the directory it is downloaded from

        openmpi_common_top_part = (
        "RUN apt-get install -y wget\n"
        "RUN apt-get install -y g++\n"
        "WORKDIR /home\n")

        openmpi_common_bottom_part = (
        "RUN ./configure --prefix=\"/home/$USER/.openmpi\"\n"
        "RUN make all install\n"
        "ENV PATH=$PATH:/home/$USER/.openmpi/bin\n"
        "ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/$USER/.openmpi/lib/:/usr/local/lib\n")

        openmpi_ver = mpi_target[8:]

        # Directory name for OpenMPI download
        openmpi_dir = "https://download.open-mpi.org/release/open-mpi/v" + openmpi_ver[0:3]

        # TODO: Check whether this file exist

        openmpi_version_part = (
        "RUN wget " + openmpi_dir + "/" + mpi_target + ".tar.gz\n"
        "RUN gunzip " + mpi_target + ".tar.gz\n"
        "RUN tar -xvf " + mpi_target + ".tar\n"
        "WORKDIR /home/" + mpi_target + "\n")

        mpi_part = openmpi_common_top_part + openmpi_version_part + openmpi_common_bottom_part

    else:
        print("ERROR: unknown MPI target: ", mpi_target)
        quit()


    f = open(dockerfile, "w")
    f.write(common_top_part + mpi_part + common_bottom_part)
    f.close()


if dry_run:
    print("This is a dry run. No Docker image will be created")
else:
    print("Making Docker images for all targets ...")

for mpi_target in mpi_targets:
    dockerfile = "Dockerfile-" + mpi_target
    target = target_prepend + mpi_target + target_append
    docker_command = "docker build -t " + target + " -f " + dockerfile + " ."
    if dry_run:
        subprocess.run("echo " + docker_command, shell=True)
    else:
        subprocess.run(docker_command, shell=True)
