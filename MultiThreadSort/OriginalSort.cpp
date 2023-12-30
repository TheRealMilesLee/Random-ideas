#include <algorithm>
#include <cmath>
#include <iostream>
#include <thread>
#include <vector>

using namespace std;
int main()
{
  cout << "Hello" << endl;
  vector<int> TestVector;
  for (size_t loop = 0; loop < 100000000; loop++)
  {
    TestVector.push_back(rand());
  }
  sort(TestVector.begin(), TestVector.end());
  return 0;
}
