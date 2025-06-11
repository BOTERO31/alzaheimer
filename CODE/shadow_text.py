import pygame

def draw_shadowed_text(surface, text, font, color, shadow_color, pos, center=True, shadow_offset=(2, 2)):
    """
    Dibuja texto con una sombra para mayor legibilidad.
    
    - surface: superficie de destino
    - text: texto a renderizar
    - font: objeto pygame.font.Font
    - color: color principal del texto
    - shadow_color: color de la sombra (por lo general, negro o gris)
    - pos: posición en pantalla
    - center: si True, centra el texto en pos; si False, lo alinea arriba a la izquierda
    - shadow_offset: desplazamiento de la sombra (x, y)
    """
    text_surface = font.render(text, True, color)
    shadow_surface = font.render(text, True, shadow_color)

    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = pos
    else:
        text_rect.topleft = pos

    shadow_rect = text_rect.copy()
    shadow_rect.x += shadow_offset[0]
    shadow_rect.y += shadow_offset[1]

    surface.blit(shadow_surface, shadow_rect)
    surface.blit(text_surface, text_rect)