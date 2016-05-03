// HMI mockup

final int widthReal =  300,  // milimeters
          heightReal = 220;

void settings(){
  size(round(widthReal*Positionable.scaleFactor),round(heightReal*Positionable.scaleFactor));
}

LedCross[] lcVect = new LedCross[5];

LedDisplay ld;
LCD lcd;
PushButton[] pb = new PushButton[2];
LedPB[] lpbs = new LedPB[4];

void doLeds(){
  ld = new LedDisplay(70,40);
  for (int i = 0; i<5; i++){
    ld.setV(i,i+3); 
    ld.setT(i,i+2); 
  }
  ld.TR.set(7);
  ld.display();
}

void doLCD(){
  LCD lcd = new LCD(140,0);
  lcd.setLn(1,"^");
  lcd.display();
}

void setup(){
  doLeds();
  doLCD();
  for (int i=0;i<2;i++){
    Actuator b = new Actuator();
    pb[i] = new PushButton(167 + i*14,30, b);
    pb[i].display();
  }
  int ind = 0;
  int[] colInd = {4,5,2,1};
  for (int i=0;i<2;i++){
    for (int j = 0;j<2;j++){
    lpbs[ind] = new LedPB(140+j*LedPB.hSpacing, 51+i*LedPB.vSpacing, LEDColors[colInd[ind]]);
    lpbs[ind].display();
    ind++;
    }
  }
   
}

void draw(){
  pb[0].display();
  pb[1].display();
  for (int i =0;i<4;i++){
    lpbs[i].display();
  }
}