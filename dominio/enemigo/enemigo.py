from dominio.entidad import Entidad, Stats, Recompensa
from motor.sistema_combate import Combate

class Enemigo(Entidad):

    def __init__(self, nombre, fila, columna, stats, recompensa):
        super().__init__(nombre, fila, columna, stats)
        self._recompensa   = recompensa

    @property
    def oro(self) -> int:
        return self._recompensa.oro

    @property
    def experiencia(self) -> int:
        return self._recompensa.experiencia

    @property
    def fov(self) -> int:
        return self._stats.fov


    def _distancia_manhattan(self, objetivo) -> int:
        return abs(self.fila - objetivo.fila) + abs(self.columna - objetivo.columna)

    def mover(self, objetivo, mapa) -> None:
        dx = objetivo.fila    - self.fila
        dy = objetivo.columna - self.columna

        if dx != 0:
            nueva_fila = self.fila + (1 if dx > 0 else -1)
            if mapa.es_transitable(nueva_fila, self.columna):
                self.fila = nueva_fila
                return

        if dy != 0:
            nueva_columna = self.columna + (1 if dy > 0 else -1)
            if mapa.es_transitable(self.fila, nueva_columna):
                self.columna = nueva_columna


    def atacar(self, objetivo) -> dict:
        return Combate.ejecutar_ataque(self, objetivo, self._stats.dano)

    def tomar_turno(self, jugador, mapa) -> None:
        dist = self._distancia_manhattan(jugador)
        if dist <= 1:
            return self.atacar(jugador)
        if dist <= self._stats.fov:
            self.mover(jugador, mapa)
