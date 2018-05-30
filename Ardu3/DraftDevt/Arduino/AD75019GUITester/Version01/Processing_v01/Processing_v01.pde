/* ProcessingTestDriver
 * gratefulfrog
 * 2018 05 11
 * v_01
 */

/* Wiring of the AD75019 for this experiment
 * 
 * SPI     : CLK, DI, SS from the Arduino to the AD75019 as per datasheet
 * Vdd/Vss : +/-12v from my boost psu, with 100nF decoupling cap to ground
 * Vcc     : +5v from Arduino, with 100nF decoupling cap to ground
 * DGND    : to Arduino GND
 * diodes as per Power Supply Sequencing and Bypassing section of datasheet
 * startup sequence : +/- 12v then Arduino boot, then +5v
 *
 * analog pins:
 * X0, X1  : signal generator + and GND, i.e. A+ and A-
 * X2,Y0   == B+
 * X3,Y1   == B-
 * ...
 * X11,Y9  == F+
 * X12,Y10 == F-
 * Y11     == O+  (i.e. Amp plus input)
 * Y12     == O-  (i.e. Amp gnd input)
 *
 *  2018 05 29 Results:
 * 3v Peak to Peak 440Hz sine wave, works as expected,
 * If all connections are turned on, AD75019 latches up and needs to be completely powered down and then restarted.
 */



///////////////////// USER PARAMETERS /////////////////////////////

final int baudRate = 115200;
final String portName = "/dev/ttyACM0";

///////////////////// END of USER PARAMETERS /////////////////////////////

import processing.serial.*;
import java.util.*;

Serial commsPort;

boolean autoExec = false;
final int autoExecPause = 2000; // milliseconds
int lastExecTime = 0;

final int maxRecDelay = 5000; // 15 seconds
int lastRecTime = -0;

final color bg = 0,
            fg = 255;
final char contactChar = '|',  // confirms arduin handshake
           pollChar    = 'p',
           execChar    = 'x';

final String startupMsg     = "Version 01: No Arduino pin reading or writing\nstarting...",
             nbFormat       = "%4d : ",
             recMsg         = "Received : ",
             sendMsg        = "Sent : ",
             actionIDFormat = "%3d";
 
final int XYValuesLength = 16,
          spiBitsLength  = 256,
          outMsgLength   = XYValuesLength + spiBitsLength,
          inMsgLength    = 2*XYValuesLength + spiBitsLength;

String outXBits   = "",
       outSPIBits = "";
int outXBitsIndex   = 0,
    outSPIBitsIndex = 0,
    xStep           = 3,
    bitStep         = 5;

int inCount=0,
    outCount=0;
boolean messageArrived = false; 
String incoming = "";
boolean running = true;

Gui gui;

void initOutBits(){
  outXBits = "";
  outSPIBits="";
  for(int i=0;i<XYValuesLength;i++){
    outXBits+="0";
  }
  for(int i=0;i<spiBitsLength;i++){
    outSPIBits+="0";
  }
  outXBitsIndex = 0;
  outSPIBitsIndex=0;
}

void setup() {
  //fullScreen();
  size(1000, 800); 
  initOutBits();
    commsPort = new Serial(this, portName, baudRate);
  fill(fg);
  background(bg);
  gui = new Gui();  
}

void processIncoming () {
  gui.display(incoming,autoExec);  // do stuff here!
}
void showBitsAsString(String bits, int size){
  for(int i=0;i<bits.length(); i+=size){
    println(String.format(nbFormat,i) + bits.substring(i,i+XYValuesLength));
  }
}

void receiveFromComms(String s, boolean countIt, int size){
   String displayMsg = (countIt 
                       ? String.format(nbFormat, inCount++) 
                       : "") 
                       + recMsg;
   println(displayMsg);
   showBitsAsString(s, size);
 }

// When we want to print to the window
void ShowIncoming() {
  receiveFromComms(incoming,true,XYValuesLength);
}

void send2Comms(char c, boolean countIt){
  String displayMsg = (countIt 
                       ? String.format(nbFormat, outCount++) 
                       : "") 
                       + sendMsg + String.valueOf(c);
  //println(displayMsg);
  commsPort.write(c);
}
 
