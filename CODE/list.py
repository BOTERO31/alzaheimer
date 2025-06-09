import pygame
import os
import random
from sprites import Collectible
from settings import BASE_PATH

def load_collectibles(map, player, all_sprites, collectible_group):
    generated_items = {}

    for obj in map.get_layer_by_name('Collectibles'):
        name = obj.name.lower()
        if name in generated_items:
            generated_items[name] += 1
        else:
            generated_items[name] = 1

    # ✅ Mostrar ítems generados
    print(f"Items generados: {generated_items}")

    # Generar lista de objetivo aleatoria
    lista_objetivo = randomly_generated(generated_items)
    print("Lista objetivo aleatoria:", lista_objetivo)

    for obj in map.get_layer_by_name('Collectibles'):
        name = obj.name.lower()
        Collectible(
            (obj.x, obj.y), obj.image,
            (all_sprites, collectible_group),
            player_group=pygame.sprite.GroupSingle(player),
            name=name,
            objetivos=lista_objetivo
        )

    return lista_objetivo

#La funcion que crea la lista random
def randomly_generated(generated_items):
    random_list = {}
    names = list(generated_items.keys())
    sample_size = min(5, len(names))  # limitar a máximo 5
    selected = random.sample(names, sample_size)
    for name in selected:
        random_list[name] = random.randint(1, min(generated_items[name], 5))
    return random_list

#Funcion para dibujar todo en orden
def draw_objectives(lista_objetivo, display_surface, hoja, memoria):
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
        if nombre in memoria.blur:
            texto = f"{nombre}-?"
            render = fuente_objetivo.render(texto, True, color_activo)

            # Simular borrosidad con baja opacidad
            alpha_surface = pygame.Surface(render.get_size(), pygame.SRCALPHA)
            alpha_surface.blit(render, (0, 0))
            alpha_surface.set_alpha(80)
            display_surface.blit(alpha_surface, (text_x, text_y))
        
        else:
            texto = f"{nombre}-{cantidad}"
            completado = cantidad == 0
            color = color_completado if completado else color_activo
            render = fuente_objetivo.render(texto, True, color)
            display_surface.blit(render, (text_x, text_y))

            if completado:
                start = (text_x, text_y + render.get_height() // 2)
                end = (text_x + render.get_width(), text_y + render.get_height() // 2)
                pygame.draw.line(display_surface, color, start, end, 2)

        text_y += 22
