@echo off

REM Start mosquitto
start /B "" "C:\Program Files\mosquitto\mosquitto.exe"

REM Wait for a moment before starting the next program
timeout /t 2

REM Start app.py with specified arguments
start "" "python" "E:\Python_Smart_Home_Monitor\app.py" --ip 192.168.31.94 --silent

start /B "" "python" "E:\Python_Smart_Home_Monitor\emulate_sens.py"

REM Keep the command prompt open
pause
