EXE=mpi_hello_world
MPICC=mpicc

all: ${EXE}

mpi_hello_world: mpi_hello_world.c
	${MPICC} -o mpi_hello_world mpi_hello_world.c

clean:
	rm ${EXE}
