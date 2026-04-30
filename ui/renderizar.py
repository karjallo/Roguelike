import pygame
from ui.constantes import TILE

class Renderizador:

    COLOR_PARED    = (100, 100, 100)
    COLOR_SUELO    = (50,  50,  50)
    COLOR_ESCALERA = (200, 200, 50)
    COLOR_JUGADOR  = (50,  200, 50)
    COLOR_ENEMIGO  = (200, 50,  50)
    COLOR_FONDO    = (0,   0,   0)

    ASCII = {
        "pared"    : "#",
        "suelo"    : ".",
        "escalera" : ">",
        "jugador"  : "@",
        "esqueleto": "s",
        "orco"     : "o",
        "boss"     : "B",
        "dragon"   : "D",
    }

    def __init__(self):
        self.fuente = pygame.font.SysFont("monospace", TILE, bold=True)

    def dibujar(self, pantalla, mapa, jugador, enemigos) -> None:
        pantalla.fill(self.COLOR_FONDO)
        self._dibujar_mapa(pantalla, mapa)
        self._dibujar_enemigos(pantalla, enemigos)
        self._dibujar_jugador(pantalla, jugador)

    def _dibujar_mapa(self, pantalla, mapa) -> None:
        for fila in range(mapa.alto()):
            for col in range(mapa.ancho()):
                x = col  * TILE
                y = fila * TILE

                if mapa.es_pared(fila, col):
                    simbolo = self.ASCII["pared"]
                    color   = self.COLOR_PARED
                elif mapa.es_escalera(fila, col):
                    simbolo = self.ASCII["escalera"]
                    color   = self.COLOR_ESCALERA
                else:
                    simbolo = self.ASCII["suelo"]
                    color   = self.COLOR_SUELO

                superficie = self.fuente.render(simbolo, True, color)
                pantalla.blit(superficie, (x, y))

    def _dibujar_enemigos(self, pantalla, enemigos) -> None:
        for enemigo in enemigos:
            x = enemigo.columna * TILE
            y = enemigo.fila    * TILE

            # elige simbolo y color segun tipo de enemigo
            nombre = enemigo.nombre.lower()
            if "orco" in nombre:
                simbolo = self.ASCII["orco"]
                color   = self.COLOR_ENEMIGO
            elif "dragon" in nombre:
                simbolo = self.ASCII["dragon"]
                color   = self.COLOR_ENEMIGO
            else:
                simbolo = self.ASCII["esqueleto"]
                color   = self.COLOR_ENEMIGO

            superficie = self.fuente.render(simbolo, True, color)
            pantalla.blit(superficie, (x, y))

    def _dibujar_jugador(self, pantalla, jugador) -> None:
        x = jugador.columna * TILE
        y = jugador.fila    * TILE
        superficie = self.fuente.render(self.ASCII["jugador"], True, self.COLOR_JUGADOR)
        pantalla.blit(superficie, (x, y))

