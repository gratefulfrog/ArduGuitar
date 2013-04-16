String s = "Msg: ",
       m = "" ,
       o = "";
boolean sent = false;

int counter = 0,
    limit = 200;

void setup(){
  size(1196/2,868/2);
  textSize(32);
  textAlign(CENTER);
}

void draw(){
  background(0);
  text(s + m, width/2,height/2);
  text("sent: " + o,width/2,height/2+ 40);
}

void keyTyped() {
  m += key;
}

void mousePressed() {
  if (mouseX > width/2){
    println("cleared!");
  }
  else if (m !=""){
      println("sent: " + m);
      o = m;
   }
   else {
    println("no action"); 
  }
  m="";
}

