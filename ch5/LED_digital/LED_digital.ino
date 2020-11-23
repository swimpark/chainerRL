void setup() {//一度だけ実行される
  pinMode(LED_BUILTIN, OUTPUT);//Arduinoボードに付いているLEDを出力に
}

void loop() {//何度も繰り返し実行される
  digitalWrite(LED_BUILTIN, HIGH);//LEDを光らせる
  delay(1000);//1000ミリ秒待つ
  digitalWrite(LED_BUILTIN, LOW);//LEDを消す
  delay(1000);//1000ミリ秒待つ
}
