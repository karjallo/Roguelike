from abc import ABC, abstractmethod

class Entidad(ABC):
    def __init__(self, nombre, fila, columna, vida, dano, defensa)
        self.nombre = nombre
        self.fila = fila
        self.columna = columna
        self.vida = vida
        self.dano = dano
        self.defensa = defensa

    @abstractmethod
    def atacar(self, objetivo):
        # cada clase tendra que definir su propio ataque
        pass

    @abstractmethod
    def mover(self, fila_destino, columna_destino):
        # cada clase definira como se mueve
        pass

    @abstractmethod
    def recibir_dano(self, cantidad):
        # modificar vida
        pass
