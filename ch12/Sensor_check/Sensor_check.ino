void setup() {
  Serial.begin(9600);
}

void loop() {
  float val0 = 4000.0/(analogRead(0)+1);
  int val1 = analogRead(1);
  int val2 = analogRead(2);
  Serial.println(String(val0)+"\t"+String(val1)+"\t"+String(val2));
  delay(100);
}
