/*
Check OpenMP
*/
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <omp.h>

int main(int argc, char** argv) 
{
    #ifdef _OPENMP
    printf("OpenMP is defined \n");
    // int nThreads;
    #endif

    // nThreads = omp_get_num_threads();
    // printf("Number of threads in serial mode: %d\n", nThreads);
    #pragma omp parallel
    {
        // int nThreads = omp_get_num_threads();
        if (omp_get_thread_num() == 0) 
        {
            // printf("Number of threads in parallel mode: %d\n", nThreads);
            printf("omp_get_max_threads: %d\n", omp_get_max_threads());
            printf("omp_get_num_threads: %d\n", omp_get_num_threads());
            printf("omp_get_num_procs: %d\n", omp_get_num_procs());
        }
    }

    int nElements = 8000;
    double x[nElements];

    clock_t clockStart = clock();
    time_t timeStart = time(NULL);

    int NTHREADS = 1;
    omp_set_num_threads(NTHREADS);


    #pragma omp parallel
    {
        int tid = omp_get_thread_num();
        int nThreads = omp_get_num_threads();
        printf("Thread %d of %d starts \n", tid, nThreads);

        int nElementsPerThread = nElements / nThreads;
        int lowerBound = tid * nElementsPerThread;
        int upperBound = lowerBound + nElementsPerThread;
        printf("Thread %d is working for elements: %d - %d ... \n", tid, lowerBound, upperBound);
        for (int i = lowerBound; i < upperBound; ++i)
        {
            // Some expensive process here
            for (int j = 0; j < 2000000; ++j)
            {
                // This computation is completely within the thread
                x[i] = x[i] + 1.0;
            }
        }
        printf("Thread %d of %d ends \n", tid, nThreads);
    }

    clock_t clockEnd = clock();
    time_t timeEnd = time(NULL);

    double clockElapsed = ((double)clockEnd - (double)clockStart) / CLOCKS_PER_SEC;
    printf("CPU time elapsed: %f seconds \n", clockElapsed);
    printf("Wall time elapsed: %f seconds \n", difftime(timeEnd, timeStart));

    return 0;
}