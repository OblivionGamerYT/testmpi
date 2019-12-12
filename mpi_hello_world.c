/*
A very simple MPI program.
*/
#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

int main(int argc, char** argv) {
    // Initialize the MPI environment
    MPI_Init(NULL, NULL);

    // Get the number of processes
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    // Get the rank of the process
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    // Get the name of the processor
    char processor_name[MPI_MAX_PROCESSOR_NAME];
    int name_len;
    MPI_Get_processor_name(processor_name, &name_len);

    // Set up an integer to be broadcast later.
    // Note the different value for master and workers.
    int uniform_int = 0;
    if (world_rank == 0) { // if master
        uniform_int = 45; // TODO: change this to random value
    } else { // if worker
        uniform_int = -3;
    }

    // Broadcast the value (from master to workers)
    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Bcast(&uniform_int, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Barrier(MPI_COMM_WORLD);

    // Print out
    // If the data transfer work
    printf("Processor %s, rank %d out of %d, uniform int %d \n",
           processor_name, world_rank, world_size, uniform_int);

    // Finalize the MPI environment.
    MPI_Finalize();
}
