#include <Servo.h>

Servo mServo;//サーボモータ用の設定

void setup() {
  Serial.begin(9600);
  mServo.attach(9);//9番ピンでサーボモータを動かす
  pinMode(2, INPUT_PULLUP); // Inputモードでプルアップ抵抗を有効に
  pinMode(LED_BUILTIN, OUTPUT);
  mServo.write(10);
  digitalWrite(LED_BUILTIN, HIGH);
}
 
void loop(){
  static int flag=0;
  if(digitalRead(2)==LOW){
    flag=1;
  }
  else{
    if(flag==1){
      flag=0;
      Serial.write('1');
      delay(500);
    }
  }
  if(Serial.available()>0){
    char a = Serial.read();
    if(a=='o'){
      mServo.write(10);
      digitalWrite(LED_BUILTIN, HIGH);
    }
    else if(a=='c'){
      mServo.write(100);
      digitalWrite(LED_BUILTIN, LOW);
    }
  }
}
