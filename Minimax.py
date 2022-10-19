from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from typing import Tuple
from Heuristic_Value import *
from Support_Function import *
import copy
import time
import numpy as np

#disini untuk kedalaman pertama menggunaakn minimax dan kedalaman berikutnya baru menggunakan alpha beta

class Minimax(Bot):
    def __init__(self) -> None:
        super().__init__()
        print("Silakan masukkan kedalaman yang diinginkan (>0)")
        self.__kedalaman = 4
        # while (self.__kedalaman <= 0 ) :
        #     print("Silakan masukkan kedalaman yang diinginkan (>0)")
        #     self.__kedalaman = int(input())

    def get_action(self, state: GameState) -> GameAction:
        start_time = time.time()
        #Menyimpan informasi parrent state (parent tree)
        parrent_state = (state)
        kedalaman = self.__kedalaman

        #Menyimpan informasi initial minimum score dan aksi yang nanti akan dikerjakan si bot
        minimum_score = 1000

        #Mengubah row_status dan col_status ke dalam bentuk array sehingga bisa diolah dalam loop
        row_status = np.array(parrent_state.row_status)
        col_status = np.array(parrent_state.col_status)
        status = ""
        a = 0
        b = 0

        i = 0
        j = 0
        for i in range (4) : #baris = sumbu y
            for j in range (4) : #kolom = sumbu x
                if (j != 3) :
                    #untuk setiap row akan dicek mana yang belum diberi garis
                    if ((row_status[i][j]) == 0): #jika ditemukan bagian belum digaris
                        #simpan aksi yang dilakukan dan state setelah melakukan aski tersebut
                        temp_action = GameAction("row", (j,i))
                        print("Aksi rencana yang dilakukan si bot")
                        print(GameAction("row", (j,i)))
                        temp_state_action = modify_state(parrent_state, temp_action)
                        
                        #lanjut ke kedalaman berikutnya dan me-return nilai cost yang didapat
                        result = self.__maximum(temp_state_action, temp_action, kedalaman-1, minimum_score, start_time)

                        #akan dicek nilai costnya secara minimax
                        if minimum_score > result :
                            minimum_score = result
                            status = "row"
                            a = j
                            b = i
                if (i != 3) :
                    #untuk setiap col akan dicek mana yang belum diberi garis
                    if ((col_status[i][j]) == 0): #jika ditemukan bagian belum digaris
                        #simpan aksi yang dilakukan dan state setelah melakukan aski tersebut
                        temp_action = GameAction("col", (j,i))
                        print("Aksi rencana yang dilakukan si bot")
                        print(GameAction("col", (j,i)))
                        temp_state_action = modify_state(parrent_state, temp_action)

                        #lanjut ke kedalaman berikutnya dan me-return nilai cost yang didapat
                        result = self.__maximum(temp_state_action, temp_action, kedalaman-1, minimum_score, start_time)

                        #akan dicek nilai costnya secara minimax
                        if minimum_score > result :
                            minimum_score = result
                            status = "col"
                            a = j
                            b = i

        print("Berikut aksi yang dilakukan si bot")
        print(GameAction(status, (a,b)))
        return (GameAction(status, (a,b)))

    def __maximum(self, state_action: GameState, action: GameAction, kedalaman, alpha, remaining_time):
        if ( time.time() - remaining_time > 5 ) :
            return(alpha)
        #Menyimpan informasi parrent state (parent tree)
        parrent_state = (state_action)

        #Dilakukan pengecekan kedalaman dan cek apakah masih dapat diberi garis atau tidak
        if ( kedalaman == 0 or (np.all(state_action.row_status == 1) and np.all(state_action.col_status == 1)) ) :
            cost = obj_func(parrent_state, action)
            print("Didapat cost pada state tersebut adalah ", cost)
            return (cost) #mengembalikan nilai cost pada keadaan sekarang

        #Menyimpan informasi initial maximum score dan aksi yang nanti akan dikerjakan si bot
        maximum_score = -1000
        row_status = np.array(parrent_state.row_status)
        col_status = np.array(parrent_state.col_status)

        #untuk setiap row akan dicek mana yang belum diberi garis
        i = 0
        j = 0
        for i in range (4) : #baris = sumbu y
            for j in range (4) : #kolom = sumbu x
                if (j != 3) :
                    #untuk setiap row akan dicek mana yang belum diberi garis
                    if ((row_status[i][j]) == 0): #jika ditemukan bagian belum digaris
                        #simpan aksi yang dilakukan dan state setelah melakukan aski tersebut
                        temp_action = GameAction("row", (j,i)) #lakukan aksi pada bagian itu
                        temp_state_action = modify_state(parrent_state, temp_action)

                        #lanjut ke kedalaman berikutnya
                        result = self.__minimum(temp_state_action, temp_action, kedalaman-1, maximum_score, remaining_time)

                        #akan dicek nilai costnya secara alpha-beta pruning
                        if maximum_score < result :
                            maximum_score = result
                        if result > alpha :
                            return result
                if (i != 3) :
                    #untuk setiap row akan dicek mana yang belum diberi garis
                    if ((col_status[i][j]) == 0): #jika ditemukan bagian belum digaris
                        #simpan aksi yang dilakukan dan state setelah melakukan aski tersebut
                        temp_action = GameAction("col", (j,i)) #lakukan aksi pada bagian itu
                        temp_state_action = modify_state(parrent_state, temp_action)

                        #lanjut ke kedalaman berikutnya
                        result = self.__minimum(temp_state_action, temp_action, kedalaman-1, maximum_score, remaining_time)

                        #akan dicek nilai costnya secara alpha-beta pruning
                        if maximum_score < result :
                            maximum_score = result
                        if result > alpha :
                            return result

        return (maximum_score)

    def __minimum(self, state_action: GameState, action: GameAction, kedalaman, beta, remaining_time):
        if ( time.time() - remaining_time > 5 ) :
            return(beta)

        #Menyimpan informasi parrent state (parent tree)
        parrent_state = (state_action)

        #Dilakukan pengecekan kedalaman dan cek apakah masih dapat diberi garis atau tidak
        if ( kedalaman == 0 or (np.all(state_action.row_status == 1) and np.all(state_action.col_status == 1)) ) :
            cost = obj_func(parrent_state, action)
            return (cost) #mengembalikan nilai cost pada keadaan sekarang

        #Menyimpan informasi initial maximum score dan aksi yang nanti akan dikerjakan si bot
        minimum_score = 1000
        row_status = np.array(parrent_state.row_status)
        col_status = np.array(parrent_state.col_status)
        
        #untuk setiap row akan dicek mana yang belum diberi garis
        i = 0
        j = 0
        for i in range (4) : #baris = sumbu y
            for j in range (3) : #kolom = sumbu x
                if (j != 3) :
                    #untuk setiap row akan dicek mana yang belum diberi garis
                    if ( (row_status[i][j]) == 0 ): #jika ditemukan bagian belum digaris
                        #simpan aksi yang dilakukan dan state setelah melakukan aski tersebut
                        temp_action = GameAction("row", (j,i)) #lakukan aksi pada bagian itu
                        temp_state_action = modify_state(parrent_state, temp_action)

                        #lanjut ke kedalaman berikutnya
                        result = self.__maximum(temp_state_action, temp_action, kedalaman-1, minimum_score, remaining_time)

                        #akan dicek nilai costnya secara alpha-beta pruning
                        if minimum_score > result :
                            minimum_score = result
                        if result < beta :
                            return result
                if (i != 3) :
                    #untuk setiap row akan dicek mana yang belum diberi garis
                    if ( (col_status[i][j]) == 0 ): #jika ditemukan bagian belum digaris
                        #simpan aksi yang dilakukan dan state setelah melakukan aski tersebut
                        temp_action = GameAction("col", (j,i)) #lakukan aksi pada bagian itu
                        temp_state_action = modify_state(parrent_state, temp_action)
                        
                        #lanjut ke kedalaman berikutnya
                        result = self.__maximum(temp_state_action, temp_action, kedalaman-1, minimum_score, remaining_time)

                        #akan dicek nilai costnya secara alpha-beta pruning
                        if minimum_score > result :
                            minimum_score = result
                        if result < beta :
                            return result

        return (minimum_score)