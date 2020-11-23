#include <Servo.h>

Servo mServo;//サーボモータを使うための設定

void setup() {
  pinMode(9, OUTPUT);
  mServo.attach(9);//デジタル9番ピンをサーボモータに使う
}

void loop() {
  int v = analogRead(0);//値を読み取る
  v = map(v, 0, 1023, 0, 180);//値の変更
  mServo.write(v);//サーボモータを回す
  delay(20);
}

