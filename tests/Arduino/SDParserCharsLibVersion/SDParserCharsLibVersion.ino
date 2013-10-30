 
#include <Arduino.h>
#include <SD.h>

#include "SDReader.h"
char pFile[] = "data.tsv",
     aFile[] = "cycle.tsv";
     
PresetClass *p;
AutoClass   *a;

boolean autoOK;
  
void printPreset(byte i){
  for (byte j=0;j<6;j++){ // iterate over the 6 values: vol, tone, neck, mid, briNor, briBoth
    Serial.print("  ");
    Serial.print((int)p->presetValue(i,j)); 
  }
  Serial.println();
  Serial.flush();
}
   
void setup(){
  Serial.begin(115200);
  p = new PresetClass(pFile);
  Serial.print("preset file id: ");
  Serial.println((int)p);
  if(p->parse()){
    for (byte i=0;i<4;i++){ // iterate over the 4 presets
      printPreset(i);
    }
    char cc[] = {'R', 'W', 'J', 'C'};
    for (int i=0;i<4;i++){
      Serial.println(p->firstLetter2Index(cc[i]));
    }
  }

  a = new AutoClass(aFile,p);
  Serial.print("auto file id: ");
  Serial.println((int)a);

  autoOK = a->parse();
  if (autoOK){
    a->start(true);
  }
  Serial.println("Init Done.");
}

byte curPs = 100;
void loop(){
  if (autoOK){
    byte newPs = a->check();
    if (newPs != curPs){
      curPs = newPs;
      printPreset(curPs);
    }
  }
}
