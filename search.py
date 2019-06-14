# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 13:02:48 2019

@author: PrimoKu

"""
import math
import copy
##--------------------------------------------------------------------------------------------------------------------------##
##設定搜索法所需要用到的參數##
##(1)最遠距離
def distance_to_goal(player, checkers):
    distance = 0
    #計算到 HUMAN 棋子到最遠終點的距離 (視窗中的位置為：480 , 680)
    if player == "human":  
        for i in range(10):
            distance += math.sqrt(math.pow(checkers[i].pos[0] - 480, 2) + math.pow(checkers[i].pos[1] - 680, 2))
    #計算到 AI 棋子到最遠終點的距離 (視窗中的位置為：480 , 120)
    else:
        for i in range(10):
            distance += math.sqrt(math.pow(checkers[i].pos[0] - 480, 2) + math.pow(checkers[i].pos[1] - 120, 2))
    return distance


##(2) y軸最遠距離
def y_to_goal(player, checkers):
    distance = 0
    # 計算到 HUMAN 棋子的y座標，到最遠終點y座標的距離 (視窗中的位置為y =680)
    if player == "human":  
        for i in range(10):
            distance += abs(680 - checkers[i].pos[1])
    # 計算到 AI 棋子的y座標，到最遠終點y座標的距離 (視窗中的位置為y =40)
    else: 
        for i in range(10):
            distance += abs(checkers[i].pos[1] - 40)
    return distance


##(3)計算棋子到棋盤中線的距離，x = 48
def distance_to_midline(checkers):
    distance = 0
    for i in range(10):
        distance += abs(checkers[i].pos[0] - 480)
    return distance

##(4)設定棋子移動後的垂直距離
def vertical_distance(self, opponent):
    distance = 0 
    self_list = []
    opponent_list = []
    for i in range(len(self)):
        self_list.append(self[i].pos)
    for i in range(len(opponent)):
        opponent_list.append(opponent[i].pos)
    for i in range(10):
        self[i].moves = []
        self[i].possible_moves(self[i].pos, False, 0, self_list, opponent_list)
        distance += abs(self[i].best_vertical_move() - self[i].pos[1])
    return distance

##(5)計算所有棋子在視窗中的平均數值(非x,y座標數值)，並棋子與平均值的距離
def checker_looseness(checkers):
    distance = 0
    c_list = []
    for i in range(len(checkers)):
        g = checkers[i].pos
        c_list.append(g[1])
    average = sum(c_list)/len(c_list)
    for i in range(len(c_list)):
        distance += abs(c_list[i] - average)
    return distance

##(6)計算盤面棋子 y座標的均值: 基本值為40
def eval_value(ai_checkers, human_checkers, ai_terminal, human_terminal):
    return (0.7 * (y_to_goal("human", human_checkers) - y_to_goal("ai", ai_checkers))+ 
            0.2 * (distance_to_midline(human_checkers) - distance_to_midline(ai_checkers)) + 
            0.3 * (vertical_distance(ai_checkers, human_checkers) - vertical_distance(human_checkers, ai_checkers)) + 
            0.2 * (checker_looseness(human_checkers) - checker_looseness(ai_checkers)) + 
            0.1 * (settled_count(ai_checkers, ai_terminal) - settled_count(human_checkers, human_terminal)))

##--------------------------------------------------------------------------------------------------------------------------##
#創建新的list#
def list_to_set(list):
    s = set([])
    for i in range(len(list)):
        s.add(list[i])
    return s

#判別棋子是否移至目標位置#
def is_terminal(current, terminal):
    current_list = []
    terminal_list = []
    u=0
    for j in range(len(current)):
        current_list.append(current[j].pos)
    for i in range(10):
        terminal_list.append(terminal[i].pos)
    for i in range(10):
        if terminal_list[i] in current_list:
            u= u + 1
    if u == 10:
        return True

#判別是否還有棋子在原位#
def in_pos(current,terminal):
    current_list = []
    terminal_list = []
    u=0
    for j in range(len(current)):
        current_list.append(current[j].pos)    
    for i in range(10):
        terminal_list.append(terminal[i].pos)
    for i in range(10):
        if terminal_list[i] in current_list:
            u= u + 1
    if u > 0:
        return True
       
#設定回合數#
def settled_count(current, terminal):
    count = 0
    terminal_list = []
    for i in range(10):
        terminal_list.append(terminal[i].pos)
    for i in range(10):
        if current[i].pos in terminal_list:
            count += 1
    return count

##--------------------------------------------------------------------------------------------------------------------------##
##A-star 搜索
class ANode:
    def __init__(self, checkers, g, h, path):
        self.checkers = checkers
        self.g = g
        self.h = h
        self.path = path

    def actions(self, ai, human):
        #記錄現有10個棋子的座標，並存成list
        checker_states = []  
        ai_list = []
        human_list = []
        for i in range(len(ai)):
            ai_list.append(ai[i].pos)
        for i in range(len(human)):
            human_list.append(human[i].pos)
        for i in range(10):
            self.checkers[i].moves = []
            self.checkers[i].possible_moves(self.checkers[i].pos, False, 0, ai_list, human_list)
            for j in range(len(self.checkers[i].moves)):
                checker_list = copy.deepcopy(self.checkers)
                checker_list[i].pos = self.checkers[i].moves[j]
                checker_states.append(checker_list)
        return checker_states

##如果 AI 的棋子附近沒有玩家的棋子，使用 A_star 搜索
def a_star(initial, terminal, opponent):
    frontier = []
    explored = []
    explored_count = 0
    frontier.append(ANode(initial, 0, heuristic(initial, opponent, terminal), [initial]))
    while frontier:
        i = 0
        for j in range(1, len(frontier)):
            if (frontier[i].g + frontier[i].h) > (frontier[j].g + frontier[j].h):
                i = j
        current = frontier[i]
        path = current.path
        frontier.remove(frontier[i])
        if explored_count == 100 or is_terminal(current.checkers, terminal):
            break
        if current.checkers in explored:
            continue
        for state in current.actions(current.checkers, opponent):
            if state in explored:
                continue
            frontier.append(ANode(state, current.g + 1, heuristic(state, terminal, opponent), current.path + [state]))
        explored.append(current.checkers)
        explored_count += 1
    #可移動的位置list
    move = []
    for i in range(10):
        if path[0][i].pos != path[1][i].pos:
            move.append(path[0][i])
            move.append(path[1][i])
    return move

##審局函數
def heuristic(checkers, terminal, opponent):
    h = 0
    count = settled_count(checkers, terminal)
    h += 0.9 * (0.3 * y_to_goal("ai", checkers) / 40 + 0.15 * distance_to_midline(checkers) / 44 +
                0.1 * checker_looseness(checkers) / 40 - 0.12 * vertical_distance(checkers, opponent) / 40 - 0.1 * count)
    return h

##--------------------------------------------------------------------------------------------------------------------------##
##Alpha- Beta Purning 搜索
class Node:
    def __init__(self, checkers, path):
        self.checkers = checkers
        self.path = path

    def actions(self, ai, human):
        checker_states = []  
        ai_list = []
        human_list = []
        for i in range(len(ai)):
            ai_list.append(ai[i].pos)
        for i in range(len(human)):
            human_list.append(human[i].pos)
        for i in range(10):
            self.checkers[i].moves = []
            self.checkers[i].possible_moves(self.checkers[i].pos, False, 0, ai_list, human_list)
            for j in range(len(self.checkers[i].moves)):
                checker_list = copy.deepcopy(self.checkers)
                checker_list[i].pos = self.checkers[i].moves[j]
                checker_states.append(checker_list)
        return checker_states
maxDepth = 2

def alpha_beta(state, terminal, human_terminal, opponent):
    infinity = float('inf')
    best_val = -infinity
    alpha = -infinity
    beta = infinity
    new_pos = None
    best_move = []
    node = Node(state, [state])
    successors = node.actions(state, opponent)

    for child in successors:
    	value = min_value(child, alpha, beta, terminal, human_terminal, opponent, 1)
    	if value > best_val:
    		best_val = value
    		new_pos = child
    #print("AlphaBeta:  最佳權重 " + str(best_val))
    for i in range(10):
    	if new_pos[i].pos != state[i].pos:
            best_move.append(state[i])
            best_move.append(new_pos[i])

    return best_move

def max_value(state, alpha, beta, terminal, human_terminal, opponent, depth):
    #print(depth)
    global maxDepth
    if terminal_test(state, terminal) or terminal_test(opponent, human_terminal) or depth >= maxDepth:
        d = eval_value(state, opponent, terminal, human_terminal)
        return d
    infinity = float('inf')
    value = -infinity
    node = Node(state, [state])
    successors = node.actions(state, opponent)

    for child in successors:
    	value = max(value, min_value(child, alpha, beta, terminal, human_terminal, opponent, depth+1))
    	if value >= beta:
    		return value
    	alpha = max(alpha, value)

    return value

def min_value(state, alpha, beta, terminal, human_terminal, opponent, depth):
    #print(depth)
    global maxDepth
    if terminal_test(state, terminal) or terminal_test(opponent, human_terminal) or depth >= maxDepth:
        d = eval_value(state, opponent, terminal, human_terminal)
        return d
    infinity = float('inf')
    value = infinity
    node = Node(opponent, [opponent])
    successors = node.actions(opponent, state)

    for child in successors:
    	# print('minnim', len(successors))
    	value = min(value, max_value(state, alpha, beta, terminal, human_terminal, child, depth+1))
    	if value <= alpha:
    		return value
    	beta = min(beta, value)

    return value

def terminal_test(state, terminal):
    s = list_to_set(state)
    t = list_to_set(terminal)
    return s == t
