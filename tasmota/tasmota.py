from flask import Flask, render_template, request
import paho.mqtt.client as mqtt

app = Flask(__name__)


mqtt_broker = "192.168.31.94"
power_state_topic = "stat/topic/RESULT"
power_command_topic = "cmnd/topic/POWER"

current_state = "Unknown" 

# MQTT-клиент
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(power_state_topic)

def on_message(client, userdata, msg):
    global current_state
    payload = msg.payload.decode()
    print(f"Received message on topic '{msg.topic}': {payload}")  # Отладка
    if "POWER" in payload:
        current_state = payload.split('"')[3]  # Извл "ON" или "OFF"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, 1883, 60)
client.loop_start()  # Запуск фон MQTT

@app.route("/", methods=["GET", "POST"])
def index():
    global current_state
    if request.method == "POST":
        if request.form.get("action") == "on" and current_state != "ON":
            client.publish(power_command_topic, "ON")
        elif request.form.get("action") == "off" and current_state != "OFF":
            client.publish(power_command_topic, "OFF")
    return render_template("index.html", state=current_state)

if __name__ == "__main__":
    app.run(debug=True)
