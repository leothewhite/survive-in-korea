import pygame


# Player 객체를 정의한다
class Character(pygame.sprite.Sprite):
    # 처음 생성 시 img만 받아서 생성
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()

    # position 값을 받아서 움직이기
    def update(self, pos):
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class Border(pygame.sprite.Sprite):
    def __init__(self, img, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self, pos):
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
