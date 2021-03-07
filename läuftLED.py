import RPi.GPIO as GPIO

def setup (pin = 21):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    return pin
