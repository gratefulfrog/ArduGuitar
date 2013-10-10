/*
 Update from Sparkfun example
 for Arduino Micro with Serial and Serial1

 */

// ardustomp-01   MAC: 0006664E4BD3
// arduguitar-02  MAC: 0006666434C3

String commandModeConfirmationString = "CMD",
       arduguitar02MACAddress = "0006666434C3",
       endOfInquiry = "Done";

void ss(String s){
  Serial.println(s);
}

void setupSerial(){
  delay(5000);   // to allow for time to turn on the Serial Monitor
  Serial.begin(9600);  // Begin the serial monitor at 9600bps
  while(!Serial);
}
  

void setup(){
  setupSerial();
  Serial1.begin(115200);  // The Bluetooth Mate defaults to 115200bps
  while(!Serial1);
  ss("Serial Ports ready, pausing for 1s before going to command mode");
  delay(1000);
 
  while (!setupCommandMode()){
    ss("failed...");
    delay(100);
  }
  
  ss("...pausing for 1s before querying for the selected MAC address");
  delay(1000);
  
  /*
  while(!queryForBluetoothDevice(arduguitar02MACAddress)){
    ss("failed...");
    delay(100);
  }
  */
  ss("...pausing for 1s before trying to connect  the selected MAC address");
  delay(1000);

  while(!connectBluetoothDevice(arduguitar02MACAddress)){
    ss("failed...");
    delay(100);
  }
  ss("...pausing for 1s before checking connection status...");
  delay(1000);
  
  boolean connected = connectOK();
  ss("Connection Status: " + String(connected));
  
  if (connected){
    ss("Exiting setup, thinking we're connected!");
  }
  else {
    ss("Exiting setup, thinking we're NOT connected!");
  }
}

boolean connectOK(){
  while (!setupCommandMode()){
    delay(100);
  }
  String rn42Output = "";
  delay(500);
  
  Serial1.println("GK");
  delay(1000);
  long startTime = millis(),
       timeOut = 5000;
  boolean something = false;
  while(Serial1.available() || !something){
      rn42Output += (char)Serial1.read();  
      something = rn42Output.indexOf('1')>-1 || rn42Output.indexOf('0')>-1;
      delay(100);
      if (millis() - startTime > timeOut){
        break;
      }
  }
  ss("GK command returned: " + rn42Output +"!");
  Serial1.println("---");
  return rn42Output.indexOf('1')>-1;
}
  
boolean connectBluetoothDevice(String btAddress){
  ss("Connecting to: " + btAddress +"...");
  
  String rn42Output = "";
  boolean ret = false;
  
  Serial1.println("C," + btAddress);  // connect to it!
 
  long startTime = millis(),
       connectTimeOut = 1500;
  
  //delay(2000);  // Long delay during search
  
  while(millis()-startTime < connectTimeOut){
    while(Serial1.available()){
      rn42Output += (char)Serial1.read();  
    }
    delay(100);
  }
  ss("Connection request Returned:\n" + rn42Output);
  if (rn42Output.indexOf("ERR" ) <0 && rn42Output.indexOf("failed" ) <0){
    ss("never got a 'ERR' or 'failed'... so connection is ok?");
    ret = true;
  }
  else {
    ss("GOT a error... means failure...");
  }
  return ret;
}

boolean queryForBluetoothDevice(String btAddress){
  ss("Inquiring for BT devices...");
  
  String rn42Output = "";

  Serial1.println("I");  // search for all BT Devices
  delay(5000);  // Long delay during search
  while((rn42Output.indexOf(endOfInquiry) <0)){
    while(Serial1.available()){
      rn42Output += (char)Serial1.read();  
    }
    delay(1000);
  }
  ss("Inquiry Returned:\n" + rn42Output);
  
  boolean ret = rn42Output.indexOf(btAddress) > -1;
  
  if (ret){
    ss("Device at: " + btAddress + " was found!");
  }
  else  {
    ss("Device at: " + btAddress + " was NOT found!");
  }
  return ret;
}

boolean setupCommandMode(){
  ss("Setting command mode...");
  
  String rn42Output = "";
  Serial1.print("$");  // Print three times individually
  Serial1.print("$");
  Serial1.print("$");  // Enter command mode
  delay(500);  // Short delay, wait for the Mate to send back CMD
  while(Serial1.available()){
    rn42Output += (char)Serial1.read();  
  }
  ss(rn42Output);
  boolean ret = rn42Output.indexOf(commandModeConfirmationString)>-1;
  if(ret){
    ss("Command mode ok!");
  }
  else {
    ss("Command mode NOT ok!");
  }
  return ret;
}

void loop(){
  /*
  if(bluetooth.available())  // If the bluetooth sent any characters
  {
    // Send any characters the bluetooth prints to the serial monitor
    Serial.print((char)bluetooth.read());  
  }
  if(Serial.available())  // If stuff was typed in the serial monitor
  {
    // Send any characters the Serial monitor prints to the bluetooth
    bluetooth.print((char)Serial.read());
  }
  // and loop forever and ever!
  */
}
