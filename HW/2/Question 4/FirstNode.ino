#include <LiquidCrystal.h>

const int rs = 2, en = 3, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

bool firstMessageSent = false;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(11, OUTPUT);
  digitalWrite(13, LOW);
  digitalWrite(12, LOW);
  lcd.begin(16,2);
  lcd.clear();
  lcd.setCursor(0,0);
  Serial.write("Hello");
  delay(500);
  String message = Serial.readString();
  lcd.print(message);
  if(message == "Hi"){
    digitalWrite(13, HIGH);
    delay(3000);
    digitalWrite(13, LOW);
  }else{
    digitalWrite(12, HIGH);
    tone(11, 1000);
    delay(3000);
    noTone(11);
    digitalWrite(12, LOW);
  }
}

void loop(){
  
}
