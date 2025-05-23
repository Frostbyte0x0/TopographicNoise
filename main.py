import random
import pygame
from noise import pnoise2
import numpy as np


def generate_perlin_noise_2d(shape, scale=10.0, octaves=6, persistence=0.5, lacunarity=2.0, seed=None):
    if seed is not None:
        np.random.seed(seed)
    arr = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            arr[i][j] = pnoise2(i / scale, j / scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=shape[0], repeaty=shape[1], base=seed if seed is not None else 0)
    return arr


ACCENT = (28, 50, 79)
BG = (21, 28, 46)
size = (1100, 700)
noise = generate_perlin_noise_2d(size, scale=100, lacunarity=1.3, seed=random.randint(0, 100))

pygame.init()

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Topographic noise")

done = False
drawn = False
maximum = 0.77
layers = 5
num = 1 / (2 * maximum * layers)
max_distance = 0.01
topo_values = [i * num for i in range(layers)]

topo_mode = True

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if not drawn:
        screen.fill(BG)
        for i in range(size[0]):
            for j in range(size[1]):
                if not topo_mode:
                    color = list(ACCENT)
                    mul = int(layers * (noise[i][j] + maximum)) * num
                    for z in range(len(color)):
                        color[z] = color[z] * mul
                    screen.set_at((i, j), color)
                else:
                    for value in topo_values:
                        if (value + max_distance) > abs(noise[i][j]) > (value - max_distance):
                            screen.set_at((i, j), ACCENT)
        drawn = True

    pygame.display.flip()
    clock.tick(20)

pygame.quit()
