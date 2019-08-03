from hash import Zobrist
import math
import time
import copy

class Node():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.parent = None
        self.children = []
        self.status = '-1'

class AI():
    def __init__(self, arrayBoard):
        self.arrayBoard = arrayBoard
        self.dictScore = {
        '00000': 100000,   # 活五  
        'x0000x': 10000,   # 活四
        '10000x': 500,     # 衝四1
        '0x000': 500,      # 衝四2
        '00x00': 500,      # 衝四3
        'x000x': 200,      # 活三1
        'x0x00x': 200,     # 活三2
        '1000xx': 50,      # 眠三1
        '100x0x': 50,      # 眠三2
        '10x00x': 50,      # 眠三3
        '00xx0': 50,       # 眠三4
        '0x0x0': 50,       # 眠三5
        '1x000x1': 50,     # 眠三6
        'xx00xx': 5,       # 活二1
        'x0x0xx': 5,       # 活二2
        'x0xx0x': 5,       # 活二3
        '100xxx': 3,       # 眠二1
        '10x0xx': 3,       # 眠二2
        '10xx0x': 3,       # 眠二3
        '0xxx0': 3,        # 眠二4
        '1x00xx1': 3,      # 眠二5
        '1x0x0x1': 3,      # 眠二6
        '1001': -1,        # 死二
        '1x01': -1,        # 死二
        '10001': -10,      # 死三
        '1x001': -10,      # 死三
        '10x01': -10,      # 死三
        '100001': -100,    # 死四
        '1x0001': -100,    # 死四
        '10x001': -100
        } 
    
    def evaluateNode(self, player, row, col):
        index_direction=0
        evaluatelist = [['x']*7 for _ in range(8)]
        for rowOffset in range(-1,2):
            for colOffset in range(-1,2):
                if rowOffset==0 and colOffset==0:
                    continue
                for index_status in range(7):
                    if row+rowOffset*index_status<0 or row+rowOffset*index_status>=15 or col+colOffset*index_status<0 or col+colOffset*index_status>=15:
                        evaluatelist[index_direction][index_status] = '1'
                    else:
                        evaluatelist[index_direction][index_status] = self.arrayBoard[row+rowOffset*index_status][col+colOffset*index_status]
                index_direction+=1    
            
        evaluateString = []
        for i in range(4):
            evaluatelist[7-i].reverse()
            evaluatelist[i][:0] = evaluatelist[7-i][:4]
            evaluateString.append(''.join(evaluatelist[i]))

        reward = 0
        isEnd = False
        for type in self.dictScore:
            for s in evaluateString:
                if type in s or type[::-1] in s:
                    reward += self.dictScore[type]
                    isEnd = True
            if isEnd: return reward
        return reward

    def alphabeta(self, zobrist, node, depth, alpha, beta, player):
        if depth == 0:
            if zobrist.zobristValue in zobrist.historyTable:
                return zobrist.historyTable[zobrist.zobristValue]
            else:
                result = self.evaluateNode(1-player, node.parent.row, node.parent.col)
                zobrist.historyTable[zobrist.zobristValue] = result
                return result

        if player == 0:     # Max(computer)
            v = float('-inf')   # alpha
            for child in node.children:
                child.parent = node
                child.children = copy.copy(node.children)
                child.children.remove(child)
                self.arrayBoard[node.row][node.col] = str(player)
                zobrist.zobristValue ^= zobrist.zobristTable[2][node.row][node.col] 
                zobrist.zobristValue ^= zobrist.zobristTable[player][node.row][node.col] 
                v = max(v, self.alphabeta(zobrist, child, depth-1, alpha, beta, 1))
                zobrist.zobristValue ^= zobrist.zobristTable[player][node.row][node.col] 
                zobrist.zobristValue ^= zobrist.zobristTable[2][node.row][node.col]
                self.arrayBoard[node.row][node.col] = 'x'
                alpha = max(alpha, v)   
                if alpha >= beta:
                    return v
            return v
        else:                # Min(player)
            v = float('inf')    # beta
            for child in node.children:
                child.parent = node
                child.children = copy.copy(node.children)
                child.children.remove(child)
                self.arrayBoard[node.row][node.col] = str(player)
                zobrist.zobristValue ^= zobrist.zobristTable[2][node.row][node.col] 
                zobrist.zobristValue ^= zobrist.zobristTable[player][node.row][node.col]
                v = min(v, self.alphabeta(zobrist, child, depth-1, alpha, beta, 0))
                zobrist.zobristValue ^= zobrist.zobristTable[player][node.row][node.col] 
                zobrist.zobristValue ^= zobrist.zobristTable[2][node.row][node.col]
                self.arrayBoard[node.row][node.col] = 'x'
                beta = min(beta, v)
                if alpha >= beta:
                    return v
            return v
        
        # v = float('-inf')   # alpha
        # for child in node.children:
        #     child.parent = node
        #     child.children = copy.copy(node.children)
        #     child.children.remove(child)
        #     self.arrayBoard[node.row][node.col] = str(player)
        #     v = max(v, -self.alphabeta(child, depth-1, beta, alpha, (1-player)))
        #     self.arrayBoard[row][col] = 'x'   # 拿掉棋子，因為進去不一定是depth=0
        #     alpha = max(alpha, v)
        #     if alpha >= beta:
        #         return v
        # return v

arrayBoard = [
['x','0','0','0','x','x','x','x','x','x','x','x','x','x','x'],
['x','1','x','x','x','x','x','x','x','x','x','x','x','x','x'],
['x','x','1','x','x','x','x','x','x','x','x','x','x','x','x'],
['x','x','x','1','x','x','x','x','x','x','x','x','x','x','x'],
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
['x','x','x','x','x','x','x','1','x','x','x','x','x','x','x'],
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
]
legalNode = []
for row in range(15):
    for col in range(15):
        if arrayBoard[row][col] == 'x':
            legalNode.append(Node(row,col))

#---#
zobrist = Zobrist()
#---#

ai = AI(arrayBoard)

choosingIndex = float('-inf')
start = time.time()
for node in legalNode:
    node.children = copy.copy(legalNode)
    node.children.remove(node)
    # ai.arrayBoard[node.row][node.col] = '0'
    temp = ai.alphabeta(zobrist, node, 3, float('-inf'), float('inf'), 0)
    # print('Row', node.row, 'Col', node.col, temp)
    if temp > choosingIndex:
        choosingIndex = temp
        rowAI = node.row
        colAI = node.col
print('Row', rowAI, 'Col', colAI)
end = time.time()
print(end-start,' s')
