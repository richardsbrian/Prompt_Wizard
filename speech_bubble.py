import pygame
import globals  # Import the globals file

class SpeechBubble(pygame.sprite.Sprite):
    def __init__(self, text, font, text_color, bg_color=(255, 255, 255), border_color=(0, 0, 0), padding=10):
        super().__init__()
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.padding = padding
        self.visible = True
        self.image = self.create_image()
        self.rect = self.image.get_rect()

    def create_image(self):
        if not self.visible:
            return pygame.Surface((0, 0), pygame.SRCALPHA)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        width = text_surface.get_width() + self.padding * 2
        height = text_surface.get_height() + self.padding * 2
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.fill(self.bg_color)
        image.blit(text_surface, (self.padding, self.padding))
        pygame.draw.rect(image, self.border_color, image.get_rect(), 2)
        return image

    def set_position(self, x, y):
        self.rect.topleft = (x, y)

    def set_text(self, text):
        self.text = text
        self.image = self.create_image()
        self.rect = self.image.get_rect()

    def set_bg_color(self, color):
        self.bg_color = color
        self.image = self.create_image()
        self.rect = self.image.get_rect()

    def set_border_color(self, color):
        self.border_color = color
        self.image = self.create_image()
        self.rect = self.image.get_rect()

    def set_text_color(self, color):
        self.text_color = color
        self.image = self.create_image()
        self.rect = self.image.get_rect()

    def toggle_visibility(self):
        self.visible = not self.visible
        self.image = self.create_image()
        self.rect = self.image.get_rect()

    def update(self, *args):
        self.image = self.create_image()
        self.rect = self.image.get_rect()

    def set_position_relative_to_sprite(self):
        sprite_x, sprite_y = globals.sprite_position
    
        bubble_x = sprite_x + 150  # Adjust the offset as needed
        bubble_y = sprite_y + 20
        self.set_position(bubble_x, bubble_y)
