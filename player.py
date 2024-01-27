from settings import *
from weapon import *
from collections import deque
import pygame as pg
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = game.map.player_info[0]
        self.angle = game.map.player_info[1]
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.weapons = []
        self.spawn_cooldown = 20
        self.spawned = True
        self.current_weapon = None
        self.weapon_index = 0
        self.shooting = False

        # stop mouse leaving screen
        pg.event.set_grab(True)

        self.death_sound = pg.mixer.Sound(SOUND_PATH + '/player/hev_dead0.wav')
        self.health_sound = pg.mixer.Sound(SOUND_PATH + '/player/addhealth.wav')
        self.pain_sound = pg.mixer.Sound(SOUND_PATH + '/player/player_pain.wav')
    
    def get_weapons(self):
        self.weapons = []

        if MAP_EDITOR:
            self.weapons = [Tool_EntitySpawner(self.game)]

        for i in self.game.map.player_info[2]:
            match i:
                case "Crowbar":
                    self.weapons.append(Weapon_Crowbar(self.game))
                case "Shotgun":
                    self.weapons.append(Weapon_Shotgun(self.game))
                case "Smg":
                    self.weapons.append(Weapon_Smg(self.game))

        if self.weapons[0]:
            self.current_weapon = self.weapons[0]      

    def check_game_over(self):
        if self.health < 1:
            pg.display.flip()
            self.game.sound.CH_PLY.play(self.death_sound)
            pg.time.delay(1500)
            pg.event.clear()
            self.game.new_game()

    def get_damage(self, damage):
        self.health -= damage
        self.game.renderer.player_damage()
        self.game.sound.CH_PLY.play(self.pain_sound)
        self.check_game_over()

    def add_health(self, health):
        if self.health + health > PLAYER_MAX_HEALTH:
            self.health = PLAYER_MAX_HEALTH
        else:
            self.health += health
        self.game.sound.CH_PLY.play(self.health_sound)
        #self.game.renderer.player_damage()

    def player_weapon_events(self, event):
        # shoot
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.current_weapon.reloading:
                self.shooting = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.shooting = False
        
        if event.type == pg.MOUSEWHEEL:
            self.scroll_weapon(event.y)

        if event.type == pg.KEYDOWN and not self.shot and not self.current_weapon.reloading:
            match event.key:
                case pg.K_SPACE:
                    self.shooting = True
                case pg.K_UP:
                    self.scroll_weapon(1)
                case pg.K_DOWN:
                    self.scroll_weapon(-1)
                case _:
                    ...            
        elif event.type == pg.KEYUP:
             match event.key:
                case pg.K_SPACE:
                    self.shooting = False
                case _:
                    ...     

        if self.shooting and not self.shot and not self.current_weapon.reloading:
            self.primary_trigger()            
    
    def primary_trigger(self):
        self.shot = True
        self.current_weapon.shoot()
            

    def scroll_weapon(self, direction):
        if MAP_EDITOR:
            self.current_weapon.entities = deque(self.current_weapon.entities)
            self.current_weapon.entities.rotate(direction)
            self.current_weapon.selection = self.current_weapon.entities[0]
            print(f"Selected entity: {self.current_weapon.selection}")
        else:
            if not self.shot and not self.current_weapon.reloading:
                self.weapons = deque(self.weapons)
                self.weapons.rotate(direction)
                self.current_weapon = self.weapons[0]
                self.weapons = list(self.weapons)

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta # correct speed for framerate
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_w]: # forward movement
            dx += speed_cos
            dy += speed_sin

        if keys[pg.K_s]: # backward movement
            dx += -speed_cos
            dy += -speed_sin

        if keys[pg.K_a]: # strafe left
            dx += speed_sin
            dy += -speed_cos

        if keys[pg.K_d]: # strafe right
            dx += -speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)

        # Keys look
        if keys[pg.K_LEFT]: # look left
            self.angle -= PLAYER_ROT_SPEED * self.game.delta
        if keys[pg.K_RIGHT]: # look right
            self.angle += PLAYER_ROT_SPEED * self.game.delta          

        self.angle %= math.tau # tau = 2pi

    def check_wall(self, x, y):
        return(x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        pg.draw.circle(self.game.screen, 'green', (self.x * 10, self.y * 10), 3)

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        # if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
        #     pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta

    def update(self):
        if self.spawned and self.spawn_cooldown > 0:
            # Stop player movement on spawn
            # (stops player teleporting out of bounds if trying to move before spawning)
            self.x, self.y = self.game.map.player_info[0]
            self.angle = self.game.map.player_info[1] / 57.3
            self.health = PLAYER_MAX_HEALTH
            self.spawn_cooldown -= 1
        else:
            self.movement()
            self.mouse_control()
            self.current_weapon.update()


    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)