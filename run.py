import subprocess
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter import ttk
import logging
import threading
import webbrowser

class TextLogHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        log_entry = self.format(record) 
        self.text_widget.insert(tk.END, f"{log_entry}\n")
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
        logger.warning("Это должно появиться как в консоли, так и в файле журнала")

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



"""
def format_log_entry(record, text_widget):
    log_entry = f"{record.levelname}: {record.msg}\n" 
    text_widget.insert(tk.END, log_entry) 

    if record.levelname == "ERROR":
        text_widget.tag_add("error", "end-2c", "end-1c")  
    elif "POST" in log_entry or "GET" in log_entry:
        if "308" in log_entry:
            text_widget.tag_add("success", "end-2c", "end-1c") 
        elif "304" in log_entry:
            text_widget.tag_add("modified", "end-2c", "end-1c") 
        elif "404" in log_entry:
            text_widget.tag_add("warning", "end-2c", "end-1c")  
"""
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        if server_started:
            stop_flask_server()
            root.destroy()
        elif not server_started:
            root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("./static/smart-home.ico")
    style = ttk.Style()
    style.theme_use("vista")
    root.title("Flask Server")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    ip_label = ttk.Label(text="IP-address:")
    ip_entry = ttk.Entry()

    port_label = ttk.Label(text="Prot:")
    port_entry = ttk.Entry()
    
    text_widget = ScrolledText(root,   bg='#000', fg='#0f0', height=20, width=80 )
    text_widget.pack(expand=True, fill=tk.BOTH)

    start_button = ttk.Button(text="Start server", command=start_app )
    stop_button = ttk.Button(text= "Stop  server", command=stop_flask_server)
    open_button = ttk.Button(text="Go to web page", command=lambda: open_webpage(ip_entry.get(), port_entry.get()))


    text_widget.tag_configure("error", foreground="red")
    text_widget.tag_configure("success", foreground="green")
    text_widget.tag_configure("modified", foreground="cyan")
    text_widget.tag_configure("warning", foreground="orange") 

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
    handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s')) 
    logger.addHandler(handler)

    root.mainloop()
