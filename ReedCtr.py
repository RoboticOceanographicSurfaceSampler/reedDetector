import asyncio
import time

# if running in dev environment install fake_rpigpio to allow simulation of RPi.GPIO
# checks if RPi.GPIO is available and if not imports fake_rpigpio as RPi.GPIO
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

    # setup defaults for function name attributes
    __on_switch = None

    def event(self, coro):

        """
        Functions are called asynchronously to allow long running operations
        (or just asyncio.sleep so timed events don't have to register callbacks)
        Because of this functions must be a coroutine

        Functions are called by their name (ex on switch callback on_switch() is called)
        if a function isn't implemented it will just be ignored
        if a function is registered twice only the first will be called
        list of currently implemented events:

        Switch state changed: on_switch(switchstate: bool)


        """
        # raise TypeError if not coroutine
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('event registered must be a coroutine function')
        # set attribute for function name
        print(f'registering function {coro.__name__}')
        setattr(self, '__' + coro.__name__, coro)

    loop = asyncio.get_event_loop()

    def __dispatch(self, coro, param):
        # do nothing if none
        if coro is None:
            print('coro is none')
            return
        # check which callback to dispatch - will be dispatched during await in main loop
        if coro.__name__ == 'on_switch':
            self.loop.create_task(coro(param))

    """blocking call which start main loop and allows for call backs coroutines to be added to the loop"""
    def run(self):
        # create asyncio loop and start the main thread which watches reed detector
        self.loop.create_task(self.__main_loop())

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.__cleanup()

    """main loop checks for reed switch and if state changes schedules the coroutine to be executed"""
    async def __main_loop(self):
        while True:
            current_state = self.__is_on()
            if self.last_state != current_state:
                if current_state:
                    '''switch turned on'''
                    self.__dispatch(getattr(self, '__on_switch'), True)
                else:
                    '''switch turned off'''
                    self.__dispatch(getattr(self, '__on_switch'), False)
            self.last_state = current_state
            await asyncio.sleep(.1)

    def __is_on(self):
        return GPIO.input(self.__em_channel)

    def __cleanup(self):
        print('control c pressed, cleaning up gpio before exit')
        GPIO.cleanup()
