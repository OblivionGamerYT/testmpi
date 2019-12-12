# Switch between OpenMPI and MPICH
IDIR=/usr/include/openmpi
#IDIR=/usr/include/mpich

MPICC=mpicc
TARGET=mpi_check

%.o: %.c
	${MPICC} -c -o $@ $< -I${IDIR}

${TARGET}: ${TARGET}.o 
	${MPICC} -o $@ $^ -I${IDIR}

clean:
	rm -f mpi_check *.o core
