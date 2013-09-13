class ArduGuitarModel {
    public Hal hal;
    public ArduGuitarGui gui;
    PresetPack presets;
    boolean selectorsVec[];
    int vt[],
	v=0,
	t=1;
    public String currentPresetName;
    ArduGuitarConf.ModelConf conf;
    // FIX
    public float vtFactor;
    public int setVec[],  // used to set update only the minimum and only once.
               svVolIndex = 4,
               svToneIndex = 5;

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
        // end fix
	// ??? doPreset(currentPresetName);
        //println("about to create the gui instance.");
	gui = new ArduGuitarGui(ac,g,v);
    }    
    void doPreset(String name){
	currentPresetName = name;
	setSelectors(presets.get(name).selectors());
	setVol(presets.get(name).vol());
	setTone(presets.get(name).tone());
    }
    void saveCurrentPreset(){
	savePreset(currentPresetName);
    }
    void savePreset(String name){
	Preset p = new Preset(vt,selectorsVec);
	presets.put(name,p);
    }
    public void setSelectors(boolean s[]){
	for (int i=0;i<s.length;i++){
	    // FIX
            if (selectorsVec[i] != s[i]){
              selectorsVec[i] = s[i];
              setVec[i] = int(s[i]);
              print("setting setVec[" +str(i) + "] to " + str(setVec[i]));
            }
	}
	//hal.update(selectorsVec);
        hal.minUpdate(setVec);
    }
    public void setSelector(int i, boolean b){
        // FIX
	if (selectorsVec[i] != b){
          selectorsVec[i] = b;
          setVec[i] = int(b);
          print("setting setVec[" +str(i) + "] to " + str(setVec[i]));
          hal.minUpdate(setVec);
        }
	//hal.update(selectorsVec);
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
        hal.minUpdate(setVec);
        //hal.update(vt,selectorsVec);
    }
    public boolean[] selectors(){
	return selectorsVec;
    }
    public boolean selector(int i){
	return selectorsVec[i];
    }
    public void setVol(int vol){
        // FIX
        //int newVol = constrain(vol,conf.minVT,conf.maxVT);
        if (round(vt[v]*vtFactor) != round(vol*vtFactor) ) {
          setVec[svVolIndex] = vol;
          hal.minUpdate(setVec);
        }
        vt[v] = vol;
	// vt[v] = constrain(vol,conf.minVT,conf.maxVT);
	// hal.updateVol(vt[v]);
    }
    public int vol(){
        //println("model vol is:" + vt[v]);
	return vt[v];
    }
    public void setTone(int tone){
      // FIX
      //int newTone = constrain(tone,conf.minVT,conf.maxVT);
      if (round(vt[t]*vtFactor) != round(tone*vtFactor) ) {
        setVec[svToneIndex] = tone;        
        hal.minUpdate(setVec);
      }
      vt[t] = tone;
      //vt[t] = constrain(tone,conf.minVT,conf.maxVT);
      //hal.updateTone(vt[t]);
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
        // FIX
        boolean newSelectors[] = new boolean[conf.nbPickups];
        
        for (int i = 0;i<conf.nbPickups;i++){
          newSelectors[i]=false;
        }
        // end FIX
	for (int i=0;i<selectorsVec.length;i++){
	    allOn |= selectorsVec[i];
	}
	for (int i=0;i< selectorsVec.length;i++){
	    // FIX
            newSelectors[i] = !allOn;
            // selectorsVec[i] = !allOn;
	}
        if (!allOn){ // then kill the split
          // FIX
          newSelectors[2] = false;
          //selectorsVec[2] = false;
        }
        // FIX 
        setSelectors(newSelectors);
	//hal.update(selectorsVec);
	return !allOn;
    }  
}
