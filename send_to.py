import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
def send_mqtt_message():
    broker_address = ip_entry.get()
    broker_port = int(port_entry.get())
    topic_inside = "topic/Temp_Inside"

    try:
        temp_inside = float(temp_inside_entry.get())

        print(f"Connecting to broker: {broker_address}:{broker_port}")

        client = mqtt.Client()
        client.connect(broker_address, broker_port)
        client.publish(topic_inside, temp_inside)

        status_label.config(text="Данні відправлено!")
    except ValueError:
        status_label.config(text="Помилка: не введено")
    except Exception as e:
        status_label.config(text=f"Помилка: {e}")
    finally:
        client.disconnect()
        
window = tk.Tk()
window.title("отправить в топики")
window.iconbitmap("static\icon.ico")
ttk.Label(window, text="IP-адреса брокера:").grid(row=0, column=0, padx=5, pady=5)
ip_entry = ttk.Entry(window)
ip_entry.grid(row=0, column=1, padx=5, pady=5)
ip_entry.insert(0, "127.0.0.1")  

ttk.Label(window, text="Порт брокера:").grid(row=1, column=0, padx=5, pady=5)
port_entry = ttk.Entry(window)
port_entry.grid(row=1, column=1, padx=5, pady=5)
port_entry.insert(0, "1883") 

ttk.Label(window, text="Температура всередині:").grid(row=2, column=0, padx=5, pady=5)
temp_inside_entry = ttk.Entry(window)
temp_inside_entry.grid(row=2, column=1, padx=5, pady=5)


ttk.Button(window, text="Відправити", command=send_mqtt_message).grid(row=4, column=0, columnspan=2, pady=10)

status_label = ttk.Label(window, text="")
status_label.grid(row=5, column=0, columnspan=2, pady=5)

window.mainloop()