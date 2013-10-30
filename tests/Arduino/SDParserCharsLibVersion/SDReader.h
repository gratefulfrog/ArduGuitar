/* SD Reader library for ArduStomp
 * SD reader select pin MUST BE PIN 10 !!!
 */

/*  This version parses the data and cycle files to create:
 * an array of 4 unsigned ints as presets
 * an array of 4 chars, which are the last letters of the name of the preset,indexed on the line number
 * the layout of the preset is on 12 bits:
 * vol:4 
 * tone:4 
 * neck:1
 * middle:1
 * bridgeN:1
 * bridgeB:1
 * wasting a total of 4x4 = 16 bits... dommage
 * Correct results for the test data.tsv:
name	vol	tone	neck	middle	bNorth	bBoth <- read but ignored
Rock	6	11	0	1	0	1
Woman	10	4	1	0	0	1
Jazz	11	1	1	0	0	0
Comp	8	11	0	1	0	1
Auto	0	0	0	0	0	0   <- not read
 1717
 2633
 2840
 2229
 k 
 n
 z
 p
cycle.tsv
name	msWait <- read but ignored
Rock	1500
Woman	1500
Jazz	1500
Comp	1500

 * the struct autoStruct is a circular linked list of unsigned ints which encode
 i:2 the index of the presset in the mapp
 i:14  the delay in milliseconds must be less than or equal to 2^14 -1 = 16383

output cycling:
9: 1500
8: 17884
7: 34268
6: 50652
5: 1500
4: 17884
3: 34268
2: 50652
1: 1500
0: 17884
Done.
 */


 
#ifndef SDREADER_H
#define SDREADER_H

#include <Arduino.h>
#include <SD.h>

// the SD card select pin is required by the SD lib...
#define SDPIN (10)

#define NB_PRESETS (4)

// defines used in protected calls
#define P_VOL_SHIFT  (8)
#define P_TONE_SHIFT (4)
#define P_NECK_SHIFT (3)
#define P_MID_SHIFT  (2)
#define P_BN_SHIFT   (1)
#define P_BB_SHIFT   (0)

#define P_VT  (0B1111)
#define P_PUP (1)

#define MAX_AUTO_PAUSE   (16383)
#define A_PAUSE (0B11111111111111)
#define A_SHIFT (14)
#define A_INDEX (0B11)

class SDReader {
  protected:
    File f;
    void skipHeaderLine();
    static boolean sdBegun;
  
  public:
    SDReader(char *FileName,boolean sdBegun = false);
    boolean openFile(); // returns false if failed
    virtual boolean parse() = 0; // returns false if failed
};

class PresetClass: public SDReader {
  protected:
    unsigned int presets[NB_PRESETS];
    char mapp[NB_PRESETS];
    byte preVal(unsigned int i, 
                unsigned int mask, 
                int shift) const;
  public:
    // use these keys to get values back
    const static byte volKey         = 0,
                      toneKey        = 1,
                      neckKey        = 2,
                      middleKey      = 3,
                      bridgeNorthKey = 4,
                      bridgeBothKey  = 5;
                      
    PresetClass(char *presetsFileName);
    byte presetValue(byte presetIndex, byte key) const;
    boolean parse();
    byte firstLetter2Index(char c) const;
};

// Auto Class stuff

struct autoStruct{
  unsigned int i;
  struct autoStruct *next;
};


class AutoClass: public SDReader {
  protected:
    struct autoStruct firstAuto;
    struct autoStruct *current;
    long lastAutoTime;
    boolean _running;
    const PresetClass *p;
 
    byte presetIndex();
    int getNextNumber();
    byte currentIndex() const;
    int currentPause() const;

  public:
    AutoClass(char *autoFileName, const PresetClass *p);
    boolean parse();
    boolean running() const;
    void start(boolean yes);
    //int inc();
    byte check();  // returns the index of the preset that is current
};

#endif
