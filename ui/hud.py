import curses
from ui.constantes import (ANCHO_MAPA, ALTO_MAPA, ANCHO_STATS, ALTO_MENSAJES,
                           COLOR_TITULO, COLOR_ORO, COLOR_VIDA, COLOR_RECURSO)


class Hud:

    def __init__(self):
        self.mensajes     = []
        self.max_mensajes = ALTO_MENSAJES

    def agregar_mensaje(self, texto: str) -> None:
        if not texto:
            return
        self.mensajes.append(texto)
        if len(self.mensajes) > self.max_mensajes:
            self.mensajes.pop(0)

    def dibujar(self, stdscr, jugador, segundos: int, of: int = 0, oc: int = 0) -> None:
        # of = offset fila
        # oc = offsets columna
        self._dibujar_stats(stdscr, jugador, segundos, of, oc)
        self._dibujar_mensajes(stdscr, of, oc)

    def _dibujar_stats(self, stdscr, jugador, segundos: int, of: int, oc: int) -> None:
        # columna de inicio del panel = offset + ancho del mapa + 1 (separador)
        columna = oc + ANCHO_MAPA + 2
        fila = of

        def titulo(txt):
            nonlocal fila
            self._put(stdscr, fila, columna, txt, COLOR_TITULO)
            fila += 2

        # par=0, seria el color por defecto blanco
        def linea(txt, par=0):
            nonlocal fila
            self._put(stdscr, fila, columna, txt, par)
            fila += 1

        titulo("[ PERSONAJE ]")
        linea(f"Clase : {jugador.nombre}")
        linea(f"Nivel : {jugador.nivel}")
        linea(f"EXP   : {jugador.experiencia}/{jugador.exp_siguiente}")
        linea(f"Oro   : {jugador.oro}", COLOR_ORO)
        linea(f"Tiempo: {self._formato_tiempo(segundos)}")
        fila += 1

        titulo("[ COMBATE ]")
        linea(f"ATK : {jugador.dano}")
        linea(f"DEF : {jugador.defensa}")
        fila += 1

        titulo("[ VIDA ]")
        linea(self._barra(jugador.vida, jugador.max_vida), COLOR_VIDA)
        linea(f"{jugador.vida}/{jugador.max_vida}", COLOR_VIDA)
        fila += 3

        titulo("[ CONTROLES ]")
        linea("WASD / flechas")
        linea("ESPACIO ataque a distancia")
        linea("Q        salir")

    # log
    def _dibujar_mensajes(self, stdscr, of: int, oc: int) -> None:
        for i, msg in enumerate(self.mensajes):
            fila = of + ALTO_MAPA + i
            txt  = msg[:ANCHO_MAPA].ljust(ANCHO_MAPA)
            try:
                stdscr.addstr(fila, oc, txt)
            except curses.error:
                pass

    # barra de vida
    @staticmethod
    def _barra(valor, maximo, ancho=18) -> str:
        if maximo > 0:
            llenos = int(ancho * valor / maximo)
        else:
            llenos = 0
        return "[" + "█" * llenos + "░" * (ancho - llenos) + "]"

    @staticmethod
    def _formato_tiempo(segundos) -> str:
        m, s = segundos // 60, segundos % 60
        return f"{m:02d}:{s:02d}"

    # un alias para ncurses
    @staticmethod
    def _put(stdscr, fila, col, texto, par: int = 0) -> None:
        try:
            stdscr.addstr(fila, col, texto, curses.color_pair(par))
        except curses.error:
            pass
