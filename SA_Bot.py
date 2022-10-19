from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from Heuristic_Value import *
from Support_Function import *
import time

class SA_Bot(Bot):
    def __init__(self) -> None:
        super().__init__()
        self.__BOT_TIMEOUT_SECOND = 5
        self.__INIT_TEMP = 100

    def get_action(self, state: GameState) -> GameAction:
        current_temp = self.__INIT_TEMP
        start_time = time.time()

        current_marking = global_random_marking(state)
        
        while (time.time() - start_time < self.__BOT_TIMEOUT_SECOND):
            current_temp = cooling_temp(current_temp)
            if (current_temp == 0):
                return current_marking
                
            neighbor_marking = local_random_marking(state, current_marking)
            E_neighbor = obj_func(state, neighbor_marking)
            E_current = obj_func(state, current_marking)
            
            delta_E = E_neighbor - E_current
            if (delta_E > 0):
                current_marking = neighbor_marking
            elif 2.71828 ** round(delta_E / current_temp, 3) > 0.85:
                current_marking = neighbor_marking
        
        return current_marking

