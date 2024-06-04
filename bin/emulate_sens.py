import paho.mqtt.publish as publish
import time
import random

mqtt_broker = "192.168.31.94"
mqtt_port = 1883
temp_topics = ["topic/Temperature", "topic/Inside", "topic/Outside"]
pressure = ["topic/Value", "topic/Pressure"]
co2 = ["topic/CO2"]
hum = ["topic/Humidity"]
bat = ["topic/Battery"]
def emulate_sensors():
    while True:
        for topic in temp_topics:
            sensor_value = round(random.uniform(20, 25), 2)
            publish.single(topic, payload=str(sensor_value), hostname=mqtt_broker, port=mqtt_port)
            print(f"Value sended: {sensor_value} to topic: {topic}")

        for topic in pressure:
            sensor_value = round(random.uniform(900, 910), 2)
            publish.single(topic, payload=str(sensor_value), hostname=mqtt_broker, port=mqtt_port)
            print(f"Value sended: {sensor_value} to topic: {topic}")
        for topic in co2:
            sensor_value = round(random.uniform(710, 720), 2)
            publish.single(topic, payload=str(sensor_value), hostname=mqtt_broker, port=mqtt_port)
            print(f"Value sended: {sensor_value} to topic: {topic}")
        for topic in hum:
            sensor_value = round(random.uniform(40, 44), 2)
            publish.single(topic, payload=str(sensor_value), hostname=mqtt_broker, port=mqtt_port)
            print(f"Value sended: {sensor_value} to topic: {topic}")    
        for topic in bat:
            sensor_value = round(random.uniform(98, 100), 2)
            publish.single(topic, payload=str(sensor_value), hostname=mqtt_broker, port=mqtt_port)
            print(f"Value sended: {sensor_value} to topic: {topic}")    
        time.sleep(10)

if __name__ == "__main__":
    emulate_sensors()
