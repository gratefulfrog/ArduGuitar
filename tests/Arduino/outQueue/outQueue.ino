#include "outQueue.h"

outQueue *q;

void setup(){
  Serial.begin(115200);
  q = new outQueue();
  String s = "12345",
         p = "abcde";
 q->enQ(s);
 q->enQ(p);
 for (i=0;i<2;i++){
   char c[q->eLen+1],
        cc[q->eLen] = q->deQ();
    for (j=0;j<q->eLen;j++){
      c[j]=cc[j];
    }
    c[q->eLen] = '\0';
    Serial.println(c);
 }
}

void loop() {
}
