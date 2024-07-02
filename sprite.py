import pygame
import math

from utils import load_image, scale_image
from screen_effect import tint_screen_blue
import globals


def toggle_bubble_visibility():
    if globals.sprite2:
        globals.sprite2.toggle_visibility()


# Animated Sprite class
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        sprite_sheet_path,
        frames_count,
        idle_sprite_sheet_path,
        idle_frames_count,
        freeze_sprite_sheet_path,
        freeze_frames_count,
        scale_factor=2,
        screen_width=800,
        screen_height=600,
    ):
        super().__init__()
        self.sprite_sheet = load_image(sprite_sheet_path).convert_alpha()
        self.idle_sprite_sheet = load_image(idle_sprite_sheet_path).convert_alpha()
        self.freeze_sprite_sheet = load_image(freeze_sprite_sheet_path).convert_alpha()
        self.scale_factor = scale_factor
        self.frames = self.get_frames(frames_count, self.sprite_sheet)
        self.idle_frames = self.get_frames(idle_frames_count, self.idle_sprite_sheet)
        self.freeze_frames = self.get_frames(
            freeze_frames_count, self.freeze_sprite_sheet
        )
        self.current_frame = 0
        self.image = self.freeze_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.width // 2, screen_height - self.rect.height // 2)
        self.speed = 5
        self.moving_animation_speed = 5
        self.idle_animation_speed = 40
        self.freeze_animation_speed = 10
        self.animation_counter = 0
        self.facing_right = True
        self.active = False
        self.is_moving = False
        self.is_freezing = True  # Set is_freezing to True initially

        # Update the position in globals on initialization
        globals.update_sprite_position(self.rect.x, self.rect.y)

    def get_frames(self, frames_count, sprite_sheet):
        frame_width = sprite_sheet.get_width() // frames_count
        frame_height = sprite_sheet.get_height()
        scaled_width = int(frame_width * self.scale_factor)
        scaled_height = int(frame_height * self.scale_factor)
        frames = []
        for i in range(frames_count):
            frame = sprite_sheet.subsurface(
                (i * frame_width, 0, frame_width, frame_height)
            )
            frame = scale_image(frame, scaled_width, scaled_height)
            frames.append(frame)
        return frames

    def flip_frames(self, frames):
        return [pygame.transform.flip(frame, True, False) for frame in frames]

    def update(self, mouse_pos):
        if self.is_freezing:
            self.animation_counter += 1
            if self.animation_counter >= self.freeze_animation_speed:
                self.current_frame += 1

                # Determine the middle frame
                middle_frame = len(self.freeze_frames) // 2

                if self.current_frame == middle_frame + 2:
                    tint_screen_blue()
                    toggle_bubble_visibility()

                if self.current_frame >= len(self.freeze_frames):
                    self.is_freezing = False
                    self.current_frame = 0
                    self.image = self.idle_frames[self.current_frame]
                else:
                    self.image = self.freeze_frames[self.current_frame]

                self.animation_counter = 0
            return

        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)

        self.is_moving = self.active and distance > 5

        if self.is_moving:
            dx = (dx / distance) * self.speed
            dy = (dy / distance) * self.speed
            self.rect.x += dx
            self.rect.y += dy

            # Update the position in globals
            globals.update_sprite_position(self.rect.x, self.rect.y)

            if dx < 0 and self.facing_right:
                self.frames = self.flip_frames(self.frames)
                self.idle_frames = self.flip_frames(self.idle_frames)
                self.facing_right = False
            elif dx > 0 and not self.facing_right:
                self.frames = self.flip_frames(self.frames)
                self.idle_frames = self.flip_frames(self.idle_frames)
                self.facing_right = True

        self.animation_counter += 1
        current_animation_speed = (
            self.moving_animation_speed if self.is_moving else self.idle_animation_speed
        )
        if self.animation_counter >= current_animation_speed:
            if self.is_moving:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
            else:
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                self.image = self.idle_frames[self.current_frame]
            self.animation_counter = 0

    def toggle_active(self):
        self.active = not self.active
