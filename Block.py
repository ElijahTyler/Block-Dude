import os
import pygame
pygame.init()

class Block:
    def __init__(self, type):
        self.type = type
        self.collide = False if type in [0, 3] else True
        match type:
            case 0:
                self.id = "air"
                self.color = (0, 0, 0)
                self.img = None
            case 1:
                self.id = "brick"
                self.img = pygame.image.load(os.path.join("assets", "brick.png"))
            case 2:
                self.id = "block"
                self.img = pygame.image.load(os.path.join("assets", "block.png"))
            case 3:
                self.id = "goal"
                self.img = pygame.image.load(os.path.join("assets", "door.png"))