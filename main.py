import sys
import pygame as pg
from settings import *
from map import *
from player import *
from raycast import *
from render import *
from sprite import *
from handler import *
from weapon import *
from sound import *
from pathfinding import *
from ui import *

class Game:
	def __init__(self, map_file):
		pg.init()
		pg.mouse.set_visible(0)
		self.screen = pg.display.set_mode(RES)
		self.clock = pg.time.Clock()
		self.delta = 1
		self.global_trigger = False
		self.global_event = pg.USEREVENT + 0
		pg.time.set_timer(self.global_event, + 40)
		self.map_file = map_file
		self.new_game()
	
	def new_game(self):
		self.map = Map(self)
		self.sound = Sound(self)
		self.sound.play_soundtrack()
		self.player = Player(self)
		self.player.get_weapons()
		self.renderer = Renderer(self)
		self.raycasting = RayCasting(self)
		self.handler = Handler(self)
		# self.weapon = Weapon(self)
		self.pathfinding = PathFinding(self)
		write_save(self)

	def update(self):
		self.raycasting.update()
		self.handler.update()
		# self.weapon.update()
		pg.display.flip()
		self.delta = self.clock.tick(FPS)
		pg.display.set_caption(f'{CAPTION}  FPS: {self.clock.get_fps() :.1f}')
		self.player.update()

	def draw(self):
		if DEBUG:
			self.screen.fill('black')
			self.map.draw()
			self.player.draw()
		else:
			self.renderer.draw()
			# self.weapon.draw()

	def check_events(self):
		self.global_trigger = False
		for event in pg.event.get():
			if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
				pg.QUIT()
				sys.exit()
			elif event.type == self.global_event:
				self.global_trigger = True
			self.player.player_weapon_events(event)

	# game loop
	def run(self):
		while True:
			self.check_events()
			self.update()
			self.draw()


class Menu:
	def __init__(self):
		pg.init()
		pg.display.set_caption(CAPTION)
		self.sound = Sound(self)
		self.screen = pg.display.set_mode(RES)
		self.background = pg.image.load("resources/textures/ui/menu_background.png")
		self.background = pg.transform.scale(self.background, (RES))

		self.sound.CH_MUS.play(pg.mixer.Sound(SOUND_PATH + 'soundtrack/03 Klaxon Beat.mp3'))

		self.objects_to_render = []

		self.title = Label(self, "CODENAME: L'MBDA", HALF_WIDTH, HALF_HEIGHT - 250, 86, 'White')
		self.new_game_button = Button(self, "new game", HALF_WIDTH, HALF_HEIGHT - 75, 75, '#fcad2d', '#c4c4c4')
		self.load_game_button = Button(self, "load game", HALF_WIDTH, HALF_HEIGHT + 75, 75, '#fcad2d', '#c4c4c4')
		self.quit_button = Button(self, "quit", HALF_WIDTH, HALF_HEIGHT + 225, 75, '#fcad2d', '#c4c4c4')

	def draw(self):
		self.screen.blit(self.background, (0, 0))
		for i in self.objects_to_render:
			i.draw()

		pg.display.update()

	def check_events(self):
		if self.new_game_button.clicked:
			game = Game('map1.txt')
			game.run()

		if self.load_game_button.clicked:
			save = open_save()
			if save:
				game = Game(open_save())
				game.run()
				
		for event in pg.event.get():
			if event.type == pg.QUIT or self.quit_button.clicked:
				pg.QUIT()
				sys.exit()

	def update(self):
		self.check_events()
		self.draw()

	def run(self):
		while True:
			self.update()

		
if __name__ == '__main__':
	game = Game('map3.txt')
	game.run()
	# menu = Menu()
	# menu.run()