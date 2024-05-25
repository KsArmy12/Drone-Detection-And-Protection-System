#include <Servo.h>

// Define the servo objects
Servo servoX;
Servo servoY;

// Define the pins for the servos and the laser module
const int servoXPin = 9;
const int servoYPin = 10;
const int laserPin = 11;

// Variables to store the angles
int angleX = 90;  // Default to 90 degrees (middle position)
int angleY = 90;

// Variable to store incoming serial data
String incomingData = "";

// Timer variables for the laser
unsigned long lastDataTime = 0;
const unsigned long timeout = 1000;  // 1 second timeout

void setup() {
  // Attach the servos to the pins
  servoX.attach(servoXPin);
  servoY.attach(servoYPin);

  // Set the laser pin as output
  pinMode(laserPin, OUTPUT);
  digitalWrite(laserPin, LOW);  // Turn off the laser initially

  // Start serial communication
  Serial.begin(9600);
}

void loop() {
  // Check if data is available on the serial port
  if (Serial.available() > 0) {
    // Read the incoming data
    char inChar = (char)Serial.read();
    incomingData += inChar;

    // Check for the end of the line
    if (inChar == '\n') {
      // Process the data
      parseData(incomingData);

      // Clear the incoming data string
      incomingData = "";

      // Update the last data time
      lastDataTime = millis();

      // Turn on the laser
      digitalWrite(laserPin, HIGH);
    }
  }

  // Check for timeout
  if (millis() - lastDataTime > timeout) {
    // Turn off the laser if timeout has occurred
    digitalWrite(laserPin, LOW);
  }

  // Update the servo positions
  servoX.write(angleX);
  servoY.write(angleY);
}

void parseData(String data) {
  // Split the data into angles
  int commaIndex = data.indexOf(',');
  if (commaIndex > 0) {
    String angleXString = data.substring(0, commaIndex);
    String angleYString = data.substring(commaIndex + 1);

    // Convert the strings to integers
    angleX = angleXString.toInt();
    angleY = angleYString.toInt();
  }
}
