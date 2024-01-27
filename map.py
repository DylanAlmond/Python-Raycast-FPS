import pygame as pg
from mapparser import *

class Map:
    def __init__(self, game):
        self.game = game
        self.world_map = {} # coordinate based map only storing location

        # map file info
        self.map_info = ()
        self.map_title = ""
        self.mini_map = []
        self.map_ents = []
        self.doors = []
        self.player_info = []
        self.soundtrack = None

        self.get_map()

    # create coordinates from mini map
    def get_map(self):
        self.map_info = read_map(self.game.map_file)

        self.map_title = self.map_info[0]
        self.mini_map = self.map_info[1]
        self.map_ents = self.map_info[2]
        self.player_info = self.map_info[3]
        self.doors = self.map_info[4]
        self.next_map = self.map_info[5]
        self.soundtrack = self.map_info[6]

        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value
        

    # draw 2d top-down of map
    def draw(self):
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 10, pos[1] * 10, 10, 10), 1)
            for pos in self.world_map]