from flask import Flask, render_template
import paho.mqtt.client as mqtt

app = Flask(__name__)

# Задаем адрес и порт MQTT брокера
mqtt_broker = "127.0.0.1"
mqtt_port = 1883

# Создаем словарь для хранения данных датчиков
sensor_data = {
    "Temp": {"value": 0, "unit": "Celsius"},
    "Value": {"value": 0, "unit": "Percentage"},
    "Pressure": {"value": 0, "unit": "hPa"},
    "sensor4": {"value": 0, "unit": "NaN"},
    "Battery": {"value": 0, "unit": "V"},
    "battery": {"value": 0, "unit": "Percent"},
}

# Функция для обработки сообщений от MQTT брокера
def on_message(client, userdata, msg):
    try:
        # Получаем имя датчика из темы
        sensor_name = msg.topic.split("/")[-1]
        # Обновляем данные датчика
        sensor_data[sensor_name]["value"] = float(msg.payload.decode("utf-8"))
    except Exception as e:
        print(f"Error processing MQTT message: {e}")

# Настраиваем подключение к MQTT брокеру
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker, mqtt_port, 60)

# Подписываемся на темы датчиков
for sensor in sensor_data:
    mqtt_topic = f"topic/{sensor}"
    mqtt_client.subscribe(mqtt_topic)

# Запускаем цикл обработки сообщений MQTT
mqtt_client.loop_start()

# Определение маршрута для главной страницы
@app.route("/")
def index():
    return render_template("index.html", sensor_data=sensor_data)

if __name__ == "__main__":
    app.run(debug=True)
