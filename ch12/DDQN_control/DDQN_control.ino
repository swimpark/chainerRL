#include <Servo.h>

Servo mServo;

int angle = 0;
int center_angle = 1575;
int max_angle = 60;
float reward = 0;
int count = -1;
float old_p;
boolean end_flag = false;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  mServo.attach(9);
  Serial.begin(9600);
  mServo.writeMicroseconds(center_angle);
}

void loop() {
  if (Serial.available() > 0) {
    end_flag = false;
    char c = Serial.read();
    if (c == 'a') {
      digitalWrite(LED_BUILTIN, HIGH);
      for (int a = angle; a < max_angle-30; a++) {
        mServo.writeMicroseconds(a + center_angle);
        delay(10);
      }
      angle = max_angle-30;
      delay(2000);
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("b");
    }
    else {
      if (c == '0') {
        angle -= 5;
      }
      else if (c == '1') {
        angle -= 1;
      }
      else if (c == '2') {
        angle += 0;
      }
      else if (c == '3') {
        angle += 1;
      }
      else if (c == '4') {
        angle += 5;
      }
      if (angle < -max_angle) {
        angle = -max_angle;
        end_flag = true;
      }
      if (angle > max_angle) {
        angle = max_angle;
        end_flag = true;
      }
      mServo.writeMicroseconds(angle + center_angle);
      count = 10;
      old_p = 4000.0 / (analogRead(0) + 1);
    }
    reward = 0;
  }
  else {
    int val = analogRead(1);
    if (val > 550)
      reward += 1.0;
  }

  if (count == 0) {
    float p = 4000.0 / (analogRead(0) + 1);
    if (end_flag == true)reward = -1;
    Serial.println(String(p) + "," + String(old_p - p) + "," + String(angle) + "," + String(reward));
    count = -1;
  }
  else if (count > 0) {
    count--;
  }
  delay(1);
}
