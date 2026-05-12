import pygame

class Gestor_sonido:
    def __init__(self):
        try:
            pygame.mixer.init()
            # Diccionario para organizar los efectos
            self.efectos = {
                # Jugador
                "jugador_ataque":  pygame.mixer.Sound("assets/sonidos/sword.mp3"),
                "jugador_paso":    pygame.mixer.Sound("assets/sonidos/paso.mp3"),

                # Enemigos
                "esqueleto_ataque": pygame.mixer.Sound("assets/sonidos/ataque-esqueleto.mp3"),
                "esqueleto_muerte": pygame.mixer.Sound("assets/sonidos/muerte-esqueleto.mp3"),
                "orco_ataque":      pygame.mixer.Sound("assets/sonidos/ataque-orco.mp3"),
                "orco_muerte":      pygame.mixer.Sound("assets/sonidos/muerte-orco.mp3"),

                # Sistema
                "subir_nivel":     pygame.mixer.Sound("assets/sonidos/level-up.mp3"),
            }
        except Exception as e:
            print(f"Error cargando audio: {e}")
            self.efectos = {}

    # reproduce solo si existe
    def reproducir(self, nombre, volumen=0.1):
        sonido = self.efectos.get(nombre)
        if sonido:
            sonido.set_volume(volumen)
            sonido.play()

    def musica_fondo(self, ruta, volumen=0.3):
        try:
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.set_volume(volumen)
            pygame.mixer.music.play(-1)
        except:
            pass
