void setup() {
  Serial.begin(115200);
  pinMode(2, INPUT_PULLUP);
}

void loop() {
  static int count = 0;
  if (count == 0) {
    if (digitalRead(2) == LOW) {
      count = 50;
      Serial.println("a");
    }
  }
  else {
    count--;
    Serial.print(analogRead(0));
    Serial.print(",");
    Serial.print(analogRead(1));
    Serial.print(",");
    Serial.println(analogRead(2));
    delay(10);
  }
}
