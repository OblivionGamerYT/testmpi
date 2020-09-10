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
machine_targets = ["generic"]

# Set MPI implementations for "generic" machine in the list below.
# Note that a specific machine already has its MPI specified.
# A valid mpi target is either "mpich" or "openmpi-X.Y.Z", 
# where X, Y and Z are version numbers (major, minor and revision).
# Possible MPI targets:
# mpi_targets = ["mpich", "mpich-3.3.2", "openmpi", "openmpi-4.0.3", "openmpi-3.1.4", "openmpi-2.1.6", "openmpi-1.10.7"]
mpi_targets = ["mpich"]

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

# The number of processors to use for the build
nproc = 1

#------------------------------------------------------------------------------
# CODE

import sys
import argparse
import subprocess
import re
from pathlib import Path

user = "user"
group = "group"
home_dir = "/home/user"

# Header for all automatically generated Dockerfiles
header = ("# This file is automatically created by " + __file__ + "\n")

mpi_dir = "/usr/local"
MPI_COMPILE_FLAGS = "-I/usr/local/include -pthread"

forbidden_chars_string = "?!@#$%^&* ;<>?|\"\a\b\f\n\r\t\v"
forbidden_chars = list(forbidden_chars_string)

# Sanitizing parameters
machine_targets = list(map(str.lower, machine_targets))
mpi_targets = list(map(str.lower, mpi_targets))


def is_proper_name(name):
    '''
    Return true if the name is non-empty and does not contain certain characters. 
    False otherwise.
    '''
    if type(name) != str:
        raise TypeError("Name is not string")
    if name == "":
        return False
    for c in forbidden_chars:
        if name.find(c) >= 0:
            return False
    return True


class DockerClass:
    recipe_name = ""
    image_name = ""
    recipe = ""

    def set_recipe_name(self, recipe_name):
        '''Set Dockerfile name'''
        if is_proper_name(recipe_name):
            self.recipe_name = recipe_name
        else:
            raise ValueError("Illegal recipe_name:", recipe_name)

    def set_recipe(self, recipe):
        '''Set the content of Dockerfile'''
        if type(recipe) == str:
            if recipe != "":
                self.recipe = recipe
            else:
                raise ValueError("Recipe is empty string")
        else:
            raise TypeError("Recipe is not string")

    def set_image_name(self, image_name):
        '''Set Docker image name'''
        if is_proper_name(image_name):
            self.image_name = image_name
        else:
            raise ValueError("Illegal image_name:", image_name)

    def write_recipe(self):
        '''Write recipe into Dockerfile'''
        if self.recipe_name == "":
            raise ValueError("Docker recipe file name has not been set")
        elif self.recipe == "":
            raise ValueError("Docker recipe content has not been set")
        else:
            with open(self.recipe_name, "w") as file:
                file.write(self.recipe)

    def get_build_command(self):
        '''Return build command'''
        if (self.recipe_name == ""):
            raise ValueError("Docker recipe file name has not been set")
        elif (self.image_name == ""):
            raise ValueError("Docker image file name has not been set")
        else:
            return ("docker build -t " + self.image_name + " -f " + self.recipe_name + " .")
         
    def build_image(self):
        '''Build the Docker image'''
        build_command = self.get_build_command()
        if (self.recipe_name == ""):
            raise ValueError("Docker recipe file name has not been set")
        else:
            file = Path(self.recipe_name)
            if file.is_file():
                # TODO: store log file, handle error
                subprocess.run(build_command, shell=True)
            else:
                raise FileExistsError("Docker recipe file does not exist:", self.recipe_name)


def split_version_number(input_ver):
    '''
    Split a given version number in string into 3 integers.
    '''
    string_list = re.findall(r'\d+', input_ver)
    if (len(string_list) == 3):
        int_list = [int(x) for x in string_list]
        return int_list
    else:
        return []


def compose_version_number(int_list):
    '''
    Given a list of 3 integers, compose version number.
    '''
    if (len(int_list) == 3):
        return (str(int_list[0]) + '.' + str(int_list[1]) + '.' + str(int_list[2]))
    else:
        return ""


