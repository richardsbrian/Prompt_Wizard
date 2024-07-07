import pygame
import sys
import keyboard
import time
import os
import win32gui
import win32con
import win32api
from speech_bubble import SpeechBubble
from sprite import AnimatedSprite
from utils import load_image, scale_image
from input_display import display_screenshot_with_input
from screen_effect import set_tint_screen_variables
from screenshot import take_screenshot
import globals  # Import the globals module

# Initialize Pygame
pygame.init()

# Set up the display
infoObject = pygame.display.Info()
width, height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
pygame.display.set_caption("Animated Desktop Sprite")

def update_background(filename="png_files/screenshots/screenshot.png"):
    global background
    try:
        background = load_image(filename).convert()
        background = scale_image(background, width, height)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Background update failed. Make sure the screenshot is saved correctly.")

# Ensure the screenshots directory exists
screenshots_dir = "png_files/screenshots"
os.makedirs(screenshots_dir, exist_ok=True)

take_screenshot("screenshot.png")
update_background()

# Create animated sprite
sprite = AnimatedSprite(
    "png_files/wizard_things/walking.png",
    4,
    "png_files/wizard_things/idle.png",
    4,
    "png_files/wizard_things/freeze.png",
    10,
    scale_factor=2,
    screen_width=width,
    screen_height=height,
)

# Update sprite position in globals
globals.sprite_position = sprite.rect.topleft

# Create the speech bubble
globals.sprite2 = SpeechBubble(
    text="Click and drag over the screen to make a selection!",
    font=pygame.font.SysFont("Arial", 24),
    text_color=(255, 255, 255),
    bg_color=(0, 0, 0),
    border_color=(0, 0, 0)
)

globals.sprite2.set_position_relative_to_sprite()

all_sprites = pygame.sprite.Group(sprite, globals.sprite2)

globals.sprite2.toggle_visibility()

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
            os.path.join(screenshots_dir, "box_screenshot.png"),
            "png_files/wizard_things/wizard_study.png",
            144,
            128,
            288,  
            256 
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
    globals.sprite_position = sprite.rect.topleft
    globals.sprite2.set_position_relative_to_sprite()

def draw_screen():
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    if dragging and start_pos and end_pos:
        rect = pygame.Rect(
            start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
        )
        pygame.draw.rect(screen, (255, 0, 0), rect, 2)
    pygame.display.flip()

def menu_screen():
    global running
    menu_running = True
    font = pygame.font.SysFont("Arial", 48)
    button_text = font.render("Start", True, (255, 255, 255))
    button_rect = button_text.get_rect(center=(width // 2, height // 2))

    # Title settings (above button)
    title_font = pygame.font.SysFont("Arial", 64)
    title_text = title_font.render("Wizard AI", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(width // 2, height // 4))

    # Subtitle settings (below button)
    subtitle_font = pygame.font.SysFont("Arial", 32)
    subtitle_text = subtitle_font.render("Press Start to Begin. Then press ---ctrl+alt+W--- to ask a question", True, (255, 255, 255))
    subtitle_rect = subtitle_text.get_rect(center=(width // 2, height // 2 + 100))

    # Box settings
    box_margin = 20
    box_rect = button_rect.inflate(box_margin, box_margin)

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                minimize_and_wait()
                menu_running = False

        screen.fill((0, 0, 0))
        
        # Draw title
        screen.blit(title_text, title_rect)

        # Draw box around button
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)
        
        # Draw button
        screen.blit(button_text, button_rect)

        # Draw subtitle
        screen.blit(subtitle_text, subtitle_rect)

        pygame.display.flip()
        pygame.time.wait(100)



def minimize_and_wait():
    global hotkey_pressed
    pygame.display.iconify()
    take_screenshot(filename="minimized_screenshot.png")
    keyboard.add_hotkey('ctrl+alt+w', on_hotkey_pressed)
    print("Waiting for hotkey...")
    while not hotkey_pressed:
        time.sleep(0.1)  # Use time.sleep to avoid high CPU usage
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    keyboard.remove_hotkey('ctrl+alt+w')
    print("Hotkey detected, taking screenshot...")
    take_screenshot(filename="hotkey_screenshot.png")
    print("Restoring window...")
    pygame.display.set_mode((width, height), pygame.NOFRAME)
    bring_to_front()
    update_background(filename=os.path.join(screenshots_dir, "hotkey_screenshot.png"))
    print("Window restored.")


def bring_to_front():
    hwnd = pygame.display.get_wm_info()['window']
    print(f"Window handle: {hwnd}")
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        win32gui.BringWindowToTop(hwnd)
    else:
        print("Error: Invalid window handle")

hotkey_pressed = False

def on_hotkey_pressed():
    global hotkey_pressed
    hotkey_pressed = True
    print("Hotkey pressed!")

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
    take_screenshot("screenshot.png")
    menu_screen()
    game_loop()
