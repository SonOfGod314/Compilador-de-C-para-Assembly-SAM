int main(){
  int b;
  int n;
  int i;

  b = 2;
  n = 5;
  i = 1;

  while (i <= n) {
    b = b * i;
    i = i + 1;
  }
  
  printf(b);
}
