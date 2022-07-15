void setup() {
  Serial.begin(9600);
  pinMode(11, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(6, OUTPUT);
}

void loop(){
  if(Serial.available()>0){
    char message = Serial.read();
    if (message == '1'){
      analogWrite(11, 50);
      analogWrite(10, 0);
    }else if (message == '2'){
      analogWrite(9, 50);
      analogWrite(6, 0);
    }else if (message == '3'){
      analogWrite(11, 0);
      analogWrite(10, 50);
    }else if (message == '4'){
      analogWrite(9, 0);
      analogWrite(6, 50);
    }else if (message == '5'){
      analogWrite(11, 255);
      analogWrite(10, 0);
    }else if (message == '6'){
      analogWrite(9, 255);
      analogWrite(6, 0);
    }else if (message == '7'){
      analogWrite(11, 0);
      analogWrite(10, 255);
    }else if (message == '8'){
      analogWrite(9, 0);
      analogWrite(6, 255);
    }else if (message == '9'){
      analogWrite(11, 255);
      analogWrite(10, 0);
      analogWrite(9, 255);
      analogWrite(6, 0);
    }else if (message == '0'){
      analogWrite(11, 0);
      analogWrite(10, 255);
      analogWrite(9, 0);
      analogWrite(6, 255);
    }else if (message == '*'){
      analogWrite(11, 0);
      analogWrite(10, 0);
    }else if (message == '#'){
      analogWrite(9, 0);
      analogWrite(6, 0);
    } 
  }
  delay(500);
}
