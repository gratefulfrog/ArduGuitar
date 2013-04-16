//import ketai.ui.*;
//KetaiGesture gesture;

// shapes tests

float sizeDiviser = 4;
float bigY = 768/2,
      bigX = 35*sizeDiviser,
      bigS = 63*sizeDiviser;

float rw = 30,
      rh = 130,
      rr = 15,
      ew = 7,
      dd = 3,
      ssw = 9,
      ssh = 20; 

float sw = rw+ssw,
      sh = rh+ssh,
      sr = rr;
float cw = rw*2+dd*3,
      ch = rh+dd*2;


PShape sCoil, sCoilSelected, dCoil, dCoilSelected, dCoilSplit, strings;

color green,black,lightBlack,grey, lightGrey, greenBody;

boolean selected[]= {false,false,false,true};

int currentPreset = 0;
int vol = 11,
    tone = 11,
    xI = 0,
    yI = 0,
    pv=11,
    pt=11,
    xRange[] = new int[4],
    yRange[]= new int[4];

boolean down = false;

color colors[] = new color[5];

String names[] = { "Rock",
                   "Blues",
                   "Jazz",
                   "Comp",
                   "Lead"};
                   
void setup() {
  size(1196,768, P2D);
  //orientation(LANDSCAPE);
  smooth();
  noStroke();
  colorMode(HSB,360,100,100);
  green = color(120,100,100);
  black = color(0,0,0);
  lightBlack = color(0,0,35);
  grey = color(120,0,60);
  lightGrey = color(120,0,90);
  greenBody = color(171,100,68);
  
  colors[0] = color(0,100,100);  //red
  colors[1] = color(60,100,100); //yellow
  colors[2] = color(120,100,100);  // green
  colors[3] = color(240,100,100);  // blue
  colors[4] = color(300,100,100); // violet
            //color(0,100,100};  // turquoise

  sCoil = sPup();
  sCoil.scale(sizeDiviser);
  
  sCoilSelected = sPupSelected();
  sCoilSelected.scale(sizeDiviser);
  
  dCoil = dPup();
  dCoil.scale(sizeDiviser);
  
  dCoilSelected = dPupSelected();
  dCoilSelected.scale(sizeDiviser);
  
  strings = makeStrings();
  strings.scale(sizeDiviser);
  
  noLoop();
}
 
PShape sPup(){
 PShape m[] = new PShape[6];
 PShape res = createShape(GROUP);
 
 PShape rect = createShape(RECT,0,0,rw,rh,rr);
 rect.setFill(black);
 res.addChild(rect);
 
 ellipseMode(CENTER);
 for (int i=0;i<6;i++){
   m[i] = createShape(ELLIPSE,rw/2,(rw/2)+2*rw*i/3,ew,ew);
   m[i].setFill(grey);
   res.addChild(m[i]);
 }
 return res;
}
 
PShape dPup(){
 PShape res = createShape(GROUP);
 
 PShape ca = createShape(RECT,0,0,cw,ch,sr);
 ca.setFill(lightBlack);
 res.addChild(ca);
 
 PShape north = sPup();
 north.translate(dd,dd);
 res.addChild(north);
 
 PShape south = sPup();
 south.translate(2*dd+rw,dd);
 res.addChild(south);
 
 return res;
}

PShape dPupSelected(){
  PShape res = createShape(GROUP);
  
  PShape rect = createShape(RECT,0,0,cw+ssw,ch+ssh,sr);
  rect.setFill(green);
  res.addChild(rect);
  
  PShape dp = dPup();
  dp.translate(ssw/2.0,ssh/2.0);
  res.addChild(dp);
  
  return res;
}

PShape sPupSelected(){
  PShape res = createShape(GROUP);
  
  PShape rect = createShape(RECT,0,0,sw,sh,sr);
  rect.setFill(green);
  res.addChild(rect);
  PShape p = sPup();
  p.translate((sw-rw)/2,(sh-rh)/2);
  res.addChild(p);
  
  return res;
}

PShape makeStrings(){
  PShape s[] = new PShape[6];
  PShape res = createShape(GROUP);
  
  stroke(lightGrey);
  strokeWeight(1.0);

  for (int i = 0; i<6;i++){
    //float ys = bigY-5*rw/3 + 2*rw*i/3;
    s[i] = createShape(LINE,0,(rw/2)+2*rw*i/3,width*7/(4*sizeDiviser),(rw/2)+2*rw*i/3);
    res.addChild(s[i]);
    println((rw/2)+2*rw*i/3);
  }
  noStroke();
  return res;
}

void drawPups(){
  shapeMode(CENTER);
  shape(sCoil, bigX, bigY);
  
  float x2 = bigX+bigS;
  shape(sCoilSelected, 
        x2, //+sCoil.width/2.0,
        bigY);
  
  float d = bigS -(rw*sizeDiviser);
  float s2 = (sizeDiviser*rw/2.0)+(sizeDiviser*cw/2.0)+d;
  float x3 = x2 + s2; 
  
  shape(dCoilSelected,
        x3, //+dCoil.width/2.0+bigS,
        bigY);
}

void draw() {
  background(greenBody);
  drawPups();
  shapeMode(CENTER);
  shape(strings,0,bigY-(rw/2)*sizeDiviser);
  drawButtons();
  drawBorder();
}
void drawBorder(){
  stroke(black);
  strokeWeight(2.0);
  line(7*width/8,0,7*width/8,height);
}

void drawButtons(){

int yEllipse = height/10, 
      yText = 0;
  ellipseMode(CENTER);    
  textSize(32);
  for (int i =0;i<5;i++){
    stroke(colors[i]);
    strokeWeight(4);
    fill(0,0,0,0);
    if (currentPreset==i){
      fill(colors[i]);
    }
    ellipse(round(width*15/16),yEllipse,width/8,height/10);
    fill(color((hue(colors[i])+180)%360,100,100));
    textAlign(CENTER,CENTER);//,CENTER);
    text(names[i],round(width*15/16),yText+height/10);
    noStroke();
    yEllipse += round(height/5);
    yText += round(height/5);
    fill(0,0,0,0);
  }
  fill(0,0,100);
  //textAlign(RIGHT,TOP);
  textAlign(CENTER,TOP);
  textSize(64);
  text(vtString("vol: ",vol),width/2,2); //width*3/4,2);
  //textAlign(RIGHT,BOTTOM);
  textAlign(CENTER,BOTTOM);
  text(vtString("tone: ",tone),width/2,height-2);//width*3/4,height-2);
  fill(0,0,0,0);
}

String vtString(String vt, int val) {
  String res = vt;
  if (val<10){
    vt +=" ";
  }
  return vt + val;
}


