/****
 * PS2tester.ino - Arduino PS/2 protocol tester
 *
 * (C) Copyright 2012 Joonas Pihlajamaa and others.
 *
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the GNU Lesser General Public License
 * (LGPL) version 2.1 which is available at
 * http://www.gnu.org/licenses/lgpl-2.1.html
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * Contributors:
 *     Joonas Pihlajamaa <jokkebk@codeandlife.com>
 *
 * Partly based on PS2keyboard version 2.4 by Christian Weichel, Paul
 * Stoffregen and others, see PS2keyboard source for all contributors:
 *
 * http://playground.arduino.cc/Main/PS2Keyboard OR
 * http://www.pjrc.com/teensy/td_libs_PS2Keyboard.html
 */

#include "Arduino.h"

// Device specific settings, configured for Arduino Uno
#define CLOCK_PIN_INT 1 // Pin 3 attached to INT1 in Uno

const int DataPin = 2; // Uno INT0
const int ClockPin =  3; // Uno INT1

#define BUFFER_SIZE 45

static volatile uint8_t buffer[BUFFER_SIZE];
static volatile uint8_t head, tail;
static volatile bool inhibiting;

// Open collector utility routines

static inline void holdClock() {
  digitalWrite(ClockPin, LOW); // pullup off
  pinMode(ClockPin, OUTPUT); // pull clock low
}

static inline void releaseClock() {
  pinMode(ClockPin, INPUT); // release line
  digitalWrite(ClockPin, HIGH); // pullup on
}

static inline void holdData() {
  digitalWrite(DataPin, LOW); // pullup off
  pinMode(DataPin, OUTPUT); // pull clock low
}

static inline void releaseData() {
  pinMode(DataPin, INPUT); // release line
  digitalWrite(DataPin, HIGH); // pullup on
}

// The ISR for the external interrupt in write mode
void ps2int_read() {
  static uint8_t bitcount=0, incoming=0;
  static uint32_t prev_ms=0;
  uint32_t now_ms;
  uint8_t n, val;

  if(inhibiting)
    return; // do nothing when clock manipulated by Arduino

  val = digitalRead(DataPin);
  now_ms = millis();
  if (now_ms - prev_ms > 250) {
    bitcount = 0;
    incoming = 0;
  }
  prev_ms = now_ms;
  n = bitcount - 1;
  if (n <= 7) {
    incoming |= (val << n);
  }
  bitcount++;
  if (bitcount == 11) {
    uint8_t i = head + 1;
    if (i >= BUFFER_SIZE) i = 0;
    if (i != tail) {
      buffer[i] = incoming;
      head = i;
    }
    bitcount = 0;
    incoming = 0;
  }
}

static volatile uint8_t writeByte;
static volatile uint8_t curbit = 0, parity = 0, ack;

// The ISR for the external interrupt in read mode
void ps2int_write() {
  if(curbit < 8) {
    if(writeByte & 1) {
      parity ^= 1;
      digitalWrite(DataPin, HIGH);
    } else
      digitalWrite(DataPin, LOW);

    writeByte >>= 1;
  } else if(curbit == 8) { // parity
    if(parity)
      digitalWrite(DataPin, LOW);
    else
      digitalWrite(DataPin, HIGH);
  } else if(curbit == 9) { // time to let go
    releaseData();
  } else { // time to check device ACK and hold clock again
    holdClock();
    ack = !digitalRead(DataPin);
  }

  curbit++;
}

// Check if data available in ring buffer
bool ps2Available() {
  return head != tail;
}

// Read a byte from ring buffer (or return \0 if empty)
static inline uint8_t ps2Read() {
  uint8_t c, i;

  i = tail;
  if (i == head) return 0;
  i++;
  if (i >= BUFFER_SIZE) i = 0;
  c = buffer[i];
  tail = i;
  return c;
}

// Prepare a byte for sending to PS/2 device
static inline void ps2Write(uint8_t byte) {
  writeByte = byte;
  curbit = parity = ack = 0;
}

// Utility function to convert hex into number
int fromHex(char ch) {
  if(ch >= '0' && ch <= '9')
    return ch - '0';
  else if(ch >= 'A' && ch <= 'F')
    return ch - 'A' + 10;
  else if(ch >= 'a' && ch <= 'f')
    return ch - 'a' + 10;

  return 0;
}

void setup() {
  // Initialize in listening mode
  releaseClock();
  releaseData();

  // Clear ring buffer
  head = tail = 0;

  // Start listening clock line
  attachInterrupt(CLOCK_PIN_INT, ps2int_read, FALLING);

  // Initialize serial
  Serial.begin(115200);
  Serial.println("PS/2 tester. Enter hex pairs to send:");
}



void loop() {
  // Inhibit communication
  inhibiting = true;
  holdClock();

  // Print data received from PS/2 device
  while(ps2Available()) {
    uint8_t byte = ps2Read(); // read the next key
    Serial.println(byte, HEX);
  }

  if (Serial.available() > 1) { // user input over serial line
    int incomingByte = (fromHex(Serial.read()) << 4) + fromHex(Serial.read());

    if(incomingByte < 0x10)
      Serial.print("> 0"); // pad a zero
    else   
      Serial.print("> ");

    Serial.println(incomingByte, HEX); // echo back byte sent
    ps2Write(incomingByte); // send byte to PS/2 device

    attachInterrupt(CLOCK_PIN_INT, ps2int_write, FALLING);

    holdData();
    releaseClock();

    while(curbit < 11) {} // wait until receive complete - MAY HANG!

    // now clock line is held low again and data line is released

    Serial.println(ack ? "*ACK*" : "no ACK"); 

    attachInterrupt(CLOCK_PIN_INT, ps2int_read, FALLING);
  }

  // Stop inhibiting comms
  releaseClock();
  inhibiting = false;

  delay(5);//00); //5); // give some time for device to send more
}


