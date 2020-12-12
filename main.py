from ReedCtr import ReedController
import asyncio
import time

controller = ReedController(21)


@controller.event
async def on_switch(is_on):
    print()


controller.run()
