
String tableCols[] =  { "name",
              "vol",
              "tone",
              "neck",
              "middle",
              "bNorth",
              "bBoth"},
         names[] = {"Rock",
                     "Woman",
                     "Jazz",
                     "Comp",
                     "Lead"};

void unload(){
  Table table = new Table();
  
  println("unloading presets");
  for (int i=0;i<tableCols.length;i++){
      table.addColumn(tableCols[i]);
  }
  for (int i=0;i<names.length;i++){
      TableRow newRow = table.addRow();
      //Preset p = get(presetNames[i]);
      newRow.setString(tableCols[0],names[i]);
      for (int j=1;j<tableCols.length;j++){
              
                newRow.setInt(tableCols[j],0);
              
      }
  }
  try {
    saveTable(table, "tableRows.tsv"); 
  }
  catch (Exception e) { 
    println("Save Failed: " + e);
  }
  println("preset rows written: " + table.getRowCount());
    }
    
    void setup(){
      unload();
    }
    
    void draw(){}
    
