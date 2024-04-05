import RPi.GPIO as GPIO
import time

class TalonSRX:
    """INSTANCE OF TALON SRX MOTOR CONTROLLER"""
    def __init__(self, pwm_high_pin, pwm_low_pin):
        self.pwm_high_pin = pwm_high_pin
        self.pwm_low_pin = pwm_low_pin

        # Set GPIO mode to BCM
        GPIO.setmode(GPIO.BCM)

        # Set up GPIO pins for PWM output
        GPIO.setup(self.pwm_high_pin, GPIO.OUT)
        GPIO.setup(self.pwm_low_pin, GPIO.OUT)

        # Initialize PWM with a frequency of 100 Hz (period of 10 ms)
        self.pwm_high = GPIO.PWM(self.pwm_high_pin, 100)
        self.pwm_low = GPIO.PWM(self.pwm_low_pin, 100)
        self.pwm_high.start(0)  # Start PWM with 0% duty cycle
        self.pwm_low.start(0)   # Start PWM with 0% duty cycle

    def set_pwm_pulse(self, pulse_width_ms):


        if pulse_width_ms > 0:
            GPIO.output(self.pwm_high_pin, GPIO.HIGH)
            GPIO.output(self.pwm_low_pin, GPIO.LOW)
        elif pulse_width_ms < 0:
            GPIO.output(self.pwm_high_pin, GPIO.LOW)
            GPIO.output(self.pwm_low_pin, GPIO.HIGH)
        else:
            GPIO.output(self.pwm_high_pin, GPIO.LOW)
            GPIO.output(self.pwm_low_pin, GPIO.LOW)


        pulse_width_ms = abs(pulse_width_ms)


        # Ensure pulse width is within the range of 1-2 ms
        pulse_width_ms = max(min(pulse_width_ms, 2.4), 1.055)

        if pulse_width_ms == 2.4:
            pulse_width_ms = 0
        
        # Convert pulse width to duty cycle
        duty_cycle = (pulse_width_ms) / 20* 100
        
        # Set duty cycle for PWM signal
        print("DUTY CYCLE: " + str(duty_cycle))
        self.pwm_high.ChangeDutyCycle(duty_cycle)

if __name__ == "__main__":
    from baseinputs import Controller


    talon = TalonSRX(3, 4)
    controller = Controller()

    try:
        while True:
            values = controller.read()

            if values["y"]:
                print("GPIO Clean up")
                break
            

            triggervalue = values["sx"]
            print("TRIGGER: " + str(triggervalue))

            movement = 2.4 - (abs(triggervalue) * 1.34)
            if triggervalue < 0:
                movement *= -1

            print("PULSE INPUT: " + str(movement))
            talon.set_pwm_pulse(movement)
            time.sleep(0.2)  # Sleep to avoid continuous updates (adjust as needed)

    finally:
        # Clean up GPIO on exit
        GPIO.cleanup()
