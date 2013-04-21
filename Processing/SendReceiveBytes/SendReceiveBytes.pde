/* SendReceiveBytes: Written by ScottC on 25 March 2013 using 
   Processing version 2.0b8
   Tested on a Samsung Galaxy SII, with Android version 2.3.4
   Android ADK - API 10 SDK platform */

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.widget.Toast;
import android.view.Gravity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;

import java.util.UUID;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import android.os.Handler;
import android.os.Message;
import android.util.Log;

import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
public BluetoothSocket scSocket;


boolean foundDevice=false; //When true, the screen turns green.
boolean BTisConnected=false; //When true, the screen turns purple.
String serverName = "ArduGuitarServer";
String btMododuleName =  "linvor";  // for my bt module... replace ref to Seee

// Message types used by the Handler
public static final int MESSAGE_WRITE = 1;
public static final int MESSAGE_READ = 2;
String readMessage="",
    sentMessage="";

//Get the default Bluetooth adapter
BluetoothAdapter bluetooth = BluetoothAdapter.getDefaultAdapter();

/*The startActivityForResult() within setup() launches an 
  Activity which is used to request the user to turn Bluetooth on. 
  The following onActivityResult() method is called when this 
  Activity exits. */
@Override
    protected void onActivityResult(int requestCode, 
				    int resultCode, 
				    Intent data) {
    if (requestCode==0) {
	if (resultCode == RESULT_OK) {
	    ToastMaster("Bluetooth has been switched ON");
	} 
	else {
	    ToastMaster("You need to turn Bluetooth ON !!!");
	}
    }
}


/* Create a BroadcastReceiver that will later be used to 
   receive the names of Bluetooth devices in range. */
BroadcastReceiver myDiscoverer = new myOwnBroadcastReceiver();

/* Create a BroadcastReceiver that will later be used to
   identify if the Bluetooth device is connected */
BroadcastReceiver checkIsConnected = new myOwnBroadcastReceiver();

// The Handler that gets information back from the Socket
private final Handler mHandler = new Handler() {
	@Override
	    public void handleMessage(Message msg) {
	    switch (msg.what) {
	    case MESSAGE_WRITE:
		//Do something when writing
		break;
	    case MESSAGE_READ:
		//Get the bytes from the msg.obj
		byte[] readBuf = (byte[]) msg.obj;
		// construct a string from the valid bytes in the buffer
		readMessage += new String(readBuf, 0, msg.arg1);
		break;
	    }
	}
    };


void setup() {
    orientation(LANDSCAPE);
    textSize(48);
    textAlign(CENTER,TOP);
    /*IF Bluetooth is NOT enabled, then ask user permission to enable it */
    if (!bluetooth.isEnabled()) {
	Intent requestBluetooth = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
	startActivityForResult(requestBluetooth, 0);
    }


    /*If Bluetooth is now enabled, then register a broadcastReceiver to report any
      discovered Bluetooth devices, and then start discovering */
    if (bluetooth.isEnabled()) {
	registerReceiver(myDiscoverer, new IntentFilter(BluetoothDevice.ACTION_FOUND));
	registerReceiver(checkIsConnected, new IntentFilter(BluetoothDevice.ACTION_ACL_CONNECTED));

	//Start bluetooth discovery if it is not doing so already
	if (!bluetooth.isDiscovering()) {
	    bluetooth.startDiscovery();
	}
    }
}


void draw() {
    //Display a green screen if a device has been found,
    //Display a purple screen when a connection is made to the device
    if (foundDevice) {
	if (BTisConnected) {
	    background(170, 50, 255); // purple screen
	}
	else {
	    background(10, 255, 10); // green screen
	}
    }

    //Display anything received from Arduino
    text("sent: " + sentMessage,width/2, 5);
    text("received: " + readMessage, width/2, 55);
}


/* This BroadcastReceiver will display discovered Bluetooth devices */
public class myOwnBroadcastReceiver extends BroadcastReceiver {
    ConnectToBluetooth connectBT;

