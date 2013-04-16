
 /* <p>Updated: 2011-06-09 Daniel Sauter/j.duran</p>
 * <p>Updated: 2013-04-14 gratefulfrog to make it work</p>
 */

import ketai.sensors.*;
KetaiSensor sensor;

PVector accelerometer = new PVector(),
        pAccelerometer = new PVector();


String tableReadName = "//sdcard/ArduGuitar/DataWrite-data.tsv";
String tableWriteName = tableReadName ;
// on linux
//String tableReadName = "DataWrite-data.tsv";
//String tableWriteName = "data/" + tableReadName; 

Table tsv;  //(1)
ArrayList<PVector> points = new ArrayList<PVector>(); 

void setup(){
  // remove on android
  //size(500,300);
  orientation(LANDSCAPE);

  sensor = new KetaiSensor(this);
  sensor.start();
  
  noStroke();
  textSize(24);
  textAlign(CENTER);
  
  try {
    tsv = loadTable(tableReadName, "tsv");  
  } 
  catch (Exception e) {  
    println(e);
    tsv = new Table();  
    print("failed to open");
  }
  for (int row = 0; row < tsv.getRowCount(); row++){
    points.add(new PVector(tsv.getInt(row, 0), tsv.getInt(row, 1), 0));
    println("adding..." + row);
  }
}

void draw() {
 background(78, 93, 75);
  for (int i = 0; i < points.size(); i++)  {
    ellipse(points.get(i).x, points.get(i).y, 5, 5);
  } 
  text("Number of points: " + points.size(), width/2, 50);
  text("size of table: " + tsv.getRowCount(),width/2, 80);

  float delta = PVector.angleBetween(accelerometer, pAccelerometer);
  if (degrees(delta) > 45) {
    shake();
  }
  pAccelerometer.set(accelerometer);

}

void mouseDragged() {
  points.add(new PVector(mouseX, mouseY)); 
  String data[] = {str(mouseX), str(mouseY)};
  println(data);
  tsv.addRow();
  tsv.setRow(tsv.getRowCount()-1, data);
}


void keyPressed(){  
    try {
      saveTable(tsv, tableReadName); 
    }
    catch (Exception e) { 
      println(e);
    }
  println("points written: " + tsv.getRowCount());
}

void onAccelerometerEvent(float x, float y, float z){
  accelerometer.x = x;
  accelerometer.y = y;
  accelerometer.z = z;
}

void shake(){
  points = new ArrayList<PVector>(); 
  tsv = new Table();
  println("Clearing points...");
}  

