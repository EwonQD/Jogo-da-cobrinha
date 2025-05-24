import pygame

pygame.mixer.init()
som_coleta = pygame.mixer.Sound("minhoquinhaDoConhecimento\\audio\\collect.wav")
som_derrota = pygame.mixer.Sound("minhoquinhaDoConhecimento\\audio\\death-sound.wav")
som_inicio = pygame.mixer.Sound("minhoquinhaDoConhecimento\\audio\\background.wav")
som_win = pygame.mixer.Sound("minhoquinhaDoConhecimento\\audio\\win.wav")
som_loopgame = pygame.mixer.Sound("minhoquinhaDoConhecimento\\audio\\loopgame.wav")