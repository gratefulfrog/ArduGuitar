/*
 * This example sketch allows RN-42 bluetooth module to
 * communicate via Serial1 on an Arduino Micro or Leonardo 
 
 * RN42 behavoir:
 * - power on: slow red blink
 * - command mode: quick red blink, searching for a connection... needs up to 10 seconds!
 * - connected: solid green
 * - loss of connection: slow red blink
 * - connection re-established (only with last connected RN42!): solid green 
 */

const String commandModeConfirmationString = "CMD";

void setup(){
  setupRN42AndConnect();
  setupSerial();
}

void setupRN42AndConnect(){
  Serial1.begin(115200);
  while(!Serial1);
  while (!setupCommandMode());
  doConnect();
  delay(10000);  // this is needed in the case of a long inquiry!
  clearRN42Output();
}

void clearRN42Output(){
  while (Serial1.available()){
    Serial1.read();  
  }
}

void doConnect(){
  Serial1.println("SR,Z");
  Serial1.println("R,1");
}

boolean setupCommandMode(){ 
  Serial1.print("$");  // Print three times individually
  Serial1.print("$");
  Serial1.print("$");  // Enter command mode
  delay(100);  // Short delay, wait for the Mate to send back CMD
  
  String rn42Output = "";
  while(Serial1.available()){
    rn42Output += (char)Serial1.read();  
  }
  boolean ret = rn42Output.indexOf(commandModeConfirmationString)>-1;
  return ret;
}

void setupSerial(){
  Serial.begin(115200);  // Begin the serial monitor at 115200bps
  while(!Serial);
}

void loop() {
  if(Serial1.available()){  // If the bluetooth sent any characters
    // Send any characters from the bluetooth to the serial monitor
    Serial.print((char)Serial1.read());  
  }
  if(Serial.available()) {  // If stuff was typed in the serial monitor
    // Send any characters typed at the Serial monitor to the bluetooth
    Serial1.print((char)Serial.read());
  }
}
