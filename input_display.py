import pygame


# Initialize the input box and its colors
def initialize_input_box(screen_width, screen_height):
    input_box = pygame.Rect(screen_width // 2 - 100, screen_height - 50, 200, 32)
    color_inactive = pygame.Color("lightskyblue3")
    color_active = pygame.Color("dodgerblue2")
    return input_box, color_inactive, color_active


# Initialize the cancel button
def initialize_cancel_button():
    button_rect = pygame.Rect(0, 0, 100, 50)  # Size and position of the cancel button
    button_rect.topright = (
        pygame.display.get_surface().get_width() - 20,
        20,
    )  # Positioning it at the top right corner
    button_color = pygame.Color("red")
    return button_rect, button_color


# Handle Pygame events and update the state and text
def handle_event(event, input_box, active, text, cancel_button):
    if event.type == pygame.MOUSEBUTTONDOWN:
        # Toggle active state if the input box is clicked
        if input_box.collidepoint(event.pos):
            active = not active
        else:
            active = False

        # Check if cancel button is clicked
        if cancel_button.collidepoint(event.pos):
            return active, text, True, True

    elif event.type == pygame.KEYDOWN and active:
        # Handle key press events when input box is active
        if event.key == pygame.K_RETURN:
            print(text)
            return active, text, True, False
        elif event.key == pygame.K_BACKSPACE:
            text = text[:-1]
        else:
            text += event.unicode
    return active, text, False, False


# Render the screen, image, input box, and cancel button with the current text
def render(
    screen,
    screenshot_image,
    input_box,
    color,
    text,
    font,
    title,
    title_font,
    cancel_button,
    button_color,
):
    screen.fill((30, 30, 30))

    # Center the image
    img_rect = screenshot_image.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2)
    )
    screen.blit(screenshot_image, img_rect.topleft)

    # Render the title
    title_surface = title_font.render(title, True, pygame.Color("white"))
    title_rect = title_surface.get_rect(
        center=(screen.get_width() // 2, input_box.y - 40)
    )
    screen.blit(title_surface, title_rect.topleft)

    # Render the current text
    txt_surface = font.render(text, True, color)
    # Resize the box if the text is too long
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    input_box.x = screen.get_width() // 2 - width // 2
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 2)

    # Render the cancel button
    pygame.draw.rect(screen, button_color, cancel_button)
    button_text = font.render("Cancel", True, pygame.Color("white"))
    button_text_rect = button_text.get_rect(center=cancel_button.center)
    screen.blit(button_text, button_text_rect.topleft)

    pygame.display.flip()


# Main function to display the screenshot with an input box and cancel button
def display_screenshot_with_input(filename):
    pygame.init()
    screen = pygame.display.set_mode(
        (0, 0), pygame.FULLSCREEN
    )  # Set the screen to full screen
    pygame.display.set_caption("Screenshot with Input Box")
    screenshot_image = pygame.image.load(filename)
    input_box, color_inactive, color_active = initialize_input_box(
        screen.get_width(), screen.get_height()
    )
    cancel_button, button_color = initialize_cancel_button()
    color = color_inactive
    active = False
    text = ""
    font = pygame.font.Font(None, 32)
    title_font = pygame.font.Font(None, 48)  # Define the font for the title
    title = "Enter your prompt below:"  # Define the title text
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            active, text, finished, cancelled = handle_event(
                event, input_box, active, text, cancel_button
            )
            if finished:
                return True
            if cancelled:
                return False
            # Update the color based on active state
            color = color_active if active else color_inactive

        render(
            screen,
            screenshot_image,
            input_box,
            color,
            text,
            font,
            title,
            title_font,
            cancel_button,
            button_color,
        )
        clock.tick(30)
