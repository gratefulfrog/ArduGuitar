/*  SD card read/write
 This example shows how to read and write data to and from an SD card file 	
 The circuit:
 * SD card attached to SPI bus as follows:
 ** 5V  ->  5V
 ** 3V3 ->  ()
 ** gnd ->  GND
 ** CLK ->  pin 13  (CLK)
 ** DO  ->  pin 12  (MISO)
 ** DI  ->  pin 11  (MOSI)
 ** CS  ->  pin 9  (can be any)
 ** CD  ->  ()
 
 //LED on pin 5
 
 This example code is in the public domain.
 	 
 */
 
#include <SD.h>

File myFile;

char dFile[] = "data.tsv",
     cFile[] = "cycle.tsv";

struct presetStruct{
  String name;
  int val[6];
} ;

struct autoStruct{
  String name;
  int ms;
};

struct presetStruct presets[4];
struct autoStruct autos[10];


void readUntilNewLine(String *s, File f){
  char c[]={'\0','\0'};
  while (f.available() && c[0] != '\n'){
    c[0]= (char)f.read();
    *s += c;
  }
  //Serial.println("Read: " + *s);
}

void splitPreset(const String *s, struct presetStruct *ps){
  int tabIndex = s->indexOf('\t');
  ps->name = s->substring(0,tabIndex);
  for (int i=0;i<5;i++){
    int nextTabIndex = s->indexOf('\t',tabIndex+1);
    ps->val[i] = s->substring(tabIndex+1,nextTabIndex).toInt();
    tabIndex = nextTabIndex;
  }
  ps->val[5]=s->substring(tabIndex+1).toInt();
}

void splitAuto(const String *s, struct autoStruct *as){
  int tabIndex = s->indexOf('\t');
  as->name = s->substring(0,tabIndex);
  as->ms = s->substring(tabIndex+1).toInt();
  //Serial.println(as->name);
  //Serial.println(as->ms);
}

void readTSVData(File f,int nbLines2Read, boolean isPresets){
  String s="";
  readUntilNewLine(&s,f);
  int lineNumber = 0;
  while (f.available() && lineNumber < nbLines2Read){
    s="";
    readUntilNewLine(&s,f);
    if (isPresets){
      splitPreset(&s,&presets[lineNumber]);
    }
    else{
      splitAuto(&s,&autos[lineNumber]);
    }
    lineNumber++ ;
  }
}

void setup(){
  Serial.begin(115200);
  delay(2000);
  Serial.println("Initializing SD card...");
  // On the Ethernet Shield, CS is pin 4. It's set as an output by default.
  // Note that even if it's not used as the CS pin, the hardware SS pin 
  // (10 on most Arduino boards, 53 on the Mega) must be left as an output 
  // or the SD library functions will not work. 
  pinMode(10, OUTPUT);
   
  if (!SD.begin(9)) {
    Serial.println("initialization failed!");
    return;
  }
  Serial.println("initialization done.");
  
  // open the file for reading:
  Serial.println("\n\rReading from: " + String(dFile));
  myFile = SD.open(dFile);
  if (myFile) {
    readTSVData(myFile,4,true);
    myFile.close();
  } 
  else {
    // if the file didn't open, print an error:
    Serial.println("error opening: " + String(dFile));
  }
  for (int i=0;i<4;i++){
    Serial.print(presets[i].name + "  ");
    for(int j=0;j<6;j++){
      Serial.print(presets[i].val[j]);
      Serial.print("  ");
    }
    Serial.println();
  }
  Serial.println("\n\rReading from: " + String(cFile));
  myFile = SD.open(cFile);
  if (myFile) {
    readTSVData(myFile,10,false);
    myFile.close();
  } 
  else {
    // if the file didn't open, print an error:
    Serial.println("error opening: " + String(cFile));
  }
  for (int i=0;i<10;i++){
    if (autos[i].name == ""){
      break;
    }
    Serial.print(autos[i].name);
    Serial.print("  ");
    Serial.println(autos[i].ms);
  }
  Serial.println("Test Complete.");  
}

void loop(){
}	// nothing happens after setup


