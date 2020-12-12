from ReedCtr import ReedController
from pwmCtrl import pwmController
import asyncio
import time

reed_ctrl = ReedController(21)

pwm_ctrl = pwmController(18, 1000)


heater_running = False
should_continue = False


@reed_ctrl.event
async def on_switch(is_on):
    global heater_running
    global should_continue

    if heater_running:
        should_continue = True
        return

    heater_running = True
    should_continue = True
    
    pwm_ctrl.set_duty(100)
    print('starting heater loop')

    while should_continue:
        print('heater renewed')
        should_continue = False
        await asyncio.sleep(10)
    
    pwm_ctrl.set_duty(0)
    heater_running = False
    print('ending heater loop')


reed_ctrl.run()
