// 2013 09 13 updates to orginal for no bt 

class Hal {
    ArduGuitarConf.HalConf conf;
    // out comment for no bt
    // private final BlockingQueue q;
    public boolean isConfiguring = true;

    public Hal(ArduGuitarConf ac){
	conf = ac.hc;
        /* out comment for no bt	
	bt.start();
	println(bt.getPairedDeviceNames());
	q = new LinkedBlockingQueue();
        SenderThread sender = new SenderThread(bt, q, ac);
        sender.start();
        */
    }
    public boolean doConnect(){
      /* out comment for no bluetooth version
      isConfiguring = !bt.connectToDeviceByName(ac.bc.btName);    
      if (!isConfiguring){
          delay(conf.configDelay);
      }
      return !isConfiguring;
      */
      // this is for no bluetooth only
      isConfiguring = false;
      return isConfiguring;
      // end of no bt 
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
      println("simulated sending: " + msg);
      /* out comment for not bt
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
    
