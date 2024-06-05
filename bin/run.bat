@echo off

REM Start mosquitto
start /B "" "C:\Program Files\mosquitto\mosquitto.exe"

REM Wait for a moment before starting the next program
timeout /t 2

REM Start app.py with specified arguments
start "" "python" "%~dp0\app.py" --ip 192.168.31.94 --silent

start /B "" "python" "%~dp0\emulate_sens.py"

REM Keep the command prompt open
pause
