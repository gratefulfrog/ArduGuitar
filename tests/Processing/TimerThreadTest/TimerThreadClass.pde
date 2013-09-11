class TimerThread extends Thread {
  boolean running;
  int delay,
      endMillis;
  
  // Constructor
  TimerThread (int del) {
    running = false;
    delay = del;
  }
 
  // Overriding "start()"
  void start () {
    running = true;
    endMillis = millis() + delay;
    super.start();
  }
 
  void reset(int del){
    endMillis = millis() + del;
    running = true;
  }
 
  boolean expired(){
    return !running;
  }
 
  void run () {
    try {
      while (true) {
        if (millis() >= endMillis){
         running = false; 
        } 
      }
    }
    catch (Exception e) {
      System.out.println(e + "caught"); 
    }
    System.out.println("timer thread is done!");  // The thread is done when we get to the end of run()
  }
 
  // Our method that quits the thread
  void quit() {
    System.out.println(str(delay) + "ms timer is quitting..."); 
    running = false;  // Setting running to false ends the loop in run()
    // IUn case the thread is waiting. . .
    interrupt();
  }
}

