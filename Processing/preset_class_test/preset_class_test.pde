class Preset { 
  int nbSelectors = 4,
      vtRange[] = {0,11};
      
  boolean selectors[] = {false, false, false, true};
                        // {neck, middle, bridgeNorth, bridgeBoth}
  int vol, tone;
  
  Preset (int v, int t, boolean sVec[]) {
    setVol(v);
    setTone(t);
    setSelectors(sVec);    
  } 
  Preset (int v, int t, boolean n,boolean m,boolean bn,boolean b ){
    setVol(v);
    setTone(t);
    boolean vv[] = {n,m,bn,b};
    setSelectors(vv);    
  } 
  void setVol(int v){
    vol = constrain(v,vtRange[0],vtRange[1]);
  }
  int vol(){
    return vol;
  }
  void setTone(int v){
    tone = constrain(v,vtRange[0],vtRange[1]);
  }
  int tone(){
    return tone;
  }
  void setSelectors(boolean sVec[]){
    for (int i=0;i< nbSelectors;i++){
      selectors[i] =  sVec[i]; 
    }
  }
  boolean[] selectors(){
    return selectors;
  }
  boolean toggleSelectors(){
   // toggle any on to all off
   // toggle all off to all on
   // return true if final state is all on
   // return false if final state is all off
  boolean allOn = false;
  for (int i=0;i< nbSelectors;i++){
    allOn |= selectors[i];
  }
  for (int i=0;i< nbSelectors;i++){
    selectors[i] = !allOn;
  }
  return !allOn;
}
  
  
  
} 

class PresetPack {
  final int nbPresets = 5;
  Preset rock   = new Preset(11,11,false,false,false,true),
         blues  = new Preset(11,8,true,false,false,true),
         jazz   =  new Preset(8,8,true,false,true,false),
         comp   =  new Preset(6,5,true,false,false,false),
         lead   =  new Preset(11,11,false,true,false,true),
         pLis[] = {rock,blues,jazz,comp,lead};

  final String names[] = { "Rock",
                           "Blues",
                           "Jazz",
                           "Comp",
                           "Lead"};
                     
  HashMap hm;                   
  
  PresetPack(){  // init to defaults
    hm = new HashMap();
    for (int i=0; i< nbPresets;i++){
      hm.put(names[i],pLis[i]);
    }
  }
  Preset get(String name){
    return (Preset)hm.get(name);
  }
  Preset put(String name, int v, int t, boolean n,boolean m,boolean bn,boolean b ){
    Preset p = new Preset(v,t,n,m,bn,b);
    hm.put(name,p);
    return p;
  } 
  Preset put(String name, Preset p){
    hm.put(name,p);
    return p;
  } 
}

PresetPack p;

void setup(){
  size(1196/2,768/2);
  smooth();
  boolean b[] = {true,false,true,false};
  p = new PresetPack();
  noLoop();
  println(p.get("Rock").selectors());
  p.get("Rock").toggleSelectors();
  println(p.get("Rock").selectors());
  p.get("Rock").toggleSelectors();
  println(p.get("Rock").selectors());
  
}

void draw(){  
}
