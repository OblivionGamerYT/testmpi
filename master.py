# Make multiple Docker images with various MPI implementations.
# Make sample batch files for SLURM.
# Author: Paulus Lahur
#
#------------------------------------------------------------------------------
# SETTINGS
#
# Set list of machine targets.
# A valid machine target is either "generic" or specific machine.
# For "generic" machine, you need to further specify MPI targets.
# For specific machine, MPI target is already specified.
# Example:
# machine_targets = ["generic", "galaxy"]
machine_targets = ["galaxy"]

# Set target MPI implementations for "generic" machine.
# A valid mpi target is either "mpich" or OpenMPI
# The latter must be in this format: "openmpi-X.Y.Z", 
# where X, Y and Z are version's major, minor and revision number, respectively.
# Example:
#mpi_targets = ["mpich", "openmpi-4.0.2", "openmpi-3.1.4", "openmpi-2.1.6"]
#mpi_targets = ["mpich-3.3.2"]
mpi_targets = []

# Docker image name is in this format: 
# target_prepend + mpi_target + target_append
image_prepend = "lahur/test"
image_append = ":latest"

# Set True if this is just a dry run. No Docker image will be created.
# Set False to actually create the Docker images.
dry_run = True

# Name for sample batch files (leave empty if not needed)
# sample_batch = "pearcey"
sample_batch = ""

#------------------------------------------------------------------------------
# CODE

class DockerClass:
    def set_file_name(self, file_name):
        self.file_name = file_name

    def set_content(self, content):
        self.content = content

    def set_image(self, image):
        self.image = image

    def write(self):
        '''Write dockerfile'''
        f = open(self.file_name, "w")
        f.write(self.content)
        f.close()


def get_mpi_type_and_version(mpi_name):
    '''
    Given the full name of MPI, return the MPI type: mpich or openmpi
    as well as the version.
    '''
    if (len(mpi_name) > 5):
        if (mpi_name[0:5] == "mpich"):
            return ("mpich", mpi_name[6:])
        elif (mpi_name[0:8] == "openmpi-"):
            return ("openmpi", mpi_name[8:])
        else:
            raise ValueError("Illegal MPI name", mpi_name)
    elif (len(mpi_name) == 5):
        if (mpi_name == "mpich"):
            return("mpich", "")
        else:
            raise ValueError("Illegal MPI name", mpi_name)
    else:
        raise ValueError("Illegal MPI name", mpi_name)


def get_mpi_type(mpi_name):
    '''Given the full name of MPI, return the type: MPICH or OpenMPI'''
    if (mpi_name[0:5] == "mpich"):
        return "mpich"
    elif (mpi_name[0:8] == "openmpi-"):
        return "openmpi"
    else:
        print("ERROR: Illegal MPI name: ", mpi_name)
        return None


def get_openmpi_version(mpi_name):
    if (mpi_name[0:8] == "openmpi-"):
        return mpi_name[8:]
    else:
        print("ERROR: This is not OpenMPI: ", mpi_name)
        return None


