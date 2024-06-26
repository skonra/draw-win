import math
import pygame
from pygame.locals import *
import numpy

pygame.init()

screen_width = 800
screen_height = 600

WORLD_WIDTH = 300
WORLD_HEIGHT = 300


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (45, 100, 245)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)

world0 = {}
world1 = {}
world = world0
world_next = world1
tick_count = 0


def initdemoworld():
    colors = [BLACK, WHITE, RED, GREEN, BLUE]
    for x in range(0, WORLD_WIDTH):
        for y in range(0, WORLD_HEIGHT):
            # Generate random color with custom possibilities
           #random_color_index = numpy.random.choice(numpy.arange(0, 5), p=[0.2, 0.15, 0.05, 0.4, 0.2])
            world[(x, y)] = {'color': colors[1]}


def world2screen(worldX, worldY):
    sx = worldX + cameraX
    sy = worldY + cameraY
    sx = math.floor(sx * zoom)
    sy = math.floor(sy * zoom)
    sw = math.floor((worldX + cameraX + 1) * zoom) - sx # width of sides in px
    if sx < 0 or sx >= screen_width or sy < 0 or sy >= screen_height:
        return None
    return pygame.Rect(sx, sy, sw, sw)


def screen2world(mouseX, mouseY):
    worldX = math.floor(mouseX / zoom) - cameraX
    worldY = math.floor(mouseY / zoom) - cameraY
    return worldX, worldY


def drawGrid():
    for x in range(0, WORLD_WIDTH):
        for y in range(0, WORLD_HEIGHT):
            rect = world2screen(x, y)
            if rect is None:
                continue
            c = world[(x, y)]['color']
            pygame.draw.rect(screen, c, rect, 0)


def recalculateWorld():
    if tick_count % 2 == 1:
        world = world0
        world_next = world1
    else:
        world = world1
        world_next = world0
    for x in range(0, WORLD_WIDTH):
        for y in range(0, WORLD_HEIGHT):
            neighbours = [(x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y), (x-1, y-1)]
            try:
                world[x, y]['neighbours'] = neighbours
            except:
                continue

def loop():
    for cell in world:
        filled_neighbours_num = 0
        cellx = cell[0]
        celly = cell[1]
        try:
            for neighbour in world[(cellx, celly)]['neighbours']:
                neighbourx = neighbour[0]
                neighboury = neighbour[1]
                if world[(neighbourx, neighboury)]['color'] == BLACK:
                    filled_neighbours_num += 1
            if filled_neighbours_num < 2 and world[(cellx, celly)]['color'] == BLACK:
                world[(cellx, celly)]['color'] = WHITE
            if (filled_neighbours_num == 2 or filled_neighbours_num == 3) and world[(cellx, celly)]['color'] == BLACK:
                continue
            if filled_neighbours_num > 3 and world[(cellx, celly)]['color'] == BLACK:
                world[(cellx, celly)]['color'] = WHITE
            if world[(cellx, celly)]['color'] == WHITE and filled_neighbours_num == 3:
                world[(cellx, celly)]['color'] = BLACK
        except:
            continue
game = True
postgame = False
initdemoworld()

cameraX = 0
cameraY = 0
sceneW = 80
sceneH = 60
zoom = 1.0

filled_squares = []

while game:
    screen.fill((255, 255, 255))

    if postgame:
        loop()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            screenx, screeny = screen2world(event.dict['pos'][0], event.dict['pos'][1])
            # Recolor the clicked cell to black if its within the map boundaries
            try:
                world[(screenx, screeny)]['color'] = BLACK
                filled_squares.append((screenx, screeny))
            except KeyError:
                continue
        elif event.type == pygame.KEYDOWN:
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
            elif keys[pygame.K_RETURN]:
                postgame = True
        elif event.type == VIDEORESIZE:
            screen_width, screen_height = event.dict['size']
    tick_count += 1
    recalculateWorld()
    drawGrid()
    pygame.display.flip()
pygame.quit()
