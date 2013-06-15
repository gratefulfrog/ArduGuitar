// Pickup Cylce tester

/* This code will loop over a sequence of pups and delays:
 *  1. select the next pup
 *  2. delay the next delay
 *  3. select the next pup.
 *  ...
 * when it reaches the end of the sequence, it starts over.
 */

// the sequence should be of form:
// (pn+)+  
// where p is a pup indicator:
//   N : neck
//   M : middle
//   S : split bridge
//   B : both bridge
// and n+ is s series of digits which will be converted into milliseconds
//     delay before selecting the next pup.
//////////////////////////////////////////////////////////////////////////
/////                 The PUP SEQUENCE                 ///////////////////

const String seq = "N100B100";

/////                 end PUP SEQUENCE                 ///////////////////
//////////////////////////////////////////////////////////////////////////

const int seqL = seq.length();

// if no pup given, then select the following one
const char defaultPup = 'N';

// used to iterate over the seq
int seqPtr = 0;

// used to accumulate the delay characters for conversion to int
String curDelay = "";

const char maxVolString1[]   = "09255",
           maxVolString2[]   = "10000",
           maxVolString3[]   = "12255",
           maxToneString[]   = "11000";

// O is on, 1 is off
const char  neck[][6]   = {"02255", "02000" },   // 0
            middle[][6] = {"03255", "03000" },   // 1
            split[][6]  = {"05255", "05000" },   // 2
            bridge[][6] = {"04255", "04000" } ;  // 3

char curPup = 'N';


void output(String s){
  //Serial.println(s);
}


void cycleSetup() {
  maxVol();
  maxTone();
  doPup('N');
}

void assignBuf(const char* s){
  for (int i=0;i<5;i++){
    incomingBuffer[i] = s[i];
  }
}

void maxVol(){
  doString(maxVolString1);
  doString(maxVolString2);
  doString(maxVolString3);
}

void maxTone(){
  doString(maxToneString);
}

void doString(const char* c){
  assignBuf(c);
  executeIncomingString();
}

void doPup(char p){
  String txt = "Setting pup: ";
  txt += p;
  output(txt);
  
  switch (p) {
   case 'N':
   case 'n':
    // turn on NECK, off all others
    doString(neck[0]);
    doString(middle[1]);
    doString(split[1]);
    doString(bridge[1]);
   break;
   case 'M':
   case 'm':
    // turn on MIDDLE, off all others
    doString(middle[0]);
    doString(neck[1]);
    doString(split[1]);
    doString(bridge[1]);
   break;
   case 'S':
   case 's':
    // turn on SPLIT and BRIDGE, off all others
    doString(split[0]);
    doString(bridge[0]);
    doString(neck[1]);
    doString(middle[1]);
   break;
   case 'B':
   case 'b':
    // turn on BRIDGE, off all others
    doString(bridge[0]);
    doString(neck[1]);
    doString(middle[1]);
    doString(split[1]);
   break;
  }
}  


// do the delay, as String
void doDelay(String d) {
  int iDelay = d.toInt();
  String txt = "Delaying ";
  txt += iDelay;
  txt += " ms.";
  output(txt);
  delay(iDelay);
}


// return true if character arg is a digit
boolean isDigit(char c) {
  return (c>= '0' && c <= '9');
}

/*
void setup() { 
  //Initialize serial and wait for port to open:
  Serial.begin(9600); 
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }
  // set the default pup
  doPup(defaultPup);
  output("Initialized!"); 
}
*/

void loop(){
  // get next char in seq
  char cc = seq[seqPtr];
  // if it's a digit, concat it to the current delay string
  if (isDigit(cc)){
    curDelay += cc;
  }
  // if not it must be a pup indicator
  else {
    // so we've read a full delay, and must delay
    doDelay(curDelay);
    // reset current delay to empty
    curDelay = "";
    // set the current pup
    doPup(cc);
  }
  // increment the seq pointer, modulo length of the seq
  seqPtr = (seqPtr+1) % seqL;
  // and loop!
}
