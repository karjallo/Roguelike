from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Stats:
    max_vida : int
    dano     : int
    defensa  : int
    fov      : int  = 5
    pierce   : bool = False

@dataclass
class Recompensa:
    oro         : int
    experiencia : int


class Entidad(ABC):

    def __init__(self, nombre: str, fila: int, columna: int, stats: Stats):
        self.nombre  = nombre
        self.fila    = fila
        self.columna = columna
        self._stats  = stats
        self._vida   = stats.max_vida

    # métodos
    def recibir_dano(self, cantidad: int, pierce: bool = False) -> int:
        if pierce:
            dano_real = cantidad
        else:
            # mínimo 1 de daño: evita que alta defensa cure al objetivo
            dano_real = max(1, cantidad - self._stats.defensa)

        self._vida = max(0, self._vida - dano_real)
        return dano_real

    @property
    def esta_vivo(self) -> bool:
        return self._vida > 0

    # metodos abstractos
    @abstractmethod
    def atacar(self, objetivo) -> dict:
        pass

    @abstractmethod
    def mover(self, *args, **kwargs):
        pass
