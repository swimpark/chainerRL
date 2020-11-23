void setup() {
  Serial.begin(9600);
  pinMode(9, OUTPUT);
}

void loop() {
  if(Serial.available()>0){
    long int v = Serial.parseInt();
    analogWrite(9, v);
  }
}