    @Override
	public void onReceive(Context context, Intent intent) {
	String action=intent.getAction();
	ToastMaster("ACTION:" + action);

	//Notification that BluetoothDevice is FOUND
	if (BluetoothDevice.ACTION_FOUND.equals(action)) {
	    //Display the name of the discovered device
	    String discoveredDeviceName = intent.getStringExtra(BluetoothDevice.EXTRA_NAME);
	    //ToastMaster("Discovered: " + discoveredDeviceName);

	    //Display more information about the discovered device
	    BluetoothDevice discoveredDevice = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
	    /*
	      ToastMaster("getName() = " + discoveredDevice.getName());
	      ToastMaster("getAddress() = " + discoveredDevice.getAddress());
	      int bondyState=discoveredDevice.getBondState();
	      ToastMaster("getBondState() = " + bondyState);

	      String mybondState;
	      switch(bondyState) {
	      case 10: 
	      mybondState="BOND_NONE";
	      break;
	      case 11: 
	      mybondState="BOND_BONDING";
	      break;
	      case 12: 
	      mybondState="BOND_BONDED";
	      break;
	      default: 
	      mybondState="INVALID BOND STATE";
	      break;
	      }
	      ToastMaster("getBondState() = " + mybondState);
	      }
	    */
	    //Change foundDevice to true which will make the screen turn green
	    foundDevice=true;

	    //Connect to the discovered bluetooth device (was SeeedBTSlave, now "linvor")
	    if (discoveredDeviceName.equals(btMododuleName)) {
		ToastMaster("Connecting you Now !!");
		unregisterReceiver(myDiscoverer);
		connectBT = new ConnectToBluetooth(discoveredDevice);
		//Connect to the the device in a new thread
		new Thread(connectBT).start();
	    }
	}

	//Notification if bluetooth device is connected
	if (BluetoothDevice.ACTION_ACL_CONNECTED.equals(action)) {
	    ToastMaster("CONNECTED _ YAY");

	    while (scSocket==null) {
		//do nothing
	    }
	    ToastMaster("scSocket" + scSocket);
	    BTisConnected=true; //turn screen purple 
	    if (scSocket!=null) {
		SendReceiveBytes1 sendReceiveBT = new SendReceiveBytes1(scSocket);
		new Thread(sendReceiveBT).start();
		String red = "02255042550325505255";
		byte[] myByte = stringToBytesUTFCustom(red);
		sendReceiveBT.write(myByte);
		sentMessage = red;
	    }
	}
    }
}

public static byte[] stringToBytesUTFCustom(String str) {
    char[] c = str.toCharArray();
    byte[] b = new byte[c.length];
    for (int i = 0; i < c.length; i++) {
	b[i] =  byte(c[i]);
    }
    return b;
}

public class ConnectToBluetooth implements Runnable {
    private BluetoothDevice btShield;
    private BluetoothSocket mySocket = null;
    private UUID uuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");

    public ConnectToBluetooth(BluetoothDevice bluetoothShield) {
	btShield = bluetoothShield;
	try {
	    mySocket = btShield.createRfcommSocketToServiceRecord(uuid);
	}
	catch(IOException createSocketException) {
	    //Problem with creating a socket
	    println("ConnectToBluetooth Error with Socket");
	}
    }

    @Override
	public void run() {
	/* Cancel discovery on Bluetooth Adapter to prevent slow connection */
	bluetooth.cancelDiscovery();

	try {
	    /*Connect to the bluetoothShield through the Socket. This will block
	      until it succeeds or throws an IOException */
	    mySocket.connect();
	    scSocket=mySocket;
	} 
	catch (IOException connectException) {
	    println("ConnectToBluetooth Error with Socket Connection");
	    try {
		mySocket.close(); //try to close the socket
	    }
	    catch(IOException closeException) {
	    }
	    return;
	}
    }

    /* Will cancel an in-progress connection, and close the socket */
    public void cancel() {
	try {
	    mySocket.close();
	} 
	catch (IOException e) {
	}
    }
}


private class SendReceiveBytes1 implements Runnable {
    private BluetoothSocket btSocket;
    private InputStream btInputStream = null;
    private OutputStream btOutputStream = null;
    String TAG = "SendReceiveBytes1";

    public SendReceiveBytes1(BluetoothSocket socket) {
	btSocket = socket;
	try {
	    btInputStream = btSocket.getInputStream();
	    btOutputStream = btSocket.getOutputStream();
	} 
	catch (IOException streamError) { 
	    println("Error when getting input or output Stream");
	}
    }


    public void run() {
	byte[] buffer = new byte[1024]; // buffer store for the stream
	int bytes; // bytes returned from read()

	// Keep listening to the InputStream until an exception occurs
	while (true) {
	    try {
		// Read from the InputStream
		bytes = btInputStream.read(buffer);
		// Send the obtained bytes to the UI activity
		mHandler.obtainMessage(MESSAGE_READ, bytes, -1, buffer)
		    .sendToTarget();
	    } 
	    catch (IOException e) {
		println("Error reading from btInputStream");
		break;
	    }
	}
    }


    /* Call this from the main activity to send data to the remote device */
    public void write(byte[] bytes) {
	try {
	    btOutputStream.write(bytes);
	} 
	catch (IOException e) { 
	    println("Error when writing to btOutputStream");
	}
    }


    /* Call this from the main activity to shutdown the connection */
    public void cancel() {
	try {
	    btSocket.close();
	} 
	catch (IOException e) { 
	    println("Error when closing the btSocket");
	}
    }
}



/* My ToastMaster function to display a messageBox on the screen */
void ToastMaster(String textToDisplay) {
    Toast myMessage = Toast.makeText(getApplicationContext(), 
				     textToDisplay, 
				     Toast.LENGTH_SHORT);
    myMessage.setGravity(Gravity.CENTER, 0, 0);
    myMessage.show();
}
