import curses
import time
import pygame

# dominio
from dominio.jugador.guerrero import Guerrero
from dominio.jugador.asesino import Asesino
from dominio.jugador.mago import Mago
from dominio.enemigo.esqueleto import Esqueleto
from dominio.enemigo.orco import Orco
from dominio.mapa.mapa import Mapa

# consola
from ui.renderizar import Renderizador
from ui.hud import Hud
from ui.menu import Menu
from ui.outro import Outro

# motor
from motor.capturar_teclas import Capturar_teclas
from motor.gestor_sonido import Gestor_sonido

CLASES = {
    "guerrero": Guerrero,
    "asesino":  Asesino,
    "mago":     Mago,
}


class Juego:

    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        # permite la utilizacion de flechas en lugar de sus
        # escape codes ^[[A
        self.stdscr.keypad(True)
        # asegura que la funcion de pedir tecla congele el juego
        self.stdscr.nodelay(False)

        # ui
        self.renderizador = Renderizador()
        self.renderizador.inicializar_colores()
        self.renderizador.calcular_offsets(stdscr)
        self.hud = Hud()
        self.menu = Menu(stdscr)

        # motor
        self.entrada = Capturar_teclas()
        self.audio   = Gestor_sonido()
        self.audio.musica_fondo("assets/musica/background.mp3")

        # estado inicial
        self.corriendo = True
        clase_elegida = self.menu.seleccion_clase()
        self._iniciar_partida(clase_elegida)
        self.correr()

    # ------------------------------------------------------------------
    # Inicialización
    # ------------------------------------------------------------------

    def _iniciar_partida(self, clase_elegida: str) -> None:
        ClaseJugador = CLASES[clase_elegida]
        self.mapa = Mapa()
        sp = self.mapa.spawn_jugador
        self.jugador = ClaseJugador(sp[0], sp[1])
        self.enemigos = self._generar_enemigos()
        self.tiempo_inicio = time.monotonic()

    def _generar_enemigos(self) -> list:
        enemigos = []
        for i in range(len(self.mapa.spawn_enemigos)):
            pos = self.mapa.spawn_enemigos[i]
            if i % 2 == 0:
                enemigo = Esqueleto(pos[0], pos[1])
            else:
                enemigo = Orco(pos[0], pos[1])
            enemigos.append(enemigo)
        return enemigos

    # bucle principal
    def correr(self) -> None:
        try:
            while self.corriendo:

                # dibujar momento inicial
                segundos = int(time.monotonic() - self.tiempo_inicio)
                self.renderizador.dibujar(self.stdscr, self.mapa, self.jugador, self.enemigos)
                self.hud.dibujar(self.stdscr, self.jugador, segundos,
                                 of=self.renderizador.offset_f,
                                 oc=self.renderizador.offset_c)
                self.stdscr.refresh()

                # leer tecla
                tecla = self.stdscr.getch()

                # key_resize es una senal que significa que se redimensiono la terminal
                # por lo tanto se calcula el offset nuevamente
                if tecla == curses.KEY_RESIZE:
                    self.renderizador.calcular_offsets(self.stdscr)
                    continue

                if self.entrada.es_salir(tecla):
                    self.corriendo = False
                    continue

                # si se apreto tecla valida, true
                turno_completado = self._turno_jugador(tecla)
                if turno_completado:
                    self._turno_enemigos()
                    self._verificar_estado()

            self._finalizar()
        finally:
            pygame.mixer.music.stop()
            pygame.mixer.quit()


    # returna true si fue valido
    def _turno_jugador(self, tecla: int) -> bool:
        if self.entrada.es_movimiento(tecla):
            df, dc = self.entrada.tecla_a_movimiento(tecla)
            resultado = self.jugador.mover(df, dc, self.mapa, self.enemigos)
            self._procesar_resultado(resultado)
            return True

        if self.entrada.es_ataque_distancia(tecla) and self.jugador.nombre == "Mago":
            resultado = self.jugador.atacar_distancia(self.enemigos)
            self._procesar_resultado(resultado)
            return True

        return False

    def _turno_enemigos(self) -> None:
        self._eliminar_enemigos_muertos()
        for enemigo in self.enemigos:
            resultado = enemigo.tomar_turno(self.jugador, self.mapa)
            self._procesar_resultado(resultado)

    # procesamiento de resultados para el log
    def _procesar_resultado(self, resultado: dict | None) -> None:
        if not resultado:
            return

        tipo     = resultado.get("tipo")
        atacante = resultado.get("atacante")

        if tipo == "sin_objetivo":
            self.hud.agregar_mensaje("No hay enemigos en rango.")

        elif tipo == "movimiento":
            self.audio.reproducir("jugador_paso")

        elif tipo == "ataque":
            self._procesar_ataque(resultado)

    def _procesar_ataque(self, resultado: dict) -> None:
        atacante = resultado["atacante"]
        objetivo = resultado["objetivo"]

        msg = f"{atacante.nombre} golpea a {objetivo.nombre} por {resultado['dano']} dmg"

        if resultado["critico"]:
            msg += " ¡CRÍTICO!"
        if resultado["muerto"]:
            msg += f" — {objetivo.nombre} muere!"

        self.hud.agregar_mensaje(msg)

        if resultado["level_up"]:
            self.hud.agregar_mensaje(f"¡{atacante.nombre} subió de nivel!")
            self.audio.reproducir("subir_nivel")

        sonido_base = objetivo.__class__.__name__.lower()
        if resultado["muerto"]:
            self.audio.reproducir(f"{sonido_base}_muerte")
        else:
            self.audio.reproducir(f"{sonido_base}_ataque")

    # estado de juego
    def _verificar_estado(self) -> None:
        if not self.jugador.esta_vivo:
            self.corriendo = False
            return

        if self.mapa.intentar_bajar(self.jugador.fila, self.jugador.columna):
            self.hud.agregar_mensaje("Has descendido de nivel...")
            self._siguiente_nivel()

    def _siguiente_nivel(self) -> None:
        self.mapa = Mapa()
        sp = self.mapa.spawn_jugador
        self.jugador.fila    = sp[0]
        self.jugador.columna = sp[1]
        self.enemigos = self._generar_enemigos()

    def _eliminar_enemigos_muertos(self) -> None:
        vivos = []
        for enemigo in self.enemigos:
            if enemigo.esta_vivo:
                vivos.append(enemigo)
        self.enemigos = vivos

    # fin de partida, muestra score
    def _finalizar(self) -> None:
        if not self.jugador.esta_vivo:
            self.menu.pantalla_game_over(self.jugador)
