from GameAction import GameAction
from GameState import GameState
from Heuristic_Value import *
from Support_Function import *
from typing import Tuple
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

def is_all_marked(matrix_status: np.ndarray) -> bool:
    """ Check whether a given matrix_status is all marked """
    return np.all(matrix_status == 1)

def cooling_temp(current_temp):
    return current_temp - 5

def local_random_marking(state: GameState, current_marking: GameAction) -> GameAction:
    """
    Return a randomly neighbor-marking action available of current_marking.
    """

    boxes_marking_at = box_positions_marking_at(current_marking)
    return random_box(state, current_marking, boxes_marking_at)

def box_positions_marking_at(current_marking: GameAction) -> list:
    (x, y) = current_marking.position
    box_points = []

    if (current_marking.action_type == "col"):
        box_points.append((x, y)) if x < 3 else None
        box_points.append((x-1, y)) if (x - 1) >= 0 else None
    else:
        box_points.append((x, y)) if y < 3 else None
        box_points.append((x, y-1)) if (y - 1) >= 0 else None
  
    return box_points

def random_box(state: GameState, current_marking: GameAction, boxes_marking_at: list):
    selected_box_pos = random_box_pos_selection(boxes_marking_at)
    (bx, by) = selected_box_pos
  
    if (current_marking.action_type == "row"):
        if (random.random() >= 0.33):
            # Random horizontally (by col)
            selected_box_pos = random_select_neigh_box(state.board_status, y_const = by)
        else: # Random vertically (by row)
            selected_box_pos = random_select_neigh_box(state.board_status, x_const = bx)
  
    else:
        if (random.random() >= 0.33):
            selected_box_pos = random_select_neigh_box(state.board_status, x_const = bx)
        else: # Random horizontally (by col)                
            selected_box_pos = random_select_neigh_box(state.board_status, y_const = by)
          
    selected_marking = random_select_marking(state, selected_box_pos)

    return selected_marking

def random_box_pos_selection(boxes_position: list) -> Tuple[int, int]:
    if (len(boxes_position) > 1):
        posisiton_selected = random.randrange(0, len(boxes_position))
        selected_box_pos = boxes_position[posisiton_selected]
    else: 
        selected_box_pos = boxes_position[0]
  
    return selected_box_pos

def random_select_neigh_box(board_status: np.ndarray, x_const = -1, y_const = -1) -> Tuple[int, int]:
    board_copy = copy.deepcopy(board_status)

    box_valid = False
    # Random horizontally
    if (x_const == -1):
        while not box_valid:
            x = random.randint(0, 2)
            box_valid = abs(board_copy[y_const, x]) != 4
      
        return (x, y_const)
  
    # Random vertically
    else:
        while not box_valid:
            y = random.randint(0, 2)
            box_valid = abs(board_copy[y, x_const]) != 4
      
        return (x_const, y)
  
def random_select_marking(state: GameState, box_position: Tuple[int, int]) -> list:
    (bx, by) = box_position
    (elmt_x, elmt_y) = (-1, -1)

    rows_position_in_box = [(bx, by), (bx, by + 1)]
    cols_position_in_box = [(bx, by), (bx + 1, by)]
    available_marking = []

    for pos in rows_position_in_box:
        (elmt_x, elmt_y) = pos
        if (state.row_status[elmt_y][elmt_x] != 1):
            available_marking.append(("row", pos))
  
    for pos in cols_position_in_box:
        (elmt_x, elmt_y) = pos
        if (state.col_status[elmt_y][elmt_x] != 1):
            available_marking.append(("col", pos))
  
    idx_marking = random.randrange(0, len(available_marking))
    (action_type, position) = available_marking[idx_marking]
  
    return GameAction(action_type, position)
