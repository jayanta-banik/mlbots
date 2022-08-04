from flask import Flask, request
import json
from libs import IOT

app_http = Flask(__name__)

app_http.add_url_rule('/IOT/DarkSourceOfCode/status', view_func=IOT.getStatus, methods=['GET'])
app_http.add_url_rule('/IOT/DarkSourceOfCode/getDHT', view_func=IOT.getSensorData, methods=['GET'])
app_http.add_url_rule('/IOT/DarkSourceOfCode/setDHT', view_func=IOT.setSensorData, methods=['POST'])

app_http.add_url_rule('/IOT/EvilKing/status', view_func=IOT.getStatus, methods=['GET'])#ExpLamp
app_http.add_url_rule('/IOT/EvilKing/getDHT', view_func=IOT.getSensorData_EK, methods=['GET'])
app_http.add_url_rule('/IOT/EvilKing/setDHT', view_func=IOT.setSensorData_EK, methods=['POST']) 

@app_http.route('/')
def hello_world():
    return "http server"

if __name__ == '__main__':
    app_http.run(debug=True, host='0.0.0.0')