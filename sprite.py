import pygame
import math
from utils import load_image, scale_image

# Animated Sprite class
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, frames_count, scale_factor=2, screen_width=800, screen_height=600):
        super().__init__()
        self.sprite_sheet = load_image(sprite_sheet_path).convert_alpha()
        self.scale_factor = scale_factor
        self.frames = self.get_frames(frames_count)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed = 3
        self.animation_speed = 5
        self.animation_counter = 0
        self.facing_right = True
        self.active = True

    def get_frames(self, frames_count):
        frame_width = self.sprite_sheet.get_width() // frames_count
        frame_height = self.sprite_sheet.get_height()
        scaled_width = int(frame_width * self.scale_factor)
        scaled_height = int(frame_height * self.scale_factor)
        frames = []
        for i in range(frames_count):
            frame = self.sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame = scale_image(frame, scaled_width, scaled_height)
            frames.append(frame)
        return frames

    def flip_frames(self, frames):
        return [pygame.transform.flip(frame, True, False) for frame in frames]

    def update(self, mouse_pos):
        if not self.active:
            return

        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 5:
            dx = (dx / distance) * self.speed
            dy = (dy / distance) * self.speed
            self.rect.x += dx
            self.rect.y += dy

            if dx < 0 and self.facing_right:
                self.frames = self.flip_frames(self.frames)
                self.facing_right = False
            elif dx > 0 and not self.facing_right:
                self.frames = self.flip_frames(self.frames)
                self.facing_right = True

        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.animation_counter = 0

    def toggle_active(self):
        self.active = not self.active
