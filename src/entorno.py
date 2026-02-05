# entorno.py
import pygame #type: ignore
from config import ANCHO, ALTO

inicio = pygame.Vector2(ANCHO // 2, ALTO - 50)
objetivo = pygame.Vector2(ANCHO // 2, 80)

obstaculos = [
    pygame.Rect(300, 200, 400, 30),
    pygame.Rect(150, 350, 700, 30)
]
