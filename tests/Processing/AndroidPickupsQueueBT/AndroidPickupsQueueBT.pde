/*
  Android Pickups with a synchroized queue...
  can simulate error to be sure error handling is ok
*/


///////////////   SET THIS TO FALSE for PRODUCTION /////////

boolean simulateErrorsOnLongPress = true;

////////////////////////////////////////////////////////////

//required for BT enabling on startup
import android.content.Intent;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.MotionEvent;

import java.util.concurrent.*;  // for the sync queue

import ketai.net.bluetooth.*;
import ketai.net.*;
import ketai.ui.*;

KetaiGesture gesture;
KetaiVibrate vibe;
KetaiBluetooth bt;

BlockingQueue q;

PImage base;
PImage overlays[] = new PImage[4];

String baseFile = "Pickups1196x768.png",
    overlayFiles[] = {"neck1196x768.png",
		      "middle1196x768.png",
		      "bridgeNorth1196x768.png",
		      "bridgeBoth1196x768.png"};
String names[] = { "Rock",
                   "Woman",
                   "Jazz",
                   "Comp",
                   "Lead"};
String errorKey = "e";
String btName = "linvor";
//String btAddress = "00:12:11:19:08:54";  
// linvor on-board Ibanez RG-140  -- doesn't work because of bug in Ketai???

boolean selected[]= {false,false,false,true};
boolean down = false;
boolean isConfiguring = true;

int textSizeInit= 48,
    textSizeEllipse = 32,
    textSizeVT = 54;

int bogus = -60;   // -60 => startup message for 1 second
int currentPreset = 0;
int nbOverlays = 4;
int vol = 11,
    tone = 11,
    xI = 0,
    yI = 0,
    pv=11,
    pt=11,
    xRange[] = new int[4],
    yRange[]= new int[4];
int colorHues = {0, //red
		 60, //yellow
		 120, // green
		 240, //blue
		 300};  // violet
                 // O // turquoise
int colorSat = 100,
    colorBrit = 100;
int configDelay = 750;

color colors[] = new color[5];

void loadImages(){
    base = loadImage(baseFile);
    for (int i=0; i<nbOverlays ;i++){
	overlays[i] = loadImage(overlayFiles[i]);
    }
}

void sendVolTone(){
    // this needs to be adapted to model/hal/etc.
    int vOut = round(map(vol,0,11,0,255)),
	tOut = round(map(tone,0,11,0,255));
    String outgoing = "11" + nf(vOut,3) +
	"09" + nf(tOut,3);                    
    doSend(outgoing);
}
void   sendPickups(){
    // this needs to be adapted to model/hal/etc.
    String s[]= {"02","03","04","05"},
	outgoing = "";
	for (int i=0;i<4;i++){
	    if(selected[i]){
		s[i] +="255";
	    }
	    else{
		s[i] +="000";
	    }
	    outgoing+=s[i];
	}
	doSend(outgoing);
}
  
void doSend(String msg){
    try {
	q.put(msg);
	println("sending: " + msg);
    }
    catch (InterruptedException ex) {
	println("ERROR sending: " + msg);
    }
}

void setupKetaiAndBT(){
    gesture = new KetaiGesture(this);
    vibe = new KetaiVibrate(this);
    bt.start();
    println(bt.getPairedDeviceNames());
    q = new LinkedBlockingQueue();
    SenderThread sender = new SenderThread(bt, q);
    sender.start();
}

void setupGUI(){
    orientation(LANDSCAPE);

    colorMode(HSB, 359, 100, 100);
    for (int i=0;i<colors.length();i++){
	colors[i] = color(colorHues[i],colorSat,colorBrit);
    }

    smooth();
    fill(255);
    noStroke();
    loadImages();
    ellipseMode(CENTER);
}

void setup() {
    setupGUI();
    setupKetaiAndBT();
}

void connectingMsg(){
    background(0,0,0);
    fill(0,0,100);
    textAlign(CENTER);
    textSize(textSizeInit);
    stroke(0,0,colorBrit);
    text("Connecting to " + btName +"...",width/2,textS);  // will be overwritten by background()...
    bogus++;
}

void doConnect(){
    isConfiguring = !bt.connectToDeviceByName(btName);    
    if (!isConfiguring){
	delay(configDelay);
	sendPickups();
	sendVolTone();
    }
}

void draw() {
    if (bogus<0){
	connectingMsg();
    }
    else if (isConfiguring){
	doConnect();
    }
    else {  // we're connected!
	drawStuff();
    }
}

void drawPickups(){
    image(base,0,0);
  
    for (int i=0;i<nbOverlays;i++){
	if (selected[i])
	    image(overlays[i],0,0);
    }
}

