from random import randint


class Combate:
    """
    Centraliza toda la resolución de combate.
    Recibe atacante y objetivo, calcula qué pasó, y retorna un diccionario de resultado.
    No sabe nada de UI ni de sonido; solo produce datos.
    """

    PROB_CRITICO_PIERCE = 15   # % con pierce activo
    PROB_CRITICO_NORMAL = 10   # % sin pierce
    MULTIPLICADOR_CRITICO = 1.5

    @staticmethod
    def ejecutar_ataque(atacante, objetivo, dano,
                        es_jugador=False, critico=10, pierce=False) -> dict:

        # variacion de ataque
        dano_base = dano + randint(-1, 1)
        es_critico = False

        # crítico solo para jugador
        if es_jugador and randint(0, 100) < critico:
            dano_base = int(dano_base * Combate.MULTIPLICADOR_CRITICO)
            es_critico = True

        # Aplicar daño al objetivo
        dano_real = objetivo.recibir_dano(dano_base, pierce)

        # Consecuencias de la muerte
        muerto = not objetivo.esta_vivo
        level_up = False
        oro = 0
        exp = 0

        if muerto and es_jugador:
            exp = objetivo.experiencia
            oro = objetivo.oro
            atacante.ganar_oro(oro)
            level_up = atacante.ganar_experiencia(exp)

        return {
            "tipo":      "ataque",
            "atacante":  atacante,
            "objetivo":  objetivo,
            "dano":      dano_real,
            "critico":   es_critico,
            "muerto":    muerto,
            "level_up":  level_up,
            "oro":       oro,
            "exp":       exp,
        }
