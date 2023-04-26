import os
import pygame
pygame.init()

class Dude:
    def __init__(self, start_i, start_j):
        self.type = 4
        self.i = start_i
        self.j = start_j
        self.id = "dude"
        self.dir = "right"
        self.set_img()

    def set_img(self):
        self.img = pygame.image.load(os.path.join("assets", f"dude_{self.dir}.png"))

    def set_dir(self, dir):
        self.dir = dir
        self.set_img()