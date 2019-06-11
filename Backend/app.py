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

current_userid = None


def lees_seriele_noten():
    print("start loop on noten te lezen")
    while True:
        # global current_userid
        # if data.lees_bericht() and current_userid is not None:
        #     print("update hiestoriek")
        #     conn.set_data(
        #         'update historiek set speeltijd = addtime(speeltijd, "00:01:00") where userid = %s and date(datum) = current_date()',
        #         [current_userid])
        #     time.sleep(60)

        print(data.lees_bericht())


# print(data.lees_bericht())


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


    knop = Button(16)
    rs_pin = 17
    e_pin = 27
    # datapinnen = [22, 5, 6, 13, 19, 26, 21, 20]
    datapinnen = [20, 21, 26, 19, 13, 6, 5, 22]
    # print(datapinnen[::-1])
    display = Lcd(datapinnen, rs_pin, e_pin)





    ip = check_output(['hostname', '--all-ip-addresses'])
    print(ip)
    ip = str(ip.split()[0]).strip("b").strip("'")
    display.write_message(ip)

    timer = False
    begintijd = ""


    def stuurtoestand(pin):
        print(knop.pressed)
        global timer
        global begintijd

        if knop.pressed:
            # timer = True
            begintijd = float(time.time())
            # print("Begintijd: %s"%begintijd)

        if not knop.pressed:
            # timer = False
            eindtijd = float(time.time())
            # print("Eindtijd: %s"%eindtijd)
            verschil = eindtijd - begintijd
            print(verschil)
            verschil = round(verschil, 2)
            print(verschil)
            socketio.emit("toestand", verschil)
            print("emit")
            nieuwe_gebeurtenis = conn.set_data(
                "INSERT INTO historiek (HistoriekID, UserID, Speeltijd) VALUES (NULL, %s, sec_to_time(%s));",
                [101, verschil])


    knop.on_action(stuurtoestand)


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


    @socketio.on("connect")
    def connecting():
        socketio.emit("connected")
        print("Connection with client established")


    @socketio.on("logout")
    def logout():
        global current_userid
        print("log user out")
        current_userid= None


    @socketio.on("effect_toepassen")
    def effect_toepassen(json_data):
        ccvals = json_data["ccvals"]

        fs.system_reset()
        for cc, val in json_data["ccvals"].items():
            fs.cc(0, int(cc), val)

    print("start loop")
    loop1 = threading.Thread(name="loop1", target=lees_seriele_noten)
    loop1.daemon = True
    loop1.start()

    if __name__ == '__main__':
        socketio.run(app, host="0.0.0.0", port=5000)

except Exception as e:
    print(e)
    print("Er ging iets mis, herstart het programma")
finally:
    GPIO.cleanup()
