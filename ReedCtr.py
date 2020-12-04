from RPi import GPIO


class ReedController:

    def __init__(self, gpio_port: int):
        GPIO.setmode(GPIO.BCM)
        self.__em_channel = gpio_port

        print("setting up gpio controller on channel " + str(self.__em_channel))

        GPIO.setup(self.__em_channel, GPIO.IN)

    def is_on(self):
        #print(f'checking voltage on channel {self.__em_channel}')
        return GPIO.input(self.__em_channel)

    def cleanup(self):
        GPIO.cleanup()
