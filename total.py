import Bodenfeuchtigkeitssensor
import Temperatursensor
import time
import RPi.GPIO as GPIO
import LED
import datetime


RETRY_MAX = 10


def write_to_file(filename, tempdata, bodendata):
    file = open("filename", "a")
    timestamp = tempdata["timestamp"]
    temperatur = tempdata["temp"]
    humidity = tempdata["humidity"]
    bodenfeuchtigkeit = bodendata

    with open(filename ,"a") as file:
        line = f"{timestamp}; {temperatur}; {humidity}; {bodenfeuchtigkeit};\n"
        file.write(line)


if __name__ == '__main__':
    tempsensor = Temperatursensor.setup()
    bodensensor = Bodenfeuchtigkeitssensor.setup()
    filename = "Lesedaten.csv"
    warnled = LED.setup()
    runled = LED.setup(pin = 21)
    try:
        with open(filename) as f:
            pass
    except FileNotFoundError:
        with open(filename, "w+") as file:
            file.write ("Timestamp; temp; humidity; bodenfeuchtigkeit;\n")
    try:
        LED.on(runled)
        while True:                                                                                                     #laeuft ewig
            for retry in range(RETRY_MAX):
                try:
                    tempdata = Temperatursensor.read(tempsensor)
                    break                                                                                               #wenn gelesen, dann "for" abbrechen
                except ValueError:
                    if retry+1 == RETRY_MAX:
                        tempdata = {"temp": -1,
                                    "humidity": -1,
                                    "timestamp": datetime.datetime.now()}
                    else:
                        time.sleep(2)
            bodendata = Bodenfeuchtigkeitssensor.read(bodensensor)
            write_to_file(filename, tempdata, bodendata)
            print(f"{tempdata['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} Bodenfeuchtigkeit: {100-(((bodendata-100)/1600)*100):>6.2f}% Temperatur: {tempdata['temp']:>6.2f}°C Luftfeuchtigkeit: {tempdata['humidity']:>6.2f}%") #":>6.2f" um Zahlenstruktur beizubehalten
            if bodendata >400:
                LED.on(warnled)
            else:
                LED.off(warnled)
            try:
                time.sleep(10-retry*2)
            except ValueError:
                pass
    finally:
        GPIO.cleanup()