#include <algorithm>
#include <future>
#include <iostream>
#include <thread>
#include <vector>

using namespace std;

/**
 * The function SortThread sorts a given vector of integers in ascending order.
 *
 * @param subVector A reference to a vector of integers.
 * @return void
 */
void SortThread(vector<int> &subVector);

/**
 * The function MultiSort sorts a vector of integers using multiple threads.
 *
 * @param VectorToBeSorted A reference to a vector of integers that needs to be sorted.
 * @return void
 */
void MultiSort(vector<int> &VectorToBeSorted);

int main()
{
  cout << "Hello" << endl;
  vector<int> TestVector;
  constexpr size_t totalElements = 100000000;
  for (size_t loop = 0; loop < totalElements; loop++)
  {
    TestVector.push_back(rand());
  }
  MultiSort(TestVector);
  return 0;
}

/**
 * The function SortThread sorts a given vector of integers in ascending order.
 *
 * @param subVector A reference to a vector of integers.
 */
void SortThread(vector<int>& subVector) { sort(subVector.begin(), subVector.end()); }

/**
 * The function MultiSort sorts a vector of integers using multiple threads.
 *
 * @param VectorToBeSorted A reference to a vector of integers that needs to be sorted.
 */
void MultiSort(vector<int>& VectorToBeSorted)
{
  const unsigned int numThreads = thread::hardware_concurrency();
  const size_t chunkSize = VectorToBeSorted.size() / numThreads;

  vector<future<void>> futures;

  for (unsigned int i = 0; i < numThreads; ++i)
  {
    size_t startIdx = i * chunkSize;
    size_t endIdx = (i == numThreads - 1) ? VectorToBeSorted.size() : startIdx + chunkSize;

    vector<int> subVector(VectorToBeSorted.begin() + startIdx, VectorToBeSorted.begin() + endIdx);

    futures.emplace_back(async(SortThread, ref(subVector)));

    futures.back().wait();

    // Move sorted subvector back to the original vector
    move(subVector.begin(), subVector.end(), VectorToBeSorted.begin() + startIdx);
  }

  // Merge sorted chunks (optional if needed)
  inplace_merge(VectorToBeSorted.begin(), VectorToBeSorted.begin() + chunkSize * (numThreads - 1),
                VectorToBeSorted.end());
}
