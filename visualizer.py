import pygame
import numpy as np
from time import sleep
import cv2
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
        self.island_height = math.ceil(size * 1/5)
        self.block_adj = self.block_height#(self.block_height - 19.08/69.15*self.block_height)-1/200*self.block_height#*(ground_h/ground_w)*


        self.player_width = self.block_width
        self.player_height = self.player_width
        self.map_size = size
        self.WINDOW_HEIGHT = math.ceil(self.block_height*self.map_size) + self.inc + self.island_height*self.block_height/2#math.ceil(self.block_adj * self.map_size + self.block_height - self.block_adj) + self.inc
        self.WINDOW_WIDTH = self.block_width * self.map_size + self.inc

        self.bomb_img = pygame.transform.smoothscale(pygame.image.load('bomb2.png'), (self.player_width, self.player_height))
        self.boost_img = pygame.transform.smoothscale(pygame.image.load('boost.png'), (self.player_width, self.player_height))
        self.explosion = pygame.transform.smoothscale(pygame.image.load('explosion.png'), (32, 32))

        self.ground_img = pygame.transform.smoothscale(pygame.image.load('bigGround.png'), (self.block_width, self.block_height))
        self.ground_left = pygame.transform.smoothscale(pygame.image.load('16x10 left big.png'), (self.block_width/2, 13/8*self.block_width/2))
        self.ground_right = pygame.transform.smoothscale(pygame.image.load('16x10 rightdark.png'), (self.block_width/2, 13/8*self.block_width/2))

        self.fire_ground = pygame.transform.scale(pygame.image.load('fireGround2.png'), (self.block_width, self.block_height))
        self.water_ground = pygame.transform.scale(pygame.image.load('waterGround.png'), (self.block_width, self.block_height))
        self.earth_ground = pygame.transform.scale(pygame.image.load('earth travel.png'),
                                                  (self.block_width, self.block_height))
        self.air_ground = pygame.transform.scale(pygame.image.load('air travel.png'),
                                                   (self.block_width, self.block_height))

        self.fire_ter = pygame.transform.smoothscale(pygame.image.load('lava ground.png'), (self.block_width, self.block_height))
        self.water_ter = pygame.transform.smoothscale(pygame.image.load('water ground.png'),
                                                     (self.block_width, self.block_height))
        self.earth_ter = pygame.transform.smoothscale(pygame.image.load('earth ground.png'),
                                                      (self.block_width, self.block_height))
        self.air_ter = pygame.transform.smoothscale(pygame.image.load('air ground.png'),
                                                      (self.block_width, self.block_height))



        self.fire_img = pygame.transform.smoothscale(pygame.image.load('fireElementEdited.png'), (self.player_width, self.player_height))
        self.water_img = pygame.transform.smoothscale(pygame.image.load('water element.png'),
                                               (self.player_width, self.player_height))
        self.earth_img = pygame.transform.smoothscale(pygame.image.load('earth element.png'),
                                                      (self.player_width, self.player_height))
        self.air_img = pygame.transform.smoothscale(pygame.image.load('air element.png'),
                                                      (self.player_width, self.player_height))
        self.old_head = {'player_0':(-1,-1), 'player_1':(-1,-1), 'player_2':(-1,-1), 'player_3':(-1,-1)}


    def init_window(self):

        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self. WINDOW_HEIGHT))
        self.screen.fill((173,216,230))
        #self.draw_grid()
        pygame.display.update()

    #helper draw initialize grid
    def draw_grid(self):
        for r in range(self.map_size):
            for c in range(self.map_size):
                x = (r-c-1)*self.block_width / 2 + self.WINDOW_WIDTH/2
                y = (r+c)*self.block_height/2 + self.inc/2
                self.screen.blit(self.ground_img, (x, y))
                if c == self.map_size - 1:
                    if(r < self.island_height):
                        z = r+1
                    else:
                        z = self.island_height
                    for i in range(z):
                        fY = (r+c+i)*self.block_height/2 + self.inc/2
                        self.screen.blit(self.ground_left, (x, fY+self.block_height/2))
                if r == self.map_size - 1:
                    if (c < self.island_height):
                        z = c+1
                    else:
                        z = self.island_height
                    for i in range(z):
                        fY = (r + c + i) * self.block_height / 2 + self.inc / 2
                        self.screen.blit(self.ground_right, (x+self.block_width/2, fY + self.block_height / 2))
                    #print(str(r) + ": "  + str(x) + " " + str(c) + ": " + str(y) + "\n")

    def render(self):
        pygame.event.pump()
        pygame.display.update()
        sleep(0.1)
    def rgbRender(self, rgb):
        self.screen.blit(pygame.surfarray.make_surface(rgb), (0,0))
        pygame.display.update()
        pygame.event.pump()
    def dims(self):
        return [self.WINDOW_WIDTH,self.WINDOW_HEIGHT]
    def update_scene(self, grid, player_num_grid, num_agents, heads):
        self.screen.fill((173,216,230)) # clear canvas

        self.player_imgs = [(self.fire_img, self.fire_ground, self.fire_ter),
                            (self.water_img, self.water_ground, self.water_ter),
                            (self.earth_img, self.earth_ground, self.earth_ter),
                            (self.air_img, self.air_ground, self.air_ter)
                            ]
        self.player_heads = {'player_0':self.fire_img, 'player_1':self.water_img, 'player_2':self.earth_img, 'player_3':self.air_img}
        for r in range(self.map_size):
            for c in range(self.map_size):
                x = self.WINDOW_WIDTH / 2 - self.block_width / 2 + (r - c) * (self.block_width) / 2
                y = self.inc / 2 + (r + c) * (self.block_height) / 2

                if(x >= self.WINDOW_WIDTH or y >= self.WINDOW_HEIGHT):
                    raise Exception("Out of Bounds Exception")
                if grid[r][c] == PASSED:
                    self.screen.blit(self.player_imgs[player_num_grid[r][c]][1], (x, y))
                elif grid[r][c] == OCCUPIED:
                    self.screen.blit(self.player_imgs[player_num_grid[r][c]][2], (x, y))
                elif grid[r][c] == UNOCCUPIED:
                    self.screen.blit(self.ground_img, (x, y))
                #redraw island boundaries
                if c == self.map_size - 1:
                    if(r < self.island_height):
                        z = r+1
                    else:
                        z = self.island_height
                    for i in range(z):
                        fY = (r+c+i)*self.block_height/2 + self.inc/2
                        self.screen.blit(self.ground_left, (x, fY+self.block_height/2))
                if r == self.map_size - 1:
                    if (c < self.island_height):
                        z = c+1
                    else:
                        z = self.island_height
                    for i in range(z):
                        fY = (r + c + i) * self.block_height / 2 + self.inc / 2
                        self.screen.blit(self.ground_right, (x+self.block_width/2, fY + self.block_height / 2))

        for r in range(self.map_size):
            for c in range(self.map_size):
                x = self.WINDOW_WIDTH / 2 - self.block_width / 2 + (r - c) * (self.block_width) / 2
                y = self.inc / 2 + (r + c) * (self.block_height) / 2
                spriteX = x + 2#+ (self.block_width - self.player_width) / 2
                spriteY = y + (self.block_height - self.player_height) / 2 - 3
                if(x >= self.WINDOW_WIDTH or y >= self.WINDOW_HEIGHT):
                    raise Exception("Out of Bounds Exception")
                img = self.ground_img
                if(player_num_grid[r][c] != -1):
                    img = self.player_imgs[player_num_grid[r][c]][2]
                if grid[r][c] == BOMB:
                    self.screen.blit(img, (x, y))
                    self.screen.blit(self.bomb_img, (spriteX, spriteY-1))
                elif grid[r][c] == BOOST:
                    self.screen.blit(img, (x, y))
                    self.screen.blit(self.boost_img, (spriteX, spriteY-2))


        #small bug, sometimes player doesn't correspond to same index?
        i = 0
        for key in heads:
            hY, hX = heads[key]
            #print(key)
            #print(hX)
            #print(hY)
            if(i >= num_agents):
                continue
            if(hX == -1 and hY == -1):
                self.screen.blit(self.explosion, (self.old_head[key][0]-10, self.old_head[key][1]-5))
                continue
            x = self.WINDOW_WIDTH / 2 - self.block_width / 2 + (hY - hX) * (self.block_width) / 2 #+ (self.block_width - self.player_width) / 2
            y = self.inc / 2 + (hY + hX) * (self.block_height) / 2 + (self.block_height - self.player_height) / 2 - 3
            self.screen.blit(self.player_heads[key], (x,y))
            self.old_head[key] = (x,y)
            i += 1
        #for video
        return pygame.surfarray.array3d(self.screen)

