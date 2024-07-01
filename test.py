import pygame
import math
from utils import load_image, scale_image
from screen_effect import tint_screen_blue
from speech_bubble import SpeechBubble

# AnimatedSprite class
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
        font=None,
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
        self.font = font if font else pygame.font.Font(None, 24)
        self.speech_bubble = None

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

                if self.current_frame >= len(self.freeze_frames):
                    self.is_freezing = False
                    self.current_frame = 0
                    self.image = self.idle_frames[self.current_frame]
                    self.show_speech_bubble("Hello, World!")  # Example text
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

        # Update speech bubble position
        if self.speech_bubble:
            self.speech_bubble.rect.midbottom = self.rect.midtop

    def toggle_active(self):
        self.active = not self.active

    def show_speech_bubble(self, text):
        self.speech_bubble = SpeechBubble(text, self.font, (50, 50, 0))
        self.speech_bubble.set_position(self.rect.centerx, self.rect.top - self.speech_bubble.rect.height)

    def hide_speech_bubble(self):
        self.speech_bubble = None

# Main game loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    animated_sprite = AnimatedSprite(
    "png_files\\wizard_things\\walking.png",
    4,
    "png_files\\wizard_things\\idle.png",
    4,
    "png_files\\wizard_things\\freeze.png",
    10,
    )
    all_sprites = pygame.sprite.Group(animated_sprite)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                animated_sprite.toggle_active()

        mouse_pos = pygame.mouse.get_pos()
        all_sprites.update(mouse_pos)

        screen.fill((255, 255, 255))
        all_sprites.draw(screen)

        if animated_sprite.speech_bubble:
            screen.blit(animated_sprite.speech_bubble.image, animated_sprite.speech_bubble.rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
