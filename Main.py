import json
import pygame
pygame.init()

import Levels as L
import Block as B
import Dude as D

def view_screen(screen, current_layout):
    sub = pygame.display.set_mode((len(current_layout[0])*24, len(current_layout)*24))
    screen.fill((255, 255, 255))
    for i in range(len(current_layout)):
        for j in range(len(current_layout[0])):
            if current_layout[i][j].type:
                sub.blit(current_layout[i][j].img, (24*j, 24*i))
    pygame.display.flip()
    # wait for user to press a key
    pygame.event.clear()
    pygame.event.wait()
    pygame.event.clear()
    pygame.display.set_mode((432, 288))
    return

def main():
    # visible screen should be 18 block wide, 12 block tall
    screen = pygame.display.set_mode((432, 288))
    level = 1

    def game_loop(level):
        current_level = L.Level(level)
        current_layout = current_level.level_blocks
        current_dude_i, current_dude_j = current_level.get_start_ij()
        last_i, last_j = current_dude_i, current_dude_j
        current_dude = D.Dude(current_dude_i, current_dude_j)
        carry_block = False

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_loop(level)
                        quit()
                    if event.key == pygame.K_TAB:
                        # view_screen(screen, current_layout)
                        pass
                    if event.key == pygame.K_s: # save
                        with open('save.json', 'w') as f:
                            layout_nums = []
                            for i in range(len(current_layout)):
                                layout_nums.append([])
                                for j in range(len(current_layout[0])):
                                    layout_nums[i].append(current_layout[i][j].type)
                            new_dict = {
                                'level': level,
                                'layout': layout_nums,
                                'player': {
                                    'i': current_dude.i,
                                    'j': current_dude.j,
                                    'dir': current_dude.dir,
                                },
                                'carry_block': carry_block,
                                }
                            json.dump(new_dict, f)
                    if event.key == pygame.K_l: # load
                        with open('save.json', 'r') as f:
                            save_dict = json.load(f)
                        level = save_dict['level']
                        current_level = L.Level(save_dict['layout'])
                        current_layout = current_level.level_blocks
                        current_dude_i, current_dude_j = save_dict['player']['i'], save_dict['player']['j']
                        current_dude = D.Dude(current_dude_i, current_dude_j)
                        current_dude.set_dir(save_dict['player']['dir'])
                        carry_block = save_dict['carry_block']
                        pygame.display.flip()
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        last_i, last_j = current_dude.i, current_dude.j
                        current_dude.set_dir(['left','right'][event.key == pygame.K_RIGHT])
                        dj = [-1,1][current_dude.dir == 'right']
                        if not current_layout[current_dude.i][current_dude.j+dj].collide:
                            if carry_block and current_layout[current_dude.i-1][current_dude.j+dj].type != 0:
                                carry_block = False
                                current_layout[current_dude.i-1][current_dude.j] = B.Block(0)
                                current_layout[current_dude.i][current_dude.j] = B.Block(2)
                            current_dude.j += dj
                            
                            while not current_layout[current_dude.i+1][current_dude.j].collide:
                                current_dude.i += 1
                    if event.key == pygame.K_UP:
                        last_i, last_j = current_dude.i, current_dude.j
                        dj = [-1,1][current_dude.dir == 'right']
                        if carry_block:
                            clear_air = current_layout[current_dude.i-2][current_dude.j+dj].type == 0
                        else:
                            clear_air = current_layout[current_dude.i-1][current_dude.j].type == 0
                        if current_layout[current_dude.i][current_dude.j+dj].type and clear_air and not current_layout[current_dude.i-1][current_dude.j+dj].collide:
                            current_dude.i -= 1
                            current_dude.j += dj
                    if event.key == pygame.K_DOWN:
                        # pick up potential block in front of you
                        dj = [-1,1][current_dude.dir == 'right']
                        if carry_block == False:
                            if current_layout[current_dude.i][current_dude.j+dj].type == 2 and current_layout[current_dude.i-1][current_dude.j].type == current_layout[current_dude.i-1][current_dude.j+dj].type == 0:
                                carry_block = True
                                current_layout[current_dude.i-1][current_dude.j] = B.Block(2)
                                current_layout[current_dude.i][current_dude.j+dj] = B.Block(0)
                        # put down block if you're carrying one
                        else:
                            if current_layout[current_dude.i-1][current_dude.j+dj].type == 0:
                                carry_block = False
                                current_layout[current_dude.i-1][current_dude.j] = B.Block(0)
                                zi, zj = current_dude.i-1, current_dude.j+dj
                                while current_layout[zi+1][zj].type == 0:
                                    zi += 1
                                current_layout[zi][zj] = B.Block(2)

            if current_layout[current_dude.i][current_dude.j].id == 'goal':
                if level == 11:
                    print('You win!')
                    quit()
                # increment level
                level += 1
                game_loop(level)
                quit()

            if carry_block:
                current_layout[last_i-1][last_j] = B.Block(0)
                current_layout[current_dude.i-1][current_dude.j] = B.Block(2)

            # use player position to determine what part of the level to draw
            if current_dude.j > len(current_layout[0]) - 9:
                left_bound = len(current_layout[0]) - 18
            else:
                left_bound = max(0, current_dude.j - 9)
            if current_dude.i > len(current_layout) - 6:
                top_bound = len(current_layout) - 12
            else:
                top_bound = min(max(0, current_dude.i - 6), len(current_layout) - 12)

            # draw screen
            screen.fill((255, 255, 255))
            for i in range(12):
                for j in range(18):
                    if current_layout[i+top_bound][j+left_bound].type:
                        screen.blit(current_layout[i+top_bound][j+left_bound].img, (24*j, 24*i))
                    elif current_dude.i == i+top_bound and current_dude.j == j+left_bound:
                        screen.blit(current_dude.img, (24*j, 24*i))
            pygame.display.flip()

    game_loop(level)



if __name__ == "__main__":
    main()