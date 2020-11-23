#include <Servo.h>

Servo mServo;

int angle = 0;
int center_angle = 1795; //êÖïΩÇ…Ç»ÇÈäpìx
int center_psd = 12; //íÜêSà íu
int max_angle = 60;

int i = 0;
int p = center_psd;
float pp;

void setup() {
  mServo.attach(9);
  Serial.begin(9600);
  mServo.writeMicroseconds(center_angle);
}
int ps = 0;
void loop() {
  int v  = analogRead(0);
  float s = 4000.0 / (v + 1);
  float p = (s - center_psd);
  float d = -(p - pp);
  float angle = p * 5 + d * 20;
  if (angle < -max_angle)angle = -max_angle;
  if (angle > max_angle)angle = max_angle;
  mServo.writeMicroseconds(center_angle + (int)angle);
  Serial.println(String(p) + "\t" + String(pp) + "\t" + String(d) + "\t" + String(angle) + "\t" + String(s) + "\t" + String(v));
  pp = p;
  delay(10);
}
