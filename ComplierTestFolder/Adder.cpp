#include <iostream>
#include <cuda_runtime.h>

__global__ void sumKernel(int *num)
{
    int idx = threadIdx.x; // 获取线程索引
    if (idx < 10)
    {
        atomicAdd(num, idx); // 使用原子操作将每个线程的计算结果累加到num
    }
}

int main()
{
    int num = 0;         // 主机上的变量
    int *d_num;          // 设备上的变量

    // 在设备上分配内存
    cudaMalloc(&d_num, sizeof(int));
    cudaMemcpy(d_num, &num, sizeof(int), cudaMemcpyHostToDevice);

    // 启动CUDA内核
    sumKernel<<<1, 10>>>(d_num);

    // 将结果从设备拷贝回主机
    cudaMemcpy(&num, d_num, sizeof(int), cudaMemcpyDeviceToHost);

    std::cout << "The sum is: " << num << std::endl;

    // 释放设备内存
    cudaFree(d_num);

    return 0;
}
