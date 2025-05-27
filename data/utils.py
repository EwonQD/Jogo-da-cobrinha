import os
import pygame
import pygame
import random
import os
from .constantes import *

def carregar_melhores_tempos():
    if not os.path.exists(ARQUIVO_TEMPOS):
        return []
    with open(ARQUIVO_TEMPOS, "r") as f:
        linhas = f.readlines()
    tempos = []
    for linha in linhas:
        try:
            t = float(linha.strip())
            tempos.append(t)
        except:
            pass
    return sorted(tempos)[:5]




def salvar_tempo(novo_tempo):
    tempos = carregar_melhores_tempos()
    tempos.append(novo_tempo)
    tempos = sorted(tempos)[:5]
    with open(ARQUIVO_TEMPOS, "w") as f:
        for t in tempos:
            f.write(f"{t}\n")




def mostrar_mensagem(texto, cor):
    tela.fill(cor_fundo)
    mensagem = fonte.render(texto, True, cor)
    ret_texto = mensagem.get_rect(center=(largura//2, altura//2))
    tela.blit(mensagem, ret_texto)
    pygame.display.update()
    pygame.time.delay(2000)




def gerar_letras_completas(palavra, linhas=5, colunas=5):
    total_posicoes = linhas * colunas

    letras = list(palavra)  # todas as letras da palavra, com repetições se houver
    letras_aleatorias = []

    alfabeto = [chr(i) for i in range(97, 123)]
    letras_da_palavra = set(letras)
    letras_possiveis = [l for l in alfabeto if l not in letras_da_palavra]

    qnt_aleatorias = total_posicoes - len(letras)

    while len(letras_aleatorias) < qnt_aleatorias:
        l = random.choice(letras_possiveis)
        if letras_aleatorias.count(l) < linhas:
            letras_aleatorias.append(l)

    letras_completas = letras + letras_aleatorias
    random.shuffle(letras_completas)

    letras_pos = []
    espacamento_x = largura // (colunas + 1)
    espacamento_y = 80  # espaço vertical entre as linhas
    inicio_y = altura // 4

    i = 0
    for linha in range(linhas):
        y = inicio_y + linha * espacamento_y
        for coluna in range(colunas):
            if i >= len(letras_completas):
                break
            x = espacamento_x * (coluna + 1) - tamanho_cobra // 2
            letras_pos.append((letras_completas[i], (x, y)))
            i += 1

    return letras_pos


