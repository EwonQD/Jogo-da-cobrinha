import random
import pygame
pygame.init()
from sons import som_inicio
som_inicio.play()
from constantes import *
from jogo import jogo
from tela_inicial import tela_inicial
from utils import carregar_melhores_tempos


def __init__(self):
    self.x = random.uniform(0, largura)
    self.y = random.uniform(0, altura)
    self.raio = random.randint(10, 30)
    self.cor = (
        random.randint(150, 255),
        random.randint(150, 255),
        random.randint(150, 255),
        50
    )  # cor pastel semi-transparente
    self.vel_x = random.uniform(-0.3, 0.3)
    self.vel_y = random.uniform(-0.3, 0.3)

def mover(self):
    self.x += self.vel_x
    self.y += self.vel_y
    # Rebate nas bordas
    if self.x < -self.raio:
        self.x = largura + self.raio
    elif self.x > largura + self.raio:
        self.x = -self.raio
    if self.y < -self.raio:
        self.y = altura + self.raio
    elif self.y > altura + self.raio:
        self.y = -self.raio

def desenhar(self, superficie):
    # Usar uma Surface com alpha para semi-transparência
    bolinha_surf = pygame.Surface((self.raio*2, self.raio*2), pygame.SRCALPHA)
    pygame.draw.circle(bolinha_surf, self.cor, (self.raio, self.raio), self.raio)
    superficie.blit(bolinha_surf, (self.x - self.raio, self.y - self.raio))

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