from flask import Flask, render_template
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)


mqtt_broker = "127.0.0.1"
mqtt_port = 1883


sensor_data = {
    "Temp": {"value": 0, "unit": "Celsius"},
    "Value": {"value": 0, "unit": "Percentage"},
    "Pressure": {"value": 0, "unit": "hPa"},
    "sensor4": {"value": 0, "unit": "NaN"},
    "Battery": {"value": 0, "unit": "V"},
    "battery": {"value": 0, "unit": "Percent"},
}

def on_message(client, userdata, msg):
    try:
       
        sensor_name = msg.topic.split("/")[-1]
       
        sensor_data[sensor_name]["value"] = float(msg.payload.decode("utf-8"))
    except Exception as e:
        print(f"Error processing MQTT message: {e}")


mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker, mqtt_port, 60)


for sensor in sensor_data:
    mqtt_topic = f"topic/{sensor}"
    mqtt_client.subscribe(mqtt_topic)


mqtt_client.loop_start()


@app.route("/")
def index():
    return render_template("index.html", sensor_data=sensor_data)


@app.route("/data")
def get_data():
    return json.dumps(sensor_data)

if __name__ == "__main__":
    app.run(debug=True)
