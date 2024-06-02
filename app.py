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
import argparse
import time
import logging
import tkinter as tk


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

def run_flask_app(ip, port, log_field):
    log_handler = TextLogHandler(log_field)
    logger = logging.getLogger(__name__) 
    logger.addHandler(log_handler)
    logger.info("Starting app")
    app.run(host=ip, port=port)

class TextLogHandler(logging.Handler):
    def __init__(self, text_field):
        super().__init__()
        if not isinstance(text_field, tk.Text):
            raise ValueError("text_field must be a tkinter Text object")
        self.text_field = text_field

    def emit(self, record):
        log_entry = f"{record.levelname}: {record.message}" 
        self.text_field.insert("end", log_entry + "\n")
        self.text_field.see("end")  

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.secret_key = 'development key'
passwords_file = 'static\\data\\passwd'
settings = read_settings()

mqtt_broker = "192.168.31.94"
mqtt_port = 1883
#settings['mqtt_broker']
#int(settings['mqtt_port'])
power_state_topic = "stat/topic/RESULT"
power_command_topic = "cmnd/topic/POWER"
current_state = "Unknown" 
hello_username = ""
status = "Offline"
last_update_time = datetime.now()

def load_sensor_data(filename="sensor_data.json"):

    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

sensor_data = load_sensor_data()

'''
sensor_data = {
    "Temperature": {"value": 0, "unit": "°C", "icon": "sun_max"},
    "Humidity": {"value": 0, "unit": "%", "icon": "drop"},
    "Pressure": {"value": 0, "unit": "hPa", "icon": "chevron_up_chevron_down"},
    "CO2": {"value": 0, "unit": "PPM", "icon": "wind"},
    "Inside": {"value": 0, "unit": "Danon", "icon": "burn"},
    "Outside": {"value": 0, "unit": "V", "icon": "bolt_horizontal_fill"},
    "battery": {"value": 0, "unit": "%", "icon": "battery_25"},
}
'''
data = []



'''
def connect_mqtt(client, rc):
    try:
        print("Connected with result code "+str(rc))

        is_connected = True
        for sensor in sensor_data:
            print(f"RABOTA SENSOR topic/{sensor} ")
            mqtt_topic = f"topic/{sensor}"
            print("TOPIC IS........",mqtt_topic)
            client.subscribe(mqtt_topic)
        time.sleep(1)
        if not client.is_connected():
            is_connected = False
            print("MQTT client not connected"+str(rc))

    except Exception as e:
        logging.error(f"MQTT connection failed: {e}")
        is_connected = False

    if is_connected:
        print("MQTT client connected:", client.is_connected())
        
'''
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for sensor in sensor_data:
        mqtt_topic = f"topic/{sensor}"
        client.subscribe(mqtt_topic)
    client.subscribe(power_state_topic) 
    client.publish(power_state_topic, " ") # Публикуем пустое сообщение, чтобы Tasmota отправила текущее состояние

def on_message(client, userdata, msg):
    global data, last_update_time, current_state

    try:
        payload = msg.payload.decode()
        print(f"Received message on topic '{msg.topic}': {payload}")  # Отладка

        if msg.topic == power_state_topic:
            current_state = json.loads(payload)["POWER"]
            client.publish("web_ui/topic/switch", current_state)
        else:
            sensor_name = msg.topic.split("/")[-1]
            if sensor_name in sensor_data:
                sensor_data[sensor_name]["value"] = float(payload)

                # Добавляем данные в список (только значение сенсора)
                data.append({
                    "timestamp": datetime.now(),
                    "sensor_name": sensor_name,
                    "value": sensor_data[sensor_name]["value"]  # Записываем только значение
                })

                # Записываем в CSV (только значение сенсора)
                with open("static/data/dataa.csv", "a", newline="") as csvfile:  # Используем 'a' для добавления
                    writer = csv.writer(csvfile)
                    writer.writerow([datetime.now(), sensor_name, sensor_data[sensor_name]["value"]])

    except Exception as e:
        print(f"Error processing MQTT message: {e}")

client = mqtt.Client(client_id="iMAC")
client.on_connect = on_connect
client.on_message = on_message
if on_message:
    print('NUBLAAA')
client.connect(mqtt_broker, mqtt_port, 60)
print(mqtt_broker,mqtt_port)

client.loop_start()




"""

# def save_to_csv(sensor_data):
#     with open('sensor_data.csv', 'w', newline='') as csvfile:
#         fieldnames = ['Sensor', 'Value', 'Unit']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#         writer.writeheader()
#         for sensor, data in sensor_data.items():
#             writer.writerow({'Sensor': sensor, 'Value': data['value'], 'Unit': data['unit']})
"""


"""

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

"""

"""
client = mqtt.Client(client_id="iMAC")
client.on_message = on_connect
client.on_message = on_message
if on_message:
    print('NUBLAAA')
#client.connect(mqtt_broker, mqtt_port, 60)
client.connect("localhost", 1883, 60)
print(mqtt_broker,mqtt_port)
client.loop_start()
#client.loop_forever()
"""

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

@app.route("/", methods=["GET", "POST"])
@cache.cached(timeout=60)
def index():
    global status, last_update_time, current_state
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

    if request.method == "POST":
        switch_state = request.form.get("switch")
        print("свич стейт",switch_state) # Добавьте эту строку для отладки
        if switch_state == "on":
            client.publish(power_command_topic, "ON")
            print("VKLUCHAUUUU")
        elif switch_state == "off":
            client.publish(power_command_topic, "OFF")
            print("OFFFFFFFFFFFFF")
    temp = sensor_data['Temperature']['value']
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",temp)
    return render_template("index.html", sensor_data=sensor_data, hello_username=hello_username, is_guest=is_guest, status=status, state=current_state, temp=temp)

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

@app.route('/sensor_graph/<sensor_name>')
def sensor_graph(sensor_name):
    return render_template('sensor_graph.html', sensor_name=sensor_name )


def read_settings():
    settings = {'mqtt_broker': '192.168.31.94', 'mqtt_port': '1883'}
    try:
        with open('data/settings.csv', mode='r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                settings[row[0]] = row[1]
    except FileNotFoundError:
        pass 

    return settings

def save_settings(settings):
    with open('static/data/settings.csv', mode='w', newline='') as csvfile:
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
                               mqtt_port=mqtt_settings['mqtt_port'], topic_settings=topic_settings, sensor_data=sensor_data)

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
    print("OTPRAVKA", data)
    return jsonify({**sensor_data, "current_state": current_state})


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
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", help="IP address", default="192.168.31.94")
    parser.add_argument("--port", help="Port number", type=int, default=80)
    parser.add_argument("--silent", help="Suppress logging", action="store_true")
    args = parser.parse_args()
    
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.info("Starting app")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('flask.log')
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


    if not args.silent:
        app.logger.setLevel(logging.INFO) 
        app.run(host=args.ip, port=args.port)
    else:
        app.run(host=args.ip, port=args.port, use_reloader=False)