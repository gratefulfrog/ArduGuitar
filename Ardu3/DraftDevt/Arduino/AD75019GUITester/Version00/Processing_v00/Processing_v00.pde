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

Serial commsPort;

final color bg = 0,
            fg = 255;
final char contactChar = '|',  // confirms arduin handshake
           pollChar    = 'p',
           execChar    = 'x';

final String startupMsg = "starting...",
             nbFormat   = "%3d : ",
             recMsg     = "Received : ",
             sendMsg    = "Sent : ";
 
final int XYValuesLength = 16,
          spiBitsLength  = 256,
          outMsgLength   = XYValuesLength + spiBitsLength,
          inMsgLength    = 2*XYValuesLength + spiBitsLength;

int inCount=0,
    outCount=0;
boolean messageArrived = false; 
String incoming = "";

final int maxRecDelay = 5000; // 5 seconds
int lastRecTime = 0;

void processIncoming () {
  // do stuff here!
}

// When we want to print to the window
void ShowIncoming() {
  receiveFromComms(incoming,true,XYValuesLength);
}

void setup() {
  size(1000, 800); 
  commsPort = new Serial(this, portName, baudRate);
  fill(fg);
  background(bg);
}

void draw() {
  if (messageArrived) {
    background(bg);
    processIncoming();
    ShowIncoming();
    messageArrived= false;
    incoming = "";
  }
  if (timeToPoll()){
    poll();
  }
 }

void serialEvent(Serial commsPort) {
  char inChar = commsPort.readChar();
  if (inChar == contactChar) {
    send2Comms(contactChar, false);
    println(startupMsg);
  }
  else if (!messageArrived){
    incoming += inChar;
    if (incoming.length() == inMsgLength)
      messageArrived = true;
      lastRecTime = millis();
  }
}

void poll(){
  send2Comms(pollChar,true);
}

int oneCount=0;
void exec(){  
  String s    = String.valueOf(execChar),
         bits = "";
  for (int i=0;i<oneCount;i++){
      bits+="1";
    }
    while (bits.length()<outMsgLength){
      bits+="0";
    }
    oneCount = (oneCount+1)%(outMsgLength+1);
  s+=bits;
  send2Comms(s,true,XYValuesLength);
}
  
void mouseClicked(){
  if (mouseButton == LEFT) {
    poll();
  }
  else{
    exec();
  } 
}

void showBitsAsString(String bits, int size){
  for(int i=0;i<bits.length(); i+=size){
    println(String.format("%3d : ",i) + bits.substring(i,i+XYValuesLength));
  }
}

void send2Comms(char c, boolean countIt){
  String displayMsg = (countIt 
                       ? String.format(nbFormat, outCount++) 
                       : "") 
                       + sendMsg + String.valueOf(c);
  println(displayMsg);
  commsPort.write(c);
 }
 
 void send2Comms(String s, boolean countIt, int size){
  String displayMsg = (countIt ? String.format(nbFormat, outCount++) : "") + sendMsg + s.substring(0,1);
  println(displayMsg);
  showBitsAsString(s.substring(1,s.length()),XYValuesLength);
  commsPort.write(s);
 }
 
 void receiveFromComms(String s, boolean countIt, int size){
   String displayMsg = (countIt 
                       ? String.format(nbFormat, inCount++) 
                       : "") 
                       + recMsg;
   println(displayMsg);
   showBitsAsString(s, size);
 }

boolean timeToPoll(){
  if (((millis() - lastRecTime) > maxRecDelay) ||
      (millis() < lastRecTime)){
      return true;
      }
  return false;
}
