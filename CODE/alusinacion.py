import pygame
import random
import math

def confusion():
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    alpha = random.randint(50,200)  # Valor de transparencia (0-255)

    x = random.randint(0,WINDOW_WIDTH)
    y = random.randint(0,WINDOW_HEIGHT)
    size = random.randint(10, 80)
    
    figures = ["circle", "rect", "triangle", "star", "hexagon"]
    figure = random.randint(figures[0], len(figures))
    
    # Crear una superficie con transparencia
    surface = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
    
    if figure == "circle":
        pygame.draw.circle(surface, (r,g,b,alpha), (size,size), size)
    elif figure == "rect":
        pygame.draw.rect(surface, (r,g,b,alpha), (0,0,size*2,size*2))
    elif figure == "triangle":
        points = [(size,0), (0,size*2), (size*2,size*2)]
        pygame.draw.polygon(surface, (r,g,b,alpha), points)
    elif figure == "star":
        points = []
        for i in range(10):
            angle = i * 36 * 3.14159 / 180
            radius = size if i % 2 == 0 else size/2
            points.append((size + radius * math.cos(angle), size + radius * math.sin(angle)))
        pygame.draw.polygon(surface, (r,g,b,alpha), points)
    elif figure == "hexagon":
        points = []
        for i in range(6):
            angle = i * 60 * 3.14159 / 180
            points.append((size + size * math.cos(angle), size + size * math.sin(angle)))
        pygame.draw.polygon(surface, (r,g,b,alpha), points)
    
    window.blit(surface, (x-size, y-size))