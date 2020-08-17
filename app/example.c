#include "example.h"
#include <stdio.h>
#include <stdlib.h>

/*
commands to compile:
swig -python -py3 -modern example.i
gcc -fPIC -c example.c example_wrap.c -I/usr/include/python3.5
ld -shared example.o example_wrap.o -o _example.so


File I/O tutorial used:
https://www.tutorialspoint.com/cprogramming/c_file_io.htm
*/

int calculate_difficulty(int max) {
  //calculate playouts number for difficulty

  //find score for 5 most recent rounds so that AI is able to adjust fast
  FILE *fp;
  char buff[255];

  fp = fopen("./scores.txt", "r");
  
  char line[256];
  int count =0;
  int wins=0;
  int losses=0;

  // use array to store only last 5 results
  int myArray[5] = { 0,0,0,0,0 };
  while (fgets(line, sizeof(line), fp)) {
      count = count +1;
      myArray[(count%5)] = atoi(&line[0]) + (-1*atoi(&line[2]));
  }

  // sum the wins and losses
  int n = 0;
  for(int i =0; i<5;i++){
    n = n + myArray[i];
  } 

  fclose(fp);

  // calculate the difficulty based on results from last 5 plays
  // 80 is very hard, and 0 is very easy
  int difficulty = max/2; //neutral
  int half = difficulty;
  if(n >0){
    
    for(int i = 0;i<n;i++){
      half = half/2;
      difficulty = half + difficulty;
    }
    difficulty = (max/2) + difficulty;
  }
  else{
    n = abs(n);
    for(int i = 0;i<n;i++){
      difficulty = difficulty/2;
    }
  }

  
  return difficulty;
}

int stats(int n) {
  /*
  0 return number of wins
  1 return number of losses
  2 return number of draws
  */
  FILE *fp;
  char buff[255];

  fp = fopen("./scores.txt", "r");
  
  char line[256];
  int count =0;

  while (fgets(line, sizeof(line), fp)) {
   
      if(n == 0){
        count = count + atoi(&line[0]);
      }
      else if (n==1){
        count = count + atoi(&line[2]);
      }
      else{
        count = count + atoi(&line[4]);
      }
       
  }
    

  fclose(fp);
  
  return count;
}

int logging_score(int n) {
  // log the new score
  FILE *fp;
 
  fp = fopen("./scores.txt", "a");

  if(n == 0){
    fprintf(fp, "1 0 0\n");
  }
  else if(n==1){
    fprintf(fp, "0 1 0\n");
  }
  else{
    fprintf(fp, "2 %d 1\n",n);
  }

  fclose(fp);
  
  return n;
}

void clear_history() {
  // overwrite the file, thus erasing it
  FILE *fp;
 
  fp = fopen("./scores.txt", "w");


  fprintf(fp, "0 0 0\n");

  fclose(fp);
  
  return ;

}
