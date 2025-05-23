import pygame
pygame.init()
from jogo import jogo
from tela_inicial import tela_inicial
from utils import carregar_melhores_tempos

def main():
    rodando = True
    ultimo_tempo = None
    while rodando:
        melhores_tempos = carregar_melhores_tempos()
        iniciar = tela_inicial(ultimo_tempo, melhores_tempos)
        if not iniciar:
            rodando = False
        else:
            continuar, tempo = jogo()
            if continuar:
                ultimo_tempo = tempo
            else:
                rodando = False

if __name__ == "__main__":
    main()
