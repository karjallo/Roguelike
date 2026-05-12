from abc import abstractmethod
from dataclasses import dataclass
from dominio.entidad import Entidad, Stats
from motor.sistema_combate import Combate

class Jugador(Entidad):
    def __init__(self, nombre, fila, columna, stats: Stats):
        super().__init__(nombre, fila, columna, stats)

        self._oro           = 0
        self._experiencia   = 0
        self._nivel         = 1
        self._exp_siguiente = 100

    # metodos
    def ganar_oro(self, cantidad) -> None:
        self._oro += cantidad

    # true si subio de nivel
    def ganar_experiencia(self, cantidad) -> bool:
        self._experiencia += cantidad
        if self._experiencia >= self._exp_siguiente:
            self._subir_nivel()
            return True
        return False

    def _subir_nivel(self) -> None:
        self._nivel          += 1
        self._experiencia     = self._experiencia - self._exp_siguiente
        self._exp_siguiente   = int(self._exp_siguiente * 1.5)
        self._aumentar_stats()
        self._vida = self._stats.max_vida

    def atacar(self, objetivo) -> dict:
        return Combate.ejecutar_ataque(self, objetivo, self._stats.dano, True)

    def mover(self, df, dc, mapa, enemigos: list) -> dict:
        nueva_fila    = self.fila    + df
        nueva_columna = self.columna + dc

        for enemigo in enemigos:
            if enemigo.esta_vivo and enemigo.fila == nueva_fila and enemigo.columna == nueva_columna:
                return self.atacar(enemigo)

        if mapa.es_transitable(nueva_fila, nueva_columna):
            self.fila    = nueva_fila
            self.columna = nueva_columna
            return {"tipo": "movimiento", "atacante": self}

        return {"tipo": "bloqueado", "atacante": self}

    # propiedades
    @property
    def oro(self) -> int:
        return self._oro

    @property
    def experiencia(self) -> int:
        return self._experiencia

    @property
    def nivel(self) -> int:
        return self._nivel

    @property
    def exp_siguiente(self) -> int:
        return self._exp_siguiente

    @property
    def dano(self) -> int:
        return self._stats.dano

    @property
    def defensa(self) -> int:
        return self._stats.defensa
    @property
    def vida(self) -> int:
        return self._vida
    @property
    def max_vida(self) -> int:
        return self._stats.max_vida


    @abstractmethod
    def _aumentar_stats(self) -> None:
        pass
