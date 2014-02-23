// -*- c++ -*-
// Ardu2Conf.h

#ifndef ARDU2CONF_H
#define ARDU2CONF_H

#include <Arduino.h>

#define ON  (1)
#define OFF (0)

// individual switch IDs:
#define INVERTER_NECK_NORTH_0     (0)
#define INVERTER_NECK_NORTH_1     (1)
#define INVERTER_NECK_NORTH_2     (2)
#define INVERTER_NECK_NORTH_3     (3)
#define INVERTER_NECK_SOUTH_0     (4)
#define INVERTER_NECK_SOUTH_1     (5)
#define INVERTER_NECK_SOUTH_2     (6)
#define INVERTER_NECK_SOUTH_3     (7)
#define INVERTER_BRIDGE_NORTH_0   (8)
#define INVERTER_BRIDGE_NORTH_1   (9)
#define INVERTER_BRIDGE_NORTH_2   (10)
#define INVERTER_BRIDGE_NORTH_3   (11)
#define INVERTER_BRIDGE_SOUTH_0   (12)
#define INVERTER_BRIDGE_SOUTH_1   (13)
#define INVERTER_BRIDGE_SOUTH_2   (14)
#define INVERTER_BRIDGE_SOUTH_3   (15)

#define VOL_NECK_NORTH_0          (16)
#define VOL_NECK_NORTH_1          (17)
#define VOL_NECK_NORTH_2          (18)
#define VOL_NECK_NORTH_3          (19)
#define VOL_NECK_NORTH_4          (20)
#define VOL_NECK_NORTH_5          (21)
#define VOL_NECK_SOUTH_0          (22)
#define VOL_NECK_SOUTH_1          (23)
#define VOL_NECK_SOUTH_2          (24)
#define VOL_NECK_SOUTH_3          (25)
#define VOL_NECK_SOUTH_4          (26)
#define VOL_NECK_SOUTH_5          (27)
#define VOL_BRIDGE_NORTH_0        (28)
#define VOL_BRIDGE_NORTH_1        (29)
#define VOL_BRIDGE_NORTH_2        (30)
#define VOL_BRIDGE_NORTH_3        (31)
#define VOL_BRIDGE_NORTH_4        (32)
#define VOL_BRIDGE_NORTH_5        (33)
#define VOL_BRIDGE_SOUTH_0        (34)
#define VOL_BRIDGE_SOUTH_1        (35)
#define VOL_BRIDGE_SOUTH_2        (36)
#define VOL_BRIDGE_SOUTH_3        (37)
#define VOL_BRIDGE_SOUTH_4        (38)
#define VOL_BRIDGE_SOUTH_5        (39)

#define TONE_NECK_NORTH_0         (40)
#define TONE_NECK_NORTH_1         (41)
#define TONE_NECK_NORTH_2         (42)
#define TONE_NECK_NORTH_3         (43)
#define TONE_NECK_SOUTH_0         (44)
#define TONE_NECK_SOUTH_1         (45)
#define TONE_NECK_SOUTH_2         (46)
#define TONE_NECK_SOUTH_3         (47)
#define TONE_BRIDGE_NORTH_0       (48)
#define TONE_BRIDGE_NORTH_1       (49)
#define TONE_BRIDGE_NORTH_2       (50)
#define TONE_BRIDGE_NORTH_3       (51)
#define TONE_BRIDGE_SOUTH_0       (52)
#define TONE_BRIDGE_SOUTH_1       (53)
#define TONE_BRIDGE_SOUTH_2       (54)
#define TONE_BRIDGE_SOUTH_3       (55)

#define COMBINTAOR_NECK_0         (56)
#define COMBINTAOR_NECK_1         (57)
#define COMBINTAOR_NECK_2         (58)
#define COMBINTAOR_BRIDGE_0       (59)
#define COMBINTAOR_BRIDGE_1       (60)
#define COMBINTAOR_BRIDGE_2       (61)

#define COMBINTAOR_NECK_BRIDGE_0  (62)
#define COMBINTAOR_NECK_BRIDGE_1  (63)
#define COMBINTAOR_NECK_BRIDGE_2  (64)
#define COMBINTAOR_BRIDGE_NECK_0  (65)
#define COMBINTAOR_BRIDGE_NECK_1  (66)
#define COMBINTAOR_BRIDGE_NECK_2  (67)

#define SELECTOR_0                (68)
#define SELECTOR_1                (69)
#define SELECTOR_2                (70)
#define SELECTOR_3                (71)

#define MASTER_VOL_0              (72)
#define MASTER_VOL_1              (73)
#define MASTER_VOL_2              (74)
#define MASTER_VOL_3              (75)
#define MASTER_VOL_4              (76)
#define MASTER_VOL_5              (77)

#define MASTER_TONE_0             (78)
#define MASTER_TONE_1             (79)
#define MASTER_TONE_2             (80)
#define MASTER_TONE_3             (81)

// Component IDs :
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
