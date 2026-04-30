from .entidad import Entidad, Stats
from abc import abstractmethod


# clase abstracta jugador
class Jugador(Entidad):

    def __init__(self, nombre: str, fila: int, columna: int, stats: Stats):
        super().__init__(nombre, fila, columna, stats)
        self._oro         = 0
        self._experiencia = 0
        self._nivel       = 1
        self._recurso     = 100
        self._recurso_max = 100
        self._exp_siguiente = 100
        self._recurso_nombre = ""
        self._recurso_color : tuple

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
    def recurso(self) -> int:
        return self._recurso

    @property
    def recurso_max(self) -> int:
        return self._recurso

    @property
    def recurso_nombre(self) -> str:
        return self._recurso_nombre

    @property
    def recurso_color(self) -> tuple:
        return self._recurso_color

    @property
    def exp_siguiente(self) -> int:
        return self._exp_siguiente

    # metodos
    def ganar_oro(self, cantidad: int) -> None:
        self._oro += cantidad

    def ganar_experiencia(self, cantidad: int) -> None:
        self._experiencia += cantidad
        if self._experiencia >= self._exp_siguiente:
            self._subir_nivel()

    def _subir_nivel(self) -> None:
        self._nivel       += 1
        self._experiencia  = 0
        self._exp_siguiente = int(self._exp_siguiente * 1.5)
        print(f"{self.nombre} subió al nivel {self._nivel}!")

    def atacar(self, objetivo) -> str:
        dano = max(0, self._stats.dano - objetivo.defensa)
        dano_real = objetivo.recibir_dano(dano, self._stats.pierce)
        msg = f"{self.nombre} golpea a {objetivo.nombre} por {dano_real} dmg"
        if not objetivo.esta_vivo:
            self.ganar_experiencia(objetivo.experiencia)
            self.ganar_oro(objetivo.oro)
            msg += f" — {objetivo.nombre} muere!"
        return msg

    def mover(self, df: int, dc: int, mapa, enemigos: list) -> str:
        nueva_fila    = self.fila    + df
        nueva_columna = self.columna + dc

        for enemigo in enemigos:
            if enemigo.esta_vivo and enemigo.fila == nueva_fila and enemigo.columna == nueva_columna:
                return self.atacar(enemigo)

        if mapa.es_transitable(nueva_fila, nueva_columna):
            self.fila    = nueva_fila
            self.columna = nueva_columna

        return ""

    def grito_de_batalla(self) -> str:
        return "*Grito de batalla genérico*"

    # metodos abstractos
    @abstractmethod
    def usar_habilidad(self, mapa, enemigos) -> str:
        pass



# clases de jugador
class Guerrero(Jugador):

    def __init__(self, fila: int, columna: int):
        stats = Stats(max_vida=120, dano=15, defensa=8, fov=6)
        super().__init__("Guerrero", fila, columna, stats)
        self._recurso_max    = 100
        self._recurso        = 0
        self._recurso_nombre = "Furia"
        self._recurso_color  = (200, 80, 20)
        self._exp_siguiente  = 100
        self._turnos_furia   = 0

    def _ganar_furia(self, cantidad: int) -> None:
        self._recurso = min(self._recurso + cantidad, self._recurso_max)

    def recibir_dano(self, cantidad, pierce=False) -> int:
        super().recibir_dano(cantidad, pierce)
        self._ganar_furia(10)


    def atacar(self, objetivo) -> str:
        # solo gana furia si no esta activa su habilidad
        if self._turnos_furia == 0:
            self._ganar_furia(8)

        dano_base = self._stats.dano
        if self._turnos_furia > 0:
            dano_base = dano_base * 1.5
            self._turnos_furia -= 1

        dano = objetivo.recibir_dano(dano_base, self._stats.pierce)
        msg = f"{self.nombre} golpea a {objetivo.nombre} por {dano} dmg"
        if not objetivo.esta_vivo:
            self.ganar_experiencia(objetivo.experiencia)
            self.ganar_oro(objetivo.oro)
            msg += f" — {objetivo.nombre} muere!"
        return msg

    def usar_habilidad(self, mapa, enemigos) -> str:
        if self._recurso < 50:
            return "No tenés suficiente furia!"
        self._turnos_furia  = 3
        self._recurso       = 0
        return "¡FURIA ACTIVADA! Daño aumentado por 3 turnos."

    def grito_de_batalla(self) -> str:
        return "*Por el honor!*"


class Asesino(Jugador):

    def __init__(self, fila, columna):
        stats = Stats(max_vida=80, dano=20, defensa=4, fov=7, pierce=True)
        super().__init__("Asesino", fila, columna, stats)
        self._recurso_max    = 100
        self._recurso        = 100
        self._recurso_nombre = "Stamina"
        self._recurso_color  = (50, 200, 50)
        self._exp_siguiente  = 100
        self._direccion      = (0, 1)   # última dirección que se movió


    def mover(self, df, dc, mapa, enemigos) -> str:
        if df != 0 or dc != 0:
            self._direccion = (df, dc)   # guarda dirección
        return super().mover(df, dc, mapa, enemigos)

    def usar_habilidad(self, mapa, enemigos) -> str:
        if self._recurso < 30:
            return "No tenés suficiente stamina!"

        df, dc = self._direccion
        aterrizaje_fila    = self.fila    + df * 2
        aterrizaje_columna = self.columna + dc * 2

        # verifica si hay enemigo en el aterrizaje
        for enemigo in enemigos:
            if enemigo.esta_vivo and enemigo.fila == aterrizaje_fila and enemigo.columna == aterrizaje_columna:
                self._recurso -= 30
                return self.atacar(enemigo)

        if mapa.es_transitable(aterrizaje_fila, aterrizaje_columna):
            self.fila    = aterrizaje_fila
            self.columna = aterrizaje_columna
            self._recurso -= 30
            return "¡Dash!"

        return "No hay espacio para el dash."


class Mago(Jugador):

    RANGO_SPELL = 5
    COSTO_MANA  = 25

    def __init__(self, fila, columna):
        stats = Stats(max_vida=70, dano=13, defensa=2, fov=6)
        super().__init__("Mago", fila, columna, stats)
        self._recurso_max    = 100
        self._recurso        = 100
        self._recurso_nombre = "Mana"
        self._recurso_color  = (50, 100, 200)
        self._exp_siguiente  = 100


    def usar_habilidad(self, mapa, enemigos) -> str:
        if self._recurso < self.COSTO_MANA:
            return "No tenés suficiente mana!"

        # busca enemigos dentro del rango
        objetivos = [
            e for e in enemigos
            if e.esta_vivo and
            abs(e.fila - self.fila) + abs(e.columna - self.columna) <= self.RANGO_SPELL
        ]

        if not objetivos:
            return "No hay enemigos en rango."

        # apunta al más cercano
        objetivo = min(
            objetivos,
            key=lambda e: abs(e.fila - self.fila) + abs(e.columna - self.columna)
        )

        dano = self._stats.dano * 2
        objetivo.recibir_dano(dano)
        self._recurso -= self.COSTO_MANA

        msg = f"¡Spell! {self.nombre} golpea a {objetivo.nombre} por {dano} dmg"
        if not objetivo.esta_vivo:
            self.ganar_experiencia(objetivo.experiencia)
            self.ganar_oro(objetivo.oro)
            msg += f" — {objetivo.nombre} muere!"
        return msg
