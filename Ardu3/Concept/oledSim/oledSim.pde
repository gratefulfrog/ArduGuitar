int w = 128,
    h = 128;
    
float  th = 20,
    nb = 9,
    bvs = 1.5,
    bhs = 8,
    bw = w/nb - bhs,
    bh = 2,
    baseline = 10*(bh+bvs);
    
color red = color(255,0,0),
      yellow = color(255,255,0),
      green =  color(0,255,0);

String seq = "(|(+AB)(+CD))",
       seqseq = seq + "\n" + seq;

void settings(){
  size(w,h);
}


VT vt[];
void setup() {
  frameRate(1);
  vt = new VT[9];
  background(0);
  for (int j = 0; j< 9;j++){
    vt[j] = new VT(j*(bw+bhs));
    vt[j].setVol(10);
    vt[j].setTone(10);
    vt[j].display();
  }
  vt[8].setVol(0);
}

void draw() { 
  background(0);
  for (int j = 0; j< 9;j++){
    vt[j].setVol(j==8 ? 0 :round(random(10)));
    vt[j].setTone(round(random(10)));
    vt[j].display();
  }
  stroke (255);
  strokeWeight(0.5);
  line(0,baseline,w, baseline);
  noStroke();
}

class VT {
  float x;
  int volV  = 0,
      toneV = 0;
  VT(float xx){
    x=xx;
  }
  void setVol(int val){
    volV = val;
  }
  void setTone(int val){
    toneV = val;
  }
  void display(){
    for (int i = 0; i< volV; i++){
      color c = i<3 ? yellow : i<7 ? green : red;
      markBox(c,x,baseline-(bh+bvs) - i*(bh+bvs));
    }
    for (int i = 0; i< toneV; i++){
      color c = i<3 ? yellow : i<7 ? green : red;
      markBox(c,x,baseline + i*(bh+bvs));
    }
  }
  void markBox(color c, float x,float y){
    float h = bh,
        w = bw;
    pushStyle();
    fill(c);
    rect(x,y,w,h);
    popStyle();
  }
}