void setup() {
  Serial.begin(9600);
}

void loop() {
  static int count=0;
  Serial.println(String(count)+','+String(count)+','+String(count*2.0));
  count ++;
  if(count == 10)
    count = 0;
  delay(1000);
}
