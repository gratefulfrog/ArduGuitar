/*
 * an arduino sketch to interface with a ps/2 mouse.
 * Also uses serial protocol to talk back to the host
 * and report what it finds.
 */

/*
 * Pin 5 is the mouse data pin, pin 6 is the clock pin
 * Feel free to use whatever pins are convenient.
 */
 /* some slight modifs to make the status report more usefull.
  *  2015 09 30
  */
#define MDATA 5
#define MCLK 6

/*
 * according to some code I saw, these functions will
 * correctly set the mouse clock and data pins for
 * various conditions.
 */
void gohi(int pin)
{
  pinMode(pin, INPUT);
  digitalWrite(pin, HIGH);  // this turns on pull up resistor on the input pin
}

void golo(int pin)
{
  pinMode(pin, OUTPUT);
  digitalWrite(pin, LOW);
}


void mouse_write(char data)
{
  char i;
  char parity = 1;

  //  Serial.print("Sending ");
  //  Serial.print(data, HEX);
  //  Serial.print(" to mouse\n");
  //  Serial.print("RTS");
  /* put pins in output mode */
  gohi(MDATA);
  gohi(MCLK);
  delayMicroseconds(300);
  golo(MCLK);
  delayMicroseconds(300);
  golo(MDATA);
  delayMicroseconds(10);
  /* start bit */
  gohi(MCLK);
  /* wait for mouse to take control of clock); */
  while (digitalRead(MCLK) == HIGH)
    ;
  /* clock is low, and we are clear to send data */
  for (i=0; i < 8; i++) {
    if (data & 0x01) {
      gohi(MDATA);
    } 
    else {
      golo(MDATA);
    }
    /* wait for clock cycle */
    while (digitalRead(MCLK) == LOW)
      ;
    while (digitalRead(MCLK) == HIGH)
      ;
    parity = parity ^ (data & 0x01);
    data = data >> 1;
  }  
  /* parity */
  if (parity) {
    gohi(MDATA);
  } 
  else {
    golo(MDATA);
  }
  while (digitalRead(MCLK) == LOW)
    ;
  while (digitalRead(MCLK) == HIGH)
    ;
  /* stop bit */
  gohi(MDATA);
  delayMicroseconds(50);
  while (digitalRead(MCLK) == HIGH)
    ;
  /* wait for mouse to switch modes */
  while ((digitalRead(MCLK) == LOW) || (digitalRead(MDATA) == LOW))
    ;
  /* put a hold on the incoming data. */
  golo(MCLK);
  //  Serial.print("done.\n");
}

/*
 * Get a byte of data from the mouse
 */
char mouse_read(void)
{
  char data = 0x00;
  int i;
  char bit = 0x01;

  //  Serial.print("reading byte from mouse\n");
  /* start the clock */
  gohi(MCLK);
  gohi(MDATA);
  delayMicroseconds(50);
  while (digitalRead(MCLK) == HIGH)
    ;
  delayMicroseconds(5);  /* not sure why */
  while (digitalRead(MCLK) == LOW) /* eat start bit */
    ;
  for (i=0; i < 8; i++) {
    while (digitalRead(MCLK) == HIGH)
      ;
    if (digitalRead(MDATA) == HIGH) {
      data = data | bit;
    }
    while (digitalRead(MCLK) == LOW)
      ;
    bit = bit << 1;
  }
  /* eat parity bit, which we ignore */
  while (digitalRead(MCLK) == HIGH)
    ;
  while (digitalRead(MCLK) == LOW)
    ;
  /* eat stop bit */
  while (digitalRead(MCLK) == HIGH)
    ;
  while (digitalRead(MCLK) == LOW)
    ;

  /* put a hold on the incoming data. */
  golo(MCLK);
  //  Serial.print("Recvd data ");
  //  Serial.print(data, HEX);
  //  Serial.print(" from mouse\n");
  return data;
}

void mouse_init()
{
  gohi(MCLK);
  gohi(MDATA);
  Serial.println("Sending reset to mouse");
  mouse_write(0xff);
  Serial.println(byte(mouse_read()));  /* ack byte */
  //  Serial.print("Read ack byte1\n");
  //mouse_read();  
  Serial.println(byte(mouse_read()));
  Serial.println(byte(mouse_read()));
  //mouse_read();  /* blank */
  //mouse_read();  /* blank */
  Serial.println("Sending remote mode code");
  mouse_write(0xf0);  /* remote mode */
  Serial.println(byte(mouse_read()));
  //mouse_read();  /* ack */
  //  Serial.print("Read ack byte2\n");
  delayMicroseconds(100);
}

void setup()
{
  Serial.begin(9600);
  mouse_init();
}


void interpretStatByte(char stat){
  String statVec[] = {"Left",
                      "Right",
                      "Middle",
                      "None",
                      "-X",
                      "-Y",
                      "X Overflow",
                      "Y Overflow"};
    Serial.print("\t");
    for (int i = 0; i<8;i++){
      if(stat & (1<<i)){
        Serial.print(statVec[i]);
        i != 7 && Serial.print(", ");
      }
    }
    Serial.println();
}

/*
 * get a reading from the mouse and report it back to the
 * host via the serial line.
 */

char mstat='y', 
       lmstat = 'n';
  char mx ='0',
       lmx = '1';
  char my ='0',
       lmy = '1'; 
int maxX =0,
    maxY = 0;
/*
void loop(){}
*/
void loop(){
  // get a reading from the mouse 
  mouse_write(0xeb);  // give me data! 
  mouse_read();      // ignore ack 
  mstat = mouse_read();
  mx = mouse_read();
  my = mouse_read();

  if((mstat != lmstat) ||
     (mx !=lmx) ||
     (my != lmy)) {
      // send the data back up 
      //Serial.print(mstat, BIN);
      Serial.print("X=");
      Serial.print(mx, DEC);
      Serial.print("\tY=");
      Serial.print(my, DEC);
      //Serial.println();
      interpretStatByte(mstat);
      lmstat = mstat;
      lmx = mx;
      lmy = my;
      //maxX = max(mx,maxX);
      //maxY = max(my,maxY);
      //Serial.print("maxX: ");
      //Serial.print(maxX,DEC);
      //Serial.print("\tmaxY: ");
      //Serial.println(maxY,DEC);
     }
     
  delay(20);  // twiddle 
}

