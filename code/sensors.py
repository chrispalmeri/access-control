import gpiod
import config
import state
import event

door = config.chip.get_line(config.door)
aux = config.chip.get_line(config.aux)

door.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_IN)
aux.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_IN)

def check():
    # door check
    if door.get_value() == 0:
        doorTemp = True
    else:
        doorTemp = False
    
    if state.doorClosed != doorTemp:
        state.doorClosed = doorTemp
        event.log('Contact closed' if state.doorClosed else 'Contact opened', 'DOOR')
    
    # aux check
    if aux.get_value() == 0:
        auxTemp = True
    else:
        auxTemp = False
    
    if state.auxClosed != auxTemp:
        state.auxClosed = auxTemp
        event.log('Contact closed' if state.auxClosed else 'Contact opened', 'AUX')
