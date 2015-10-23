void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(1000);

  pinMode(5,OUTPUT);
  digitalWrite(5,LOW);

  Serial.println("time for a LOW OUTPUT to get pulled HIGH as INPUT");
  long u = micros();
  pinMode(5, INPUT);
  digitalWrite(5,HIGH);
  while (digitalRead(5) != HIGH);
  Serial.println(micros()-u);  // 20 u secs

  Serial.println("time for a High input to go to LOW output");
  u = micros();
  pinMode(5,OUTPUT);
  digitalWrite(5,LOW);
  while (digitalRead(5) != LOW);
  Serial.println(micros()-u);  // 16 U secs

  Serial.println("time for a LOW output to go to HIGH OUTPUT");
  u = micros();
  pinMode(5,OUTPUT);
  digitalWrite(5,HIGH);
  while (digitalRead(5) != HIGH);
  Serial.println(micros()-u); // 20 u secs
}

void loop() {
  // put your main code here, to run repeatedly:
}
