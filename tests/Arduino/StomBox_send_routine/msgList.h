#ifndef MSGLIST_H
#define MSGLIST_H

typdef msg char[5];

class msgCons {
  private:
    msg m;
    msg *n;
  public:
   msgCons(msg);
   msg carg() const;
   msg* cdr() const;
};

class msgListClass {
  private:
    msg *first,
        *last;
  public:
   msgClass();
   msgLisClass* put(msgCons);
   msgLisClass* pop();
   msg* first() const;
};



#endif
