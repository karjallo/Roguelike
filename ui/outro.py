import curses

class Outro:
    @staticmethod
    def mostrar(stdscr, jugador, segundos: int, titulo="¡VICTORIA!"):
        # limpiamos terminal
        stdscr.clear()
        alto, ancho = stdscr.getmaxyx()
        stdscr.nodelay(False)
        #curses.curs_set(0)

        lineas = [
            titulo,
            "==================================",
            "    HASTA AQUÍ LLEGÓ EL DEMO      ",
            "==================================",
            "",
            f" Clase:           {jugador.nombre}",
            f" Nivel Alcanzado: {jugador.nivel}",
            f" Oro Recolectado: {jugador.oro}",
            f" Tiempo Total:    {segundos}s",
            "",
            "==================================",
            "Presiona cualquier tecla para salir"
        ]

        # centrar
        vertical_inicio = (alto // 2) - (len(lineas) // 2)

        # dibuja cada linea
        for i, texto in enumerate(lineas):
            #centramos
            horizontal_centro = (ancho // 2) - (len(texto) // 2)

            # va aumentando en i, siendo el indice
            vertical = vertical_inicio + i

            # titulo
            estilo = curses.A_BOLD if i == 0 else curses.A_NORMAL

            # intentamos dibujar
            try:
                stdscr.addstr(vertical, horizontal_centro, texto, estilo)
            # si es muy pequena la terminal, ignoramos error
            except curses.error:
                pass

        stdscr.refresh()
        # sale en el momento en el que se aprieta una tecla
        stdscr.getch()
