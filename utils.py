import pygame
import sys

# Function to load an image with error handling
def load_image(path):
    try:
        image = pygame.image.load(path)
        return image
    except pygame.error as e:
        print(f"Unable to load image at {path}: {e}")
        sys.exit()

# Function to scale image
def scale_image(image, width, height):
    return pygame.transform.scale(image, (width, height))
