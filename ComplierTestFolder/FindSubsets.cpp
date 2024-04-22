#include <iostream>
#include <vector>

using namespace std;

// Function to generate all subsets of a given set
void generateSubsets(vector<int> &S, vector<int> &subset, int index);

// Main function
int main()
{
  // Example set S
  vector<int> S = {1, 2, 3, 4};

  // Empty subset to start with
  vector<int> subset;

  // Generate subsets
  generateSubsets(S, subset, 0);

  return 0;
}

void generateSubsets(vector<int> &S, vector<int> &subset, int index)
{
  for (size_t loop = 0; loop < S.size(); loop++)
  {
    for (size_t i = 0; i < subset.size(); i++)
    {
      cout << subset[i] << " ";
    } 
  }
}
