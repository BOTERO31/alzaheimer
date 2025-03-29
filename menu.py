import pygame
import constantes
import mundo
import alzheimer
import tiles 
import os


#sprite

#cargar imagenes del mundo
tile_list = []
for x in range(constantes.TILE_TYPES):
    tile_image = pygame.transform.scale(tile_image, (constantes.TILE_SIZE, constantes.TILE_SIZE))
    tile_list.append(tile_image)
    
      
    
#mapa para poner los tiles  
world_data = [
    [0]
]

world = mundo.Mundo()
world.process_data(world_data, tile_list)



#dibujar mundo    
world.draw(alzheimer.ventana)