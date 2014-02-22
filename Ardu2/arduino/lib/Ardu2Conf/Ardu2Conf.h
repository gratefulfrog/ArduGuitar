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
#define INVERTER_FORWARD        (5)
#define INVERTER_INVERTED       (10)
#define INVERTER_OFF            (0)
#define VOL_0                   (0)  
#define VOL_1                   (1) 
#define VOL_2                   (2)
#define VOL_3                   (4)
#define VOL_4                   (8)
#define VOL_5                   (16)
#define TONE_0                  (0)  
#define TONE_1                  (1)
#define TONE_2                  (2) 
#define TONE_3                  (3)
#define TONE_4                  (4)
#define TONE_5                  (5)
#define TONE_6                  (6)
#define TONE_7                  (7)
#define TONE_8                  (8)
#define TONE_9                  (9)
#define TONE_10                 (10)
#define TONE_11                 (11)
#define TONE_12                 (12)
#define TONE_13                 (13)
#define TONE_14                 (14)
#define TONE_15                 (15)
#define COMBINATOR_SERIES       (2)
#define COMBINATOR_PARALLEL     (5)
#define COMBINATOR_A            (4)
#define COMBINATOR_B            (1)
#define SELECTOR_A              (5)
#define SELECTOR_B              (10)
#define SELECTOR_A_B            (15)
#define SELECTOR_NONE           (0)

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
