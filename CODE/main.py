import pygame
import settings  
from os.path import join
from player import Player
from collisions import Collisions
# import camera

# Inicializar todos los módulos necesarios de Pygame
pygame.init()

# Crear la ventana del juego con el tamaño definido previamente
ventana = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
pygame.display.set_caption("Supermarket Rush")

# Colores y velocidad del personaje
x = 100
y = 100

collision_system = Collisions()

# Contador fruta
contador_frutas = 0

#Imagen
background = pygame.image.load(join('DATA', 'maps','tile.png'))


# Inicializar jugador y grupo de sprites
moving_sprites = collision_system.visible_sprites
player = collision_system.player

# Dibujar la cuadrícula
def dibujar_grid():
    for x in range(30):
        pygame.draw.line(ventana, settings.BLANCO, (x * 40, 0), (x * 40, settings.WINDOW_HEIGHT)) 
        pygame.draw.line(ventana, settings.BLANCO, (0, x * 40), (settings.WINDOW_WIDTH, x * 40))

# Bucle principal del juego
corriendo = True
reloj = pygame.time.Clock()

while corriendo:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False

    # Rellenar la ventana con el color de fondo
    ventana.fill(settings.NEGRO)
    dibujar_grid()
    
    #background
    ventana.blit(background, (0,0))

    # Actualizar y dibujar el sprite animado del jugador
    moving_sprites.update(4, keys)  # Y que player esté dentro de ese grupo
    moving_sprites.update(0.2, keys)
    
    # Detección de colisión con frutas
    moving_sprites.draw(ventana)
    
    colisiones_frutas = pygame.sprite.spritecollide(player, collision_system.items_sprites, False)
    if colisiones_frutas and keys[pygame.K_SPACE]:
        for fruta in colisiones_frutas:
            fruta.kill()
        contador_frutas += len(colisiones_frutas)
        print(f"Frutas recogidas: {contador_frutas}")

    
    # Actualizar la pantalla
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()