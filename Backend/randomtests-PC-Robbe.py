import time
from subprocess import check_output

import fluidsynth


def print_intput(tekst):
    pass


# fs = fluidsynth.Synth()
# fs.start()
print("ik geraak hier")
# inputs = check_output("fluidsynth -a alsa -m alsa_seq -g 1.0 -s /usr/share/sounds/sf2/FluidR3_GM.sf2".split())
# print_intput('en hier')
# print("lijn 1: %s" % inputs.decode('UTF-8'))

# inputs2 = check_output("^Z")
# print("lijn 2: %s" % inputs2.decode('UTF-8'))


# test2 = check_output("aconnect 20:0 128:0".split())
# print(test2.decode('UTF-8'))

inputs3 = check_output("fg".split())
print("lijn 3: %s" % inputs3.decode('UTF-8'))
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt as e:
    print_intput(e)
finally:
    check_output("exit".split())
    # fs.delete()
