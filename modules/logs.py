import curses
import time
from datetime import datetime
from config import ENABLE_HARDWARE, ENABLE_COMMIT, ENABLE_RANDOM, ENABLE_WEATHER, ENABLE_WINDOW, ENABLE_MUSIC
from modules import hardware, gitinfo, weather, window, music
import random

ASCII_ART = r"""welcome to
                       _
  ______              | |                ______
 |______|  _ __  _   _| |__   _____  __ |______|
  ______  | '_ \| | | | '_ \ / _ \ \/ /  ______
 |______| | |_) | |_| | |_) | (_) >  <  |______|
          | .__/ \__, |_.__/ \___/_/\_\
          | |     __/ |
          |_|    |___/
"""
def initui():
    print(ASCII_ART)
    if ENABLE_HARDWARE:
        print(hardware.get_gpu())
    if ENABLE_COMMIT:
        print("Commit: ", gitinfo.get_git_commit())
    if ENABLE_WEATHER:
        print(weather.get_weather())
    if ENABLE_MUSIC:
        print(music.get_music())
    if ENABLE_WINDOW:
        print(window.get_window())