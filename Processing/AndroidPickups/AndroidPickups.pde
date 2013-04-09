/*
World's simplest Android App!
blprnt@blprnt.com
Sept 25, 2010
*/

// Build a container to hold the current rotation of the box
//float boxRotation = 0;
PImage base;
PImage overlays[] = new PImage[4];

String baseFile = "Pickups1196x768.png",
       overlayFiles[] = {"neck1196x768.png",
                         "middle1196x768.png",
                         "bridgeNorth1196x768.png",
                         "bridgeBoth1196x768.png"};

boolean on = false;
int pTime = 2000;
int imageI = 0;
int nbOverlays = 4;

void loadImages(){
  base = loadImage(baseFile);
  for (int i=0; i<nbOverlays ;i++){
    overlays[i] = loadImage(overlayFiles[i]);
  }
}

void setup() {

  // Set the size of the screen (this is not really necessary 
  // in Android mode, but we'll do it anyway)
  //size(1196,768)

  // Turn on smoothing to make everything pretty.
  smooth();

  // Set the fill and stroke color
  fill(255);
  stroke(255);

  loadImages();

  orientation(LANDSCAPE);
}

void draw() {
  background(100,100,0);

  image(base,0,0);
  
  delay(pTime);
  on = !on;
  if (!on){
    imageI = (imageI+1)%nbOverlays;
  }
  else {
    image(overlays[imageI],0,0);
  }  
}

