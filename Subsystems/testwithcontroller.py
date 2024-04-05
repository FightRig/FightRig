import signal
from baseinputs import Controller
from testwithcontroller import SPX

v1 = SPX(4, 5)
controller = Controller()

while 1:
    values = controller

    if values["y"]:
        print("GPIO Clean up")
        break

    movement = values["movement"]
    v1.set_pwm_pulse(movement * 2)
