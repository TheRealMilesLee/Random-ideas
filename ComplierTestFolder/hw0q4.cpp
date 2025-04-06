#include <iostream>

using namespace std;

int main()
{
  int x, y, i;
  x = y = i = 0;
  while (i < 25)
  {
    i++;
    x++;
    cout << i << " ";
    if (i % 2 == 0)
    {
      y++;
      cout << y << endl;
    }
    cout << endl;
  }
  return 0;
}
