from sprite import *
from random import randint, random, choice
from raycast import *

class NPC(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/npc/grunt/0.png', pos=(0, 0), scale=0.5, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')
        self.ray_cast_result = []
        self.frame_counter = 0
        self.enemy_search_trigger = False
        self.alive = True
        self.pain = False    
        
        # Stats
        self.attack_dist = randint(3,6)
        self.speed = 0.01
        self.attackSpeed = 30
        self.size = 64
        self.health = 100
        self.attack_dmg = 10
        self.accuracy = 0.3
        
        # Attack Speed cooldown
        self.attackCooldown = 0
        
        self.currentAnimation = self.idle_images

        # Sound
        self.sound_pain = pg.mixer.Sound(SOUND_PATH + '/grunt/grunt_pain.wav')
        self.sound_death = pg.mixer.Sound(SOUND_PATH + '/grunt/grunt_death.wav')
        self.sound_attack = pg.mixer.Sound(SOUND_PATH + '/grunt/grunt_attack.wav')


    def update(self):
      self.check_animation_time()
      self.get_sprite()
      if self.alive:
        self.animate(self.currentAnimation)
        self.run_logic()
      else:
        self.animate_death()
        
      if DEBUG:
        self.draw_ray_cast()
        
        
    # Wall checking
    def check_wall(self, x, y):
        return(x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    # Movement
    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.player.map_pos)
        next_x, next_y = next_pos
        if next_pos not in self.game.handler.npc_positions and self.player.map_pos:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

        if DEBUG:
            pg.draw.rect(self.game.screen, 'green', (10 * next_x, 10 * next_y, 10, 10))

    # Attack
    def attack(self):
        if self.animation_trigger:
            self.game.sound.CH_NPC_W.play(self.sound_attack)
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_dmg)
                self.attackCooldown = self.attackSpeed


    # Death animation
    def animate_death(self):
        if not self.alive:
            if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1
    
    # Pain animation
    def animate_pain(self):
        self.set_current_animation(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    # Am I being shot at?
    def check_hit(self):
        if self.ray_cast_result[0] and self.game.player.shot:
            # am i in range?
            if self.ray_cast_result[1] <= self.game.player.current_weapon.range:
                # am I at the center of the screen?
                print(HALF_WIDTH - self.size < self.screen_x < HALF_WIDTH + self.size)
                if HALF_WIDTH - self.size < self.screen_x < HALF_WIDTH + self.size:
                    self.game.sound.CH_NPC.play(self.sound_pain)
                    self.game.player.shot = False
                    self.pain = True
                    self.health -= self.game.player.current_weapon.damage

    # Am I still alive?
    def check_health(self):
        if self.health < 1:
            self.alive = False
            self.game.sound.CH_NPC.play(self.sound_death)

    # Thinking
    def run_logic(self):
            self.ray_cast_result = castRay_e(self.game, self.pos, self.game.player.pos, self.theta)
            self.check_hit()
            self.check_health()
            
            # print(f"Can attack: {self.can_attack}")
            
            if self.pain: # In pain
                self.animate_pain()
            elif self.can_attack:
              if self.ray_cast_result[0]: # On sight of player
                  self.enemy_search_trigger = True
                  if self.dist < self.attack_dist:
                      self.set_current_animation(self.attack_images)
                      self.attack()
                  else:
                      self.set_current_animation(self.walk_images)
                      self.movement()
            elif self.enemy_search_trigger:
              if self.dist > self.attack_dist:
                self.set_current_animation(self.walk_images)
                self.movement()              

            else: # Idle
                self.set_current_animation(self.idle_images)
            
            
            if self.attackCooldown > 0:    
              self.attackCooldown -= 1

    def set_current_animation(self, anim):
      if self.currentAnimation == anim: return False
      
      self.currentAnimation = anim

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
      
    @property
    def can_attack(self):
        return self.attackCooldown <= 0

    def draw_ray_cast(self):
        if DEBUG:
            pg.draw.circle(self.game.screen, 'red', (10 * self.x, 10 * self.y), 3) 
            
        castRay_e(self.game, self.pos, self.game.player.pos, self.theta)


class Grunt(NPC):
    def __init__(self, game, path='resources/sprites/npc/grunt/0.png', pos=(0, 0), scale=0.5, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)

        # Stats
        self.attack_dist = randint(3,12)
        self.speed = 0.01
        self.attackSpeed = 30
        self.size = 64
        self.health = 100
        self.attack_dmg = 10
        self.accuracy = 0.4  
        
        # Sound
        self.sound_pain = pg.mixer.Sound(SOUND_PATH + '/grunt/grunt_pain.wav')
        self.sound_death = pg.mixer.Sound(SOUND_PATH + '/grunt/grunt_death.wav')
        self.sound_attack = pg.mixer.Sound(SOUND_PATH + '/grunt/grunt_attack.wav')


class Zombie(NPC):
    def __init__(self, game, path='resources/sprites/npc/zombie/0.png', pos=(0, 0), scale=0.5, shift=0.38, animation_time=260):
        super().__init__(game, path, pos, scale, shift, animation_time)

        # Stats
        self.attack_dist = 1
        self.speed = 0.01
        self.attackSpeed = 260
        self.size = 128
        self.health = 150
        self.attack_dmg = 20
        self.accuracy = 1
        
        # Sound
        self.sound_pain = pg.mixer.Sound(SOUND_PATH + '/zombie/zombie_pain.wav')
        self.sound_death = pg.mixer.Sound(SOUND_PATH + '/zombie/zombie_death.wav')
        self.sound_attack = pg.mixer.Sound(SOUND_PATH + '/zombie/zombie_attack.wav')