void send2Comms(String s, boolean countIt, int size){
  String displayMsg = (countIt ? String.format(nbFormat, outCount++) : "") + sendMsg + s.substring(0,1);
  //println(displayMsg);
  //showBitsAsString(s.substring(1,s.length()),size);
  commsPort.write(s);
}

char notChar(char c){
  return c== '0' ? '1' : '0';
}


boolean timeToPoll(){
  if (((millis() - lastRecTime) > maxRecDelay) ||
      (millis() < lastRecTime)){
      return true;
      }
  return false;
}

void poll(){
  send2Comms(pollChar,true);
}

boolean timeToExec(){
  if (((millis() - lastExecTime) > autoExecPause) ||
      (millis() < lastExecTime)){
      return true;
      }
  return false;
}

void exec(){  
  send2Comms(execChar+outXBits+outSPIBits,true,XYValuesLength);
  // now inc outbits
  String newBits = "";
  for(int i=0;i<XYValuesLength;i++){
    newBits+= (i==outXBitsIndex ? notChar(outXBits.charAt(i)) : outXBits.charAt(i)); 
  }
  outXBitsIndex = (outXBitsIndex+xStep) % XYValuesLength;
  outXBits = newBits;
  newBits = "";
  for(int i=0;i<spiBitsLength;i++){
    newBits+= (i==outSPIBitsIndex ? notChar(outSPIBits.charAt(i)) : outSPIBits.charAt(i)); 
  }
  outSPIBitsIndex = (outSPIBitsIndex+bitStep) % spiBitsLength;
  outSPIBits = newBits;
  lastExecTime = millis();
}

void draw() {
  if (messageArrived) {
    background(bg);
    processIncoming();
    //ShowIncoming();
    messageArrived= false;
    incoming = "";
  }
  if (timeToPoll()){
    poll();
  }
  if (autoExec && timeToExec()){
    exec();
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

void connectionsAllOff(){
  outSPIBits="";
  for(int i=0;i<spiBitsLength;i++){
    outSPIBits+="0";
  }
  outSPIBitsIndex=0;
}
void connectionsAllOn(){
  outSPIBits="";
  for(int i=0;i<spiBitsLength;i++){
    outSPIBits+="1";
  }
  outSPIBitsIndex=0;
}

void clearMonitor(){
  for(int i= 0; i< 100;i++){
    println();
  }
}

void mouseClicked(){
    int actionID = gui.getMouseAction(mouseX,mouseY);
    switch(actionID){
      case -2:
        // all exec toggles
        println("toggle autoexec");
        autoExec = ! autoExec;
        break;
      case -1:
        // connections toggles
        if (mouseButton == LEFT) {
          println("all connections: OFF");
          connectionsAllOff();
        }
        else{
          println("all connections: ON");
          connectionsAllOn();
        }
        send2Comms(execChar+outXBits+outSPIBits,true,XYValuesLength);
        break;
      default:
        if (actionID >= 0 && actionID < outMsgLength){  
           autoExec = false;
           println("actionID : ", String.format(actionIDFormat,actionID));
           
           if(actionID<XYValuesLength){    // it's an X button
             println("Not sending anything...");
             /*         
             String newXBits = "";
             for(int i=0;i<XYValuesLength;i++){
               newXBits+= (actionID==i ? notChar(outXBits.charAt(i)) : outXBits.charAt(i)); 
              }
              outXBits = newXBits;
              send2Comms(execChar+outXBits+outSPIBits,true,XYValuesLength);
              lastExecTime = millis();
              */
           }
           else if (actionID >= XYValuesLength && actionID < outMsgLength){  // it's a Matrix Button
             String newSPIBits = "";
             int targetId = actionID - XYValuesLength;
             for(int i=0;i<spiBitsLength;i++){
               newSPIBits+= (targetId == i ? notChar(outSPIBits.charAt(i)) : outSPIBits.charAt(i)); 
             }
             outSPIBits = newSPIBits;
             send2Comms(execChar+outXBits+outSPIBits,true,XYValuesLength);
             lastExecTime = millis();
           }
        }
        else{
          // clear the message display
          clearMonitor();
        }
        break;
    }
}

void keyPressed(){
  if(running){
    noLoop();
  }
  else{
    loop();
  }
  running = !running ;
}
