#include <iostream>

using namespace std;

int foo(int n);
int main()
{
  foo(5);
  return 0;
}

int foo(int n)
{
  if (n == 1)
  {
    cout << 1 << endl;
  }
  else
  {
    cout << n << endl;
    foo(n - 1);
  }
  return n;
}
