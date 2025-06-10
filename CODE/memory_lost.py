# memory_lot.py
import time
import random

class MemoryLossManager:
    def __init__(self, intervalo=60):
        self.last_memory_loss = time.time()
        self.memory_loss_interval = intervalo  # tiempo en segundos
        self.blur = set()

        self.mensajes = [
            "Sientes una niebla mental... algo se está desvaneciendo.",
            "Un leve mareo te invade. ¿Qué era lo que ibas a hacer?",
            "Tus pensamientos se mezclan... ¿Qué tenías en la lista?",
            "Tus recuerdos parecen deshilacharse por un momento.",
            "Un zumbido sutil llena tu mente. Te cuesta enfocarte.",
        ]
        self.mostrar_mensaje = False
        self.mensaje_actual = None
        self.mensaje_timer = 0
        self.item_a_borrar = None



    def actualizar(self, lista_objetivo):
        # Verifica si ya pasó suficiente tiempo
        if time.time() - self.last_memory_loss >= self.memory_loss_interval:
            self.borrar_elemento(lista_objetivo)
            self.last_memory_loss = time.time()

    def borrar_elemento(self, lista_objetivo):
        # Borra un elemento aleatorio pendiente
        if not lista_objetivo:
            return

        pendientes = [k for k, v in lista_objetivo.items() if v > 0]
        if not pendientes:
            return

        self.mensaje_actual = random.choice(self.mensajes)
        self.mostrar_mensaje = True
        self.mensaje_timer = time.time()
        self.item_a_borrar = random.choice(pendientes)

    def check_mensaje(self, lista_objetivo):
        if self.mostrar_mensaje and time.time() - self.mensaje_timer >= 5:
            if self.item_a_borrar:  # Asegura que no sea None
                print(f" Se olvidó visualmente el producto: {self.item_a_borrar}")
                self.blur.add(self.item_a_borrar)
            self.mostrar_mensaje = False
            self.mensaje_actual = None
            self.item_a_borrar = None