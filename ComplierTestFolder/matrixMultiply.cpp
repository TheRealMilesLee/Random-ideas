#include <iostream>
using namespace std;
void multiplyIK(double A[3][3], double B[3][3], double C[3][3], int matrix_size, int block_size);
void multiplyIJ(double A[3][3], double B[3][3], double C[3][3], int matrix_size, int block_size);
void multiplyKJ(double A[3][3], double B[3][3], double C[3][3], int matrix_size, int block_size);
int main(int argc, char **argv)
{
  double A[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
  double B[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
  double C[3][3] = {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}};
  if (argv[1] == "IK")
  {
    multiplyIK(A, B, C, 3, 2);
  }
  else if (argv[1] == "IJ")
  {
    multiplyIJ(A, B, C, 3, 2);
  }
  else if (argv[1] == "KJ")
  {
    multiplyKJ(A, B, C, 3, 2);
  }

  cout << "---------------------------------------------------" << endl;
  for (size_t row = 0; row < 3; row++)
  {
    for (size_t column = 0; column < 3; column++)
    {
      cout << C[row][column] << " | ";
    }
    cout << endl;
    cout << "---------------------" << endl;
  }
  return 0;
}

void multiplyIK(double A[3][3], double B[3][3], double C[3][3], int matrix_size, int block_size)
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

void multiplyIJ(double A[3][3], double B[3][3], double C[3][3], int matrix_size, int block_size)
{
  for (int ii = 0; ii < matrix_size; ii += block_size)
  {
    for (int jj = 0; jj < matrix_size; jj += block_size)
    {
      for (int k = 0; k < matrix_size; k++)
      {
        for (int i = ii; i < ii + block_size; i++)
        {
          for (int j = jj; j < jj + block_size; j++)
          {
            C[i][j] += A[i][k] * B[k][j];
          }
        }
      }
    }
  }
}

void multiplyKJ(double A[3][3], double B[3][3], double C[3][3], int matrix_size, int block_size)
{
  for (int kk = 0; kk < matrix_size; kk += block_size)
  {
    for (int jj = 0; jj < matrix_size; jj += block_size)
    {
      for (int i = 0; i < matrix_size; i++)
      {
        for (int k = kk; k < kk + block_size; k++)
        {
          for (int j = jj; j < jj + block_size; j++)
          {
            C[i][j] += A[i][k] * B[k][j];
          }
        }
      }
    }
  }
}
