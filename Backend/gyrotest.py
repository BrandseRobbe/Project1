# import time
# from subprocess import call
# from Modules import mypyfluid  as pyfluidsynth
#
# print("Maak synth aan")
# fs = pyfluidsynth.Synth(gain=4)
# try:
#     print("Start synth")
#     fs.start(driver="alsa", midi_driver="alsa_seq")
#     print(call(["aconnect", "20:0", "128:0"]))
#     print("laad soundfond")
#     sfid1 = fs.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
#     print("program soundfont")
#     fs.program_select(0, sfid1, 0, 0)
#     fs.program_change(9, 1)
#
#     sfid2 = fs.sfload("/usr/share/sounds/sf2/STAIN_SOUNDFONT_gm.sf2")
#     fs.program_select(0, sfid2, 0, 0)
#     fs.program_change(9, 3)
#     print("speel noten")
#     while True:
#         for i in range(0,16):
#             print("channel: %s = %s"%(i, fs.channel_info(i)))
#             fs.program_change(i, 24)
#         # fs.cc(0,5,100)
#         # time.sleep(3)
#         # fs.cc(0,5,0)
#         # time.sleep(3.0)
#             time.sleep(1)
#
#
# finally:
#     fs.delete()
#
# # import threading
# # import time
# #
# # import array
# # import serial
# #
# # from Modules.SerialRaspberry import SerialRaspberry
# #
# # # serialData = serial.Serial('/dev/ttyACM0',115200)
# # data = SerialRaspberry(500000, '/dev/ttyACM0')
# #
# #
# # def lees_seriele_noten():
# #     print("start loop")
# #     while True:
# #         print(data.lees_bericht())
# #
# #
# # loop1 = threading.Thread(name="loop1", target=lees_seriele_noten)
# # loop1.daemon = True
# #
# # loop1.start()
# #
# # time.sleep(10)

import time

from numpy.ma import arange

from Modules.MPU9250 import MPU9250

mpu9250 = MPU9250()

try:
    max = 0
    min = 0
    while True:

        # gyro = mpu9250.readGyro()
        # waarde = gyro['z']
        # if waarde > max:
        #     max = waarde
        # if waarde < min:
        #     min = waarde
        # print(waarde)

        gyro = mpu9250.readGyro()

        if round(gyro['x']) in range(0,2):
            if gyro['x'] > 0:
                print(round(gyro['x'] * 123))
        #     waarde 0.0 - 1.023 omzetten naar cc val van

        # value from 0.0 - 1.0 -> cc vals

        # print(" gx = " , ( gyro['x'] ))
        # print(" gy = " , ( gyro['y'] ))
        # print(" gz = " , ( gyro['z'] ))



        time.sleep(0.3)

except KeyboardInterrupt as e:
    print(e)
    print("min: %s"%min)
    print("max: %s" % max)

