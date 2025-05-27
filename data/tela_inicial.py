import pygame
from .constantes import *
from .jogo import *
from .sons import som_inicio

fonte = pygame.font.SysFont(None, 25)

imagem_fundo = pygame.image.load("data\\visual\\inicio.png").convert()
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))
def desenhar_botao(texto, retangulo, mouse_pos):
    cor = cor_botao_hover if retangulo.collidepoint(mouse_pos) else cor_botao
    pygame.draw.rect(tela, cor, retangulo)
    texto_img = fonte_titulo.render(texto, True, cor_texto)
    texto_rect = texto_img.get_rect(center=retangulo.center)

    tela.blit(texto_img, texto_rect)





def tela_inicial(ultimo_tempo, melhores_tempos):    
    rodando = True
    botao_inicio = pygame.Rect(largura//2 - 100, altura//2, 200, 50)

    # Garante que a música será reiniciada corretamente
    som_inicio.stop()
    som_inicio.set_volume(0.8)
    som_inicio.play(-1)  # -1 para repetir em loop
    while rodando:        
        tela.blit(imagem_fundo, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        titulo = fonte_titulo.render("Minhoquinha do Conhecimento", True, cor_texto)
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
                    som_inicio.stop()
                    return True

        pygame.display.update()