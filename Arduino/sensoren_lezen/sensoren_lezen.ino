const int softpot1 = A0;
const int softpot2 = A1;
const int psr1 = A2;
const int psr2 = A3;
int waarde = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  
}

void loop() {
  float positie1 = analogRead(softpot1);
  positie1 = floor((positie1 /1023) * 19);
  Serial.println(positie1);
  float druk1 = analogRead(psr1);
  Serial.println(druk1);
  
  
  delay(10);
  }
