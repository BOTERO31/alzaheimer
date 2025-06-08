import pygame 
import os
import sys

#Base path
if getattr(sys, 'frozen', False):
    # Running in PyInstaller bundle
    BASE_PATH = sys._MEIPASS
else:
    # Running in normal Python environment
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# window setup
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
BLACK = 0, 0, 0
# tile size
TILE_SIZE = 64