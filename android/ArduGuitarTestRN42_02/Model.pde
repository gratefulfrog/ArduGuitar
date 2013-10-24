// * 2013 09 13 updates for minimized data

class ArduGuitarModel {
    public Hal hal;
    public ArduGuitarGui gui;
    PresetPack presets;
    boolean selectorsVec[];
    int vt[],
	v=0,
	t=1;
    public String currentPresetName,
                  preAutoPresetName;
    ArduGuitarConf.ModelConf conf;
    // FIX
    public float vtFactor;
    public int setVec[];  // used to set update only the minimum and only once.

    boolean cycling = false;
    
    public ArduGuitarModel(ArduGuitarConf ac, KetaiGesture g,KetaiVibrate v){
	conf = ac.mc;
        vtFactor = ac.hc.vtFactor;
        vt = new int[2];
	hal = new Hal(ac);
	presets = new PresetPack(ac);
        //println("after presetpack creation");
	selectorsVec =  new boolean[conf.nbPickups];
        for (int i=0;i<selectorsVec.length;i++){
          selectorsVec[i] = false;
        }
	currentPresetName = presets.presetNames[0];
        // FIX
        setVec = new int[conf.nbPickups +2];
        confirmSet();

        cycling = false;

        //println("about to create the gui instance.");
	gui = new ArduGuitarGui(ac,g,v);
    }    
    void doPreset(String name){
        //print("called doPreset with preset: " + name +".");
        if (name.equals(conf.cyclePresetLabel)){
          startCycle();
        }
        else {
          currentPresetName = name;
          setSelectors(presets.get(name).selectors(),true);    
          setVol(presets.get(name).vol(),true);
          setTone(presets.get(name).tone(), false);
        }
    }
    
    void startCycle() {
      print("startCycling called");
      cycling = true;
      preAutoPresetName = currentPresetName;
      presets.startCycling();
      doPreset(presets.c.currentName());
    }
    
    boolean isCycling(){
      return cycling;
    }
        
    boolean isCurrentPresetIndex(int i){
      return (currentPresetName.equals(presets.presetNames[i]) || 
              (isCycling() && presets.presetNames[i].equals(conf.cyclePresetLabel)));
    }
    
    void incCycle(){
      //print("incCycle called");
      if (cycling && presets.incCycle()){
        print("new preset cycled");
        doPreset(presets.c.currentName());
      }
    }
    
    void stopCycling(){
      //print("stopCycling called");
      if(cycling){
        presets.stopCycling();
        cycling = false;
        doPreset(preAutoPresetName);
        print("Cycling stopped");
      }
    }

    public void setSelectors(boolean s[],boolean wait){
      for (int i=0;i<s.length;i++){
        // FIX
        if (selectorsVec[i] != s[i]){
          selectorsVec[i] = s[i];
          setVec[i] = int(s[i]);
          print("setting setVec[" +str(i) + "] to " + str(setVec[i]));
        }
      }
      if (!wait){
        hal.minUpdate(setVec, false);
      }
    }
    public void setSelector(int i, boolean b,boolean wait){
      // FIX
      if (selectorsVec[i] != b){
        selectorsVec[i] = b;
        setVec[i] = int(b);
        println("setting setVec[" +str(i) + "] to " + str(setVec[i]));
      }
      if (!wait){
        hal.minUpdate(setVec, false);
      }
    }
    // FIX
    public void confirmSet(){
      for (int i=0;i<setVec.length;i++){
        setVec[i] = conf.setVecOkVal;
      }
    }
    
    public void reset() {
    // call this when the hardware is confused after transmission error
    // FIX
      hal.minUpdate(setVec, true);
    }
    
    public boolean[] selectors(){
	return selectorsVec;
    }
    public boolean selector(int i){
	return selectorsVec[i];
    }
    public void setVol(int vol, boolean wait){
      // FIX
      if (round(vt[v]*vtFactor) != round(vol*vtFactor) ) {
        setVec[conf.svVolIndex] = vol;
      }
      if (!wait){
        hal.minUpdate(setVec, false);
      }  
      vt[v] = vol;
    }
    public int vol(){
      //println("model vol is:" + vt[v]);
      return vt[v];
    }
    public void setTone(int tone, boolean wait){
      // FIX
      if (round(vt[t]*vtFactor) != round(tone*vtFactor) ) {
        setVec[conf.svToneIndex] = tone;        
      }
      if (!wait){
        hal.minUpdate(setVec, false);
      }
      vt[t] = tone;
    }
    public int tone(){
      //println("model tone is:" + vt[t]);
      return vt[t];
    }
    public boolean toggleSelectors(){
      // toggle any on to all off
      // toggle all off to all on
      // return true if final state is all on
      // return false if final state is all off
      boolean allOn = false;
      boolean newSelectors[] = new boolean[conf.nbPickups];
        
      for (int i = 0;i<conf.nbPickups;i++){
        newSelectors[i]=false;
      }
      for (int i=0;i<selectorsVec.length;i++){
        allOn |= selectorsVec[i];
      }
      for (int i=0;i< selectorsVec.length;i++){
        newSelectors[i] = !allOn;
      }
      if (!allOn){ // then kill the split
        newSelectors[2] = false;
      }
      setSelectors(newSelectors, false);
      return !allOn;
    }         
}
