// -*- c++ -*-
// Ardu2Conf.h

#ifndef ARDU2CONF_H
#define ARDU2CONF_H

#include <Arduino.h>

#define ON  (1)
#define OFF (0)

// Switch IDs :
#define INVERTER_NECK_NORTH     (0)
#define INVERTER_NECK_SOUTH     (1)
#define INVERTER_BRIDGE_NORTH   (2)
#define INVERTER_BRIDGE_SOUTH   (3)
#define VOL_NECK_NORTH          (4)
#define VOL_NECK_SOUTH          (5)
#define VOL_BRIDGE_NORTH        (6)
#define VOL_BRDIGE_SOUTH        (7)
#define TONE_NECK_NORTH         (8)
#define TONE_NECK_SOUTH         (9)
#define TONE_BRIDGE_NORTH       (10)
#define TONE_BRDIGE_SOUTH       (11)
#define COMBINTAOR_NECK         (12)
#define COMBINTAOR_BRIDGE       (13)
#define COMBINTAOR_NECK_BRIDGE  (14)
#define COMBINTAOR_BRIDGE_NECK  (15)
#define SELECTOR                (16)
#define MASTER_VOL              (17)
#define MASTER_TONE             (18)

// Switch Control Values
#define INVERTER_FORWARD        (5)  //   0101
#define INVERTER_INVERTED       (10) //   1010
#define INVERTER_OFF            (0)  //   0000
#define VOL_0                   (1)  // 000001
#define VOL_1                   (2)  // 000010
#define VOL_2                   (4)  // 000100
#define VOL_3                   (8)  // 001000
#define VOL_4                   (16) // 010000
#define VOL_5                   (32) // 100000
#define TONE_0                  (0)  //   0000  
#define TONE_1                  (1)  //   0001
#define TONE_2                  (2)  //   0010
#define TONE_3                  (3)  //   0011
#define TONE_4                  (4)  //   0100
#define TONE_5                  (5)  //   0101
#define TONE_6                  (6)  //   0110
#define TONE_7                  (7)  //   0111
#define TONE_8                  (8)  //   1000
#define TONE_9                  (9)  //   1001
#define TONE_10                 (10) //   1010
#define TONE_11                 (11) //   1011
#define TONE_12                 (12) //   1100
#define TONE_13                 (13) //   1101
#define TONE_14                 (14) //   1110
#define TONE_15                 (15) //   1111
#define COMBINATOR_SERIES       (2)  //    010
#define COMBINATOR_PARALLEL     (5)  //    101
#define COMBINATOR_A            (4)  //    100
#define COMBINATOR_B            (1)  //    001
#define SELECTOR_A              (5)  //   0101
#define SELECTOR_B              (10) //   1010
#define SELECTOR_A_B            (15) //   1111
#define SELECTOR_NONE           (0)  //   0000

// PINS
#define LATCH_PIN (13)

// Shift Registers 
#define NB_SHIFT_REGS (11)

class Ardu2Conf {
 public:

  static const byte startIndex[];
  static byte curVec[], 
    onVec[],
    offVec[];
  static void resetVecs(boolean all=false);
  static void init();  // initialize static variables
};
		     
#endif
