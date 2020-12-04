from ReedCtr import ReedController
import time

controller = ReedController(21)

last_state = False

while True:
    current_state = controller.is_on()
    if last_state == current_state:
        if current_state:
            print('Switch turned on')
        else:
            print('Switch turned off')
    time.sleep(0.1)

controller.cleanup()
