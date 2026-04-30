import json
import os

class Mapa:

    def __init__(self):
        self.nivel_actual   = 1
        self.datos          = None
        self.grilla         = []
        self.spawn_jugador  = None
        self.spawn_enemigos = []
        self.spawn_boss     = None
        self.escalera       = None

        self.cargar_nivel(self.nivel_actual)

    # carga
    def cargar_nivel(self, numero: int) -> None:
        ruta = self._ruta_nivel(numero)

        if not os.path.exists(ruta):
            raise FileNotFoundError(f"No existe el nivel {numero}: {ruta}")

        with open(ruta, encoding="utf-8") as archivo:
            self.datos = json.load(archivo)

        self.nivel_actual   = numero
        self.grilla         = self.datos["mapa"]
        self.spawn_jugador  = self.datos["spawn_jugador"]
        self.spawn_enemigos = self.datos.get("spawn_enemigos", [])
        self.spawn_boss     = self.datos.get("spawn_boss")
        self.escalera       = self.datos.get("escalera")

        print(f"[Mapa] Nivel {numero} cargado — {self.ancho()}x{self.alto()}")

    def bajar_escalera(self) -> bool:
        """Intenta cargar el siguiente nivel. Devuelve True si lo logró."""
        try:
            self.cargar_nivel(self.nivel_actual + 1)
            return True
        except FileNotFoundError:
            print("[Mapa] No hay más niveles.")
            return False

    def intentar_bajar(self, fila: int, columna: int) -> bool:
        """Devuelve True si el jugador estaba en la escalera y bajó."""
        if self.es_escalera(fila, columna):
            return self.bajar_escalera()
        return False

    # Consultas
    def es_pared(self, fila: int, columna: int) -> bool:
        return self.grilla[fila][columna] == 1

    def es_transitable(self, fila: int, columna: int) -> bool:
        if fila < 0 or columna < 0 or fila >= self.alto() or columna >= self.ancho():
            return False
        return self.grilla[fila][columna] == 0

    def es_escalera(self, fila: int, columna: int) -> bool:
        if self.escalera is None:
            return False
        return [fila, columna] == self.escalera

    def ancho(self) -> int:
        return len(self.grilla[0]) if self.grilla else 0

    def alto(self) -> int:
        return len(self.grilla)

    # interno
    @staticmethod
    def _ruta_nivel(numero: int) -> str:
        base = os.path.dirname(__file__)
        return os.path.join(base, f"nivel{numero}.json")
