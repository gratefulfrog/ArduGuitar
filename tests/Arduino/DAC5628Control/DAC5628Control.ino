/*
  DAC  Control
  
  This example controls an TLC 5628 8 channel DAC
 
 The DAC is SPI-compatible,and to command it, you send two bytes, 
 * one with the channel number mutliplied by 2, plus a Range extender bit:
   if RNG bit == then the Max outut voltage is doubled
 * one byte with a level value [0..255]

The output Voltage = Vref * (leve/256) * (1 + Range)

VDD is the supply voltage (5V in our case)

Note that the following must be true: Vref  <= VDD - 1.5V

The circuit:
  * DAC pin   - Arduino Pin
  * 3 (gnd)   - gnd
  * 4 (DATA)  - 11 (MOSI)
  * 5 (CLK)   - 13 (SCK serial clock)
  * 6 (VDD)   - +5V
  * 11 (REF2) - +1V (from voltage divider)
  * 14 (REF1) - +1V
  * 12 (LOAD) - 10 select pin, LOW means do nothing, HIGH means read DATA, then LOW loads data read.
  * 13 (LDAC) - gnd (unused in my application)
*/


// inslude the SPI library:
#include <SPI.h>

#define DAC dACh

// set pin 10 as the slave select for the digital pot:
const int loadPin = 10;

const int dACa = 0,
          dACb = 2,
          dACc = 4,
          dACd = 6,
          dACe = 8,
          dACf = 10,
          dACg = 12,
          dACh = 14,
          dRNG = 1;



void setup() {
  // set the slaveSelectPin as an output:
  pinMode (loadPin, OUTPUT);
  // initialize SPI:
  SPI.begin(); 
  SPI.setBitOrder(MSBFIRST);  // Most Significant bit first.
  SPI.setClockDivider(SPI_CLOCK_DIV16);  //16MHz divided by 16 = 1MHz
  SPI.setDataMode(SPI_MODE1);  // zero based clock, data on falling edge, seems like the correct setting
  digitalWrite(loadPin,LOW);
  zeroDACs();
  delay(5000);
  //dACWrite(DAC,255);
  //  delay(5000);
}

void zeroDACs(){
  for (int i=0;i< dACh+1; i+=2){
    dACWrite(i,0);
  }
}

void loop() {
  
  //change the Anaolg Voltage on this channel from min to max, in steps of 1/5
  for (int level = 0; level < 256; level+=51) {
    dACWrite(DAC, level);
    delay(2500);
  }
  // wait a second at the top:
  delay(5000);
  // change the analog voltage on this channel from max to min:
  for (int level = 0; level < 256; level+=51) {
    dACWrite(DAC, 255 - level);
    delay(2500);
  }
  
}

void dACWrite(int channel, int level) {
  // take the SS pin low to select the chip:
  digitalWrite(loadPin,HIGH);
  //  send in the address and value via SPI:
  SPI.transfer(channel);
  SPI.transfer(level);
  // take the SS pin high to de-select the chip:
  digitalWrite(loadPin,LOW);
}

