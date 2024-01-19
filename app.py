from flask import Flask, render_template, request, redirect, url_for,session
import paho.mqtt.client as mqtt
import json
import sys
app = Flask(__name__)
app.secret_key = 'your_secret_key'

mqtt_broker = "127.0.0.1"
mqtt_port = 1883


sensor_data = {
    "Temp": {"value": 0, "unit": "Celsius"},
    "Value": {"value": 0, "unit": "Percentage"},
    "Pressure": {"value": 0, "unit": "hPa"},
    "sensor1": {"value": 0, "unit": "NaN"},
    "sensor2": {"value": 0, "unit": "NaN"},
    "sensor3": {"value": 0, "unit": "NaN"},
    "sensor4": {"value": 0, "unit": "NaN"},
    "sensor5": {"value": 0, "unit": "NaN"},
    "sensor6": {"value": 0, "unit": "NaN"},
    "sensor7": {"value": 0, "unit": "NaN"},
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

@app.route('/submit_form', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error_message = 'Неверные учетные данные. Пожалуйста, повторите вход.'
            return render_template('login_form.html', error_message=error_message)

    return render_template('login_form.html')

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route("/")
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("index.html", sensor_data=sensor_data)



@app.route("/data")
def get_data():
    return json.dumps(sensor_data)


if __name__ == '__main__':
    ip_address = '192.168.31.94'            #Set Default to your own IP instead of localhost
    port = 5000                         #Set Default to the desired port instead of the default port
    silent = False                      #Set True if no logging is required by default
    

    for i in range(1, len(sys.argv), 2):

        if sys.argv[i] == '--ip':
            ip_address = sys.argv[i + 1]
        elif sys.argv[i] == '--port':
            port = int(sys.argv[i + 1])
        elif sys.argv[i] == '--silent':
            silent = True

    if not silent:
        app.run(host=ip_address, port=port)
    else:
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        app.run(host=ip_address, port=port, use_reloader=False)
