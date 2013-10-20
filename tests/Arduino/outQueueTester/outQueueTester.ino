#include "outQueue.h"
#define NBTESTS 10
#define MOTLIMIT 3


outQueue *q;

char *mot = new char[q->eLen];
int incomingCount = 0,
    motCount=0;
    
void  printTop(){
   char *cc = q->pQ();
   if(cc != NULL){
     char c[q->eLen+1];
     for (int j=0;j<q->eLen;j++){
        c[j]=cc[j];
      }
      c[q->eLen] = '\0';
    Serial.println(c);
 }
}
void  printLast(){
   char *cc = q->nthQ(motCount-1);
   if(cc != NULL){
     char c[q->eLen+1];
     for (int j=0;j<q->eLen;j++){
        c[j]=cc[j];
      }
      c[q->eLen] = '\0';
    Serial.println(c);
 }
}
  
void printAll(){
   char *cc = q->deQ();
 while(cc != NULL){
   char c[q->eLen+1];
   for (int j=0;j<q->eLen;j++){
      c[j]=cc[j];
    }
    c[q->eLen] = '\0';
    Serial.println(c);
    cc = q->deQ();
 }
}

void setup(){
  Serial.begin(115200);
  while(!Serial);
  delay(5);
  Serial.println("test");
  char s[] = "12345",
       p[] = "abcde";
 q = new outQueue();
 for (int i=0;i<NBTESTS;i++){
   q->enQ(p);
   Serial.println("enqd p");
   q->enQ(s);
   Serial.println("enqd s");
 }
 printAll();
}

void loop() {
  if(Serial.available()>0){
    mot[incomingCount++] = Serial.read();
  }
  if (incomingCount == q->eLen) {
    q->enQ(mot);
    incomingCount=0;
    motCount++;
    printTop();
    printLast();
  }
  if (motCount == MOTLIMIT){
    printAll();
    motCount=0;
  }
}
