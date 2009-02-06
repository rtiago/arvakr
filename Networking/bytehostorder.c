/* Program to determine the host byte order */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
  union {
    // storage for our bytes
    short bytes;
    char arr[sizeof(short)];
  } order;

  order.bytes = 0x0102;

  if (sizeof(short) ==  2)
  {
    if (order.arr[0] == 1 && order.arr[1] == 2)
    {
      printf("big-endian\n");
    }
    else if (order.arr[0] == 2 & order.arr[1] == 1)
    {
      printf("little-endian\n");
    }
    else
      printf("unkown\n");
  }
  else
  {
    printf("sizeof(short) = %d\n",sizeof(short));
  }

  exit(0);
}
