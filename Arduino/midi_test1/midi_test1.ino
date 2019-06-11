#include <frequencyToNote.h>
#include <MIDIUSB.h>
#include <MIDIUSB_Defs.h>
#include <pitchToFrequency.h>
#include <pitchToNote.h>

#include "MIDIUSB.h"

void setup() {
  // put your setup code here, to run once:
  Serial.begin(500000);
}

void loop() {
  // put your main code here, to run repeatedly:
  noteOn(0,62, 60);
  noteOn(0,65, 60);
  noteOn(0,69, 60);
  delay(300);
  noteOff(0,62, 60);
  noteOff(0,65, 60);
  noteOff(0,69, 60);
  delay(300);
  

}

void noteOn(byte channel, byte pitch, byte velocity) {
  midiEventPacket_t noteOn = {0x09, 0x90 | channel, pitch, velocity};
  MidiUSB.sendMIDI(noteOn);
  Serial.println("G");
  MidiUSB.flush();
}

void noteOff(byte channel, byte pitch, byte velocity) {
  midiEventPacket_t noteOff = {0x08, 0x80 | channel, pitch, velocity};
  MidiUSB.sendMIDI(noteOff);
  MidiUSB.flush();
}

void controlChange(byte channel, byte control, byte value) {
  midiEventPacket_t event = {0x0B, 0xB0 | channel, control, value};
  MidiUSB.sendMIDI(event);
}
