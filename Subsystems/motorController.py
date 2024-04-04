

class SPX:
    """INSTANCE OF VICTOR SPX"""
    def __init__(self, pwm_high_pin, pwm_low_pin):
        self.pwm_high_pin = pwm_high_pin
        self.pwm_low_pin = pwm_low_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwm_high_pin, GPIO.OUT)
        GPIO.setup(self.pwm_low_pin, GPIO.OUT)

        self.pwm_high = GPIO.PWM(self.pwm_high_pin, 1000)  # 1000 Hz frequency
        self.pwm_low = GPIO.PWM(self.pwm_low_pin, 1000)    # 1000 Hz frequency

        self.pwm_high.start(0)  # Start PWM with 0% duty cycle
        self.pwm_low.start(0)   # Start PWM with 0% duty cycle

    def set_pwm_pulse(self, pulse_width_ms):
        # Ensure pulse width is within the range of 1-2ms
        pulse_width_ms = max(min(pulse_width_ms, 2.0), 1.0)
        
        # Convert pulse width to duty cycle (1ms = 0% duty, 2ms = 100% duty)
        duty_cycle = (pulse_width_ms - 1.0) / 1.0 * 100.0
        
        # Set duty cycle for both PWM signals
        self.pwm_high.ChangeDutyCycle(duty_cycle)
        self.pwm_low.ChangeDutyCycle(100.0 - duty_cycle)  # Inverse duty cycle for low

if __name__ == "__main__":
    import RPi.GPIO as GPIO
    import time
    pwm_high_pin = 3
    pwm_low_pin = 4
    
    # Initialize motor controller
    motor = SPX(pwm_high_pin, pwm_low_pin)

    try:
        # Example usage: Set pulse width to 1.5ms (neutral position)
        motor.set_pwm_pulse(.15)
        time.sleep(2)  # Wait for 2 seconds

        # Example usage: Set pulse width to 1ms (move in one direction)
        motor.set_pwm_pulse(.15)
        time.sleep(2)  # Wait for 2 seconds

        # Example usage: Set pulse width to 2ms (move in the opposite direction)
        motor.set_pwm_pulse(.15)
        time.sleep(2)  # Wait for 2 seconds

    finally:
        # Clean up GPIO on exit
        GPIO.cleanup()
