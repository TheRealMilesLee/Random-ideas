#include <iostream>
using namespace std;
void multiply(int A[3][3], int B[3][3], int C[3][3], int matrix_size, int block_size);
int main()
{
  int A[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
  int B[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
  int C[3][3] = {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}};
  multiply(A, B, C, 3, 2);
  return 0;
}

void multiply(int A[3][3], int B[3][3], int C[3][3], int matrix_size, int block_size)
{
  for (int ii = 0; ii < matrix_size; ii += block_size)
  {
    for (int kk = 0; kk < matrix_size; kk += block_size)
    {
      for (int j = 0; j < matrix_size; j++)
      {
        for (int i = ii; i < ii + block_size; i++)
        {
          for (int k = kk; k < kk + block_size; k++)
          {
            cout << "C[" << i << "][" << j << "] += A[" << i << "][" << k << "]*B[" << k << "][" << j << "]" << endl;
            C[i][j] += A[i][k] * B[k][j];
          }
        }
      }
    }
  }
}
