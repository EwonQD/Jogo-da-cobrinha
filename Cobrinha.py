import pygame
import random
import time
import os

pygame.init()

# Configurações da tela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da Cobra - Letras")

# Cores
cor_fundo = (0, 0, 0)
cor_cobra = (0, 255, 0)
cor_letra = (255, 0, 0)
cor_texto = (255, 255, 255)
cor_botao = (50, 150, 50)
cor_botao_hover = (70, 200, 70)

# Fonte
fonte = pygame.font.SysFont(None, 25)
fonte_titulo = pygame.font.SysFont(None, 40)

# Tamanho cobra/letra
tamanho_cobra = 20

# Lista de palavras simples para escolher aleatoriamente
palavras = ["bola", "casa", "gato", "sol", "lua", "pato", "amor", "faca", "pé", "rio"]

ARQUIVO_TEMPOS = os.path.join("Jogo da cobrinha", "melhores_tempos.txt")

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
    # ... mantém igual ao seu código original ...
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

def jogo():
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

def desenhar_botao(texto, retangulo, mouse_pos):
    cor = cor_botao_hover if retangulo.collidepoint(mouse_pos) else cor_botao
    pygame.draw.rect(tela, cor, retangulo)
    texto_img = fonte_titulo.render(texto, True, cor_texto)
    texto_rect = texto_img.get_rect(center=retangulo.center)
    tela.blit(texto_img, texto_rect)

def tela_inicial(ultimo_tempo, melhores_tempos):
    rodando = True
    botao_inicio = pygame.Rect(largura//2 - 100, altura//2, 200, 50)

    while rodando:
        tela.fill(cor_fundo)
        mouse_pos = pygame.mouse.get_pos()

        titulo = fonte_titulo.render("Jogo da Cobra - Letras", True, cor_texto)
        tela.blit(titulo, (largura//2 - titulo.get_width()//2, altura//4))

        # Exibir último tempo
        if ultimo_tempo is not None:
            ult_temp_str = f"Último tempo: {int(ultimo_tempo//60):02d}:{int(ultimo_tempo%60):02d}"
            texto_ultimo = fonte.render(ult_temp_str, True, cor_texto)
            tela.blit(texto_ultimo, (largura//2 - texto_ultimo.get_width()//2, altura//4 + 50))

        # Exibir 5 melhores tempos
        y_inicio = altura//2 + 100
        titulo_best = fonte.render("5 Melhores tempos:", True, cor_texto)
        tela.blit(titulo_best, (largura//2 - titulo_best.get_width()//2, y_inicio))

        for i, t in enumerate(melhores_tempos):
            t_str = f"{i+1}. {int(t//60):02d}:{int(t%60):02d}"
            texto_tempo = fonte.render(t_str, True, cor_texto)
            tela.blit(texto_tempo, (largura//2 - texto_tempo.get_width()//2, y_inicio + 30 * (i+1)))

        desenhar_botao("Iniciar", botao_inicio, mouse_pos)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_inicio.collidepoint(mouse_pos):
                    return True

        pygame.display.update()

def main():
    ultimo_tempo = None
    rodando = True
    while rodando:
        melhores_tempos = carregar_melhores_tempos()
        iniciar_jogo = tela_inicial(ultimo_tempo, melhores_tempos)
        if not iniciar_jogo:
            break
        rodando, ultimo_tempo = jogo()
    pygame.quit()

if __name__ == "__main__":
    main()