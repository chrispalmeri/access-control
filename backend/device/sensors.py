import gpiod
import config
import state
import broadcast

door = config.chip.get_line(config.door)
aux = config.chip.get_line(config.aux)

door.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_IN)
aux.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_IN)

async def check():
    # door check
    if door.get_value() == 0:
        doorTemp = True
    else:
        doorTemp = False

    if state.doorClosed != doorTemp:
        state.doorClosed = doorTemp
        await broadcast.event('INFO', 'Door closed' if state.doorClosed else 'Door opened')

    # aux check
    if aux.get_value() == 0:
        auxTemp = True
    else:
        auxTemp = False

    if state.auxClosed != auxTemp:
        state.auxClosed = auxTemp
        await broadcast.event('INFO', 'Aux closed' if state.auxClosed else 'Aux opened')

