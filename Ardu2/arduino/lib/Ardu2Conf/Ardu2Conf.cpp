// -*- c++ -*-
// remove the next when in Arduino Envt.
#define RUNTESTS

#include <Ardu2Conf.h>

const byte Ardu2Conf::startIndex[] = {0, // inverter Neck North
				      4, // inverter Neck South
				      8, // inverter Bridge North
				      12, // inverter Bridge South
				      16, // vol Neck North
				      22, // vol Neck South
				      28, // vol Bridge North
				      34, // vol Brdige South
				      40, // tone Neck North
				      44, // tone Neck South
				      48, // tone Bridge North
				      52, // tone Brdige South
				      56, // combintaor Neck
				      59, // combintaor Bridge
				      62, // combintaor Neck-Bridge
				      65, // combintaor Bridge-Neck
				      68, // selector
				      72, // master vol
				      78, // master tone
				      82  // empty space
};

byte Ardu2Conf::curVec[NB_SHIFT_REGS],
  Ardu2Conf::onVec[NB_SHIFT_REGS],
  Ardu2Conf::offVec[NB_SHIFT_REGS];

void Ardu2Conf::resetVecs(boolean all){  // initialize static variables
  for (byte i=0;i<NB_SHIFT_REGS;i++){
    if (all){
      Ardu2Conf::curVec[i] = 0;
    }
    Ardu2Conf::onVec[i] = 0;
    Ardu2Conf::offVec[i] = 255;
  }
}

void Ardu2Conf::init(){  // initialize static variables
  Ardu2Conf::resetVecs(true);
}

		     

