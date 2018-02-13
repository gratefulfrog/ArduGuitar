#include "spiMgr.h"

const int ledPin = 13,
          showTime = 5; //secs


/* results
 *  2018 02 13:
 *  with SPI mode 0
 *  Vss -7.6v
 *  Vdd +7.6V
 *  bits : resistance pin 15, pin 32
 *  0     : 0L
 *  1     : 143 165
 *  0     : 0L
 *  all 1 : 27 ohm
 *  0     : 0L
 *  1     : 144 - 165 Ohm
 *  0     : 0L
 *  
 *  Vss -11.35v
 *  Vdd +11.3V
 *  22.7v
 *  bits : resistance pin 15, pin 32
 *  0     : 0L
 *  1     : 143 
 *  0     : 0L
 *  all 1 : 27 ohm
 *  0     : 27 ohm
 *  1     : 27 ohm
 *  0     : 27 ohm
 */

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
  // flash 1x, turn everything off and wait showTime seconds
  Serial.println("\nStep: 1");
  //flash(1);
  allOff();
  waitSecs(showTime);

  // flash 2x, turn on (0,0)  wait showTime seconds,
  Serial.println("\nStep: 2");
  //flash(2);
  connect00(true);  
  waitSecs(showTime);

  // flash 3x, turn off (0,0) wait showTime seconds,
  Serial.println("\nStep: 3");
  //flash(3);
  connect00(false);
  waitSecs(showTime);

  // flash 4x, turn all on,   wait showTime seconds,
  Serial.println("\nStep: 4");
  //flash(4);
  allOn();
  waitSecs(showTime);

  // flash 5x, turn all off,  wait showTime seconds,
  Serial.println("\nStep: 5");
  //flash(5);
  allOff();
  waitSecs(showTime);
  
  // flash 6x, turn on (0,0), wait showTime seconds,
  Serial.println("\nStep: 6");
  //flash(6);
  connect00(true);
  waitSecs(showTime);

  // flash 7x, turn all off,  wait showTime seconds.
  Serial.println("\nStep: 7");
  //flash(7);
  allOff();
  waitSecs(showTime);

  Serial.println("\nDone");
}
