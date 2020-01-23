#include <stdio.h>
#include "omp.h"
#include <time.h>
#include <stdlib.h>

#define SIZE 1000000000
//10000 1000000 10000000 100000000
#define NUMTHREADS 8

int main(){
	unsigned long long int *data,*data_1,*partial_sum;
	data = (unsigned long long int *)malloc(SIZE*sizeof(unsigned long long int));
    data_1 = (unsigned long long int *)malloc(SIZE*sizeof(unsigned long long int));
	const int nthreads = NUMTHREADS;
	//initialize data array
	for(unsigned long long int i=0; i<SIZE; i++){
		data[i] = i+1;
        data_1[i] = i+1;
	}
    partial_sum =  (unsigned long long int *)malloc((nthreads+1)*sizeof(unsigned long long int));
	for(int i=0;i<nthreads+1;i++){
        partial_sum[i]=0;
    }
    double time_spent = 0.0;
	double begin = omp_get_wtime();
	
	#pragma omp parallel num_threads(NUMTHREADS)
    {
        const int tid = omp_get_thread_num();
        unsigned long long int  sum = 0;
        #pragma omp for schedule(static)
        for (unsigned long long int i=0; i<SIZE; i++) {
            sum += data[i];
            data[i] = sum;
        }
        partial_sum[tid+1] = sum;
        #pragma omp barrier
        unsigned long long int offset = 0;
        for(int i=0; i<(tid+1); i++) {
            offset += partial_sum[i];
        }
        #pragma omp for schedule(static)
        for (unsigned long long int i=0; i<SIZE; i++) {
            data[i] += offset;
        }
    }
    double end = omp_get_wtime();
	time_spent = (double)(end - begin);

    double start1 = omp_get_wtime();
    //serial part
    for(unsigned long long int i=1; i<SIZE; i++){
        data_1[i] = data_1[i] + data_1[i-1];
    }
    double end1 = omp_get_wtime();
    double time2 = (double)(end1 - start1);
	printf("%f %f\n", time_spent, time2);
    //printf("%llu %llu\n",data[SIZE-1], data_1[SIZE-1] );
	//free memory	
	free(data);free(partial_sum);free(data_1);
	

	return 0;
}