def get_mpi_type_and_version(mpi_name):
    '''
    Given the full name of MPI, return MPI type (mpich / openmpi)
    as well as version.
    When the version is not specified, the simplest version to install 
    is chosen (ie. using "apt-get install").
    Input should be in one of these formats:
    - mpich
    - openmpi
    - mpich-X.Y.Z
    - openmpi-X.Y.Z
    Where "X.Y.Z" is version number.
    '''
    length = len(mpi_name)
    if (type(mpi_name) == str):
        if (length < 5):
            raise ValueError("MPI name is too short:", mpi_name)

        elif (length == 5):
            # Unspecified MPICH
            if (mpi_name == "mpich"):
                return("mpich", "")
            else:
                raise ValueError("Expecting mpich:", mpi_name)

        elif (length == 6):
            raise ValueError("Illegal MPI name:", mpi_name)

        elif (length == 7):
            # Unspecified OpenMPI
            if (mpi_name == "openmpi"):
                return("openmpi", "")
            else:
                raise ValueError("Expecting openmpi:", mpi_name)

        else:
            if (mpi_name[0:5] == "mpich"):
                # MPICH with specified version number
                int_ver = split_version_number(mpi_name[6:])
                if (len(int_ver) == 3):
                    return ("mpich", compose_version_number(int_ver))
                else:
                    raise ValueError("Illegal mpich version:", mpi_name[6:])

            elif (mpi_name[0:7] == "openmpi"):
                # OpenMPI with specified version number
                int_ver = split_version_number(mpi_name[8:])
                if (len(int_ver) == 3):
                    return ("openmpi", compose_version_number(int_ver))
                else:
                    raise ValueError("Illegal openmpi version:", mpi_name[8:])
            else:
                raise ValueError("Illegal MPI name:", mpi_name)
    else:
        raise TypeError("MPI name is not a string:", mpi_name)



