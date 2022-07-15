#include <HCSR04.h>

const byte triggerPin = 7;
const byte echoPin = 6;
UltraSonicDistanceSensor distanceSensor(triggerPin, echoPin);

// Template ID, Device Name and Auth Token are provided by the Blynk.Cloud
// See the Device Info tab, or Template settings
#define BLYNK_TEMPLATE_ID           "TMPL6oL2KxHy"
#define BLYNK_DEVICE_NAME           "Quickstart Device"
#define BLYNK_AUTH_TOKEN            "g7e4yzaMToEEwaW86tDwmmQ7OT5ZfR-D"


// Comment this out to disable prints and save space
#define BLYNK_PRINT SwSerial


#include <SoftwareSerial.h>
SoftwareSerial SwSerial(10, 11); // RX, TX

#include <BlynkSimpleStream.h>

char auth[] = BLYNK_AUTH_TOKEN;

BlynkTimer timer;

// This function sends Arduino's up time every second to Virtual Pin (5).
// In the app, Widget's reading frequency should be set to PUSH. This means
// that you define how often to send data to Blynk App.
void myTimerEvent()
{
  // You can send any value at any time.
  // Please don't send more that 10 values per second.
  int distance = distanceSensor.measureDistanceCm() + 1;
  Blynk.virtualWrite(V0, distance);
  if(distance < 10){
    Blynk.virtualWrite(V1, HIGH);
  }
}

void setup()
{
  // Debug console
  SwSerial.begin(115200);

  // Blynk will work through Serial
  // Do not read or write this serial manually in your sketch
  Serial.begin(9600);
  Blynk.begin(Serial, auth);

  // Setup a function to be called every second
  timer.setInterval(1000L, myTimerEvent);
}

void loop()
{
  Blynk.run();
  timer.run(); // Initiates BlynkTimer
}
