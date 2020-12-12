
try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils
    fake_rpigpio.utils.install()
    import RPi.GPIO as GPIO


class pwmController:

    def __init__(self, gpio_port: int, freq: int):
        GPIO.setmode(GPIO.BCM)
        self.duty = 0
        self.__em_channel = gpio_port

        print("setting up gpio controller on channel " + str(self.__em_channel))

        GPIO.setup(self.__em_channel, GPIO.OUT)
        self.pwm = GPIO.PWM(self.__em_channel, freq)
        self.pwm.start(0)

    def set_duty(self, duty: int):
        print(f'turning on gpio channel {self.__em_channel}')
        self.pwm.ChangeDutyCycle(duty)
        self.duty = duty

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()
        self.duty = 0
