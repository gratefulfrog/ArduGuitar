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

String incoming = "",
       outgoing = "";
       
boolean isConfiguring = true;
int textS= 48;
String btName = "linvor";
//String btAddress = "00:12:11:19:08:54";  // linvor on-board Ibanez RG-140  -- doesn't work because of bug in Ketai???
int bogus = -60,   // -60 => startup message for 1 second
    maxIn = 24,
    bogusCycles = 500;

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

void setup(){   
  orientation(LANDSCAPE);
  background(0);
  textSize(textS);
  textAlign(CENTER);

  bt.start();
  println(bt.getPairedDeviceNames());
}

void draw(){
  if (bogus<0){
    text("Connecting to " + btName +"...",width/2,textS);  // will be overwritten by background()...
    bogus++;
  }
  else if (isConfiguring){
    isConfiguring = !bt.connectToDeviceByName(btName);    
    if (!isConfiguring){
      delay(500);
    }
  }
  else {  // we're connected!
    background(0);
    KetaiKeyboard.show(this);
    text("Sent: " + outgoing,width/2,textS);
    text("Recd: " + incoming,width/2,2*textS);
    text("type 5 digits or 'ENTER' to send; or 'x' to exit",width/2,4*textS);
    if (bogus > 0){
      text("I said, '5 digits, s or ENTER'! Pay Attention!",width/2,5*textS);
      bogus--;
    }
  }   
}

//Call-back method to manage data received by bluetooth listner thread (created in KetaiBluetooth
void onBluetoothDataEvent(String who, byte[] data)
{
  if (isConfiguring)
    return;
  if(incoming.length()> maxIn){
     incoming = "";
  }
  for (int i=0;i<data.length;i++){
    incoming += char(data[i]);
  }
}

public void keyPressed() {
  if (isConfiguring){
    return;
  }
  if (key >='0' && key <= '9') {
    //out += key;
    outgoing += key;  
    bogus=0;
  }
  else if ((keyCode == android.view.KeyEvent.KEYCODE_ENTER) && 
           (outgoing.length()>0)                            && 
           (outgoing.length() % 5 == 0)) {
    SenderThread st = new SenderThread(bt,outgoing);
    st.start();
    println("kicked off a SenderThread!");
    outgoing = "";
    bogus=0;
  }
  else if (key == 'x'){
    bogus=0;
    bt.stop();
    System.exit(0);
  }  
  else{
    outgoing = "";
    bogus = bogusCycles;
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

