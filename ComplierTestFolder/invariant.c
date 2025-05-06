#include <stdio.h>

int bar(int *p, int *q);

int main()
{
  int numbers = 10;
  int *p = &numbers;
  // int numbers2 = 10;
  int *q = &numbers;
  int results = bar(p, q);
  printf("Results: %i\n", results);
  return 0;
}

int bar(int *p, int *q)
{
  if (*p != *q)
  {
    return 10;
  }
  (*q)++;
  (*p)++;
  (*q)++;
  printf("p: %i, q: %i\n", *p, *q);
  return (*p < *q);
}
