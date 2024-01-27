import pygame as pg
from settings import *
from sprite import *

class Door:
    def __init__(self, game, pos=(1,1)):
        self.game = game
        self.world_map = game.map.world_map
        self.pos = pos       
        self.texture = 10
        self.sound = pg.mixer.Sound(SOUND_PATH + '/door/doormove.wav')
        self.visible = True
        self.cooldown = 0

        # W, N, E, S, NW, NE, SE, SW
        self.dir = [-1, 0], [0, -1], [1, 0], [0, 1]
        self.neighbours = self.get_positions()

        self.close()

    # get neighbouring tiles
    def get_positions(self):
        return [(self.pos[0] + dx, self.pos[1] + dy) for dx, dy in self.dir if (self.pos[0] + dx, self.pos[1] + dy) not in self.world_map]      

    # open door
    def open(self):
        if self.visible:
            self.visible = False
            self.game.sound.CH_AMB.play(self.sound)  

            # do i exist in the world map?
            if self.world_map.get(self.pos):
                self.world_map.pop(self.pos)

        self.cooldown = DOOR_COOLDOWN

    # close door
    def close(self):
        self.visible = True
        self.world_map[self.pos] = self.texture

    def check_toggle(self):
        for i in self.neighbours:
            if i == self.game.player.map_pos or self.pos == self.game.player.map_pos:
                self.open()

    def update(self):
        self.check_toggle()
        if self.visible == False:
            if self.cooldown < 1:
                self.close()
            else:
                self.cooldown -=1

# end of level sprite
class LevelSprite(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/animated_sprites/lambda/1.png', 
                pos=..., scale=0.5, shift=0.32, animation_time=400):
        super().__init__(game, path, pos, scale, shift, animation_time)

    def update(self):
        super().update()
        self.check_player()

    def check_player(self):
        if self.map_pos == self.game.player.map_pos:
            self.game.map_file = self.game.map.next_map
            self.game.new_game()

# health kit
class Healthkit(SpriteObject):
    def __init__(self, game, path='resources/sprites/static_sprites/healthkit.png', pos=..., scale=0.5, shift=0.32):
        super().__init__(game, path, pos, scale, shift)

        self.health = 20
        self.enabled = True

    def update(self):
        if self.enabled:
            super().update()
            self.check_player()

    def check_player(self):
        if self.map_pos == self.game.player.map_pos and self.game.player.health < PLAYER_MAX_HEALTH:
            self.game.player.add_health(20)
            self.enabled = False