def make_image(machine_target, mpi_target, actual):
    '''
    Make Docker image for a given machine and MPI target.
    '''
    apt_install_part = (
    "RUN apt-get update \\\n"
    "    && apt-get upgrade -y \\\n"
    "    && apt-get autoremove -y \\\n"
    "    && apt-get install -y")

    # Put apps to install from Ubuntu here
    apt_install_items = [
    "g++",
    "gfortran",
    "git",
    "wget",
    "make"]

    for apt_install_item in apt_install_items:
        apt_install_part += " \\\n" + "        " + apt_install_item
    apt_install_part += "\n"

    cmake_ver = "3.18.2"
    cmake_source = "cmake-" + cmake_ver + ".tar.gz"

    common_top_part = (
    apt_install_part +
    "# Common top part\n"
    "# Build the latest cmake\n"
    "RUN mkdir /usr/local/share/cmake\n"
    "WORKDIR /usr/local/share/cmake\n"
    "RUN wget https://github.com/Kitware/CMake/releases/download/v" + cmake_ver + "/" + cmake_source + " \\\n"
    "    && tar -zxf " + cmake_source + " \\\n"
    "    && rm " + cmake_source + "\n"
    "WORKDIR /usr/local/share/cmake/cmake-" + cmake_ver + "\n"
    "RUN ./bootstrap --system-curl \\\n"
    "    && make \\\n"
    "    && make install\n"
    )

    common_bottom_part = (
    "# Common bottom part\n"
    "WORKDIR " + home_dir + "\n"
    "RUN git clone https://github.com/prlahur/testmpi.git\n"
    "WORKDIR " + home_dir + "/testmpi\n"
    "WORKDIR " + home_dir + "/testmpi/build\n"
    "RUN cmake ..\n"
    "# Set environment variables\n"
    "ENV PATH=" + home_dir + "/testmpi/bin:$PATH \n"
    "# Switch into user and group ID on the host side\n"
    "ARG USER_ID\n"
    "ARG GROUP_ID\n"
    "RUN if [ ${USER_ID:-0} -ne 0 ] && [ ${GROUP_ID:-0} -ne 0 ] ; then \\\n"
    "    if id " + user + " ; then userdel -f " + user + " ; fi &&\\\n"
    "    if getent group " + group + " ; then groupdel " + group + " ; fi &&\\\n"
    "    groupadd --gid ${GROUP_ID} " + group + " &&\\\n"
    "    useradd --no-log-init --uid ${USER_ID} --gid " + group + " " + user + " \\\n"
    ";fi\n"
    "WORKDIR " + home_dir + "\n"
    "RUN chown --changes --silent --no-dereference --recursive ${USER_ID}:${GROUP_ID} " + home_dir + "\n"
    "USER " + user + "\n"
    "# Set up aliases in .bashrc\n"
    "RUN echo \"alias rm=\'rm -i\'\" >> ~/.bashrc &&\\\n"                                                          
    "    echo \"alias cp=\'cp -i\'\" >> ~/.bashrc &&\\\n"
    "    echo \"alias mv=\'mv -i\'\" >> ~/.bashrc \n"
    "# Put start-up message in .bashrc\n"
    "RUN echo \"echo \" >> ~/.bashrc &&\\\n"
    "    echo \"echo ================================================================================\" >> ~/.bashrc &&\\\n"
    "    echo \"echo Welcome to testmpi container! \" >> ~/.bashrc &&\\\n"
    "    echo \"echo ================================================================================\" >> ~/.bashrc \n"
    "WORKDIR " + home_dir + "/testmpi \n"
    )

    if machine_target == "generic":
        base_system_part = ("FROM ubuntu:bionic as buildenv\n")

        (mpi_type, mpi_ver) = get_mpi_type_and_version(mpi_target)

        if (mpi_type == "mpich"):
            if (mpi_ver == ""):
                # if MPICH version is not specified, get the precompiled version
                mpi_part = "RUN apt-get install -y libmpich-dev\n"

            else:
                # else (if version is specified), download the source from website and build           
                web_dir = "https://www.mpich.org/static/downloads/" + mpi_ver

                mpi_part = (
                "# Build MPICH\n"
                "WORKDIR /home\n"
                "RUN wget " + web_dir + "/" + mpi_target + ".tar.gz \\\n"
                "    && tar -zxf " + mpi_target + ".tar.gz\n"
                "    && rm " + mpi_target + ".tar.gz \n"
                "WORKDIR /home/" + mpi_target + "\n"
                "RUN ./configure --prefix=" + mpi_dir + " \\\n"
                "    && make -j" + str(nproc) + " \\\n"
                "    && make install \n"
                "ENV PATH=$PATH:" + mpi_dir + "/bin\n"
                "ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:" + mpi_dir + "/lib\n"
                )

        elif (mpi_type == "openmpi"):
            if (mpi_ver == ""):
                # if OpenMPI version is not specified, get the precompiled version
                mpi_part = "RUN apt-get install -y libopenmpi-dev\n"

            else:
                # Download the source from OpenMPI website and build
                int_ver = split_version_number(mpi_ver)
                ver_dir = "v" + str(int_ver[0]) + "." + str(int_ver[1])
                web_dir = "https://download.open-mpi.org/release/open-mpi/" + ver_dir

                # Note: Enable C++ binding when configuring, because some programs use it.
                # ./configure --enable-mpi-cxx

                mpi_part = (
                "# Build OpenMPI\n"
                "WORKDIR /home\n"
                "RUN wget " + web_dir + "/" + mpi_target + ".tar.gz \\\n"
                "    && tar -zxf " + mpi_target + ".tar.gz \\\n"
                "    && rm " + mpi_target + ".tar.gz \n"
                "WORKDIR /home/" + mpi_target + "\n"
                "RUN ./configure --enable-mpi-cxx \\\n"
                "    && make all -j" + str(nproc) + " \\\n"
                "    && make install\n"
                "ENV PATH=/usr/local/bin:$PATH\n"
                "ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH\n"
                )

        else:
            raise ValueError("Unknown MPI target:", mpi_target)

        docker_target = DockerClass()
        docker_target.set_recipe_name("Dockerfile-" + mpi_target)
        docker_target.set_recipe(header + base_system_part + common_top_part + mpi_part + common_bottom_part)
        docker_target.set_image_name(image_prepend + mpi_target + image_append)

    elif (machine_target == "galaxy"):
        # Galaxy (of Pawsey) has Docker image with its MPICH implementation already baked into 
        # an Ubuntu base.
        base_system_part = ("FROM pawsey/mpi-base:latest as buildenv\n")

        docker_target = DockerClass()
        docker_target.set_recipe_name("Dockerfile-" + machine_target)
        docker_target.set_recipe(header + base_system_part + common_top_part + common_bottom_part)
        docker_target.set_image_name(image_prepend + machine_target + image_append)

    else:
        raise ValueError("Unknown machine target:", machine_target)

    docker_target.write_recipe()
    if actual:
        docker_target.build_image()
    else:
        print(docker_target.get_build_command())

    return docker_target



