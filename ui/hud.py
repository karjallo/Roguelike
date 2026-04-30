import pygame
from ui.constantes import ANCHO_JUEGO, ALTO_JUEGO, ANCHO_STATS, ALTO_MENSAJES, ALTO_VENTANA, NEGRO, GRIS, BLANC, ROJO, VERDE, AMARIL

# HUD
class Hud:

    def __init__(self):
        self.fuente        = pygame.font.SysFont("monospace", 13)
        self.fuente_titulo = pygame.font.SysFont("monospace", 14, bold=True)
        self.mensajes      = []
        self.max_mensajes  = 3

    def agregar_mensaje(self, texto: str) -> None:
        if not texto:
            return
        self.mensajes.append(texto)
        if len(self.mensajes) > self.max_mensajes:
            self.mensajes.pop(0)

    def dibujar(self, pantalla, jugador, segundos: int) -> None:
        self._dibujar_stats(pantalla, jugador, segundos)
        self._dibujar_mensajes(pantalla)
        self._dibujar_leyenda(pantalla)

    def _dibujar_stats(self, pantalla, jugador, segundos: int) -> None:
        pygame.draw.rect(pantalla, GRIS, (ANCHO_JUEGO, 0, ANCHO_STATS, ALTO_VENTANA))
        pygame.draw.line(pantalla, BLANC, (ANCHO_JUEGO, 0), (ANCHO_JUEGO, ALTO_VENTANA), 1)

        x   = ANCHO_JUEGO + 10
        y   = [10]
        sep = 22

        def texto(contenido, color=BLANC):
            sup = self.fuente.render(contenido, True, color)
            pantalla.blit(sup, (x, y[0]))
            y[0] += sep

        def titulo(contenido):
            sup = self.fuente_titulo.render(contenido, True, AMARIL)
            pantalla.blit(sup, (x, y[0]))
            y[0] += sep
            pygame.draw.line(pantalla, AMARIL, (x, y[0] - 4), (x + ANCHO_STATS - 20, y[0] - 4), 1)

        titulo("[ PERSONAJE ]")
        texto(f"Clase : {jugador.nombre}")
        texto(f"Nivel : {jugador.nivel}")
        texto(f"EXP   : {jugador.experiencia}/{jugador.exp_siguiente}")
        texto(f"Oro   : {jugador.oro}", AMARIL)
        texto(f"Tiempo: {self._formato_tiempo(segundos)}")

        y[0] += 10
        titulo("[ COMBATE ]")
        texto(f"ATK : {jugador.dano}")
        texto(f"DEF : {jugador.defensa}")

        y[0] += 10
        titulo("[ VIDA ]")
        self._barra(pantalla, x, y[0], jugador.vida, jugador.max_vida, ROJO)
        y[0] += 16
        texto(f"{jugador.vida} / {jugador.max_vida}", ROJO)

        y[0] += 10
        titulo(f"[ {jugador.recurso_nombre.upper()} ]")
        self._barra(pantalla, x, y[0], jugador.recurso, jugador.recurso_max, jugador.recurso_color)
        y[0] += 16
        texto(f"{jugador.recurso} / {jugador.recurso_max}", jugador.recurso_color)

    def _barra(self, pantalla, x, y, valor, maximo, color) -> None:
        ancho_total = ANCHO_STATS - 20
        ancho_lleno = int(ancho_total * valor / maximo) if maximo > 0 else 0
        pygame.draw.rect(pantalla, (60, 60, 60), (x, y, ancho_total, 12))
        pygame.draw.rect(pantalla, color,        (x, y, ancho_lleno, 12))
        pygame.draw.rect(pantalla, BLANC,        (x, y, ancho_total, 12), 1)

    def _dibujar_mensajes(self, pantalla) -> None:
        pygame.draw.rect(pantalla, GRIS, (0, ALTO_JUEGO, ANCHO_JUEGO, ALTO_MENSAJES))
        pygame.draw.line(pantalla, BLANC, (0, ALTO_JUEGO), (ANCHO_JUEGO, ALTO_JUEGO), 1)
        for i, msg in enumerate(self.mensajes):
            sup = self.fuente.render(msg, True, BLANC)
            pantalla.blit(sup, (10, ALTO_JUEGO + 6 + i * 14))


    def _dibujar_leyenda(self, pantalla) -> None:
        fuente = self.fuente

        leyenda = [
            ("@", "Jugador",   (50,  200, 50)),
            ("s", "Esqueleto", (200, 50,  50)),
            ("o", "Orco",      (200, 130, 30)),
            ("D", "Dragón",    (200, 50,  50)),
            ("#", "Pared",     (100, 100, 100)),
            (".", "Suelo",     (50,  50,  50)),
            (">", "Escalera",  (200, 200, 50)),
        ]

        # titulo
        x     = ANCHO_JUEGO + 10
        y     = ALTO_VENTANA - (len(leyenda) * 18) - 30
        titulo = self.fuente_titulo.render("[ LEYENDA ]", True, (200, 200, 50))
        pantalla.blit(titulo, (x, y))
        pygame.draw.line(pantalla, (200, 200, 50),
                         (x, y + 18), (x + ANCHO_STATS - 20, y + 18), 1)
        y += 24

        for simbolo, nombre, color in leyenda:
            sup_simbolo = fuente.render(simbolo, True, color)
            sup_nombre  = fuente.render(f" {nombre}", True, (200, 200, 200))
            pantalla.blit(sup_simbolo, (x,      y))
            pantalla.blit(sup_nombre,  (x + 14, y))
            y += 18


    @staticmethod
    def _formato_tiempo(segundos: int) -> str:
        m = segundos // 60
        s = segundos % 60
        return f"{m:02d}:{s:02d}"

