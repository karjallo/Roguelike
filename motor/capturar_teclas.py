import curses


class Capturar_teclas:

    # Teclas de movimiento y su delta (fila, columna)
    TECLAS_MOVIMIENTO = {
        curses.KEY_UP:    (-1,  0),
        curses.KEY_DOWN:  ( 1,  0),
        curses.KEY_LEFT:  ( 0, -1),
        curses.KEY_RIGHT: ( 0,  1),
    }

    TECLAS_MOVIMIENTO_WASD = {
        ord('w'): (-1,  0),
        ord('W'): (-1,  0),
        ord('s'): ( 1,  0),
        ord('S'): ( 1,  0),
        ord('a'): ( 0, -1),
        ord('A'): ( 0, -1),
        ord('d'): ( 0,  1),
        ord('D'): ( 0,  1),
    }

    TECLAS_SALIR = {ord('q'), ord('Q')}
    TECLAS_DISTANCIA = {ord(' ')}

    def es_salir(self, tecla: int) -> bool:
        return tecla in self.TECLAS_SALIR

    def es_ataque_distancia(self, tecla: int) -> bool:
        return tecla in self.TECLAS_DISTANCIA

    def es_movimiento(self, tecla: int) -> bool:
        return tecla in self.TECLAS_MOVIMIENTO or tecla in self.TECLAS_MOVIMIENTO_WASD

    def tecla_a_movimiento(self, tecla: int) -> tuple[int, int]:
        if tecla in self.TECLAS_MOVIMIENTO:
            return self.TECLAS_MOVIMIENTO[tecla]
        if tecla in self.TECLAS_MOVIMIENTO_WASD:
            return self.TECLAS_MOVIMIENTO_WASD[tecla]
        return (0, 0)

