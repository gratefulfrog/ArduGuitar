class Pup{
  int position;
  VT vt[];
  Pup(int pos){
    position = pos;
  }
  void initHelper(float base, float jMult){
    for (int j = 0; j< vt.length;j++){
      vt[j] = new VT(base + j*jMult);
      setVol(j,10);
      setTone(j,10);
    }
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
    initHelper(pos*(pupw+puphs)+bhs, (bw+bhs));
  }
}

class S extends Pup {
  final int nbVt = 1;
  S(int pos){ // position 0,1,2
    super(pos);
    vt = new VT[nbVt];
    initHelper(pos*(pupw+puphs)+(pupw - bw)/2.0, 0);
  }
}