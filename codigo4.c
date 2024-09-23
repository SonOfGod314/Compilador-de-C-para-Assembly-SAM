int main(){
    int r;
    int a;
    int b;
    int x;

    r = 0;
    a = 1;
    b = 100;
    x = 0;

    while (a <=b){
        a = a * 2;
        x = x + 1;
    }

    if (x < 10){
        r = x;
        printf(r);
    }
    else{
        r = 10;
        printf(r);
    }
    endif

}
