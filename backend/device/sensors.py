from types import SimpleNamespace
import gpiod
import config
import broadcast

door = config.CHIP.get_line(config.DOOR)
aux = config.CHIP.get_line(config.AUX)

door.request(consumer=config.NAME, type=gpiod.LINE_REQ_DIR_IN)
aux.request(consumer=config.NAME, type=gpiod.LINE_REQ_DIR_IN)

status = SimpleNamespace()
status.door_closed = False
status.aux_closed = False

async def check():
    door_check = bool(door.get_value() == 0)

    if status.door_closed != door_check:
        status.door_closed = door_check
        await broadcast.event('INFO', 'Door closed' if status.door_closed else 'Door opened')

    aux_check = bool(aux.get_value() == 0)

    if status.aux_closed != aux_check:
        status.aux_closed = aux_check
        await broadcast.event('INFO', 'Aux closed' if status.aux_closed else 'Aux opened')
