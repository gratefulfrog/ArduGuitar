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
