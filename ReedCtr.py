import asyncio
import time

try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils
    fake_rpigpio.utils.install()
    import RPi.GPIO as GPIO


class ReedController:

    def __init__(self, gpio_port: int):
        GPIO.setmode(GPIO.BCM)
        self.__em_channel = gpio_port

        print("setting up gpio controller on channel " + str(self.__em_channel))

        GPIO.setup(self.__em_channel, GPIO.IN)

        self.last_state = False

    def run(self):
        try:
            while True:
                current_state = self.__is_on()
                if self.last_state != current_state:
                    if current_state:
                        print('Switch turned on')
                    else:
                        print('Switch turned off')
                self.last_state = current_state
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.__cleanup()

    def __is_on(self):
        #print(f'checking voltage on channel {self.__em_channel}')
        return GPIO.input(self.__em_channel)

    def __cleanup(self):
        GPIO.cleanup()
