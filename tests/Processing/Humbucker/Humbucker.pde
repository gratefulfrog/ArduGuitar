

/**
 * Image button. 
 * 
 * Loading images and using them to create a button. 
 */
 

ImageButtons button;

void setup()
{
  size(600, 500);
  background(102, 102, 102);
  //orientation(LANDSCAPE);
  // Define and create image button
  //imageMode(CENTER);
  PImage b = loadImage("humbucker.png");
  PImage r = loadImage("humbucker-selected.png");
  PImage d = loadImage("humbucker-selected.png");
  int x = width/2; //- b.width/2;
  int y = height/2;// - b.height/2; 
  int w = b.width/4;
  int h = b.height/4;
  button = new ImageButtons(x, y, w, h, b, r, d);
 }

void draw()
{
  background(0);
  button.update();
  button.display();
}

class Button
{
  int x, y;
  int w, h;
  color basecolor, highlightcolor;
  color currentcolor;
  boolean over = false;
  boolean pressed = false;   
  
  void pressed() {
    if(over && mousePressed) {
      pressed = true;
    } else {
      pressed = false;
    }    
  }
  
  boolean overRect(int x, int y, int width, int height) {
  if (mouseX >= x && mouseX <= x+width && 
      mouseY >= y && mouseY <= y+height) {
    return true;
  } else {
    return false;
  }
}
}

class ImageButtons extends Button 
{
  PImage base;
  PImage roll;
  PImage down;
  PImage currentimage;

  ImageButtons(int ix, int iy, int iw, int ih, PImage ibase, PImage iroll, PImage idown) 
  {
    x = ix;
    y = iy;
    w = iw;
    h = ih;
    base = ibase;
    roll = iroll;
    down = idown;
    currentimage = base;
  }
  
  void update() 
  {
    over();
    pressed();
    if(pressed) {
      currentimage = down;
      println("current image: down");
    } else if (over){
      currentimage = roll;
      println("current image: roll");
    } //else {
      //currentimage = base;
      //println("current image: base");
    //}
  }
  
  void over() 
  {
    if( overRect(x, y, w, h) ) {
      over = true;
    } else {
      over = false;
    }
  }
  
  void display() 
  {
    image(currentimage, x, y,w,h);
  }
}

