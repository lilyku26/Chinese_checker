# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 14:11:56 2019

@author: PrimoKu
"""
import pygame
from search import *

screen = pygame.display.set_mode((960, 720))
pygame.display.set_caption('Chinese Checkers')

#設定視窗座標參數
a = 480
d = 40
#所有棋盤座標list
board_list = []
#設定顏色
black = (0, 0, 0)
Gray = (0, 0, 0)
white = (255, 255, 255)
blue = (65,105,225) 
red = (255,99,71)
light_red = (255,228,225)
light_blue = (240,248,255)
pink = (255, 200, 200)
#圓的大小
r=15 
#走過的點的list
visited = []
#AI的棋子(10個)，要贏的位置list
ai_terminal = []
#Human的棋子(10個)，要贏的位置list
human_terminal = []


class Player:
    def __init__(self, color):
        self.color = color
        self.checkers = []

    #AI下棋
    def make_move(self):
        if is_mixed() is False: #如果上下左右沒有human的棋子，使用a_star
            move = a_star(self.checkers, ai_terminal, human.checkers)
            target = move[0]
            new = move[1]
            pygame.draw.circle(screen, white, target.pos, r, 0)
            pygame.draw.circle(screen, Gray, target.pos, r, 1)
            pygame.draw.circle(screen, blue, new.pos, r, 0)
            for i in range(10):
                if self.checkers[i].pos == target.pos:
                    self.checkers[i] = new
            print("ai has made a a_star move")
        else:  
            move =  alpha_beta(self.checkers, ai_terminal, human_terminal, human.checkers)
            target = move[0]
            new = move[1]
            pygame.draw.circle(screen, white, target.pos, r, 0)
            pygame.draw.circle(screen, Gray, target.pos, r, 1)
            pygame.draw.circle(screen, blue, new.pos, r, 0)
            for i in range(10):
                if self.checkers[i].pos == target.pos:
                    self.checkers[i] = new
            print("ai has made a minimax move")


human = Player(red)
ai = Player(blue)

##設定棋子的走向與移動
class Checker:

    def __init__(self, pos):
        self.pos = pos
        self.moves = []

    def render(self, color):
        pygame.draw.circle(screen, color, self.pos, r, 0)

    def selected(self):
        pygame.draw.circle(screen, light_red, self.pos, r, 0)
        # show possible moves
        human_list = []
        ai_list = []
        for i in range(len(human.checkers)):
            human_list.append(human.checkers[i].pos)
        for i in range(len(ai.checkers)):
            ai_list.append(ai.checkers[i].pos)

        self.moves = []
        self.possible_moves(self.pos, False, 0, ai_list, human_list)

        for i in range(len(self.moves)):
            pygame.draw.circle(screen, pink, self.moves[i], r, 0)
            pygame.draw.circle(screen, Gray, self.moves[i], r, 1)

    def unselected(self):
        pygame.draw.circle(screen, red, self.pos, r, 0)
        #刪除提示位置
        for i in range(len(self.moves)):
            pygame.draw.circle(screen, white, self.moves[i], r, 0)
            pygame.draw.circle(screen, Gray, self.moves[i], r, 1)

    def move(self, new_pos):
        pygame.draw.circle(screen, white, self.pos, r, 0)
        pygame.draw.circle(screen, Gray, self.pos, r, 1)
        pygame.draw.circle(screen, red, new_pos, r, 0)
        self.pos = new_pos
        # 畫新位置，刪除提示位置
        for i in range(len(self.moves)):
            if self.moves[i] != new_pos:
                pygame.draw.circle(screen, white, self.moves[i], r, 0)
                pygame.draw.circle(screen, Gray, self.moves[i], r, 1)
        self.moves = []

    def possible_moves(self, pos, hop, mode, ai_list, human_list):
        global visited
        if mode == 0:
            visited = []

        x = pos[0]
        y = pos[1]

        # 左上
        if is_free([x - 22, y - 40], ai_list, human_list) and hop is False:
            self.moves.append((x - 22, y - 40))
        elif ((x - 22, y - 40) in human_list or (x - 22, y - 40) in ai_list) and (
            x - 22, y - 40) not in visited:
            visited.append((x - 22, y - 40))
            if is_free((x - 22 * 2, y - 40 * 2), ai_list, human_list):
                self.moves.append((x - 22 * 2, y - 40 * 2))
                self.possible_moves((x - 22 * 2, y - 40 * 2), True, 1, ai_list, human_list)

        # 右上
        if is_free((x + 22, y - 40), ai_list, human_list) and hop is False:
            self.moves.append((x + 22, y - 40))
        elif ((x + 22, y - 40) in human_list or (x + 22, y - 40) in ai_list) and (
            x + 22, y - 40) not in visited:
            visited.append((x + 22, y - 40))
            if is_free((x + 22 * 2, y - 40 * 2), ai_list, human_list):
                self.moves.append((x + 22 * 2, y - 40 * 2))
                self.possible_moves((x + 22 * 2, y - 40 * 2), True, 1, ai_list, human_list)

        # 左
        if is_free((x - 44, y), ai_list, human_list) and hop is False:
            self.moves.append((x - 44, y))
        elif ((x - 44, y) in human_list or (x - 44, y) in ai_list) and (x - 44, y) not in visited:
            visited.append((x - 44, y))
            if is_free((x - 44 * 2, y), ai_list, human_list):
                self.moves.append((x - 44 * 2, y))
                self.possible_moves((x - 44 * 2, y), True, 1, ai_list, human_list)

        # 右
        if is_free((x + 44, y), ai_list, human_list) and hop is False:
            self.moves.append((x + 44, y))
        elif ((x + 44, y) in human_list or (x + 44, y) in ai_list) and (x + 44, y) not in visited:
            visited.append((x + 44, y))
            if is_free((x + 44 * 2, y), ai_list, human_list):
                self.moves.append((x + 44 * 2, y))
                self.possible_moves((x + 44 * 2, y), True, 1, ai_list, human_list)

        # 左下
        if is_free((x - 22, y + 40), ai_list, human_list) and hop is False:
            self.moves.append((x - 22, y + 40))
        elif ((x - 22, y + 40) in human_list or (x - 22, y + 40) in ai_list) and (
            x - 22, y + 40) not in visited:
            visited.append((x - 22, y + 40))
            if is_free((x - 22 * 2, y + 40 * 2), ai_list, human_list):
                self.moves.append((x - 22 * 2, y + 40 * 2))
                self.possible_moves((x - 22 * 2, y + 40 * 2), True, 1, ai_list, human_list)

        # 右下
        if is_free((x + 22, y + 40), ai_list, human_list) and hop is False:
            self.moves.append((x + 22, y + 40))
        elif ((x + 22, y + 40) in human_list or (x + 22, y + 40) in ai_list) and (
            x + 22, y + 40) not in visited:
            visited.append((x + 22, y + 40))
            if is_free((x + 22 * 2, y + 40 * 2), ai_list, human_list):
                self.moves.append((x + 22 * 2, y + 40 * 2))
                self.possible_moves((x + 22 * 2, y + 40 * 2), True, 1, ai_list, human_list)
                
    #找各方以移動的棋子離初始點最遠的y
    #最為搜索法語判斷是否相鄰的設定
    def best_vertical_move(self):
        if self is human:  
            ymax = 0
            for i in range(len(self.moves)):
                if self.moves[i][1] > ymax:
                    ymax = self.moves[i][1]
            return ymax
        else:  
            ymin = 700
            for i in range(len(self.moves)):
                if self.moves[i][1] < ymin:
                    ymin = self.moves[i][1]
            return ymin

##使用計算視窗的 x,y 座標，畫出棋盤
def init_board():
    for i in range(0, 4):
        for j in range(i+1):
            board_list.append((a - 22 * i + 44 * j, d * (i + 1)))
    for i in range(4, 9):
        for j in range(17-i):
            board_list.append((a - 22 * (16-i) + 44 * j, d * (i + 1)))
    for i in range(9, 13):
        for j in range(i+1):
            board_list.append((a - 22 * i + 44 * j, d * (i + 1)))
    for i in range(13, 17):
        for j in range(17-i):
            board_list.append((a - 22 * (16-i) + 44 * j, d * (i + 1)))

##畫棋盤
def draw_board():
    #screen.fill(white)
    for i in range(len(board_list)):
        pygame.draw.circle(screen, Gray, board_list[i], r, 1)

##記錄各方棋子的初始值
def init_checkers():
    global ai_terminal, human_terminal

    for i in range(10):
        piece = Checker(board_list[i])
        ai_terminal.append(piece)
    for i in reversed(range(len(board_list)-10, len(board_list))):
        piece = Checker(board_list[i])
        human_terminal.append(piece)

    human.checkers = []
    ai.checkers = []
    for i in range(10):
        piece = Checker(board_list[i])
        piece.render(human.color)
        human.checkers.append(piece)
    for i in reversed(range(len(board_list)-10, len(board_list))):
        piece = Checker(board_list[i])
        piece.render(ai.color)
        ai.checkers.append(piece)
  
##記錄空著的位置
def is_free(pos, ai_list, human_list):
    if pos in board_list and pos not in human_list and pos not in ai_list:
        return True
    else:
        return False

##判別 AI棋子是否與 HUMAN棋子有相鄰
def is_mixed():
    human_max = 0
    ai_min = 700
    human_min = 700
    ai_max = 0
    for i in range(10):
        if human.checkers[i].pos[1] > human_max:
            human_max = human.checkers[i].pos[1]
        if ai.checkers[i].pos[1] < ai_min:
            ai_min = ai.checkers[i].pos[1]

    for i in range(10):
        if human.checkers[i].pos[1] < human_min:
            human_min = human.checkers[i].pos[1]
        if ai.checkers[i].pos[1] > ai_max:
            ai_max = ai.checkers[i].pos[1]
    if (human_min < ai_min and (ai_min - human_max) > 120) or (ai_min < human_min and (human_min - ai_max) > 0):  
        return False
    else:
        return True