import pygame

pygame.mixer.init()
som_coleta = pygame.mixer.Sound("data\\audio\\collect.wav")
som_derrota = pygame.mixer.Sound("data\\audio\\death-sound.wav")
som_inicio = pygame.mixer.Sound("data\\audio\\background.wav")
som_win = pygame.mixer.Sound("data\\audio\\win.wav")
som_loopgame = pygame.mixer.Sound("data\\audio\\loopgame.wav")