def main():
    import subprocess

    print("Making Dockerfiles for all targets ...")

    docker_targets = []

    header = ("# This file is automatically created by " + __file__ + "\n")

    for machine_target in machine_targets:
        if machine_target == "generic":
            common_top_part = (
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
                (mpi_type, mpi_ver) = get_mpi_type_and_version(mpi_target)

                if (mpi_type == "mpich"):
                    if (mpi_ver == ""):
                        # if MPICH version is not specified, get the precompiled generic version
                        mpi_part = "RUN apt-get install -y mpich\n"

                    else:
                        # Otherwise, download the source and build it           
                        mpich_dir = "http://www.mpich.org/static/downloads/" + mpi_ver
                        mpi_part = (
                        "RUN apt-get install -y wget\n"
                        "RUN apt-get install -y g++\n"
                        "RUN apt-get install -y gfortran\n"
                        "WORKDIR /home\n"
                        "RUN wget " + mpich_dir + "/" + mpi_target + ".tar.gz\n"
                        "RUN gunzip " + mpi_target + ".tar.gz\n"
                        "RUN tar -xf " + mpi_target + ".tar\n"
                        "WORKDIR /home/" + mpi_target + "\n"
                        "RUN ./configure --prefix=\"/home/$USER/mpich-install\n"
                        "RUN make\n"
                        "RUN make install\n"
                        "ENV PATH=$PATH:/home/$USER/mpich-install/bin\n"
                        "ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/$USER/mpich-install/lib/:/usr/local/lib\n")

                elif (mpi_type == "openmpi"):
                    # Note that OpenMPI is more complicated than MPICH, because:
                    # - There are multiple incompatible versions
                    # - Must be built from the source code
                    # - Must be downloaded from OpenMPI website first
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

                    # TODO: Check whether the version number is correct

                    # Directory name for OpenMPI download
                    openmpi_dir = "https://download.open-mpi.org/release/open-mpi/v" + openmpi_ver[0:3]

                    # TODO: Check whether this file exist

                    openmpi_version_part = (
                    "RUN wget " + openmpi_dir + "/" + mpi_target + ".tar.gz\n"
                    "RUN gunzip " + mpi_target + ".tar.gz\n"
                    "RUN tar -xf " + mpi_target + ".tar\n"
                    "WORKDIR /home/" + mpi_target + "\n")

                    mpi_part = openmpi_common_top_part + openmpi_version_part + openmpi_common_bottom_part

                else:
                    print("ERROR: unknown MPI target: ", mpi_target)
                    quit()

                docker_target = DockerClass()
                docker_target.set_file_name("Dockerfile-" + mpi_target)
                docker_target.set_content(header + common_top_part + mpi_part + common_bottom_part)
                docker_target.set_image(image_prepend + mpi_target + image_append)
                docker_targets.append(docker_target)
            # Next mpi target

        elif (machine_target == "galaxy"):
            # Galaxy (of Pawsey) has Docker image with its MPICH implementation already baked into 
            # an Ubuntu base.

            dockerfile_content = (
            "FROM pawsey/mpi-base:latest\n"
            "RUN apt-get update\n"
            "RUN apt-get upgrade -y\n"
            "RUN apt-get autoremove -y\n"
            "RUN apt-get install -y git\n"
            "RUN apt-get install -y make\n"
            "RUN apt-get install -y wget\n"
            "RUN apt-get install -y g++\n"
            "RUN apt-get install -y gfortran\n"
            "WORKDIR /home\n"
            "RUN git clone https://github.com/prlahur/testmpi.git\n"
            "WORKDIR /home/testmpi\n"
            "RUN make\n")

            docker_target = DockerClass()
            docker_target.set_file_name("Dockerfile-" + machine_target)
            docker_target.set_content(header + dockerfile_content)
            docker_target.set_image(image_prepend + machine_target + image_append)
            docker_targets.append(docker_target)

        else:
            print("ERROR: unknown machine target: ", machine_target)
            quit()

    print("Docker target count:", len(docker_targets))

    if dry_run:
        print("This is a dry run. No Docker image will be created")
    else:
        print("Making Docker images for all targets ...")

    for docker_target in docker_targets:
        docker_target.write()
        docker_command = ("docker build -t " + docker_target.image + " -f " + docker_target.file_name + " .")
        if dry_run:
            subprocess.run("echo " + docker_command, shell=True)
        else:
            subprocess.run(docker_command, shell=True)

    # Consider: Add automatic upload to DockerHub? This requires Docker login.

    if (sample_batch != ""):
        print()
        print("Making sample batch files ...")

        for mpi_target in mpi_targets:
            batch_common_part = (
            "#!/bin/bash -l\n"
            "## This file is automatically created by " + __file__ + "\n"
            "#SBATCH --ntasks=20\n"
            "#SBATCH --time=00:10:00\n\n"
            "module load singularity/3.5.0\n")

            mpi_type, mpi_ver = get_mpi_type_and_version(mpi_target)
            if (mpi_type == "mpich"):
                module = "mpich/3.3.0"
                image = "testmpich_latest.sif"
                batch_mpi_part = (
                "module load " + module + "\n\n"
                "mpirun -n 20 singularity exec " + image + " /home/testmpi/mpi_check\n")
            elif (mpi_type == "openmpi"):
                openmpi_ver = get_openmpi_version(mpi_target)
                if (openmpi_ver != None):
                    module = "openmpi/" + openmpi_ver + "-ofed45-gcc"
                    image = "testopenmpi-" + openmpi_ver + "_latest.sif"
                    batch_mpi_part = (
                    "module load " + module + "\n\n"
                    "mpirun -n 20 -oversubscribe singularity exec " + image + " /home/testmpi/mpi_check\n")
                else:
                    break
            else:
                break

            batch_file = sample_batch + "-" + mpi_target + ".sbatch"
            print("Making batch file:", batch_file)
            f = open(batch_file, "w")
            f.write(batch_common_part + batch_mpi_part)
            f.close()


if (__name__ == "__main__"):
    main()