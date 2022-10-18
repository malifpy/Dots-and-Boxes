from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from typing import Tuple
import copy
import numpy as np

#disini untuk kedalaman pertama menggunaakn minimax dan kedalaman berikutnya baru menggunakan alpha beta

class RandomBot(Bot):
    def __init__(self) -> None:
        super().__init__()
        print("Silakan masukkan kedalaman yang diinginkan (>0)")
        self.__kedalaman = int(input())
        while (self.__kedalaman <= 0 ) :
            print("Silakan masukkan kedalaman yang diinginkan")
            self.__kedalaman = int(input())

    def get_action(self, state: GameState) -> GameAction:
        #Menyimpan informasi parrent state (parent tree)
        parrent_state = copy.deepcopy(state)
        print("state parrent")
        print(parrent_state)
        kedalaman = self.__kedalaman
        #Menyimpan informasi initial minimum score dan aksi yang nanti akan dikerjakan si bot
        minimum_score = 1000
        status = ""
        a = 0
        b = 0

        #untuk setiap row akan dicek mana yang belum diberi garis
        status = "row"
        print(status)
        i = 0
        j = 0
        print(i,j)
        for i in range (4) :
            for j in range (3) :
                if (parrent_state.row_status[i][j] == 0): #jika ditemukan bagian belum digaris
                    #dicek kedalaman tree (ini bakal ada perubahan)
                    if kedalaman < 1 :
                        return (GameAction(status, (i,j)))
                    #simpan aksi yang dilakukan dan state setelah melakukan aski tersebut
                    temp_action = GameAction(status, (i,j)) #lakukan aksi pada bagian itu
                    print(temp_action)
                    temp_state_action = self.__modify_state(parrent_state, temp_action)
                    #lanjut ke kedalaman berikutnya
                    result = self.__maximum(temp_state_action, temp_action, kedalaman-1, minimum_score)
                    #akan dicek nilai costnya secara minimax
                    if minimum_score > result :
                        minimum_score = result
                        a = i
                        b = j

        #untuk setiap col akan dicek mana yang belum diberi garis
        status = "col"
        print(status)
        i = 0
        j = 0
        print(i,j)
        for i in range (3) :
            for j in range (4) :
                if (parrent_state.col_status[i][j] == 0): #jika ditemukan bagian belum digaris
                    #dicek kedalaman tree (ini bakal ada perubahan)
                    if kedalaman < 1 :
                        return (GameAction(status, (i,j)))
                    #simpan aksi yang dilakukan dan state setelah melakukan aski tersebut
                    temp_action = GameAction(status, (i,j)) #lakukan aksi pada bagian itu
                    print(temp_action)
                    temp_state_action = self.__modify_state(parrent_state, temp_action)
                    result = self.__maximum(temp_state_action, temp_action, kedalaman-1, minimum_score)
                    #akan dicek nilai costnya secara minimax
                    if minimum_score > result :
                        minimum_score = result
                        a = i
                        b = j

        return (GameAction(status, (a,b)))

    def __maximum(self, state_action: GameState, action: GameAction, kedalaman, alpha):
        parrent_state = copy.deepcopy(state_action)
        print("maximum")
        print("state parrent")
        print(parrent_state)

        if kedalaman == 0:
            return (self.__obj_func(parrent_state, action)) #mengembalikan nilai cost pada keadaan sekarang

        #Menyimpan informasi initial maximum score dan aksi yang nanti akan dikerjakan si bot
        maximum_score = -1000
        status = ""
        
        #untuk setiap row akan dicek mana yang belum diberi garis
        status = "row"
        print(status)
        i = 0
        j = 0
        print(i,j)
        for i in range (4) :
            for j in range (3) :
                if (parrent_state.row_status[i][j] == 0): #jika ditemukan bagian belum digaris
                    #simpan aksi yang dilakukan dan state setelah melakukan aski tersebut
                    temp_action = GameAction(status, (i,j)) #lakukan aksi pada bagian itu
                    print(temp_action)
                    temp_state_action = self.__modify_state(parrent_state, temp_action)
                    #lanjut ke kedalaman berikutnya
                    result = self.__minimum(temp_state_action, temp_action, kedalaman-1, maximum_score) #lakukan rekursif
                    #akan dicek nilai costnya secara alpha-beta pruning
                    if maximum_score < result :
                        maximum_score = result
                    if result > alpha :
                        return result

        #untuk setiap col akan dicek mana yang belum diberi garis
        status = "col"
        print(status)
        i = 0
        j = 0
        print(i,j)
        for i in range (3) :
            for j in range (4) :
                if (parrent_state.col_status[i][j] == 0): #jika ditemukan bagian belum digaris
                    #simpan aksi yang dilakukan dan state setelah melakukan aski tersebut
                    temp_action = GameAction(status, (i,j)) #lakukan aksi pada bagian itu
                    print(temp_action)
                    temp_state_action = self.__modify_state(parrent_state, temp_action)
                    #lanjut ke kedalaman berikutnya
                    result = self.__minimum(temp_state_action, temp_action, kedalaman-1, maximum_score) #lakukan rekursif
                    #akan dicek nilai costnya secara alpha-beta pruning
                    if maximum_score < result :
                        maximum_score = result
                    if result > alpha :
                        return result

        return (maximum_score)

    def __minimum(self, state_action: GameState, action: GameAction, kedalaman, beta):
        parrent_state = copy.deepcopy(state_action)
        print("minimum")
        print("state parrent")
        print(parrent_state)

        if kedalaman == 0:
            return (self.__obj_func(parrent_state, action)) #mengembalikan nilai cost pada keadaan sekarang

        #Menyimpan informasi initial maximum score dan aksi yang nanti akan dikerjakan si bot
        minimum_score = 1000
        status = ""
        
        #untuk setiap row akan dicek mana yang belum diberi garis
        status = "row"
        i = 0
        j = 0
        print(i,j)
        for i in range (4) :
            for j in range (3) :
                if (parrent_state.row_status[i][j] == 0): #jika ditemukan bagian belum digaris
                    #simpan aksi yang dilakukan dan state setelah melakukan aski tersebut
                    temp_action = GameAction(status, (i,j)) #lakukan aksi pada bagian itu
                    print(temp_action)
                    temp_state_action = self.__modify_state(parrent_state, temp_action)
                    #lanjut ke kedalaman berikutnya
                    result = self.__maximum(temp_state_action, temp_action, kedalaman-1, minimum_score) #lakukan rekursif
                    #akan dicek nilai costnya secara alpha-beta pruning
                    if minimum_score > result :
                        minimum_score = result
                    if result < beta :
                        return result

        #untuk setiap col akan dicek mana yang belum diberi garis
        status = "col"
        i = 0
        j = 0
        print(i,j)
        for i in range (3) :
            for j in range (4) :
                if (parrent_state.col_status[i][j] == 0): #jika ditemukan bagian belum digaris
                    #simpan aksi yang dilakukan dan state setelah melakukan aski tersebut
                    temp_action = GameAction(status, (i,j)) #lakukan aksi pada bagian itu
                    print(temp_action)
                    temp_state_action = self.__modify_state(parrent_state, temp_action)
                    #lanjut ke kedalaman berikutnya
                    result = self.__maximum(temp_state_action, temp_action, kedalaman-1, minimum_score) #lakukan rekursif
                    #akan dicek nilai costnya secara alpha-beta pruning
                    if minimum_score > result :
                        minimum_score = result
                    if result < beta :
                        return result

        return (minimum_score)

    def __modify_state(self, state: GameState, action: GameAction) -> GameState:
        modfied_state = copy.deepcopy(state)
        x = action.position[0]
        y = action.position[1]
        if (action.action_type == "row"):
            modfied_state.row_status[x][y] = 1
        elif (action.action_type == "col"):
            modfied_state.col_status[x][y] = 1
        return modfied_state

    """ Heuristic Functions """
    def __get_ud_status_row(self, state: GameState, position: Tuple[int, int]):
        [max_y, max_x] = state.board_status.shape
        (px, py) = position
        print("posisi aksi di get ud status", position)
        #print(position)
        if (py - 1 < 0):
            up_status = np.nan
        else:
            up_status = state.board_status[px][py - 1]

        if (py >= max_y):
            down_status = np.nan
        else:
            down_status = state.board_status[px][py]

        #print("status row", up_status, down_status)
        return np.array([up_status, down_status])

    def __get_lr_status_col(self, state: GameState, position: Tuple[int, int]):
        [max_y, max_x] = state.board_status.shape
        (px, py) = position
        #print(position)
        if (px - 1 < 0):
            left_status = np.nan
        else:
            left_status = state.board_status[px - 1][py]

        if (px >= max_x):
            right_status = np.nan
        else:
            right_status = state.board_status[px][py]

        #print("status col", left_status, right_status)
        return np.array([left_status, right_status])

    def __has_extra_move(self, state: GameState, action: GameAction):
        #print(action)
        if action.action_type == "row":
            #print("menjalankan fungsi __get_ud_status_row")
            adjacent_status = self.__get_ud_status_row(state, action.position)
        else:
            #print("menjalankan fungsi __get_lr_status_col")
            adjacent_status = self.__get_lr_status_col(state, action.position)

        #print(np.any(np.absolute(adjacent_status) + 1 == 4))
        return np.any(np.absolute(adjacent_status) + 1 == 4)

    def __box_eval(self, box_status: int, is_extra_turn: bool = False):
        if box_status == 4:
            return 2
        elif box_status == -4:
            return 2
        elif box_status == 0:
            return 0
        else:
            box_side = abs(box_status)
            if box_side == 1:
                return -1
            elif box_side == 2:
                return -1
            else:
                return (int(is_extra_turn) * 2 - 1) * 2

    def __obj_func(self, modified_state: GameState, marked_position: GameAction):
        #print(marked_position)
        #print("menjalankan fungsi __has_extra_move")
        has_extra_turn = self.__has_extra_move(modified_state, marked_position)
        total_score = 0
        for box_status_row in modified_state.board_status:
            for box_status in box_status_row:
                #print("menjalankan fungsi __box_eval")
                total_score += self.__box_eval(box_status, has_extra_turn)
        return total_score
