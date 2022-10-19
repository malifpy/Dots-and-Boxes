from GameAction import GameAction
from GameState import GameState
from Heuristic_Value import *
from Support_Function import *
import random
import numpy as np
import copy

def modify_state(state: GameState, action: GameAction) -> GameState:
    """ 
    Create a new-copy GameState of a given state which a new state is evaluated by action taken to, 
    i.e., its col_status/row_status and board_status--used for calculating objective/heuristic function.     
    """
    
    modified_state = copy.deepcopy(state)
    _ = make_no_taken_box_abs(modified_state.board_status)
    
    (col_status, row_status) = action.position
    if (action.action_type == "row"):
        modified_state.row_status[row_status][col_status] = 1
        modified_state.board_status[(row_status - 1) if (row_status - 1) >= 0 else 0][col_status] += 1 if (row_status - 1) >= 0 else 0 
        modified_state.board_status[row_status if row_status < 3 else 2][col_status] += 1 if row_status < 3 else 0 
    elif (action.action_type == "col"):
        modified_state.col_status[row_status][col_status] = 1
        modified_state.board_status[row_status][(col_status - 1) if (col_status - 1) >= 0 else 0] += 1 if (col_status - 1) >= 0 else 0
        modified_state.board_status[row_status][col_status if col_status < 3 else 2] += 1 if col_status < 3 else 0
    return modified_state

def make_no_taken_box_abs(board: np.ndarray):
    """ Convert some board element values into absolute value """
    for row in range(3):
        for col in range(3):
            if (board[row][col] < 0 and board[row][col] != -4):
                board[row][col] = abs(board[row][col])
    return None

def global_random_marking(state: GameState) -> GameAction:
    """ Return a random available edge/marking """
    all_row_marked = is_all_marked(state.row_status)
    all_col_marked = is_all_marked(state.col_status)
    if not (all_row_marked or all_col_marked):
        return global_get_random_marking(state)
    elif all_row_marked:
        return global_random_col_marking(state)
    else:
        return global_random_row_marking(state)

def global_get_random_marking(state: GameState) -> GameAction:
    """ Randomly selecting either row or column marking-action  """
    if random.random() < 0.5:
        return global_random_row_marking(state)
    else:
        return global_random_col_marking(state)

def global_random_row_marking(state: GameState) -> GameAction:
    """ Return a row marking-action of any available edges of row """
    position = global_random_position_with_zero_value(state.row_status)
    return GameAction("row", position)

def global_random_col_marking(state: GameState) -> GameAction:
    """ Return a column marking-action of any available edges of column """
    position = global_random_position_with_zero_value(state.col_status)
    return GameAction("col", position)

def global_random_position_with_zero_value(matrix_status: np.ndarray):
    """ Return an available point/edge of a given matrix_status """
    [ny, nx] = matrix_status.shape
    x = -1
    y = -1
    valid = False
    
    while not valid:
        x = random.randrange(0, nx)
        y = random.randrange(0, ny)
        valid = matrix_status[y, x] == 0
    
    return (x, y)

def local_random_marking(state: GameState, current_marking: GameAction) -> GameAction:
    """
        Return a randomly neighbor-marking action available of current_marking.
        Neighbor-marking of current_marking is defined as legal clockwise and counterclockwise rotation "sweeping" areas 
    """
    if (current_marking.action_type == "row"):
        if (random.random() >= 0.43):
            return local_random_row_marking(state.row_status, current_marking)
        else:
            return local_random_col_marking(state.col_status, current_marking)         
    else:
        if (random.random() >= 0.43):
            return local_random_col_marking(state.col_status, current_marking)
        else:
            return local_random_row_marking(state.row_status, current_marking)

def local_random_row_marking(row_state: np.ndarray, current_marking: GameAction) -> GameAction:
    """ Return a row marking-action of any legal available edges """
    (pos_x, pos_y) = copy.deepcopy(current_marking.position)
    if (current_marking.action_type == "row"):
        init_x = pos_x - 1 if (pos_x - 1) >= 0 else 0
        max_x = pos_x + 1 if (pos_x + 1) <= 2 else 2
        init_y = pos_y - 1 if (pos_y - 1) >= 0 else 0
        max_y = pos_y + 1 if (pos_y + 1) <= 3 else 3
    else:
        init_x = pos_x - 1 if (pos_x - 1) >= 0 else 0
        max_x = pos_x if pos_x <= 2 else 2
        init_y = pos_y - 1 if (pos_y - 1) >= 0 else 0
        max_y = pos_y + 2 if (pos_y + 2) <= 3 else 3
        
    if (is_all_marked(row_state[init_y: max_y + 1, init_x: max_x + 1] == 1)):
        return current_marking
    valid = False
    while not valid:
        pos_x = random.randint(init_x, max_x)
        pos_y = random.randint(init_y, max_y)
        valid = row_state[pos_y, pos_x] == 0
    
    return GameAction("row", (pos_x, pos_y))

def local_random_col_marking(col_state: np.ndarray, current_marking: GameAction) -> GameAction:
    """ Return a column marking-action of any legal available edges """
    (pos_x, pos_y) = copy.deepcopy(current_marking.position)
    if (current_marking.action_type == "row"):
        init_x = pos_x - 1 if (pos_x - 1) >= 0 else 0
        max_x = pos_x + 2 if (pos_x + 2) <= 3 else 3
        init_y = pos_y - 1 if (pos_y - 1) >= 0 else 0
        max_y = pos_y if pos_y <= 2 else 2
    else:
        init_x = pos_x - 1 if (pos_x - 1) >= 0 else 0
        max_x = pos_x + 1 if (pos_x + 1) <= 3 else 3
        init_y = pos_y - 1 if (pos_y - 1) >= 0 else 0
        max_y = pos_y + 1 if (pos_y + 1) <= 2 else 2
    
    if (is_all_marked(col_state[init_y: max_y + 1, init_x: max_x + 1] == 1)):
        return current_marking
    
    valid = False
    while not valid:
        pos_x = random.randint(init_x, max_x)
        pos_y = random.randint(init_y, max_y)
        valid = col_state[pos_y, pos_x] == 0
    
    return GameAction("col", (pos_x, pos_y))
def is_all_marked(matrix_status: np.ndarray) -> bool:
    """ Check whether a given matrix_status is all marked """
    return np.all(matrix_status == 1)

def cooling_temp(current_temp):
    return current_temp / 2