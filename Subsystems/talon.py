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
        pulse_width_ms = max(min(pulse_width_ms, 2.44), 1.04)

        if pulse_width_ms == 2.44:
            pulse_width_ms = .9
        
        # Convert pulse width to duty cycle
        duty_cycle = (pulse_width_ms) / 20* 100
        
        # Set duty cycle for PWM signal
        print("DUTY CYCLE: " + str(duty_cycle))
        self.pwm.ChangeDutyCycle(duty_cycle)

if __name__ == "__main__":
    from baseinputs import Controller


    talon = TalonSRX(3)
    controller = Controller()

    try:
        while True:
            values = controller.read()

            if values["y"]:
                print("GPIO Clean up")
                break

            movement = 2.4 - (values["RightTrigger"] * 1.36)
            print(movement)
            talon.set_pwm_pulse(movement)
            time.sleep(0.2)  # Sleep to avoid continuous updates (adjust as needed)

    finally:
        # Clean up GPIO on exit
        GPIO.cleanup()
