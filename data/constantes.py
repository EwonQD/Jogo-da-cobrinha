import pygame
import os

# Tela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Minhoquinha do Conhecimento")

# Cores
cor_fundo = (0, 0, 0)
cor_cobra = (70, 50, 70)
cor_letra = (255, 0, 0)
cor_texto = (255, 255, 255)
cor_botao = (30, 80, 20)
cor_botao_hover = (70, 50, 70)

# Fontes
fonte = pygame.font.SysFont(None, 20)
fonte_titulo = pygame.font.SysFont(None, 40)

# Cobra
tamanho_cobra = 25

# Palavras
# Função para carregar palavras do arquivo txt
def carregar_palavras(nome_arquivo):
    palavras_carregadas = []
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                palavra = linha.strip()
                if palavra:  # evita linhas vazias
                    palavras_carregadas.append(palavra)
    except FileNotFoundError:
        print(f"Arquivo {nome_arquivo} não encontrado. Usando lista padrão.")
        # Se quiser, retorna lista padrão aqui
        return ["bola", "casa", "gato", "sol", "lua", "pato", "amor", "faca", "pé", "rio"]
    return palavras_carregadas


# Exemplo: caminho do arquivo de palavras
ARQUIVO_PALAVRAS = os.path.join("minhoquinhaDoConhecimento", "data", "palavras.txt")

# Carrega as palavras no início do seu código
palavras = carregar_palavras(ARQUIVO_PALAVRAS)


def cor_pastel():
    import random
    base = 180
    r = random.randint(base, 255)
    g = random.randint(base, 255)
    b = random.randint(base, 255)
    return (r, g, b, 100)  # alfa para semi-transparência, só se usar Surface com alpha



# Arquivo de tempo
ARQUIVO_TEMPOS = os.path.join("data", "melhores_tempos.txt")