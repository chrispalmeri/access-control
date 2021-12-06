import gpiod
import config
import state

door = config.chip.get_line(config.door)
aux = config.chip.get_line(config.aux)

door.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_IN)
aux.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_IN)

def check():
    updates = False

    # door check
    if door.get_value() == 0:
        doorTemp = True
    else:
        doorTemp = False

    if state.doorClosed != doorTemp:
        state.doorClosed = doorTemp
        config.logger.debug('Door closed' if state.doorClosed else 'Door opened')
        updates = True

    # aux check
    if aux.get_value() == 0:
        auxTemp = True
    else:
        auxTemp = False

    if state.auxClosed != auxTemp:
        state.auxClosed = auxTemp
        config.logger.debug('Aux closed' if state.auxClosed else 'Aux opened')
        updates = True

    return updates
