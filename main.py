import math
import pygame
import numpy

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WORLD_WIDTH = 300
WORLD_HEIGHT = 300


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (45, 100, 245)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode(size=[SCREEN_WIDTH, SCREEN_HEIGHT])

world = {}

def initdemoworld():
    colors = [BLACK, WHITE, RED, GREEN, BLUE]
    for x in range(0, WORLD_WIDTH):
        for y in range(0, WORLD_HEIGHT):
            random_color_index = numpy.random.choice(numpy.arange(0, 5), p=[0.2, 0.15, 0.05, 0.4, 0.2])
            world[(x, y)] = {'color': colors[random_color_index]}


def world2screen(worldW, worldH):
    sx = worldW + cameraX
    sy = worldH + cameraY
    sx = math.floor(sx * zoom)
    sy = math.floor(sy * zoom)
    sw = math.floor((worldW + cameraX + 1) * zoom) - sx
    if sx < 0 or sx + sw >= SCREEN_WIDTH or sy < 0 or sy + sw >= SCREEN_HEIGHT:
        return None
    return pygame.Rect(sx, sy, sw, sw)


def drawGrid():
    for x in range(0, WORLD_WIDTH):
        for y in range(0, WORLD_HEIGHT):
            rect = world2screen(x, y)
            if rect is None:
                continue
            c = world[(x, y)]['color']
            pygame.draw.rect(screen, c, rect, 0)


game = True

initdemoworld()

cameraX = 0
cameraY = 0
sceneW = 80
sceneH = 60
zoom = 1.0

while game:
    screen.fill((255, 255, 255))

    # Create the map
    drawGrid()

    for event in pygame.event.get():
        #if event.type != pygame.MOUSEMOTION:
        #    print(event.type)
       # print(pygame.mouse.get_pressed()[0])
        #for i in world:
        #    print(i)
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                if cameraY >= 5:
                    cameraY -= 5
            elif keys[pygame.K_DOWN]:
                if cameraY + sceneH < WORLD_HEIGHT:
                    cameraY += 5
            elif keys[pygame.K_LEFT]:
                if cameraX >= 5:
                    cameraX -= 5
            elif keys[pygame.K_RIGHT]:
                if cameraX + sceneW < WORLD_WIDTH:
                    cameraX += 5
            elif keys[pygame.K_z]:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    zoom = math.floor(zoom * 2)
                    print(zoom, 'novel')
                else:
                    zoom = max(1, math.floor(zoom / 2))
                    print(zoom, 'csokkent')
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
    pygame.display.flip()
pygame.quit()
