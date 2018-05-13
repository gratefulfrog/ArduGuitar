int currentPin = 2;

void incCurrentPin(){
  switch(currentPin){
    case 53:
    case 0:
    case 1:
      currentPin = 2;
      break;
    case 12:
      currentPin = 14;
      break;
    default:
      currentPin++;
      break;
  }
}


void setup() {
  for (int i=2;i<54;i++){
      pinMode(i,OUTPUT);
      digitalWrite(i,LOW);
  }
  // put your setup code here, to run once:
  Serial.begin(115200);
  while(!Serial);

}

void loop() {
  digitalWrite(currentPin, HIGH);
  Serial.println(currentPin);
  while(Serial.available()<=0);
  Serial.read();
  digitalWrite(currentPin,!digitalRead(currentPin));
  incCurrentPin();
  
}
