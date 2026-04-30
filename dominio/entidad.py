from abc import ABC, abstractmethod
from dataclasses import dataclass


# dataclass permite definir datos sin hacer __init__ y permite
# hacer un print de estos
@dataclass
class Stats:
    max_vida : int
    dano     : int
    defensa  : int
    fov      : int  = 5
    pierce   : bool = False

@dataclass
class Recompensa:
    oro         : int = 0
    experiencia : int = 0

class Entidad(ABC):

    def __init__(self, nombre: str, fila: int, columna: int, stats: Stats):
        self.nombre   = nombre
        self.fila     = fila
        self.columna  = columna
        self._stats   = stats
        self._vida    = stats.max_vida

    # propiedades
    @property
    def vida(self) -> int:
        return self._vida

    @property
    def max_vida(self) -> int:
        return self._stats.max_vida

    @property
    def dano(self) -> int:
        return self._stats.dano

    @property
    def defensa(self) -> int:
        return self._stats.defensa

    @property
    def stats(self) -> Stats:
        return self._stats

    @property
    def pierce(self) -> bool:
        return self._stats.pierce

    @property
    def esta_vivo(self) -> bool:
        return self._vida > 0


    # metodos
    def recibir_dano(self, cantidad: int, pierce: bool = False) -> int:
        if pierce:
            self._vida = max(0, self._vida - cantidad)
            return cantidad

        # si defensa > cantidad, que no cure al objetivo
        dano_real = max(0, cantidad - self._stats.defensa)
        # evitar valores menores a 0 e vida
        self._vida = max(0, self._vida - dano_real)
        return dano_real


    def curar(self, cantidad: int) -> None:
        # evitar curar mas alla de max_vida
        self._vida = min(self._vida + cantidad, self._stats.max_vida)

    # metodos abstractos
    @abstractmethod
    def atacar(self, objetivo) -> str:
        pass

    @abstractmethod
    def mover(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def grito_de_batalla(self) -> str:
        pass
