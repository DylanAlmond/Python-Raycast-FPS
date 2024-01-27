import pygame as pg
import os
from settings import *

class Renderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.path = 'resources/textures/'
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/sky/indoors.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture(f'{self.path}ui/blood_screen.png', RES)
        self.crosshair = self.get_texture(f'{self.path}ui/crosshair.png', (CROSSHAIR_SIZE, CROSSHAIR_SIZE))
        self.digit_size = 48
        self.digit_images = [self.get_texture(f'{self.path}ui/digits/{i}.png', [self.digit_size] * 2)
                            for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))

        # map name display
        self.intro_time = 200
        self.intro = True

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_hud()
        if self.intro and self.intro_time > 0:
            self.intro_time -= 1
            self.map_intro()   

    # display map title upon spawn
    def map_intro(self):
        font2 = pg.font.SysFont('didot.ttc', 32)
        txt = font2.render(self.game.map.map_title, True, 'GREY')
        txt_obj = txt.get_rect()
        self.screen.blit(txt, (WIDTH // 2 - txt_obj.width // 2, HEIGHT * 0.7))

    def game_over(self):
        self.screen.blit(self.blood_screen, (0, 0))  

    def draw_player_hud(self):
        # put weapon here as its technically a hud element
        self.game.player.current_weapon.draw()

        health = str(self.game.player.health)
        self.screen.blit(self.digits['10'], (10, HEIGHT - self.digit_size - 20))
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], ((i+1) * self.digit_size, HEIGHT - self.digit_size - 20))

        self.screen.blit(self.crosshair, ((WIDTH // 2 - CROSSHAIR_SIZE // 2, HEIGHT // 2 - CROSSHAIR_SIZE // 2)))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        # set sky position relative to mouse movement
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image , (-self.sky_offset, 0))
        self.screen.blit(self.sky_image , (-self.sky_offset + WIDTH, 0))

        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            if FOG:
                color = [255 / (1 + depth ** 4 * 0.00002)] * 3
                image.fill(color, special_flags=pg.BLEND_RGB_MULT)

            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        images = []
        count = 1
        for file_name in os.listdir(self.path):
            if os.path.isfile(os.path.join(self.path, file_name)):
                images.append(self.get_texture(f'{self.path}{count}.png'))
                count += 1
        return images