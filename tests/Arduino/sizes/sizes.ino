
int aInt =10;
int *intPtr = &aInt;

byte aByte =10;
byte *bytePtr = &aByte;

void setup(){
  Serial.begin(115200);
  while(!Serial);
  delay(5000);
  Serial.print("sizeof(int): ");
  Serial.println(sizeof(aInt));
  Serial.print("sizeof(int*): ");
  Serial.println(sizeof(intPtr));
  Serial.print("sizeof(byte): ");
  Serial.println(sizeof(aByte));
  Serial.print("sizeof(byte*): ");
  Serial.println(sizeof(bytePtr));
}
void loop(){}

/* Results:
sizeof(int): 2
sizeof(int*): 2
sizeof(byte): 1
sizeof(byte*): 2
*/

