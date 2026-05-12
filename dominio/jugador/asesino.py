from dominio.jugador.jugador import Jugador, Stats
from motor.sistema_combate import Combate


class Asesino(Jugador):

    def __init__(self, fila: int, columna: int):
        stats = Stats(max_vida=80, dano=20, defensa=4, pierce=True)
        super().__init__("Asesino", fila, columna, stats)

    def _aumentar_stats(self) -> None:
        self._stats.max_vida += 10
        self._stats.dano     += 5

# aumenta el critico y tiene pierce
    def atacar(self, objetivo) -> dict:
        return Combate.ejecutar_ataque(self, objetivo, self,_stats.dano,
                                       True, 15, True)
