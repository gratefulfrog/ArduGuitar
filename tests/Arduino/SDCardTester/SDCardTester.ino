/*  SD card read/write
 This example shows how to read and write data to and from an SD card file 	
 The circuit:
 * SD card attached to SPI bus as follows:
 ** MOSI - pin 11
 ** MISO - pin 12
 ** CLK - pin 13
 ** CS - pin 9
 
 LED on pin 5
 
 This example code is in the public domain.
 	 
 */
 
#include <SD.h>

File myFile;

void setup(){
  int i;
  Serial.begin(9600);
  Serial.println("\r\nHobbytronics Test Program for SD card...");  
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
  
  if (SD.exists("test.txt")) {
    SD.remove("test.txt");
  }

  myFile = SD.open("test.txt", FILE_WRITE);
  
  // if the file opened okay, write to it:
  if (myFile) {
    Serial.println("Writing to test.txt...");
    Serial.println("Hobbytronics Test");    
    for(i=0;i<20;i++){
      myFile.println("Hobbytronics Test of file writing");    
    }  
    // close the file:
    myFile.close();
    Serial.println("done.");
  } 
  else {
    // if the file didn't open, print an error:
    Serial.println("error opening test.txt");
  }
  
  // re-open the file for reading:
  Serial.println("\n\rReading from test.txt...");  
  myFile = SD.open("test.txt");
  if (myFile) {
    
    // read from the file until there's nothing else in it:
    while (myFile.available()) {
    	Serial.write(myFile.read());
   
    }
    // close the file:
    myFile.close();
  } 
  else {
    // if the file didn't open, print an error:
    Serial.println("error opening test.txt");
  }
  Serial.println("Test Complete.");  
}

void loop(){
}	// nothing happens after setup


