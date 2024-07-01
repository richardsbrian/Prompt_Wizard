import pygame
import time
import sys

# Initialize global variables
screen = None
width = None
height = None
background = None
all_sprites = None
clock = None


def set_tint_screen_variables(scr, w, h, bg, sprites, clk):
    global screen, width, height, background, all_sprites, clock
    screen = scr
    width = w
    height = h
    background = bg
    all_sprites = sprites
    clock = clk


def create_tint_surface(size, color, alpha):
    tint_surface = pygame.Surface(size)
    tint_surface.set_alpha(alpha)
    tint_surface.fill(color)
    return tint_surface


def apply_tint(screen, tint_surface, duration, background, all_sprites, clock):
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < duration * 50:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        screen.blit(tint_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)  # Maintain 60 FPS


def tint_screen_blue():
    light_blue_tint = create_tint_surface((width, height), (173, 216, 230), 128)
    apply_tint(screen, light_blue_tint, 3, background, all_sprites, clock)
