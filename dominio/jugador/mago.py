from dominio.jugador.jugador import Jugador, Stats


class Mago(Jugador):

    def __init__(self, fila: int, columna: int):
        stats = Stats(max_vida=60, dano=13, defensa=1, fov=4)
        super().__init__("Mago", fila, columna, stats)

    def _aumentar_stats(self) -> None:
        self._stats.max_vida += 5
        self._stats.dano += 4

    def _distancia(self, enemigo):
        return abs(self.fila - enemigo.fila) + abs(self.columna - enemigo.columna)

    def atacar_distancia(self, enemigos):
        en_rango = []
        for enemigo in enemigos:
            if enemigo.esta_vivo and self._distancia(enemigo) <= self._stats.fov:
                en_rango.append(enemigo)

        if not en_rango:
            return {"tipo": "sin_objetivo", "atacante": self}

        mas_cercano = en_rango[0]
        for enemigo in en_rango:
            if self._distancia(enemigo) < self._distancia(mas_cercano):
                mas_cercano = enemigo

        objetivo = mas_cercano
        return self.atacar(objetivo)
