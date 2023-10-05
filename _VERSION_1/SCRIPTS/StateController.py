from enum import Enum

class States(Enum):
    LOADING = 1
    STARTING_GAME = 2
    GEN_PLAYER_HAND_DATA = 3
    GEN_COMBINATIONS_FROM_PLAYER_HAND = 4
    END_TURN = 5

class StateController:
    def __init__(self):
        self.state = States.LOADING

    def return_state(self):
        return self.state.name

    def trigger_state_machine(self):
        if self.state == States.LOADING:
            self.state = States.STARTING_GAME
        elif self.state == States.STARTING_GAME:
            self.state = States.GEN_PLAYER_HAND_DATA
        elif self.state == States.GEN_PLAYER_HAND_DATA:
            self.state = States.GEN_COMBINATIONS_FROM_PLAYER_HAND
        elif self.state == States.GEN_COMBINATIONS_FROM_PLAYER_HAND:
            self.state = States.GEN_PLAYER_HAND_DATA
        elif self.state == States.GEN_PLAYER_HAND_DATA:
            self.state = States.END_TURN
        elif self.state == States.END_TURN:
            self.state = States.GEN_PLAYER_HAND_DATA
        return self.state





