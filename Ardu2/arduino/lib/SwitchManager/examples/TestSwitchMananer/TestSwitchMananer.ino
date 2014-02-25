// -*- c++ -*-

#include <SPI.h>
#include <Ardu2Conf.h>
#include <SwitchManager.h>

void printVecs(byte howMany=3){
  char *names[] = {"curVec","onVec","offVec"};
  byte *vecs[] = {Ardu2Conf::curVec,Ardu2Conf::onVec,Ardu2Conf::offVec};
  for (byte j = 0;j<howMany;j++){
    Serial.println(names[j]);
    for (byte i = 0;i<NB_SHIFT_REGS; i++){
      Serial.println(vecs[j][i],BIN);
      //Serial.print("\t");
    }
    Serial.println();
  }
}

void runComponentSwitches(){
  byte first[] = {INVERTER_FORWARD,  
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
		  TONE_15},
    second[] = {INVERTER_INVERTED,
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
    
    Serial.println("Running Component Switches");
    for (byte s=0;s<19;s++){
      SwitchManager::setComponent(s, first[s]);
    }
    //printVecs(1);
    SwitchManager::executeSwitching();
    //printVecs(1);
    
    for (byte s=0;s<19;s++){
      SwitchManager::setComponent(s, second[s]);
    }
    //printVecs(1);
    SwitchManager::executeSwitching();
    printVecs(1);
        
    SwitchManager::setComponent(INVERTER_NECK_NORTH,INVERTER_OFF);
    printVecs(1);
    SwitchManager::executeSwitching();
    printVecs(1);
    
    SwitchManager::setComponent(MASTER_TONE,TONE_15);
    printVecs(1);
    SwitchManager::executeSwitching();
    printVecs(1);
}

void runSingleSwitches(){
  byte onList1[10],
    onList2[10],
    offList1[10],
    offList2[10];
  byte *ptrLis[] = {onList1,offList1,onList2,offList2};
  

  Serial.println("Running Single Switches");
  for (byte  b=0;b<10;b++){
    onList1[b] = 2*b;
    onList2[b] = 3*b;
    offList1[b] = 4*b;
    offList2[b] = 6*b;
  }
  for(byte b =0;b<2;b++){
    for (byte c=0;c<10;c++){
      SwitchManager::setSwitch(ptrLis[b*2][c], true);
      SwitchManager::setSwitch(ptrLis[(b*2)+1][c], false);
    }
    SwitchManager::executeSwitching();
    printVecs(1);
  }
}

void setup(){
  Ardu2Conf::init();
  SwitchManager::init();
  Serial.begin(9600);
  delay(5000);
  runComponentSwitches();
  Ardu2Conf::init();
  runSingleSwitches();
}

void loop(){}

/* single swith tests:
On 1:
0,2,4,6,8,10,12,14,16,18
Off 1:
0,4,8,12,16,20,24,28,32,36
Net result:
On: 2,6,10,14,18

On 2:
0,3,6,9,12,15,18,21,24,27
+
2,6,10,14,18
= 0,2,3,6,9,10,12,14,15,18,21,24,27
Off 2:
0,6,12,18,24,30,36,42,48,54
Net on:
2,3,9,10,14,15,21,27

Results 2014 02 25:

Running Single Switches
curVec
1000100
1000100
100
0
0
0
0
0
0
0
0

curVec
1100
11000110
100000
1000
0
0
0
0
0
0
0
*/


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
/* results 2014 02 25
Running Component Switches
curVec
1011010
1011010
10000001
1001000
100010
1000000
10101000
1100101
101
11010000
11

curVec
1011010
1011010
10000001
1001000
100010
1000000
10101000
1100101
101
11010000
11

curVec
1010000
1011010
10000001
1001000
100010
1000000
10101000
1100101
101
11010000
11

curVec
1010000
1011010
10000001
1001000
100010
1000000
10101000
1100101
101
11010000
11

curVec
1010000
1011010
10000001
1001000
100010
1000000
10101000
1100101
101
11010000
11
 */
