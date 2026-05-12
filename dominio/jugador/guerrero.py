from dominio.jugador.jugador import Jugador, Stats

class Guerrero(Jugador):

    def __init__(self, fila: int, columna: int):
        stats = Stats(max_vida=120, dano=15, defensa=6)
        super().__init__("Guerrero", fila, columna, stats)

    def _aumentar_stats(self) -> None:
        self._stats.max_vida += 20
        self._stats.dano     += 2
