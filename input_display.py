import pygame
from anthropic_api_call import send_image_and_prompt

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

# Extract the text from the response object
def extract_text_from_response(response):
    try:
        return response.content[0].text
    except Exception as e:
        print(f"Error extracting text from response: {e}")
        return "Error extracting response text"

# Handle Pygame events and update the state and text
def handle_event(event, input_box, active, text, cancel_button, scroll_offset, response_surf_rect, screen_height):
    if event.type == pygame.MOUSEBUTTONDOWN:
        # Toggle active state if the input box is clicked
        if input_box.collidepoint(event.pos):
            active = not active
        else:
            active = False

        # Check if cancel button is clicked
        if cancel_button.collidepoint(event.pos):
            return active, text, True, True, "", scroll_offset

    elif event.type == pygame.KEYDOWN and active:
        # Handle key press events when input box is active
        if event.key == pygame.K_RETURN:
            print(text)
            response = send_image_and_prompt(text)
            print("response-------", response)
            response_text = extract_text_from_response(response)
            return active, text, True, False, response_text, 0  # Reset scroll offset
        elif event.key == pygame.K_BACKSPACE:
            text = text[:-1]
        else:
            text += event.unicode

    elif event.type == pygame.MOUSEBUTTONDOWN and not active:
        if event.button == 4:  # Scroll up
            scroll_offset = max(scroll_offset - 30, 0)
        elif event.button == 5:  # Scroll down
            scroll_offset = min(scroll_offset + 30, max(0, response_surf_rect.height - screen_height + 100))

    return active, text, False, False, "", scroll_offset

# Extract frames from sprite sheet
def load_frames(sprite_sheet, frame_width, frame_height, scale_width, scale_height):
    frames = []
    sheet_width, sheet_height = sprite_sheet.get_size()
    for i in range(sheet_width // frame_width):
        frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (scale_width, scale_height))
        frames.append(frame)
    return frames

# Render the screen, image, input box, cancel button, and animated sprite with the current text
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
    response,
    scroll_offset,
    response_surf,
    response_surf_rect,
    frames,
    frame_index
):
    screen.fill((30, 30, 30))

    if response:
        # Draw the response box
        box_x = screen.get_width() // 2 - response_surf_rect.width // 2 - 20
        box_y = 100
        box_width = response_surf_rect.width + 40
        box_height = min(screen.get_height() - 200, response_surf_rect.height + 40)
        pygame.draw.rect(screen, pygame.Color("white"), (box_x, box_y, box_width, box_height), 2)

        # Render the response in a scrollable text box
        response_viewport = pygame.Rect(0, scroll_offset, response_surf_rect.width, response_surf_rect.height)
        screen.blit(response_surf, (box_x + 20, box_y + 20), response_viewport)
    else:
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
    button_text = font.render("Close", True, pygame.Color("white"))
    button_text_rect = button_text.get_rect(center=cancel_button.center)
    screen.blit(button_text, button_text_rect.topleft)

    # Render the animated sprite
    frame = frames[frame_index]
    screen.blit(frame, (20, screen.get_height() - frame.get_height() - 20))

    pygame.display.flip()

# Wrap text to fit within a given width
def wrap_text(text, font, max_width):
    lines = []
    words = text.split(' ')
    while words:
        line_words = []
        while words and font.size(' '.join(line_words + [words[0]]))[0] <= max_width:
            line_words.append(words.pop(0))
        lines.append(' '.join(line_words))
    return lines

# Main function to display the screenshot with an input box and cancel button
def display_screenshot_with_input(filename, sprite_sheet_file, frame_width, frame_height, scale_width, scale_height):
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
    code_font = pygame.font.Font(None, 32)  # Monospaced font for code blocks
    title_font = pygame.font.Font(None, 48)  # Define the font for the title
    title = "Enter your prompt below:"  # Define the title text
    clock = pygame.time.Clock()
    response = ""
    scroll_offset = 0

    # Load the sprite sheet and extract frames
    sprite_sheet = pygame.image.load(sprite_sheet_file).convert_alpha()
    frames = load_frames(sprite_sheet, frame_width, frame_height, scale_width, scale_height)
    frame_index = 0
    frame_timer = 0
    frame_delay = 12  # Adjust the delay to control the animation speed

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            active, text, finished, cancelled, new_response, scroll_offset = handle_event(
                event, input_box, active, text, cancel_button, scroll_offset, response_surf.get_rect() if response else pygame.Rect(0, 0, 0, 0), screen.get_height()
            )
            if finished:
                response = new_response
                # Process the response text, wrapping lines and handling code blocks
                max_width = screen.get_width() - 1000
                lines = response.split('\n')
                wrapped_lines = []
                in_code_block = False
                for line in lines:
                    if line.startswith('```') and not in_code_block:
                        in_code_block = True
                        wrapped_lines.append(line)
                    elif line.startswith('```') and in_code_block:
                        in_code_block = False
                        wrapped_lines.append(line)
                    elif in_code_block:
                        wrapped_lines.append(line)
                    else:
                        wrapped_lines.extend(wrap_text(line, font, max_width))
                line_height = font.size(wrapped_lines[0])[1]
                response_surf_height = len(wrapped_lines) * (line_height + 5)
                response_surf = pygame.Surface((max_width, response_surf_height))
                response_surf.fill((30, 30, 30))
                y_offset = 0
                for line in wrapped_lines:
                    if line.startswith('```'):
                        line_surf = code_font.render(line, True, pygame.Color("white"))
                        pygame.draw.rect(response_surf, pygame.Color("black"), (0, y_offset, max_width, line_surf.get_height() + 5))
                    else:
                        line_surf = font.render(line, True, pygame.Color("white"))
                    response_surf.blit(line_surf, (0, y_offset))
                    y_offset += line_surf.get_height() + 5
                response_surf_rect = response_surf.get_rect()
            if cancelled:
                return False
            # Update the color based on active state
            color = color_active if active else color_inactive

        # Update the animation frame
        frame_timer += 1
        if frame_timer >= frame_delay:
            frame_index = (frame_index + 1) % len(frames)
            frame_timer = 0

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
            response,
            scroll_offset,
            response_surf if response else None,
            response_surf_rect if response else pygame.Rect(0, 0, 0, 0),
            frames,
            frame_index
        )
        clock.tick(30)

# Call the function to run the program
if __name__ == "__main__":
    display_screenshot_with_input(
        "png_files\\screenshots\\box_screenshot.png",
        "png_files\\wizard_things\\wizard_study.png",
        144,
        128,
        288,  # Scaled width
        256   # Scaled height
    )  # Adjust the filename and frame dimensions as needed
