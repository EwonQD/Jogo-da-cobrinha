import pygame
import random
import time
from .utils import *
from .sons import *

fonte = pygame.font.SysFont(None, 25)

imagem_sala = pygame.image.load("data\\visual\\sala.png").convert()
imagem_sala = pygame.transform.scale(imagem_sala, (largura, altura))

def desenhar_cobra_lisa(tela, corpo_cobra, cor_cobra_base, tamanho_cobra):
    raio_cabeca = int(tamanho_cobra * 0.6)  # cabeça maior
    raio_corpo = int(tamanho_cobra * 0.5)   # corpo menor que a cabeça
    raio_calda = int(tamanho_cobra * 0.3)   # calda menor que o corpo

    # Desenha linhas do corpo da cobra (opcional, mantém linhas lisas)
    if len(corpo_cobra) > 1:
        pontos = [segmento.center for segmento in corpo_cobra]

        grupos = []
        grupo_atual = [pontos[0]]

        for i in range(1, len(pontos)):
            x1, y1 = pontos[i-1]
            x2, y2 = pontos[i]

            dx = abs(x2 - x1)
            dy = abs(y2 - y1)

            if dx > largura / 2 or dy > altura / 2:
                grupos.append(grupo_atual)
                grupo_atual = [pontos[i]]
            else:
                grupo_atual.append(pontos[i])
        grupos.append(grupo_atual)

        for grupo in grupos:
            if len(grupo) > 1:
                pygame.draw.lines(tela, cor_cobra_base, False, grupo, raio_corpo*2)

    # Cores para os segmentos do corpo (gradiente simples)
    cores_gradiente = [
        (255, 0, 0),    # vermelho
        (255, 127, 0),  # laranja
        (255, 255, 0),  # amarelo
        (0, 255, 0),    # verde
        (0, 0, 255),    # azul
        (75, 0, 130),   # anil
        (148, 0, 211)   # violeta
    ]

    # Desenha cabeça com cor fixa (pode ser cor_cobra_base)
    pygame.draw.circle(tela, cor_cobra_base, corpo_cobra[0].center, raio_cabeca)

    # Desenha olhinhos (mesmo do seu código)
    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)

    cx, cy = corpo_cobra[0].center
    olho_raio = max(2, int(tamanho_cobra * 0.15))

    olho1_pos = (cx - olho_raio * 2, cy - olho_raio)
    olho2_pos = (cx + olho_raio * 2, cy - olho_raio)

    pygame.draw.circle(tela, BRANCO, olho1_pos, olho_raio)
    pygame.draw.circle(tela, BRANCO, olho2_pos, olho_raio)

    pygame.draw.circle(tela, PRETO, olho1_pos, max(1, olho_raio // 2))
    pygame.draw.circle(tela, PRETO, olho2_pos, max(1, olho_raio // 2))

    # Desenha segmentos do corpo (exceto cabeça e calda) com cores variáveis
    for idx, segmento in enumerate(corpo_cobra[1:-1]):
        cor_idx = idx % len(cores_gradiente)  # repete as cores ciclicamente
        cor_segmento = cores_gradiente[cor_idx]
        pygame.draw.circle(tela, cor_segmento, segmento.center, raio_corpo)

    # Desenha calda com cor fixa (pode usar uma cor do gradiente ou a base)
    if len(corpo_cobra) > 1:
        pygame.draw.circle(tela, cor_cobra_base, corpo_cobra[-1].center, raio_calda)

def jogo():
    fonte = pygame.font.SysFont(None, 25)
    palavra = random.choice(palavras)
    indice_letra = 0
    letra_correta = palavra[indice_letra]
    letras_coletadas = ""

    cobra_x = largura // 2
    cobra_y = altura - tamanho_cobra * 2  # Posiciona a cobra um pouco acima do rodapé da tela

    cobra_dx = 0  # Parada no início
    cobra_dy = 0

    # Cabeça da cobra
    cabeca = pygame.Rect(cobra_x, cobra_y, tamanho_cobra, tamanho_cobra)

    # Calda à esquerda da cabeça
    calda = pygame.Rect(cobra_x - tamanho_cobra, cobra_y, tamanho_cobra, tamanho_cobra)

    # Corpo inicial com cabeça e calda
    corpo_cobra = [cabeca, calda]


    # Começa com cabeça e calda
    corpo_cobra = [cabeca, calda]


    letras_visiveis = gerar_letras_completas(palavra)

    venceu = False
    perdeu = False

    crescer = 0
    crescimento_por_letra = 2

    clock = pygame.time.Clock()
    jogo_em_execucao = True
    som_loopgame.play(-1) # O -1 reproduz o audio em loop

    # INICIO CRONÔMETRO
    tempo_inicio = time.time()

    while jogo_em_execucao:
        clock.tick(5)

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
                som_coleta.play()
                som_coleta.set_volume(1.9)
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
                som_derrota.play()
                perdeu = True
                jogo_em_execucao = False
        else:
            if crescer > 0:
                crescer -= 1
            else:
                corpo_cobra.pop()

        # Só verifica colisão se a cobra já estiver em movimento
        if (cobra_dx != 0 or cobra_dy != 0) and cabeca.collidelist(corpo_cobra[1:]) != -1:
            som_derrota.play()
            perdeu = True
            jogo_em_execucao = False

        # Tempo decorrido atual para exibir na tela
        tempo_decorrido = time.time() - tempo_inicio
        tempo_formatado = f"{int(tempo_decorrido // 60):02d}:{int(tempo_decorrido % 60):02d}"

        tela.blit(imagem_sala, (0, 0))

        desenhar_cobra_lisa(tela, corpo_cobra, cor_cobra, tamanho_cobra)

        # Cores suaves para os quadrados (ciclo)
        cores_alimentos = [
            (255, 182, 193),  # rosa claro
            (176, 224, 230),  # azul claro
            (144, 238, 144),  # verde claro
            (255, 255, 224),  # amarelo claro
            (221, 160, 221),  # roxo claro
            (255, 228, 196),  # bege claro
            (240, 230, 140)   # dourado claro
        ]

        for i, (letra, pos) in enumerate(letras_visiveis):
            cor_fundo = cores_alimentos[i % len(cores_alimentos)]
            # Retângulo com cantos arredondados
            pygame.draw.rect(tela, cor_fundo, (pos[0], pos[1], tamanho_cobra, tamanho_cobra), border_radius=8)
            
            # Letra em cor escura para contraste
            img_letra = fonte.render(letra.upper(), True, (40, 40, 40))
            rect_letra = img_letra.get_rect()
            rect_letra.center = (pos[0] + tamanho_cobra // 2, pos[1] + tamanho_cobra // 2)
            tela.blit(img_letra, rect_letra)


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
        som_loopgame.stop()
        som_win.play()
        salvar_tempo(tempo_final)
        mostrar_mensagem(f"Você venceu! Tempo: {int(tempo_final//60):02d}:{int(tempo_final%60):02d}", (0, 255, 0))
        pygame.time.wait(2000)   # espera 2000 ms = 2 segundos
    elif perdeu:
        som_loopgame.stop()
        mostrar_mensagem("Você perdeu! Tente novamente.", (255, 0, 0))

    return True, tempo_final