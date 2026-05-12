import curses
from ui.constantes import (
    COLOR_PARED, COLOR_SUELO, COLOR_ESCALERA, COLOR_JUGADOR,
    COLOR_ENEMIGO, COLOR_TITULO, COLOR_STATS, COLOR_ORO,
    COLOR_VIDA, COLOR_RECURSO, ANCHO_MAPA, ALTO_MAPA,
    ANCHO_STATS, ALTO_MENSAJES
)

class Renderizador:

    ascii = {
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
        self.CONTENIDO_COLS = ANCHO_MAPA + 1 + ANCHO_STATS
        self.CONTENIDO_FILAS = ALTO_MAPA + ALTO_MENSAJES
        self.offset_f = 0
        self.offset_c = 0

    def inicializar_colores(self) -> None:
        curses.start_color()
        curses.use_default_colors()

        # curses.init_pair toma 3 args (indice, color fg y color bg)
        # siendo -1, el color bg para mantener el de la terminal
        curses.init_pair(COLOR_PARED,    curses.COLOR_WHITE,  -1)
        curses.init_pair(COLOR_SUELO,    curses.COLOR_WHITE,  -1)
        curses.init_pair(COLOR_ESCALERA, curses.COLOR_YELLOW, -1)
        curses.init_pair(COLOR_JUGADOR,  curses.COLOR_GREEN,  -1)
        curses.init_pair(COLOR_ENEMIGO,  curses.COLOR_RED,    -1)
        curses.init_pair(COLOR_TITULO,   curses.COLOR_YELLOW, -1)
        curses.init_pair(COLOR_STATS,    curses.COLOR_WHITE,  -1)
        curses.init_pair(COLOR_ORO,      curses.COLOR_YELLOW, -1)
        curses.init_pair(COLOR_VIDA,     curses.COLOR_RED,    -1)
        curses.init_pair(COLOR_RECURSO,  curses.COLOR_CYAN,   -1)

    def calcular_offsets(self, stdscr) -> None:
        term_filas, term_cols = stdscr.getmaxyx()
        self.offset_f = max(0, (term_filas - self.CONTENIDO_FILAS) // 2)
        self.offset_c = max(0, (term_cols  - self.CONTENIDO_COLS)  // 2)

    def dibujar(self, stdscr, mapa, jugador, enemigos) -> None:
        stdscr.erase()
        self._dibujar_mapa(stdscr, mapa)
        self._dibujar_enemigos(stdscr, enemigos)
        self._dibujar_jugador(stdscr, jugador)

    def _dibujar_mapa(self, stdscr, mapa) -> None:
        for fila in range(mapa.alto()):
            for col in range(mapa.ancho()):
                if mapa.es_pared(fila, col):
                    simbolo, par = self.ascii["pared"], COLOR_PARED
                elif mapa.es_escalera(fila, col):
                    simbolo, par = self.ascii["escalera"], COLOR_ESCALERA
                else:
                    simbolo, par = self.ascii["suelo"], COLOR_SUELO

                self._put(stdscr, self.offset_f + fila, self.offset_c + col, simbolo, par)

    def _dibujar_enemigos(self, stdscr, enemigos) -> None:
        for e in enemigos:
            nombre = e.nombre.lower()
            if "orco"   in nombre: simbolo = self.ascii["orco"]
            elif "dragon" in nombre: simbolo = self.ascii["dragon"]
            else:                    simbolo = self.ascii["esqueleto"]

            self._put(stdscr, self.offset_f + e.fila, self.offset_c + e.columna,
                      simbolo, COLOR_ENEMIGO)

    def _dibujar_jugador(self, stdscr, jugador) -> None:
        self._put(stdscr, self.offset_f + jugador.fila, self.offset_c + jugador.columna,
                  self.ascii["jugador"], COLOR_JUGADOR)

    @staticmethod
    def _put(stdscr, fila, col, texto, par) -> None:
        try:
            stdscr.addstr(fila, col, texto, curses.color_pair(par))
        except curses.error:
            pass
