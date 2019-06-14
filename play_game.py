# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 14:22:26 2019

@author: PrimoKu
"""

from chess_board import *
from search import *
import time
import pygame.font

#設定字型
pygame.font.init()
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

#設定顯現文字方塊message
def message_display(text, x, y, size):
    largeText = pygame.font.SysFont("華康pop1體stdw5regular", 20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x, y)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

#設定顯示輸贏的訊息
def game_end(winner):
    if winner is human:
        screen.fill(Light_Yellow, (0, 300, 960, 50))
        message_display('恭喜，你贏了!', 480, 320, 25)    
    else:
        screen.fill(Light_Yellow, (0, 300, 960, 50))
        message_display('你輸了', 480, 320, 100)
    pygame.display.update()

#設定按鈕(悔棋,開始遊戲)
#設定按衂連結滑鼠事件
def button(text, x, y, w, h, light_color, color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, light_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "開始遊戲":
                game_loop()
            elif action == "結束遊戲":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))

    smallText = pygame.font.SysFont("華康pop1體stdw5regular", 20)
    TextSurf, TextRect = text_objects(text, smallText)
    TextRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(TextSurf, TextRect)

#開始頁面
def game_intro():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        background=pygame.image.load("ih1wjr.png") 
        screen.blit(background, (0,0))
        largeText = pygame.font.SysFont("華康pop1體stdw5regular", 50)
        TextSurf, TextRect = text_objects("跳棋遊戲", largeText)
        TextRect.center = (960/2, 200)
        screen.blit(TextSurf, TextRect)

        button("開始遊戲", 250, 350, 120, 50, pink, red, "開始遊戲")
        button("結束遊戲", 650, 350, 120, 50, light_blue, blue, "結束遊戲")
       
        pygame.display.update()

#遊戲loop    
def game_loop():
    global turn
    background=pygame.image.load("ih1wjr.png") 
    screen.blit(background, (0,0))
    draw_board()
    init_checkers()
    selected_checker = None
    turn = 0
    ai_count = 0
    human_count = 0
    ai_time = 0
    intro = "【玩家為「紅色棋子】"
    message_display(intro, 800, 50, 20)
    about1 ="★按滑鼠左鍵選擇想要移動的棋子★"
    message_display(about1, 200, 650,10)
    about2 ="★並點選想移動的位置★"
    message_display(about2, 780, 650,10)
    while True:
        button("悔棋", 50, 50, 100, 50, pink, red)
        button("結束遊戲", 180, 50, 120, 50, light_blue, blue)
        move_string = "移動 " + str(human_count) + "回合"
        time_string = "AI 思考 " + str(ai_time) + "秒"
        screen.fill(white, (30, 140, 150, 40))
        message_display(move_string, 100, 150, 20)
        screen.fill(white, (20, 180, 170, 40))
        message_display(time_string, 100, 200, 20)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            #設定滑鼠事件
            #利用游標位置判斷移動棋子，與所按的button
            #先由 HUMAN 開始移動
            if event.type == pygame.MOUSEBUTTONDOWN and turn == 0:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] < 300 and mouse_pos[1] < 100:
                    button("悔棋", 50, 50, 100, 50, pink, red, "開始遊戲")
                    button("結束遊戲", 180, 50, 120, 50, light_blue, blue, "結束遊戲")

                if selected_checker is None:
                    for i in range(len(human.checkers)):
                        if math.sqrt(math.pow(mouse_pos[0] - human.checkers[i].pos[0], 2) + math.pow(mouse_pos[1] - human.checkers[i].pos[1], 2)) < 20:
                            human.checkers[i].selected()
                            selected_checker = human.checkers[i]
                            break
                else:
                    for i in range(len(board_list)):
                        if math.sqrt(math.pow(mouse_pos[0] - selected_checker.pos[0], 2) + math.pow(mouse_pos[1] - selected_checker.pos[1], 2)) < 20:
                            selected_checker.unselected()
                            selected_checker = None
                            break
                        if math.sqrt(math.pow(mouse_pos[0] - board_list[i][0], 2) + math.pow(mouse_pos[1] - board_list[i][1], 2)) < 20:
                            if board_list[i] in selected_checker.moves:
                                selected_checker.move(board_list[i])
                                #回合數
                                human_count += 1
                                
                                #判別輸贏
                                if is_terminal(human.checkers, human_terminal):
                                    game_end(human)
                                    
                                #如果回合超過40，雙方仍沒有移開棋子，則輸   
                                elif human_count == 40 :
                                    if in_pos(human.checkers,ai_terminal):
                                        game_end(ai)
                                        
                                #若沒有贏，也沒有輸，則換 AI 下棋
                                else:
                                    selected_checker = None
                                    turn = 1
           
                            break
            # AI 移動
            elif turn == 1:  
                t0 = time.time()
                ai.make_move()
                ai_time = round(time.time() - t0, 2)
                print(ai_time)
                turn = 0
                ai_count += 1
                if is_terminal(ai.checkers, ai_terminal):
                    game_end(ai)
                    
        pygame.display.update()        

pygame.init()
init_board()
game_intro()
game_loop()
pygame.quit()
quit()