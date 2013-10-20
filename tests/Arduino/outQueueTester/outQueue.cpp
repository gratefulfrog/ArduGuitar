#include "outQueue.h"

outQueue::outQueue(){
  head = tail = NULL;
}

outQueue::outQueue(char *first){
  head = tail = new qNode;
  head->nxtptr = NULL;
  for (int i = 0; i<eLen;i++){
    head->data[i] = first[i];
    //Serial.println(first[i]);
  }
}

void outQueue::enQ(char *next){
  if (head == NULL){  // empty Queue
    head = new qNode;
    tail = head;
  }
  else{
    tail->nxtptr = new qNode;
    tail= tail->nxtptr;
  }
  tail->nxtptr = NULL;
  for (int i = 0; i<eLen;i++){
    tail->data[i] = next[i];
    //Serial.println(next[i]);
  }
}  

char* outQueue::deQ(){
  static char c[eLen];
  if (head == NULL){
    return NULL;
  }
  for (int i = 0; i<eLen;i++){
    c[i] = head->data[i];
    //Serial.println(c[i]);
  }
  qNode *temp = head->nxtptr;
  delete head;
  head = temp;
  return c;
}

char* outQueue::nthQ(int n) const{ // zero based!
  static char c[eLen];
  qNode *cur = head;
  if (head == NULL){
    return NULL;
  }
  while (n-- != 0 && cur !=NULL){
    cur = cur->nxtptr;
  }
  if (cur == NULL){
    return NULL;
  }
  else {
    for (int i = 0; i<eLen;i++){
      c[i] = cur->data[i];
      //Serial.println(c[i]);
    }
  }
  return c;
}

char* outQueue::pQ() const{
  return nthQ(0);
}
  
  

