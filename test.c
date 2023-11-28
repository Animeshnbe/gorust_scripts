#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

float train[][2] = {
    {0.0, 0.0},
    {1.0, 2.0},
    {2.0, 4.0},
    {3.0, 6.0},
    {4.0, 8.0},
    {5.0, 10.0}
};
size_t t_count=sizeof(train) / sizeof(train[0]);

float rand_float(void){
    return (float)rand() / (float)(RAND_MAX);
}

float sigmoidf(float x){
    return 1.f/(1.f+expf(-x));
}

float cost(float w, float b){
    float res = 0.0f;
    for (int i=0; i<t_count; i++){
        float d = (train[i][0]*w + b) - train[i][1];
        res += d * d;
    }
    res /= t_count;
    return res;
}

int main(){
    srand(69);

    // init
    float w = rand_float(), b = rand_float()*0.02f;

    // train
    float eps = 1e-3;
    float lr = 1e-3;
    for (int i=0; i<1000; i++) {
        float c = cost(w, b);
        float dw = (cost(w+eps, b)-c)/eps;
        float db = (cost(w, b+eps)-c)/eps;
        w -= (lr*dw);
        b -= (lr*db);
        if (i%100 == 0)
            printf("cost = %f, w = %f, b = %f\n",cost(w, b),w,b);
    }
    printf("Final params: w = %f, b = %f",w,b);
}