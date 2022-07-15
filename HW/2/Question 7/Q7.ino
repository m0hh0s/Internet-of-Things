/*************************************************************
  

  Rotate a servo using a slider!

  App project setup:
    Slider widget (0...180) on V0
 *************************************************************/

// Template ID, Device Name and Auth Token are provided by the Blynk.Cloud
// See the Device Info tab, or Template settings
#define BLYNK_TEMPLATE_ID           "TMPL6oL2KxHy"
#define BLYNK_DEVICE_NAME           "Quickstart Device"
#define BLYNK_AUTH_TOKEN            "QThp1fE5APkqcoJW4q3GRv4DDoomCb6q"


// Comment this out to disable prints and save space
#define BLYNK_PRINT SwSerial


#include <SoftwareSerial.h>
SoftwareSerial SwSerial(10, 11); // RX, TX

#include <BlynkSimpleStream.h>
#include <Servo.h>

char auth[] = BLYNK_AUTH_TOKEN;

Servo servo;

BLYNK_WRITE(V0)
{
  servo.write(param.asInt());
}

void setup()
{
  // Debug console
  SwSerial.begin(115200);

  // Blynk will work through Serial
  // Do not read or write this serial manually in your sketch
  Serial.begin(9600);
  Blynk.begin(Serial, auth);

  servo.attach(9);
}

void loop()
{
  Blynk.run();
}
