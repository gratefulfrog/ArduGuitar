// radios

import controlP5.*;

RadioButton r,s;

int pickupActivationMap[] ={5, 11, 7, 13, 9, 2, 17},
    splitActivationMap[] = {0,1};

boolean initSelectors(ControlP5 cp5){
  r = cp5.addRadioButton("pickupSelector")
         .setPosition(20,130)
         .setSize(120,25)
         .setColorForeground(itemForegroundColor)
         .setColorActive(itemActiveColor)
         .setColorLabel(labelColor)
         .setItemsPerRow(5)
         .setSpacingColumn(-55)
         .setSpacingRow(5)    
         .addItem("null1",-1)
         .addItem("null2",-1)
         .addItem("Neck Bridge",5)
         .addItem("null4",-1)
         .addItem("null5",-1)
         .addItem("Neck",0)
         .addItem("null7",-1)
         .addItem("Middle",2)
         .addItem("null9",-1)
         .addItem("Bridge",4)
         .addItem("null11",-1)
         .addItem("Neck Middle",1)
         .addItem("null13",-1)
         .addItem("Middle Bridge",3)
         .addItem("null15",-1)
         .addItem("null16",-1)
         .addItem("null17",-1)
         .addItem("Neck Middle Bridge",6)
         .addItem("null19",-1)
         .addItem("null20",-1)
         ;
  r.activate(5);      

  for(Toggle t:r.getItems()) {
    if(t.captionLabel().getText().charAt(1) == 'u'){
      t.setVisible(false);
      t.setSize(0,0);
    }
    t.captionLabel().align(ControlP5.CENTER,ControlP5.CENTER);
    t.captionLabel().toUpperCase(false);
    t.captionLabel().setFont(createFont("Free Sans",12));
  }
  
  s = cp5.addRadioButton("splitSelector")
         .setPosition(140,260)
         .setSize(70,20)
         .setColorForeground(itemForegroundColor)
         .setColorActive(itemActiveColor)
         .setColorLabel(labelColor)
         .setItemsPerRow(2)
         .setSpacingColumn(2)       
         .addItem("Both",0)
         .addItem("Split",1)
         ;
  s.activate(0);
  
  for(Toggle t:s.getItems()) {
    t.captionLabel().align(ControlP5.CENTER, ControlP5.CENTER);
    t.captionLabel().toUpperCase(false);
    t.captionLabel().setFont(createFont("Free Sans",12));
  }
  arduinoSetPickup(currentPickup);
  arduinoSetSplit(currentSplit);
  println("Radios initialized.");
  return true;
}
/*
void keyPressed() {
  switch(key) {
    case('n'): r.activate(5); break;  // n: Neck
    case('m'): r.activate(7); break;  // m: Middle
    case('b'): r.activate(9); break;  // b: Bridge
    case('a'): r.activate(17); break; // a: All pickups
    case('l'): r.activate(11); break; // l: Left mix = neck + middle
    case('r'): r.activate(13); break; // r: Right mix = middle + bridge
    case('t'): r.activate(2); break;  // t: Top mix = neck + bridge
    case('s'): s.activate(1); break;  // s: Split
    case('u'): s.activate(0); break;  // u: Unsplit
  }
}
*/
