import RPi.GPIO as GPIO
import time

class Talon:
    """INSTANCE OF TALON MOTOR CONTROLLER"""
    def __init__(self, pwm_pin):
        self.pwm_pin = pwm_pin

        # Set GPIO mode to BCM
        GPIO.setmode(GPIO.BCM)

        # Set up GPIO pin for PWM output
        GPIO.setup(self.pwm_pin, GPIO.OUT)

        # Initialize PWM with a frequency of 15.625 kHz
        self.pwm = GPIO.PWM(self.pwm_pin, 15.625)
        self.pwm.start(0)  # Start PWM with 0% duty cycle

    def set_pwm_pulse(self, pulse_width_ms):
        # Ensure pulse width is within the range of 1-2 ms nominal, 0.67 - 2.33 ms max
        pulse_width_ms = max(min(pulse_width_ms, 2.33), 0.67)
        
        # Convert pulse width to duty cycle
        duty_cycle = (pulse_width_ms - 1.0) / 1.0 * 100.0
        
        # Set duty cycle for PWM signal
        self.pwm.ChangeDutyCycle(duty_cycle)

if __name__ == "__main__":
    try:
        # Initialize Talon motor controller on GPIO pin 4
        talon = Talon(2)

        # Set PWM pulse width to 1 ms (minimum throttle)
        talon.set_pwm_pulse(1)

        time.sleep(2)  # Wait for 2 seconds

        # Set PWM pulse width to 2 ms (maximum throttle)
        talon.set_pwm_pulse(2)

        time.sleep(2)  # Wait for 2 seconds

    finally:
        # Clean up GPIO on exit
        GPIO.cleanup()
