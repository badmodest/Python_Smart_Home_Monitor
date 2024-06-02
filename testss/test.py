from flask import Flask, render_template, request, redirect, url_for
import json


def load_sensor_data(filename="sensor_data.json"):

    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_sensor_data(data, filename="sensor_data.json"):
    """Сохраняет данные сенсора в JSON файл."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)  


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def sensor_dashboard():
    sensor_data = load_sensor_data()

    if request.method == "POST":
        if "add" in request.form:
            new_key = request.form["new_key"]
            sensor_data[new_key] = {"value": 0, "unit": "", "icon": ""}
        elif "delete" in request.form:
            del_key = request.form["del_key"]
            del sensor_data[del_key]
        else:  # Обновление значений
            for key in sensor_data:
                sensor_data[key]["value"] = float(request.form[key + "_value"])
                sensor_data[key]["unit"] = request.form[key + "_unit"]
                sensor_data[key]["icon"] = request.form[key + "_icon"]

        save_sensor_data(sensor_data)  # Сохраняем изменения
        return redirect(url_for("sensor_dashboard"))  # Перезагружаем страницу

    return render_template("dashboard.html", sensor_data=sensor_data)

if __name__ == "__main__":
    app.run(debug=True)
