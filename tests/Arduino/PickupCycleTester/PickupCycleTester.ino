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
const String seq = "N100M200B300";
const int seqL = seq.length();

// if no pup given, then select the following one
const char defaultPup = 'N';

// used to iterate over the seq
int seqPtr = 0;

// used to accumulate the delay characters for conversion to int
String curDelay = "";

// select the pup
void doPup(char p) {
  String msg = "Set Pup: ";
  msg += p;
  output(msg);
}

// do the delay, as String
void doDelay(String d) {
  int iDelay = d.toInt();
  String msg = "Delaying ";
  msg += iDelay;
  msg += " ms.";
  output(msg);
  delay (1000);
}


// return true if character arg is a digit
boolean isDigit(char c) {
  return (c>= '0' && c <= '9');
}

// send a msg to serial port
void output(String s){
  Serial.println(s);
}

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
