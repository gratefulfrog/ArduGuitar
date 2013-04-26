import java.io.File;
import java.io.IOException;
import android.os.Environment;



void setup(){
  String basePath = Environment.getExternalStorageDirectory().getAbsolutePath();
  try{
    println(basePath);  // path is: /storage/emulated/0
  }
  catch(Exception e) {
    e.printStackTrace();
  }
}

void draw(){}
