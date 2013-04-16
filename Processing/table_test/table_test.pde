
Table table;

void setup(){
  size(500,300);
 table =   loadTable("new.tsv", "header,tsv");
 
 println(table.getRowCount() + " total rows in table"); 

  for (TableRow row : table.rows()) {
    
    int x = row.getInt("x");
    int y = row.getInt("y");
    boolean z = boolean(row.getString("z"));
    
    println("x: " + x + " y: " + y + " z: " +z);
  }
  TableRow newRow = table.addRow();
  newRow.setInt("x", 123);
  newRow.setInt("y", 456);
  newRow.setString("z", "false");
  
  saveTable(table, "new.tsv");
   
}

void draw(){
}
