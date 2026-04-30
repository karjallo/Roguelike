import pygame
from ui.constantes import NEGRO, GRIS, BLANC, ROJO, VERDE, AMARIL

#  Menú de selección
class Menu:

    def __init__(self, pantalla):
        self.pantalla      = pantalla
        self.fuente_titulo = pygame.font.SysFont("monospace", 28, bold=True)
        self.fuente_opcion = pygame.font.SysFont("monospace", 18)

    def seleccion_clase(self) -> str:
        opciones = [
            ("1", "Guerrero", "Tanque resistente. Furia aumenta con el combate."),
            ("2", "Asesino",  "Veloz y letal. Dash para reposicionarse."),
            ("3", "Mago",     "Frágil pero poderoso. Spells a distancia."),
        ]

        while True:
            self.pantalla.fill(NEGRO)
            titulo = self.fuente_titulo.render("Elegí tu clase", True, AMARIL)
            self.pantalla.blit(titulo, (50, 60))

            for i, (tecla, nombre, descripcion) in enumerate(opciones):
                y = 160 + i * 100
                pygame.draw.rect(self.pantalla, GRIS,   (50, y, 700, 70))
                pygame.draw.rect(self.pantalla, AMARIL, (50, y, 700, 70), 1)
                self.pantalla.blit(
                    self.fuente_opcion.render(f"[{tecla}]  {nombre}", True, AMARIL), (70, y + 10))
                self.pantalla.blit(
                    self.fuente_opcion.render(f"     {descripcion}", True, BLANC),   (70, y + 38))

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_1: return "guerrero"
                    if evento.key == pygame.K_2: return "asesino"
                    if evento.key == pygame.K_3: return "mago"

    def pantalla_game_over(self, jugador) -> bool:
        """Muestra game over. Devuelve True si quiere jugar de nuevo, False si sale."""
        fuente_titulo = pygame.font.SysFont("monospace", 36, bold=True)
        fuente_opcion = pygame.font.SysFont("monospace", 18)
        fuente_stats  = pygame.font.SysFont("monospace", 14)

        ROJO   = (200, 50,  50)
        AMARIL = (200, 200, 50)
        BLANC  = (200, 200, 200)
        GRIS   = (50,  50,  50)
        NEGRO  = (0,   0,   0)

        while True:
            self.pantalla.fill(NEGRO)

            # titulo
            titulo = fuente_titulo.render("HAS MUERTO", True, ROJO)
            self.pantalla.blit(titulo, (ANCHO_VENTANA // 2 - titulo.get_width() // 2, 80))

            # stats finales
            stats = [
                f"Clase     : {jugador.nombre}",
                f"Nivel     : {jugador.nivel}",
                f"Oro       : {jugador.oro}",
                f"Experiencia: {jugador.experiencia}",
            ]
            y = 180
            for linea in stats:
                sup = fuente_stats.render(linea, True, BLANC)
                self.pantalla.blit(sup, (ANCHO_VENTANA // 2 - sup.get_width() // 2, y))
                y += 24

            # opciones
            opciones = [
                ("R", "Jugar de nuevo"),
                ("Q", "Salir"),
            ]
            y = 340
            for tecla, texto in opciones:
                pygame.draw.rect(self.pantalla, GRIS,
                                 (ANCHO_VENTANA // 2 - 150, y, 300, 50))
                pygame.draw.rect(self.pantalla, AMARIL,
                                 (ANCHO_VENTANA // 2 - 150, y, 300, 50), 1)
                sup = fuente_opcion.render(f"[{tecla}]  {texto}", True, AMARIL)
                self.pantalla.blit(sup, (ANCHO_VENTANA // 2 - sup.get_width() // 2, y + 14))
                y += 70

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r: return True
                    if evento.key == pygame.K_q: return False
