import time
from subprocess import call
from Modules import mypyfluid  as pyfluidsynth

print("Maak synth aan")
fs = pyfluidsynth.Synth(gain=4)
try:
    print("Start synth")
    fs.start(driver="alsa", midi_driver="alsa_seq")
    print(call(["aconnect", "20:0", "128:0"]))
    print("laad soundfond")
    sfid1 = fs.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
    print("program soundfont")
    fs.program_select(0, sfid1, 0, 0)
    fs.program_change(0, 1)

    # sfid2 = fs.sfload("/usr/share/sounds/sf2/STAIN_SOUNDFONT_gm.sf2")
    # fs.program_select(0, sfid2, 0, 0)
    # fs.program_change(0, 3)
    print("speel noten")
    while True:
        fs.cc(0,5,100)
        time.sleep(3)
        fs.cc(0,5,0)
        time.sleep(3.0)


finally:
    fs.delete()

