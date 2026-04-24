from .entidad import Entidad

class Enemigo(Entidad):
    def __init__(self, nombre, fila, columna, vida, dano, defensa, recompensa, fov, experiencia)
        super().__init__(nombre, fila, columna, vida, dano, defensa)
        self.recompensa = recompensa
        self.fov = fov
        self.experiencia = experiencia
