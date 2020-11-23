void setup() {
  Serial.begin(9600);//シリアルモニタを使うための設定
  pinMode(2, INPUT_PULLUP);//デジタル2番ピンを入力に（何もつながっていない場合HIGH）
}

void loop() {
  int a, b;
  a = digitalRead(2);//デジタル2番ピンの値を読む
  b = analogRead(0);//アナログ0番ピンの値を読む
  Serial.print(a);//aの値をシリアルモニタに表示
  Serial.print("\t");//タブ文字を表示
  Serial.println(b);//bの値をシリアルモニタに表示して改行
  delay(500);
}
