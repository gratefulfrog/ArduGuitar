class Preset { 
    boolean selectors[];// = {false, false, false, true};
                       // {neck, middle, bridgeNorth, bridgeBoth}
    int vol, tone;
    
    public Preset (int vt[], boolean sVec[]) {
  setVol(vt[0]);
  setTone(vt[1]);
  selectors = new boolean[sVec.length];
  setSelectors(sVec);    
    } 
    public Preset (int v, int t, boolean sVec[]) {
  setVol(v);
  setTone(t);
  selectors = new boolean[sVec.length];
  setSelectors(sVec);    
    } 
    public Preset (int v, int t, boolean n,boolean m,boolean bn,boolean b ){
  setVol(v);
  setTone(t);
  selectors = new boolean[4];
  boolean vv[] = {n,m,bn,b};
  setSelectors(vv);    
    } 
    int getAsInt(int i){
  if (i==0)               { return vol; }
  else if (i==1)          { return tone; }
  else if(selectors[i-2]) { return 1; }
  else                    { return 0; }
    }
    public void setVol(int v){
  vol = v;
    }
    public int vol(){
  return vol;
    }
    public void setTone(int t){
  tone = t;
    }
    public int tone(){
  return tone;
    }
    public void setSelectors(boolean sVec[]){
  for (int i=0;i< sVec.length;i++){
      selectors[i] =  sVec[i]; 
  }
    }
    public boolean[] selectors(){
  return selectors;
    }
}

class PresetPack {
    HashMap hm;                   
    ArduGuitarConf conf;
    int currentPresetIndex;
    String presetNames[];
    PresetPack(ArduGuitarConf ac){  // init to defaults
  hm = new HashMap();
  conf = ac;
  presetNames = new String[ac.psc.names.length];
  load();
    }
    public Preset get(String name){
  return (Preset)hm.get(name);
    }
    public Preset put(String name, 
          int v, 
          int t, 
          boolean n,
          boolean m,
          boolean bn,
          boolean b ){
  Preset p = new Preset(v,t,n,m,bn,b);
  hm.put(name,p);
  return p;
    } 
    public Preset put(String name, Preset p){
  hm.put(name,p);
  return p;
    } 
    public void load(){
  Table tsv = null;
  try {
      tsv = loadTable(ac.psc.tableFileName, "tsv");  
  } 
  catch (Exception e) {  
      println("Table load failed: " + e);
      tsv = null;  
      println("failed to open, creating new presets...");
      createDefaultPresets();
  }
  if (tsv != null) {
      for (int row = 1; row < tsv.getRowCount(); row++){
    put(tsv.getString(row,0), rowToPreset(tsv,row));
    presetNames[row-1]=tsv.getString(row,0);
    println("adding..." + tsv.getString(row,0));
      }
  }
  currentPresetIndex = 0;
    }
    void createDefaultPresets(){
  Preset plis[];
  for (int i=0;i<conf.psc.names.length;i++){
      presetNames[i]= conf.psc.names[i];
      put(conf.psc.names[i], 
    new Preset(conf.psc.defaultVT[i],
         conf.psc.defaultSelectors[i]));
  }
    }
    Preset rowToPreset(Table tsv, int row){
  int vals[] = new int[6];
  for (int i=1;i<7;i++){
      vals[i-1] = tsv.getInt(row,i);
  }
  boolean pVec[] = new boolean[4];
  for (int i=0;i<4;i++){
      if (vals[2+i]==0){
    pVec[i]=false;
      }
      else {
    pVec[i]=true;
      }
  }
  return new Preset(vals[0],vals[1],pVec);
    }
    public void unload(){
  Table table = createTable();
  
  println("unloading presets");
  for (int i=0;i<ac.psc.tableCols.length;i++){
      table.addColumn(ac.psc.tableCols[i]);
  }
  for (int i=0;i<ac.psc.names.length;i++){
      TableRow newRow = table.addRow();
      Preset p = get(presetNames[i]);
      newRow.setString(ac.psc.tableCols[0],presetNames[i]);
      for (int j=1;j<ac.psc.tableCols.length;j++){
    newRow.setInt(ac.psc.tableCols[j],p.getAsInt(j-1));
      }
  }
  try {
      saveTable(table, ac.psc.tableFileName); 
  }
  catch (Exception e) { 
      println("Save Failed: " + e);
  }
  println("rows written: " + table.getRowCount());
    }
}
void setup(){
  PresetPack p = new PresetPack(ac);
  for (int i=0;i<5;i++){
    println( "vol:" + p.get(p.presetNames[i]).vol());
    println( "tone:" + p.get(p.presetNames[i]).tone());
    print( "selectors: " );
    for (int j=0;j<4;j++){
        print(p.get(p.presetNames[i]).selectors()[j] + " ");
    }
    println();
  }
  p.unload();
}
void draw(){}
