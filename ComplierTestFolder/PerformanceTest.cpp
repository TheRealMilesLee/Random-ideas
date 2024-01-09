#include <iostream>
#include <mutex>
#include <random>
#include <thread>
#include <vector>

const int size = 4096;
const int numThreads = std::thread::hardware_concurrency(); // Get number of hardware threads

std::mutex mtx; // Mutex for synchronization

void matrixMultiply(const std::vector<std::vector<int>>& m1, const std::vector<std::vector<int>>& m2,
                    std::vector<std::vector<int>>& result, int startRow, int endRow)
{
  for (int i = startRow; i < endRow; ++i)
  {
    for (int j = 0; j < size; ++j)
    {
      for (int k = 0; k < size; ++k)
      {
        result[i][j] += m1[i][k] * m2[k][j];
      }
    }
  }
}

int main()
{
  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_int_distribution<int> dis(1, 4096); // Adjust range as needed

  std::vector<std::vector<int>> myVector1(size, std::vector<int>(size));
  std::vector<std::vector<int>> myVector2(size, std::vector<int>(size));
  std::vector<std::vector<int>> myVector3(size, std::vector<int>(size));

  for (int i = 0; i < size; ++i)
  {
    for (int j = 0; j < size; ++j)
    {
      myVector1[i][j] = dis(gen);
      myVector2[i][j] = dis(gen);
      myVector3[i][j] = 0; // Initialize result matrix to zero
    }
  }

  std::vector<std::thread> threads;
  int chunkSize = size / numThreads;

  for (int i = 0; i < numThreads; ++i)
  {
    int startRow = i * chunkSize;
    int endRow = (i == numThreads - 1) ? size : (i + 1) * chunkSize;

    threads.emplace_back(matrixMultiply, std::ref(myVector1), std::ref(myVector2), std::ref(myVector3), startRow,
                         endRow);
  }

  for (auto& th : threads)
  {
    th.join();
  }

  return 0;
}
