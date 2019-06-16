# Imports
import threading
import time
from subprocess import check_output
from subprocess import call

import hashlib

from Modules import mypyfluid  as pyfluidsynth
from RPi import GPIO
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import numpy

# from Database.DP1Database import Database
from Modules.DP1Database import Database
from Modules.Button import Button
from Modules.Lcd import Lcd
from Modules.MPU9250 import MPU9250
from Modules.SerialRaspberry import SerialRaspberry

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

conn = Database(app=app, user='mct', password='mct', db='Project1', host='localhost', port=3306)
endpoint = '/api/v1'
GPIO.setmode(GPIO.BCM)
# print("Maak synth aan")
fs = pyfluidsynth.Synth(gain=3)

data = SerialRaspberry(500000, '/dev/ttyACM0')
mpu9250 = MPU9250()

current_userid = None


def lees_seriele_noten():
    while True:
        # print("start loop on noten te lezen")
        global current_userid
        if data.lees_bericht() and current_userid is not None:
            print("update hiestoriek")
            conn.set_data(
                'update historiek set speeltijd = addtime(speeltijd, "00:00:10") where userid = %s and date(datum) = current_date()',
                [current_userid])
            geschiedenis()
            time.sleep(10)
        time.sleep(0.05)


def lees_gyro():
    while True:
        # print("lees gyro")
        time.sleep(0.05)
        data.lees_bericht()  # seriele communicatie door doorschuiven -> anders stapelen ze op en is het dus geen live data meer
        gyro = mpu9250.readGyro()

        if round(gyro['x']) in range(0, 2):
            if gyro['x'] > 0 and gyro['x'] < 1.023:
                ccval = round(gyro['x'] * 123)
                print("ccval = %s" % ccval)
                fs.cc(0, 1, ccval)


try:
    print("Start synth")
    fs.start(driver="alsa", midi_driver="alsa_seq")
    call(["aconnect", "20:0", "128:0"])
    print("laad soundfond")
    sfid1 = fs.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
    print("program soundfont")
    fs.program_select(0, sfid1, 0, 0)

    print("program change")
    fs.program_change(0, 1)

    rs_pin = 17
    e_pin = 27
    # datapinnen = [22, 5, 6, 13, 19, 26, 21, 20]
    datapinnen = [20, 21, 26, 19, 13, 6, 5, 22]
    # print(datapinnen[::-1])
    display = Lcd(datapinnen, rs_pin, e_pin)

    ip1 = check_output(['sudo', 'hostname', '--all-ip-addresses']).decode('UTF-8').split(" ")
    ip = ip1[0]
    if ip == '169.254.10.1' or ip == '169.254.14.33':
        ip = ip1[1]
    # import socket
    #
    # time.sleep(5)
    # testIP = "8.8.8.8"
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect((testIP, 0))
    # ip = s.getsockname()[0]
    # print(ip)

    display.displayOn(1, 1)
    display.write_message("IP-adres:")
    display.enter()
    display.write_message(ip)


    def h5(pw):
        return hashlib.md5(pw).hexdigest()


    @app.route(endpoint + '/testconnectie', methods=["GET"])
    def testconnectie():
        if request.method == "GET":
            return jsonify(message='geconnecteerd')


    @app.route(endpoint + '/register', methods=["POST", "GET"])
    def register():
        print('register attempt')
        if request.method == "GET":
            return jsonify(message='geconnecteerd')
        if request.method == "POST":
            print("POST")
            jsondata = request.get_json()
            print(jsondata)
            hashpw = hashlib.md5(str(jsondata["passwoord"]).encode()).hexdigest()

            print("INSERT INTO users (Email, Password) VALUES ('%s', '%s');" % (str(jsondata["email"]), hashpw))

            nieuwe_gebruiker = conn.set_data("INSERT INTO users (Email, Password) VALUES (%s, %s);",
                                             [str(jsondata["email"]), hashpw])

            print(nieuwe_gebruiker)
            if type(nieuwe_gebruiker) is int:
                output = nieuwe_gebruiker
            else:
                output = False
            return jsonify(output)


    @app.route(endpoint + '/login', methods=['POST'])
    def login():
        if request.method == "POST":
            jsondata = request.get_json()
            hashpw = hashlib.md5(str(jsondata["passwoord"]).encode()).hexdigest()
            print("select * from users where email = %s and password = '%s' " % (jsondata["email"], hashpw))

            user = conn.get_data("select * from users where email = %s and password = %s ",
                                 [jsondata["email"], hashpw])

            print(user)
            if user:
                # user is toegelaten
                userid = user[0]["UserID"]
                # controleren of nieuwe historiek record aangemaakt moet worden
                historiek_controle = conn.get_data(
                    "SELECT * FROM historiek where userid = %s and date(datum) = current_date()", [userid])

                if historiek_controle:
                    print("Hiestoriek bestaat al")
                else:
                    # print("maak een nieuwe historiek aan")
                    conn.set_data("INSERT INTO historiek (UserID) VALUES (%s);", [userid])

                output = userid
                global current_userid
                current_userid = userid

            else:
                output = False

            print(output)
            return jsonify(output)


    @app.route('/shutdown')
    def shutdown():
        print('shutdown now')
        GPIO.cleanup()
        fs.delete()
        call("sudo shutdown -h now".split())
        return jsonify(messag='Apparaat is zodadelijk afgesloten en veilig om te verwijderen'), 200

    @socketio.on('getgeschiedenis')
    def geschiedenis():
        global current_userid
        print(current_userid)
        user_geschiedenis = conn.get_data(
            'SELECT concat(Date(Datum)) as datum, concat(Speeltijd) as speeltijd, concat((hour(speeltijd)*60) + Minute(Speeltijd)) as minuten FROM historiek where userid = %s order by datum desc limit 7',
            [current_userid])
        # print(user_geschiedenis)
        print(user_geschiedenis)
        socketio.emit("setgeschiedenis", user_geschiedenis)


    @socketio.on("connect")
    def connecting():
        socketio.emit("connected")
        print("Connection with client established")


    @socketio.on("logout")
    def logout():
        global current_userid
        print("log user out")
        current_userid = None


    @socketio.on("setuser")
    def setuser(userid):
        global current_userid
        print("userid = %s" % userid)
        current_userid = userid


    @socketio.on("effect_toepassen")
    def effect_toepassen(json_data):
        fs.system_reset()
        print(json_data)
        ccvals = json_data["ccvals"]
        fs.program_change(0, int(json_data["sfnummer"]))
        print("change to inst: %s" % json_data["sfnummer"])

        for cc, val in json_data["ccvals"].items():
            fs.cc(0, int(cc), val)


    print("start loop: noten lezen")
    loop1 = threading.Thread(name="loop1", target=lees_seriele_noten)
    loop1.daemon = True
    loop1.start()

    print("start loop: gyro lezen")
    loop2 = threading.Thread(name="loop2", target=lees_gyro)
    loop2.daemon = True
    loop2.start()

    if __name__ == '__main__':
        socketio.run(app, host="0.0.0.0", port=5000)

except Exception as e:
    print(e)
    print("Er ging iets mis, herstart het programma")
finally:
    GPIO.cleanup()
    fs.delete()
