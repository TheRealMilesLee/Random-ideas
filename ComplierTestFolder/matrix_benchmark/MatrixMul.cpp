#include <iostream>
#include <vector>
#include <thread>
#include <algorithm>

using namespace std;

void matrix_mul(vector<vector<int>> &src1,
                vector<vector<int>> &src2,
                vector<vector<int>> &dst,
                size_t blockSize,
                size_t start,
                size_t end);

void parallel_computing_simple_multithread(
    std::vector<std::vector<int>> &matrix1,
    std::vector<std::vector<int>> &matrix2,
    std::vector<std::vector<int>> &result,
    size_t block_size);
int main()
{
  // Default values
  size_t matrix_size = 4096;
  size_t block_size = 128;

  // Initialize matrices
  vector<vector<int>> src1(matrix_size, vector<int>(matrix_size));
  vector<vector<int>> src2(matrix_size, vector<int>(matrix_size));
  vector<vector<int>> dst(matrix_size, vector<int>(matrix_size, 0));

  for (size_t row = 0; row < matrix_size; row++)
  {
    for (size_t col = 0; col < matrix_size; col++)
    {
      src1[row][col] = static_cast<int>(row) + static_cast<int>(col);
      src2[row][col] = static_cast<int>(row) + static_cast<int>(col);
    }
  }

  auto start_time = std::chrono::high_resolution_clock::now();
  matrix_mul(src1, src2, dst, block_size, 0, src1.size());
  auto end_time = std::chrono::high_resolution_clock::now();
  auto duration = std::chrono::duration_cast<std::chrono::microseconds>(
      end_time - start_time);

  double seconds = static_cast<double>(duration.count()) / 1000000.0;

  cout << "Matrix multiplication time with single thread: " << seconds
       << " seconds or " << duration.count() % 1000000 << " microseconds"
       << endl;

  auto start_time_para = std::chrono::high_resolution_clock::now();
  parallel_computing_simple_multithread(src1, src2, dst, block_size);
  auto end_time_para = std::chrono::high_resolution_clock::now();
  auto duration_para = std::chrono::duration_cast<std::chrono::microseconds>(
      end_time_para - start_time_para);

  double seconds_para =
      static_cast<double>(duration_para.count()) / 1000000.0;

  cout << "Matrix multiplication time with multi thread: " << seconds_para
       << " seconds or " << duration_para.count() % 1000000 << " microseconds"
       << endl;
  return 0;
}

void matrix_mul(vector<vector<int>> &src1,
                vector<vector<int>> &src2,
                vector<vector<int>> &dst,
                size_t blockSize,
                size_t start,
                size_t end)
{
  // Perform matrix multiplication for the given block range using block ik
  // method
  for (size_t iblock = start; iblock < end; iblock += blockSize)
  {
    for (size_t kblock = 0; kblock < src2.size(); kblock += blockSize)
    {
      for (size_t jblock = 0; jblock < dst.size(); jblock += blockSize)
      {
        for (size_t i = iblock; i < min(iblock + blockSize, src1.size()); i++)
        {
          for (size_t k = kblock; k < min(kblock + blockSize, src2.size());
               k++)
          {
            for (size_t j = jblock; j < min(jblock + blockSize, dst.size());
                 j++)
            {
              dst[i][j] += src1[i][k] * src2[k][j];
            }
          }
        }
      }
    }
  }
}

void parallel_computing_simple_multithread(
    std::vector<std::vector<int>> &matrix1,
    std::vector<std::vector<int>> &matrix2,
    std::vector<std::vector<int>> &result,
    size_t block_size)
{
  std::vector<std::thread> threads;

  for (size_t i = 0; i < matrix1.size(); i += block_size)
  {
    threads.push_back(std::thread(
        [&matrix1, &matrix2, &result, block_size, i]()
        {
          size_t end = std::min(i + block_size, matrix1.size());
          matrix_mul(matrix1, matrix2, result, block_size, i, end);
        }));
  }

  for (auto &t : threads)
  {
    t.join();
  }

  threads.clear();
}
