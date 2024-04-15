import pygame
from src.entity.player import Player
from src.frame.frame import Frame
WIDTH, HEIGHT = 1280 , 720
TITLE ="TEST MOTION"


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
frame = Frame(None, None,None, None,None)
player = Player(frame)
background = pygame.transform.scale(pygame.image.load('res/tex/src/backgrounds/background_01.xcf').convert(), (WIDTH, HEIGHT))
while True:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit( background, (0, 0))
    screen.blit(player.image, player.rect)
    player.update()

    pygame.display.update()
    clock.tick(60)




