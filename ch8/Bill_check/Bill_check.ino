const int MaxPoint = 4;
int dd[MaxPoint];
int dn;
boolean rf;
int ss;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP); // インプットプルアップ
  pinMode(3, INPUT_PULLUP); // 同様
  pinMode(4, INPUT_PULLUP); // 同様
  pinMode(5, INPUT_PULLUP); // 同様
  pinMode(6, INPUT_PULLUP); // 同様
  dn = 0;
  rf = true;
  ss = -1;
}

void loop() {
  if (digitalRead(2) == LOW) {
    rf = false;
    delay(100);
  }
  else {
    if (rf == false) { //ボタンが離されたら
      rf = true;//次のボタンが押されたら
      int v = analogRead(0);
      dd[dn] = v;//データを配列に
      dn ++;
      if (dn == MaxPoint) { //5個のデータを読み取ったら
        for (int i = 0; i < MaxPoint; i++)
          Serial.print(String(dd[i]) + ","); //データの送信
        Serial.println(ss);//最後にお札の種類と改行コードを送信
        dn = 0;
      }
    }
  }
  if (digitalRead(3) == LOW) {
    ss = 0;//お札の種類
    dn = 0;//読み込んだデータ数を0に
  }
  else if (digitalRead(4) == LOW) {
    ss = 1;
    dn = 0;
  }
  else if (digitalRead(5) == LOW) {
    ss = 2;
    dn = 0;
  }
  else if (digitalRead(6) == LOW) {
    ss = 3;
    dn = 0;
  }
}
