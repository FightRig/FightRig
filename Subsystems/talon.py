import RPi.GPIO as GPIO
import time

class TalonSRX:
    """INSTANCE OF TALON SRX MOTOR CONTROLLER"""
    def __init__(self, pwm_pin):
        self.pwm_pin = pwm_pin

        # Set GPIO mode to BCM
        GPIO.setmode(GPIO.BCM)

        # Set up GPIO pin for PWM output
        GPIO.setup(self.pwm_pin, GPIO.OUT)

        # Initialize PWM with a frequency of 100 Hz (period of 10 ms)
        self.pwm = GPIO.PWM(self.pwm_pin, 100)
        self.pwm.start(0)  # Start PWM with 0% duty cycle

    def set_pwm_pulse(self, pulse_width_ms):
        # Ensure pulse width is within the range of 1-2 ms
        pulse_width_ms = max(min(pulse_width_ms, 2), 1)
        
        # Convert pulse width to duty cycle
        duty_cycle = pulse_width_ms / 20 * 100
        
        # Set duty cycle for PWM signal
        print("DUTY CYCLE: " + str(duty_cycle))
        self.pwm.ChangeDutyCycle(duty_cycle)

if __name__ == "__main__":
    try:
        # Initialize Talon SRX motor controller on GPIO pin 4
        talon_srx = TalonSRX(4)

        # Set PWM pulse width to 1.5 ms (neutral)
        talon_srx.set_pwm_pulse(1.5)

        time.sleep(2)  # Wait for 2 seconds

        # Set PWM pulse width to 1 ms (minimum throttle)
        talon_srx.set_pwm_pulse(1)

        time.sleep(2)  # Wait for 2 seconds

        # Set PWM pulse width to 2 ms (maximum throttle)
        talon_srx.set_pwm_pulse(1.9)

        time.sleep(2)  # Wait for 2 seconds

    finally:
        # Clean up GPIO on exit
        GPIO.cleanup()
