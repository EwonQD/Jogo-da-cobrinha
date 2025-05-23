import pygame
import random
import time
from utils import *

def jogo():
    pygame.init()
    palavra = random.choice(palavras)
    indice_letra = 0
    letra_correta = palavra[indice_letra]
    letras_coletadas = ""

    cobra_x = largura // 2.1
    cobra_y = altura // -20
    cobra_dx = 0
    cobra_dy = 0

    corpo_cobra = [pygame.Rect(cobra_x, cobra_y, tamanho_cobra, tamanho_cobra)]

    letras_visiveis = gerar_letras_completas(palavra)

    venceu = False
    perdeu = False

    crescer = 0
    crescimento_por_letra = 2

    clock = pygame.time.Clock()
    jogo_em_execucao = True

    # INICIO CRONÔMETRO
    tempo_inicio = time.time()

    while jogo_em_execucao:
        clock.tick(7)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False, None
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and cobra_dx == 0:
                    cobra_dx = -tamanho_cobra
                    cobra_dy = 0
                elif evento.key == pygame.K_RIGHT and cobra_dx == 0:
                    cobra_dx = tamanho_cobra
                    cobra_dy = 0
                elif evento.key == pygame.K_UP and cobra_dy == 0:
                    cobra_dx = 0
                    cobra_dy = -tamanho_cobra
                elif evento.key == pygame.K_DOWN and cobra_dy == 0:
                    cobra_dx = 0
                    cobra_dy = tamanho_cobra

        cobra_x = (cobra_x + cobra_dx) % largura
        cobra_y = (cobra_y + cobra_dy) % altura
        cabeca = pygame.Rect(cobra_x, cobra_y, tamanho_cobra, tamanho_cobra)
        corpo_cobra.insert(0, cabeca)

        letra_comida = None
        indice_letra_comida = None
        for i, (letra, pos) in enumerate(letras_visiveis):
            letra_rect = pygame.Rect(pos[0], pos[1], tamanho_cobra, tamanho_cobra)
            if cabeca.colliderect(letra_rect):
                letra_comida = letra
                indice_letra_comida = i
                break

        if letra_comida:
            if letra_comida == letra_correta:
                letras_coletadas += letra_comida
                indice_letra += 1
                letras_visiveis.pop(indice_letra_comida)
                crescer += crescimento_por_letra
                if indice_letra == len(palavra):
                    venceu = True
                    jogo_em_execucao = False
                else:
                    letra_correta = palavra[indice_letra]
            else:
                perdeu = True
                jogo_em_execucao = False
        else:
            if crescer > 0:
                crescer -= 1
            else:
                corpo_cobra.pop()

        if cabeca.collidelist(corpo_cobra[1:]) != -1:
            perdeu = True
            jogo_em_execucao = False

        # Tempo decorrido atual para exibir na tela
        tempo_decorrido = time.time() - tempo_inicio
        tempo_formatado = f"{int(tempo_decorrido // 60):02d}:{int(tempo_decorrido % 60):02d}"

        tela.fill(cor_fundo)

        for segmento in corpo_cobra:
            pygame.draw.rect(tela, cor_cobra, segmento)

        for letra, pos in letras_visiveis:
            pygame.draw.rect(tela, cor_letra, (pos[0], pos[1], tamanho_cobra, tamanho_cobra))
            img_letra = fonte.render(letra.upper(), True, cor_texto)
            tela.blit(img_letra, (pos[0] + 5, pos[1] + 2))

        # Exibe o cronômetro em vez da pontuação
        texto_tempo = fonte.render(f"Tempo: {tempo_formatado}", True, cor_texto)
        tela.blit(texto_tempo, (10, 10))

        texto_coletadas = fonte.render(f"Letras coletadas: {letras_coletadas.upper()}", True, cor_texto)
        tela.blit(texto_coletadas, (10, 50))

        texto_palavra = fonte.render(f"Monte a palavra: {palavra.upper()}", True, cor_texto)
        tela.blit(texto_palavra, (10, 90))

        pygame.display.update()

    tempo_final = time.time() - tempo_inicio

    if venceu:
        salvar_tempo(tempo_final)
        mostrar_mensagem(f"Você venceu! Tempo: {int(tempo_final//60):02d}:{int(tempo_final%60):02d}", (0, 255, 0))
    elif perdeu:
        mostrar_mensagem("Você perdeu! Tente novamente.", (255, 0, 0))

    return True, tempo_final