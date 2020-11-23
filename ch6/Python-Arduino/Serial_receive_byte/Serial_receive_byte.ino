void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if(Serial.available()>0){
    char c = Serial.read();
    if(c=='a')
          digitalWrite(LED_BUILTIN,HIGH);
    else if(c=='b')
          digitalWrite(LED_BUILTIN,LOW);
  }
}
