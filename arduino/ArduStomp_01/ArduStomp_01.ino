/* ArduStomp_01
 * code to command the ARduGuitar from an arduino based stomp box.
 */

#include "biInc.h" 
#include "cyclerClass.h" 

namespace stomp {
  biInc vol(5),
        tone(5);

  int vi = 1,
      ti = 1;

  cyclerClass  neck(2),    // off, on
               middle(2),  // off, on
               bridge(3),  //off, left, both
               presets(4), // any of 4
               autom(2);    // off, on
  cyclerClass *cyclers[] = {&neck,&middle,&bridge,&presets,&autom};
}

void setup(){
   Serial.begin(9600);
 }


void loop(){
   Serial.print ("vol: " + String(stomp::vol.getVal()) + "\t");
   Serial.print ("tone: " + String(stomp::tone.getVal()) + "\t");
   Serial.print ("neck: " + String(stomp::neck.getState()) + "\t");
   Serial.print ("middle: " + String(stomp::middle.getState()) + "\t");
   Serial.print ("bridge: " + String(stomp::bridge.getState()) + "\t");
   Serial.print ("presets: " + String(stomp::presets.getState()) + "\t");
   Serial.print ("autom: " + String(stomp::autom.getState()) + "\n");
   
   inc(&stomp::vol,&stomp::vi);
   inc(&stomp::tone,&stomp::ti);
   //stomp::neck.incState();
   for (int i = 0; i< 5;i++){
     stomp::cyclers[i]->incState();
   }
   delay(1000);
 }
 
 void inc (biInc *b, int *sens){
   int v = b->getVal();
   if (v == 0) {
     *sens = 1;
   }
   else if (v ==5) {
     *sens= -1;
   }
   b->inc(*sens);
 }
     
 
