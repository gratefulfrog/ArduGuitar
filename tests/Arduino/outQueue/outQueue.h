#ifndef OUTQUEUE_H
#define OUTQUEUE_H

#include <Arduino.h>

typedef struct qNode
{
  char data[5];
  struct qNode *nxtptr;

} qNode_t;

class outQueue {
  private:
   qNode *head,
         *tail; 
  public:
    static const int eLen = 5;
    outQueue();
    char* deQ();
    void enQ(String s);
    char** elts();
};

#endif
