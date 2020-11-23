#include <Servo.h>

Servo mServo;

int center_angle = 1575;
int max_angle = 60;

void setup() {
  mServo.attach(9);
  mServo.writeMicroseconds(center_angle);
}
void loop() {
  int val;
  val = (analogRead(2)-512)/5;
  if (val < -max_angle)val = -max_angle;
  if (val > max_angle)val = max_angle;

  mServo.writeMicroseconds(val + center_angle);
}
