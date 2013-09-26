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
      if (isConfiguring){
        if (connectCount++ == 0){
          isConfiguring = !bt.connectToDeviceByName(ac.bc.btName);
        }
        else if (connectCount >= conf.connectionIterationLimit) {
          connectCount = 0;
        }
      }
      */
      // this is for no bluetooth only
      isConfiguring = false;
      return !isConfiguring;
      // end of no bt 
    }
    
    // FIX
    String getVolString(int v){
        String outgoing = "";
        if (v != conf.setVecOkVal){
          // first make the volume
          for(int i=0;i<conf.volPins.length;i++){
            outgoing += conf.volPins[i] + conf.volPWM[i][round(v*conf.vtFactor)];
          }
        }  
        return outgoing;
    }
    String getToneString(int t){
        String outgoing = "";
        if (t != conf.setVecOkVal){
          // then add the tone
          outgoing += conf.tonePin + conf.tonePWM[round(t*conf.vtFactor)];
        }
        return outgoing;
    }    
    String getSelectorsString(int setVecFull[]){
      String outgoing = "";
      // handle all the selectors, since mgt of BN and BB has already been done!
      for (int i=0;i<setVecFull.length-2;i++){
        if (setVecFull[i] != conf.setVecOkVal){
          outgoing +=conf.selectorPins[i] + conf.onOff[setVecFull[i]];
        }
      }
     return outgoing;
    }
    // END FIX
    // FIX
    public void minUpdate(int sv[], boolean force) { // just update all elements in the arg setVec
       if (isConfiguring){
            return;
       }
       String outgoing = getSelectorsString(sv) + 
                         getVolString(sv[sv.length-2]) + 
                         getToneString(sv[sv.length-1]) ;
       if (!outgoing.equals("")) {
         doSend(outgoing, force);
       }        
    }
    
    // FIX ENDS
    
    void doSend(String msg, boolean force){
      println("simulated sending: " + msg);
      // for not BT version only  !!
      model.confirmSet();
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
    
