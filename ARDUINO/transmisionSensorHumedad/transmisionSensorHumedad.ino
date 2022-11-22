int out1 = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  out1 = analogRead(A0);
  Serial.println(out1);
  delay(100);
} 
