#include <Keypad.h>
#include <Servo.h>

Servo servo;

const byte ROWS = 4;
const byte COLS = 3;
char hexaKeys[ROWS][COLS] = {
  {'1','2','3'},
  {'4','5','6'},
  {'7','8','9'},
  {'*','0','#'}
};
byte rowPins[ROWS] = {5, 4, 3, 2};
byte colPins[COLS] = {6, 7, 8};
Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

char password[] = {'1', '2', '3', '4'};
char c[4];
bool isOpen = false;
bool changingPass = false;
bool passAccepted = false;

void setup() {
  pinMode(11,OUTPUT);
  pinMode(12,OUTPUT);
  pinMode(13,OUTPUT);
  servo.attach(10);
  servo.write(0);
}
void loop(){
  for(int i = 0 ; i < 4 ; i++){
    c[i] = customKeypad.waitForKey();
    if(c[0] == '*'){
      changingPass = true;
      break;
    }
  }
  if(c[0]==password[0] && c[1]==password[1] && c[2]==password[2] && c[3]==password[3]){
    if(!changingPass){
      isOpen = true;
      digitalWrite(11, HIGH);
      digitalWrite(12, LOW);
      servo.write(90);
    }else{
      passAccepted = true;
    }
  }else if(!changingPass){
    isOpen = false;
    digitalWrite(11, LOW);
    digitalWrite(12, HIGH);
    servo.write(0);
    tone(13, 1000);
    delay(200);
    noTone(13);
  }else{
    if(passAccepted){
      password[0] = c[0];
      password[1] = c[1];
      password[2] = c[2];
      password[3] = c[3];
      passAccepted = false;
      changingPass = false;
    }
  }
}
