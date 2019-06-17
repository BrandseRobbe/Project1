# Project1
My final project for the first year of NMCT

It's called the Sensonizer. It's an synthesizer based on sensors.
If you want to remake this project the same way I did, check out this instructable I made:
[https://www.instructables.com/id/The-SENSONIZER-a-DIY-Synthesizer/](https://www.instructables.com/id/The-SENSONIZER-a-DIY-Synthesizer/) 

In order to remake this project, you need at least a basic understanding of:
- Synthesizers and MIDI
- Arduino IDE 
- Flask or Socketio
 
## The structure
    
An Arduino Leonardo that'll act as an MIDI input device
    
I used an Raspberry Pi to run:
- Python flask webserver
- MardiaDB database     
- Fluidsynth synthesizer
- Apache2 http server
    
## Arduino code

The Arduino code is pretty simple, I use analogRead() to get the values from both of my sensors. Then I put these values in a function that will play the right note.

    const int s1presure = A1;
    const int s1position = A0;
    vorige_key_value_1 = speel_strip(int(analogRead(s1presure)), int(analogRead(s1position)), vorige_key_value_1);
 
Now we need to know how to play notes, to do this we need the MIDIUSB library
    
    #include <MIDIUSB.h>

    //these are the requirements to play a note
    noteOn(byte channel, byte pitch, byte velocity)

    //these are the requirements to stop playing a note.
    noteOff(byte channel, byte pitch, byte velocity)
 
The rest of the code transforms the variable values from the sensors to a new range, and making sure it doesn't keep playing the same note when you hold it down.

One important thing to note, normally  you can set the velocity of a note between 0 -255 , but the synthesizer software that I'll use in the back-end only handles velocities between 0 -130.

## Back-end code: Python
I wrote this code using Pycharm and I recommend that you do the same, it'll do a lot of the database commands for you, and has great debugging tools.


Most of the back-end code is a farely  standard fask project.
The most important code that stands out is the API to control the fluidsynth synthesizer software.

```
    # start the fluidsynth software with the best drivers (from my experience)
    fs.start(driver="alsa", midi_driver="alsa_seq")

    # connect the Arduino (that is recognized as an midi input device) to the fluidsynth output.
    call(["aconnect", "20:0", "128:0"])

    # Load a soundfont I used the default one that came with the software. 
    # But you can easily download a new one and replace the path
    sfid1 = fs.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
    
    # select which soundfont to use
    fs.program_select(0, sfid1, 0, 0)

    # change the intrument sound
    fs.program_change(0, 1)

    # change the effect, in this case it'll add a vibrato effect
    fs.cc(0, 1, 50)
```
# Extra Tip
I had a lot of trouble getting the fluidsynth API to work.
Here's the original repo for the library: [https://github.com/nwhitehead/pyfluidsynth](https://github.com/nwhitehead/pyfluidsynth)

But if i followed their steps on installing it, I just couldn't get it to work

So this is how i did it:
- I copied the code from [here](https://github.com/nwhitehead/pyfluidsynth/blob/master/fluidsynth.py)
- Created a new python package called mypyfluid
- Made a new python file: [`__init__.py`](https://github.com/RobbeBrandse/Project1/blob/master/Backend/Modules/mypyfluid/__init__.py) and pasted the code there
- Added this line `from Modules import mypyfluid  as pyfluidsynth`

After this it should work just fine.