def make_batch_file(machine, mpi):
    '''
    Make sample batch files for SLURN
    '''

    batch_common_part = (
    "#!/bin/bash -l\n"
    "## This file is automatically created by " + __file__ + "\n"
    "#SBATCH --ntasks=5\n"
    "##SBATCH --ntasks=305\n"
    "#SBATCH --time=02:00:00\n"
    "#SBATCH --job-name=cimager\n"
    "#SBATCH --export=NONE\n\n"
    "module load singularity/3.5.0\n")

    (mpi_type, mpi_ver) = get_mpi_type_and_version(mpi)
    if (mpi_type == "mpich"):
        module = "mpich/3.3.0"
        image = "yandasoft-mpich_latest.sif"
        batch_mpi_part = (
        "module load " + module + "\n\n"
        "mpirun -n 5 singularity exec " + image +
        " cimager -c dirty.in > dirty_${SLURM_JOB_ID}.log\n")

    elif (mpi_type == "openmpi"):
        if (mpi_ver != None):
            module = "openmpi/" + mpi_ver + "-ofed45-gcc"
            image = "yandasoft-" + mpi_ver + "_latest.sif"
            batch_mpi_part = (
            "module load " + module + "\n\n"
            "mpirun -n 5 -oversubscribe singularity exec " + image +
            " cimager -c dirty.in > dirty_${SLURM_JOB_ID}.log\n")

    else:
        raise ValueError("Unknown MPI target:", mpi)

    batch_file = "sample-" + machine + "-" + mpi + ".sbatch"
    print("Making batch file:", batch_file)
    with open(batch_file, "w") as file:
        file.write(batch_common_part + batch_mpi_part)



def show_targets():
    print("The list of Docker targets: ")
    for machine in machine_targets:
        print("- Machine:", machine)
        if machine == "generic":
            for mpi in mpi_targets:
                print("  - MPI:", mpi)
    print("Note that specific machine has a preset MPI target")



def main():
    parser = argparse.ArgumentParser(
        description="Make Docker images for various MPI implementations",
        epilog="The targets can be changed from inside the script (the SETTINGS section)")
    parser.add_argument('-i', '--image', help='Create image', action='store_true')
    parser.add_argument('-s', '--show_targets_only', help='Show targets only', action='store_true')
    #parser.add_argument('-s', '--slurm', help='Create sample batch files for SLURM', action='store_true')
    args = parser.parse_args()

    if args.show_targets_only:
        show_targets()
        sys.exit(0)

    if args.image:
        print("Making Docker images ...")
    else:
        print("Docker image will not be made")

    for machine_target in machine_targets:
        if machine_target == "generic":
            for mpi_target in mpi_targets:
                docker = make_image(machine_target, mpi_target, args.image)
                if docker == None:
                    raise ValueError("Failed to make base image:", machine_target, mpi_target)
        else:
            # Specific machine
            docker = make_image(machine_target, None, args.image)
            if docker == None:
                raise ValueError("Failed to make base image:", machine_target)



if (__name__ == "__main__"):
    if sys.version_info[0] == 3:
        main()
    else:
        raise ValueError("Must use Python 3")
