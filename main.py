import curses
from motor.juego import Juego

if __name__ == "__main__":
    curses.wrapper(Juego)
