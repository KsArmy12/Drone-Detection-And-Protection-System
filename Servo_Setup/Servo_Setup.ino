#include <Servo.h>

Servo myServo;  // Create a servo object to control the servo

void setup() {
  myServo.attach(3);  // Attach the servo to pin 9
}

void loop() {
    myServo.write(180);
    delay(1000);
    // myServo.write(90);
    // delay(1000);
    // myServo.write(180);
    // delay(1000);
}
