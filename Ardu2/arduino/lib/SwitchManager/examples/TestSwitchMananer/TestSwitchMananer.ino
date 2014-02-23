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
      Serial.println(vecs[j][i],BIN);
      //Serial.print("\t");
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


byte second[] = {
  INVERTER_INVERTED,
  INVERTER_FORWARD,  
  INVERTER_INVERTED,
  INVERTER_FORWARD,  
  VOL_0,VOL_1,VOL_2,VOL_3,
  TONE_0,TONE_4,TONE_8,TONE_10,
  COMBINATOR_PARALLEL,
  COMBINATOR_A,      
  COMBINATOR_B,      
  COMBINATOR_SERIES,
  SELECTOR_NONE,      
  VOL_4,
  TONE_11};

void setup(){
  SwitchManager::init();
  Serial.begin(9600);
  delay(5000);
  //Serial.println("ok");
  for (byte s=0;s<19;s++){
    SwitchManager::setSwitchVal(s, first[s]);
  }
  //printVecs();
  SwitchManager::executeSwitching();
  //printVecs();

  for (byte s=0;s<19;s++){
    SwitchManager::setSwitchVal(s, second[s]);
  }
  //printVecs();
  SwitchManager::executeSwitching();
  printVecs();
  

  SwitchManager::setSwitchVal(INVERTER_NECK_NORTH,INVERTER_OFF);
  printVecs();
  SwitchManager::executeSwitching();
  printVecs();

  SwitchManager::setSwitchVal(MASTER_TONE,TONE_15);
  printVecs();
  SwitchManager::executeSwitching();
  printVecs();
}

void loop(){}

/*
First:
onVec TARGET
 1010 0101    invI/4, invF/4
 1010 0101    invI/4, invF/4
 00 100000    vol5/2, vol5/6
 0000 1000    vol5/4, vol5/4
 100000 10    vol5/6, vol5/2
 1111 1111    ton15/4, ton15/4
 1111 1111    ton15/4, ton15/4
00 101 010    comA/2,  comP/3, comS/3
1111 001 1    selAB/4, comB/3, comA/1
 11 100000    ton15/2, vol5/6, 
        11    tone15/2
 */

/*
Second:
onVec TARGET
 0101 1010    invF/4, invI/4, 
 0101 1010    invF/4, invI/4, 
 10 000001    vol1/2, vol0/6
 0100 0000    vol2/4, vol1/4
 001000 00    vol3/6, vol2/2
 0100 0000    ton4/4, ton0/4
 1010 1000    ton10/4, ton8/4
01 100 101    comB/2, comA/3,  comP/3
0000 010 0    selAB/4, comS/3, comB/1
 11 010000    ton11/2, vol4/6, 
        10    tone11/2
*/

/* then set1:
curVec[0] target
 0101 000
*/
/* then set2:
curVec[17,18] target
 11 010000
        11
*/
/* results 2014 02 23
curVec
1011010
1011010
10000001
1000000
100000
1000000
10101000
1100101
100
11010000
10

after setting set1
offVec
11110000 11111111 11111111 11111111 11111111 11111111 
11111111 11111111 11111111 11111111 11111111

curVec
1010000
1011010
10000001
1000000
100000
1000000
10101000
1100101
100
11010000
10

At Set2
onVec
0
0
0
0
0
0
0
0
0
11000000
11

offVec
11111111
11111111
11111111
11111111
11111111
11111111
11111111
11111111
11111111
11111111
11111111

curVec
1010000
1011010
10000001
1000000
100000
1000000
10101000
1100101
100
11010000
11
 */
