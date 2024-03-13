#include <Servo.h>
#include <Keyboard.h>

Servo Servo1;

int servoPin = 9;
int potPin = A0;


void setup() {
    Serial.begin(9600);
    Servo1.attach(servoPin);
}


void loop() {
      if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');
        int direction = input.toInt();
        Servo1.write(direction);
    }
}
