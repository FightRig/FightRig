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

        self.last_update = time.time()
        self.acceleration = 5.0  # Acceleration rate per second (adjust as needed)
        self.current_duty = .9


    def set_pwm_pulse(self, pulse_width_ms):
        output_pulse_width_ms = abs(pulse_width_ms)

        # output_pulse_width_ms = max(min(output_pulse_width_ms, 2.4), 1.055)

        
        # Convert pulse width to duty cycle
        # Determine target duty cycle
        target_duty = output_pulse_width_ms / 20 * 100  # Forward direction


        acceleration = self.acceleration * (time.time() - self.last_update)

        # Adjust current duty towards target duty with acceleration
        if abs(target_duty - 14.49) < .3:
            self.current_duty = 0
        elif target_duty > self.current_duty:
            if self.current_duty == 0:
                self.current_duty = 14.49
            self.current_duty = min(self.current_duty + acceleration, target_duty)
        elif target_duty < self.current_duty:
            if self.current_duty == 0:
                self.current_duty = 14.49
            self.current_duty = max(self.current_duty - acceleration, target_duty)
        
        # Set duty cycle for PWM signal
        print("DUTY CYCLE: " + str(self.current_duty) + "TARGET: " + str(target_duty))
        self.pwm_high.ChangeDutyCycle(self.current_duty)
        self.last_update = time.time()



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

            movement = 2.9 - (triggervalue * 1.85)
            # if triggervalue < 0:
            #     movement *= -1

            print("PULSE INPUT: " + str(movement))
            talon.set_pwm_pulse(movement)
            time.sleep(0.2)  # Sleep to avoid continuous updates (adjust as needed)

    finally:
        # Clean up GPIO on exit
        GPIO.cleanup()
