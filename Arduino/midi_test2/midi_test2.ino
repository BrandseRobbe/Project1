#include <frequencyToNote.h>
#include <MIDIUSB.h>
// #include <MIDIUSB_Defs.h>
#include <pitchToFrequency.h>
#include <pitchToNote.h>

#include "MIDIUSB.h"


const int softpot1 = A0;
const int softpot2 = A1;
const int psr1 = A2;
const int psr2 = A3;
int waarde = 0;
void setup() {


  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  float positie1 = analogRead(softpot1);
  int positie = floor((positie1 / 1023) * 19);

  if ( waarde != positie) {
    waarde = positie;
    Serial.println("Speel noot: "+ String(positie+60));
    noteOn(1, 60+positie, 64);
    delay(100);
    noteOff(1, 60+positie, 64);
  }
}

void noteOn(byte channel, byte pitch, byte velocity) {
  midiEventPacket_t noteOn = {0x09, 0x90 | channel, pitch, velocity};
  MidiUSB.sendMIDI(noteOn);
}

void noteOff(byte channel, byte pitch, byte velocity) {
  midiEventPacket_t noteOff = {0x08, 0x80 | channel, pitch, velocity};
  MidiUSB.sendMIDI(noteOff);
}

void controlChange(byte channel, byte control, byte value) {
  midiEventPacket_t event = {0x0B, 0xB0 | channel, control, value};
  MidiUSB.sendMIDI(event);
}
