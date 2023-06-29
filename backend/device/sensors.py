import gpiod
import config
import state
import broadcast

door = config.CHIP.get_line(config.DOOR)
aux = config.CHIP.get_line(config.AUX)

door.request(consumer=config.NAME, type=gpiod.LINE_REQ_DIR_IN)
aux.request(consumer=config.NAME, type=gpiod.LINE_REQ_DIR_IN)

async def check():
    door_check = bool(door.get_value() == 0)

    if state.doorClosed != door_check:
        state.doorClosed = door_check
        await broadcast.event('INFO', 'Door closed' if state.doorClosed else 'Door opened')

    aux_check = bool(aux.get_value() == 0)

    if state.auxClosed != aux_check:
        state.auxClosed = aux_check
        await broadcast.event('INFO', 'Aux closed' if state.auxClosed else 'Aux opened')
