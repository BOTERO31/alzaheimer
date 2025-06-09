import pygame
import json
import sprites
import player

class Puntuacion:
    def __init__(self):
        self.path_puntuacion = 'puntuacion.json'
        self.mejor_puntuacion = self.cargar_puntuacion()

    def cargar_puntuacion(self):
        try:
            with open(self.path_puntuacion, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            # Si el archivo no existe o está vacío, devolver una lista vacía
            return []

    def guardar_puntuacion(self, puntos, tiempo_usado):
        puntuacion = {
            'puntuacion': puntos,
            'tiempo': tiempo_usado
        }
        self.mejor_puntuacion.append(puntuacion)
        self.mejor_puntuacion.sort(key=lambda x: x['puntuacion'], reverse=True)
        self.mejor_puntuacion = self.mejor_puntuacion[:1]

        with open(self.path_puntuacion, 'w', encoding='utf-8') as archivo:
            json.dump(self.mejor_puntuacion, archivo, indent=2, ensure_ascii=False)

