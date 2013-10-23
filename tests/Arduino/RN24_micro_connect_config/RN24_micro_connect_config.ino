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

///////////////////////////////////////////////////////////////////////////
///////////////////      RN42 Functions     ///////////////////////////////
///////////////////////////////////////////////////////////////////////////

boolean setupCommandMode(){
  // set command mode to the RN42, when it is not connected automatically
  // wait for confirmation and reply TRUE if confirmed, false otherwise
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
void doConnect(){
  Serial1.println("SR,Z");
  Serial1.println("R,1");
}
void clearRN42Output(){
  while (Serial1.available()){
    Serial1.read();  
  }
}
void setupRN42AndConnect(){
  // this version depends ont eh RN42 being in automatic reconnect mode (SM,3), 
  // which means that it will automatically reconnect to the last BT device that it
  // knew, if in range!
  // so, to get it to connect to a new device, you have to rease the previous
  // device from memory, and reboot, which will force a scan for RN devices
  // and connection, and storage of that new device in RN42 memory
  // the 10 second delay is needed for the BT device scan.
  // at the end, we clear any relics that the RN42 may have sent during the scan
  // and connect process.
  Serial1.begin(115200);
  while(!Serial1);
  while (!setupCommandMode());
  doConnect();
  delay(10000);  // this is needed in the case of a long inquiry!
  clearRN42Output();
}

///////////////////////////////////////////////////////////////////////////
///////////////////   Serial Monitor Functions     ////////////////////////
///////////////////////////////////////////////////////////////////////////

void setupSerial(){
  Serial.begin(115200);  // Begin the serial monitor at 115200bps
  while(!Serial);
}
///////////////////////////////////////////////////////////////////////////
///////////////////       Std Functions     ///////////////////////////////
///////////////////////////////////////////////////////////////////////////

void setup(){
  setupRN42AndConnect();
  setupSerial();
}

void loop() {
  // just an echo
  // just write to Serial1 from Serial Monitor input
  // and read from Serial1 and write it to Serial Monitor.
  if(Serial1.available()){  // If the bluetooth sent any characters
    // Send any characters from the bluetooth to the serial monitor
    Serial.print((char)Serial1.read());  
  }
  if(Serial.available()) {  // If stuff was typed in the serial monitor
    // Send any characters typed at the Serial monitor to the bluetooth
    Serial1.print((char)Serial.read());
  }
}
