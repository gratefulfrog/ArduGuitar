/**  Simple Bluetooth Connection
 * at last something that works!!!
 */

//required for BT enabling on startup
import android.content.Intent;
import android.os.Bundle;

import ketai.net.bluetooth.*;
import ketai.ui.*;
import ketai.net.*;

KetaiBluetooth bt;

String incoming = "",
       outgoing = "";
boolean isConfiguring = true;
int textS= 48;
String btName = "linvor";
int bogus = -60;

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

//********************************************************************

void setup(){   
  orientation(LANDSCAPE);
  background(0);
  textSize(textS);
  textAlign(CENTER);

  bt.start();
  // for debugging
  println(bt.getPairedDeviceNames());
}

void draw(){
    if (bogus<0){
      text("Connecting to " + btName +"...",width/2,textS);  // will be overwritten by background()...
      bogus++;
    }
    else {
      if (isConfiguring){
      isConfiguring = !bt.connectToDeviceByName(btName);    
      if (!isConfiguring){
        delay(500);
      }
    }
    background(0);
    if (!isConfiguring){  // we're connected!
      KetaiKeyboard.show(this);
      text("Sent: " + outgoing,width/2,textS);
      text("Recd: " + incoming,width/2,2*textS);
      text("type 'a' pin2 on; or 'x' pin2 off; or 'z' exit",width/2,4*textS);
      if (bogus > 0){
        text("I said, 'a or z or x'! Pay Attention!",width/2,5*textS);
        bogus--;
      }
    }   
  }
}

//Call back method to manage data received
void onBluetoothDataEvent(String who, byte[] data)
{
  if (isConfiguring)
    return;
  //incoming = "";
  for (int i=0;i<data.length;i++){
    incoming += char(data[i]);
  }
}

public void keyPressed() {
  if (isConfiguring){
    return;
  }
  String out = "";
  if (key =='a') {
    out ="02255";
    bogus=0;
  }
  else if (key == 'z'){
    out ="02000";
  bogus=0;  
  }
  else if (key == 'x'){
    bogus=0;
    bt.stop();
    System.exit(0);
  }
  else  {
    bogus = 1000;
    return;
  }
  outgoing += out;
  bt.writeToDeviceName("linvor", str2bytes(out,5));
}

byte[] str2bytes(String s, int len){
  byte b[] = new byte[len];
  for (int i=0;i<5;i++){
    b[i] = byte(s.charAt(i));
  }
  return b;
}

