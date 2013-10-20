#ifndef OUTQUEUE_H
#define OUTQUEUE_H

#include <Arduino.h>

/////////////////////////////////////
// this is where the lenght of elements in the queue is defined!!
#define ELEN 5

typedef struct qNode {
  char data[ELEN];
  struct qNode *nxtptr;
} qNode_t;

class outQueue {
  private:
   qNode *head,
         *tail;       
  public:
    static const int eLen=ELEN;
    outQueue();
    outQueue(char *first);
    void enQ(char*);
    char* deQ();
    char* nthQ(int n) const; // peek the nth elt of the queue
    char* pQ() const;  // peek the top elt of the queue!
};

#endif
