from abc import abstractmethod, ABC
from motor.juego import Juego

def Entidad(ABC):
    # clase abstracta
    def __init__(self)
    def caminar():
        pass
    def atacar():
        pass

    # debe diferenciarse en enemigo y jugador
    # porque jugador se mueve por turno, y enemigos solo
    # si jugador ingresa a su FOV
    @abstractmethod
    def actualizar():
        pass

    pass

def Enemigo(Entidad):
    # clase abstracta para usar de plantilla
    pass

def Esqueleto_guerrero(Enemigo):
    # clase de enemigo esqueleto
    pass

def Serpiente(Enemigo):
    # clase de enemigo serpiente
    pass

def Esqueleto_arquero(Enemigo):
    # clase de enemigo arquero
    pass

def Dragon(Enemigo):
    # clase de enemigo dragon
    pass

def Jugador(Entidad):
    # clase abstraacta de plantilla para jugador
    pass

def Arquero(Jugador):
    # clase arquero para jugador
    pass

def Guerrero(Jugador):
    # clase guerrero para jugador
    pass

def Asesino(Jugador):
    # clase asesino para jugador
    pass

def Juego():
    # logica del juego
    pass

def Terreno():
    # clase para el terreno de juego
    pass

def Consumibles(ABC):
    # clase abstracta para la creacion de consumibles
    pass

def Pocimas(Consumibles):
    # clase para consumibles pocimas
    pass

def Comidas(Consumibles):
    # clase para consumibles comida
    pass




def main():
    mi_juego = Juego()
    mi_juego.ejecutar()


if __name__ == "main":
    main()
