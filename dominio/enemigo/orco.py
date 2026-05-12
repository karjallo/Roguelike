from dominio.enemigo.enemigo import Enemigo, Stats, Recompensa


class Orco(Enemigo):

    def __init__(self, fila, columna):
        stats      = Stats(max_vida=90, dano=12, defensa=5, fov=8)
        recompensa = Recompensa(oro=30, experiencia=45)
        super().__init__(
            nombre     = "Orco",
            fila       = fila,
            columna    = columna,
            stats      = stats,
            recompensa = recompensa,
        )
        self._turno_actual = 0
        self._velocidad    = 2

    def tomar_turno(self, jugador, mapa) -> dict | None:
        self._turno_actual += 1
        dist = self._distancia_manhattan(jugador)

        if dist <= 1:
            return self.atacar(jugador)

        # el orco solo se mueve cada _velocidad turnos
        if self._turno_actual >= self._velocidad:
            self._turno_actual = 0
            if dist <= self._stats.fov:
                self.mover(jugador, mapa)

        return None
