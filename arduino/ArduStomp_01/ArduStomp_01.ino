/* ArduStomp_01
 * code to command the ARduGuitar from an arduino based stomp box.
 */

#define DEBUG
#include <Arduino.h>
#include "biInc.h" 
#include "cyclerClass.h" 
#include "confClass.h" 

#define VUP_PIN 1
#define VDW_PIN 2
#define TUP_PIN 3
#define TDW_PIN 4
#define N_PIN   5
#define M_PIN   6
#define B_PN    7
#define P_PIN   8
#define A_PIN   9

int pins[]= {VUP_PIN,
             VDW_PIN,
             TUP_PIN,
             TDW_PIN,
             N_PIN,
             M_PIN,
             B_PN,
             P_PIN,
             A_PIN };

const int nbButtons = 9;

confClass conf;

String volUp(){return conf.incVT(0,1);}
String volDown(){return conf.incVT(0,-1);}

String toneUp(){return conf.incVT(1,1);}
String toneDown(){return conf.incVT(1,-1);}

String neck(){return conf.incPup(0);}
String middle(){return conf.incPup(1);}
String bridge(){return conf.incPup(2);}

String preset() {return conf.incPreset();}
String autoL(){;}


typedef String (*buttonFuncPtr)();

buttonFuncPtr buttonFuncs[]= { &volUp,     
                               &volDown,
                               &toneUp,
                               &toneDown,
                               &neck,
                               &middle,
                               &bridge,
                               &preset,
                               &autoL};



void msg(String s){
  #ifdef DEBUG
  Serial.print(s + '\n');
  #endif
}

void setupPins(){
   for (int i=0;i<nbButtons;i++){
     pinMode(pins[i],INPUT);
   }
   msg("Pins setup!");
}

void setupData(){
  msg("Setup Data!");
  commBT(conf.incPreset());
}

void commBT(String s){
  msg(s);
}

void setup(){
   Serial.begin(9600);
   msg("Starting...");
   setupPins();
   setupData();
   msg("5 seconds delay...");
   delay (5000);
 }

boolean buttonPressedNow(int i){
 // just for tests
 int pressed[] =  {0,0,0,0,0,
                   1,1,1,1,1,
                   2,2,2,2,2,
                   3,3,3,3,3,
                   4,4,
                   5,5,
                   6,6,6,
                   7,7,7,7};
 static int current = 0;
 boolean result =  i== pressed[current];
 if (result){
   current = (current + 1)% 31;
   msg("pressed: "+ String(i));
   
 }
 return  result;
}

void checkButtons(){
  for (int i=0;i<nbButtons;i++){
    if(buttonPressedNow(i)){
      commBT((*buttonFuncs[i])());
    }
  }
}

int sens =  1;

void loop(){
  checkButtons();
  /*
  // this test loop cycles through all the possible values of vol, tone, pups.
  // demonstrating that everyting works ok, or at least seems to do so;
  // for vol, tone and pup inc-ing
  /*String s = conf.incVT(0,sens); 
   s +=   "\t" + conf.incVT(1,sens++); 
   if (sens == 6 ) { 
     sens = -4;
   }
   
   for (int i= 0 ; i<3;i++){
     s += "\t"+ conf.incPup(i);
   }
   
   // test preset inc-ing
   String s = conf.incPreset();
   commBT(s);
   */
   delay(1000);
 }
 
