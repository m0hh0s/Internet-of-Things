void setup() {
  pinMode(7, OUTPUT);
  pinMode(9, OUTPUT);
}
void loop(){
  int ldr = analogRead(A0);
  if (ldr < 80){
    analogWrite(9, 255);
  }else if(80 < ldr && ldr < 150){
    analogWrite(9, 192);
  }else if(150 < ldr && ldr < 190){
    analogWrite(9, 128);
  }else if(190 < ldr && ldr < 220){
    analogWrite(9, 64);
  }else if(220 < ldr){
    analogWrite(9, 0);
    tone(7, 1000);
    delay(100);
    noTone(7);
  }
  delay(500);
}
