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