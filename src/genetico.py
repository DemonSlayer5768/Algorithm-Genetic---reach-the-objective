# genetico.py
import random
from config import PASOS, ELITISMO, TASA_MUTACION, FUERZA_MAX
import pygame 
 
def seleccionar(poblacion):
    fitness = [ind.fitness for ind in poblacion]
    min_f = min(fitness)

    if min_f < 0:
        fitness = [f - min_f for f in fitness]

    total = sum(fitness)
    if total == 0:
        return random.sample(poblacion, ELITISMO)

    seleccionados = []
    for _ in range(ELITISMO):
        r = random.uniform(0, total)
        acc = 0
        for ind, f in zip(poblacion, fitness):
            acc += f
            if acc >= r:
                seleccionados.append(ind)
                break

    return seleccionados
# def seleccionar(poblacion):
#     seleccionados = []
#     k = 4  # tamaño del torneo

#     for _ in range(ELITISMO):
#         aspirantes = random.sample(poblacion, k)
#         ganador = max(aspirantes, key=lambda ind: ind.fitness)
#         seleccionados.append(ganador)

#     return seleccionados



def cruzar(a, b):
    punto = random.randint(0, PASOS)
    return [
        pygame.Vector2(a.genes[i]) if i < punto else pygame.Vector2(b.genes[i])
        for i in range(PASOS)
    ]


def mutar(genes):
    for i in range(PASOS):
        if random.random() < TASA_MUTACION:
            genes[i] = pygame.Vector2(
                random.uniform(-FUERZA_MAX, FUERZA_MAX),
                random.uniform(-FUERZA_MAX, FUERZA_MAX)
            )
    return genes
