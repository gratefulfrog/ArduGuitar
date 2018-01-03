int w = 128,
    h = 128;
    
char conf[] = {'s','s','h'};    
int  
    th = 20,
    nbPups = conf.length;
float
    bvs = 1.5,
    bhs = 6,
    puphs = 2,
    pupw = (w-(nbPups*puphs))/(nbPups+1),
    bw = (pupw-3*bhs)/2.0,
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

Pup pupVec[];
void setup() {
  pupVec = new Pup[4];
  for (int j = 0; j< nbPups;j++){
    if (conf[j] == 's') {
      pupVec[j] = new S(j);
    }
    else{
      pupVec[j] = new H(j);
    }
  }
  pupVec[nbPups] = new H(nbPups);
  pupVec[nbPups].setVol(1,0);
}

void draw() { 
  background(0);
  for (int j = 0; j< 4;j++){
    pupVec[j].display();
  }
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

class Pup{
  int position;
  VT vt[];
  Pup(int pos){
    position = pos;
  }
  void setVol(int i, int val){
    vt[i].setVol(val);
  }
  void setTone(int i, int val){
    vt[i].setTone(val);
  }
  void display(){
    for (int i=0; i < vt.length;i++){
      vt[i].display();
    }
  }
}
  
    
class H extends Pup {
  final int nbVt = 2;
  H(int pos){ // position 0,1,2
    super(pos);
    vt = new VT[nbVt];
    for (int j = 0; j< nbVt;j++){
      vt[j] = new VT(pos*(pupw+puphs)+(bhs + j*(bw+bhs)));
      vt[j].setVol(10);
      vt[j].setTone(10);
      vt[j].display();
    }
  }
}

class S extends Pup {
  final int nbVt = 1;
  S(int pos){ // position 0,1,2
    super(pos);
    vt = new VT[nbVt];
    for (int j = 0; j< nbVt;j++){
      vt[j] = new VT(pos*(pupw+puphs)+(pupw - bw)/2.0); //bhs + j*(bw+bhs)));
      vt[j].setVol(10);
      vt[j].setTone(10);
      vt[j].display();
    }
  }
}