import subprocess
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import logging
import threading
import webbrowser

class TextLogHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        log_entry = self.format(record)
        formatted_log_entry = format_log_entry(record)  # Форматирование текста
        self.text_widget.insert(tk.END, formatted_log_entry + "\n")
        self.text_widget.see(tk.END)

server_started = False

def start_flask_server(ip_address, port):
    global app_process
    app_process = subprocess.Popen(["python", "app.py", "--ip", ip_address, "--port", port],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in app_process.stdout:
        logger.info(line.strip())

def stop_flask_server():
    global app_process
    if app_process and app_process.poll() is None:
        app_process.terminate()
        logger.info("Flask server stopped")

def open_webpage(ip_address, port):
    url = f"http://{ip_address}:{port}"
    webbrowser.open(url)

def start_app():
    ip_address = ip_entry.get()
    port = port_entry.get()

    if not ip_address:
        logger.error("Введите IP-адрес")
        return

    if not port:
        logger.error("Введите порт")
        return

    threading.Thread(target=start_flask_server, args=(ip_address, port), daemon=True).start()
    server_started = True
    
def format_log_entry(record):
    log_entry = f"{record.levelname}: {record.msg}"
    if record.levelname == "ERROR":
        return f"<font color='red'>{log_entry}</font>"
    elif "POST" in log_entry or "GET" in log_entry:
        if "308" in log_entry:
            return f"<font color='green'>{log_entry}</font>"
        elif "304" in log_entry:
            return f"<font color='cyan'>{log_entry}</font>"
    elif "404" in log_entry:
        return f"<font color='red'>{log_entry}</font>"
    return log_entry

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        if server_started:
            stop_flask_server()
            root.destroy()
        elif not server_started:
            root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Flask Server")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    ip_label = tk.Label(text="IP-адрес:")
    ip_entry = tk.Entry()

    port_label = tk.Label(text="Порт:")
    port_entry = tk.Entry()
    
    text_widget = ScrolledText(root, height=20, width=80)
    text_widget.pack(expand=True, fill=tk.BOTH)

    start_button = tk.Button(text="Запуск", command=start_app)
    stop_button = tk.Button(text="Остановить", command=stop_flask_server)
    open_button = tk.Button(text="Перейти на сайт", command=lambda: open_webpage(ip_entry.get(), port_entry.get()))

    ip_label.pack()
    ip_entry.pack()

    port_label.pack()
    port_entry.pack()

    start_button.pack()
    stop_button.pack()
    open_button.pack()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = TextLogHandler(text_widget)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s'))  # Установка форматтера
    logger.addHandler(handler)

    root.mainloop()
