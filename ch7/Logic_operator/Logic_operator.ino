boolean in0 = false;
boolean in1 = false;
boolean in2 = false;
boolean out0 = false;
boolean out1 = false;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP); // 入力モードでプルアップ抵抗を有効に
  pinMode(3, INPUT_PULLUP); // 同様
  pinMode(4, INPUT_PULLUP); // 同様
  pinMode(5, INPUT_PULLUP); // 同様
  pinMode(6, INPUT_PULLUP); // 同様
  pinMode(7, INPUT_PULLUP); // 同様
  pinMode(8, OUTPUT); // 出力モードに
  pinMode(9, OUTPUT); // 同様
  pinMode(10, OUTPUT); // 同様
  pinMode(11, OUTPUT); // 同様
  pinMode(12, OUTPUT); // 同様
}

void loop() {
  if (digitalRead(2) == LOW) {//送信スイッチ
    int out = out0 + out1 * 2;
    Serial.println(String(in0) + "," + String(in1) + "," + String(in2) + "," + String(out));
  }
  else if (digitalRead(3) == LOW) {//左の入力LEDの反転
    in0 = !in0;
  }
  else if (digitalRead(4) == LOW) {//中央の入力LEDの反転
    in1 = !in1;
  }
  else if (digitalRead(5) == LOW) {//右の入力LEDの反転
    in2 = !in2;
  }
  else if (digitalRead(6) == LOW) {//1ビット目の出力LEDの反転
    out0 = !out0;
  }
  else if (digitalRead(7) == LOW) {//2ビット目の出力LEDの反転
    out1 = !out1;
  }
  digitalWrite(8, in0);//LEDの点灯と消灯
  digitalWrite(9, in1);
  digitalWrite(10, in2);
  digitalWrite(11, out0);
  digitalWrite(12, out1);

  delay(500);
}
