/**  Threaded Android Comms Tester
 * maybe this will work, too....at last something that works!!!
 */

//required for BT enabling on startup
import android.content.Intent;
import android.os.Bundle;
import android.view.KeyEvent;

import ketai.net.bluetooth.*;
import ketai.ui.*;
import ketai.net.*;

KetaiBluetooth bt;

       
boolean isConfiguring = true;
int textS= 48;
String btName = "linvor";
//String btAddress = "00:12:11:19:08:54";  // linvor on-board Ibanez RG-140  -- doesn't work because of bug in Ketai???
int bogus = -60;   // -60 => startup message for 1 second

//********************************************************************
// The following code is required to enable bluetooth at startup.
//********************************************************************
void onCreate(Bundle savedInstanceState) {
  super.onCreate(savedInstanceState);
  bt = new KetaiBluetooth(this);
}

void onActivityResult(int requestCode, int resultCode, Intent data) {
  bt.onActivityResult(requestCode, resultCode, data);
}


class SenderThread extends Thread {
  private String outgoingS;
  private KetaiBluetooth bt;
  private byte []outgoingB;
 
  // Constructor, create the thread
  public SenderThread (KetaiBluetooth mbt, String outS){
    outgoingS =  new String(outS);
    outgoingB =  new byte[outS.length()];
    for (int i=0;i<outS.length();i++){
      outgoingB[i] = byte(outS.charAt(i));
    }
    bt = mbt;
  }
  public void start (){
    // Print messages
    System.out.println("Starting thread to send: " + outgoingS); 
    // Do whatever start does in Thread, don't forget this!
    super.start();
  }
  public void run (){
    // do the bluetooth writing, and report to stdout
    bt.writeToDeviceName(btName, outgoingB);
    System.out.println("SenderThread is done!");  // The thread is done when we get to the end of run()
  }
}
//********************************************************************


//Call-back method to manage data received by bluetooth listner thread (created in KetaiBluetooth
void onBluetoothDataEvent(String who, byte[] data)
{
  if (isConfiguring)
    return;
  String incoming = "";
  for (int i=0;i<data.length;i++){
    incoming += char(data[i]);
  }
  println("Bt Recd: " + incoming);
}
        
byte[] str2bytes(String s){
  // convert a String into an array of bytes and return it.
  byte b[] = new byte[s.length()];
  for (int i=0;i<s.length();i++){
    b[i] = byte(s.charAt(i));
  }
  return b;
}

