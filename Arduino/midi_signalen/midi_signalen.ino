#include <MIDIUSB.h>

//strip1
const int s1presure = A1;
const int s1position = A0;

//strip2
const int s2presure = A2;
const int s2position = A3;

int vorige_key_value_1 = 0;
int vorige_key_value_2 = 0;

void setup() {
  Serial.begin(500000);
}

void loop() {

  //int waarden[2] = {int(analogRead(s1t)), int(analogRead(s1p))};
  vorige_key_value_1 = speel_strip(int(analogRead(s1presure)), int(analogRead(s1position)), vorige_key_value_1);

  //vorige_key_value_2 = speel_strip(int(analogRead(s2presure)), int(analogRead(s2position)), vorige_key_value_2);

  //Serial.println(String(1023 - analogRead(s1presure)) + ": druk, " + String(analogRead(s1position)) + " :positie");
  //Serial.println(String(analogRead(s2presure)) + ": druk, "+String(analogRead(s2position))+" :positie");
  //Serial.println();
  MidiUSB.flush();
  delay(50);
}

int speel_strip(int presure_val, int position_val, int last_value) {
  int vorige_key_value = last_value;
  int waarden[2] = {presure_val, position_val};
  int key_value = 0;
  if (waarden[0] < 655) {
    //midi signalen sturen van 45 tot 67 -> 20 noten range
    key_value = round((waarden[1] * 20 / 655) + 45);

    if (key_value != vorige_key_value) {
      // snelheid waarop knop ingedrukt wordt berekenen
      int pressure = 1024 - analogRead(s1presure);
      // waarde van 0-1023 omzetten naar een waarde van 10-130 normaal kan een synthesiser snelheiden krijgen van 0 - 255, maar fluidsynth niet.
      int velocity = map(pressure, 0, 1023, 10, 130);
      //Serial.println(velocity);

      noteOff(0, vorige_key_value, velocity);
      noteOn(0, key_value, velocity);
      //vorige_key_value = key_value;
    }
  }
  else {
    if (vorige_key_value != 0) {
      noteOff(0, vorige_key_value, 60);
      key_value = 0;
    }
  }
  return key_value;
}

void noteOn(byte channel, byte pitch, byte velocity) {
  midiEventPacket_t noteOn = {0x09, 0x90 | channel, pitch, velocity};
  MidiUSB.sendMIDI(noteOn);
  //Serial.println("GO");
  Serial.println(String(pitch) + " " + String(velocity));
  //MidiUSB.flush();
}

void noteOff(byte channel, byte pitch, byte velocity) {
  midiEventPacket_t noteOff = {0x08, 0x80 | channel, pitch, velocity};
  MidiUSB.sendMIDI(noteOff);
  //Serial.println(String(pitch) + "uit");
  //MidiUSB.flush();
}

void controlChange(byte channel, byte control, byte value) {
  midiEventPacket_t event = {0x0B, 0xB0 | channel, control, value};
  MidiUSB.sendMIDI(event);
}
