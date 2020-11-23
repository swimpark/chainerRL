void setup() {
  pinMode(9, OUTPUT);//デジタル9番ピンを出力に
}

void loop() {
  for(int i=0;i<256;i++){
    analogWrite(9, i);//iの値に従って明るさを設定
    delay(10);
  }
}

