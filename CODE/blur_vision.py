import pygame
import random
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
    gray = random.randint(180, 220)
    alpha = random.randint(200, 250)  # Muy transparente

    size = random.randint(80, 180)  # Tamaño más grande
    x = random.randint(0, settings.WINDOW_WIDTH - size)
    y = random.randint(0, settings.WINDOW_HEIGHT - size)
    
    figure = random.choice(["circle", "rect"])
    
    return Shape(x, y, size, (gray, gray, gray, alpha), figure)

def draw_shape(window, shape):
    elapsed_time = time.time() - shape.creation_time
    if elapsed_time >= shape.lifetime:
        return False

    # Mantener el alpha original hasta que desaparezca
    fade_progress = elapsed_time / shape.lifetime
    r, g, b, alpha = shape.color
    new_alpha = int(alpha * (1 - fade_progress))  # más tenue pero no se vuelve invisible al instante

    surface = pygame.Surface((shape.size*2, shape.size*2), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))  # Fondo transparente
    new_color = (r, g, b, new_alpha)

    if shape.shape_type == "circle":
        pygame.draw.circle(surface, new_color, (shape.size, shape.size), shape.size)
    elif shape.shape_type == "rect":
        pygame.draw.ellipse(surface, new_color, (0, 0, shape.size*2, shape.size*2))  # ovalo en vez de cuadrado

    window.blit(surface, (shape.x - shape.size, shape.y - shape.size))
    return True

def confusion(window):
    global active_shapes
    
    # Crear una nueva forma cada cierto tiempo
    if len(active_shapes) < 10 and random.random() < 0.1: #10% de probabilidad por frma y no haya mas de 10
        active_shapes.append(create_shape())
    
    # Actualizar y dibujar todas las formas activas
    active_shapes = [shape for shape in active_shapes if draw_shape(window, shape)]