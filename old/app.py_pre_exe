from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_caching import Cache
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import yaml
import paho.mqtt.client as mqtt
import json
import sys
import csv
from random import randint
import time
def read_settings():
    try:
        with open('static/data/settings.csv', mode='r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            settings = {rows[0]: rows[1] for rows in reader}
            return settings
    except FileNotFoundError:
        with open('static/data/settings.csv', mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['mqtt_broker', '127.0.0.1'])
            writer.writerow(['mqtt_port', '1883'])
        return {'mqtt_broker': '127.0.0.1', 'mqtt_port': '1883'}


settings = read_settings()

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.secret_key = 'development key'
passwords_file = 'static\\data\\passwd'


mqtt_broker = settings['mqtt_broker']
mqtt_port = int(settings['mqtt_port'])
hello_username = ""
status = "Offline"
last_update_time = datetime.now()
sensor_data = {

    "Temp": {"value": 25, "unit": "°C", "icon": "sun_max"},
    "Value": {"value": 50, "unit": "%", "icon": "chart_bar_fill"},
    "Pressure": {"value": 1015, "unit": "hPa", "icon": "tornado"},
    "sensor1": {"value": 0, "unit": "NaN", "icon": "burn"},
    "sensor3": {"value": 31, "unit": "Danon", "icon": "burn"},
    "Battery": {"value": 4.4, "unit": "V", "icon": "bolt_horizontal_fill"},
    "battery": {"value": 69, "unit": "%", "icon": "battery_25"},
}
data = []

def on_message(client, userdata, msg , rc):
    if rc == 0:
        print("Connected to MQTT broker!")
    else:
        print("Connection failed with code:", rc) 
    global data
    global last_update_time

    try:
        sensor_name = msg.topic.split("/")[-1]
        sensor_value = float(msg.payload.decode("utf-8"))

        # + данные в список
        data.append({
            "timestamp": datetime.now(),
            "sensor_name": sensor_name,
            "value": sensor_value
        })

        # Записc в CSV 
        with open("static/data/dataa.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["timestamp", "sensor_name", "value"])
            for data_point in data:
                writer.writerow([data_point["timestamp"], data_point["sensor_name"], data_point["value"]])

        last_update_time = datetime.now()

    except Exception as e:
        print(f"Error processing MQTT message: {e}")


mqtt_client = mqtt.Client(client_id="", protocol=mqtt.MQTTv5)
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker, mqtt_port, 60)

for sensor in sensor_data:
    mqtt_topic = f"topic/{sensor}"
    mqtt_client.subscribe(mqtt_topic)

mqtt_client.loop_start()

# def update_sensor_values():
#     while True:
#         for sensor in sensor_data:
#             if sensor.st artswith("sensor"):
#                 sensor_data[sensor]["value"] = round(random.uniform(0, 100), 2)
#             elif sensor == "Temp":
#                 sensor_data[sensor]["value"] = round(random.uniform(15, 30), 2)
#             elif sensor == "Battery":
#                 sensor_data[sensor]["value"] = round(random.uniform(3.5, 4.2), 2)
#             elif sensor == "battery":
#                 sensor_data[sensor]["value"] = round(random.uniform(0, 100), 2)
#             else:
#                 sensor_data[sensor]["value"] = round(random.uniform(0, 100), 2)

#         save_to_csv(sensor_data)
#         time.sleep(10)

# def save_to_csv(sensor_data):
#     with open('sensor_data.csv', 'w', newline='') as csvfile:
#         fieldnames = ['Sensor', 'Value', 'Unit']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#         writer.writeheader()
#         for sensor, data in sensor_data.items():
#             writer.writerow({'Sensor': sensor, 'Value': data['value'], 'Unit': data['unit']})



##################################

# @app.route('/editor')
# def editor():
#     return render_template('editor.html')

# @app.route('/save_card', methods=['POST'])
# def save_card():
#     data = request.get_json()
#     card_name = data.get('name')
#     card_code = data.get('code')

#     file_path = f'cards/{card_name.lower()}.yaml'
#     with open(file_path, 'w') as file:
#         file.write(card_code)

#     return jsonify({'success': True, 'message': 'Карточка успешно сохранена'})

##################################





@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        with open(passwords_file, 'a') as file:
            file.write(f'{username}:{hashed_password}\n')

        return redirect(url_for('login'))

    return render_template('register_form.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        passwords = {}

        try:
            with open(passwords_file, 'r') as file:
                for line in file:
                    parts = line.strip().split(':', 1)
                    if len(parts) == 2:
                        usernames, hashed_password = parts
                        passwords[usernames] = hashed_password
        except FileNotFoundError:
            pass

        if username in passwords:
            if check_password_hash(passwords[username], password):
                session['logged_in'] = True
                session['hello_username'] = username
                return redirect(url_for('index'))
        else:
            error_message = 'Wrong password. Try again.'
            return render_template('login_form.html', error_message=error_message)

    return render_template('login_form.html')

@app.route("/logout")
def logout():
    session.clear()
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route("/")
@cache.cached(timeout=60)
def index():
    global status, last_update_time

    time_difference = datetime.now() - last_update_time
    if time_difference.total_seconds() > 10:
        status = "Offline"
        print("like")
    else:
        status = "Online"
        print("dislike")

    hello_username = session.get('hello_username', 'Guest')
    is_guest = (hello_username == 'Guest')

    if request.args.get('guest') == 'true':
        session['logged_in'] = True
        session['hello_username'] = 'Guest'

    return render_template("index.html", sensor_data=sensor_data, hello_username=hello_username, is_guest=is_guest, status=status)

@app.route("/overview")
def overview():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("overview.html", sensor_data=sensor_data)

@app.route("/charts")
def charts():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("charts.html", sensor_data=sensor_data)

def read_settings():
    settings = {'mqtt_broker': '127.0.0.1', 'mqtt_port': '1883'}
    try:
        with open('data/settings.csv', mode='r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                settings[row[0]] = row[1]
    except FileNotFoundError:
        pass 

    return settings

def save_settings(settings):
    with open('data/settings.csv', mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for key, value in settings.items():
            writer.writerow([key, value])

@app.route("/settings", methods=['GET', 'POST'])
def settings_route():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        mqtt_broker = request.form['mqtt_broker']
        mqtt_port = request.form['mqtt_port']

        settings = read_settings()
        settings['mqtt_broker'] = mqtt_broker
        settings['mqtt_port'] = mqtt_port
        save_settings(settings)

        return redirect(url_for('index'))
    else:
        mqtt_settings = read_settings()
        topic_settings = read_topic_settings()
        return render_template("settings.html", mqtt_broker=mqtt_settings['mqtt_broker'],
                               mqtt_port=mqtt_settings['mqtt_port'], topic_settings=topic_settings)

def read_topic_settings():
    topic_settings = {}
    try:
        with open('topic_data/settings.csv', mode='r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                topic_settings[row[0]] = {'value': float(row[1]), 'unit': row[2], 'icon': row[3]}
    except FileNotFoundError:
        pass  

    return topic_settings

def save_topic_settings(topic_settings):
    with open('topic_data/settings.csv', mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for key, value in topic_settings.items():
            writer.writerow([key, value['value'], value['unit'], value['icon']])


@app.route("/data")
def get_data():
    return json.dumps(sensor_data)

@app.errorhandler(404)
@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/get_notification', methods=['GET'])
def get_notification():
    i_value = randint(28, 32)
    if i_value > 30:
        print("AAAHAAAAAUUUU")
        return jsonify({'message': 'Значение I больше 30!'})
    else:
        return jsonify({'message': ''})

if __name__ == '__main__':
    ip_address = '192.168.31.94'        #Set Default to your own IP instead of localhost
    port = 80                           #Set Default to the desired port instead of the default port
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



























































                                                                    