from flask import Flask, render_template
import paho.mqtt.client as mqtt

app = Flask(__name__)

mqtt_broker = "127.0.0.1"
mqtt_topic = "test/topic" 

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print(f"Received message from topic {msg.topic}: {msg.payload}")
    sensor_data[msg.topic] = msg.payload.decode('utf-8')

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker, 1883, 60)

sensor_data = {} 

@app.route("/")
def index():
    return render_template("index.html", sensor_data=sensor_data)

if __name__ == "__main__":
    mqtt_client.loop_start()
    app.run(debug=True)
