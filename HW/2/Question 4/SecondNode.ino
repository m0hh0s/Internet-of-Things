#include <LiquidCrystal.h>

const int rs = 2, en = 3, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  Serial.begin(9600);
  lcd.begin(16,2);
  lcd.clear();
  lcd.setCursor(0,0);
  randomSeed(3055);
  String message = Serial.readString();
  lcd.print(message); 
  int temp = random(0, 100);
  if(temp < 50)
    Serial.write("Hi");
  else
    Serial.write("Hello");
  delay(500);
}

void loop(){
  
}
