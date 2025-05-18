# Importar las librerías necesarias
import pygame
import constantes  
import os
from player import Player
from colisiones import Collisions
import Camara
# Inicializar todos los módulos necesarios de Pygame
pygame.init()

# Crear la ventana del juego con el tamaño definido previamente
ventana = pygame.display.set_mode((constantes.ancho_ventana, constantes.alto_ventana))
pygame.display.set_caption("Supermarket Rush")

# Colores y velocidad del personaje
x = 100
y = 100

collision_system = Collisions()
#Join imagen
ruta_tiles = "tiles"

#Imagen
background = pygame.image.load(os.path.join(ruta_tiles, "tile.png"))

# Clase del jugador con sprites y animación


# Inicializar jugador y grupo de sprites
moving_sprites = collision_system.visible_sprites
player = collision_system.player

# Dibujar la cuadrícula
def dibujar_grid():
    for x in range(30):
        pygame.draw.line(ventana, constantes.BLANCO, (x * 40, 0), (x * 40, constantes.alto_ventana)) 
        pygame.draw.line(ventana, constantes.BLANCO, (0, x * 40), (constantes.ancho_ventana, x * 40))

# Bucle principal del juego
corriendo = True
reloj = pygame.time.Clock()

while corriendo:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False

    # Rellenar la ventana con el color de fondo
    ventana.fill(constantes.NEGRO)
    dibujar_grid()
    
    #background
    ventana.blit(background, (0,0))

    # Actualizar y dibujar el sprite animado del jugador
    player.update(4, keys)
    moving_sprites.update(0.2, keys)
    moving_sprites.draw(ventana)
    
    
    # Actualizar la pantalla
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()


