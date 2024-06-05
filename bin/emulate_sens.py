import paho.mqtt.publish as publish
import time
import random

mqtt_broker = "192.168.31.94"
mqtt_port = 1883
temp_topics = ["topic/Temperature", "topic/Inside", "topic/Outside"]
pressure = ["topic/Pressure"]
co2 = ["topic/CO2"]
hum = ["topic/Humidity"]
bat = ["topic/Battery"]
def emulate_sensorss():
    while True:
        for topic in temp_topics:
            sensor_value = round(random.uniform(23, 25), 2)
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
def emulate_sensors():
    previous_values = {} 
    
    # Define topic ranges as tuples (immutable)
    topic_ranges = {
        tuple(temp_topics): (23, 25),
        tuple(pressure): (900, 910),
        tuple(co2): (710, 720),
        tuple(hum): (40, 44),
        tuple(bat): (98, 100),
    }

    while True:
        for topic_list, (min_val, max_val) in topic_ranges.items():  # Iterate over tuples directly
            for topic in topic_list:
                step = 0.1  

                prev_value = previous_values.get(topic, (min_val + max_val) / 2) 

                new_value = round(random.uniform(max(min_val, prev_value - step), min(max_val, prev_value + step)), 2) 

                previous_values[topic] = new_value 

                publish.single(topic, payload=str(new_value), hostname=mqtt_broker, port=mqtt_port)
                print(f"Value sended: {new_value} to topic: {topic}")
        time.sleep(10) 
if __name__ == "__main__":
    emulate_sensors()
