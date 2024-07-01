# main.py
import pygame
from speech_bubble import SpeechBubble
from sprite import AnimatedSprite
from utils import load_image, scale_image
from input_display import display_screenshot_with_input
from screen_effect import set_tint_screen_variables
from screenshot import take_screenshot
import globals  # Import the globals module

# Initialize Pygame
pygame.init()

take_screenshot()

# Set up the display
infoObject = pygame.display.Info()
width, height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
pygame.display.set_caption("Animated Desktop Sprite")

# Load and scale the background image
background = load_image("png_files\\screenshots\\screenshot.png").convert()
background = scale_image(background, width, height)

# Create animated sprite
sprite = AnimatedSprite(
    "png_files\\wizard_things\\walking.png",
    4,
    "png_files\\wizard_things\\idle.png",
    4,
    "png_files\\wizard_things\\freeze.png",
    10,
    scale_factor=2,
    screen_width=width,
    screen_height=height,
)

globals.sprite2 = SpeechBubble(
    text="Hello, World!", 
    font=pygame.font.SysFont("Arial", 24), 
    text_color=(50, 50, 0),
    bg_color=(255, 255, 255),
    border_color=(0, 0, 0)
)

globals.sprite2.set_position(100, 100)

all_sprites = pygame.sprite.Group(sprite, globals.sprite2)

# Variables for dragging box
dragging = False
start_pos = None
end_pos = None

# Set up Pygame clock
clock = pygame.time.Clock()

set_tint_screen_variables(screen, width, height, background, all_sprites, clock)

def handle_quit_event(event):
    global running
    if event.type == pygame.QUIT or (
        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
    ):
        running = False

def handle_mouse_button_down_event(event):
    global dragging, start_pos, end_pos
    if sprite.rect.collidepoint(event.pos):
        sprite.toggle_active()
    elif globals.sprite2.rect.collidepoint(event.pos):
        globals.sprite2.toggle_visibility()  # Toggle visibility when speech bubble is clicked
    else:
        dragging = True
        start_pos = event.pos
        end_pos = event.pos

def handle_mouse_button_up_event(event):
    global dragging, start_pos, end_pos, running
    if dragging:
        dragging = False
        end_pos = event.pos
        # Calculate the region to capture based on the drag rectangle
        x = min(start_pos[0], end_pos[0])
        y = min(start_pos[1], end_pos[1])
        width = abs(end_pos[0] - start_pos[0])
        height = abs(end_pos[1] - start_pos[1])
        region = (x, y, width, height)
        take_screenshot(filename="box_screenshot.png", region=region)
        if not display_screenshot_with_input(
            "png_files\\screenshots\\box_screenshot.png"
        ):
            running = False

def handle_mouse_motion_event(event):
    global end_pos
    if dragging:
        end_pos = event.pos

def handle_events():
    for event in pygame.event.get():
        handle_quit_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_button_down_event(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            handle_mouse_button_up_event(event)
        elif event.type == pygame.MOUSEMOTION:
            handle_mouse_motion_event(event)

def update_sprites():
    mouse_pos = pygame.mouse.get_pos()
    all_sprites.update(mouse_pos)

def draw_screen():
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    if dragging and start_pos and end_pos:
        rect = pygame.Rect(
            start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
        )
        pygame.draw.rect(screen, (255, 0, 0), rect, 2)
    pygame.display.flip()

def game_loop():
    global running
    running = True
    while running:
        handle_events()
        update_sprites()
        draw_screen()
        clock.tick(60)  # 60 FPS
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    take_screenshot()
    game_loop()
