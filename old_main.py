import pygame
import sys
import math
import pyautogui
from pygame.locals import *

# Initialize Pygame
pygame.init()

def take_screenshot(filename='screenshot.png', region=None):
    try:
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        print(f"Screenshot saved as {filename}")
    except Exception as e:
        print(f"Error taking screenshot: {e}")

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

# Screenshot
take_screenshot()

# Set up the display
infoObject = pygame.display.Info()
width, height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
pygame.display.set_caption("Animated Desktop Sprite")

# Load and scale the background image
background = load_image('screenshot.png').convert()
background = scale_image(background, width, height)

# Animated Sprite class
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, frames_count, scale_factor=2):
        super().__init__()
        self.sprite_sheet = load_image(sprite_sheet_path).convert_alpha()
        self.scale_factor = scale_factor
        self.frames = self.get_frames(frames_count)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)
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

# Create animated sprite with a larger scale factor
sprite = AnimatedSprite("wizard.png", 4, scale_factor=2)  # Adjust the scale_factor as needed
all_sprites = pygame.sprite.Group(sprite)

# Variables for dragging box
dragging = False
start_pos = None
end_pos = None

# Set up Pygame clock
clock = pygame.time.Clock()

# Function to display the screenshot with a text input
def display_screenshot_with_input(filename):
    screenshot_image = pygame.image.load(filename)
    input_box = pygame.Rect(100, 300, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)  # Handle the text input (e.g., save it or use it in your game)
                        return True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        screen.blit(screenshot_image, (50, 50))

        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)


# Game loop
# Main game loop
def game_loop():
    global dragging, start_pos, end_pos
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sprite.rect.collidepoint(event.pos):
                    sprite.toggle_active()
                else:
                    dragging = True
                    start_pos = event.pos
                    end_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    dragging = False
                    end_pos = event.pos
                    # Calculate the region to capture based on the drag rectangle
                    x = min(start_pos[0], end_pos[0])
                    y = min(start_pos[1], end_pos[1])
                    width = abs(end_pos[0] - start_pos[0])
                    height = abs(end_pos[1] - start_pos[1])
                    region = (x, y, width, height)
                    take_screenshot(filename='box_screenshot.png', region=region)
                    if not display_screenshot_with_input('box_screenshot.png'):
                        running = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    end_pos = event.pos

        mouse_pos = pygame.mouse.get_pos()
        all_sprites.update(mouse_pos)

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)

        if dragging and start_pos and end_pos:
            rect = pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
            pygame.draw.rect(screen, (255, 0, 0), rect, 2)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game_loop()