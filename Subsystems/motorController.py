import RPi.GPIO as GPIO
import time

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

        self.current_duty = 0.0
        self.target_duty = 0.0
        self.acceleration = 10.0  # Acceleration rate per second (adjust as needed)

    def set_pwm_pulse(self, pulse_width_ms):
        # Ensure pulse width is within the range of 1-2ms
        pulse_width_ms = max(min(pulse_width_ms, 2.0), 1.0)
        
        # Convert pulse width to duty cycle (1ms = 0% duty, 2ms = 100% duty)
        duty_cycle = (pulse_width_ms - 1.0) / 1.0 * 100.0
        
        # Set duty cycle for both PWM signals
        print(duty_cycle)
        self.pwm_high.ChangeDutyCycle(duty_cycle)
        self.pwm_low.ChangeDutyCycle(100.0 - duty_cycle)  # Inverse duty cycle for low
    
    def setDuty(self, percent):
        print(percent)
        # Clamp acceleration
        target_duty = max(min(percent, 100.0), 0.0)
        acceleration = self.acceleration * (time.time() - self.last_update)
        self.current_duty += acceleration
        self.current_duty = max(min(self.current_duty, 100.0), 0.0)

        # Update PWM
        self.pwm_high.ChangeDutyCycle(self.current_duty)
        self.pwm_low.ChangeDutyCycle(100.0 - self.current_duty)
        self.last_update = time.time()

if __name__ == "__main__":
    from baseinputs import Controller
    import RPi.GPIO as GPIO

    pwm_high_pin = 4
    pwm_low_pin = 5
    
    # Initialize motor controller
    motor = SPX(pwm_high_pin, pwm_low_pin)
    controller = Controller()

    try:
        while True:
            values = controller.read()

            if values["y"]:
                print("GPIO Clean up")
                break

            movement = values["RightTrigger"] * 100
            motor.setDuty(movement)
            time.sleep(0.1)  # Sleep to avoid continuous updates (adjust as needed)

    finally:
        # Clean up GPIO on exit
        GPIO.cleanup()
