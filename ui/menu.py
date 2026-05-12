import curses
from ui.constantes import COLOR_TITULO, COLOR_STATS

class Menu:

    def __init__(self, stdscr):
        self.stdscr = stdscr

    def seleccion_clase(self) -> str:
        # lista de opciones:
        opciones = [
            ('1', "guerrero", "Guerrero", "Tanque resistente. +vida + defensa."),
            ('2', "asesino",  "Asesino",  "Veloz y letal, +crit +ataque."),
            ('3', "mago",     "Mago",     "Frágil pero poderoso, ataque a distancia"),
        ]

        while True:
            self.stdscr.erase()
            vertical, horizontal = self.stdscr.getmaxyx()

            # dibujar titulo centrado
            titulo = "=== Elegí tu clase ==="
            pos_horizontal_titulo = (horizontal // 2) - (len(titulo) // 2)
            self.stdscr.addstr(2, pos_horizontal_titulo, titulo, curses.color_pair(COLOR_TITULO) | curses.A_BOLD)

            # dibujar opciones
            fila_actual = 6
            for opcion in opciones:
                tecla = opcion[0]
                nombre = opcion[2]
                desc = opcion[3]

                # tecla y nombre
                self.stdscr.addstr(fila_actual, 4, f"[{tecla}]  {nombre}", curses.color_pair(COLOR_TITULO))
                #descripcion
                self.stdscr.addstr(fila_actual + 1, 4, f"     {desc}")

                # aumentamos espacio para siguiente opcion
                fila_actual = fila_actual + 3

            self.stdscr.refresh()

            # caputrar tecla
            tecla_presionada = self.stdscr.getch()

            if tecla_presionada == ord('1'):
                return "guerrero"
            if tecla_presionada == ord('2'):
                return "asesino"
            if tecla_presionada == ord('3'):
                return "mago"

    def pantalla_game_over(self, jugador) -> bool:
        while True:
            self.stdscr.erase()
            vertical, horizontal = self.stdscr.getmaxyx()

            titulo = "HAS MUERTO"
            pos_horizontal_titulo = (horizontal // 2) - (len(titulo) // 2)
            self.stdscr.addstr(3, pos_horizontal_titulo, titulo, curses.color_pair(1) | curses.A_BOLD)

            stats = [
                f"Clase      : {jugador.nombre}",
                f"Nivel      : {jugador.nivel}",
                f"Oro        : {jugador.oro}",
                f"Experiencia: {jugador.experiencia}",
            ]

            # dibujar stats
            fila_stats = 6
            for linea in stats:
                pos_horizontal_linea = (horizontal // 2) - (len(linea) // 2)
                self.stdscr.addstr(fila_stats, pos_horizontal_linea, linea)
                # espacio entre stats
                fila_stats = fila_stats + 1

            # dibujar opciones para rejugar o salir
            opciones_txt = "Presiona cualquier tecla para salir"
            pos_horizontal_opc = (horizontal // 2) - (len(opciones_txt) // 2)
            self.stdscr.addstr(12, pos_horizontal_opc, opciones_txt, curses.color_pair(COLOR_TITULO))

            self.stdscr.refresh()

            tecla_presionada = self.stdscr.getch()

            if tecla_presionada:
                return False
