import pygame
import os
pygame.init()

# Tela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Minhoquinha do Conhecimento")

# Cores
cor_fundo = (0, 0, 0)
cor_cobra = (0, 255, 0)
cor_letra = (255, 0, 0)
cor_texto = (255, 255, 255)
cor_botao = (50, 150, 50)
cor_botao_hover = (70, 200, 70)

# Fontes
fonte = pygame.font.SysFont(None, 25)
fonte_titulo = pygame.font.SysFont(None, 40)

# Cobra
tamanho_cobra = 20

# Palavras
palavras = ["bola", "casa", "gato", "sol", "lua", "pato", "amor", "faca", "pé", "rio"]

# Arquivo de tempo
ARQUIVO_TEMPOS = os.path.join("minhoquinhaDoConhecimento", "melhores_tempos.txt")