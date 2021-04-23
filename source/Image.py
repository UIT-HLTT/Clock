import pygame

pygame.init()

class IMG:
    def __init__(self, display_surface, nameIMG, x, y):
        self.display_surface = display_surface
        self.nameIMG = nameIMG
        self.x = x
        self.y = y
        self.img = self.load()
    
    def load(self):
        self.img = pygame.image.load(self.nameIMG)
        return self.img
    
    def render(self):
        self.display_surface.blit(self.img, (self.x, self.y))