void drawPresetButtons(){
    int yEllipse = height/10, 
	yText = 0,
	xEllipse = round(width*15.0/16.0),
	wEllipse = width/8,
	yInc = round(height/5.0);
 
    textSize(textSizeEllipse);
    for (int i =0;i<5;i++){
	stroke(colors[i]);
	strokeWeight(4);
	fill(0,0,0,0);
	if (currentPreset==i){
	    fill(colors[i]);
	}
	ellipse(xEllipse,yEllipse,wEllipse,yInc/2);
	fill(color((hue(colors[i])+180)%360,colorSat,colorBrit));
	textAlign(CENTER,CENTER);
	text(names[i],xEllipse,yText+yInc/2);
	noStroke();
	yEllipse += yInc;
	yText += yInc;
	fill(0,0,0,0);
    }
}

void drawVT(){
    fill(0,0,100);

    textAlign(CENTER,TOP);
    textSize(textSizeVT);
    text(vtString("vol: ",vol),width/2,2); 

    textAlign(CENTER,BOTTOM);
    text(vtString("tone: ",tone),width/2,height-2);
    fill(0,0,0,0);
}

void drawStuff(){
    background(0,0,0,0);
    drawPickups();
    drawPresetButtons();
    drawVT();
}

String vtString(String vt, int val) {
    String res = vt;
    if (val<10){
	vt +=" ";
    }
    return vt + val;
}

void onTap(float x, float y){       
    if (isConfiguring){
	return;
    }
    if (x < width/4) {
	selected[0]= !selected[0];
    }
    else if (x < width/2) {   
	selected[1]= !selected[1];
    }
    else if (x < width*5/8) {
	selected[2]= !selected[2];
	if (selected[2]){
	    selected[3] = false;
	}
    }
    else if (x < width*7/8){
	selected[3]= !selected[3];
	if (selected[3]){
	    selected[2] = false;
	}
    }
    else {
	for (int i=0;i< 5;i++){
	    if (y < height*(i+1)/5) {
		println("color selected: " + i);
		currentPreset = i;
		break;
	    }
	}
    }
    sendPickups();
}

void onLongPress(float x, float y){
    if (isConfiguring){
	return;
    }
    if (x < width*7/8) {
	println("  doAllOnOff!");
	if (simulateErrorsOnLongPress){
	    doSend("17300");
	    println("Simlating an error... 17300");
	}
	else {
	    doAllOnOff();
	}
    }
    else {
	// do stuff
	onTap(x,y);
	vibe.vibrate(1000);
	println("vibrate!");    
    }
}

void doAllOnOff(){
    boolean allOn = false;
    for (int i=0;i< nbOverlays;i++){
	allOn |= selected[i];
    }
    for (int i=0;i< nbOverlays;i++){
	selected[i] = !allOn;
    }
    sendPickups();
}

void keyPressed() {
    if (isConfiguring){
	return;
    }
    if (key == CODED && keyCode == MENU) {
	println("menu press!");
	vibe.vibrate(1000);
    }
}

void mousePressed() {
    if (isConfiguring){
	return;
    }
    if(!down){
	xI = mouseX;
	yI = mouseY;
	pv = vol;
	pt = tone;
	down = true;
    }
    println("pressed");
}

void mouseDragged(){
    if (isConfiguring){
	return;
    }
    if (xI>=width*7/8){
	return;
    }
    checkDirection();
    vol = constrain(round(map(mouseX - xI,xRange[0],xRange[1],xRange[2],xRange[3])),0,11);
    tone = constrain(round(map(mouseY - yI, yRange[0],yRange[1],yRange[2],yRange[3])),0,11);
    sendVolTone();
}

void checkDirection(){
    if (mouseX>=xI){
	xRange[0] = 0;
	xRange[1] = width-xI;
	xRange[2] = pv;
	xRange[3] = 11;
    
    }
    else{
	xRange[0] = -xI;
	xRange[1] = 0;
	xRange[2] = 0;
	xRange[3] = pv;
    }
    if (mouseY>=yI){
	yRange[0] = 0;
	yRange[1] = height-yI;
	yRange[2] = pt;
	yRange[3] = 0;
    
    }
    else{
	yRange[0] = 0;
	yRange[1] = -yI;
	yRange[2] = pt;
	yRange[3] = 11;
    }
}

void mouseReleased() {
    down = false;
    println("released");
}

public boolean surfaceTouchEvent(MotionEvent event) {
    //call to keep mouseX, mouseY, etc updated
    super.surfaceTouchEvent(event);
    //forward event to class for processing
    return gesture.surfaceTouchEvent(event);
}

