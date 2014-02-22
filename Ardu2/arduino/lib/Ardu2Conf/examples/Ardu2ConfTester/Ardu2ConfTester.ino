// -*- c++ -*-
#include <Ardu2Conf.h>

void setup(){
  Ardu2Conf::init();
  Serial.begin(9600);
  while (!Serial);
  delay(5000);
  
  char *names[] = {"curVec","onVec","offVec"};
  byte *vecs[] = {Ardu2Conf::curVec,Ardu2Conf::onVec,Ardu2Conf::offVec};

  for (byte j = 0;j<3;j++){
    Serial.println(names[j]);
    for (byte i = 0;i<NB_SHIFT_REGS; i++){
      Serial.print(vecs[j][i],BIN);
      Serial.print("\t");
    }
    Serial.println();
  }
}

void loop(){
}
