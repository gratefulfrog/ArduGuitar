// file_ops
// read/write presets file

String defaultPresetsFile = "presets.csv" ; //"/home/bob/.presets.csv";
String currentPresetsFile = defaultPresetsFile; 

ArrayList presetsA = new ArrayList();  // this is where the presets are stored

int getPresetVolume(int presetInd){
  return Integer.parseInt(((String[])presetsA.get(presetInd))[1]);
}
int getPresetTone(int presetInd){
  return Integer.parseInt(((String[])presetsA.get(presetInd))[2]);
}

int getPresetPickup(int presetInd){
  return Integer.parseInt(((String[])presetsA.get(presetInd))[3]);
}
int getPresetSplit(int presetInd){
  return Integer.parseInt(((String[])presetsA.get(presetInd))[4]);
}
String headerLine = "n,v,t,s,l";

void readConfig(String fileName) {
  // read all the presets from the fileName
  println("Reading file: " + fileName);
  presetsA = new ArrayList(); 
  String lines[] = loadStrings(fileName);
  for (int i=1;i<lines.length;i++){
    addConfig(lines[i]);
  }
}

void readDefaultConfig(){
  String def =  new String("Default,5,5,0,0");
  addConfig("Default,5,5,0,0");
}

void addConfig(String str){
  presetsA.add(split(str,','));
  println("Adding config: " + str);
}

void writeConfig(String fileName) {
  PrintWriter output = createWriter(fileName);
  println("Writing file: " + fileName);
  println("Writing Header Line : " + headerLine);
  output.println(headerLine); 
  for (int i = 0 ; i < presetsA.size(); i++) {
    String line = join((String[])presetsA.get(i),",");
    println("Writing Config Line : " + line);
    output.println(line);
  }   
  output.flush();
  output.close();
}

boolean initPresets(){
  File f = new File(dataPath(currentPresetsFile));
  if (!f.exists()) {
    println("Default Presets File does not exist");
    readDefaultConfig();
  }
  else {
   readConfig(currentPresetsFile);
   println("Presets initialized.");
  }
 return true;
}

