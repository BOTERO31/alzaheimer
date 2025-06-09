from settings import *
import pygame

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

        #Necesito diferentes tamaños y valores de hitbox para ciertos objetos colicionables por lo que recorriendo los objeto hago:
        if self.name == 'shelf5':
            self.hitbox = self.rect.inflate(-10, -50) #Al shelf5 o el de leche y yogur le cambio la hitbox
        elif self.name == 'shelf6_bread':
            self.image = pygame.transform.scale(surf, (128.28, 186.28))  #Al de los panes le cambio el tamaño para que coincida con el del tiled_map
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-10, -70)  # Ajusta colisión
        elif self.name == 'milk':
            self.image = pygame.transform.scale(surf, (133.86, 182.97)) 
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-10, -70)  # Ajusta colisión
        elif self.name == 'fish':
            self.image = pygame.transform.scale(surf, (69.67, 95.67))  #Al del hielo le cambio el tamaño para que coincida con el del tiled_map
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-10, -10)
        elif self.name == 'meat':
            self.image = pygame.transform.scale(surf, (69.00, 94.67))
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-10, -10)
        elif self.name == 'ice':
            self.image = pygame.transform.scale(surf, (207.00, 98.00))
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-10, -10)
        elif self.name == 'cake':
            self.image = pygame.transform.scale(surf, (183.08, 143.12))
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-10, -10)
        elif self.name == 'sit':
            self.image = pygame.transform.scale(surf, (164.43, 117.23)) 
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-10, -50)  # Ajusta colisión
        elif self.name == 'shelf2_1' or self.name == 'shelf2_2' or self.name == 'shelf2_3' or self.name == 'shelf2_4':
            self.image = pygame.transform.scale(surf, (73.38, 235.71)) 
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-10, -90)  # Ajusta colisión
        elif self.name == 'mini_shelf5':
            self.image = pygame.transform.scale(surf, (169.00, 159.00)) 
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-10, -70)  # Ajusta colisión
        elif self.name == 'drinks':
            self.image = pygame.transform.scale(surf, (99.00, 195.00)) 
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-10, -70)  # Ajusta colisión
        elif self.name == 'beauty':
            self.image = pygame.transform.scale(surf, (164.00, 240.00)) 
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-10, -70)  # Ajusta colisión
        else:
            self.hitbox = self.rect.inflate(-10, -10) #Sino estos son los valores para el resto de los objetos

        self.ground = False

class Collectible(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups, player_group, name="", objetivos=None):
        super().__init__(groups)
        self.name = name.lower()
        self.player_group = player_group
        self.objetivos = objetivos
        self.collected = False
        self.ground = False
        sound_path = os.path.join(BASE_PATH,'AUDIO', 'pick.mp3')
        self.collected_sfx = pygame.mixer.Sound(sound_path)


        # Escalado personalizado según el nombre del ítem, para que cada item tenga el tamaño que tienen en el tiled_map
        size_map = {
            'manzana': (36.17, 38.17),
            'zanahoria': (43.50, 58.00),
            'leche': (27.33, 31.67),
            'yogurt': (20.00, 22.00),
            'papas': (53.50, 65.00),
            'galleta': (33.00, 30.33),
            'cola': (15.25, 35.75),
            'cebolla': (33.00, 35.33),
            'pescado': (40.50, 33.50),
            'pan': (30.00, 29.50),
            'queso': (31.67, 31.33),
            'carne': (32.67, 29.00),
            'agua': (14.00, 30.00),
            'arroz': (26.83, 35.00),
            'harina': (24.50, 34.00),
            'frijol': (31.67, 33.67),
            'helado': (28.50, 36.50)
        }

        # Obtener el tamaño adecuado si el nombre coincide
        default_size = (48, 48)
        #Busca si el nombre del elemento esta en la lista de 'size_map' y si lo haya le da los valores de tamaño de la lista, sino el 'default_size'
        size = next((v for k, v in size_map.items() if k in self.name), default_size)

        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect(topleft=pos)

        large_hitbox = {
            'leche': (40, 80),
            'yogurt': (40, 80),
            'cola': (40, 80),
            'pan': (40, 80),
            'queso': (40, 80),
            'agua': (40, 80),
            'arroz': (40, 80),
            'harina': (40, 80),
            'frijol': (40, 80),
        }

        # Buscar si el ítem está en la lista de hitbox grandes
        for key in large_hitbox:
            if key in self.name:
                w, h = large_hitbox[key]
                self.hitbox = self.rect.inflate(w, h)
                break
        else:
            self.hitbox = self.rect.inflate(40, 50)

        # Marcar si debe ir en la capa superior, estos elementos siempre se van a dibujar enciama del resto
        self.top_layer = (
            'manzana' in self.name or 'zanahoria' in self.name 
            or 'zanahoria' in self.name or 'cebolla' in self.name 
            or 'pescado' in self.name or 'helado' in self.name 
            or 'carne' in self.name or 'harina' in self.name
        )

    def update(self, dt, invert_keys, remaining):

        for player in self.player_group:
            if self.hitbox.colliderect(player.hitbox_rect):
                keys = pygame.key.get_pressed()
                if keys[pygame.K_e] and not self.collected:
                    self.collected = True
                    self.collected_sfx.play()
                    #Le crea al jugadro un inventario segun los elementos que va recogiendo
                    #ahora mismo no se usa
                    if self.name in player.inventory:
                        player.inventory[self.name] += 1
                    else:
                        player.inventory[self.name] = 1
                    print(f"Objetivos recogidos: {player.inventory}")

                    #Verifica los elementos recogidos con la lista creada aleatoria en "list"
                    if self.objetivos and self.name in self.objetivos:
                        if self.objetivos[self.name] > 0:
                            self.objetivos[self.name] -=1 #Le resta el elemento si se recoge
                            player.puntos += 100 #Logica del contador de puntos
                        
                        if remaining > 0 :
                            player.puntos = player.puntos          

                        print("puntos", player.puntos)
                        print(f"Objetivos restantes: {self.objetivos}")
                    self.kill()  # Eliminar el ítem