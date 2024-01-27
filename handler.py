from sprite import *
from npc import *
from entity import *

class Handler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'resources/sprites/npc'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        self.npc_positions = {}

        self.door_list = []

        add_sprite = self.add_sprite
        add_npc = self.add_npc

        self.spawn_map_entities()


    def spawn_map_entities(self):
        for i in self.game.map.doors:
            self.door_list.append(Door(self.game, pos=i))

        for i in self.game.map.map_ents:
            match i[0]:
                case "SpriteObject":
                    self.add_sprite(SpriteObject(self.game, pos=(float(i[1]), float(i[2]))))

                case "LevelSprite":
                    self.add_sprite(LevelSprite(self.game, pos=(float(i[1]), float(i[2]))))

                case "AnimatedSprite":
                    self.add_sprite(AnimatedSprite(self.game, pos=(float(i[1]), float(i[2]))))   

                case "Healthkit":
                    self.add_sprite(Healthkit(self.game, pos=(float(i[1]), float(i[2]))))   
                        
                case "Grunt":
                    self.add_npc(Grunt(self.game, pos=(float(i[1]), float(i[2]))))

                case "Zombie":
                    self.add_npc(Zombie(self.game, pos=(float(i[1]), float(i[2]))))

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [NPC.update() for NPC in self.npc_list]
        [Door.update() for Door in self.door_list]

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def add_npc(self, npc):
        self.npc_list.append(npc)  