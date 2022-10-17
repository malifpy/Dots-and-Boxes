from GameAction import *
from GameState import *
from Node import *
from Bot import *
import numpy as np
import time

class MinimaxBot(Bot): # masih rada ngaco karna belum kepikiran cara bikin treenya
    def __init__(self) -> None:
        super().__init__()
        self.__BOT_TIMEOUT_SECOND = 5

    def minimax(self, root : Node, alpha : int , beta : int, depth : int, isMax : bool) -> int:
        start = time.time()
        Max = -99999
        Min = 99999
        
        if (depth == 0 ):
            root.evaluated()
            return root.value
        
        while(time.time() - start <= 5):
            if isMax:
                Max = -99999
                for n in root.chidren: #belum implementasi
                    value = self.minimax(n, alpha, beta, depth - 1, isMax) # menggunakan rekursif
                    if(value > Max):
                        Max = value
                    if(Max > alpha):
                        alpha = Max
                    if(beta <= alpha):
                        break;
                root.val = Max;
                return Max;
            else:
                for n in root.children :
                    value = self.minimax(n, alpha, beta, depth - 1, isMax)
                    if(value < Min):
                        Min = value
                    if(Min < beta):
                        beta = Min
                    if(beta <= alpha):
                        break;
                root.val = Min;
                return Min;
            
    def get_action(self, node : Node, depth : int, isMax : bool) -> GameAction: # akan menghasilkan pergerakan yang best, sesuai dengan algoritma minimax keluarannya berupa tuple posisi
        current = [0,0] #random value dari nilai
        Max = -99999
        Min = 99999
        bestmove = minimax(node, Max, Min, depth, isMax)
        for n in node.children:
            if n.value == bestmove:
                current[0] = n.ChangeRow() #implementasi pada node
                current[1] = n.ChangeCols()
                return current
        return current