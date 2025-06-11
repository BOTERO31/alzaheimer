import pygame
from settings import *
def iscreen():
    pygame.init()
    
    irect = pygame.rect(0, 0, WINDOW_WIDTH*0.8, WINDOW_HEIGHT*0.8)
    pygame.draw.rect(pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT)), (0,0,0,200), irect)
     
    return irect