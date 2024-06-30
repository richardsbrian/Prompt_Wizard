import pygame

#hello

# Initialize the input box and its colors
def initialize_input_box():
    input_box = pygame.Rect(100, 300, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    return input_box, color_inactive, color_active

# Handle Pygame events and update the state and text
def handle_event(event, input_box, active, text):
    if event.type == pygame.MOUSEBUTTONDOWN:
        # Toggle active state if the input box is clicked
        if input_box.collidepoint(event.pos):
            active = not active
        else:
            active = False
    elif event.type == pygame.KEYDOWN and active:
        # Handle key press events when input box is active
        if event.key == pygame.K_RETURN:
            print(text)
            return active, text, True
        elif event.key == pygame.K_BACKSPACE:
            text = text[:-1]
        else:
            text += event.unicode
    return active, text, False

# Render the screen, image, and input box with the current text
def render(screen, screenshot_image, input_box, color, text, font):
    screen.fill((30, 30, 30))
    screen.blit(screenshot_image, (50, 50))

    # Render the current text
    txt_surface = font.render(text, True, color)
    # Resize the box if the text is too long
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 2)

    pygame.display.flip()

# Main function to display the screenshot with an input box
def display_screenshot_with_input(filename):
    screen = pygame.display.get_surface()
    screenshot_image = pygame.image.load(filename)
    input_box, color_inactive, color_active = initialize_input_box()
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            active, text, finished = handle_event(event, input_box, active, text)
            if finished:
                return True
            # Update the color based on active state
            color = color_active if active else color_inactive

        render(screen, screenshot_image, input_box, color, text, font)
        clock.tick(30)
