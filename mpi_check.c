/*
Check whether a master can broadcast data to multiple workers.
If there is only one process, then the master has no worker.
*/
#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

enum data {DATA_NONE=0, DATA_MASTER=1, DATA_WORKER=-1};

int main(int argc, char** argv) {
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

    // Set up the data to be broadcast later.
    int data = DATA_NONE;
    if (world_rank == 0) { // master
        data = DATA_MASTER; // value to be broadcast
    } else { // worker
        data = DATA_WORKER;  // value to be overwritten
    }

    // Broadcast the value (from master to workers)
    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Bcast(&data, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Barrier(MPI_COMM_WORLD);

    // Print out
    if (world_size > 1) {
        if (world_rank == 0) { // master
            printf("Processor %s, rank %d of %d (MASTER): %d \n",
                processor_name, world_rank, world_size, data);
        } else { // worker
            if (data == DATA_MASTER) {
                printf("Processor %s, rank %d of %d (worker): %d SUCCESS\n",
                    processor_name, world_rank, world_size, data);
            } else { // data is not master data
                printf("Processor %s, rank %d of %d (worker): %d FAIL\n",
                    processor_name, world_rank, world_size, data);
            }
        }
    } else {
        printf("Processor %s, rank %d of %d (MASTER without worker): %d \n",
            processor_name, world_rank, world_size, data);
    }

    MPI_Finalize();
}
