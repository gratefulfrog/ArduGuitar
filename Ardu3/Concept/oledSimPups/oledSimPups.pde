final int w = 128,
    h = 128,
    fr = 1;
    
final int coilConf[] = {2,1,2};    
final int  
    th = 20,
    nbPups = coilConf.length;

final float
    bvs = 1.5,
    bhs = 6,
    puphs = 2,
    pupw = (w-(nbPups*puphs))/(nbPups+1),
    bw = (pupw-3*bhs)/2.0,
    bh = 2,
    baseline = 10*(bh+bvs);
      
final color red = color(255,0,0),
            yellow = color(255,255,0),
            green =  color(0,255,0);

final String seq = "(|(+AB)(+CD))",
             seqseq = seq + "\n" + seq;

Pup pupVec[];
void setup() {
  size(128,128);
  frameRate(fr);
  pupVec = new Pup[nbPups+1];
  // pup's vol/tone
  for (int j = 0; j< nbPups;j++){
    if (coilConf[j] == 1) {
      pupVec[j] = new S(j);
    }
    else{
      pupVec[j] = new H(j);
    }
  }
  // create master vol/tone
  pupVec[nbPups] = new H(nbPups);
  pupVec[nbPups].setVol(1,0);
  background(0);
}

void draw() { 
  background(0);
  // update and display pup's vol tone
  for (int j = 0; j< 3;j++){
    for (int i =0; i<coilConf[j];i++){
      pupVec[j].setVol(i,round(random(10)));
      pupVec[j].setTone(i,round(random(10)));
    }
    pupVec[j].display();
  }
  // update and display master vol tone
  for (int i =0; i<2;i++){
    pupVec[nbPups].setTone(i,round(random(10)));
  }
  pupVec[nbPups].setVol(0,round(random(10)));
  pupVec[nbPups].display();
  
  // display baseline
  displayBaseline();
}

void displayBaseline(){
  pushStyle();
  stroke (255);
  strokeWeight(0.5);
  line(0,baseline,w, baseline);
  popStyle();
}