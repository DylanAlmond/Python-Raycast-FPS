from sprite import *

class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', pos=(0,0), scale=1.5, animation_time=120):

        if RES <= RES_S:
            scale *= 0.66

        super().__init__(game=game, path=path, pos=pos, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
            for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2 + 100, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0

        self.damage = 50
        self.range = 6.0 # measured in grid spaces
        self.primary_sound = pg.mixer.Sound(SOUND_PATH + '/w_shotgun/shotgun.wav')

    def shoot(self):
        self.game.sound.CH_WPN.play(self.primary_sound)
        self.reloading = True

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()

class Weapon_Crowbar(Weapon):
    def __init__(self, game, path='resources/sprites/weapon/crowbar/0.png', pos=(0, 0), scale=1.5, animation_time=90):
        super().__init__(game, path, pos, scale, animation_time)

        self.damage = 60
        self.range = 1
        self.primary_sound = pg.mixer.Sound(SOUND_PATH + '/w_crowbar/crowbar.wav')


class Weapon_Shotgun(Weapon):
    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', pos=(0, 0), scale=1.5, animation_time=120):
        super().__init__(game, path, pos, scale, animation_time)
        
        self.damage = 50
        self.range = 6.0 # measured in grid spaces
        self.primary_sound = pg.mixer.Sound(SOUND_PATH + '/w_shotgun/shotgun.wav')

class Weapon_Smg(Weapon):
    def __init__(self, game, path='resources/sprites/weapon/smg/0.png', pos=(0, 0), scale=1.5, animation_time=30):
        super().__init__(game, path, pos, scale, animation_time)
        
        self.damage = 10
        self.range = 12 # measured in grid spaces
        self.primary_sound = pg.mixer.Sound(SOUND_PATH + '/w_smg/smg.wav')

class Tool_EntitySpawner(Weapon):
    def __init__(self, game, path='resources/sprites/weapon/mapTool/0.png', pos=(0, 0), scale=1.5, animation_time=1):
        super().__init__(game, path, pos, scale, animation_time)

        self.damage = 1000
        self.range = 10
        self.primary_sound = pg.mixer.Sound(SOUND_PATH + '/w_crowbar/crowbar.wav')

        self.entities = ["Human Grunt", "Health Kit", "Level End"]
        self.names = {
            "Human Grunt":  "Grunt",
            "Zombie":       "Zombie",
            "Health Kit":   "Healthkit",
            "Level End":    "LevelSprite"
        }
        self.selection = self.entities[0]
        self.loc = (0, 0)

    def shoot(self):
        print(f"Line: '{self.names[self.selection]}, {self.loc[0]}, {self.loc[1]}'")
        self.game.player.shot = False

    def update(self):
        if self.loc != self.game.player.map_pos:
            self.loc = self.game.player.map_pos
            print(self.loc)

        return super().update()

    