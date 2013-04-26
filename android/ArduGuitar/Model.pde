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

    public ArduGuitarModel(ArduGuitarConf ac, KetaiGesture g,KetaiVibrate v){
	conf = ac.mc;
        vt = new int[2];
	hal = new Hal(ac);
	presets = new PresetPack(ac);
        //println("after presetpack creation");
	selectorsVec =  new boolean[conf.nbPickups];
	currentPresetName = presets.presetNames[0];
	doPreset(currentPresetName);
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
	    selectorsVec[i] = s[i];
	}
	hal.update(selectorsVec);
    }
    public void setSelector(int i, boolean b){
	selectorsVec[i] = b;
	hal.update(selectorsVec);
    }
    public void reset() {
	// call this when the hardware is confused after transmission error
	hal.update(vt,selectorsVec);
    }
    public boolean[] selectors(){
	return selectorsVec;
    }
    public boolean selector(int i){
	return selectorsVec[i];
    }
    public void setVol(int vol){
	vt[v] = constrain(vol,conf.minVT,conf.maxVT);
	hal.updateVol(vt[v]);
    }
    public int vol(){
        //println("model vol is:" + vt[v]);
	return vt[v];
    }
    public void setTone(int tone){
	vt[t] = constrain(tone,conf.minVT,conf.maxVT);
	hal.updateTone(vt[t]);
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
	for (int i=0;i<selectorsVec.length;i++){
	    allOn |= selectorsVec[i];
	}
	for (int i=0;i< selectorsVec.length;i++){
	    selectorsVec[i] = !allOn;
	}
        if (!allOn){ // then kill the split
          selectorsVec[2] = false;
        }
	hal.update(selectorsVec);
	return !allOn;
    }  
}
