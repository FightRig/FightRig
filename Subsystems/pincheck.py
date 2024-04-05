import RPi.GPIO as GPIO
import time

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set up GPIO pins 4 and 5 as output pins
GPIO.setup(4, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)

try:
    # Turn on GPIO pin 4
    GPIO.output(4, GPIO.HIGH)
    print("GPIO pin 4 is ON")

    # Turn on GPIO pin 5
    GPIO.output(5, GPIO.HIGH)
    print("GPIO pin 5 is ON")

    # Wait for 5 seconds
    time.sleep(5)

finally:
    # Clean up GPIO
    GPIO.cleanup()
