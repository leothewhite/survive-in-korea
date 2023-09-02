import pygame
from property import Size, MenuBackground
import os

pygame.font.init()


FONT = pygame.font.Font("./resources/fonts/NeoDunggeunmoPro-Regular.ttf", 30)
BORDER_SIZE = Size(16, 32)
SCREEN_SIZE = Size(640, 480)
BG_SIZE = Size(640, 480)
PLACE_PATH = "./resources/images/place/"
GUAGE_PATH = "./resources/images/guage/"

############### 이미지+스프라이트 로딩 #################

BORDER_IMAGE = pygame.image.load("./resources/images/background/border.png")
BG_IMAGE = pygame.image.load("./resources/images/background/background.png")

# place_path에서 파일들을 받아와서 이미지로 place_image 리스트에 저장
PLACE_IMAGE = [
    (i.split(".")[0], pygame.image.load(PLACE_PATH + i))
    for i in os.listdir(PLACE_PATH)
    if i != ".DS_Store"
]

# guage_path에서 파일들을 받아와서 이미지로 guage_image 딕셔네리에 저장
GUAGE_IMAGE = {
    i.split(".")[0]: pygame.image.load(GUAGE_PATH + i)
    for i in os.listdir(GUAGE_PATH)
    if i != ".DS_Store"
}


MENU_BACKGROUND = MenuBackground()
