#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <vector>

using namespace std;

int main()
{
  vector<int> v;
  srand(time(0)); // Seed the random number generator
  for (size_t i = 0; i < 327680000; i++)
  {
    v.push_back(rand());
  }

  // Binary search
  int target = 10240;
  v[rand() % v.size()] = target; // Randomly place the target in the vector
  sort(v.begin(), v.end());
  bool found = false;
  int start = 0;
  int end = v.size() - 1;
  int FoundIndex = -1;
  while (start <= end && !found)
  {
    int mid = start + (end - start) / 2;
    if (v[mid] == target)
    {
      found = true;
      FoundIndex = mid;
    }
    else if (v[mid] < target)
    {
      start = mid + 1;
    }
    else
    {
      end = mid - 1;
    }
  }
  if (FoundIndex != -1)
  {
    cout << "Found at index: " << FoundIndex << endl;
  }
  else
  {
    cout << "Not found" << endl;
  }
}
