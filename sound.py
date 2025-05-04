import os
import pygame as pg
from settings import *


class Sound:
  def __init__(self, game):
    self.game = game
    pg.mixer.stop()
    pg.mixer.init()
    self.path = SOUND_PATH

    pg.mixer.set_num_channels(CH_MAX)  # default is 8
    self.CH_PLY = pg.mixer.Channel(0)    # player sounds
    self.CH_WPN = pg.mixer.Channel(1)    # player weapons
    self.CH_NPC = pg.mixer.Channel(2)    # npc
    self.CH_NPC_W = pg.mixer.Channel(3)  # npc weapons
    self.CH_AMB = pg.mixer.Channel(4)    # ambient sounds (doors...)
    self.CH_MUS = pg.mixer.Channel(5)    # music

  def play_soundtrack(self, track):
    full_path = os.path.join(SOUND_PATH, 'soundtrack', track)

    if not os.path.isfile(full_path):
      print(f"Soundtrack file not found: {full_path}")
      return

    try:
      self.CH_MUS.play(pg.mixer.Sound(full_path))
    except pg.error as e:
      print(f"Error loading or playing soundtrack: {track}\n{e}")
