from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.ground = True
        
        
class CollisionSprite(Sprite):
    def __init__(self, pos, surf, groups, name=""):
        super().__init__(pos, surf, groups)
        self.name = name.lower()

        if self.name == 'shelf5':
            self.hitbox = self.rect.inflate(-10, -50)
        else:
            self.hitbox = self.rect.inflate(-10, -10)

        self.ground = False


class Collectible(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups, player_group, name=""):
        super().__init__(groups)
        self.name = name.lower()
        self.player_group = player_group
        self.collected = False
        self.ground = False

        # Escalado personalizado según el nombre del ítem
        size_map = {
            'manzana': (36.17, 38.17),
            'zanahoria': (43.50, 58.00),
            'leche': (27.33, 31.67),
            'yogurt': (20.00, 22.00),
            'papas': (53.50, 65.00),
            'galleta': (33.00, 30.33)
        }

        # Obtener el tamaño adecuado si el nombre coincide
        default_size = (48, 48)
        size = next((v for k, v in size_map.items() if k in self.name), default_size)

        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(70, 80)

        # Marcar si debe ir en la capa superior
        self.top_layer = 'manzana' in self.name or 'zanahoria' in self.name

    def update(self, dt):
        for player in self.player_group:
            if self.hitbox.colliderect(player.hitbox_rect):
                keys = pygame.key.get_pressed()
                if keys[pygame.K_e] and not self.collected:
                    self.collected = True
                    self.kill()  # Eliminar el ítem
                    # Aquí puedes sumar puntos, reproducir sonido, etc.