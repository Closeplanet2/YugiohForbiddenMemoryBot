from enum import Enum

class States(Enum):
    LOADING = 0
    GEN_HAND_DATA = 1

class StateController:
    def __init__(self):
        self.current_state = States.LOADING

    def TriggerStateMachine(self):
        if self.current_state is States.LOADING:
            self.current_state = States.GEN_HAND_DATA
        elif self.current_state is States.GEN_HAND_DATA:
            self.current_state = States.GEN_HAND_DATA
        return self.current_state