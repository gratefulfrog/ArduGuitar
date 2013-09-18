class Cycle {
  boolean cycling = false;
  public TimerThread timer;
  int index = 0;
  PairList plis;

  Cycle(String slis[], int ilis[]){
    plis = new PairList();
    for (int i=0;i< min(slis.length,ilis.length);i++){
      Pair p = new Pair(slis[i],ilis[i]);
      plis.add(p);
    }
  }
  
  Cycle(String cycleFileName){
    plis = new PairList();
    Table tsv = null;
    try {
      tsv = loadTable(cycleFileName, "header, tsv");  
    } 
    catch (Exception e) {  
      println("Table load failed: " + e);
      tsv = null;  
      println("failed to open cycle table, aborting...");
      exit();
    }
    if (tsv != null) {
      for (int row = 0; row < tsv.getRowCount(); row++){
        Pair p = new Pair(tsv.getString(row,0), tsv.getInt(row,1));
        addPair(p);  
        println("adding..." + tsv.getString(row,0) + " " + str(tsv.getInt(row,1)));
      }
      println("data loaded OK!");
    }
    else {
      println("data load FAILED!");
      exit();
    }
  }
  
  void addPair(Pair p){
     plis.add(p);
  }
  
  void reset(){
    if (cycling()){
      quit();  
    }
    index = 0;
  }
 
  boolean cycling(){ 
    return cycling;
  }
 
  boolean cycleTimeUp(){
    return cycling() && timer.expired();
  }
  
  void startCycle(){
    timer = new TimerThread(plis.get(index).delay);
    timer.start();  
    cycling = true;
  }
  
  void incCycle(){
    timer.quit();
    incIndex();
    timer = new TimerThread(plis.get(index).delay);
    timer.start();
  }
  
  void quit(){
    timer.quit();
    cycling = false;
  }
  
  void incIndex(){
    index = (index + 1) % plis.size();
  }

  String currentName(){
     return plis.get(index).name;
  }
}
