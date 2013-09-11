class Hal {
    ArduGuitarConf.HalConf conf;
    //private final BlockingQueue q;
    public boolean isConfiguring = true;

    public Hal(ArduGuitarConf ac){
	conf = ac.hc;	
	/*
        bt.start();
	println(bt.getPairedDeviceNames());
	q = new LinkedBlockingQueue();
        SenderThread sender = new SenderThread(bt, q, ac);
        sender.start();
        */
    }
    public boolean doConnect(){
      isConfiguring = false;
      return isConfiguring;
      /*isConfiguring = !bt.connectToDeviceByName(ac.bc.btName);    
      if (!isConfiguring){
          delay(conf.configDelay);
      }
      return !isConfiguring;
      */
    }
    public void updateVol(int v){
       if (isConfiguring){
            return;
        }
        String outgoing = "";
        // first make the volume
        for(int i=0;i<conf.volPins.length;i++){
          outgoing += conf.volPins[i] + conf.volPWM[i][round(v*conf.vtFactor)];
        }
        doSend(outgoing);
    }
    public void updateTone(int t){
       if (isConfiguring){
            return;
        }
        String outgoing = "";
        // then add the tone
        outgoing += conf.tonePin + conf.tonePWM[round(t*conf.vtFactor)];
        doSend(outgoing);
    }
    public void update(int vt[]){
       if (isConfiguring){
            return;
        }
	
	String outgoing = "";
	// first make the volume
	for(int i=0;i<conf.volPins.length;i++){
	    outgoing += conf.volPins[i] + conf.volPWM[i][round(vt[0]*conf.vtFactor)];
	}
	// then add the tone
	outgoing += conf.tonePin + conf.tonePWM[round(vt[1]*conf.vtFactor)];
	doSend(outgoing);
    }
    public void update(boolean selectors[]){
        if (isConfiguring){
            return;
        }
	String outgoing = "";
	// handle first neck, middle and bridgeNorth
	for (int i=0;i<selectors.length-1;i++){
	    outgoing +=conf.selectorPins[i];
	    if (selectors[i]){
		outgoing += conf.onOff[0];
	    }
	    else {
		outgoing += conf.onOff[1];
	    }
	}
	// now if Bridgeboth or bridgeNorth then bridge is on
	outgoing+=conf.selectorPins[3];
	if (selectors[3] || selectors[2]){
	    outgoing += conf.onOff[0];
	}
	else {
	    outgoing += conf.onOff[1];
	}
	doSend(outgoing);
    }
    public void update(int vt[],boolean selectors[]){
       if (isConfiguring){
            return;
        }
	update(vt);
	update(selectors);
    }
    void doSend(String msg){
      println("sending: " + msg);
      /*
	try {
	    q.put(msg);
	    //println("sending: " + msg);
	}
	catch (InterruptedException ex) {
	    println("ERROR sending: " + msg);
	}
      */
    }
}
    
