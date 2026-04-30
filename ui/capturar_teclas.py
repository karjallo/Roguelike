import pygame

class Capturar_teclas:

    def capturar_movimiento(self) -> tuple[int, int]:
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]    or teclas[pygame.K_w]: return (-1,  0)
        if teclas[pygame.K_DOWN]  or teclas[pygame.K_s]: return ( 1,  0)
        if teclas[pygame.K_LEFT]  or teclas[pygame.K_a]: return ( 0, -1)
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: return ( 0,  1)
        return (0, 0)
