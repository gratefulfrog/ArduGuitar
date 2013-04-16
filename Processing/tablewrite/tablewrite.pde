void setup(){
  Table t =  createTable();
  t.addColumn("x");
  t.addColumn("y");
  TableRow newRow = t.addRow();
  newRow.setString("x", "a");
  newRow.setString("y", "b");
  saveTable(t,"data/data.csv"); 
}
void draw(){} 


