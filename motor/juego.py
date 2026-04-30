import pygame
import time
from dominio.jugador    import Guerrero, Asesino, Mago
from dominio.enemigo    import Esqueleto, Orco
from dominio.mapa       import Mapa
from ui.renderizar      import Renderizador
from ui.hud             import Hud
from ui.menu            import Menu
from ui.capturar_teclas import Capturar_teclas
from ui.constantes      import ANCHO_VENTANA, ALTO_VENTANA
DELAY_MOVIMIENTO = 150

CLASES = {
    "guerrero": Guerrero,
    "asesino" : Asesino,
    "mago"    : Mago,
}

class Juego:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Roguelike")
        self.pantalla     = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        self.reloj        = pygame.time.Clock()
        self.entrada      = Capturar_teclas()
        self.renderizador = Renderizador()
        self.hud          = Hud()
        self.menu         = Menu(self.pantalla)
        self.corriendo    = True

        clase_elegida  = self.menu.seleccion_clase()
        ClaseJugador   = CLASES[clase_elegida]

        self.mapa          = Mapa()
        sp                 = self.mapa.spawn_jugador
        self.jugador       = ClaseJugador(sp[0], sp[1])
        self.enemigos      = self._generar_enemigos()
        self.tiempo_inicio     = time.time()
        self.ultimo_movimiento = 0
        self.turno_jugador     = False


    def _generar_enemigos(self) -> list:
        enemigos = []
        for i, pos in enumerate(self.mapa.spawn_enemigos):
            if i % 2 == 0:
                enemigos.append(Esqueleto(pos[0], pos[1]))
            else:
                enemigos.append(Orco(pos[0], pos[1]))
        return enemigos


    def _reiniciar(self) -> None:
        clase_elegida  = self.menu.seleccion_clase()
        ClaseJugador   = CLASES[clase_elegida]
        self.mapa      = Mapa()
        sp             = self.mapa.spawn_jugador
        self.jugador   = ClaseJugador(sp[0], sp[1])
        self.enemigos  = self._generar_enemigos()
        self.hud       = Hud()
        self.tiempo_inicio     = time.time()
        self.ultimo_movimiento = 0
        self.turno_jugador     = False
        self.corriendo         = True


    def correr(self):
        while self.corriendo:
            self._eventos()
            self._actualizar()
            segundos = int(time.time() - self.tiempo_inicio)
            self.renderizador.dibujar(self.pantalla, self.mapa, self.jugador, self.enemigos)
            self.hud.dibujar(self.pantalla, self.jugador, segundos)
            pygame.display.flip()
            self.reloj.tick(60)

        # al salir del loop pregunta si quiere reiniciar
        if not self.jugador.esta_vivo:
            jugar_de_nuevo = self.menu.pantalla_game_over(self.jugador)
            if jugar_de_nuevo:
                self._reiniciar()
                self.correr()   # vuelve a correr el juego

        pygame.quit()

    def _eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.corriendo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    msg = self.jugador.usar_habilidad(self.mapa, self.enemigos)
                    self.hud.agregar_mensaje(msg)

        df, dc = self.entrada.capturar_movimiento()
        ahora  = pygame.time.get_ticks()
        self.turno_jugador = False

        if ahora - self.ultimo_movimiento >= DELAY_MOVIMIENTO:
            if df != 0 or dc != 0:
                msg = self.jugador.mover(df, dc, self.mapa, self.enemigos)
                if msg:
                    self.hud.agregar_mensaje(msg)
                self.turno_jugador     = True
                self.ultimo_movimiento = ahora

    def _actualizar(self):
        self.enemigos = [e for e in self.enemigos if e.esta_vivo]

        if self.turno_jugador:
            for enemigo in self.enemigos:
                msg = enemigo.tomar_turno(self.jugador, self.mapa)
                if msg:
                    self.hud.agregar_mensaje(msg)

        if not self.jugador.esta_vivo:
            self.hud.agregar_mensaje("¡Has muerto! Game Over.")
            self.corriendo = False

        if self.mapa.intentar_bajar(self.jugador.fila, self.jugador.columna):
            sp                   = self.mapa.spawn_jugador
            self.jugador.fila    = sp[0]
            self.jugador.columna = sp[1]
            self.enemigos        = self._generar_enemigos()
            self.hud.agregar_mensaje("Bajaste al siguiente nivel...")
