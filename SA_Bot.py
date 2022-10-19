from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from Heuristic_Value import *
from Support_Function import *
import random
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
        current_state = modify_state(state, current_marking)
        
        while (time.time() - start_time < self.__BOT_TIMEOUT_SECOND):
            print(">>> Iteration")
            print(state.board_status)
            current_temp = cooling_temp(current_temp)
            if (current_temp == 0):
                return current_marking
                
            neighbor_marking = local_random_marking(state, current_marking)
            # neighbor_marking = global_random_marking(state)
            neighbor_state = modify_state(state, neighbor_marking)
            E_neighbor, sh_n = obj_func(state, neighbor_marking)
            E_current, sh_c = obj_func(state, current_marking)

            print("  " + ">>> Neighbor")
            print("  " * 2 + f"Action={neighbor_marking.action_type} pos=({neighbor_marking.position})")
            print("  " * 2 + f"E_neighbor={E_neighbor}")
            print(sh_n)
            print("  " + "<<< Neighbor")

            print("  >>> Current")
            print(f"    Action={current_marking.action_type} pos=({current_marking.position})")
            print(f"    E_current={E_current}")
            print(sh_c)
            print("  <<< Current")
            print("<<< Iteration")
            
            delta_E = E_neighbor - E_current
            if (delta_E > 0):
                current_marking = neighbor_marking
                current_state = neighbor_state
            # elif 2.71828 ** round(delta_E / current_temp, 3) > random.random():
            elif 2.71828 ** round(delta_E / current_temp, 3) > 0.85:
                # print(f"Elif p = {2.71828} ** {round(delta_E / current_temp, 3)}")
                print(f"Elif p = {2.71828} ** ({delta_E} / {current_temp}) = {2.71828 ** round(delta_E / current_temp, 3)}")
                current_marking = neighbor_marking
                current_state = neighbor_state
            else:
                print(f"Elif p = {2.71828} ** ({delta_E} / {current_temp}) = {2.71828 ** round(delta_E / current_temp, 3)}")

        
        return current_marking

