import RPi.GPIO as GPIO
import time
from threading import Thread
import signal
import sys

class LEDControl:
    def __init__(self, led_pin, button_a_pin, button_b_pin):
        self.led_pin = led_pin
        self.button_a_pin = button_a_pin
        self.button_b_pin = button_b_pin
        self.led_state = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.setup(self.button_a_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_b_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.button_a_pin, GPIO.FALLING, callback=self.turn_off_led, bouncetime=300)
        GPIO.add_event_detect(self.button_b_pin, GPIO.FALLING, callback=self.turn_on_led, bouncetime=300)

    def turn_on_led(self, channel):
        self.led_state = True
        GPIO.output(self.led_pin, self.led_state)
        print("LED turned on")

    def turn_off_led(self, channel):
        self.led_state = False
        GPIO.output(self.led_pin, self.led_state)
        print("LED turned off")

    def cleanup(self):
        GPIO.cleanup()
        print("GPIO cleaned up")

def signal_handler(sig, frame):
    print('\nProgram stopped by user')
    led_control.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    LED_PIN = 13  # Adjust this to the correct GPIO pin for your LED
    BUTTON_A_PIN = 5  # Adjust this to the correct GPIO pin for button A
    BUTTON_B_PIN = 6  # Adjust this to the correct GPIO pin for button B

    led_control = LEDControl(LED_PIN, BUTTON_A_PIN, BUTTON_B_PIN)

    signal.signal(signal.SIGINT, signal_handler)
    print("Press button A to turn the LED off, and button B to turn it on.")
    print("Press Ctrl+C to exit.")

    # Keep the script running
    while True:
        time.sleep(0.1)
