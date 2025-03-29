import pygame

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Supermarket Rush")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

# Cargar sprites (puedes reemplazar con imágenes reales)
player_size = 40
player = pygame.Rect(WIDTH // 2, HEIGHT - 100, player_size, player_size)

# Lista de estanterías (paredes/obstáculos)
shelves = [
    pygame.Rect(100, 100, 600, 20),
    pygame.Rect(100, 200, 600, 20),
    pygame.Rect(100, 300, 600, 20),
    pygame.Rect(100, 400, 600, 20)
]

# Velocidad de movimiento
speed = 5

# Bucle del juego
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Controles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    if keys[pygame.K_UP]:
        player.y -= speed
    if keys[pygame.K_DOWN]:
        player.y += speed
    
    # Dibujar estanterías
    for shelf in shelves:
        pygame.draw.rect(screen, BROWN, shelf)
    
    # Dibujar personaje
    pygame.draw.rect(screen, BLUE, player)
    
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()