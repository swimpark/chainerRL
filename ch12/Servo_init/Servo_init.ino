#include <Servo.h>

Servo mServo;

int center_angle = 1575;

void setup() {
  mServo.attach(9);
  mServo.writeMicroseconds(center_angle);
}

void loop() {
}
