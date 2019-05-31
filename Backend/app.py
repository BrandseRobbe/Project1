# Imports
import time
from subprocess import check_output

import socketio
from RPi import GPIO
from flask import Flask, request, jsonify, json
from flask_socketio import SocketIO
from flask_cors import CORS

# from Database.DP1Database import Database
from Database.DP1Database import Database
from GPIONMCT.Button import Button
from GPIONMCT.Lcd import Lcd

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

conn = Database(app=app, user='mct', password='mct', db='Project1', host='localhost', port=3306)
endpoint = '/api/v1'
GPIO.setmode(GPIO.BCM)
try:
    knop = Button(16)
    rs_pin = 17
    e_pin = 27
    # datapinnen = [22, 5, 6, 13, 19, 26, 21, 20]
    datapinnen = [20, 21, 26, 19, 13, 6, 5, 22]
    # print(datapinnen[::-1])
    display = Lcd(datapinnen, rs_pin, e_pin)
    display.displayOn(1,1)
    display.write_message("ip-adres: ")
    display.enter()
    # ip adres ophalen en in een string steken
    ip = check_output(['hostname', '--all-ip-addresses'])
    ip = str(ip.split()[-2]).strip("b").strip("'")
    display.write_message(ip)

    timer = False
    begintijd = ""


    def stuurtoestand(pin):
        print(knop.pressed)
        global timer
        global begintijd

        if knop.pressed == True:
            # timer = True
            begintijd = float(time.time())
            # print("Begintijd: %s"%begintijd)

        if knop.pressed == False:
            # timer = False
            eindtijd = float(time.time())
            # print("Eindtijd: %s"%eindtijd)
            verschil = eindtijd - begintijd
            print(verschil)
            verschil = round(verschil, 2)
            print(verschil)
            nieuwe_gebeurtenis = conn.set_data("INSERT INTO historiek (HistoriekID, UserID, Speeltijd) VALUES (NULL, %s, sec_to_time(%s));",[101,verschil])
            socketio.emit("toestand", verschil)


    knop.on_action(stuurtoestand)


    @app.route(endpoint + '/testconnectie', methods=["GET"])
    def testconnectie():
        if request.method == "GET":
            return jsonify(message='geconnecteerd')


    @socketio.on("connect")
    def connecting():
        socketio.emit("connected")
        print("Connection with client established")

        # randomdata = conn.get_data("select * from users")
        # print(randomdata)
        # socketio.emit("datatest",randomdata)


    if __name__ == '__main__':
        socketio.run(app, host="0.0.0.0", port=5000)

except Exception as e:
    print("Er ging iets mis, herstart het programma")
finally:
    GPIO.cleanup()