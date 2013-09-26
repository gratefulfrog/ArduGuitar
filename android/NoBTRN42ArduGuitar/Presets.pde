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
    Cycle c;
    HashMap hm;                   
    ArduGuitarConf conf;
    public String presetNames[];
    public PresetPack(ArduGuitarConf ac){  // init to defaults
	hm = new HashMap();
	conf = ac;
	presetNames = new String[conf.psc.names.length];
	load();
        //println(presetNames[0]);
    }
    public Preset get(String name){
	return (Preset)hm.get(name);
    }
    public int nbPresets(){
	return presetNames.length;
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
	    tsv = loadTable(conf.psc.tableFileName, "tsv");  
	} 
	catch (Exception e) {  
	    println("Table load failed: " + e);
	    tsv = null;  
	    println("failed to open, creating new presets...");
	    createDefaultPresets();
	}
	if (tsv != null) {
	    for (int row = 1; row < tsv.getRowCount(); row++){
              if (tsv.getString(row,0).equals("")){
                println("empty name in presets file! Please correct this!");
                continue;
              }
              // if the name == conf.cycleLabel, then load the cycle file and continue the loop
              if (conf.mc.cyclePresetLabel.equals(tsv.getString(row,0))){
                c = new Cycle(conf.psc.cycleFileName);
                println("creating cycles & adding..." + tsv.getString(row,0));
              }
                
              put(tsv.getString(row,0), rowToPreset(tsv,row));
	      presetNames[row-1]=tsv.getString(row,0);
	      println("adding..." + tsv.getString(row,0));
	    }
	}
    }
    void createDefaultPresets(){
        println("creating default presets.");
	for (int i=0;i<conf.psc.names.length;i++){
	    presetNames[i]= conf.psc.names[i];
	    put(conf.psc.names[i], 
		new Preset(conf.psc.defaultVT[i],
			   conf.psc.defaultSelectors[i]));
	}
        println("default presets created.");
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
	for (int i=0;i<conf.psc.tableCols.length;i++){
	    table.addColumn(conf.psc.tableCols[i]);
	}
	for (int i=0;i<conf.psc.names.length;i++){
	    TableRow newRow = table.addRow();
	    Preset p = get(presetNames[i]);
	    newRow.setString(conf.psc.tableCols[0],presetNames[i]);
	    for (int j=1;j<conf.psc.tableCols.length;j++){
              if (!conf.mc.cyclePresetLabel.equals(presetNames[i])){
	        newRow.setInt(conf.psc.tableCols[j],p.getAsInt(j-1));
              }
              else {
                newRow.setInt(conf.psc.tableCols[j],0);
              }
	    }
	}
	try {
	  saveTable(table, conf.psc.tableFileName); 
	}
	catch (Exception e) { 
	  println("Save Failed: " + e);
	}
	println("preset rows written: " + table.getRowCount());
    }
    
    public void startCycling(){
      c.reset();
      c.startCycle();
    }
   
    public boolean incCycle() {
      boolean ret = false; 
      if (c.cycleTimeUp()) {
        ret = true;
        c.incCycle();
      }
      return ret;
    }

    public void stopCycling(){
      if(c.cycling()) {
        c.quit();
      }
    }
}
