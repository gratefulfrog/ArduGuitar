/* R Lattice 00
 * 2 Max 4679 analog switches
 * 1 TC1044 Charge Pump
 * make a resistor lattice potentiometer
 */
 
#define NB_SWITCHES 8
#define OFF 0
#define ON 1

byte pinBase = 2;
byte curSwitchID = 0;
int pause = 2000;

byte id2Pin(byte id){
  return id+pinBase;
}

void setSwitch(byte switchID,byte logic){
  byte sLogic = (switchID%4 == 0 || switchID%4 == 3 ? logic : ! logic);
  Serial.print("ID: ");
  Serial.print(switchID);
  byte pin = id2Pin(switchID);
  Serial.print(" Pin: ");
  Serial.print(pin);
  if (sLogic){
    digitalWrite(pin,HIGH);
    Serial.println(" HIGH");
  }
  else {
    digitalWrite(id2Pin(switchID),LOW);
    Serial.println(" LOW");
  }
}

void setup(){
  Serial.begin(9600);
  for (byte id=0; id<NB_SWITCHES;id++){
    pinMode(id2Pin(id),OUTPUT);
    setSwitch(id,OFF);
  }
}

void incMod(byte*b,byte m){
  *b = (*b+1)%m;
}
  
void loop(){
  //delay(pause);
  Serial.print("Switching off: ");
  Serial.println(curSwitchID);
  setSwitch(curSwitchID,OFF);
  incMod(&curSwitchID,NB_SWITCHES);
  Serial.print("Switching on: ");
  Serial.println(curSwitchID);
  setSwitch(curSwitchID,ON);   
  while(!Serial.available());
  Serial.read();
}
  
  
  
