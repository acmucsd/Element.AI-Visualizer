import pygame
import numpy as np
from time import sleep
from constants import *
import math
class Visualizer:
    def __init__(self, size) -> None:
        ground_w = 16
        ground_h = 10

        self.inc = 100

        self.block_width = 16
        self.block_height = self.block_width*ground_h/ground_w
        self.island_height = math.ceil(size * 1/5)
        self.block_adj = self.block_height


        self.player_width = self.block_width
        self.player_height = self.player_width
        self.map_size = size
        self.WINDOW_HEIGHT = math.ceil(self.block_height*self.map_size) + self.inc + self.island_height*self.block_height/2#math.ceil(self.block_adj * self.map_size + self.block_height - self.block_adj) + self.inc
        self.WINDOW_WIDTH = self.block_width * self.map_size + self.inc

        self.bomb_img = pygame.transform.smoothscale(pygame.image.load(game + 'bomb.png'), (self.player_width, self.player_height))
        self.boost_img = pygame.transform.smoothscale(pygame.image.load(game + 'boost.png'), (self.player_width, self.player_height))
        self.explosion = pygame.transform.smoothscale(pygame.image.load(game + 'explosion.png'), (2*self.player_width, 2*self.player_height))

        self.ground_img = pygame.transform.smoothscale(pygame.image.load(game + 'ground.png'), (self.block_width, self.block_height))
        self.ground_left = pygame.transform.smoothscale(pygame.image.load(game + 'island left.png'), (self.block_width/2, 13/8*self.block_width/2))
        self.ground_right = pygame.transform.smoothscale(pygame.image.load(game + 'island right.png'), (self.block_width/2, 13/8*self.block_width/2))

        self.fire_ground = pygame.transform.scale(pygame.image.load(fire + 'fire travel.png'), (self.block_width, self.block_height))
        self.water_ground = pygame.transform.scale(pygame.image.load(water + 'water travel.png'), (self.block_width, self.block_height))
        self.earth_ground = pygame.transform.scale(pygame.image.load(earth + 'earth travel.png'),
                                                  (self.block_width, self.block_height))
        self.air_ground = pygame.transform.scale(pygame.image.load(air + 'air travel.png'),
                                                   (self.block_width, self.block_height))

        self.fire_ter = pygame.transform.smoothscale(pygame.image.load(fire + 'lava ground.png'), (self.block_width, self.block_height))
        self.water_ter = pygame.transform.smoothscale(pygame.image.load(water + 'water ground.png'),
                                                     (self.block_width, self.block_height))
        self.earth_ter = pygame.transform.smoothscale(pygame.image.load(earth + 'earth ground.png'),
                                                      (self.block_width, self.block_height))
        self.air_ter = pygame.transform.smoothscale(pygame.image.load(air + 'air ground.png'),
                                                      (self.block_width, self.block_height))



        self.fire_img = pygame.transform.smoothscale(pygame.image.load(fire + 'fire element.png'), (self.player_width, self.player_height))
        self.water_img = pygame.transform.smoothscale(pygame.image.load(water + 'water element.png'),
                                               (self.player_width, self.player_height))
        self.earth_img = pygame.transform.smoothscale(pygame.image.load(earth + 'earth element.png'),
                                                      (self.player_width, self.player_height))
        self.air_img = pygame.transform.smoothscale(pygame.image.load(air + 'air element.png'),
                                                      (self.player_width, self.player_height))

        self.old_head = {'player_0':(-1,-1), 'player_1':(-1,-1), 'player_2':(-1,-1), 'player_3':(-1,-1)}
        self.player_imgs = [(self.fire_ground, self.fire_ter),
                            (self.water_ground, self.water_ter),
                            (self.earth_ground, self.earth_ter),
                            (self.air_ground, self.air_ter)]
        self.player_heads = {'player_0': self.fire_img, 'player_1': self.water_img, 'player_2': self.earth_img,
                             'player_3': self.air_img}


    def init_window(self):
        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self. WINDOW_HEIGHT))
        self.screen.fill(background)
        #self.draw_grid()
        pygame.display.update()

    #helper drawing method to render empty board
    def draw_grid(self):
        for r in range(self.map_size):
            for c in range(self.map_size):
                x = (r-c-1)*self.block_width / 2 + self.WINDOW_WIDTH/2
                y = (r+c)*self.block_height/2 + self.inc/2
                self.screen.blit(self.ground_img, (x, y))
                #draw island base if it is the bottom of the board
                if c == self.map_size - 1:
                    #size to draw scales with location, maxes out at island_height
                    if(r < self.island_height):
                        z = r+1
                    else:
                        z = self.island_height
                    #stitch component bases together
                    for i in range(z):
                        fY = (r+c+i)*self.block_height/2 + self.inc/2
                        self.screen.blit(self.ground_left, (x, fY+self.block_height/2))
                if r == self.map_size - 1:
                    # size to draw scales with location, maxes out at island_height
                    if (c < self.island_height):
                        z = c+1
                    else:
                        z = self.island_height
                    #stich component bases togethet
                    for i in range(z):
                        fY = (r + c + i) * self.block_height / 2 + self.inc / 2
                        self.screen.blit(self.ground_right, (x+self.block_width/2, fY + self.block_height / 2))

    #render onto pygame screen
    def render(self):
        pygame.event.pump()
        pygame.display.update()
        #time.sleep(0.1) #control time between each step

    #return dimensions of pygame window
    def dims(self):
        return [self.WINDOW_WIDTH,self.WINDOW_HEIGHT]

    #converts board index to render coordinates
    #left board is col = 0, right board is row = 0 | 0,0 top middle of the board
    def posToIsometricCoords(self, r, c):
        #move x by difference of row col index, starting at middle of window
        x = self.WINDOW_WIDTH / 2 - self.block_width / 2 + (r - c) * (self.block_width) / 2
        #move y coord by custom white space and sum of row col index
        y = self.inc / 2 + (r + c) * (self.block_height) / 2
        return (x,y)

    #update scene with new game board information
    def update_scene(self, grid, player_num_grid, num_agents, heads):
        self.screen.fill(background) # clear canvas

        for r in range(self.map_size):
            for c in range(self.map_size):
                x,y = self.posToIsometricCoords(r, c) #convert to window coordinates
                spriteX = x + 2
                spriteY = y + (self.block_height - self.player_height) / 2 - 3
                #out of bounds, raise exception
                if(x >= self.WINDOW_WIDTH or y >= self.WINDOW_HEIGHT):
                    raise Exception("Out of Bounds Exception")
                #draw tail image
                if grid[r][c] == PASSED:
                    self.screen.blit(self.player_imgs[player_num_grid[r][c]][0], (x, y))
                #draw territory image
                elif grid[r][c] == OCCUPIED:
                    self.screen.blit(self.player_imgs[player_num_grid[r][c]][1], (x, y))
                #draw ground image
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
                #convert board index corodinate
                x,y = self.posToIsometricCoords(r, c)
                #coordinates for game pieces
                spriteX = x + 2
                spriteY = y + (self.block_height - self.player_height) / 2 - 3 #move up by difference in height
                if(x >= self.WINDOW_WIDTH or y >= self.WINDOW_HEIGHT):
                    raise Exception("Out of Bounds Exception")
                #replace ground with players territory ground if captured
                img = self.ground_img
                if(player_num_grid[r][c] != -1):
                    img = self.player_imgs[player_num_grid[r][c]][1]
                #draw game pieces
                if grid[r][c] == BOMB:
                    self.screen.blit(img, (x, y))
                    self.screen.blit(self.bomb_img, (spriteX, spriteY-1))
                elif grid[r][c] == BOOST:
                    self.screen.blit(img, (x, y))
                    self.screen.blit(self.boost_img, (spriteX, spriteY-2))


        #draw head sprites
        i = 0
        for key in heads:
            hX, hY = heads[key]
            #skip if more than number of players
            if(i >= num_agents):
                continue
            #if player is dead, draw explosion at previous location
            if(hX == -1 and hY == -1):
                self.screen.blit(self.explosion, (self.old_head[key][0]-10, self.old_head[key][1]-5))
                continue

            x, y = self.posToIsometricCoords(hX, hY)
            y = y + (self.block_height - self.player_height) / 2 - 3
            #draw player head
            self.screen.blit(self.player_heads[key], (x,y))
            #store old coordinate for explosions
            self.old_head[key] = (x,y)
            i += 1
        #for video rendering
        return pygame.surfarray.array3d(self.screen)

