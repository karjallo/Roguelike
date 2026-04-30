from .entidad import Entidad, Stats, Recompensa

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


    def distancia_manhattan(self, objetivo) -> int:
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

    def atacar(self, objetivo) -> str:
        dano = max(0, self._stats.dano - objetivo.stats.defensa)
        objetivo.recibir_dano(dano)
        msg = f"{self.nombre} golpea a {objetivo.nombre} por {dano} dmg"
        if not objetivo.esta_vivo:
            msg += f" — {objetivo.nombre} ha muerto!"
        return msg

    def tomar_turno(self, jugador, mapa) -> str:
        dist = self.distancia_manhattan(jugador)
        if dist <= 1:
            return self.atacar(jugador)
        if dist <= self._stats.fov:
            self.mover(jugador, mapa)
        return ""



class Esqueleto(Enemigo):

    def __init__(self, fila, columna):
        stats = Stats(max_vida=40, dano=8, defensa=2)
        recompensa = Recompensa(oro=20, experiencia=30)
        super().__init__(
            nombre      = "Esqueleto",
            fila        = fila,
            columna     = columna,
            stats       = stats,
            recompensa = recompensa
        )

    def grito_de_batalla(self) -> str:
        return "*Castañeo de huesos*"


class Orco(Enemigo):

    def __init__(self, fila, columna):
        stats = Stats(max_vida=80, dano=14, defensa=4, fov=8)
        recompensa = Recompensa(oro=30, experiencia=45)
        super().__init__(
            nombre      = "Orco",
            fila        = fila,
            columna     = columna,
            stats       = stats,
            recompensa  = recompensa
        )
        self._turno_actual = 0
        self._velocidad    = 2

    # sobreescribo comportamiento orco para que se mueva cada 2 turnos
    def tomar_turno(self, jugador, mapa) -> str:
        self._turno_actual += 1
        dist = self.distancia_manhattan(jugador)

        if dist <= 1:
            return self.atacar(jugador)

        # si pasamos la cantidad de turnos definida en velocidad
        # toma turno y resetea contador
        if self._turno_actual >= self._velocidad:
            self._turno_actual = 0
            if dist <= self._stats.fov:
                self.mover(jugador, mapa)

        return ""

    def grito_de_batalla(self) -> str:
        return "*Gruñido gutural*"
