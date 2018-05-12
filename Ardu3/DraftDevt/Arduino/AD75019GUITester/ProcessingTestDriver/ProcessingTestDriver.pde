/* ProcessingTestDriver
 * gratefulfrog
 * 2018 05 11
 *
 */

///////////////////// USER PARAMETERS /////////////////////////////

final int baudRate = 115200;
final String portName = "/dev/ttyACM0";

///////////////////// END of USER PARAMETERS /////////////////////////////

import processing.serial.*;
import java.util.*;

Serial commsPort;       // The serial port
boolean messageArrived = false; 

String incoming = "";

final char startChar        = '*',  // start of a message from the arduino
           endChar          = '#',  // end of a message from the arduino
           contactCharacter = '|';  // indactes the arduino is trying to make contact and start a session

final int msgLength = 16 + 256;

int inCount=0;  

void processIncoming () {
  // do stuff here!
}

// When we want to print to the window
void ShowIncoming() {
  //println(incoming);
  int i=0;
  while(i<incoming.length()){
    println(incoming.substring(i,i+16));
    i+=16;
  }
  print("reply count : ");
  println(++inCount);
}

void setup() {
  size(1000, 800);  // Stage size
  fill(255);
  background(0);
  
  //printArray(Serial.list());
  commsPort = new Serial(this, portName, baudRate);
}

char processOneChar(char inChar){
  switch (inChar) {
    case contactCharacter:
      commsPort.write(contactCharacter);       // ask for more
      println("starting...");
      
      break;
    default:      
      if (!messageArrived){
        return inChar;
      }      
      break;
  }
  return '!';
}

void draw() {
  if (commsPort.available()>0){
    char c = processOneChar(commsPort.readChar());
    if (c != '!'){
      incoming += c; 
    }
  }
  //println(incoming.length());
  if (incoming.length() == msgLength){
    messageArrived = true;
    println("arrived!");
  }
  if (messageArrived) {
    background(0);
    println("goop");
    processIncoming();
    ShowIncoming();
    messageArrived= false;
    incoming = "";
  }
}
/*
void serialEvent(Serial commsPort) {
  // read a byte from the serial port:
  char inChar = commsPort.readChar();
  switch (inChar) {
    case contactCharacter:
      commsPort.write(contactCharacter);       // ask for more
      println("starting...");
      break;
    default:      
      if (!messageArrived){
        incoming += inChar;
        //println("got one");
      }      
      break;
  }
}
*/
int oneCount=0,
    xlen = 16;

void mouseClicked(){
  if (mouseButton == LEFT) {
    commsPort.write('p');
    print("sending : ");
    println('p');
  } 
  else{
    String s= "x",
           zerosX16_256 = "";
    for (int i=0;i<(16+256);i++){
      zerosX16_256 += '0';
    }
    for (int i=0;i<oneCount;i++){
      s+="1";
    }
    while (s.length()<(xlen+1)){
      s+="0";
    }
    oneCount = (oneCount+1)%(xlen+1);
    print("sending : ");
    println(s+zerosX16_256);
    commsPort.write(s+zerosX16_256  );
  } 
}
