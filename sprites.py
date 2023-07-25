import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()

    def update(self, pos):
        self.rect = self.image.get_rect()
        self.rect.center = pos