import pygame  # type: ignore
import random
from config import *
from entorno import objetivo, obstaculos, inicio


class Individuo:
    def __init__(self, genes=None):
        self.pos = inicio.copy()
        self.vel = pygame.Vector2()

        self.genes = genes or [
            pygame.Vector2(
                random.uniform(-FUERZA_MAX, FUERZA_MAX),
                random.uniform(-FUERZA_MAX, FUERZA_MAX)
            ) for _ in range(PASOS)
        ]

        self.step = 0
        self.colisiones = 0
        self.llego = False
        self.vivo = True
        self.fitness = 0

        # 🔹 NUEVAS METRICAS PARA FITNESS
        self.min_distancia = self.pos.distance_to(objetivo)
        self.cambios_direccion = 0
        self.ultima_vel = pygame.Vector2()

    def update(self, limites):
        if not self.vivo:
            return
        
        if self.step >= PASOS:
            self.vivo = False
            return

        # aplicar gen
        try:
            self.vel += self.genes[self.step]
        except Exception:
            self.vivo = False
            return

        # cambios de dirección
        try:
            if self.vel.length() > 0 and self.ultima_vel.length() > 0:
                if abs(self.vel.angle_to(self.ultima_vel)) > 45:
                    self.cambios_direccion += 1
        except Exception:
            pass

        self.ultima_vel = self.vel.copy()

        # normalizar velocidad
        try:
            if self.vel.length() > 0:
                self.vel.scale_to_length(10)  # Aumentado de 7 a 10
        except Exception:
            self.vivo = False
            return

        self.pos += self.vel
        self.step += 1

        # progreso
        d = self.pos.distance_to(objetivo)
        self.min_distancia = min(self.min_distancia, d)

        if d < 10:
            self.llego = True
            self.vivo = False

        for obs in obstaculos:
            if obs.collidepoint(self.pos):
                self.colisiones += 1
                self.pos -= self.vel  # Retroceder en lugar de morir

        if not limites.collidepoint(self.pos):
            self.vivo = False

    # def calcular_fitness(self):
    #     progreso = 1 / (self.min_distancia + 1)
    #     eficiencia = 1 / (self.step + 1)
    #     suavidad = 1 / (self.cambios_direccion + 1)

    #     self.fitness = (
    #         5.0 * progreso
    #         + 30.0 * int(self.llego)
    #         + 0.5 * eficiencia
    #         + 0.1 * suavidad
    #         - 3.0 * self.colisiones
    #     )
    def calcular_fitness(self):
        # Distancia inicial desde inicio hasta objetivo
        distancia_inicial = 570.0  # (500,600) -> (500,80)
        progreso_directo = distancia_inicial - self.min_distancia
        eficiencia = 1 / (self.step + 1)
        
        self.fitness = (
            10.0 * progreso_directo    # 10 puntos por cada píxel de progreso real
            + 5000.0 * int(self.llego) # Mega bonificación si llega
            + 1.0 * eficiencia         # Pequeño bonus por eficiencia
            - 0.05 * self.colisiones   # Casi sin penalización
        )


    def draw(self, pantalla, mejor=False):
        color = (60, 220, 120) if mejor else (100, 160, 255)
        pygame.draw.circle(pantalla, color, self.pos, 4)
