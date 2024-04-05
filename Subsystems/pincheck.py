import RPi.GPIO as GPIO
import time

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set up GPIO pins 17 and 27 as output pins
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

try:
    # Turn on GPIO pin 17
    GPIO.output(17, GPIO.HIGH)
    print("GPIO pin 17 is ON")

    # Turn on GPIO pin 27
    GPIO.output(27, GPIO.HIGH)
    print("GPIO pin 27 is ON")

    # Wait for 27 seconds
    time.sleep(27)

finally:
    # Clean up GPIO
    GPIO.cleanup()
