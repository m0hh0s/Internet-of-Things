#include <LiquidCrystal.h>
#include <Servo.h>

const int rs = 2, en = 3, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

Servo servo;

void setup() {
  Serial.begin(9600);
  lcd.begin(16,2);
  lcd.clear();
  servo.attach(13);
}
void loop(){
  lcd.setCursor(0,0);
  lcd.clear();
  int ldr1 = analogRead(A0);
  int ldr2 = analogRead(A1);
  int ldr3 = analogRead(A2);
  if(ldr1 > ldr2 && ldr1 > ldr2){
    lcd.print("Morning");
    servo.write(0);
  }else if(ldr2 > ldr1 && ldr2 > ldr3){
    lcd.print("Noon");
    servo.write(90);
  }else if(ldr3 > ldr1 && ldr3 > ldr2){
    lcd.print("Afternoon");
    servo.write(180);
  }
  delay(500);
}
