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
    // #ifdef _OPENMP
    // printf("OpenMP is defined \n");
    // #endif

    int maxThreads;

    #pragma omp parallel
    {
        maxThreads = omp_get_num_threads();
        printf("maxThreads: %d \n", maxThreads);
    }
    // printf("maxThreads: %d \n", maxThreads);

    // Get the number of threads from input
    int nThreads = maxThreads;  // Default
    if (argc == 2)
    {
        if (argv[1][0] == '-')
        {
            printf("Usage: openmp_check [nThread|option] \n");
            printf("  nThread     Number of threads (positive integer).\n");
            printf("              Default: max number of threads.\n");
            printf("Options: \n");
            printf("  -h          This help.\n");

            return 0;
        }
        else
        {
            int n = atoi(argv[1]);
            // printf("n: %d \n", n);
            if ((n >= 1) && (n <= maxThreads))
            {
                nThreads = n;
            }
            else
            {
                printf("Illegal number of threads. Default is used instead.\n");
            }
        }
    }
    printf("nThreads: %d \n", nThreads);

    int nElements = 1000000 * maxThreads;
    double x[nElements];
    double y[nElements];

    for (int i = 0; i < nElements; ++i)
    {
        x[i] = (double)(i);
        y[i] = (double)(i);
    }

    // int NTHREADS = 1;
    omp_set_num_threads(nThreads);

    clock_t clockStart = clock();
    time_t timeStart = time(NULL);

    #pragma omp parallel
    {
        int tid = omp_get_thread_num();
        printf("Thread %d of %d starts \n", tid, nThreads);

        int nElementsPerThread = nElements / nThreads;
        int lowerBound = tid * nElementsPerThread;
        int upperBound = lowerBound + nElementsPerThread;
        double t;
        printf("Thread %d is working for elements: %d - %d ... \n", tid, lowerBound, upperBound);
        for (int i = lowerBound; i < upperBound; ++i)
        {
            // Some expensive process here
            for (int j = 0; j < 20000; ++j)
            {
                // This computation is completely within the thread
                //x[i] = x[i] + 1.0;
                t = x[i];
                x[i] = y[i];
                y[i] = t;
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
