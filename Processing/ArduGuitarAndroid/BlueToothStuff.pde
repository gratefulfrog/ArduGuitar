/**  Threaded Android Comms Tester
 *  maybe this will work, too....at last something that works!!!
 */

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
 
  // Constructor, create the thread
  public SenderThread (KetaiBluetooth mbt, BlockingQueue q) {
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
        /*byte []outgoingB =  new byte[outS.length()];
        for (int i=0;i<outS.length();i++){
          outgoingB[i] = byte(outS.charAt(i));
        }
	*/
        // do the bluetooth writing, and report to stdout
        bt.writeToDeviceName(btName, outgoingB);
        println("Sent: " + outS);
      }
    }
    catch (InterruptedException ex) { 
      println("Error in SenderThread while sending...");
   }
  }
  
  void quit() {
    //System.out.println("SenderThread is done!");  // The thread is done 
    // In case the thread is waiting. . .
    interrupt();
  }
}

//********************************************************************
//Call-back method to manage data received by bluetooth listner thread 
// (created in KetaiBluetooth))
void onBluetoothDataEvent(String who, byte[] data){
  if (isConfiguring)
    return;
  String incoming = "";
  for (int i=0;i<data.length;i++){
    incoming += char(data[i]);
  }
  println("Bt Recd: " + incoming);
  if (match(incoming, errorKey) != null) {
    println("BT RECEIVE ERROR DETECTED!!!");
    delay(50);
    sendVolTone();
    sendPickups();    
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
