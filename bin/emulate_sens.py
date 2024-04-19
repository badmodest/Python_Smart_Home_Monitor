import paho.mqtt.publish as publish
import time
import random

mqtt_broker = "192.168.31.94"
mqtt_port = 1883
temp_topics = ["topic/Temp"]
sensor_topics = ["topic/Value", "topic/Pressure"]

def emulate_sensors():
    while True:
        for topic in sensor_topics:
            sensor_value = round(random.uniform(0, 100), 2)
            publish.single(topic, payload=str(sensor_value), hostname=mqtt_broker, port=mqtt_port)
            print(f"Value sended: {sensor_value} to topic: {topic}")

        for topic in temp_topics:
            sensor_value = round(random.uniform(2, 5), 2)
            publish.single(topic, payload=str(sensor_value), hostname=mqtt_broker, port=mqtt_port)
            print(f"Value sended: {sensor_value} to topic: {topic}")

        time.sleep(10)

if __name__ == "__main__":
    emulate_sensors()
