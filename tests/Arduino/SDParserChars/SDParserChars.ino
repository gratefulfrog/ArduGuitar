/*  This version parses the data and cycle files to create:
 * an array of 4 unsigned ints as presets
 * an array of 4 chars, which are the last letters of the name of the preset,indexed on the line number
 * the layout of the preset is on 12 bits:
 * vol:4 
 * tone:4 
 * neck:1
 * middle:1
 * bridgeN:1
 * bridgeB:1
 * wasting a total of 4x4 = 16 bits... dommage
 * Correct results for the test data.tsv:
name	vol	tone	neck	middle	bNorth	bBoth <- read but ignored
Rock	6	11	0	1	0	1
Woman	10	4	1	0	0	1
Jazz	11	1	1	0	0	0
Comp	8	11	0	1	0	1
Auto	0	0	0	0	0	0   <- not read
 1717
 2633
 2840
 2229
 k 
 n
 z
 p
cycle.tsv
name	msWait <- read but ignored
Rock	1500
Woman	1500
Jazz	1500
Comp	1500

 * the struct autoStruct is a circular linked list of unsigned ints which encode
 i:2 the index of the presset in the mapp
 i:14  the delay in milliseconds must be less than or equal to 2^15 -1  32767

output cycling:
9: 1500
8: 17884
7: 34268
6: 50652
5: 1500
4: 17884
3: 34268
2: 50652
1: 1500
0: 17884
Done.
 */

#include <SD.h>

#define MAX_DELAY   (32767)
#define A_DELAY (0B11111111111111)
#define A_SHIFT (14)
#define A_INDEX (0B11)

#define P_VOL_SHIFT  (8)
#define P_TONE_SHIFT (4)
#define P_NECK_SHIFT (3)
#define P_MID_SHIFT  (2)
#define P_BN_SHIFT   (1)
#define P_BB_SHIFT   (0)

#define P_VT  (0B1111)
#define P_PUP (1)

File file;

char dFile[] = "data.tsv",
     cFile[] = "cycle.tsv",
     mapp[4];
     
unsigned int presets[4] = {0,0,0,0};

byte preVal(unsigned int i, unsigned int mask, int shift){
  return (i >> shift) & mask;
}

byte pre2byte(unsigned int i, byte key){
  switch (key) {
    case 0:
      return preVal(i,P_VT, P_VOL_SHIFT);
    case 1:
      return preVal(i,P_VT, P_TONE_SHIFT);
    case 2:
      return preVal(i,P_PUP, P_NECK_SHIFT);
    case 3:
      return preVal(i,P_PUP, P_MID_SHIFT);
    case 4:
      return preVal(i,P_PUP, P_BN_SHIFT);    
    case 5:
      return preVal(i,P_PUP, P_BB_SHIFT);    
  }
}

byte autIndex(unsigned int i){
  return (i >> A_SHIFT)  & A_INDEX ;
}

int autoVal(unsigned int i){
  return (i & A_DELAY);
}

struct autoStruct{
  unsigned int i;
  struct autoStruct *next;
};

struct autoStruct firstAuto = {0,NULL};

void skipHeaderLine(File *f){
  char c = file.read();     
  while (c!='\r' && c != '\n'){
      c = f->read();
  }    
}

// parse a data file
void parseData(File *f){
  byte line = 0,
       pos = 0;
  skipHeaderLine(f);
  while(line < 4 && f->available()){
    char c[] = {'\0', '\0', '\0'},
         cc[] = {'\0','\0'};
    c[0] = f->read();
    switch (c[0]){
      case '\r':
      case '\n':
        line++;
        pos = 0;
        //Serial.println("R or N");
        break;
      case '\t':
        pos++;
        //Serial.println("T");
        break;
      default:
        switch (pos){ 
          case 0: // first letter read  for name
            mapp[line] = c[0];
            //Serial.println(c);
            break;
          case 1: // volume, read another char and convert
            if (f->peek() != '\t'){
              //Serial.println("reading another in vol.");
              c[1] = f->read();
            }
            //Serial.println(c);
            presets[line] |= (atoi(c) << P_VOL_SHIFT);
            break;
          case 2: // tone, read another and convert
            cc[0] = f->peek();
            //Serial.print("Got this on the tone peek: ");
            //Serial.println(cc);
            if (f->peek() != '\t'){
              //Serial.println("reading another in tone.");
              c[1] = f->read();
            }
            //Serial.println(c);
            presets[line] |= (atoi(c) << P_TONE_SHIFT);
            break;
          default: // neck , mid, bridgeN, bridgeB
            presets[line] |= (atoi(c) << (6 - pos));
            //Serial.println(c);
        }
    }
  }
}

byte getLastLetter(File *f){
  char c = f->read();
  char cc[] = {'\0','\0'};
  cc[0] =  c;
  //Serial.println(cc);
  while(f->available() && f->peek() != '\t'){
    c = f->read();
    cc[0] =  c;
    //Serial.println(cc);
  }
  cc[0] =  c;
  //Serial.println(cc);
  byte ret = 0; 
  while (ret<4){
    if (mapp[ret] == c){
      break;
    }
    ret++;
  }
  //Serial.println(ret);
  return ret;
}

int getNextNumber(File *f){
  char nc[] = {'\0','\0','\0','\0','\0','\0'};
  byte i=0;
  while(f->available() && f->peek() != '\n'){
    nc[i++] = f->read();
  }
  //Serial.println(min(16384, atoi(nc)));
  return min(MAX_DELAY, atoi(nc));
}

// parse a data file
void parseAuto(File *f){
  struct autoStruct *cur = &firstAuto;
  skipHeaderLine(f);
  while(f->available()){
    cur->i  = (getLastLetter(f) << 14);
    cur->i |= getNextNumber(f);
    //Serial.print("Made one: ");
    //Serial.println(cur->i);
    if (f->available()) { // then move forward by one
      cur->next = new struct autoStruct;
      cur = cur->next;
    }
  }
  cur->next = &firstAuto;
}
  
void setup(){
  Serial.begin(115200);
  pinMode(10, OUTPUT); 
  SD.begin(10);
  File f = SD.open(dFile);
  parseData(&f);
  for (int i=0;i<4;i++){
    Serial.print(presets[i]);
    for (int j=0;j<6;j++){
      Serial.print("  ");
      Serial.print((int)pre2byte(presets[i],j)); 
    }
    Serial.println();
  }
  for (int i=0;i<4;i++){
    Serial.println(mapp[i]);
  }
  f = SD.open(cFile);
  parseAuto(&f);

  int counter = 10;
  struct autoStruct *cur = &firstAuto;
  while(counter-- >0){
    Serial.print(counter);
    Serial.print(": ");
    Serial.print(cur->i);
    Serial.print(": ");
    Serial.print((int)autIndex(cur->i));
    Serial.print(": ");
    Serial.println((int)autoVal(cur->i));
    delay(5);
    cur = cur->next;
  }

  Serial.println("Done.");
}

void loop(){
}
