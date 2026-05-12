from dominio.enemigo.enemigo import Enemigo, Stats, Recompensa

class Esqueleto(Enemigo):

    def __init__(self, fila, columna):
        stats = Stats(max_vida=50, dano=9, defensa=2)
        recompensa = Recompensa(oro=20, experiencia=30)
        super().__init__(
            nombre      = "Esqueleto",
            fila        = fila,
            columna     = columna,
            stats       = stats,
            recompensa  = recompensa
        )

