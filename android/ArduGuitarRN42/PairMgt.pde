/* mgt of pairs and so on
 */
 
 
class Pair {
 public String name;
 public int delay;

 Pair(String s, int d){
  name = s; 
  delay = d;
 }
}

class PairList {
  ArrayList<Pair> pLis;
  
  PairList(){
    pLis = new ArrayList<Pair>();
  }
  
  void add(Pair p){
     pLis.add(p);
  }
  
  Pair get(int i){
    return pLis.get(i);
  }
  
  int size(){
    return pLis.size();
  }
}
