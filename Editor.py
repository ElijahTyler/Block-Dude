import Levels as L
import Block as B
import Dude as D
import os
import json
import pygame
pygame.init()
maindir = os.path.dirname(os.path.abspath(__file__))
bkgrddir = os.path.join(maindir, 'assets', 'backgrounds')

current_level = L.Level(8)
new_level = current_level.level_blocks

size = width, height = 24*len(new_level[0]), 24*len(new_level)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Block Dude - Level Editor')

def make_new_level_array(level):
    new_level_array = []
    [new_level_array.append([0]*len(new_level[0])) for i in range(len(new_level))]

    for i in range(len(new_level)):
        for j in range(len(new_level[0])):
            new_level_array[i][j] = level[i][j].type
    
    return new_level_array

while True:
    mouse = pygame.mouse.get_pos()
    mouse_ij = [mouse[1]//24, mouse[0]//24]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            new_dict = {"level": make_new_level_array(new_level)}
            json_object = json.dumps(new_dict)

            with open("newlevel.json", "w") as outfile:
                outfile.write(json_object)

            quit()
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_0, pygame.K_KP0]:
                new_level[mouse_ij[0]][mouse_ij[1]] = B.Block(0)
            if event.key in [pygame.K_1, pygame.K_KP1]:
                new_level[mouse_ij[0]][mouse_ij[1]] = B.Block(1)
            if event.key in [pygame.K_2, pygame.K_KP2]:
                new_level[mouse_ij[0]][mouse_ij[1]] = B.Block(2)
            if event.key in [pygame.K_3, pygame.K_KP3]:
                new_level[mouse_ij[0]][mouse_ij[1]] = B.Block(3)
            if event.key in [pygame.K_4, pygame.K_KP4]:
                new_level[mouse_ij[0]][mouse_ij[1]] = D.Dude(mouse_ij[0], mouse_ij[1])

    screen.fill((255, 255, 255))
    for i in range(len(new_level)):
        for j in range(len(new_level[0])):
            if new_level[i][j].img:
                screen.blit(new_level[i][j].img, (24*j, 24*i))
    pygame.display.flip()