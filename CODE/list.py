import pygame
import os
import random
from sprites import Collectible
from settings import BASE_PATH

def load_collectibles(map, player, all_sprites_group, collectible_group):
    generated_items = {}

    # Contar ítems
    for obj in map.get_layer_by_name('Collectibles'):
        name = obj.name.lower()
        generated_items[name] = generated_items.get(name, 0) + 1

    print(f"Items generados: {generated_items}")

    # Generar lista objetivo aleatoria
    lista_objetivo = randomly_generated(generated_items)
    print("Lista objetivo aleatoria:", lista_objetivo)

    # Crear objetos Collectible, tambien le envia la lista random a Collectible en "sprites"
    for obj in map.get_layer_by_name('Collectibles'):
        name = obj.name.lower()
        Collectible(
            (obj.x, obj.y), obj.image,
            (all_sprites_group, collectible_group),
            player_group=pygame.sprite.GroupSingle(player),
            name=name,
            objetivos=lista_objetivo
        )

    return lista_objetivo

#La funcion que crea la lista random
def randomly_generated(generated_items):
    random_list = {}

    # Obtener los nombres de los ítems generados
    item_names = list(generated_items.keys())
    random.shuffle(item_names)  # Mezcla aleatoria

    # Elegir hasta 5 únicos, para que siempre tenga 5 items la lista
    selected = item_names[:min(5, len(item_names))]

    # Asignar cantidades aleatorias a los 5 items seleccionados
    for name in selected:
        amount = generated_items[name]
        random_amount = random.randint(1, amount)
        random_list[name] = min(random_amount, amount)
    print(amount)
    return random_list

#Funcion para dibujar todo en orden
def draw_objectives(display_surface, hoja, lista_objetivo):
    x, y = 20, 40
    #Dibuja la oja sobre las coordenas (x, y)
    display_surface.blit(hoja, (x, y))

    #Carga el tipo de letra para los elementos de la lista
    font_path = os.path.join(BASE_PATH, 'DATA', 'fonts', 'EBGaramond-BoldItalic.ttf')
    #El titulo y los objetivos tienen tamaños diferentes
    fuente_titulo = pygame.font.Font(font_path, 24)
    fuente_objetivo = pygame.font.Font(font_path, 22)

    #Color antes de recogerlo y color despues de recogerlo
    color_activo = (89, 51, 25)
    color_completado = (181, 123, 87)

    #Coordenadas para no dibujar le texto al ras de la hoja
    text_x = x + 10
    text_y = y + 5

    #Primero dibujamos el titulo ya que tiene diferentes valores
    titulo = fuente_titulo.render("- Objetivos -", True, color_activo)
    display_surface.blit(titulo, (text_x, text_y))
    text_y += 27

    #Luego recorremos la lista objetivo dibujando los items
    for nombre, cantidad in lista_objetivo.items():
        texto = f"{nombre}-{cantidad}"
        
        #Verifica si ya esta en 0 la cantidad para dibujarla del color antes de recoger o ya recogido
        completado = cantidad == 0
        color = color_completado if completado else color_activo

        #Carga el tipo de fuente y dibuja el texto
        render = fuente_objetivo.render(texto, True, color)
        display_surface.blit(render, (text_x, text_y))

        #En caso de estar completado, este if calcula la mitad del texto y sobre esa mitad traza una linea
        if completado:
            start = (text_x, text_y + render.get_height() // 2) #Comienza la linea
            end = (text_x + render.get_width(), text_y + render.get_height() // 2) #Termina la linea
            pygame.draw.line(display_surface, color, start, end, 2)

        #Espaciado entre un texto y el otro, para que coincida con los renglones de la imagen 'hoja'
        text_y += 22