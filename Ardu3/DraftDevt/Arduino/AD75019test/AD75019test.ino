#include "spiMgr.h"

const int ledPin = 13;

SPIMgr *spiMgr;

void flashOne(){
  digitalWrite(ledPin,!digitalRead(ledPin));
  delay(500); 
  digitalWrite(ledPin,!digitalRead(ledPin));
  delay(500);      
}

void flash(int nbFlashes){
  if (nbFlashes<0){
    while(true){
      flashOne();
    }
  }
  else{
    while(nbFlashes--){
      flashOne();
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(ledPin,OUTPUT);
  digitalWrite(ledPin,LOW);
  spiMgr = new SPIMgr();
  if (!spiMgr){
    // allocation failed
    flash(-1);
  }
}

void waitSecs(int n){
   String s = String("wait ") + String(n) + String(" seconds...");
   Serial.println(s);
   delay(1000*n);
}

void allOff(){
  Serial.println("turn everything off");
  spiMgr->clear();
  spiMgr->update();
}
void allOn(){
  Serial.println("turn everything on");
  spiMgr->setAll();
  spiMgr->update();
}

void connect00(boolean set){
  String s = String("Connecting 0,0: ") + String(set);
  Serial.println(s);
  spiMgr->connect(0,0,set);
  spiMgr->update();
}

void loop() {
  // flash 1x, turn everything off and wait 10 seconds
  Serial.println("\nStep: 1");
  flash(1);
  allOff();
  waitSecs(10);

  // flash 2x, turn on (0,0)  wait 10 seconds,
  Serial.println("\nStep: 2");
  flash(2);
  connect00(true);  
  waitSecs(10);

  // flash 3x, turn off (0,0) wait 10 seconds,
  Serial.println("\nStep: 3");
  flash(3);
  connect00(false);
  waitSecs(10);

  // flash 4x, turn all on,   wait 10 seconds,
  Serial.println("\nStep: 4");
  flash(4);
  allOn();
  waitSecs(10);

  // flash 5x, turn all off,  wait 10 seconds,
  Serial.println("\nStep: 5");
  flash(5);
  allOff();
  waitSecs(10);
  
  // flash 6x, turn on (0,0), wait 10 seconds,
  Serial.println("\nStep: 6");
  flash(6);
  connect00(true);
  waitSecs(10);

  // flash 7x, turn all off,  wait 10 seconds.
  Serial.println("\nStep: 7");
  flash(7);
  allOff();
  waitSecs(10);

  Serial.println("\nDone");
}
