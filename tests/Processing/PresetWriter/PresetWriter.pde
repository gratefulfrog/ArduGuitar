/* PresetWriter tests reading and writing tables
 */

//String tableReadName = "//sdcard/ArduGuitar/data.tsv";
//String tableWriteName = tableReadName ;
// on linux
String tableReadName = "DataWrite-data.tsv";
String tableWriteName = "data/" + tableReadName;

int rock[] = {0,0,0,0,0,0,0},
    woman[]  = {1,1,0,0,0,0,0},
    jazz[]   = {2,2,0,0,0,0,0},
    comp[]   = {3,3,0,0,0,0,0},
    lead[]   = {4,4,0,0,0,0,0}, 
    plis[][] = {rock,woman,jazz,comp,lead};

void setup(){
  // remove on android
  //orientation(LANDSCAPE);
  Table table =createTable();
  table.addColumn("vol");
  table.addColumn("tone");
  table.addColumn("neck");
  table.addColumn("middle");
  table.addColumn("bNorth");
  table.addColumn("bBoth");
  
  for (int i=0;i<5;i++){
    TableRow newRow = table.addRow();
    newRow.setInt("vol", plis[i][0]);
    newRow.setInt("tone", plis[i][1]); 
    newRow.setInt("neck", plis[i][2]);
    newRow.setInt("middle", plis[i][3]);
    newRow.setInt("bNorth", plis[i][4]);
    newRow.setInt("bBoth", plis[i][5]);
  }
  try {
    saveTable(table, tableWriteName); 
  }
  catch (Exception e) { 
    println("Save Failed: " + e);
  }
  println("rows written: " + table.getRowCount());

  delay(500);
  Table newTable;
  try {
    newTable = loadTable(tableReadName, "tsv");  
  } 
  catch (Exception e) {  
    println(e);  
    newTable = createTable();
    print("failed to open");
  }
  for (int row = 1; row < newTable.getRowCount(); row++){
    String s = "";
    for (int i=0;i<6;i++){
      s += str(newTable.getInt(row, i)) +" ";
    }
    println(s);
  }
  
}



void draw() {}
