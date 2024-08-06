#include <Servo.h>

// Create Servo objects
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

void setup() {
  // Attach the servos to their respective pins
  servo1.attach(6);
  servo2.attach(5);
  servo3.attach(4);
  servo4.attach(3);

  // Start serial communication
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char wasteType = Serial.read();
    switch (wasteType) {
      case 'R':
        servo4.write(90); // Recyclable waste (pin 3)
        delay(1000);
        servo4.write(0);
        break;
      case 'H':
        servo3.write(90); // Hazardous waste (pin 4)
        delay(1000);
        servo3.write(0);
        break;
      case 'F':
        servo2.write(90); // Food waste (pin 5)
        delay(1000);
        servo2.write(0);
        break;
      case 'N':
        servo1.write(90); // Residual waste (pin 6)
        delay(1000);
        servo1.write(0);
        break;
      default:
        break;
    }
  }
}