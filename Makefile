# The MPI compiler to use. This is a generic name that links to actual compiler.
MPICC = mpicc

# Header files for OpenMPI and MPICH. Add more if necessary.
INCLUDES = -I/usr/include/openmpi -I/usr/include/mpich

TARGET = mpi_check

.PHONY: clean

%.o: %.c
	${MPICC} -c -o $@ $< ${INCLUDES}

${TARGET}: ${TARGET}.o 
	${MPICC} -o $@ $^ ${INCLUDES}

clean:
	rm -f ${TARGET} *.o core
