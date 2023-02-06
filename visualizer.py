import pygame
import numpy as np
from time import sleep

import math
TEMP, UNOCCUPIED, PASSED, OCCUPIED, BOMB, BOOST = -1, 0, 1, 2, 3, 4
class Visualizer:
    def __init__(self, size) -> None:
        # self.screen = pygame.display.set_mode((3*N*game_map.width, N*game_map.height))
        ground_w = 16
        ground_h = 10

        self.angle_factor = 2.4
        self.inc = 100
        self.block_width = 16#math.ceil(200*69.19/86.52);
        self.block_height = self.block_width*ground_h/ground_w
        self.block_adj = self.block_height#(self.block_height - 19.08/69.15*self.block_height)-1/200*self.block_height#*(ground_h/ground_w)*


        self.player_width = 8
        self.player_height = 8
        self.map_size = size
        self.WINDOW_HEIGHT = math.ceil(self.block_height*self.map_size) + self.inc#math.ceil(self.block_adj * self.map_size + self.block_height - self.block_adj) + self.inc
        self.WINDOW_WIDTH = self.block_width * self.map_size + self.inc

        self.ground_img = pygame.transform.scale(pygame.image.load('ground5.png'), (self.block_width, self.block_height))
        self.fire_ground = pygame.transform.scale(pygame.image.load('fireGround2.png'), (self.block_width, self.block_height))
        self.water_ground = pygame.transform.scale(pygame.image.load('waterGround.png'), (self.block_width, self.block_height))

        self.p1_img = pygame.transform.scale(pygame.image.load('fireElementEdited.png'), (self.player_width, self.player_height))
        #self.boost_array = pygame.surfarray.array3d(boost_img)
        self.eps = 0


    def init_window(self):

        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self. WINDOW_HEIGHT))
        self.screen.fill((255, 255, 255))
        self.draw_grid()
        pygame.display.update()

    def draw_grid(self):
        # for x in range(0, self.WINDOW_WIDTH, self.block_width):
        #     for y in range(0, self.WINDOW_HEIGHT, self.block_height):
        #         rect = pygame.Rect(x, y, self.block_width, self.block_height)
        #         pygame.draw.rect(self.screen, color.BLACK, rect, 1)
        #self.block_width = self.ground_img.get_rect().x
        #self.block_height = self.ground_img.get_rect().y

        for r in range(self.map_size):
            for c in range(self.map_size):
                if(r > -1 and c > -1):
                    x = (r-c-1)*self.block_width / 2 + self.WINDOW_WIDTH/2
                    y = (r+c)*self.block_height/2 + self.inc/2
                    self.screen.blit(self.ground_img, (x, y))
                    #print(str(r) + ": "  + str(x) + " " + str(c) + ": " + str(y) + "\n")

    def render(self):
        pygame.event.pump()
        pygame.display.update()
        sleep(0.5)

    def update_scene(self, grid, player_num_grid, num_agents, heads):

        self.player_imgs = [(self.p1_img, self.fire_ground),
                            (self.p1_img, self.water_ground)
                            ]

        for r in range(self.map_size):
            for c in range(self.map_size):
                x = self.WINDOW_WIDTH / 2 - self.block_width / 2 + (r - c) * (self.block_width) / 2
                y = self.inc / 2 + (r + c) * (self.block_height) / 2
                #spriteX = x + (self.block_width - self.player_width) / 2
                #spriteY = y - (self.block_height - self.player_height) / 2
                if(x >= self.WINDOW_WIDTH or y >= self.WINDOW_HEIGHT):
                    raise Exception("Out of Bounds Exception")
                if grid[r][c] == PASSED:
                    self.screen.blit(self.player_imgs[player_num_grid[r][c]][1], (x, y))
                elif grid[r][c] == OCCUPIED:
                    self.screen.blit(self.player_imgs[player_num_grid[r][c]][1], (x, y))
                elif grid[r][c] == UNOCCUPIED:
                    self.screen.blit(self.ground_img, (x, y))
        for head in heads:
            hX, hY = head
            x = self.WINDOW_WIDTH / 2 - self.block_width / 2 + (hY - hX) * (self.block_width) / 2 + + (self.block_width - self.player_width) / 2
            y = self.inc / 2 + (hY + hX) * (self.block_height) / 2 - (self.block_height - self.player_height) / 2
            self.screen.blit(self.player_imgs[0][0], (x,y))

                    #print("hi why i no draw :(")
                    #self.screen.blit(self.p1_img, ((r-c)*self.block_width / 2 + (r-c)*(self.block_width-self.player_width)/2 + self.WINDOW_WIDTH/2, 30 + (r+c)*self.block_adj/2))
                #pygame.draw.rect(self.screen, color.BLACK, rect, 1)
                #self.screen.blit(self.bomb_img, (x,y))
                #self.screen.blit(self.ground_img, (x/2, y/2))
                # if grid[r][c] == UNOCCUPIED:
                #     #self.rgb_array[r][c] = WHITE_SMOKE
                #     #pygame.draw.rect(self.screen, color.WHITE, rect, 0)
                #     self.screen.blit(self.ground_img, (x,y))
                # elif grid[r][c] == BOMB:
                #     #self.rgb_array[r][c] = BLACK
                #     self.screen.blit(self.bomb_img, (x,y))
                # elif grid[r][c] == BOOST:
                #     #self.rgb_array[r][c] = PURPLE
                #     self.screen.blit(self.boost_img, (x,y))
                # elif grid[r][c] == PASSED:
                #     #self.rgb_array[r][c] = self.player_colors[player_num_grid[r][c]][0]
                #     #pygame.draw.rect(self.screen, self.player_colors[player_num_grid[r][c]][0], rect, 0)
                #     # pygame.draw.rect(self.screen, color.BLACK, rect, 1)
                #     self.screen.blit(self.player_imgs[player_num_grid[r][c]][0], (x,y))
                # elif grid[r][c] == OCCUPIED:
                #     #self.rgb_array[r][c] = self.player_colors[player_num_grid[r][c]][1]
                #     self.screen.blit(self.player_imgs[player_num_grid[r][c]][1], (x,y))
                # else:
                #     raise Exception("Unknown grid value")
