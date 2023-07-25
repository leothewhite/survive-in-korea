from main import *

def game_play():
    # 참고: https://www.askpython.com/python-modules/pygame-looping-background
    screen.blit(bg, (0, i))
    screen.blit(bg, (0, height+i))
    if (i <= -height+1):
        i = 0
    # 속도
    i -= 0.2*dt