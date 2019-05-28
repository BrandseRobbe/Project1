# Imports
import socketio
from flask import Flask, request, jsonify, json
from flask_socketio import SocketIO
from flask_cors import CORS

# from Database.DP1Database import Database
from Database.DP1Database import Database

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

conn = Database(app=app, user='mct', password='mct', db='Project1', host='localhost', port=3306)
endpoint = '/api/v1'


@app.route(endpoint + '/testconnectie', methods=["GET"])
def testconnectie():
    if request.method == "GET":
        return jsonify(message = 'geconnecteerd')

@socketio.on("connect")
def connecting():
    socketio.emit("connected")
    print("Connection with client established")

    # randomdata = conn.get_data("select * from users")
    # print(randomdata)
    # socketio.emit("datatest",randomdata)



if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
