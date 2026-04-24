from .entidad import Entidad

class Jugador(Entidad):
    def __init__(self, nombre, fila, columna, vida, dano, defensa, oro):
        super().__init__(nombre, fila, columna, vida, dano, defensa)
        self.oro = oro
