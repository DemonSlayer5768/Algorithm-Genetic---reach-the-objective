# main.py
import pygame 
import random
from config import *
from individuo import Individuo
from genetico import seleccionar, cruzar, mutar
from entorno import obstaculos, objetivo

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Algoritmo Genético - Llegar al Objetivo")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("Consolas", 16)


def main():
    poblacion = [Individuo() for _ in range(POBLACION)]
    limites = pantalla.get_rect()
    generacion = 1
    mejor = None
    llegados = 0

    while True:
        reloj.tick(0)  # Sin límite de FPS
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return

        pantalla.fill((20, 20, 20))
        pygame.draw.circle(pantalla, (220, 60, 60), objetivo, 10)
        for obs in obstaculos:
            pygame.draw.rect(pantalla, (120, 120, 120), obs)

        vivos = False

        
        for ind in poblacion:
            ind.update(limites)
            ind.draw(pantalla)
            if ind.vivo:
                vivos = True


        # for ind in poblacion:
        #     try:
        #         ind.update(limites)
        #         ind.draw(pantalla)
        #         if ind.vivo:
        #             vivos = True
        #     except Exception as e:
        #         ind.vivo = False

        if not vivos:
            for ind in poblacion:
                ind.calcular_fitness()

            # Contar individuos que llegaron al objetivo
            llegados = sum(1 for ind in poblacion if ind.llego)

            padres = seleccionar(poblacion)
            mejor = padres[0]

            # Crear nuevos individuos con los genes de los mejores padres
            nueva = [Individuo([g.copy() if hasattr(g, 'copy') else pygame.Vector2(g) for g in pad.genes]) for pad in padres]
            while len(nueva) < POBLACION:
                a, b = random.sample(padres, 2)
                genes = mutar(cruzar(a, b))
                nueva.append(Individuo(genes))

            poblacion = nueva
            generacion += 1

        if mejor:
            mejor.draw(pantalla, mejor=True)

        texto = fuente.render(
            f"Gen: {generacion} | Mejor fitness: {mejor.fitness:.3f} | Llegados: {llegados}/{POBLACION}" if mejor else "",
            True, (240, 240, 240)
        )
        pantalla.blit(texto, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    main()
