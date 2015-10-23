#include <ps2.h>

/*
 * an arduino sketch to interface with a ps/2 mouse.
 * Also uses serial protocol to talk back to the host
 * and report what it finds.
 * Heavily modified by gratefulfrog October 2015
 * Timing shows that 1150 µseconds are needed to read/write a byte
 * of data, i.e. 1150/11 bits = +/- 100 µsecond per bit which is
 * indeed the PS/2 clock period.
 */

#define CLOCK (5)
#define DATA (6)
    
PS2 mouse(CLOCK, DATA);

/*
 * initialize the mouse. Reset it, and place it into remote
 * mode, so we can get the encoder data on demand.
 */
void mouse_init(){
  int r1,r2,r3;
  mouse.write(0xff);  // reset
  r1= mouse.read();  // ack byte
  r2= mouse.read();  // blank */
  r3 =mouse.read();  // blank */
  Serial.print(r1,HEX);
  Serial.print('\t');
  Serial.print(r2,HEX);
  Serial.print('\t');
  Serial.println(r3,HEX);
  mouse.write(0xf0);  // remote mode
  r3=mouse.read();  // ack
  Serial.println(r3,HEX);
  delayMicroseconds(100);
}

void setup(){
  Serial.begin(9600);
  mouse_init();
}

String interpretStatByte(char stat){
    const static String statVec[] = {"Left",
				     "Right",
				     "Middle",
				     "None",
				     "-X",
				     "-Y",
				     "X Overflow",
				     "Y Overflow"};
    String res  = "\t";
    for (int i = 0; i<8;i++){
	if(stat & (1<<i)){
	    res =  res + statVec[i];
	    if (i <7){
		res  = res + ", ";
	    }
	}
    }
    return res;
}


/*
 * get a reading from the mouse and report it back to the
 * host via the serial line.
 */

char mstat='y', 
  lmstat = 'n',
  mx ='0',
  lmx = '1',
  my ='0',
  lmy = '1'; 

long uSecs = 0;

void loop(){
  uSecs = micros();
  /* get a reading from the mouse */
  mouse.write(0xeb);  // give me data!
  mouse.read();      // ignore ack
  mstat = mouse.read();
  mx = mouse.read();
  my = mouse.read();
  uSecs =  micros() - uSecs;

  if((mstat != lmstat) ||
     (mx !=lmx) ||
     (my != lmy)) {
      // send the data back up 
      //Serial.print(mstat, BIN);
      Serial.print("X=");
      Serial.print(mx, DEC);
      Serial.print("\tY=");
      Serial.print(my, DEC);
      Serial.print(interpretStatByte(mstat));
      Serial.print("\tmicroseconds per byte: ");
      Serial.println(uSecs/5.0);
      lmstat = mstat;
      lmx = mx;
      lmy = my;
  }
  delay(20);  /* twiddle */
}
