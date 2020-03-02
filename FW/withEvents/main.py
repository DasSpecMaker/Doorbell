import nfc

LedPin = 24
ButtonPin = 26

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(ButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LedPin, GPIO.OUT) #not working at the moment

while True: #change statment to get input from APP
    input_state = GPIO.input(ButtonPin)
    if input_state == False:
        print("Button Pressed!")
        GPIO.output(LedPin, 1)
        nfc.run()
        time.sleep(0.5)
    else:
        print("Waiting ...")
        GPIO.output(LedPin, 0)
        time.sleep(0.5)
