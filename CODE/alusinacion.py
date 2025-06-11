import pygame
import random
import math
import settings
import time

# Lista para almacenar las figuras activas
active_shapes = []

class Shape:
    def __init__(self, x, y, size, color, shape_type):
        self.x = x
        self.y = y
        self.size = size
        self.color = color  # (r,g,b,alpha)
        self.shape_type = shape_type
        self.creation_time = time.time()
        self.lifetime = 3.0  # 3 segundos de duración
        
def create_shape():
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    alpha = 200  # Comienza completamente visible

    x = random.randint(0,settings.WINDOW_WIDTH)
    y = random.randint(0,settings.WINDOW_HEIGHT)
    size = random.randint(50, 150)
    
    figures = ["circle", "rect"]
    figure = random.choice(figures)
    
    return Shape(x, y, size, (r,g,b,alpha), figure)

def draw_shape(window, shape, self):
    # Calcular ls trsnsparencia(alpha) basado en el tiempo transcurrido
    elapsed_time = time.time() - shape.creation_time
    if elapsed_time >= shape.lifetime:
        return False  # se elimina
    
    # Calcular el nuevo alpha (se desvanece linealmente)
    fade_progress = elapsed_time / shape.lifetime
    new_alpha = int(255 * (1 - fade_progress))
    
    # Crear superficie con el nuevo alpha
    self.surface = pygame.Surface((shape.size*2, shape.size*2), pygame.SRCALPHA)
    r, g, b, _ = shape.color
    new_color = (r, g, b, new_alpha)
    
    # Dibujar la forma
    if shape.shape_type == "circle":
        pygame.draw.circle(self.surface, new_color, (shape.size,shape.size), shape.size)
    elif shape.shape_type == "rect":
        pygame.draw.rect(self.surface, new_color, (0,0,shape.size*2,shape.size*2))
    
    window.blit(self.surface, (shape.x-shape.size, shape.y-shape.size))
    return True  # La forma sigue activa

def confusion(window):
    global active_shapes
    
    # Crear una nueva forma cada cierto tiempo
    if random.random() < 0.2:  # 20% de probabilidad cada frame
        active_shapes.append(create_shape())
    
    # Actualizar y dibujar todas las formas activas
    active_shapes = [shape for shape in active_shapes if draw_shape(window, shape)]