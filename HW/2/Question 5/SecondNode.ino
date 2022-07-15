void setup() {
  Serial.begin(9600);
  pinMode(11, OUTPUT);
}

void loop(){
  if(Serial.available()>0){
    int message = Serial.read();
    analogWrite(11, message*1.5);
  }
  delay(500);
}
