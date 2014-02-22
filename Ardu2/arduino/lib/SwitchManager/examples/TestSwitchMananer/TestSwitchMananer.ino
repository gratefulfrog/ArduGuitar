// -*- c++ -*-

#include <SPI.h>
#include <Ardu2Conf.h>
#include <SwitchManager.h>

void printVecs(){
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

byte first[] = {
  INVERTER_FORWARD,  
  INVERTER_INVERTED,
  INVERTER_FORWARD,  
  INVERTER_INVERTED,
  VOL_5,VOL_5,VOL_5,VOL_5,
  TONE_15,TONE_15,TONE_15,TONE_15,
  COMBINATOR_SERIES,
  COMBINATOR_PARALLEL,
  COMBINATOR_A,      
  COMBINATOR_B,      
  SELECTOR_A_B,      
  VOL_5,
  TONE_15};


void setup(){
  SwitchManager::init();
  Serial.begin(9600);
  delay(5000);
  Serial.println("ok");
  for (byte s=0;s<19;s++){
    SwitchManager::setSwitchVal(s, first[s]);
  }
  printVecs();
}

void loop(){}
