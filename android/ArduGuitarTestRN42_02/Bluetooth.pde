/**  Threaded Android bluetooth Comms with queue
 *  at last something that works!!!
 * 2013 09 13 updates for minimized data
 */

KetaiBluetooth bt;

///////////////////////////////////////////////////////////////////////////
/////    The following code is required to enable bluetooth at startup. ////
void onCreate(Bundle savedInstanceState) {
  super.onCreate(savedInstanceState);
  bt = new KetaiBluetooth(this);
}
void onActivityResult(int requestCode, int resultCode, Intent data) {
  bt.onActivityResult(requestCode, resultCode, data);
}
///////////////////////////////////////////////////////////////////////////

class SenderThread extends Thread {
  private final BlockingQueue queue;
  private KetaiBluetooth bt;
  private ArduGuitarConf.BluetoothConf conf;
 
  // Constructor, create the thread
    public SenderThread (KetaiBluetooth mbt, BlockingQueue q, ArduGuitarConf ac) {
    conf = ac.bc;  
    bt = mbt;
    queue = q;
  }
  public void start (){
    System.out.println("Starting SenderThread..."); 
    super.start();
  }
  public void run (){
    try {
      while (true) {
        String outS = (String)queue.take(); 
	byte []outgoingB = str2bytes(outS);
        // do the bluetooth writing, and report to stdout
        bt.writeToDeviceName(conf.btName, outgoingB);
        println("Sent: " + outS);
      }
    }
    catch (InterruptedException ex) { 
      println("Error in SenderThread while sending...");
   }
  }
    byte[] str2bytes(String s){
	// convert a String into an array of bytes and return it.
	byte b[] = new byte[s.length()];
	for (int i=0;i<s.length();i++){
	    b[i] = byte(s.charAt(i));
	}
	return b;
    }
  
  public void quit() {
    //System.out.println("SenderThread is done!");  // The thread is done 
    // In case the thread is waiting. . .
    interrupt();
  }
}

//********************************************************************
// Call-back method to manage data received by bluetooth listner thread 
// (created in KetaiBluetooth))
void onBluetoothDataEvent(String who, byte[] data){
    if (model.hal.isConfiguring){
      return;
    }
    
    
    String incoming = "";
    for (int i=0;i<data.length;i++){
	incoming += char(data[i]);
    }
    println("Bt Recd: " + incoming);
    if (match(incoming, ac.bc.errorKey) != null) {
	println("BT RECEIVE ERROR DETECTED!!!");
	int start = millis();
        while(millis()-start < ac.bc.errorRecoveryDelay);
        //delay(ac.bc.errorRecoveryDelay);
	model.reset();
    }
    else if (match(incoming, ac.bc.initChar) != null){ // we want an init
      if (!model.hal.initialized) { // give an init
        model.hal.doSend(ac.bc.initChar,true);
        model.hal.initialized = true;
      }
      else{ // ignore since we got an extra initChar! (I hope).
        println("received extra init char");
      }  
    }
    // FIX 
    else {
      model.confirmSet();
    }
}

