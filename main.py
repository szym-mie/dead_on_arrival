from math import ceil, floor

import pygame
from src.entity.player import Player
from src.frame.frame import Frame
from src.level.level import Level
from src.level.level_import import LevelImport

WIDTH, HEIGHT = 1280 , 720
TITLE ="TEST MOTION"


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
frame = Frame(None, None,None, None,None)
player = Player(frame)
player.position.x = 3
player.position.y = 3
background = pygame.transform.scale(pygame.image.load('res/tex/src/backgrounds/background_01.xcf').convert(), (WIDTH, HEIGHT))
# with open('res/lvl/lvl1.json', 'r') as f:
#     level = Level(LevelImport.from_json(f.read()))

level_pa = pygame.PixelArray(pygame.image.load("res/lvl/lvl1.bmp"))

xs, ys = level_pa.shape
pix = []

for j in range(ys):
    for i in range(xs):
        pix.append(level_pa[i, j])

level = Level(LevelImport.from_bitmap(24, 24, pix, []))

# print(level.chunks[0].tiles.array)

while True:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background, (0, 0))

    level.draw(screen, -player.position[0] * 32 + 640, -player.position[1] * 32 + 360)

    screen.blit(player.image, player.rect)
    player.update(0)

    if level.get_tile_at(player.position.x, player.position.y - 0.8) == 0:  # up
        player.position.y = floor(player.position.y) + 0.8

    if level.get_tile_at(player.position.x, player.position.y + 0.8) == 0:  # down
        player.position.y = ceil(player.position.y) - 0.8

    if level.get_tile_at(player.position.x - 0.8, player.position.y) == 0:  # left
        player.position.x = floor(player.position.x) + 0.8

    if level.get_tile_at(player.position.x + 0.8, player.position.y) == 0:  # right
        player.position.x = ceil(player.position.x) - 0.8

    pygame.display.update()
    clock.tick(60)




