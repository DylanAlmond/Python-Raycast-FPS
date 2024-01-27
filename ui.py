from sound import *

class Label():
	def __init__(self, menu, text, x, y, size, color):
		self.menu = menu
		self.font = pg.font.Font("resources/fonts/K12HL2.ttf", size)
		self.color = color
		self.line = text
		self.text = self.font.render(self.line, True, self.color)
		self.rect = self.text.get_rect(center = (x, y))
		self.menu.objects_to_render.append(self)

	def draw(self):
		#draw button on screen
		self.menu.screen.blit(self.text, self.rect)

class Button(Label):
	def __init__(self, menu, text, x, y, size, color, hover_color):
		super().__init__(menu, text, x, y, size, color)
		self.hover_color = hover_color
		self.clicked = False
		self.hovered = False

		self.hover_sound = pg.mixer.Sound(SOUND_PATH + '/ui/btn1.wav')
		self.pressed_sound = pg.mixer.Sound(SOUND_PATH + '/ui/btn2.wav')

	def draw(self):
		action = False
		#get mouse position
		pos = pg.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if not self.hovered:
				self.menu.sound.CH_PLY.play(self.hover_sound)
				self.text = self.font.render(self.line, True, self.hover_color)
				self.hovered = True

			if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.menu.sound.CH_PLY.play(self.pressed_sound)
				self.clicked = True
				action = True
		else:
			self.text = self.font.render(self.line, True, self.color)
			self.hovered = False

		if pg.mouse.get_pressed()[0] == 0:
			self.clicked = False

		super().draw()

		return action