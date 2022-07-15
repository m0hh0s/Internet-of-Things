void setup() {
  Serial.begin(9600);
}

void loop(){
  int temp = analogRead(A0)/2;
  Serial.write(temp);
  delay(500);
}
