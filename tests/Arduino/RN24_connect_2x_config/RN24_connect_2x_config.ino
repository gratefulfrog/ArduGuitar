/*
  Example Bluetooth Serial Passthrough Sketch
 by: Jim Lindblom
 SparkFun Electronics
 date: February 26, 2013
 license: Public domain

 This example sketch converts an RN-42 bluetooth module to
 communicate at 9600 bps (from 115200), and passes any serial
 data between Serial Monitor and bluetooth module.
 */
#include <SoftwareSerial.h>  

int bluetoothStompTx = 2;  // TX-O pin of bluetooth mate, Arduino D2
int bluetoothStompRx = 3;  // RX-I pin of bluetooth mate, Arduino D3

int bluetoothArduGuitarTx = 8;  // TX-O pin of bluetooth mate, Arduino D2
int bluetoothArduGuitarRx = 9;  // RX-I pin of bluetooth mate, Arduino D3


SoftwareSerial stomp(bluetoothStompTx, bluetoothStompRx);  //  MAC:  0006664E4BD3
SoftwareSerial arduGuitar(bluetoothArduGuitarTx, bluetoothArduGuitarRx);  // MAC: 0006666434C3


void setup()
{
  Serial.begin(9600);  // Begin the serial monitor at 9600bps
  Serial.println("starting...");
  //delay(5000);
  Serial.println("configuring stomp");
  stomp.begin(115200);  // The Bluetooth Mate defaults to 115200bps
  delay(1000);
  stomp.print("$");  // Print three times individually
  stomp.print("$");
  stomp.print("$");  // Enter command mode
  delay(1000);  // Short delay, wait for the Mate to send back CMD
  stomp.println("U,9600,N");  // Temporarily Change the baudrate to 9600, no parity

  // 115200 can be too fast at times for NewSoftSerial to relay the data reliably
  stomp.begin(9600);  // Start bluetooth serial at 9600
  stomp.println("---");
  Serial.println("Stomp configured, waiting 1s");
  delay(1000);
  
  
  Serial.println("configuring arduguitar");
  arduGuitar.begin(115200);
  ///delay(1000);
  arduGuitar.print("$");  // Print three times individually
  arduGuitar.print("$");
  arduGuitar.print("$");  // Enter command mode
  delay(1000);  // Short delay, wait for the Mate to send back CMD
  arduGuitar.println("U,9600,N");  // Temporarily Change the baudrate to 9600, no parity
  arduGuitar.begin(9600);  // Start bluetooth serial at 9600
  delay(1000);
  arduGuitar.println("---");  // Temporarily Change the baudrate to 9600, no parity
  Serial.println("ArduGuitar configured, waiting 5s");
  delay(5000);
  
  Serial.println("connecting stomp to arduguitar");
  Serial.println("setting stomp to command mode");
  stomp.print("$");  // Print three times individually
  delay(100);
  stomp.print("$");
  delay(100);
  stomp.print("$");  // Enter command mode
  
  delay(1000);
  Serial.println("stomp in command mode?, sending connect string");
  stomp.println("C,0006666434C3");
  delay(1000);
  Serial.println("looping to nowhere, in 5s");
  delay(5000);
  
  
}

boolean onlyOnce = false;

void loop(){
  if (!onlyOnce){
    stomp.print("X");
    onlyOnce = true;
  }
  /*
  if(stomp.available()) { // If the bluetooth sent any characters
  // Send any characters the stomp  prints to the serial monitor
      Serial.print((char)stomp.read());  
  } 
  */
  if(arduGuitar.available()) { // If the bluetooth sent any characters
    // Send any characters the stomp  prints to the serial monitor
    Serial.println((char)arduGuitar.read());  
  }
  /*
  if(Serial.available()) { // If stuff was typed in the serial monitor
    // Send any characters the Serial monitor prints to the bluetooth
    arduGuitar.print((char)Serial.read());
  }
  */
}

