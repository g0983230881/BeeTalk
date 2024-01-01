from flask import Flask
from flask_mqtt import Mqtt

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0 
mqtt = Mqtt(app)

@app.route('/')
def index():
    return 'hello world'
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('NIU')
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    topic=message.topic,
    payload=message.payload.decode()