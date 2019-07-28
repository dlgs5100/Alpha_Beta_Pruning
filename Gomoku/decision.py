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
        self.listScore = [
            ['ooooo',100000],   # 活五
            ['xoooox',10000],   # 活四
            ['|oooox',500],     # 衝四1
            ['oxooo',500],      # 衝四2
            ['ooxoo',500],      # 衝四3
            ['xooox',200],      # 活三1
            ['xoxoox',200],     # 活三2
            ['|oooxx',50],      # 眠三1
            ['|ooxox',50],      # 眠三2
            ['|oxoox',50],      # 眠三3
            ['ooxxo',50],       # 眠三4
            ['oxoxo',50],       # 眠三5
            ['|xooox|',50],     # 眠三6
            ['xxoox',5],        # 活二1
            ['xoxox',5],        # 活二2
            ['xoxxox',5],       # 活二3
            ['|ooxxx',3],       # 眠二1
            ['|oxoxx',3],       # 眠二2
            ['|oxxox',3],       # 眠二3
            ['oxxxo',3],        # 眠二4
            ['|xooxx|',3],      # 眠二5
            ['|xoxox|',3],      # 眠二6
            ['|oo|',-1],        # 死二
            ['|xo|',-1],        # 死二
            ['|ooo|',-10],      # 死三
            ['|xoo|',-10],      # 死三
            ['|oxo|',-10],      # 死三
            ['|oooo|',-100],    # 死四
            ['|xooo|',-100],    # 死四
            ['|oxoo|',-100]     # 死四
        ]
    
    def evaluateNode(self, board, player, row, col):
        index_direction=0
        evaluatelist = [['x']*7 for _ in range(8)]
        for rowOffset in range(-1,2):
            for colOffset in range(-1,2):
                if rowOffset==0 and colOffset==0:
                    continue
                for index_status in range(7):
                    if row+rowOffset*index_status<0 or row+rowOffset*index_status>=15 or col+colOffset*index_status<0 or col+colOffset*index_status>=15:
                        evaluatelist[index_direction][index_status] = '|'
                    else:
                        evaluatelist[index_direction][index_status] = board[row+rowOffset*index_status][col+colOffset*index_status]
                index_direction+=1
        evaluateString = []
        for i in range(4):
            evaluatelist[7-i].reverse()
            evaluatelist[i][:0] = evaluatelist[7-i][:4]
            evaluateString.append(''.join(evaluatelist[i]))
            evaluateString[i] = evaluateString[i].replace('1','|').replace('0','o')
        if player == 0:
                Score = self.listScore
        else:
                Score = reversed(self.listScore)

        reward = 0
        isEnd = False
        for type in Score:
            for s in evaluateString:
                if type[0] in s or type[0][::-1] in s:
                    reward += type[1]
                    isEnd = True
            if isEnd: return reward
        return reward

    def alphabeta(self, board, node, depth, alpha, beta, player): # node = 节点，depth = 深度，maximizingPlayer = 大分玩家
        if depth == 0:
            result = self.evaluateNode(board, 1-player, node.parent.row, node.parent.col)
            return result

        if player == 0:     # Max(computer)
            v = float('-inf')   # alpha
            for child in node.children:
                child.parent = node
                child.children = copy.copy(node.children)
                child.children.remove(child)
                childBoard = copy.deepcopy(board)
                childBoard[node.row][node.col] = str(player)
                v = max(v, self.alphabeta(childBoard, child, depth-1, alpha, beta, 1))
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
                childBoard = copy.deepcopy(board)
                childBoard[node.row][node.col] = str(player)
                v = min(v, self.alphabeta(childBoard, child, depth-1, alpha, beta, 0))
                beta = min(beta, v)
                if alpha >= beta:
                    return v
            return v
        
        # v = float('-inf')   # alpha
        # for child in node.children:
        #     child.children = copy.copy(node.children)
        #     child.children.remove(child)
        #     v = max(v, -self.alphabeta(child, depth-1, -beta, -alpha, (1-player)))
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

ai = AI(arrayBoard)

choosingIndex = float('-inf')
start = time.time()
for node in legalNode:
    node.children = copy.copy(legalNode)
    node.children.remove(node)
    board = copy.deepcopy(ai.arrayBoard)
    temp = ai.alphabeta(board, node, 2, float('-inf'), float('inf'), 0)
    print('row:', node.row, 'col:', node.col, temp)
    if temp > choosingIndex:
        choosingIndex = temp
        rowAI = node.row
        colAI = node.col
print('Row', rowAI, 'Col', colAI)
end = time.time()
print(end-start,' s')
