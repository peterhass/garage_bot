import RPi.GPIO as GPIO
import time

SWITCH_PORT = 17
RELAIS_PORT = 2

class DoorIO:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SWITCH_PORT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(RELAIS_PORT, GPIO.OUT, initial=GPIO.HIGH)
        
    def cleanup(self):
        GPIO.cleanup()

    def is_switch_on(self):
        switch = GPIO.input(SWITCH_PORT)
        return not switch

    def on_switch_changed(self, callback):
        event_callback = lambda _: callback(self.is_switch_on())
        GPIO.add_event_detect(SWITCH_PORT, GPIO.BOTH, callback=event_callback)

    def trigger_relais(self):
        GPIO.output(RELAIS_PORT, False)
        time.sleep(0.3)
        GPIO.output(RELAIS_PORT, True)

