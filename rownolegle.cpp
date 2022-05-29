#include<iostream>
#include <stdlib.h> // niezbędne dla funkcji srand i rand
#include <time.h> // niezbędne dla funkcji time
#include <cmath>
#include <bitset>
#include <stdio.h>
#include <string.h>
#include <iomanip>

using namespace std;

string toBinary(int n, int lenBits)
{
    string binary;
    while (n != 0){
        binary += ( n % 2 == 0 ? "0" : "1" );
        n /= 2;
    }
    binary.insert(0, lenBits - binary.size(), '0');
    return binary;
}

int difference(string combination, int set[])
{
  int setA = 0;
  int setB = 0;
  for(int i=0; i<combination.length(); i++) {
    if(combination[i] == '0') {
      setA += set[i];
    } else {
      setB += set[i];
    }
  }
  return abs(setA-setB);
}

int main(int argc, char *argv[])
{
    
    int n = atoi(argv[1]);
    int maxNumber = atoi(argv[2]);
    int* set = new int[n];
    unsigned int lenBits = pow(2, double(n));
    srand(time(NULL));
    cout<<"Wylosowany zbior: "<<endl;
    for(int i = 0; i < n; i++){
        set[i] = rand() % (maxNumber + 1);
        printf("%d ", set[i]);
    }
    
    int diff;
    string combinations;

    string winSet =  toBinary(0, n);
    int min = difference(winSet, set);

    string localWinSet = winSet;
    int localMin = min;

    #pragma omp parallel private(combinations, diff, localWinSet, localMin) shared(min, winSet)  num_threads(4)
    {
        #pragma omp for schedule(dynamic)
        for(int i=1; i<lenBits; i++){
            combinations = toBinary(i, n);
            diff = difference(combinations, set);
              if (diff < min) {
                localMin = diff;
                localWinSet = combinations;
            }
        }
        
        #pragma omp critical
        {
          if (localMin < min) {  
            
            min = localMin;
            winSet = localWinSet;
          }
        }
    }


    
    cout<<"\nWinset "<<winSet<<" min "<<min<<endl;
}