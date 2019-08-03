import numpy as np

class Zobrist():
    def __init__(self):
        self.zobristTable = None
        self.zobristValue = None
        self.initZobrist()
        self.historyTable = {}
        
    def initZobrist(self):
        self.zobristTable = np.random.rand(3,15,15)
        self.zobristTable.dtype = 'uint64'

        self.zobristValue = np.bitwise_xor.reduce(np.bitwise_xor.reduce(self.zobristTable[2]))
