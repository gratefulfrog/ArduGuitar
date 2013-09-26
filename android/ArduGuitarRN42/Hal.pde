// * 2013 09 13 updates for minimized data
// maybe not correction of non-transmission of initial preset?

class Hal {
  ArduGuitarConf.HalConf conf;
  private final BlockingQueue q;
  public boolean isConfiguring = true;
  String lastMsgEqueued = "";
  int connectCount = 0;
  
  public Hal(ArduGuitarConf ac){
    conf = ac.hc;	
    bt.start();
    println(bt.getPairedDeviceNames());
    q = new LinkedBlockingQueue();
    SenderThread sender = new SenderThread(bt, q, ac);
    sender.start();
  }
  public boolean doConnect(){
    if (isConfiguring){
      if (connectCount++ == 0){
        isConfiguring = !bt.connectToDeviceByName(ac.bc.btName);
      }
      else if (connectCount >= conf.connectionIterationLimit) {
        connectCount = 0;
      }
    }
    return !isConfiguring;
  }
  
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

  // FIX STARTS
  public void minUpdate(int sv[],boolean force) { // just update all elements in the arg setVec
    if (isConfiguring){
      return;
    }
    String outgoing = getSelectorsString(sv) + 
                      getVolString(sv[sv.length-2]) + 
                      getToneString(sv[sv.length-1]) ;
    if (!outgoing.equals("")) {
      doSend(outgoing,force);
    }        
  }
  // FIX ENDS
    
  void doSend(String msg,boolean force){
    try {
      if (force || !msg.equals(lastMsgEqueued)){
        lastMsgEqueued = msg;
        q.put(msg);
        println("enqueing: " + msg);
      }
    }
    catch (InterruptedException ex) {
      println("ERROR sending: " + msg);
    }
  }
}

